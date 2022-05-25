# Copyright DB Netz AG and the capellambse contributors
# SPDX-License-Identifier: Apache-2.0

# pylint: disable=abstract-method, useless-suppression
# For some reason, pylint in Github CI didn't get the memo that these aren't
# actually abstract methods. Other pylint installations seem to agree that
# implementing these methods isn't necessary. So we just ignore the warning
# about that here.
# TODO Revisit this decision some time in the future

from __future__ import annotations

import collections.abc as cabc
import functools
import hashlib
import io
import itertools
import logging
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import tempfile
import textwrap
import typing as t
import urllib.parse
import weakref

import capellambse.helpers

from .. import modelinfo
from . import FileHandler, TransactionClosedError

LOGGER = logging.getLogger(__name__)


class _TreeEntry(t.NamedTuple):
    mode: str
    type: str
    object: str
    file: str

    @classmethod
    def fromstring(cls, entry: str) -> _TreeEntry:
        info, file = entry.split("\t", maxsplit=1)
        mode, type, object = info.split(" ")
        return cls(mode, type, object, file)

    def tostring(self) -> str:
        return f"{self.mode} {self.type} {self.object}\t{self.file}"


class _ProcessWriter(t.BinaryIO):
    def __init__(
        self,
        command: cabc.Sequence[t.Any],
        *,
        cwd: pathlib.Path,
        env: dict[str, str],
    ) -> None:
        # pylint: disable=consider-using-with
        LOGGER.debug("Spawning process to stream to: %r", command)
        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        assert self.process.stdin is not None
        self.write = self.process.stdin.write  # type: ignore[assignment]

    def write(self, s: bytes) -> int:
        return len(s)  # stub

    def close(self) -> None:
        assert self.process.stdin is not None
        assert self.process.stdout is not None
        if not self.process.stdin.closed:
            self.process.stdin.close()
        if not self.process.stdout.closed:
            self.process.stdout.close()
        self.process.wait()
        assert self.process.returncode is not None
        if self.process.returncode != 0:
            raise RuntimeError(
                f"Subprocess returned error {self.process.returncode}"
            )

    @property
    def closed(self) -> bool:
        assert self.process.stdin is not None
        return self.process.stdin.closed

    def __enter__(self) -> _ProcessWriter:
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.close()


class _WritableIndexFile(_ProcessWriter):
    def __init__(
        self,
        cb: cabc.Callable[[str], None],
        cwd: pathlib.Path,
        env: dict[str, str],
        filename: pathlib.PurePosixPath,
    ) -> None:
        super().__init__(
            ["git", "hash-object", "--path", filename, "--stdin", "-w"],
            cwd=cwd,
            env=env,
        )
        self.callback = cb

    def close(self) -> None:
        assert self.process.stdin is not None
        assert self.process.stdout is not None

        hash, _ = self.process.communicate()
        assert hash
        super().close()
        self.callback(hash.decode("ascii").strip())


class _WritableLFSFile(_ProcessWriter):
    def __init__(
        self,
        cb: cabc.Callable[[str], None],
        cwd: pathlib.Path,
        env: dict[str, str],
        filename: pathlib.PurePosixPath,
    ) -> None:
        super().__init__(
            ["git", "lfs", "clean", "--", filename], cwd=cwd, env=env
        )
        self.__indexfile = _WritableIndexFile(  # type: ignore[abstract]
            cb, cwd, env, filename
        )

    def close(self) -> None:
        assert self.process.stdin is not None
        assert self.process.stdout is not None

        try:
            pointer, _ = self.process.communicate()
            super().close()

            assert pointer
            self.__indexfile.write(pointer)
        finally:
            self.__indexfile.close()


