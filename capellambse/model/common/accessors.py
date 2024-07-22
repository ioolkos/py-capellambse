# SPDX-FileCopyrightText: Copyright DB InfraGO AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

__all__ = [
    "InvalidModificationError",
    "NonUniqueMemberError",
    "Accessor",
    "Alias",
    "DeprecatedAccessor",
    "WritableAccessor",
    "DirectProxyAccessor",
    "DeepProxyAccessor",
    "LinkAccessor",
    "AttrProxyAccessor",
    "PhysicalLinkEndsAccessor",
    "IndexAccessor",
    "AlternateAccessor",
    "ParentAccessor",
    "CustomAccessor",
    "AttributeMatcherAccessor",
    "SpecificationAccessor",
    "ReferenceSearchingAccessor",
    "ElementListCouplingMixin",
    "RoleTagAccessor",
    "TypecastAccessor",
    "PhysicalAccessor",
]

import abc
import collections.abc as cabc
import contextlib
import itertools
import logging
import operator
import sys
import typing as t
import warnings

import markupsafe
import typing_extensions as te
from lxml import etree

import capellambse
from capellambse import helpers

from . import XTYPE_HANDLERS, S, T, U, build_xtype, element

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

_NOT_SPECIFIED = object()
"Used to detect unspecified optional arguments"

LOGGER = logging.getLogger(__name__)


class InvalidModificationError(RuntimeError):
    """Raised when a modification would result in an invalid model."""


class NonUniqueMemberError(ValueError):
    """Raised when a duplicate member is inserted into a list."""

    parent = property(lambda self: self.args[0])
    attr = property(lambda self: self.args[1])
    target = property(lambda self: self.args[2])

    def __str__(self) -> str:
        if len(self.args) != 3:
            return super().__str__()

        return (
            f"Cannot insert: {self.attr!r} of {self.parent._short_repr_()}"
            f" already contains a reference to {self.target._short_repr_()}"
        )


class _NewObject:
    """A marker class that indicates that a new object should be created.

    This object can be assigned to an attribute of a model object, and
    will be replaced with a new object of the correct type by the
    attribute's accessor.

    In the future, this class will be replaced with a function that
    simply returns a new object of the correct type.
    """

    def __init__(self, /, *type_hint: str, **kw: t.Any) -> None:
        self._type_hint = type_hint
        self._kw = kw

    def __repr__(self) -> str:
        kw = ", ".join(f"{k}={v!r}" for k, v in self._kw.items())
        return f"<new object {self._type_hint!r} ({kw})>"


class Accessor(t.Generic[T], metaclass=abc.ABCMeta):
    """Super class for all Accessor types."""

    __objclass__: type[t.Any]
    __name__: str

    def __init__(self) -> None:
        super().__init__()
        self.__doc__ = (
            f"A {type(self).__name__} that was not properly configured."
            " Ensure that ``__set_name__`` gets called after construction."
        )

    @t.overload
    def __get__(self, obj: None, objtype: type[t.Any]) -> te.Self: ...
    @t.overload
    def __get__(
        self, obj: element.ModelObject, objtype: type[t.Any] | None = ...
    ) -> T | element.ElementList[T]: ...
    @abc.abstractmethod
    def __get__(
        self,
        obj: element.ModelObject | None,
        objtype: type[t.Any] | None = None,
    ) -> te.Self | T | element.ElementList[T]:
        pass

    def __set__(self, obj: element.ModelObject, value: t.Any) -> None:
        raise TypeError("Cannot set this type of attribute")

    def __delete__(self, obj: element.ModelObject) -> None:
        raise TypeError("Cannot delete this type of attribute")

    def __set_name__(self, owner: type[t.Any], name: str) -> None:
        self.__objclass__ = owner
        self.__name__ = name
        friendly_name = name.replace("_", " ")
        self.__doc__ = f"The {friendly_name} of this {owner.__name__}."

    def __repr__(self) -> str:
        return f"<{self._qualname!r} {type(self).__name__}>"

    @property
    def _qualname(self) -> str:
        """Generate the qualified name of this descriptor."""
        if not hasattr(self, "__objclass__"):
            return f"(unknown {type(self).__name__} - call __set_name__)"
        return f"{self.__objclass__.__name__}.{self.__name__}"


class Alias(Accessor[T]):
    """Provides an alias to another attribute.

    Parameters
    ----------
    target
        The target to redirect to.
    dirhide
        If True, hide this alias from `dir()` calls.
    """

    __slots__ = ("dirhide", "target")

    def __init__(self, target: str, /, *, dirhide: bool = True) -> None:
        if "." in target:
            raise ValueError(f"Unsupported alias target: {target!r}")

        super().__init__()
        self.target = target
        self.dirhide = dirhide

    @t.overload
    def __get__(self, obj: None, objtype: type[t.Any]) -> te.Self: ...
    @t.overload
    def __get__(
        self,
        obj: element.ModelObject,
        objtype: type[t.Any] | None = ...,
    ) -> T | element.ElementList[T]: ...
    def __get__(
        self,
        obj: element.ModelObject | None,
        objtype: type[t.Any] | None = None,
    ) -> te.Self | T | element.ElementList[T]:
        if obj is None:
            return self
        return getattr(obj, self.target)

    def __set__(self, obj: element.ModelObject, value: t.Any) -> None:
        setattr(obj, self.target, value)

    def __delete__(self, obj: element.ModelObject) -> None:
        delattr(obj, self.target)


class DeprecatedAccessor(Accessor[T]):
    """Provides a deprecated alias to another attribute."""

    __slots__ = ("alternative",)

    def __init__(self, alternative: str, /) -> None:
        super().__init__()
        self.alternative = alternative

    @t.overload
    def __get__(self, obj: None, objtype: type[t.Any]) -> te.Self: ...
    @t.overload
    def __get__(
        self,
        obj: element.ModelObject,
        objtype: type[t.Any] | None = ...,
    ) -> T | element.ElementList[T]: ...
    def __get__(
        self,
        obj: element.ModelObject | None,
        objtype: type[t.Any] | None = None,
    ) -> te.Self | T | element.ElementList[T]:
        if obj is None:
            return self

        self.__warn()
        return getattr(obj, self.alternative)

    def __set__(self, obj: element.ModelObject, value: t.Any) -> None:
        self.__warn()
        setattr(obj, self.alternative, value)

    def __delete__(self, obj: element.ModelObject) -> None:
        self.__warn()
        delattr(obj, self.alternative)

    def __warn(self) -> None:
        msg = f"{self._qualname} is deprecated, use {self.alternative} instead"
        warnings.warn(msg, FutureWarning, stacklevel=3)


