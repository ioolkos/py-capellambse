# SPDX-FileCopyrightText: Copyright DB InfraGO AG
# SPDX-License-Identifier: Apache-2.0
"""Common classes used by all MelodyModel functions.

.. diagram:: [CDB] Common Types ORM
"""
from __future__ import annotations

import collections
import collections.abc as cabc
import operator
import typing as t

import capellambse

S = t.TypeVar("S", bound=t.Optional[str])
T = t.TypeVar("T", bound="ModelObject")
U = t.TypeVar("U")


XTYPE_ANCHORS = {
    "capellambse.model": "org.polarsys.capella.core.data.capellamodeller",
    "capellambse.model.crosslayer": "org.polarsys.capella.core.data",
    "capellambse.model.diagram": "viewpoint",
    "capellambse.model.layers": "org.polarsys.capella.core.data",
}
"""A mapping from anchor modules to Capella packages.

This dictionary maps Python modules and packages to the Capella packages
they represent. ``build_xtype`` and related functions/classes can then
use this information to automatically derive an ``xsi:type`` from any
class that is defined in such an anchor module (or a submodule of one).
"""
XTYPE_HANDLERS: dict[str | None, dict[str, type[t.Any]]] = (
    collections.defaultdict(dict)
)
r"""Defines a mapping between ``xsi:type``\ s and wrapper classes.

The first layer's keys can be either ``None`` or the ``xsi:type`` of the
architectural layer that the wrapper should be applied to. In the case
of ``None``, the wrapper will be applied to all layers. Note that
layer-specific wrappers have precedence over layer-agnostic ones.

These keys map to a further dictionary. This second layer maps from the
``xsi:type``\ (s) that each wrapper handles to the wrapper class.
"""


def build_xtype(class_: type[ModelObject]) -> str:
    anchor = package = ""
    for a, p in XTYPE_ANCHORS.items():
        if len(a) > len(anchor) and class_.__module__.startswith(a):
            anchor = a
            package = p

    if not anchor:
        raise TypeError(f"Module is not an xtype anchor: {class_.__module__}")

    module = class_.__module__[len(anchor) :]
    clsname = class_.__name__
    return f"{package}{module}:{clsname}"


def find_wrapper(typehint: str) -> tuple[type[ModelObject], ...]:
    """Find the possible wrapper classes for the hinted type.

    The typehint is either a single class name, or a namespace prefix
    and class name separated by ``:``. This function searches for all
    known wrapper classes that match the given namespace prefix (if any)
    and which have the given name, and returns them as a tuple. If no
    matching wrapper classes are found, an empty tuple is returned.
    """
    return tuple(
        v
        for i in XTYPE_HANDLERS.values()
        for k, v in i.items()
        if k.endswith(f":{typehint}") or k == typehint
    )


def enumliteral(
    generic_element: GenericElement, attr: str, default: str = "NOT_SET"
) -> AttributeProperty | str:
    uuid = generic_element._element.attrib.get(attr)
    if uuid is None:
        return default

    return generic_element.from_model(
        generic_element._model, generic_element._model._loader[uuid]
    ).name


def set_accessor(
    cls: type[ModelObject], attr: str, accessor: Accessor
) -> None:
    setattr(cls, attr, accessor)
    accessor.__set_name__(cls, attr)


def set_self_references(*args: tuple[type[ModelObject], str]) -> None:
    for cls, attr in args:
        set_accessor(cls, attr, DirectProxyAccessor(cls, aslist=ElementList))


def xtype_handler(
    arch: str | None = None, /, *xtypes: str
) -> cabc.Callable[[type[T]], type[T]]:
    """Register a class as handler for a specific ``xsi:type``.

    ``arch`` is the ``xsi:type`` of the desired architecture. It must
    always be a simple string or None. In the latter case the definition
    applies to all elements regardless of their architectural layer.
    Architecture-specific definitions will always win over
    architecture-independent ones.

    Each string given in ``xtypes`` notes an ``xsi:type`` of elements
    that this class handles. It is possible to specify multiple values,
    in which case the class will be registered for each ``xsi:type``
    under the architectural layer given in ``arch``.

    Handler classes' ``__init__`` methods must accept two positional
    arguments. The first argument is the
    :class:`~capellambse.model.MelodyModel` instance which loaded the
    corresponding model, and the second one is
    the LXML element that needs to be handled.

    Example::

        >>> @xtype_handler('arch:xtype', 'xtype:1', 'xtype:2')
        ... class Test:
        ...     _xmltag = "ownedTests"
        ...     def from_model(self, model, element, /):
        ...         ...  # Instantiate from model XML element
    """
    if arch is not None and not isinstance(arch, str):  # pragma: no cover
        raise TypeError(
            f"'arch' must be a str or None, not {type(arch).__name__}"
        )

    # Compile a list of all xtype strings
    xtype_strs = []
    for xtype in xtypes:
        if isinstance(xtype, str):
            xtype_strs.append(xtype)
        else:  # pragma: no cover
            raise ValueError(
                f"All `xtype`s must be str, not {type(xtype).__name__!r}"
            )

    def register_xtype_handler(cls: type[T]) -> type[T]:
        # Avoid double registration when executing an extension as module
        if cls.__module__ == "__main__":
            return cls

        if not xtype_strs:
            xtype_strs.append(build_xtype(cls))

        for xtype in xtype_strs:
            if xtype in XTYPE_HANDLERS[arch]:  # pragma: no cover
                raise LookupError(f"Duplicate xsi:type {xtype} in {arch}")
            XTYPE_HANDLERS[arch][xtype] = cls
        return cls

    return register_xtype_handler


def resolve_handler(xtype: str) -> tuple[str, type[t.Any]]:
    matches: list[tuple[str, type[t.Any]]] = []

    if ":" in xtype:
        ismatch: cabc.Callable[[str, str], bool] = operator.eq
        searchname = xtype
    else:
        ismatch = str.endswith
        searchname = ":" + xtype

    for i in XTYPE_HANDLERS.values():
        matches.extend(t for t in i.items() if ismatch(t[0], searchname))

    if len(matches) < 1:
        raise ValueError(f"No handlers found for xsi:type: {xtype}")
    if len(matches) > 1:
        raise RuntimeError(f"Multiple handlers for xsi:type: {xtype}")
    return matches[0]


from .accessors import *
from .accessors import _NewObject as new_object
from .element import *
from .properties import *

set_accessor(GenericElement, "parent", ParentAccessor(GenericElement))