class _GitTransaction:
    __old_sha: str
    __unclosed_error = textwrap.dedent(
        """\
        %d file(s) is/are still opened.

        =======================================================================

        You still have open files when committing a transaction.

        Files that are still open CANNOT be committed and are LOST FOREVER!

        Fix your code to ``close()`` all opened files BEFORE control flows out
        of the ``with:`` block opened by ``write_transaction()``.

        Again: YOU HAVE JUST LOST DATA.

        =======================================================================
        """
    )

    def __init__(
        self,
        outer_transactor: cabc.Callable[..., t.ContextManager],
        filehandler: GitFileHandler,
        /,
        *,
        dry_run: bool = False,
        author_name: str | None = None,
        author_email: str | None = None,
        commit_msg: str = "Changes made with python-capellambse",
        remote_branch: str | None = None,
        push: bool = True,
        push_options: cabc.Sequence[str] | None = None,
        **kw: t.Any,
    ) -> None:
        """Create a transaction that records all changes as a new commit.

        Parameters
        ----------
        author_name
            The name of the commit author.
        author_email
            The e-mail address of the commit author.
        commit_msg
            The commit message.
        dry_run
            If True, stop before updating the ``revision`` pointer. The
            commit will be created, but will not be part of any branch
            or tag.
        remote_branch
            An alternative branch name to push to on the remote, instead
            of pushing back to the same branch.  This is required if
            ``push`` is ``True`` and the ``revision`` that was passed to
            the constructor does not refer to a branch (or looks like a
            git object).

            Note: For convenience, ``refs/heads/`` will be prepended
            automatically to this name if it isn't already present. This
            also means that it is not possible to create tags or other
            types of refs; passing in something like ``refs/tags/v2.4``
            would result in the full ref name
            ``refs/heads/refs/tags/v2.4``.
        push
            Set to ``False`` to inhibit pushing the changes back.
        push_options
            Additional git push options.  See ``--push-option`` in
            ``git-push(1)``. Ignored if ``push`` is ``False``.

        Raises
        ------
        ValueError
            - If a commit hash was used during loading, and no
              ``remote_branch`` was given
            - If the given ``remote_branch`` (or the final part of the
              originally given revision) looks like a git object
        """
        self.__updates: dict[pathlib.PurePosixPath, str] = {}
        self.__outer_context = outer_transactor(**kw)
        self.__handler = filehandler
        self.__dry_run = dry_run
        self.__commit_msg = commit_msg
        self.__push = push
        self.__push_opts = [f"--push-option={i}" for i in push_options or ()]

        self.__gitenv: dict[str, str] = {}
        if author_name:
            self.__gitenv["GIT_AUTHOR_NAME"] = author_name
        if author_email:
            self.__gitenv["GIT_AUTHOR_EMAIL"] = author_email

        targetref = remote_branch or filehandler.revision

        if targetref == "HEAD":
            targetref = self.__resolve_head() or targetref

        if re.search("(^|/)([0-9a-fA-F]{4,}|(.+_)?HEAD)$", targetref):
            raise ValueError(
                f"Target ref looks like a git object, use a different remote_branch: {targetref}"
            )
        if not targetref.startswith("refs/heads/"):
            targetref = "refs/heads/" + targetref

        self.__targetref = targetref
        self.__open_files: cabc.MutableMapping[
            tuple[int, pathlib.PurePosixPath], _ProcessWriter
        ] = weakref.WeakValueDictionary()

    def __enter__(self) -> cabc.Mapping[str, t.Any]:
        self.__updates = {}
        self.__old_sha = (
            self.__handler._git("rev-parse", self.__handler.revision)
            .decode("ascii")
            .strip()
        )
        if self.__handler._transaction is not None:
            raise RuntimeError("Another transaction is already open")
        self.__handler._transaction = self

        return self.__outer_context.__enter__()

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value is not None:
            return self.__outer_context.__exit__(
                exc_type, exc_value, exc_trace
            )
        try:
            LOGGER.debug("Creating updated tree structures")
            tree = self.__update_tree(
                self.__read_tree(self.__old_sha),
                self.__updates,
            )

            LOGGER.debug("Creating commit object with tree %s", tree)
            commit = self.__commit(tree)
            if self.__dry_run:
                LOGGER.debug("Not updating branch pointers (dry_run=True)")
                return None

            LOGGER.debug("Updating ref %r to %s", self.__targetref, commit)
            self.__update_target_ref(commit)

            if not self.__push:
                LOGGER.debug("Not pushing changes to remote (push=False)")
                return None

            LOGGER.debug("Pushing updated ref %r", self.__targetref)
            self.__push_updates("origin")
        finally:
            del self.__old_sha
            self.__handler._transaction = None
            self.__outer_context.__exit__(exc_type, exc_value, exc_trace)
        return None

    def record_update(self, path: pathlib.PurePosixPath, new_sha: str) -> None:
        """Record an updated blob in the current transaction.

        Parameters
        ----------
        path
            The path of the blob, relative to the root of the repository.
        new_sha
            The SHA sum (object name) of the new blob.
        """
        assert re.fullmatch("[0-9a-fA-F]+", new_sha)
        assert self.__handler._transaction is not None
        if path in self.__updates:
            LOGGER.warning(
                "Path changed twice in the same transaction: %s", path
            )
        self.__updates[path] = new_sha

    def record_pending_update(
        self, filename: pathlib.PurePosixPath, file: _ProcessWriter
    ) -> None:
        self.__open_files[id(file), filename] = file

    def __commit(self, tree: str) -> str:
        """Commit ``tree`` as child commit of ``__target_ref``."""
        commit_hash = (
            self.__handler._git(
                "commit-tree",
                tree,
                "-p",
                self.__old_sha,
                "-m",
                self.__commit_msg,
                env=self.__gitenv,
            )
            .strip()
            .decode("ascii")
        )
        LOGGER.debug("Created commit with hash %r", commit_hash)
        return commit_hash

    def __push_updates(self, remote: str) -> None:
        """Push the locally updated ``__target_ref`` to ``remote``."""
        self.__handler._git(
            "-c",
            f"remote.{remote}.mirror=false",
            "push",
            *self.__push_opts,
            "--",
            remote,
            self.__targetref,
        )

    def __read_tree(self, treeish: str) -> dict[str, _TreeEntry]:
        """Read a tree object from git into a dictionary."""
        treedata = self.__handler._git("ls-tree", treeish, "-z")
        tree: dict[str, _TreeEntry] = {}
        for line in treedata.decode("utf-8").split("\0"):
            if line == "":
                continue
            leaf = _TreeEntry.fromstring(line)
            tree[leaf.file] = leaf
        return tree

    def __resolve_head(self) -> str:
        """Resolve HEAD to a single symbolic name."""
        try:
            name = self.__handler._git(
                "rev-parse", "--symbolic-full-name", "HEAD", silent=True
            )
        except subprocess.CalledProcessError:
            name = b""
        return name.decode("utf-8").strip()

    def __update_target_ref(self, commit: str) -> None:
        """Update the local ``__target_ref``."""
        self.__handler._git(
            "update-ref",
            f"-m[{capellambse.__name__}] Commit by capellambse",
            self.__targetref,
            commit,
        )

    def __update_tree(
        self,
        old_tree: cabc.Mapping[str, _TreeEntry],
        updates: cabc.Mapping[pathlib.PurePosixPath, str],
    ) -> str:
        """Apply ``updates`` to ``old_tree`` and create a new tree object."""
        unclosed_files = 0
        for (_, filename), file in self.__open_files.items():
            if not file.closed:
                unclosed_files += 1
                LOGGER.warning("File is still open: %s", filename)
        if unclosed_files:
            LOGGER.critical(self.__unclosed_error, unclosed_files)
        tree = dict(old_tree)

        def groupkey(i: tuple[pathlib.PurePosixPath, str]) -> str:
            if len(i[0].parts) > 1:
                return i[0].parts[0]
            return ""

        for prefix, contents in itertools.groupby(
            sorted(updates.items(), key=groupkey), key=groupkey
        ):
            if not prefix:
                for f, h in contents:
                    tree[f.name] = _TreeEntry("100644", "blob", h, f.name)
            else:
                ent = tree.get(prefix)
                if ent is None or ent.type != "tree":
                    ent = _TreeEntry("040000", "tree", "", prefix)

                new_subtree = self.__update_tree(
                    self.__read_tree(ent.object) if ent.object else {},
                    {k.relative_to(prefix): v for k, v in contents},
                )
                tree[prefix] = ent._replace(object=new_subtree)

        tree_dump = "\0".join(i.tostring() for i in tree.values())
        tree_hash = (
            self.__handler._git(
                "mktree", "-z", input=tree_dump.encode("utf-8")
            )
            .decode("ascii")
            .strip()
        )
        LOGGER.debug("Created tree with hash %r", tree_hash)
        return tree_hash


