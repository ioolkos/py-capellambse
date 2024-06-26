# SPDX-FileCopyrightText: Copyright DB InfraGO AG
# SPDX-License-Identifier: Apache-2.0
"""Tools for the Logical Architecture layer.

.. diagram:: [CDB] LA ORM
"""
from __future__ import annotations

from .. import common as c
from .. import crosslayer, diagram
from ..crosslayer import capellacommon, capellacore, cs, fa, interaction
from . import ctx

XT_ARCH = "org.polarsys.capella.core.data.la:LogicalArchitecture"


@c.xtype_handler(XT_ARCH)
class LogicalFunction(fa.Function):
    """A logical function on the Logical Architecture layer."""

    realized_system_functions = c.TypecastAccessor(
        ctx.SystemFunction, "realized_functions"
    )
    owner: c.Accessor[LogicalComponent]


@c.xtype_handler(XT_ARCH)
class LogicalFunctionPkg(c.GenericElement):
    """A logical function package."""

    _xmltag = "ownedFunctionPkg"

    functions = c.RoleTagAccessor(
        "ownedLogicalFunctions", LogicalFunction, aslist=c.ElementList
    )

    packages: c.Accessor


@c.xtype_handler(XT_ARCH)
class LogicalComponent(cs.Component):
    """A logical component on the Logical Architecture layer."""

    _xmltag = "ownedLogicalComponents"

    allocated_functions = c.LinkAccessor[LogicalFunction](
        "ownedFunctionalAllocation",
        fa.XT_FCALLOC,
        aslist=c.ElementList,
        attr="targetElement",
        backattr="sourceElement",
    )
    realized_system_components = c.TypecastAccessor(
        ctx.SystemComponent,
        "realized_components",
    )

    components: c.Accessor
    functions = c.DeprecatedAccessor[LogicalFunction]("allocated_functions")


@c.xtype_handler(XT_ARCH)
class LogicalComponentPkg(c.GenericElement):
    """A logical component package."""

    _xmltag = "ownedLogicalComponentPkg"

    components = c.DirectProxyAccessor(LogicalComponent, aslist=c.ElementList)
    state_machines = c.DirectProxyAccessor(
        capellacommon.StateMachine, aslist=c.ElementList
    )
    exchanges = c.DirectProxyAccessor(
        fa.ComponentExchange, aslist=c.ElementList
    )

    packages: c.Accessor


@c.xtype_handler(None)
class CapabilityRealization(c.GenericElement):
    """A capability."""

    _xmltag = "ownedCapabilityRealizations"

    owned_chains = c.DirectProxyAccessor(
        fa.FunctionalChain, aslist=c.ElementList
    )
    involved_functions = c.LinkAccessor[LogicalFunction](
        "ownedAbstractFunctionAbstractCapabilityInvolvements",
        interaction.AbstractFunctionAbstractCapabilityInvolvement,
        aslist=c.ElementList,
        attr="involved",
    )
    involved_chains = c.LinkAccessor[fa.FunctionalChain](
        "ownedFunctionalChainAbstractCapabilityInvolvements",
        interaction.XT_CAP2PROC,
        aslist=c.ElementList,
        attr="involved",
    )
    involved_components = c.LinkAccessor[LogicalComponent](
        "ownedCapabilityRealizationInvolvements",
        capellacommon.XT_CAPABILITY_REALIZATION_INVOLVEMENT,
        aslist=c.MixedElementList,
        attr="involved",
    )
    realized_capabilities = c.LinkAccessor[ctx.Capability](
        None,  # FIXME fill in tag
        interaction.XT_CAP_REAL,
        aslist=c.ElementList,
        attr="targetElement",
    )

    postcondition = c.AttrProxyAccessor(
        capellacore.Constraint, "postCondition"
    )
    precondition = c.AttrProxyAccessor(capellacore.Constraint, "preCondition")
    scenarios = c.DirectProxyAccessor(
        interaction.Scenario, aslist=c.ElementList
    )
    states = c.AttrProxyAccessor(
        capellacommon.State, "availableInStates", aslist=c.ElementList
    )

    packages: c.Accessor


