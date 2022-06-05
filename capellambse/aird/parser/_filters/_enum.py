# Copyright DB Netz AG and the capellambse contributors
# SPDX-License-Identifier: Apache-2.0

"""
Filter enum values for all filters derived from official capella repo
file:
core/plugins/org.polarsys.capella.core.sirius.analysis/src/org/polarsys/capella/core/sirius/analysis/constants/IFilterNameConstants.java
"""

import enum


class Filters(enum.Enum):
    #  Common filters
    FILTER_COMMON_HIDE_PV = "hide.property.values.filter"

    # CC filters - Contextual Capability
    FILTER_CC_HIDE_CAPABILITIES = "hide.capabilities.filter"
    FILTER_CC_HIDE_CAPABILITY_EXPLOITATION = (
        "hide.capability.exploitations.filter"
    )
    FILTER_CC_HIDE_CAPABILITY_EXTENDS = "hide.capability.extends.filter"
    FILTER_CC_HIDE_CAPABILITY_INCLUDES = "hide.capability.includes.filter"
    FILTER_CC_HIDE_CAPABILITY_GENERALIZATIONS = (
        "hide.capability.generalizations.filter"
    )
    FILTER_CC_HIDE_MISSIONS = "hide.missions.filter"
    FILTER_CC_HIDE_ACTORS = "hide.actors.filter"
    FILTER_CC_HIDE_ACTOR_INVOLVEMENTS = "hide.actor.involvements.filter"
    FILTER_CC_HIDE_ACTOR_GENERALIZATIONS = "hide.actor.generalizations.filter"
    FILTER_CC_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  CDB filters - Class Diagram Blank
    FILTER_CDB_HIDE_PROPERTIES = "hide.properties.filter"
    FILTER_CDB_HIDE_OPERATIONS = "hide.operations.filter"
    FILTER_CDB_HIDE_ASSOCIATIONS = "hide.associations.filter"
    FILTER_CDB_HIDE_GENERALIZATIONS = "hide.generalizations.filter"
    FILTER_CDB_HIDE_EXCHANGE_ITEMS_DETAILS_IN_INTERFACES = (
        "hide.exchange.items.details.in.interfaces.filter"
    )
    FILTER_CDB_HIDE_ASSOCIATION_LABELS = "hide.association.labels.filter"
    FILTER_CDB_HIDE_ROLE_LABELS = "hide.role.labels.filter"
    FILTER_CDB_SHOW_FULL_PATH = "show.full.path.filter"
    FILTER_CDB_HIDE_DERIVED_PROPERTIES = "hide.derived.properties.filter"
    FILTER_CDB_HIDE_TECHNICALS_INTERFACES = "hide.technical.interfaces.filter"
    FILTER_CDB_HIDE_ROLE_NAMES = "hide.role.names.filter"
    FILTER_CDB_SHOW_MODIFIERS = "show.modifiers.filter"
    FILTER_CDB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"
    FILTER_COMMON_HIDE_DIAGRAM_TITLE_BLOCKS = (
        "hide.diagram.title.blocks.filter"
    )
    FILTER_COMMON_HIDE_ELEMENT_TITLE_BLOCKS = (
        "hide.element.title.blocks.filter"
    )

    #  CDI filters - Contextual Component Detailed Interfaces
    FILTER_CDI_HIDE_INTERFACE_CONTENTS = "hide.interface.contents.filter"
    FILTER_CDI_HIDE_INTERFACES = "hide.interfaces.filter"
    FILTER_CDI_HIDE_EXCHANGE_ITEMS_DETAILS_IN_INTERFACES = (
        "hide.exchange.items.details.in.interfaces.filter"
    )
    FILTER_CDI_HIDE_EXCHANGE_ITEM_ELEMENTS = (
        "hide.exchange.item.elements.filter"
    )
    FILTER_CDI_HIDE_EXCHANGE_ITEMS = "hide.exchange.items.filter"
    FILTER_CDI_HIDE_COMPONENT_PORTS = "hide.component.ports.filter"
    FILTER_CDI_HIDE_USE_LINKS = "hide.use.links.filter"
    FILTER_CDI_HIDE_IMPLEMENTATION_LINKS = "hide.implmentation.links.filter"
    FILTER_CDI_HIDE_PROVIDE_LINKS = "hide.provide.links.filter"
    FILTER_CDI_HIDE_REQUIRE_LINKS = "hide.require.links.filter"
    FILTER_CDI_HIDE_COMMUNICATION_LINKS = "hide.communication.links.filter"
    FILTER_CDI_HIDE_GENERALIZATION_LINKS = "hide.generalization.links.filter"
    FILTER_CDI_HIDE_TECHNICALS_INTERFACES = "hide.technical.interfaces.filter"
    FILTER_CDI_SHOW_MODIFIERS = "show.modifiers.filter"
    FILTER_CDI_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  filter id
    FILTER_CDI_HIDE_IMPLEMENTATION_LINKS_ID = "hide.implmentation.links.filter"

    # CEI filters - Contextual Component External Interface
    FILTER_CEI_HIDE_INTERFACES = "hide.interfaces.filter"
    FILTER_CEI_HIDE_EXCHANGEITEM_ALLOCATION = (
        "hide.exchange.item.allocation.filter"
    )
    FILTER_CEI_HIDE_EXCHANGE_ITEMS = "hide.exchange.items.filter"
    FILTER_CEI_HIDE_COMPONENT_PORTS = "hide.component.ports.filter"
    FILTER_CEI_HIDE_USE_LINKS = "hide.use.links.filter"
    FILTER_CEI_HIDE_IMPLEMENTATION_LINKS = "hide.implmentation.links.filter"
    FILTER_CEI_HIDE_PROVIDE_LINKS = "hide.provide.links.filter"
    FILTER_CEI_HIDE_REQUIRE_LINKS = "hide.require.links.filter"
    FILTER_CEI_HIDE_COMMUNICATION_LINKS = "hide.communication.links.filter"
    FILTER_CEI_HIDE_GENERALIZATION_LINKS = "hide.generalization.links.filter"
    FILTER_CEI_HIDE_SIMPLIFIED_COMPONENT_INTERACTIONS = (
        "hide.simplified.component.interactions.filter"
    )
    FILTER_CEI_HIDE_TECHNICALS_INTERFACES = "hide.technical.interfaces.filter"

    #  filter id
    FILTER_CEI_HIDE_IMPLEMENTATION_LINKS_ID = "hide.implmentation.links.filter"

    #  COAI filters - Contextual Operational Activity Interaction
    FILTER_COAI_HIDE_INTERACTIONS = "hide.interactions.filter"
    FILTER_COAI_BACKUP_SHOW_EXCHANGEITEMS = "show.exchange.items.filters"
    FILTER_COAI_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_COAI_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_COAI_SHOW_FUNCTIONAL_EXCHANGES = "show.functional.exchanges.filter"

    #  COC filters - Contextual Operational Capability
    FILTER_COC_HIDE_ENTITIES = "hide.entities.filter"
    FILTER_COC_HIDE_INVOLVEMENT_LINKS = "hide.involvement.links.filter"
    FILTER_COC_HIDE_OPERATIONAL_CAPABILITY_EXTENDS = (
        "hide.operational.capability.extends.filter"
    )
    FILTER_COC_HIDE_OPERATIONAL_CAPABILITY_INCLUDES = (
        "hide.operational.capability.includes.filter"
    )
    FILTER_COC_HIDE_OPERATIONAL_CAPABILITY_GENERALIZATIONS = (
        "hide.operational.capability.generalizations.filter"
    )
    FILTER_COC_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    # CM filters - Contextual Mission
    FILTER_CM_HIDE_CAPABILITIES = "hide.capabilities.filter"
    FILTER_CM_HIDE_CAPABILITY_EXPLOITATIONS = (
        "hide.capability.exploitations.filter"
    )
    FILTER_CM_HIDE_CAPABILITY_GENERALIZATIONS = (
        "hide.capabilities.generalizations.filter"
    )
    FILTER_CM_HIDE_ACTORS = "hide.actors.filter"
    FILTER_CM_HIDE_ACTOR_INVOLVEMENTS = "hide.actor.involvements.filter"
    FILTER_CM_HIDE_ACTOR_GENERALIZATIONS = "hide.actor.generalizations.filter"
    FILTER_CM_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    # CRB filters - Capability Realization Blank
    FILTER_CRB_HIDE_CAPABILITY_REALIZATIONS = (
        "hide.capability.realizations.filter"
    )
    FILTER_CRB_HIDE_INVOLVEMENTS = "hide.involvements.filter"
    FILTER_CRB_HIDE_CAPABILITY_EXTENDS = "hide.capability.extends.filter"
    FILTER_CRB_HIDE_CAPABILTY_INCLUDES = "hide.capability.includes.filter"
    FILTER_CRB_HIDE_CAPABILITY_REALIZATION_GENERALIZATIONS = (
        "hide.capability.realization.generalizations.filter"
    )
    FILTER_CRB_HIDE_COMPONENTS = "hide.components.filter"
    FILTER_CRB_HIDE_ACTORS = "hide.actors.filter"
    FILTER_CRB_HIDE_ACTOR_GENERALIZATIONS = "hide.actor.generalizations.filter"

    #  EAB filters - EPBS Architecture Blank
    FILTER_EAB_HIDE_PHYSICAL_ARTIFACTS = "hide.physical.artifacts.filter"

    #  ES filters - Exchange Scenario
    FILTER_ES_HIDE_EXECUTIONS = "hide.executions.filter"
    FILTER_ES_HIDE_PRE_AND_POST_CONDITIONS = "hide.pre.post.conditions.filter"
    FILTER_ES_HIDE_PRE_AND_POST_CONDITIONS_ID = (
        "hide.pre.post.conditions.filter"
    )
    FILTER_ES_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_ES_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES = "show.functional.exchanges.filter"
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_ES_SHOW_COMPONENT_EXCHANGES_EXCHANGEITEMS = (
        "show.component.exchanges.exchange.items.filter"
    )
    FILTER_ES_SHOW_CEPARAM = "show.ce.param.filter"
    FILTER_ES_SHOW_CEEIPARAM = "show.ce.ei.param.filter"
    FILTER_ES_SHOW_EXCHANGE_CONTEXT = "show.exchange.context.filter"
    FILTER_ES_SHOW_FE_EXCHANGE_CONTEXT = "show.fe.exchange.context.filter"
    FILTER_ES_SHOW_CE_EXCHANGE_CONTEXT = "show.ce.exchange.context.filter"
    FILTER_ES_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_ES_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_ID = "show.functional.exchanges.filter"
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_ES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_ES_SHOW_COMPONENT_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.component.exchanges.exchange.items.filter"
    )
    FILTER_ES_SHOW_CEPARAM_ID = "show.ce.param.filter"
    FILTER_ES_SHOW_CEEIPARAM_ID = "show.ce.ei.param.filter"
    FILTER_ES_SHOW_EXCHANGE_CONTEXT_ID = "show.exchange.context.filter"
    FILTER_ES_SHOW_CE_EXCHANGE_CONTEXT_ID = "show.ce.exchange.context.filter"
    FILTER_ES_SHOW_FE_EXCHANGE_CONTEXT_ID = "show.fe.exchange.context.filter"

    #  FCD filters - Functional Chain Description
    FILTER_FCD_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_FCD_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_FCD_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_FCD_HIDE_FUNCTIONAL_CHAIN_INVOLVEMENT_LINKS = (
        "hide.functional.chain.involvement.links.filter"
    )
    FILTER_FCD_HIDE_SEQUENCING_INFORMATION = (
        "hide.sequencing.information.filter"
    )
    FILTER_FCD_HIDE_COMPUTED_SEQUENCING_INFORMATION = (
        "hide.computed.sequencing.information.filter"
    )
    FILTER_FCD_HIDE_ASSOCIATION_LINKS = "hide.association.links.filter"
    FILTER_FCD_MERGE_FE_SL = "merge.associated.functional.exchange.involvements.and.sequence.links.without.control.node.filter"

    #  FS filters - Function Scenario
    FILTER_FS_HIDE_EXECUTIONS = "hide.executions.filter"
    FILTER_FS_HIDE_PRE_AND_POST_CONDITIONS = "hide.pre.post.conditions.filter"
    FILTER_FS_HIDE_PRE_AND_POST_CONDITIONS_ID = (
        "hide.pre.post.conditions.filter"
    )
    FILTER_FS_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_FS_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_FS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_FS_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_FS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_FS_SHOW_EXCHANGE_CONTEXT = "show.exchange.context.filter"
    FILTER_FS_SHOW_FE_EXCHANGE_CONTEXT = "show.fe.exchange.context.filter"
    FILTER_FS_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_FS_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_FS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_FS_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_FS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )

    # IDB filters - Interfaces Diagram Blank
    FILTER_IDB_HIDE_INTERFACE_CONTENTS = "hide.interface.contents.filter"
    FILTER_IDB_HIDE_INTERFACES = "hide.interfaces.filter"
    FILTER_IDB_HIDE_EXCHANGE_ITEMS_DETAILS_IN_INTERFACES = (
        "hide.exchange.items.details.in.interfaces.filter"
    )
    FILTER_IDB_HIDE_EXCHANGE_ITEM_ELEMENTS = (
        "hide.exchange.item.elements.filter"
    )
    FILTER_IDB_HIDE_EXCHANGE_ITEMS = "hide.exchange.items.filter"
    FILTER_IDB_HIDE_COMPONENT_PORTS = "hide.component.ports.filter"
    FILTER_IDB_HIDE_USE_LINKS = "hide.use.links.filter"
    FILTER_IDB_HIDE_IMPLEMENTATION_LINKS = "hide.implmentation.links.filter"
    FILTER_IDB_HIDE_PROVIDE_LINKS = "hide.provide.links.filter"
    FILTER_IDB_HIDE_REQUIRE_LINKS = "hide.require.links.filter"
    FILTER_IDB_HIDE_COMMUNICATION_LINKS = "hide.communication.links.filter"
    FILTER_IDB_HIDE_GENERALIZATION_LINKS = "hide.generalization.links.filter"
    FILTER_IDB_HIDE_PORT_DELEGATIONS = "hide.port.delegations.filter"
    FILTER_IDB_HIDE_SIMPLIFIED_MODEL_BASED_INTERACTIONS = (
        "hide.simplified.component.interactions.filter"
    )
    FILTER_IDB_HIDE_SIMPLIFIED_DIAGRAM_BASED_INTERACTIONS = (
        "hide.simplified.diagram.based.interactions.filter"
    )
    FILTER_IDB_HIDE_TECHNICALS_INTERFACES = "hide.technical.interfaces.filter"
    FILTER_IDB_HIDE_DELEGATED_COMMUNICATION_LINKS = (
        "hide.delegated.communication.links.filter"
    )
    FILTER_IDB_HIDE_DELEGATED_USE_IMPLEMENTATION_LINKS = (
        "hide.delegated.use.implementation.require.provide.links.filter"
    )
    FILTER_IDB_SHOW_MODIFIERS = "show.modifiers.filter"
    FILTER_IDB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  filter id
    FILTER_IDB_HIDE_IMPLEMENTATION_LINKS_ID = "hide.implmentation.links.filter"
    FILTER_IDB_HIDE_SIMPLIFIED_MODEL_BASED_INTERACTIONS_ID = (
        "hide.simplified.component.interactions.filter"
    )

    #  IS filters - Interface Scenario
    FILTER_IS_HIDE_EXECUTIONS = "hide.executions.filter"
    FILTER_IS_HIDE_CALL_ARGUMENTS = "hide.call.arguments.filter"
    FILTER_IS_HIDE_PRE_AND_POST_CONDITIONS = "hide.pre.post.conditions.filter"
    FILTER_IS_HIDE_PRE_AND_POST_CONDITIONS_ID = (
        "hide.pre.post.conditions.filter"
    )
    FILTER_IS_SHOW_EXCHANGE_CONTEXT = "show.ei.exchange.context.filter"
    FILTER_IS_SHOW_EXCHANGE_CONTEXT_ID = "show.ei.exchange.context.filter"

    #  XAB Filters
    FILTER_XAB_HIDE_SIMPLIFIED_DIAGRAM_BASED_COMPONENT_EXCHANGES = (
        "hide.simplified.diagram.based.component.exchanges.filter"
    )
    FILTER_XAB_HIDE_SIMPLIFIED_GROUP_OF_COMPONENT_EXCHANGES_ID = (
        "hide.simplified.group.of.component.exchanges.filter"
    )
    FILTER_XAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES = (
        "hide.simplified.oriented.grouped.component.exchanges.filter"
    )
    FILTER_XAB_HIDE_SEQUENCING_INFORMATION = (
        "hide.sequencing.information.filter"
    )

    #  LAB filters - Logical Architecture Blank
    FILTER_LAB_COLLAPSE_COMPONENT_PORTS = "collapse.component.ports.filter"
    FILTER_LAB_COLLAPSE_FUNCTION_PORTS = "collapse.function.ports.filter"
    FILTER_LAB_HIDE_FUNCTION_PORTS_WITHOUT_EXCHANGES = (
        "hide.function.ports.without.exchanges.filter"
    )
    FILTER_LAB_HIDE_COMPONENT_PORTS_WITHOUT_EXCHANGES = (
        "hide.component.ports.without.exchanges.filter"
    )
    FILTER_LAB_HIDE_ALLOCATED_FUNCTIONAL_EXCHANGES = (
        "hide.allocated.functional.exchanges.filter"
    )
    FILTER_LAB_HIDE_FUNCTIONS = "hide.functions.filter"
    FILTER_LAB_HIDE_FUNCTIONAL_EXCHANGES = "hide.functional.exchanges.filter"
    FILTER_LAB_HIDE_FUNCTIONAL_EXCHANGES_NAMES = (
        "hide.functional.exchanges.names.filter"
    )
    FILTER_LAB_HIDE_COMPONENT_EXCHANGES = "hide.connections.filter"
    FILTER_LAB_HIDE_COMPONENT_EXCHANGES_NAMES = (
        "hide.component.exchanges.names.filter"
    )
    FILTER_LAB_HIDE_PORT_ALLOCATIONS = "hide.port.realizations.filter"
    FILTER_LAB_HIDE_PORT_DELEGATIONS = "hide.port.delegations.filter"
    FILTER_LAB_HIDE_ALLOCATED_FUNCTION_PORTS = "hide.realized.ports.filter"
    FILTER_LAB_SHOW_EXCHANGE_ITEMS_ON_FUNCTIONAL_EXCHANGES = (
        "show.exchange.items.filter"
    )
    FILTER_LAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGES = (
        "show.exchange.items.on.component.exchanges.filter"
    )
    FILTER_LAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGE_WITHOUT_FUNCTIONAL_EXCHANGES = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"
    FILTER_LAB_SHOW_ALLOCATED_FUNCTIONAL_EXCHANGES_ON_COMPONENT_EXCHANGES = (
        "show.allocated.functional.exchanges.on.component.exchanges.filter"
    )
    FILTER_LAB_HIDE_CROSS_FUNCTIONAL_EXCHANGES_OF_REUSABLE_COMPONENTS = (
        "hide.cross.functional.exchanges.of.reusable.components.filter"
    )
    FILTER_LAB_HIDE_SIMPLIFIED_DIAGRAM_BASED_COMPONENT_EXCHANGES = FILTER_XAB_HIDE_SIMPLIFIED_DIAGRAM_BASED_COMPONENT_EXCHANGES  # $NON-NLS-1$
    FILTER_LAB_HIDE_SIMPLIFIED_GROUPED_COMPONENT_EXCHANGES = (
        "hide.simplified.group.of.component.exchanges.filter"
    )
    FILTER_LAB_HIDE_SIMPLIFIED_GROUP_OF_COMPONENT_EXCHANGES_ID = FILTER_XAB_HIDE_SIMPLIFIED_GROUP_OF_COMPONENT_EXCHANGES_ID  # $NON-NLS-1$
    FILTER_LAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES = FILTER_XAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES  # $NON-NLS-1$
    FILTER_LAB_HIDE_PHYSICAL_LINKS_NAME = "hide.physical.links.names.filter"
    FILTER_LAB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"
    FILTER_LAB_HIDE_SEQUENCING_INFORMATION = (
        "hide.sequencing.information.filter"
    )
    FILTER_XAB_HIDE_COMPUTED_CE = "hide.computed.component.exchanges.filter"
    FILTER_XAB_HIDE_COMPUTED_PL = "hide.computed.physical.links.filter"
    FILTER_LAB_HIDE_COMPUTED_CE = FILTER_XAB_HIDE_COMPUTED_CE
    FILTER_LAB_HIDE_COMPUTED_PL = FILTER_XAB_HIDE_COMPUTED_PL

    #  filter id
    FILTER_LAB_HIDE_COMPONENT_EXCHANGES_ID = "hide.connections.filter"
    FILTER_LAB_HIDE_PORT_ALLOCATIONS_ID = "hide.port.realizations.filter"
    FILTER_LAB_HIDE_ALLOCATED_FUNCTION_PORTS_ID = "hide.realized.ports.filter"
    FILTER_LAB_SHOW_EXCHANGE_ITEMS_ON_FUNCTIONAL_EXCHANGES_ID = (
        "show.exchange.items.filter"
    )
    FILTER_LAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGE_WITHOUT_FUNCTIONAL_EXCHANGES_ID = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"

    #  LCBD Filters
    FILTER_LCBD_HIDE_ROOT_CONTAINER = "hide.root.container.filter"
    FILTER_LCBD_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  LCCII filters - Logical Component Contextual Component Internal Interfaces
    FILTER_LCCII_HIDE_INTERFACES = "hide.interfaces.filter"
    FILTER_LCCII_HIDE_PORT_DELEGATIONS = "hide.port.delegations.filter"
    FILTER_LCCII_HIDE_SUBLINKS_WITH_INTERFACES = (
        "hide.sub-links.with.interfaces.filter"
    )
    FILTER_LCCII_HIDE_SUPERLINKS_WITH_INTERFACES = (
        "hide.super-links.with.interfaces.filter"
    )
    FILTER_LCCII_HIDE_EXCHANGE_ITEMS = "hide.exchange.items.filter"
    FILTER_LCCII_HIDE_EXCHANGEITEM_ALLOCATION = (
        "hide.exchange.item.allocation.filter"
    )
    FILTER_LCCII_HIDE_COMPONENT_PORTS = "hide.component.ports.filter"
    FILTER_LCCII_HIDE_USE_LINKS = "hide.use.links.filter"
    FILTER_LCCII_HIDE_IMPLEMENTATION_LINKS = "hide.implmentation.links.filter"
    FILTER_LCCII_HIDE_IMPLEMENTATION_LINKS_ID = (
        "hide.implmentation.links.filter"
    )
    FILTER_LCCII_HIDE_PROVIDE_LINKS = "hide.provide.links.filter"
    FILTER_LCCII_HIDE_REQUIRE_LINKS = "hide.require.links.filter"
    FILTER_LCCII_HIDE_COMMUNICATION_LINKS = "hide.communication.links.filter"
    FILTER_LCCII_HIDE_GENERALIZATION_LINKS = "hide.generalization.links.filter"
    FILTER_LCCII_HIDE_SIMPLIFIED_COMPONENT_INTERACTIONS = (
        "hide.simplified.component.interactions.filter"
    )
    FILTER_LCCII_HIDE_TECHNICALS_INTERFACES = (
        "hide.technical.interfaces.filter"
    )
    FILTER_LCCII_HIDE_DELEGATED_COMMUNICATION_LINKS = (
        "hide.delegated.communication.links.filter"
    )
    FILTER_LCCII_HIDE_DELEGATED_USE_IMPLEMENTATION_LINKS = (
        "hide.delegated.use.implementation.require.provide.links.filter"
    )
    FILTER_LCCII_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  LDFB filters - Logical Data Flow Blank
    FILTER_LDFB_COLLAPSE_PORTS = "collapse.ports.filter"
    FILTER_LDFB_HIDE_FUNCTIONAL_EXCHANGES = "hide.functional.exchanges.filter"
    FILTER_LDFB_HIDE_FUNCTIONAL_EXCHANGES_NAMES = (
        "hide.functional.exchanges.names.filter"
    )
    FILTER_LDFB_HIDE_FUNCTION_PORTS_WITHOUT_EXCHANGES = (
        "hide.function.ports.without.exchanges.filter"
    )
    FILTER_LDFB_HIDE_EXCHANGE_CATEGORIES = "hide.exchange.categories.filter"
    FILTER_LDFB_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_LDFB_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_LDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_LDFB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_LDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_LDFB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"
    FILTER_LDFB_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_LDFB_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_LDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_LDFB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_LDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )

    #  LFBD Filters
    FILTER_LFBD_HIDE_CONTROL_NODES = "hide.control.nodes.filter"
    FILTER_LFBD_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  MB filters - Missions Blank
    FILTER_MB_HIDE_CAPABILITIES = "hide.capabilities.filter"
    FILTER_MB_HIDE_CAPABILITY_EXPLOITATION = (
        "hide.capability.exploitations.filter"
    )
    FILTER_MB_HIDE_CAPABILITY_GENERALIZATIONS = (
        "hide.capability.generalizations.filter"
    )
    FILTER_MB_HIDE_MISSIONS = "hide.missions.filter"
    FILTER_MB_HIDE_ACTORS = "hide.actors.filter"
    FILTER_MB_HIDE_ACTOR_INVOLVEMENTS = "hide.actor.involvements.filter"
    FILTER_MB_HIDE_ACTOR_GENERALIZATIONS = "hide.actor.generalizations.filter"
    FILTER_MB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  MCB filters - Mission Capabilities Blank
    FILTER_MCB_HIDE_CAPABILITIES = "hide.capabilities.filter"
    FILTER_MCB_HIDE_CAPABILITY_EXPLOITATIONS = (
        "hide.capability.exploitations.filter"
    )
    FILTER_MCB_HIDE_CAPABILITY_EXTENDS = "hide.capability.extends.filter"
    FILTER_MCB_HIDE_CAPABILITY_INCLUDES = "hide.capability.includes.filter"
    FILTER_MCB_HIDE_CAPABILITY_GENERALIZATIONS = (
        "hide.capability.generalizations.filter"
    )
    FILTER_MCB_HIDE_MISSIONS = "hide.missions.filter"
    FILTER_MCB_HIDE_ACTORS = "hide.actors.filter"
    FILTER_MCB_HIDE_ACTOR_MISSION_INVOLVEMENTS = (
        "hide.actor.mission.involvements.filter"
    )
    FILTER_MCB_HIDE_ACTOR_CAPABILITY_INVOLVEMENTS = (
        "hide.actor.capability.involvements.filter"
    )
    FILTER_MCB_HIDE_ACTOR_GENERALIZATIONS = "hide.actor.generalizations.filter"
    FILTER_MCB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  M&S filters - Modes and States
    FILTER_MS_HIDE_INTERNAL_STATES = "hide.internal.states.filter"
    FILTER_MS_HIDEINTERNALSTATES_ID = "HideInternalStates"
    FILTER_MSM_HIDECOMPUTEDTRANSITIONS_ID = "hide.computed.transitions.filter"

    #  New Capability Realization Refinement
    FILTER_NEWCAPABILITYREALIZATIONREFINEMENT_HIDE_ACTORS = (
        "hide.actors.filter"
    )

    #  OAB filters - Operational Architecture Blank
    FILTER_OAB_HIDE_ALLOCATED_INTERACTIONS = (
        "hide.allocated.interactions.filter"
    )
    FILTER_OAB_HIDE_OPERATIONAL_ACTIVITIES = (
        "hide.operational.activities.filter"
    )
    FILTER_OAB_HIDE_ROLES = "hide.roles.filter"
    FILTER_OAB_HIDE_OPERATIONAL_ACTORS = "hide.operational.actors.filter"
    FILTER_OAB_HIDE_INTERACTIONS = "hide.interactions.filter"
    FILTER_OAB_HIDE_INTERACTIONS_NAMES = "hide.interactions.names.filter"
    FILTER_OAB_HIDE_COMMUNICATION_MEANS = "hide.communication.means.filter"
    FILTER_OAB_HIDE_COMMUNICATION_MEANS_NAMES = (
        "hide.communication.means.names.filter"
    )
    FILTER_OAB_SHOW_EXCHANGE_ITEMS_ON_INTERACTIONS = (
        "show.exchange.items.filter"
    )
    FILTER_OAB_SHOW_EXCHANGE_ITEM_ON_COMMUNICATION_MEANS = (
        "show.exchange.items.on.component.exchanges.filter"
    )
    FILTER_OAB_SHOW_EXCHANGE_ITEM_ON_COMMUNICATION_MEANS_WITHOUT_INTERACTIONS = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"
    FILTER_OAB_SHOW_ALLOCATED_INTERACTIONS_ON_COMMUNICATION_MEANS = (
        "show.allocated.functional.exchanges.on.component.exchanges.filter"
    )
    FILTER_OAB_HIDE_CROSS_INTEREACTIONS_OF_ROLES = (
        "hide.cross.functional.exchanges.of.reusable.components.filter"
    )
    FILTER_OAB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"
    FILTER_OAB_HIDE_SEQUENCING_INFORMATION = (
        "hide.sequencing.information.filter"
    )

    #  filter id
    FILTER_OAB_SHOW_EXCHANGE_ITEMS_ON_INTERACTIONS_ID = (
        "show.exchange.items.filter"
    )
    FILTER_OAB_SHOW_EXCHANGE_ITEM_ON_COMMUNICATION_MEANS_ID = (
        "show.exchange.items.on.component.exchanges.filter"
    )
    FILTER_OAB_SHOW_EXCHANGE_ITEM_ON_COMMUNICATION_MEANS_WITHOUT_INTERACTIONS_ID = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"
    FILTER_OAB_SHOW_ALLOCATED_INTERACTIONS_ON_COMMUNICATION_MEANS_ID = (
        "show.allocated.functional.exchanges.on.component.exchanges.filter"
    )
    FILTER_OAB_HIDE_CROSS_INTEREACTIONS_OF_ROLES_ID = (
        "hide.cross.functional.exchanges.of.reusable.components.filter"
    )
    FILTER_OAB_HIDE_INTERACTIONS_NAMES_ID = "hide.interactions.names.filter"
    FILTER_OAB_HIDE_COMMUNICATION_MEANS_NAMES_ID = (
        "hide.communication.means.names.filter"
    )

    # OAIB filters - Operational Activity Interaction Blank
    FILTER_OAIB_HIDE_INTERACTIONS = "hide.interactions.filter"
    FILTER_OAIB_HIDE_INTERACTIONS_NAMES = "hide.interactions.names.filter"
    FILTER_OAIB_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_OAIB_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_OAIB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_OAIB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_OAIB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )

    #  filter id
    FILTER_OAIB_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_OAIB_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_OAIB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_OAIB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_OAIB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )

    #  OCB filters - Operational Capabilities Blank
    FILTER_OCB_HIDE_COMMUNICATION_MEANS = "hide.communication.means.filter"
    FILTER_OCB_HIDE_INVOLVEMENT_LINKS = "hide.involvement.links.filter"
    FILTER_OCB_HIDE_OPERATIONAL_CAPABILITY_EXTENDS = (
        "hide.operational.capability.extends.filter"
    )
    FILTER_OCB_HIDE_OPERATIONAL_CAPABILITY_INCLUDES = (
        "hide.operational.capability.includes.filter"
    )
    FILTER_OCB_HIDE_OPERATIONAL_CAPABILITY_GENERALIZATIONS = (
        "hide.operational.capability.generalizations.filter"
    )
    FILTER_OCB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  OAS filters - Operational Activity Scenario
    FILTER_OAS_HIDE_EXECUTIONS = "hide.executions.filter"
    FILTER_OAS_HIDE_PRE_AND_POST_CONDITIONS = "hide.pre.post.conditions.filter"
    FILTER_OAS_HIDE_PRE_AND_POST_CONDITIONS_ID = (
        "hide.pre.post.conditions.filter"
    )
    FILTER_OAS_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_OAS_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_OAS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_OAS_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_OAS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_OAS_SHOW_CEEIPARAM = "show.ce.ei.param.filter"
    FILTER_OAS_SHOW_I_EXCHANGE_CONTEXT = "show.fe.exchange.context.filter"
    FILTER_OAS_SHOW_EXCHANGE_CONTEXT = "show.exchange.context.filter"
    FILTER_OAS_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_OAS_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_OAS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_OAS_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_OAS_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )

    #  OEB filters - Operational Entity Blank
    FILTER_OEB_HIDE_OPERATIONAL_ACTIVITIES = (
        "hide.operational.activities.filter"
    )
    FILTER_OEB_HIDE_ROLES = "hide.roles.filter"
    FILTER_OEB_HIDE_OPERATIONAL_ACTORS = "hide.operational.actors.filter"
    FILTER_OEB_HIDE_INTERACTIONS = "Hide Interactions"
    FILTER_OEB_HIDE_COMMUNICATION_MEANS = "Hide Communication Means"
    FILTER_OEB_SHOW_EXCHANGE_ITEMS_ON_INTERACTIONS = (
        "show.exchange.items.filter"
    )
    FILTER_OEB_SHOW_EXCHANGE_ITEM_ON_COMMUNICATION_MEANS = (
        "show.exchange.items.on.component.exchanges.filter"
    )
    FILTER_OEB_SHOW_EXCHANGE_ITEM_ON_COMMUNICATION_MEANS_WITHOUT_INTERACTIONS = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"
    FILTER_OEB_SHOW_ALLOCATED_INTERACTIONS_ON_COMMUNICATION_MEANS = (
        "show.allocated.functional.exchanges.on.component.exchanges.filter"
    )
    FILTER_OEB_HIDE_CROSS_INTEREACTIONS_OF_ROLES = (
        "hide.cross.functional.exchanges.of.reusable.components.filter"
    )

    #  OES filters - Operational Entity Scenario
    FILTER_OES_HIDE_EXECUTIONS = "hide.executions.filter"
    FILTER_OES_HIDE_PRE_AND_POST_CONDITIONS = "hide.pre.post.conditions.filter"
    FILTER_OES_HIDE_PRE_AND_POST_CONDITIONS_ID = (
        "hide.pre.post.conditions.filter"
    )
    FILTER_OES_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_OES_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES = "show.functional.exchanges.filter"
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_OES_SHOW_COMPONENT_EXCHANGES_EXCHANGEITEMS = (
        "show.component.exchanges.exchange.items.filter"
    )
    FILTER_OES_SHOW_CEPARAM = "show.ce.param.filter"
    FILTER_OES_SHOW_CEEIPARAM = "show.ce.ei.param.filter"
    FILTER_OES_SHOW_I_EXCHANGE_CONTEXT = "show.fe.exchange.context.filter"
    FILTER_OES_SHOW_EXCHANGE_CONTEXT = "show.exchange.context.filter"
    FILTER_OES_SHOW_CM_EXCHANGE_CONTEXT = "show.ce.exchange.context.filter"

    #  filter id
    FILTER_OES_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_OES_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_ID = (
        "show.functional.exchanges.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_OES_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_OES_SHOW_COMPONENT_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.component.exchanges.exchange.items.filter"
    )
    FILTER_OES_SHOW_CEPARAM_ID = "show.ce.param.filter"
    FILTER_OES_SHOW_CEEIPARAM_ID = "show.ce.ei.param.filter"

    #  ORB filters - Operational Role Blank
    FILTER_ORB_HIDE_ALLOCATED_INTERACTIONS = (
        "hide.allocated.interactions.filter"
    )
    FILTER_ORB_HIDE_INTERACTIONS = "hide.interactions.filter"
    FILTER_ORB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    # PAB filters - Physical Architecture Blank
    FILTER_PAB_COLLAPSE_COMPONENT_PHYSICAL_PORTS = (
        "collapse.component.physical.ports.filter"
    )
    FILTER_PAB_COLLAPSE_COMPONENT_PORTS = "collapse.component.ports.filter"
    FILTER_PAB_COLLAPSE_FUNCTION_PORTS = "collapse.function.ports.filter"
    FILTER_PAB_HIDE_FUNCTION_PORTS_WITHOUT_EXCHANGES = (
        "hide.function.ports.without.exchanges.filter"
    )
    FILTER_PAB_HIDE_COMPONENT_PORTS_WITHOUT_EXCHANGES = (
        "hide.component.ports.without.exchanges.filter"
    )
    FILTER_PAB_HIDE_PHYSICAL_PORTS_WITHOUT_LINKS = (
        "hide.physical.ports.without.links.filter"
    )
    FILTER_PAB_HIDE_ALLOCATED_FUNCTION_ON_PARENT_CONTAINERS = (
        "hide.allocated.function.on.parent.containers.filter"
    )
    FILTER_PAB_HIDE_ALLOCATED_FUNCTIONAL_EXCHANGES = (
        "hide.allocated.functional.exchanges.filter"
    )
    FILTER_PAB_HIDE_FUNCTIONS = "hide.functions.filter"
    FILTER_PAB_HIDE_FUNCTIONAL_EXCHANGES = "hide.functional.exchanges.filter"
    FILTER_PAB_HIDE_FUNCTIONAL_EXCHANGES_NAMES = (
        "hide.functional.exchanges.names.filter"
    )
    FILTER_PAB_HIDE_COMPONENT_EXCHANGES = "hide.connections.filter"
    FILTER_PAB_HIDE_COMPONENT_EXCHANGES_NAMES = (
        "hide.component.exchanges.names.filter"
    )
    FILTER_PAB_HIDE_PHYSICAL_LINKS = "hide.physical.links.filter"
    FILTER_PAB_HIDE_PHYSICAL_LINKS_NAMES = "hide.physical.links.names.filter"
    FILTER_PAB_HIDE_PORT_ALLOCATIONS = "hide.port.realizations.filter"
    FILTER_PAB_HIDE_PORT_DELEGATIONS = "hide.port.delegations.filter"
    FILTER_PAB_HIDE_COMPONENT_PORT_ALLOCATIONS = (
        "hide.component.port.allocations.filter"
    )
    FILTER_PAB_HIDE_ALLOCATED_FUNCTION_PORTS = "hide.realized.ports.filter"
    FILTER_PAB_HIDE_NODE_PCS = "hide.node.pcs.filter"
    FILTER_PAB_HIDE_BEHAVIOR_PCS = "hide.behavior.pcs.filter"
    FILTER_PAB_HIDE_PHYSICAL_ACTORS = "hide.physical.actors.filter"
    FILTER_PAB_HIDE_DEPLOYED_PCS = "hide.deployed.pcs.filter"
    FILTER_PAB_SHOW_EXCHANGE_ITEMS_ON_FUNCTIONAL_EXCHANGES = (
        "show.exchange.items.filter"
    )
    FILTER_PAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGES = (
        "show.exchange.items.on.component.exchanges.filter"
    )
    FILTER_PAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGE_WITHOUT_FUNCTIONAL_EXCHANGES = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"
    FILTER_PAB_SHOW_ALLOCATED_FUNCTIONAL_EXCHANGES_ON_COMPONENT_EXCHANGES = (
        "show.allocated.functional.exchanges.on.component.exchanges.filter"
    )
    FILTER_PAB_HIDE_CROSS_FUNCTIONAL_EXCHANGES_OF_REUSABLE_COMPONENTS = (
        "hide.cross.functional.exchanges.of.reusable.components.filter"
    )
    FILTER_PAB_HIDE_SIMPLIFIED_DIAGRAM_BASED_COMPONENT_EXCHANGES = FILTER_XAB_HIDE_SIMPLIFIED_DIAGRAM_BASED_COMPONENT_EXCHANGES  # $NON-NLS-1$
    FILTER_PAB_HIDE_SIMPLIFIED_GROUPED_COMPONENT_EXCHANGES = (
        "hide.simplified.group.of.component.exchanges.filter"
    )
    FILTER_PAB_HIDE_SIMPLIFIED_GROUP_OF_COMPONENT_EXCHANGES_ID = FILTER_XAB_HIDE_SIMPLIFIED_GROUP_OF_COMPONENT_EXCHANGES_ID  # $NON-NLS-1$
    FILTER_PAB_HIDE_PORT_REALIZATIONS_ID = "hide.port.realizations.filter"
    FILTER_PAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES = FILTER_XAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES  # $NON-NLS-1$
    FILTER_PAB_HIDE_COMPUTED_CE = FILTER_XAB_HIDE_COMPUTED_CE
    FILTER_PAB_HIDE_COMPUTED_PL = FILTER_XAB_HIDE_COMPUTED_PL
    FILTER_PAB_HIDE_SEQUENCING_INFORMATION = (
        "hide.sequencing.information.filter"
    )
    FILTER_PAB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  filter id
    FILTER_PAB_HIDE_COMPONENT_EXCHANGES_ID = "hide.connections.filter"
    FILTER_PAB_HIDE_PORT_ALLOCATIONS_ID = "hide.port.realizations.filter"
    FILTER_PAB_HIDE_ALLOCATED_FUNCTION_PORTS_ID = "hide.realized.ports.filter"
    FILTER_PAB_SHOW_EXCHANGE_ITEMS_ON_FUNCTIONAL_EXCHANGES_ID = (
        "show.exchange.items.filter"
    )
    FILTER_PAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGE_WITHOUT_FUNCTIONAL_EXCHANGES_ID = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"

    #  PDFB filters - Physical Data Flow Blank
    FILTER_PDFB_COLLAPSE_PORTS = "collapse.ports.filter"
    FILTER_PDFB_HIDE_FUNCTIONAL_EXCHANGES = "hide.functional.exchanges.filter"
    FILTER_PDFB_HIDE_FUNCTIONAL_EXCHANGES_NAMES = (
        "hide.functional.exchanges.names.filter"
    )
    FILTER_PDFB_HIDE_FUNCTION_PORTS_WITHOUT_EXCHANGES = (
        "hide.function.ports.without.exchanges.filter"
    )
    FILTER_PDFB_HIDE_EXCHANGE_CATEGORIES = "hide.exchange.categories.filter"
    FILTER_PDFB_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_PDFB_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_PDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_PDFB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_PDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_PDFB_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_PDFB_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_PDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_PDFB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_PDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_PDFB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  PFBD Filters
    FILTER_PFBD_HIDE_CONTROL_NODES = "hide.control.nodes.filter"
    FILTER_PFBD_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  SAB filters - System Architecture Blank
    FILTER_SAB_COLLAPSE_COMPONENT_PORTS = "collapse.component.ports.filter"
    FILTER_SAB_COLLAPSE_FUNCTION_PORTS = "collapse.function.ports.filter"
    FILTER_SAB_HIDE_FUNCTION_PORTS_WITHOUT_EXCHANGES = (
        "hide.function.ports.without.exchanges.filter"
    )
    FILTER_SAB_HIDE_COMPONENT_PORTS_WITHOUT_EXCHANGES = (
        "hide.component.ports.without.exchanges.filter"
    )
    FILTER_SAB_HIDE_ALLOCATED_FUNCTIONAL_EXCHANGES = (
        "hide.allocated.functional.exchanges.filter"
    )
    FILTER_SAB_HIDE_FUNCTIONS = "hide.functions.filter"
    FILTER_SAB_HIDE_FUNCTIONAL_EXCHANGES = "hide.functional.exchanges.filter"
    FILTER_SAB_HIDE_FUNCTIONAL_EXCHANGES_NAMES = (
        "hide.functional.exchanges.names.filter"
    )
    FILTER_SAB_HIDE_COMPONENT_EXCHANGES = "hide.connections.filter"
    FILTER_SAB_HIDE_COMPONENT_EXCHANGES_NAMES = (
        "hide.component.exchanges.names.filter"
    )
    FILTER_SAB_HIDE_PHYSICAL_LINKS_NAMES = "hide.physical.links.names.filter"
    FILTER_SAB_HIDE_PORT_ALLOCATIONS = "hide.port.realizations.filter"
    FILTER_SAB_HIDE_ALLOCATED_FUNCTION_PORTS = "hide.realized.ports.filter"
    FILTER_SAB_SHOW_EXCHANGE_ITEMS_ON_FUNCTIONAL_EXCHANGES = (
        "show.exchange.items.filter"
    )
    FILTER_SAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGES = (
        "show.exchange.items.on.component.exchanges.filter"
    )
    FILTER_SAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGE_WITHOUT_FUNCTIONAL_EXCHANGES = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"
    FILTER_SAB_SHOW_ALLOCATED_FUNCTIONAL_EXCHANGES_ON_COMPONENT_EXCHANGES = (
        "show.allocated.functional.exchanges.on.component.exchanges.filter"
    )
    FILTER_SAB_HIDE_CROSS_FUNCTIONAL_EXCHANGES_OF_REUSABLE_COMPONENTS = (
        "hide.cross.functional.exchanges.of.reusable.components.filter"
    )
    FILTER_SAB_HIDE_SIMPLIFIED_GROUPED_COMPONENT_EXCHANGES = (
        "hide.simplified.group.of.component.exchanges.filter"
    )
    FILTER_SAB_HIDE_SIMPLIFIED_GROUPED_COMPONENT_EXCHANGES_ID = FILTER_XAB_HIDE_SIMPLIFIED_GROUP_OF_COMPONENT_EXCHANGES_ID  # $NON-NLS-1$
    FILTER_SAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES = FILTER_XAB_HIDE_SIMPLIFIED_ORIENTED_GROUPED_COMPONENT_EXCHANGES  # $NON-NLS-1$
    FILTER_SAB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"
    FILTER_SAB_HIDE_SEQUENCING_INFORMATION = (
        "hide.sequencing.information.filter"
    )

    #  filter id
    FILTER_SAB_HIDE_COMPONENT_EXCHANGES_ID = "hide.connections.filter"
    FILTER_SAB_HIDE_PORT_ALLOCATIONS_ID = "hide.port.realizations.filter"
    FILTER_SAB_HIDE_ALLOCATED_FUNCTION_PORTS_ID = "hide.realized.ports.filter"
    FILTER_SAB_SHOW_EXCHANGE_ITEMS_ON_FUNCTIONAL_EXCHANGES_ID = (
        "show.exchange.items.filter"
    )
    FILTER_SAB_SHOW_EXCHANGE_ITEMS_ON_COMPONENT_EXCHANGE_WITHOUT_FUNCTIONAL_EXCHANGES_ID = "show.exchange.items.on.component.exchange.without.functional.exchanges.filter"

    #  SDFB filters - System Data Flow Bank
    FILTER_SDFB_COLLAPSE_PORTS = "collapse.ports.filter"
    FILTER_SDFB_HIDE_FUNCTIONAL_EXCHANGES = "hide.functional.exchanges.filter"
    FILTER_SDFB_HIDE_FUNCTIONAL_EXCHANGES_NAMES = (
        "hide.functional.exchanges.names.filter"
    )
    FILTER_SDFB_HIDE_FUNCTION_PORTS_WITHOUT_EXCHANGES = (
        "hide.function.ports.without.exchanges.filter"
    )
    FILTER_SDFB_HIDE_EXCHANGE_CATEGORIES = "hide.exchange.categories.filter"
    FILTER_SDFB_SHOW_EXCHANGEITEMS = "show.exchange.items.filter"
    FILTER_SDFB_SHOW_EXCHANGEITEMS_PARAMETERS = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_SDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_SDFB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_SDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )
    FILTER_SDFB_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  filter id
    FILTER_SDFB_SHOW_EXCHANGEITEMS_ID = "show.exchange.items.filter"
    FILTER_SDFB_SHOW_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.exchange.items.parameters.filter"
    )
    FILTER_SDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_ID = (
        "show.functional.exchanges.exchange.items.filter"
    )
    FILTER_SDFB_SHOW_FUNCTIONAL_EXCHANGES_PARAMETERS_ID = (
        "show.functional.exchanges.parameters.filter"
    )
    FILTER_SDFB_SHOW_FUNCTIONAL_EXCHANGES_EXCHANGEITEMS_PARAMETERS_ID = (
        "show.functional.exchanges.exchange.items.parameters.filter"
    )

    #  SFBD filters - System Function Breakdown
    FILTER_SFBD_HIDE_CONTROL_NODES = "hide.control.nodes.filter"
    FILTER_SFBD_HIDE_PROPERTY_VALUES = "hide.property.values.filter"

    #  Exchange Context filters
    FILTER_SHOW_EXCHANGE_CONTEXT_ID = "show.exchange.context.filter"
    FILTER_SHOW_CE_EXCHANGE_CONTEXT_ID = "show.ce.exchange.context.filter"
    FILTER_SHOW_FE_EXCHANGE_CONTEXT_ID = "show.fe.exchange.context.filter"
    FILTER_SHOW_EI_EXCHANGE_CONTEXT_ID = "show.ei.exchange.context.filter"
    FILTER_FUNCTIONAL_CHAINS_INTERNAL_LINKS_ID = (
        "hide.functional.chains.internal.links.filter"
    )
    FILTER_PHYSICAL_PATHS_INTERNAL_LINKS_ID = (
        "hide.physical.paths.internal.links.filter"
    )
    FILTER_MERGE_ASSOCIATED_FE_AND_SL = "merge.associated.functional.exchange.involvements.and.sequence.links.without.control.node.filter"