class GitFileHandler(FileHandler):
    """File handler for ``git://`` and related protocols."""

    username: str
    password: str
    identity_file: str
    known_hosts_file: str
    cache_dir: pathlib.Path

    __fnz: object
    __lfsfiles: frozenset[str]
    __repo: pathlib.Path

    def __init__(
        self,
        path: str | os.PathLike,
        revision: str = "HEAD",
        username: str = "",
        password: str = "",
        identity_file: str = "",
        known_hosts_file: str = "",
        disable_cache: bool = False,
        update_cache: bool = True,
        *,
        subdir: str | pathlib.PurePosixPath = "/",
    ) -> None:
        super().__init__(path, subdir=subdir)
        self.revision = revision
        self.disable_cache = disable_cache
        self.username = username
        self.password = password
        self.identity_file = identity_file
        self.known_hosts_file = known_hosts_file
        self.update_cache = update_cache

        self.__init_cache_dir()
        self.__init_worktree()

        self._transaction: _GitTransaction | None = None
        try:
            self.__lfsfiles = frozenset(
                self._git("lfs", "ls-files", "-n", silent=True)
                .decode("utf-8", errors="surrogateescape")
                .splitlines()
            )
        except subprocess.CalledProcessError:
            LOGGER.debug("LFS not installed, disabling related functionality")
            self.__lfsfiles = frozenset()

    def open(
        self,
        filename: str | pathlib.PurePosixPath,
        mode: t.Literal["r", "rb", "w", "wb"] = "rb",
    ) -> t.BinaryIO:
        path = capellambse.helpers.normalize_pure_path(
            filename, base=self.subdir
        )
        if "w" in mode:
            if self._transaction is None:
                raise TransactionClosedError(
                    "Writing to git requires a transaction"
                )
            return self.__open_writable(path)
        return self.__open_readable(path)

    def __open_readable(self, path: pathlib.PurePosixPath) -> t.BinaryIO:
        try:
            if str(path) in self.__lfsfiles:
                content = self.__open_from_lfs(path)
            else:
                content = self.__open_from_index(path)
        except subprocess.CalledProcessError as err:
            stderr = err.stderr.decode("utf-8")
            if str(path) in stderr.splitlines()[0]:
                raise FileNotFoundError(stderr) from err
            raise
        return io.BytesIO(content)

    def __open_writable(self, path: pathlib.PurePosixPath) -> t.BinaryIO:
        assert self._transaction is not None

        cls: type[_WritableLFSFile] | type[_WritableIndexFile]
        if str(path) in self.__lfsfiles:
            cls = _WritableLFSFile
        else:
            cls = _WritableIndexFile
        file = cls(
            cb=functools.partial(self._transaction.record_update, path),
            cwd=self.cache_dir,
            env=self.__get_git_env(),
            filename=path,
        )
        self._transaction.record_pending_update(path, file)
        return file

    def get_model_info(self) -> modelinfo.ModelInfo:
        def revparse(*args: str) -> str:
            return (
                self._git("rev-parse", *args, silent=True)
                .decode("utf-8", errors="surrogateescape")
                .strip()
            )

        title = str(self.path).rsplit("/", maxsplit=1)[-1]
        if title.endswith(".git"):
            title = title[: -len(".git")]

        return modelinfo.ModelInfo(
            branch=revparse("--abbrev-ref", self.revision),
            title=title,
            url=str(self.path),
            revision=self.revision,
            rev_hash=revparse(self.revision),
        )

    def write_transaction(
        self, **kw: t.Any
    ) -> t.ContextManager[cabc.Mapping[str, t.Any]]:
        """See _GitTransaction for the actual docstring."""
        return _GitTransaction(super().write_transaction, self, **kw)

    write_transaction.__doc__ = _GitTransaction.__init__.__doc__

    @staticmethod
    def __cleanup_worktree(
        repo_root: pathlib.Path, worktree: pathlib.Path, /
    ) -> None:
        LOGGER.debug("Removing worktree at %s", worktree)
        subprocess.run(
            ["git", "worktree", "remove", "-f", str(worktree)],
            check=True,
            cwd=repo_root,
        )

    def __get_git_env(self) -> dict[str, str]:
        git_env = os.environ.copy()
        if not os.environ.get("GIT_ASKPASS"):
            path_to_askpass = (
                pathlib.Path(__file__).parent / "git_askpass.py"
            ).absolute()

            git_env["GIT_ASKPASS"] = str(path_to_askpass)

            try:
                os.chmod(path_to_askpass, 0o755)
            except OSError:
                LOGGER.info(
                    "Setting permission 755 for GIT_ASKPASS file failed"
                )

        if self.username and self.password:
            git_env["GIT_USERNAME"] = self.username
            git_env["GIT_PASSWORD"] = self.password

        if self.identity_file and self.known_hosts_file:
            ssh_command = [
                "ssh",
                "-i",
                self.identity_file,
                f"-oUserKnownHostsFile={self.known_hosts_file}",
            ]
            git_env["GIT_SSH_COMMAND"] = shlex.join(ssh_command)

        return git_env

    def __init_cache_dir(self) -> None:
        if str(self.path).startswith("file://"):
            self.__init_cache_dir_local()
        else:
            self.__init_cache_dir_remote()

    def __init_cache_dir_local(self) -> None:
        parts = urllib.parse.urlparse(str(self.path))
        if parts.netloc and parts.netloc != "localhost":
            raise ValueError(f"Unsupported file:// URL netloc: {parts.netloc}")

        path = pathlib.Path(urllib.parse.unquote(parts.path))
        if isinstance(path, pathlib.WindowsPath):
            path = pathlib.Path(str(path)[1:])
        assert path.is_absolute()
        self.cache_dir = path.resolve()

    def __init_cache_dir_remote(self) -> None:
        slug_pattern = '[\x00-\x1F\x7F"*/:<>?\\|]+'
        path_hash = hashlib.sha256(
            str(self.path).encode("utf-8", errors="surrogatepass")
        ).hexdigest()
        path_slug = re.sub(slug_pattern, "-", str(self.path))
        self.cache_dir = pathlib.Path(
            capellambse.dirs.user_cache_dir,
            "models",
            path_hash,
            path_slug,
        )

        if self.cache_dir.exists() and self.disable_cache:
            shutil.rmtree(str(self.cache_dir))

        if not (self.cache_dir / "config").exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            LOGGER.debug("Cloning %r to %s", self.path, self.cache_dir)
            self._git("clone", self.path, ".", "--bare", "--mirror")
        elif self.update_cache:
            LOGGER.debug("Updating cache at %s", self.cache_dir)
            self._git("fetch")

    def __init_worktree(self) -> None:
        worktree = pathlib.Path(
            tempfile.mkdtemp(None, f"capellambse-{os.getpid()}-")
        )
        LOGGER.debug("Setting up a worktree at %s", worktree)
        try:
            self._git(
                "worktree",
                "add",
                "--detach",
                "--no-checkout",
                worktree,
                self.revision,
                silent=True,
            )
        except:
            os.rmdir(worktree)
            raise
        self.__repo = self.cache_dir
        self.cache_dir = worktree

        self.__fnz = weakref.finalize(  # pylint: disable=unused-private-member
            self, self.__cleanup_worktree, self.__repo, worktree
        )

        self._git("reset", "--mixed", self.revision)

    def __open_from_index(self, filename: pathlib.PurePosixPath) -> bytes:
        return self._git("cat-file", "blob", f"{self.revision}:{filename}")

    def __open_from_lfs(self, filename: pathlib.PurePosixPath) -> bytes:
        lfsinfo = self.__open_from_index(filename)
        return self._git("lfs", "smudge", "--", filename, input=lfsinfo)

    @t.overload
    def _git(
        self,
        *cmd: t.Any,
        encoding: str,
        env: cabc.Mapping[str, str] | None = ...,
        silent: bool = ...,
        **kw: t.Any,
    ) -> str:
        ...

    @t.overload
    def _git(
        self,
        *cmd: t.Any,
        encoding: None = ...,
        env: cabc.Mapping[str, str] | None = ...,
        silent: bool = ...,
        **kw: t.Any,
    ) -> bytes:
        ...

    def _git(
        self,
        *cmd: t.Any,
        env: cabc.Mapping[str, str] | None = None,
        silent: bool = False,
        **kw: t.Any,
    ) -> bytes | str:
        LOGGER.debug("Running command %s", cmd)
        returncode = 0
        stderr = None
        try:
            proc = subprocess.run(
                ["git"] + [str(i) for i in cmd],
                capture_output=True,
                check=True,
                cwd=self.cache_dir,
                env={**self.__get_git_env(), **(env or {})},
                **kw,
            )
            returncode = proc.returncode
            stderr = proc.stderr
            return proc.stdout
        except subprocess.CalledProcessError as err:
            returncode = err.returncode
            stderr = err.stderr
            raise
        finally:
            if silent:
                err_level = ret_level = logging.DEBUG
            elif returncode != 0:
                err_level = ret_level = logging.ERROR
            else:
                err_level = logging.INFO
                ret_level = logging.DEBUG

            if stderr:
                for line in stderr.decode("utf-8").splitlines():
                    LOGGER.getChild("git").log(err_level, "%s", line)
            LOGGER.log(ret_level, "Exit status: %d", returncode)