@c.xtype_handler(XT_ARCH)
class CapabilityRealizationPkg(c.GenericElement):
    """A capability package that can hold capabilities."""

    _xmltag = "ownedAbstractCapabilityPkg"

    capabilities = c.DirectProxyAccessor(
        CapabilityRealization, aslist=c.ElementList
    )

    packages: c.Accessor


@c.xtype_handler(None)
class LogicalArchitecture(crosslayer.BaseArchitectureLayer):
    """Provides access to the LogicalArchitecture layer of the model."""

    root_component = c.AttributeMatcherAccessor(
        LogicalComponent,
        attributes={"is_actor": False},
        rootelem=LogicalComponentPkg,
    )
    root_function = c.DirectProxyAccessor(
        LogicalFunction, rootelem=LogicalFunctionPkg
    )

    function_package = c.DirectProxyAccessor(LogicalFunctionPkg)
    component_package = c.DirectProxyAccessor(LogicalComponentPkg)
    capability_package = c.DirectProxyAccessor(CapabilityRealizationPkg)

    all_functions = c.DeepProxyAccessor(
        LogicalFunction,
        aslist=c.ElementList,
        rootelem=LogicalFunctionPkg,
    )
    all_capabilities = c.DeepProxyAccessor(
        CapabilityRealization, aslist=c.ElementList
    )
    all_components = (  # maybe this should exclude .is_actor
        c.DeepProxyAccessor(LogicalComponent, aslist=c.ElementList)
    )
    all_actors = property(
        lambda self: self._model.search(LogicalComponent).by_is_actor(True)
    )
    all_functional_chains = property(
        lambda self: self._model.search(fa.FunctionalChain, below=self)
    )

    actor_exchanges = c.DirectProxyAccessor(
        fa.ComponentExchange,
        aslist=c.ElementList,
        rootelem=LogicalComponentPkg,
    )
    component_exchanges = c.DeepProxyAccessor(
        fa.ComponentExchange,
        aslist=c.ElementList,
        rootelem=[LogicalComponentPkg, LogicalComponent],
    )

    all_function_exchanges = c.DeepProxyAccessor(
        fa.FunctionalExchange,
        aslist=c.ElementList,
        rootelem=[LogicalFunctionPkg, LogicalFunction],
    )
    all_component_exchanges = c.DeepProxyAccessor(
        fa.ComponentExchange, aslist=c.ElementList
    )

    diagrams = diagram.DiagramAccessor(
        "Logical Architecture", cacheattr="_MelodyModel__diagram_cache"
    )


c.set_accessor(
    ctx.Capability,
    "realizing_capabilities",
    c.ReferenceSearchingAccessor(
        CapabilityRealization, "realized_capabilities", aslist=c.ElementList
    ),
)
c.set_accessor(
    ctx.SystemComponent,
    "realizing_logical_components",
    c.ReferenceSearchingAccessor(
        LogicalComponent, "realized_components", aslist=c.ElementList
    ),
)
c.set_accessor(
    ctx.SystemFunction,
    "realizing_logical_functions",
    c.ReferenceSearchingAccessor(
        LogicalFunction, "realized_system_functions", aslist=c.ElementList
    ),
)
c.set_accessor(
    LogicalFunction,
    "owner",
    c.ReferenceSearchingAccessor(LogicalComponent, "allocated_functions"),
)
c.set_accessor(
    LogicalFunction,
    "packages",
    c.DirectProxyAccessor(
        LogicalFunctionPkg,
        aslist=c.ElementList,
    ),
)
c.set_accessor(
    LogicalFunction,
    "involved_in",
    c.ReferenceSearchingAccessor(
        CapabilityRealization, "involved_functions", aslist=c.ElementList
    ),
)
c.set_self_references(
    (LogicalComponent, "components"),
    (LogicalComponentPkg, "packages"),
    (LogicalFunction, "functions"),
    (LogicalFunctionPkg, "packages"),
)