class WritableAccessor(Accessor[T], metaclass=abc.ABCMeta):
    """An Accessor that also provides write support on lists it returns."""

    aslist: type[ElementListCouplingMixin] | None
    class_: type[T]
    list_extra_args: cabc.Mapping[str, t.Any]
    single_attr: str | None

    def __init__(
        self,
        *args: t.Any,
        aslist: type[element.ElementList] | None,
        single_attr: str | None = None,
        **kw: t.Any,
    ) -> None:
        super().__init__(*args, **kw)
        self.single_attr = single_attr
        if aslist is not None:
            self.aslist = type(
                "Coupled" + aslist.__name__,
                (ElementListCouplingMixin, aslist),
                {"_accessor": self},
            )
            self.aslist.__module__ = __name__
        else:
            self.aslist = None

    def __set__(
        self,
        obj: element.ModelObject,
        value: T | _NewObject | cabc.Iterable[T | _NewObject],
    ) -> None:
        raise TypeError("Cannot set this type of attribute")

    def create(
        self,
        elmlist: ElementListCouplingMixin,
        /,
        *type_hints: str | None,
        **kw: t.Any,
    ) -> T:
        """Create and return a new element of type ``elmclass``.

        Parameters
        ----------
        elmlist
            The (coupled)
            :py:class:`~capellambse.model.common.element.ElementList` to
            insert the new object into.
        type_hints
            Hints for finding the correct type of element to create. Can
            either be a full or shortened ``xsi:type`` string, or an
            abbreviation defined by the specific Accessor instance.
        kw
            Initialize the properties of the new object. Depending on
            the object's type, some attributes may be required.
        """
        raise TypeError("Cannot create objects")

    def create_singleattr(
        self, elmlist: ElementListCouplingMixin, arg: t.Any, /
    ) -> T:
        """Create an element that only has a single attribute of interest."""
        if self.single_attr is None:
            raise TypeError(
                "Cannot create object from string, a dictionary is required"
            )
        return self.create(elmlist, **{self.single_attr: arg})

    def insert(
        self,
        elmlist: ElementListCouplingMixin,
        index: int,
        value: element.ModelObject | _NewObject,
    ) -> None:
        """Insert the ``value`` object into the model.

        The object must be inserted at an appropriate place, so that, if
        ``elmlist`` were to be created afresh, ``value`` would show up
        at index ``index``.
        """
        raise NotImplementedError("Objects cannot be inserted into this list")

    def delete(
        self,
        elmlist: ElementListCouplingMixin,
        obj: element.ModelObject,
    ) -> None:
        """Delete the ``obj`` from the model."""
        raise NotImplementedError("Objects in this list cannot be deleted")

    def _create(
        self,
        parent: element.ModelObject,
        xmltag: str | None,
        /,
        *type_hints: str | None,
        **kw: t.Any,
    ) -> T:
        if type_hints:
            elmclass, kw["xtype"] = self._match_xtype(*type_hints)
        else:
            elmclass, kw["xtype"] = self._guess_xtype()
        assert elmclass is not None

        want_id: str | None = None
        if "uuid" in kw:
            want_id = kw.pop("uuid")

        pelem = parent._element
        with parent._model._loader.new_uuid(pelem, want=want_id) as obj_id:
            obj = elmclass(parent._model, pelem, xmltag, uuid=obj_id, **kw)
        return obj

    def _make_list(self, parent_obj, elements):
        assert hasattr(self, "class_")
        assert hasattr(self, "list_extra_args")
        if self.aslist is None:
            return no_list(self, parent_obj._model, elements, self.class_)
        return self.aslist(
            parent_obj._model,
            elements,
            self.class_,
            parent=parent_obj,
            **self.list_extra_args,
        )

    def _match_xtype(
        self,
        type_1: str | None,
        type_2: str | object = _NOT_SPECIFIED,
        /,
    ) -> tuple[type[T], str]:
        r"""Find the right class for the given ``xsi:type``\ (s)."""

        def match_xt(xtp: S, itr: cabc.Iterable[S]) -> S:
            matches: list[S] = []
            for i in itr:
                if (
                    xtp is i is None
                    or i is not None
                    and xtp == i
                    or xtp == i.split(":")[-1]  # type: ignore[union-attr]
                ):
                    matches.append(i)
            if not matches:
                raise ValueError(f"Invalid or unknown xsi:type {xtp!r}")
            if len(matches) > 1:
                raise ValueError(
                    f"Ambiguous xsi:type {xtp!r}, please qualify: "
                    + ", ".join(repr(i) for i in matches)
                )
            return matches[0]

        if not isinstance(type_1, str):
            raise TypeError(
                f"Expected str as first type, got {type(type_1).__name__!r}"
            )
        candidate_classes: dict[str, type[T]]
        if type_2 is _NOT_SPECIFIED:
            candidate_classes = dict(
                itertools.chain.from_iterable(
                    i.items() for i in XTYPE_HANDLERS.values()
                )
            )
            objtype = type_1
        elif not isinstance(type_2, str):
            raise TypeError(
                f"Expected a str objtype, not {type(type_2).__name__}"
            )
        else:
            candidate_classes = XTYPE_HANDLERS[
                match_xt(type_1, XTYPE_HANDLERS)
            ]
            objtype = type_2

        objtype = match_xt(objtype, candidate_classes)
        return candidate_classes[objtype], objtype

    def _guess_xtype(self) -> tuple[type[T], str]:
        try:
            super_guess = super()._guess_xtype  # type: ignore[misc]
        except AttributeError:
            pass
        else:
            return super_guess()
        raise TypeError(f"{self._qualname} requires a type hint")

    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> contextlib.AbstractContextManager[None]:
        """Purge references to the given object from the model.

        This method is called while deleting physical objects, in order
        to get rid of references to that object (and its descendants).
        Reference purging is done in two steps, which is why this method
        returns a context manager.

        The first step, executed by the ``__enter__`` method, collects
        references to the target and ensures that deleting them would
        result in a valid model. If any validity constraints would be
        violated, an exception is raised to indicate as such, and the
        whole operation is aborted.

        Once all ``__enter__`` methods have been called, the target
        object is deleted from the model. Then all ``__exit__`` methods
        are called, which triggers the actual deletion of all previously
        discovered references.

        As per the context manager protocol, ``__exit__`` will always be
        called after ``__enter__``, even if the operation is to be
        aborted. The ``__exit__`` method must therefore inspect whether
        an exception was passed in or not in order to know whether the
        operation succeeded.

        In order to not confuse other context managers and keep the
        model consistent, ``__exit__`` must not raise any further
        exceptions. Exceptions should instead be logged to stderr, for
        example by using the :py:meth:`logging.Logger.exception`
        facility.

        The ``purge_references`` method will only be called for Accessor
        instances that actually contain a reference.

        Parameters
        ----------
        obj
            The model object to purge references from.
        target
            The object that is to be deleted; references to this object
            will be purged.

        Returns
        -------
        contextlib.AbstractContextManager
            A context manager that deals with purging references in a
            transactional manner.

        Raises
        ------
        InvalidModificationError
            Raised by the returned context manager's ``__enter__``
            method if the attempted modification would result in an
            invalid model. Note that it is generally preferred to allow
            the operation and take the necessary steps to keep the model
            consistent, if possible. This can be achieved for example by
            deleting dependent objects along with the original deletion
            target.
        Exception
            Any exception may be raised before ``__enter__`` returns in
            order to abort the transaction and prevent the ``obj`` from
            being deleted. No exceptions must be raised by ``__exit__``.

        Examples
        --------
        A simple implementation for purging a single object reference
        could look like this:

        .. code-block:: python

           @contextlib.contextmanager
           def purge_references(self, obj, target):
               assert self.__get__(obj, type(obj)) == target

               yield

               try:
                   self.__delete__(obj)
               except Exception:
                   LOGGER.exception("Could not purge a dangling reference")
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not support purging references"
        )


class PhysicalAccessor(Accessor[T]):
    """Helper super class for accessors that work with real elements."""

    __slots__ = (
        "aslist",
        "class_",
        "list_extra_args",
        "xtypes",
    )

    aslist: type[element.ElementList] | None
    class_: type[T]
    list_extra_args: cabc.Mapping[str, t.Any]
    xtypes: cabc.Set[str]

    def __init__(
        self,
        class_: type[T],
        xtypes: (
            str
            | type[element.ModelObject]
            | cabc.Iterable[str | type[element.ModelObject]]
            | None
        ) = None,
        *,
        aslist: type[element.ElementList[T]] | None = None,
        mapkey: str | None = None,
        mapvalue: str | None = None,
        fixed_length: int = 0,
        list_extra_args: cabc.Mapping[str, t.Any] | None = None,
    ) -> None:
        super().__init__()
        if xtypes is None:
            self.xtypes = (
                {build_xtype(class_)}
                if class_ is not element.GenericElement
                else set()
            )
        elif isinstance(xtypes, type):
            assert issubclass(xtypes, element.GenericElement)
            self.xtypes = {build_xtype(xtypes)}
        elif isinstance(xtypes, str):
            self.xtypes = {xtypes}
        else:
            self.xtypes = {
                i if isinstance(i, str) else build_xtype(i) for i in xtypes
            }

        self.aslist = aslist
        self.class_ = class_
        self.list_extra_args = {}
        if list_extra_args is not None:
            warnings.warn(
                (
                    "list_extra_args is deprecated,"
                    " pass mapkey and/or mapvalue directly instead"
                ),
                DeprecationWarning,
            )
            self.list_extra_args.update(list_extra_args)
        if mapkey is not None:
            self.list_extra_args["mapkey"] = mapkey
        if mapvalue is not None:
            self.list_extra_args["mapvalue"] = mapvalue
        if fixed_length > 0:
            self.list_extra_args["fixed_length"] = fixed_length
        elif fixed_length < 0:
            raise ValueError("List length cannot be negative")

    def _guess_xtype(self) -> tuple[type[T], str]:
        """Try to guess the type of element that should be created."""
        if self.class_ is element.GenericElement or self.class_ is None:
            raise ValueError("Multiple object types that can be created")
        if not self.xtypes:
            raise ValueError("No matching `xsi:type` found")
        if len(self.xtypes) > 1:
            raise ValueError("Multiple matching `xsi:type`s")
        return self.class_, next(iter(self.xtypes))

    def _make_list(self, parent_obj, elements):
        if self.aslist is None:
            return no_list(self, parent_obj._model, elements, self.class_)
        return self.aslist(
            parent_obj._model,
            elements,
            self.class_,
            **self.list_extra_args,
        )


class DirectProxyAccessor(WritableAccessor[T], PhysicalAccessor[T]):
    """Creates proxy objects on the fly."""

    __slots__ = ("follow_abstract", "rootelem")

    aslist: type[ElementListCouplingMixin] | None
    class_: type[T]
    single_attr: str | None

    def __init__(
        self,
        class_: type[T],
        xtypes: str | type[T] | cabc.Iterable[str | type[T]] | None = None,
        *,
        aslist: type[element.ElementList] | None = None,
        mapkey: str | None = None,
        mapvalue: str | None = None,
        fixed_length: int = 0,
        follow_abstract: bool = False,
        list_extra_args: dict[str, t.Any] | None = None,
        rootelem: (
            str
            | type[element.GenericElement]
            | cabc.Sequence[str | type[element.GenericElement]]
            | None
        ) = None,
        single_attr: str | None = None,
    ):
        r"""Create a DirectProxyAccessor.

        Parameters
        ----------
        class_
            The proxy class.
        xtypes
            The ``xsi:type``\ (s) of the child element(s). If None, then
            the constructed proxy will be passed the original element
            instead of a child.
        aslist
            If None, only a single element must match, which will be
            returned directly. If not None, must be a subclass of
            :class:`~capellambse.model.common.element.ElementList`,
            which will be used to return a list of all matched objects.
        mapkey
            Specify the attribute to look up when the returned list is
            indexed with a str. If not specified, str indexing is not
            possible.

            Ignored if *aslist* is not specified.
        mapvalue
            If specified, return this attribute of the found object when
            using str indices into the returned list. If not specified,
            the found object itself is returned.

            Ignored if *aslist* is not specified.
        fixed_length
            When non-zero, the returned list will try to stay at exactly
            this length, by not allowing to insert or delete beyond this
            many members.

            Ignored if *aslist* is not specified.
        follow_abstract
            Follow the link in the ``abstractType`` XML attribute of
            each list member and instantiate that object instead. The
            default is to instantiate the child elements directly.
        list_extra_args
            Extra arguments to pass to the
            :class:`~capellambse.model.common.element.ElementList`
            constructor.

            .. deprecated: 0.5.68

               Use 'mapkey', 'mapvalue' and 'fixed_length' directly
               instead.
        rootelem
            A class or ``xsi:type`` (or list thereof) that defines the
            path from the current object's XML element to the search
            root. If None, the current element will be used directly.
        single_attr
            If objects can be created with only a single attribute
            specified, this argument is the name of that attribute. This
            :meth:`~capellambse.model.common.accessors\
            .WritableAccessor.create_singleattr`.
        """
        super().__init__(
            class_,
            xtypes,
            aslist=aslist,
            list_extra_args=list_extra_args,
            mapkey=mapkey,
            mapvalue=mapvalue,
            fixed_length=fixed_length,
            single_attr=single_attr,
        )
        self.follow_abstract: bool = follow_abstract
        if rootelem is None:
            self.rootelem: cabc.Sequence[str] = []
        elif isinstance(rootelem, str):
            self.rootelem = rootelem.split("/")
        elif isinstance(rootelem, type) and issubclass(
            rootelem, element.GenericElement
        ):
            self.rootelem = [build_xtype(rootelem)]
        else:
            self.rootelem = [
                i if isinstance(i, str) else build_xtype(i) for i in rootelem
            ]

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        elems = [
            self._resolve(obj, e)
            for e in self._getsubelems(obj)
            if e.get("id") is not None
        ]
        return self._make_list(obj, elems)

    def __set__(
        self,
        obj: element.ModelObject,
        value: str | T | _NewObject | cabc.Iterable[str | T | _NewObject],
    ) -> None:
        if self.aslist:
            if isinstance(value, str) or not isinstance(value, cabc.Iterable):
                raise TypeError("Can only set list attribute to an iterable")
            list = self.__get__(obj)
            for v in list:
                self.delete(list, v)
            for i, v in enumerate(value):
                if isinstance(v, str):
                    self.create_singleattr(list, v)
                else:
                    self.insert(list, i, v)
        else:
            if isinstance(value, cabc.Iterable) and not isinstance(value, str):
                raise TypeError("Cannot set non-list attribute to an iterable")
            if not isinstance(value, _NewObject):
                raise NotImplementedError(
                    "Moving model objects is not supported yet"
                )
            if self.__get__(obj) is not None:
                raise NotImplementedError(
                    "Replacing model objects is not supported yet"
                )
            self._create(obj, None, *value._type_hint, **value._kw)

    def __delete__(self, obj: element.ModelObject) -> None:
        if self.rootelem:
            raise TypeError("Cannot delete due to 'rootelem' being set")
        if self.follow_abstract:
            raise TypeError("Cannot delete when following abstract types")

        if self.aslist is not None:
            self._delete(obj._model, list(self._getsubelems(obj)))
        else:
            raise TypeError(f"Cannot delete {self._qualname}")

    def _delete(
        self, model: capellambse.MelodyModel, elements: list[etree._Element]
    ) -> None:
        all_elements = (
            list(
                itertools.chain.from_iterable(
                    model._loader.iterdescendants_xt(i) for i in elements
                )
            )
            + elements
        )
        with contextlib.ExitStack() as stack:
            for elm in all_elements:
                if elm.get("id") is None:
                    continue

                obj = element.GenericElement.from_model(model, elm)
                for ref, attr, _ in model.find_references(obj):
                    acc = getattr(type(ref), attr)
                    if acc is self or not isinstance(acc, WritableAccessor):
                        continue
                    stack.enter_context(acc.purge_references(ref, obj))

            for elm in elements:
                parent = elm.getparent()
                assert parent is not None
                model._loader.idcache_remove(elm)
                parent.remove(elm)

    def _resolve(
        self, obj: element.ModelObject, elem: etree._Element
    ) -> etree._Element:
        if self.follow_abstract:
            if abstype := elem.get("abstractType"):
                elem = obj._model._loader[abstype]
            else:
                raise RuntimeError("Broken XML: No abstractType defined?")
        return elem

    def _getsubelems(
        self, obj: element.ModelObject
    ) -> cabc.Iterator[etree._Element]:
        return itertools.chain.from_iterable(
            obj._model._loader.iterchildren_xt(i, *iter(self.xtypes))
            for i in self._findroots(obj)
        )

    def _findroots(self, obj: element.ModelObject) -> list[etree._Element]:
        roots = [obj._element]
        for xtype in self.rootelem:
            roots = list(
                itertools.chain.from_iterable(
                    obj._model._loader.iterchildren_xt(i, xtype) for i in roots
                )
            )
        return roots

    def create(
        self,
        elmlist: ElementListCouplingMixin,
        /,
        *type_hints: str | None,
        **kw: t.Any,
    ) -> T:
        if self.rootelem:
            raise TypeError("Cannot create objects here")

        return self._create(elmlist._parent, None, *type_hints, **kw)

    def insert(
        self,
        elmlist: ElementListCouplingMixin,
        index: int,
        value: element.ModelObject | _NewObject,
    ) -> None:
        if isinstance(value, _NewObject):
            raise NotImplementedError(
                "Creating new objects in lists with new_object() is not"
                " supported yet"
            )

        if value._model is not elmlist._model:
            raise ValueError("Cannot move elements between models")
        try:
            indexof = elmlist._parent._element.index
            if index > 0:
                parent_index = indexof(elmlist._elements[index - 1]) + 1
            elif index < -1:
                parent_index = indexof(elmlist._elements[index + 1]) - 1
            else:
                parent_index = index
        except ValueError:
            parent_index = len(elmlist._parent._element)
        elmlist._parent._element.insert(parent_index, value._element)
        elmlist._model._loader.idcache_index(value._element)

    def delete(
        self,
        elmlist: ElementListCouplingMixin,
        obj: element.ModelObject,
    ) -> None:
        assert obj._model is elmlist._model
        self._delete(obj._model, [obj._element])

    @contextlib.contextmanager
    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> cabc.Iterator[None]:
        yield


class DeepProxyAccessor(DirectProxyAccessor[T]):
    """A DirectProxyAccessor that searches recursively through the tree."""

    __slots__ = ()

    def _getsubelems(
        self, obj: element.ModelObject
    ) -> cabc.Iterator[etree._Element]:
        return itertools.chain.from_iterable(
            obj._model._loader.iterdescendants_xt(i, *iter(self.xtypes))
            for i in self._findroots(obj)
        )


class LinkAccessor(WritableAccessor[T], PhysicalAccessor[T]):
    """Accesses elements through reference elements."""

    __slots__ = ("backattr", "tag", "unique")

    aslist: type[ElementListCouplingMixin] | None
    backattr: str | None
    class_: type[T]
    tag: str | None

    def __init__(
        self,
        tag: str | None,
        xtype: str | type[element.GenericElement],
        /,
        *,
        aslist: type[element.ElementList] | None = None,
        mapkey: str | None = None,
        mapvalue: str | None = None,
        attr: str,
        backattr: str | None = None,
        unique: bool = True,
    ) -> None:
        """Create a LinkAccessor.

        Parameters
        ----------
        tag
            The XML tag that the reference elements will have.
        xtype
            The ``xsi:type`` that the reference elements will have. This
            has no influence on the elements that are referenced.
        attr
            The attribute on the reference element that contains the
            actual link.
        backattr
            An optional attribute on the reference element to store a
            reference back to the owner (parent) object.
        aslist
            Optionally specify a different subclass of
            :class:`~capellambse.model.common.element.ElementList`.
        mapkey
            Specify the attribute to look up when the returned list is
            indexed with a str. If not specified, str indexing is not
            possible.

            Ignored if *aslist* is not specified.
        mapvalue
            If specified, return this attribute of the found object when
            using str indices into the returned list. If not specified,
            the found object itself is returned.

            Ignored if *aslist* is not specified.
        unique
            Enforce that each element may only appear once in the list.
            If a duplicate is attempted to be added, an exception will
            be raised. Note that this does not have an effect on lists
            already existing within the loaded model.
        """
        if not tag:
            warnings.warn(
                "Unspecified XML tag is deprecated",
                DeprecationWarning,
                stacklevel=2,
            )
        elif not isinstance(tag, str):
            raise TypeError(f"tag must be a str, not {type(tag).__name__}")
        super().__init__(
            element.GenericElement,
            xtype,
            aslist=aslist,
            mapkey=mapkey,
            mapvalue=mapvalue,
        )
        if len(self.xtypes) != 1:
            raise TypeError(f"One xtype is required, got {len(self.xtypes)}")
        self.follow = attr
        self.backattr = backattr
        self.tag = tag
        self.unique = unique

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        elems: list[etree._Element] = []
        seen: set[etree._Element] = set()
        for i in self.__find_refs(obj):
            e = self.__follow_ref(obj, i)
            if e is None:
                continue
            if e not in seen:
                elems.append(e)
                seen.add(e)
        return self._make_list(obj, elems)

    def __set__(self, obj: element.ModelObject, value: t.Any) -> None:
        if self.aslist is None:
            if isinstance(value, cabc.Iterable) and not isinstance(value, str):
                raise TypeError(f"{self._qualname} expects a single element")
            value = (value,)
        elif isinstance(value, str) or not isinstance(value, cabc.Iterable):
            raise TypeError(f"{self._qualname} expects an iterable")
        if self.tag is None:
            raise NotImplementedError("Cannot set: XML tag not set")

        self.__delete__(obj)
        for v in value:
            self.__create_link(obj, v)

    def __delete__(self, obj: element.ModelObject) -> None:
        refobjs = list(self.__find_refs(obj))
        for i in refobjs:
            obj._model._loader.idcache_remove(i)
            obj._element.remove(i)

    def __follow_ref(
        self, obj: element.ModelObject, refelm: etree._Element
    ) -> etree._Element | None:
        link = refelm.get(self.follow)
        if not link:
            return None
        return obj._model._loader.follow_link(obj._element, link)

    def __find_refs(
        self, obj: element.ModelObject
    ) -> cabc.Iterator[etree._Element]:
        for refelm in obj._element.iterchildren(tag=self.tag):
            if helpers.xtype_of(refelm) in self.xtypes:
                yield refelm

    def __backref(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> etree._Element | None:
        for i in self.__find_refs(obj):
            if self.__follow_ref(obj, i) == target._element:
                return i
        return None

    def __create_link(
        self,
        parent: element.ModelObject,
        target: element.ModelObject,
        *,
        before: element.ModelObject | None = None,
    ) -> etree._Element:
        assert self.tag is not None
        loader = parent._model._loader

        if self.unique:
            for i in self.__find_refs(parent):
                if self.__follow_ref(parent, i) is target._element:
                    raise NonUniqueMemberError(parent, self.__name__, target)

        with loader.new_uuid(parent._element) as obj_id:
            (xtype,) = self.xtypes
            link = loader.create_link(parent._element, target._element)
            refobj = parent._element.makeelement(
                self.tag,
                {helpers.ATT_XT: xtype, "id": obj_id, self.follow: link},
            )
            if self.backattr and (parent_id := parent._element.get("id")):
                refobj.set(self.backattr, f"#{parent_id}")
            if before is None:
                parent._element.append(refobj)
            else:
                before_elm = self.__backref(parent, before)
                assert before_elm is not None
                assert before_elm in parent._element
                before_elm.addprevious(refobj)
            loader.idcache_index(refobj)
        return refobj

    def insert(
        self,
        elmlist: ElementListCouplingMixin,
        index: int,
        value: element.ModelObject | _NewObject,
    ) -> None:
        if self.aslist is None:
            raise TypeError("Cannot insert: This is not a list (bug?)")
        if self.tag is None:
            raise NotImplementedError("Cannot insert: XML tag not set")
        if isinstance(value, _NewObject):
            raise NotImplementedError("Cannot insert new objects yet")

        self.__create_link(
            elmlist._parent,
            value,
            before=elmlist[index] if index < len(elmlist) else None,
        )

    def delete(
        self,
        elmlist: ElementListCouplingMixin,
        obj: element.ModelObject,
    ) -> None:
        if self.aslist is None:
            raise TypeError("Cannot delete: This is not a list (bug?)")

        parent = elmlist._parent
        for ref in self.__find_refs(parent):
            if self.__follow_ref(parent, ref) == obj._element:
                parent._model._loader.idcache_remove(ref)
                parent._element.remove(ref)
                break
        else:
            raise ValueError("Cannot delete: Target object not in this list")

    @contextlib.contextmanager
    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> cabc.Generator[None, None, None]:
        purge: list[etree._Element] = []
        for ref in self.__find_refs(obj):
            if self.__follow_ref(obj, ref) is target._element:
                purge.append(ref)

        yield

        for ref in purge:
            try:
                parent = ref.getparent()
                if parent is None:
                    continue
                parent.remove(ref)
            except Exception:
                LOGGER.exception("Cannot purge dangling ref object %r", ref)


class AttrProxyAccessor(WritableAccessor[T], PhysicalAccessor[T]):
    """Provides access to elements that are linked in an attribute."""

    __slots__ = ("attr",)

    aslist: type[ElementListCouplingMixin] | None
    class_: type[T]

    def __init__(
        self,
        class_: type[T] | None,
        attr: str,
        *,
        aslist: type[element.ElementList] | None = None,
        mapkey: str | None = None,
        mapvalue: str | None = None,
        list_extra_args: cabc.Mapping[str, t.Any] | None = None,
    ):
        """Create an AttrProxyAccessor.

        Parameters
        ----------
        class_
            The proxy class. Currently only used for type hints.
        attr
            The XML attribute to handle.
        aslist
            If None, the attribute contains at most one element
            reference, and either None or the constructed proxy will be
            returned. If not None, must be a subclass of
            :class:`~capellambse.model.common.element.ElementList`. It
            will be used to return a list of all matched objects.
        mapkey
            Specify the attribute to look up when the returned list is
            indexed with a str. If not specified, str indexing is not
            possible.

            Ignored if *aslist* is not specified.
        mapvalue
            If specified, return this attribute of the found object when
            using str indices into the returned list. If not specified,
            the found object itself is returned.

            Ignored if *aslist* is not specified.
        list_extra_args
            Extra arguments to pass to the
            :class:`~capellambse.model.common.element.ElementList`
            constructor.

            .. deprecated: 0.5.68

               Use 'mapkey' and 'mapvalue' directly instead.
        """
        del class_
        super().__init__(
            element.GenericElement,
            aslist=aslist,
            list_extra_args=list_extra_args,
            mapkey=mapkey,
            mapvalue=mapvalue,
        )
        self.attr = attr

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        elems = obj._model._loader.follow_links(
            obj._element, obj._element.get(self.attr, "")
        )

        return self._make_list(obj, elems)

    def __set__(
        self,
        obj: element.ModelObject,
        values: T | _NewObject | cabc.Iterable[T | _NewObject],
    ) -> None:
        if not isinstance(values, cabc.Iterable):
            values = (values,)
        elif self.aslist is None:
            raise TypeError(
                f"{self._qualname} requires a single item, not an iterable"
            )

        if any(isinstance(i, _NewObject) for i in values):
            raise NotImplementedError("Cannot create new objects here")

        assert isinstance(values, cabc.Iterable)
        self.__set_links(obj, values)  # type: ignore[arg-type]

    def __delete__(self, obj: element.ModelObject) -> None:
        del obj._element.attrib[self.attr]

    def insert(
        self,
        elmlist: ElementListCouplingMixin,
        index: int,
        value: element.ModelObject | _NewObject,
    ) -> None:
        assert self.aslist is not None
        if isinstance(value, _NewObject):
            raise NotImplementedError("Cannot insert new objects yet")
        if value._model is not elmlist._parent._model:
            raise ValueError("Cannot insert elements from different models")
        objs = [*elmlist[:index], value, *elmlist[index:]]
        self.__set_links(elmlist._parent, objs)

    def delete(
        self, elmlist: ElementListCouplingMixin, obj: element.ModelObject
    ) -> None:
        assert self.aslist is not None
        objs = [i for i in elmlist if i != obj]
        self.__set_links(elmlist._parent, objs)

    def __set_links(
        self, obj: element.ModelObject, values: cabc.Iterable[T]
    ) -> None:
        parts: list[str] = []
        for value in values:
            if value._model is not obj._model:
                raise ValueError(
                    "Cannot insert elements from different models"
                )
            link = obj._model._loader.create_link(obj._element, value._element)
            parts.append(link)
        obj._element.set(self.attr, " ".join(parts))

    @contextlib.contextmanager
    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> cabc.Generator[None, None, None]:
        # pylint: disable=unnecessary-dunder-call
        yield

        if self.aslist is not None:
            try:
                elt = obj._element
                links = obj._model._loader.follow_links(
                    elt, elt.get(self.attr, ""), ignore_broken=True
                )
                remaining_links = [
                    link for link in links if link is not target._element
                ]
                self.__set_links(obj, self._make_list(obj, remaining_links))
            except Exception:
                LOGGER.exception("Cannot write new list of targets")
        else:
            try:
                del obj._element.attrib[self.attr]
            except KeyError:
                pass
            except Exception:
                LOGGER.exception("Cannot update link target")


class PhysicalLinkEndsAccessor(AttrProxyAccessor[T]):
    def __init__(
        self,
        class_: type[T],
        attr: str,
        *,
        aslist: type[element.ElementList],
        mapkey: str | None = None,
        mapvalue: str | None = None,
    ) -> None:
        super().__init__(
            class_,
            attr,
            aslist=aslist,
            list_extra_args={"fixed_length": 2},
            mapkey=mapkey,
            mapvalue=mapvalue,
        )
        assert self.aslist is not None

    @contextlib.contextmanager
    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> cabc.Generator[None, None, None]:
        # TODO This should instead delete the link
        raise NotImplementedError("Cannot purge references from PhysicalLink")


class IndexAccessor(Accessor[T]):
    """Access a specific index in an ElementList of a fixed size."""

    __slots__ = ("index", "wrapped")

    def __init__(self, wrapped: str, index: int) -> None:
        super().__init__()
        self.index = index
        self.wrapped = wrapped

    @t.overload
    def __get__(self, obj: None, objtype=None) -> te.Self: ...
    @t.overload
    def __get__(self, obj, objtype=None) -> T | element.ElementList[T]: ...
    def __get__(
        self,
        obj: element.ModelObject | None,
        objtype: type[t.Any] | None = None,
    ) -> te.Self | T | element.ElementList[T]:
        if obj is None:
            return self
        container = getattr(obj, self.wrapped)
        if not isinstance(container, element.ElementList):
            raise RuntimeError(
                f"Cannot get {self._qualname}: {self.wrapped} is not a list"
            )
        if len(container) <= self.index:
            raise RuntimeError(
                f"Broken XML: Expected at least {self.index + 1} elements,"
                f" found {len(container)}"
            )
        return container[self.index]

    def __set__(self, obj: element.ModelObject, value: t.Any) -> None:
        container = getattr(obj, self.wrapped)
        if not isinstance(container, ElementListCouplingMixin):
            raise TypeError(
                f"Cannot set {self._qualname}:"
                f" {self.wrapped} is not a coupled list"
            )
        if len(container) < self.index:
            raise RuntimeError(
                f"Broken XML: Expected at least {self.index+1} elements,"
                f" found {len(container)}"
            )
        container[self.index] = value


class AlternateAccessor(Accessor[T]):
    """Provides access to an "alternate" form of the object."""

    __slots__ = ("class_",)

    def __init__(self, class_: type[T]):
        super().__init__()
        self.class_ = class_

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self
        return self.class_.from_model(obj._model, obj._element)


class ParentAccessor(PhysicalAccessor[T]):
    """Accesses the parent XML element."""

    __slots__ = ()

    def __init__(self, class_: type[T]):
        super().__init__(class_)

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        parent = next(obj._model._loader.iterancestors(obj._element), None)
        if parent is None:
            objrepr = getattr(obj, "_short_repr_", obj.__repr__)()
            raise AttributeError(f"Object {objrepr} is orphaned")
        return self.class_.from_model(obj._model, parent)


@deprecated(
    "CustomAccessor is deprecated,"
    " create a specialized Accessor subclass instead"
)
class CustomAccessor(PhysicalAccessor[T]):
    """Customizable alternative to the DirectProxyAccessor.

    .. deprecated:: 0.5.4

       Deprecated due to overcomplexity and (ironically) a lack of
       flexibility.
    """

    __slots__ = (
        "elmfinders",
        "elmmatcher",
        "matchtransform",
    )

    def __init__(
        self,
        class_: type[T],
        *elmfinders: cabc.Callable[[element.GenericElement], cabc.Iterable[T]],
        elmmatcher: cabc.Callable[
            [U, element.GenericElement], bool
        ] = operator.contains,  # type: ignore[assignment]
        matchtransform: cabc.Callable[[T], U] = (
            lambda e: e  # type: ignore[assignment,return-value]
        ),
        aslist: type[element.ElementList] | None = None,
    ) -> None:
        """Create a CustomAccessor.

        Parameters
        ----------
        class_
            The target subclass of ``GenericElement``
        elmfinders
            Functions that are called on the current element. Each
            returns an iterable of possible targets.
        aslist
            If None, only a single element must match, which will be
            returned directly. If not None, must be a subclass of
            :class:`~capellambse.model.common.element.ElementList`,
            which will be used to return a list of all matched objects.
        elmmatcher
            Function that is called with the transformed target element
            and the current element to determine if the untransformed
            target should be accepted.
        matchtransform
            Function that transforms a target so that it can be used by
            the matcher function.
        """
        super().__init__(class_, aslist=aslist)
        self.elmfinders = elmfinders
        self.elmmatcher = elmmatcher
        self.matchtransform = matchtransform

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:
            return self

        elms = itertools.chain.from_iterable(f(obj) for f in self.elmfinders)
        matches = [
            e._element
            for e in elms
            if self.elmmatcher(self.matchtransform(e), obj)
        ]
        return self._make_list(obj, matches)


class AttributeMatcherAccessor(DirectProxyAccessor[T]):
    __slots__ = (
        "_AttributeMatcherAccessor__aslist",
        "attributes",
    )

    def __init__(
        self,
        class_: type[T],
        xtypes: str | type[T] | cabc.Iterable[str | type[T]] | None = None,
        *,
        aslist: type[element.ElementList] | None = None,
        attributes: dict[str, t.Any],
        **kwargs,
    ) -> None:
        super().__init__(
            class_, xtypes, aslist=element.MixedElementList, **kwargs
        )
        self.__aslist = aslist
        self.attributes = attributes

    def __get__(self, obj, objtype=None):
        if obj is None:  # pragma: no cover
            return self

        elements = super().__get__(obj, objtype)
        matches = []
        assert isinstance(elements, cabc.Iterable)
        for elm in elements:
            try:
                if all(
                    getattr(elm, k) == v for k, v in self.attributes.items()
                ):
                    matches.append(elm._element)
            except AttributeError:
                pass

        if self.__aslist is None:
            return no_list(self, obj._model, matches, self.class_)
        return self.__aslist(obj._model, matches, self.class_)


class _Specification(t.MutableMapping[str, str]):
    _aliases = {"LinkedText": "capella:linkedText"}
    _linked_text = frozenset({"capella:linkedText"})
    _model: capellambse.MelodyModel
    _element: etree._Element

    def __init__(
        self, model: capellambse.MelodyModel, elm: etree._Element
    ) -> None:
        self._model = model
        self._element = elm

    def __delitem__(self, k: str) -> None:
        k = self._aliases.get(k, k)
        i, lang_elem = self._index_of(k)
        body_elem = self._body_at(k, i)
        self._element.remove(lang_elem)
        self._element.remove(body_elem)

    def __getitem__(self, k: str) -> str:
        k = self._aliases.get(k, k)
        i, _ = self._index_of(k)
        v = self._body_at(k, i).text or ""
        if k in self._linked_text:
            v = helpers.unescape_linked_text(self._model._loader, v)
        return v

    def __iter__(self) -> cabc.Iterator[str]:
        for i in self._element.iterchildren("languages"):
            yield i.text or ""

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __setitem__(self, k: str, v: str) -> None:
        k = self._aliases.get(k, k)
        if k in self._linked_text:
            v = helpers.escape_linked_text(self._model._loader, v)
        try:
            i, lang = self._index_of(k)
        except KeyError:
            self._element.append(body := self._element.makeelement("bodies"))
            self._element.append(
                lang := self._element.makeelement("languages")
            )
            body.text = v
            lang.text = k
        else:
            body = self._body_at(k, i)
            body.text = v

    def _index_of(self, k: str) -> tuple[int, etree._Element]:
        for i, elm in enumerate(self._element.iterchildren("languages")):
            if elm.text == k:
                return i, elm

        raise KeyError(k)

    def _body_at(self, k: str, i: int) -> etree._Element:
        try:
            return next(
                itertools.islice(
                    self._element.iterchildren("bodies"), i, i + 1
                )
            )
        except StopIteration:
            raise KeyError(k) from None

    def __html__(self) -> str:
        return markupsafe.escape(self.__str__())

    def __str__(self) -> str:  # pragma: no cover
        return next(iter(self.values()))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{type(self).__name__} at 0x{id(self):016X} {list(self)!r}>"

    @classmethod
    def from_model(cls, _1: capellambse.MelodyModel, _2: t.Any) -> te.Self:
        """Specifications can not be instantiated."""
        raise RuntimeError("Can not create a specification from a model")


class SpecificationAccessor(Accessor[_Specification]):
    """Provides access to linked specifications."""

    __slots__ = ()

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        try:
            spec_elm = next(obj._element.iterchildren("ownedSpecification"))
        except StopIteration:
            raise AttributeError("No specification found") from None

        return _Specification(obj._model, spec_elm)


class ReferenceSearchingAccessor(PhysicalAccessor[T]):
    """Searches for references to the current element elsewhere."""

    __slots__ = ("attrs", "target_classes")

    attrs: tuple[operator.attrgetter, ...]
    target_classes: tuple[type[element.ModelObject], ...]

    def __init__(
        self,
        class_: type[T] | tuple[type[element.ModelObject], ...],
        *attrs: str,
        aslist: type[element.ElementList] | None = None,
        mapkey: str | None = None,
        mapvalue: str | None = None,
    ) -> None:
        """Create a ReferenceSearchingAccessor.

        Parameters
        ----------
        class_
            The type of class to search for references on.
        attrs
            The attributes of the target classes to search through.
        aslist
            If None, only a single element must match, which will be
            returned directly. If not None, must be a subclass of
            :class:`~capellambse.model.common.element.ElementList`,
            which will be used to return a list of all matched objects.
        mapkey
            Specify the attribute to look up when the returned list is
            indexed with a str. If not specified, str indexing is not
            possible.

            Ignored if *aslist* is not specified.
        mapvalue
            If specified, return this attribute of the found object when
            using str indices into the returned list. If not specified,
            the found object itself is returned.

            Ignored if *aslist* is not specified.
        """
        if isinstance(class_, tuple):
            super().__init__(
                element.GenericElement,  # type: ignore[arg-type]
                aslist=aslist,
                mapkey=mapkey,
                mapvalue=mapvalue,
            )
            self.target_classes = class_
        else:
            super().__init__(
                class_, aslist=aslist, mapkey=mapkey, mapvalue=mapvalue
            )
            self.target_classes = (class_,)
        self.attrs = tuple(operator.attrgetter(i) for i in attrs)

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        matches: list[etree._Element] = []
        for candidate in obj._model.search(*self.target_classes):
            for attr in self.attrs:
                try:
                    value = attr(candidate)
                except AttributeError:
                    continue
                if (
                    isinstance(value, element.ElementList)
                    and obj in value
                    or isinstance(value, element.GenericElement)
                    and obj == value
                ):
                    matches.append(candidate._element)
                    break
        return self._make_list(obj, matches)


class TypecastAccessor(WritableAccessor[T], PhysicalAccessor[T]):
    """Changes the static type of the value of another accessor.

    This is useful for when a class has an attribute that is
    polymorphic, but the accessor should always return a specific
    subclass.

    At runtime, this Accessor mostly behaves like a simple alias
    (without performing any runtime type checks or conversions). When
    creating new objects, it will only allow to create objects of the
    specified type.
    """

    aslist: type[ElementListCouplingMixin] | None
    class_: type[T]

    def __init__(
        self,
        cls: type[T],
        attr: str,
        mapkey: str | None = None,
        mapvalue: str | None = None,
    ) -> None:
        super().__init__(
            cls,
            (),
            aslist=element.ElementList,
            mapkey=mapkey,
            mapvalue=mapvalue,
        )
        self.attr = attr

    @t.overload
    def __get__(self, obj: None, objtype: type[t.Any]) -> te.Self: ...
    @t.overload
    def __get__(
        self, obj: element.ModelObject, objtype: type[t.Any] | None = None
    ) -> element.ElementList[T]: ...
    def __get__(
        self,
        obj: element.ModelObject | None,
        objtype: type[t.Any] | None = None,
    ) -> te.Self | element.ElementList[T]:
        del objtype
        if obj is None:
            return self

        return getattr(obj, self.attr)

    def __set__(
        self,
        obj: element.ModelObject,
        value: T | _NewObject | cabc.Iterable[T | _NewObject],
    ) -> None:
        if isinstance(value, (list, element.ElementList, tuple)):
            pass
        elif isinstance(value, cabc.Iterable):
            value = list(value)
        else:
            raise TypeError(f"Expected list, got {type(value).__name__}")

        if any(isinstance(i, _NewObject) for i in value):
            raise NotImplementedError("Cannot create new objects here")

        if not all(isinstance(i, self.class_) for i in value):
            raise TypeError(
                f"Expected {self.class_.__name__}, got {type(value).__name__}"
            )
        setattr(obj, self.attr, value)

    def __delete__(self, obj):
        delattr(obj, self.attr)

    def create(
        self,
        elmlist: ElementListCouplingMixin,
        /,
        *type_hints: str | None,
        **kw: t.Any,
    ) -> T:
        if type_hints:
            raise TypeError(f"{self._qualname} does not support type hints")
        acc: WritableAccessor = getattr(self.class_, self.attr)
        obj = acc.create(elmlist, build_xtype(self.class_), **kw)
        assert isinstance(obj, self.class_)
        return obj

    def insert(
        self,
        elmlist: ElementListCouplingMixin,
        index: int,
        value: element.ModelObject | _NewObject,
    ) -> None:
        if isinstance(value, _NewObject):
            raise NotImplementedError("Cannot insert new objects yet")
        if not isinstance(value, self.class_):
            raise TypeError(
                f"Expected {self.class_.__name__}, got {type(value).__name__}"
            )
        acc: WritableAccessor = getattr(self.class_, self.attr)
        acc.insert(elmlist, index, value)

    def delete(
        self,
        elmlist: ElementListCouplingMixin,
        obj: element.ModelObject,
    ) -> None:
        acc: WritableAccessor = getattr(self.class_, self.attr)
        acc.delete(elmlist, obj)

    @contextlib.contextmanager
    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> cabc.Iterator[None]:
        acc: WritableAccessor = getattr(self.class_, self.attr)
        with acc.purge_references(obj, target):
            yield


class RoleTagAccessor(WritableAccessor, PhysicalAccessor):
    __slots__ = ("classes", "role_tag")

    aslist: type[ElementListCouplingMixin] | None
    class_: type[element.GenericElement]
    alternate: type[element.GenericElement] | None

    def __init__(
        self,
        role_tag: str,
        classes: (
            type[element.ModelObject]
            | cabc.Iterable[type[element.ModelObject]]
        ) = (),
        *,
        aslist: type[element.ElementList[T]] | None = None,
        mapkey: str | None = None,
        mapvalue: str | None = None,
        list_extra_args: dict[str, t.Any] | None = None,
        alternate: type[element.GenericElement] | None = None,
    ) -> None:
        super().__init__(
            element.GenericElement,
            (),
            aslist=aslist,
            list_extra_args=list_extra_args,
            mapkey=mapkey,
            mapvalue=mapvalue,
        )
        self.role_tag = role_tag
        if not isinstance(classes, type):
            self.classes = tuple(classes)
        else:
            self.classes = (classes,)

        if len(self.classes) != 1 and alternate is not None:
            raise TypeError("alternate needs exactly 1 possible origin class")
        self.alternate = alternate

    def __get__(self, obj, objtype=None):
        del objtype
        if obj is None:  # pragma: no cover
            return self

        elts = list(obj._element.iterchildren(self.role_tag))
        rv = self._make_list(obj, elts)
        if self.classes:
            rv = rv.filter(lambda i: isinstance(i, self.classes))
        if self.alternate is not None:
            assert isinstance(rv, element.ElementList)
            assert not isinstance(rv, element.MixedElementList)
            rv._elemclass = self.alternate
        return rv

    def __set__(
        self,
        obj: element.ModelObject,
        value: (
            str
            | element.GenericElement
            | _NewObject
            | cabc.Iterable[str | element.GenericElement | _NewObject]
        ),
    ) -> None:
        if self.aslist:
            raise NotImplementedError(
                "Setting lists of model objects is not supported yet"
            )
        else:
            if isinstance(value, cabc.Iterable) and not isinstance(value, str):
                raise TypeError("Cannot set non-list attribute to an iterable")
            if not isinstance(value, _NewObject):
                raise NotImplementedError(
                    "Moving model objects is not supported yet"
                )
            if (elem := self.__get__(obj)) is not None:
                valueclass, _ = self._match_xtype(*value._type_hint)
                elemclass = elem.__class__
                if elemclass is not valueclass:
                    obj._model._loader.idcache_remove(elem._element)
                    obj._element.remove(elem._element)
                else:
                    for k, v in value._kw.items():
                        setattr(elem, k, v)
                    return
            self._create(obj, self.role_tag, *value._type_hint, **value._kw)

    def create(
        self,
        elmlist: ElementListCouplingMixin,
        /,
        *type_hints: str | None,
        **kw: t.Any,
    ) -> element.GenericElement:
        return self._create(elmlist._parent, self.role_tag, *type_hints, **kw)

    def insert(
        self,
        elmlist: ElementListCouplingMixin,
        index: int,
        value: element.ModelObject | _NewObject,
    ) -> None:
        if isinstance(value, _NewObject):
            raise NotImplementedError("Cannot insert new objects yet")
        if value._model is not elmlist._model:
            raise ValueError("Cannot move elements between models")
        try:
            indexof = elmlist._parent._element.index
            if index > 0:
                parent_index = indexof(elmlist._elements[index - 1]) + 1
            elif index < -1:
                parent_index = indexof(elmlist._elements[index + 1]) - 1
            else:
                parent_index = index
        except ValueError:
            parent_index = len(elmlist._parent._element)
        elmlist._parent._element.insert(parent_index, value._element)
        elmlist._model._loader.idcache_index(value._element)

    def delete(
        self,
        elmlist: ElementListCouplingMixin,
        obj: element.ModelObject,
    ) -> None:
        assert obj._model is elmlist._model
        model = obj._model
        all_elements = list(model._loader.iterdescendants_xt(obj._element)) + [
            obj._element
        ]
        with contextlib.ExitStack() as stack:
            for elm in all_elements:
                if elm.get("id") is None:
                    continue

                obj = element.GenericElement.from_model(model, elm)
                for ref, attr, _ in model.find_references(obj):
                    acc = getattr(type(ref), attr)
                    if acc is self or not isinstance(acc, WritableAccessor):
                        continue
                    stack.enter_context(acc.purge_references(ref, obj))

            elm = obj._element
            parent = elm.getparent()
            assert parent is not None
            model._loader.idcache_remove(elm)
            parent.remove(elm)

    @contextlib.contextmanager
    def purge_references(
        self, obj: element.ModelObject, target: element.ModelObject
    ) -> cabc.Iterator[None]:
        yield

    def _match_xtype(
        self,
        type_1: str | None,
        type_2: str | object = _NOT_SPECIFIED,
        /,
    ) -> tuple[type[element.ModelObject], str]:
        if not self.classes:
            return super()._match_xtype(type_1, type_2)

        if type_2 is not _NOT_SPECIFIED:
            raise TypeError(
                f"Only a single type hint is allowed for {self._qualname},"
                f" got ({type_1!r}, {type_2!r})"
            )

        cls = next((i for i in self.classes if i.__name__ == type_1), None)
        if cls is None:
            raise ValueError(f"Invalid class for {self._qualname}: {type_1}")
        return cls, build_xtype(cls)

    def _guess_xtype(self) -> tuple[type[element.ModelObject], str]:
        if len(self.classes) == 1:
            return self.classes[0], build_xtype(self.classes[0])

        if len(self.classes) > 1:
            hint = ", valid values: " + ", ".join(
                i.__name__ for i in self.classes
            )
        else:
            hint = ""
        raise ValueError(f"{self._qualname} requires a type hint{hint}")


def no_list(
    desc: Accessor,
    model: capellambse.MelodyModel,
    elems: cabc.Sequence[etree._Element],
    class_: type[T],
) -> element.ModelObject | None:
    """Return a single element or None instead of a list of elements.

    Parameters
    ----------
    desc
        The descriptor that called this function
    model
        The ``MelodyModel`` instance
    elems
        List of elements that was matched
    class_
        The ``GenericElement`` subclass to instantiate
    """
    if not elems:  # pragma: no cover
        return None
    if len(elems) > 1:  # pragma: no cover
        raise RuntimeError(
            f"Expected 1 object for {desc._qualname}, got {len(elems)}"
        )
    return class_.from_model(model, elems[0])


class ElementListCouplingMixin(element.ElementList[T], t.Generic[T]):
    """Couples an ElementList with an Accessor to enable write support.

    This class is meant to be subclassed further, where the subclass has
    both this class and the originally intended one as base classes (but
    no other ones, i.e. there must be exactly two bases). The Accessor
    then inserts itself as the ``_accessor`` class variable on the new
    subclass. This allows the mixed-in methods to delegate actual model
    modifications to the Accessor.
    """

    _accessor: WritableAccessor[T]

    def __init__(
        self,
        *args: t.Any,
        parent: element.ModelObject,
        fixed_length: int = 0,
        **kw: t.Any,
    ) -> None:
        assert type(self)._accessor

        super().__init__(*args, **kw)
        self._parent = parent
        self.fixed_length = fixed_length

    @t.overload
    def __setitem__(self, index: int, value: T) -> None: ...
    @t.overload
    def __setitem__(self, index: slice, value: cabc.Iterable[T]) -> None: ...
    @t.overload
    def __setitem__(self, index: str, value: t.Any) -> None: ...
    def __setitem__(self, index: int | slice | str, value: t.Any) -> None:
        assert self._parent is not None
        accessor = type(self)._accessor
        assert isinstance(accessor, WritableAccessor)

        if not isinstance(index, (int, slice)):
            super().__setitem__(index, value)
            return

        new_objs = list(self)
        new_objs[index] = value

        if self.fixed_length and len(new_objs) != self.fixed_length:
            raise TypeError(
                f"Cannot set: List must stay at length {self.fixed_length}"
            )

        accessor.__set__(self._parent, new_objs)

    def __delitem__(self, index: int | slice) -> None:
        if self.fixed_length and len(self) <= self.fixed_length:
            raise TypeError("Cannot delete from a fixed-length list")

        assert self._parent is not None
        accessor = type(self)._accessor
        assert isinstance(accessor, WritableAccessor)
        if not isinstance(index, slice):
            index = slice(index, index + 1 or None)
        for obj in self[index]:
            accessor.delete(self, obj)
        super().__delitem__(index)

    def _newlist_type(self) -> type[element.ElementList[T]]:
        assert len(type(self).__bases__) == 2
        assert type(self).__bases__[0] is ElementListCouplingMixin
        return type(self).__bases__[1]

    def create(self, *type_hints: str | None, **kw: t.Any) -> T:
        """Make a new model object (instance of GenericElement).

        Instead of specifying the full ``xsi:type`` including the
        namespace, you can also pass in just the part after the ``:``
        separator. If this is unambiguous, the appropriate
        layer-specific type will be selected automatically.

        This method can be called with or without the ``layertype``
        argument. If a layertype is not given, all layers will be tried
        to find an appropriate ``xsi:type`` handler. Note that setting
        the layertype to ``None`` explicitly is different from not
        specifying it at all; ``None`` tries only the "Transverse
        modelling" type elements.

        Parameters
        ----------
        type_hints
            Hints for finding the correct type of element to create. Can
            either be a full or shortened ``xsi:type`` string, or an
            abbreviation defined by the specific Accessor instance.
        kw
            Initialize the properties of the new object. Depending on
            the object, some attributes may be required.
        """
        if self.fixed_length and len(self) >= self.fixed_length:
            raise TypeError("Cannot create elements in a fixed-length list")

        assert self._parent is not None
        acc = type(self)._accessor
        assert isinstance(acc, WritableAccessor)
        newobj = acc.create(self, *type_hints, **kw)
        try:
            acc.insert(self, len(self), newobj)
            super().insert(len(self), newobj)
        except:
            self._parent._element.remove(newobj._element)
            raise
        return newobj

    def create_singleattr(self, arg: t.Any) -> T:
        """Make a new model object (instance of GenericElement).

        This new object has only one interesting attribute.

        See Also
        --------
        :meth:`ElementListCouplingMixin.create` :
            More details on how elements are created.
        :meth:`WritableAccessor.create_singleattr` :
            The method to override in Accessors in order to implement
            this operation.
        """
        if self.fixed_length and len(self) >= self.fixed_length:
            raise TypeError("Cannot create elements in a fixed-length list")

        assert self._parent is not None
        acc = type(self)._accessor
        assert isinstance(acc, WritableAccessor)
        newobj = acc.create_singleattr(self, arg)
        try:
            acc.insert(self, len(self), newobj)
            super().insert(len(self), newobj)
        except:
            self._parent._element.remove(newobj._element)
            raise
        return newobj

    def insert(self, index: int, value: T) -> None:
        if self.fixed_length and len(self) >= self.fixed_length:
            raise TypeError("Cannot insert into a fixed-length list")

        assert self._parent is not None
        acc = type(self)._accessor
        assert isinstance(acc, WritableAccessor)
        acc.insert(self, index, value)
        super().insert(index, value)
