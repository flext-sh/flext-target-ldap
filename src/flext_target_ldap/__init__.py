# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext target ldap package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes
    from flext_ldap import d, e, h, x

    from flext_target_ldap import application, infrastructure, patterns, singer
    from flext_target_ldap.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_target_ldap.application.orchestrator import LDAPTargetOrchestrator
    from flext_target_ldap.catalog import build_singer_catalog
    from flext_target_ldap.client import LDAPClient, LDAPConnection, LDAPSearchEntry
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants,
        FlextTargetLdapConstants as c,
    )
    from flext_target_ldap.infrastructure.di_container import (
        configure_flext_target_ldap_dependencies,
        get_flext_target_ldap_container,
        get_flext_target_ldap_service,
    )
    from flext_target_ldap.models import (
        FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )
    from flext_target_ldap.patterns.ldap_patterns import (
        LDAPDataTransformer,
        LDAPEntryManager,
        LDAPSchemaMapper,
        LDAPTypeConverter,
        SingerPropertyDefinition,
        SingerSchemaDefinition,
    )
    from flext_target_ldap.processing_result import LdapProcessingCounters
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )
    from flext_target_ldap.settings import (
        FlextTargetLdapSettings,
        LDAPConnectionSettings,
        LDAPOperationSettings,
        validate_ldap_config,
    )
    from flext_target_ldap.singer.catalog import (
        SingerLDAPCatalogEntry,
        SingerLDAPCatalogManager,
    )
    from flext_target_ldap.singer.stream import (
        LDAPStreamProcessingStats,
        SingerLDAPStreamProcessor,
    )
    from flext_target_ldap.singer.target import SingerTargetLDAP
    from flext_target_ldap.sinks import (
        GroupsSink,
        LDAPBaseSink,
        LDAPProcessingResult,
        LDAPProcessingResult as r,
        OrganizationalUnitsSink,
        Sink,
        Target,
        UsersSink,
    )
    from flext_target_ldap.target import TargetLDAP, flext_cli_create_helper, main
    from flext_target_ldap.target_client import (
        LdapBaseSink,
        LdapGroupsSink,
        LdapOrganizationalUnitsSink,
        LdapProcessingResult,
        LdapSearchEntry,
        LdapTargetClient,
        LdapUsersSink,
        TargetLdap,
    )
    from flext_target_ldap.target_config import (
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )
    from flext_target_ldap.target_exceptions import (
        FlextTargetLdapAuthenticationError,
        FlextTargetLdapConnectionError,
        FlextTargetLdapError,
        FlextTargetLdapProcessingError,
        FlextTargetLdapSettingsurationError,
        FlextTargetLdapTimeoutError,
        FlextTargetLdapValidationError,
    )
    from flext_target_ldap.target_models import (
        LdapAttributeMappingModel,
        LdapBatchProcessingModel,
        LdapEntryModel,
        LdapOperationStatisticsModel,
        LdapTransformationResultModel,
    )
    from flext_target_ldap.target_services import (
        LdapConnectionService,
        LdapConnectionService as s,
        LdapTargetApiService,
        LdapTargetOrchestrator,
        LdapTargetService,
        LdapTransformationService,
    )
    from flext_target_ldap.transformation import (
        DataTransformationEngine,
        MigrationValidator,
        TransformationResult,
        TransformationRule,
        logger,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes,
        FlextTargetLdapTypes as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "DataTransformationEngine": (
        "flext_target_ldap.transformation",
        "DataTransformationEngine",
    ),
    "FlextTargetLdapAuthenticationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapAuthenticationError",
    ),
    "FlextTargetLdapConnectionError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapConnectionError",
    ),
    "FlextTargetLdapConstants": (
        "flext_target_ldap.constants",
        "FlextTargetLdapConstants",
    ),
    "FlextTargetLdapError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapError",
    ),
    "FlextTargetLdapModels": ("flext_target_ldap.models", "FlextTargetLdapModels"),
    "FlextTargetLdapProcessingError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapProcessingError",
    ),
    "FlextTargetLdapProtocols": (
        "flext_target_ldap.protocols",
        "FlextTargetLdapProtocols",
    ),
    "FlextTargetLdapSettings": (
        "flext_target_ldap.settings",
        "FlextTargetLdapSettings",
    ),
    "FlextTargetLdapSettingsurationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapSettingsurationError",
    ),
    "FlextTargetLdapTimeoutError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapTimeoutError",
    ),
    "FlextTargetLdapTypes": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
    "FlextTargetLdapUtilities": (
        "flext_target_ldap.utilities",
        "FlextTargetLdapUtilities",
    ),
    "FlextTargetLdapValidationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapValidationError",
    ),
    "GroupsSink": ("flext_target_ldap.sinks", "GroupsSink"),
    "LDAPBaseSink": ("flext_target_ldap.sinks", "LDAPBaseSink"),
    "LDAPClient": ("flext_target_ldap.client", "LDAPClient"),
    "LDAPConnection": ("flext_target_ldap.client", "LDAPConnection"),
    "LDAPConnectionSettings": ("flext_target_ldap.settings", "LDAPConnectionSettings"),
    "LDAPDataTransformer": (
        "flext_target_ldap.patterns.ldap_patterns",
        "LDAPDataTransformer",
    ),
    "LDAPEntryManager": (
        "flext_target_ldap.patterns.ldap_patterns",
        "LDAPEntryManager",
    ),
    "LDAPOperationSettings": ("flext_target_ldap.settings", "LDAPOperationSettings"),
    "LDAPProcessingResult": ("flext_target_ldap.sinks", "LDAPProcessingResult"),
    "LDAPSchemaMapper": (
        "flext_target_ldap.patterns.ldap_patterns",
        "LDAPSchemaMapper",
    ),
    "LDAPSearchEntry": ("flext_target_ldap.client", "LDAPSearchEntry"),
    "LDAPStreamProcessingStats": (
        "flext_target_ldap.singer.stream",
        "LDAPStreamProcessingStats",
    ),
    "LDAPTargetOrchestrator": (
        "flext_target_ldap.application.orchestrator",
        "LDAPTargetOrchestrator",
    ),
    "LDAPTypeConverter": (
        "flext_target_ldap.patterns.ldap_patterns",
        "LDAPTypeConverter",
    ),
    "LdapAttributeMappingModel": (
        "flext_target_ldap.target_models",
        "LdapAttributeMappingModel",
    ),
    "LdapBaseSink": ("flext_target_ldap.target_client", "LdapBaseSink"),
    "LdapBatchProcessingModel": (
        "flext_target_ldap.target_models",
        "LdapBatchProcessingModel",
    ),
    "LdapConnectionService": (
        "flext_target_ldap.target_services",
        "LdapConnectionService",
    ),
    "LdapEntryModel": ("flext_target_ldap.target_models", "LdapEntryModel"),
    "LdapGroupsSink": ("flext_target_ldap.target_client", "LdapGroupsSink"),
    "LdapOperationStatisticsModel": (
        "flext_target_ldap.target_models",
        "LdapOperationStatisticsModel",
    ),
    "LdapOrganizationalUnitsSink": (
        "flext_target_ldap.target_client",
        "LdapOrganizationalUnitsSink",
    ),
    "LdapProcessingCounters": (
        "flext_target_ldap.processing_result",
        "LdapProcessingCounters",
    ),
    "LdapProcessingResult": ("flext_target_ldap.target_client", "LdapProcessingResult"),
    "LdapSearchEntry": ("flext_target_ldap.target_client", "LdapSearchEntry"),
    "LdapTargetApiService": (
        "flext_target_ldap.target_services",
        "LdapTargetApiService",
    ),
    "LdapTargetClient": ("flext_target_ldap.target_client", "LdapTargetClient"),
    "LdapTargetOrchestrator": (
        "flext_target_ldap.target_services",
        "LdapTargetOrchestrator",
    ),
    "LdapTargetService": ("flext_target_ldap.target_services", "LdapTargetService"),
    "LdapTransformationResultModel": (
        "flext_target_ldap.target_models",
        "LdapTransformationResultModel",
    ),
    "LdapTransformationService": (
        "flext_target_ldap.target_services",
        "LdapTransformationService",
    ),
    "LdapUsersSink": ("flext_target_ldap.target_client", "LdapUsersSink"),
    "MigrationValidator": ("flext_target_ldap.transformation", "MigrationValidator"),
    "OrganizationalUnitsSink": ("flext_target_ldap.sinks", "OrganizationalUnitsSink"),
    "SingerLDAPCatalogEntry": (
        "flext_target_ldap.singer.catalog",
        "SingerLDAPCatalogEntry",
    ),
    "SingerLDAPCatalogManager": (
        "flext_target_ldap.singer.catalog",
        "SingerLDAPCatalogManager",
    ),
    "SingerLDAPStreamProcessor": (
        "flext_target_ldap.singer.stream",
        "SingerLDAPStreamProcessor",
    ),
    "SingerPropertyDefinition": (
        "flext_target_ldap.patterns.ldap_patterns",
        "SingerPropertyDefinition",
    ),
    "SingerSchemaDefinition": (
        "flext_target_ldap.patterns.ldap_patterns",
        "SingerSchemaDefinition",
    ),
    "SingerTargetLDAP": ("flext_target_ldap.singer.target", "SingerTargetLDAP"),
    "Sink": ("flext_target_ldap.sinks", "Sink"),
    "Target": ("flext_target_ldap.sinks", "Target"),
    "TargetLDAP": ("flext_target_ldap.target", "TargetLDAP"),
    "TargetLdap": ("flext_target_ldap.target_client", "TargetLdap"),
    "TransformationResult": (
        "flext_target_ldap.transformation",
        "TransformationResult",
    ),
    "TransformationRule": ("flext_target_ldap.transformation", "TransformationRule"),
    "UsersSink": ("flext_target_ldap.sinks", "UsersSink"),
    "__all__": ("flext_target_ldap.__version__", "__all__"),
    "__author__": ("flext_target_ldap.__version__", "__author__"),
    "__author_email__": ("flext_target_ldap.__version__", "__author_email__"),
    "__description__": ("flext_target_ldap.__version__", "__description__"),
    "__license__": ("flext_target_ldap.__version__", "__license__"),
    "__title__": ("flext_target_ldap.__version__", "__title__"),
    "__url__": ("flext_target_ldap.__version__", "__url__"),
    "__version__": ("flext_target_ldap.__version__", "__version__"),
    "__version_info__": ("flext_target_ldap.__version__", "__version_info__"),
    "application": ("flext_target_ldap.application", ""),
    "build_singer_catalog": ("flext_target_ldap.catalog", "build_singer_catalog"),
    "c": ("flext_target_ldap.constants", "FlextTargetLdapConstants"),
    "configure_flext_target_ldap_dependencies": (
        "flext_target_ldap.infrastructure.di_container",
        "configure_flext_target_ldap_dependencies",
    ),
    "create_default_ldap_target_config": (
        "flext_target_ldap.target_config",
        "create_default_ldap_target_config",
    ),
    "d": ("flext_ldap", "d"),
    "e": ("flext_ldap", "e"),
    "flext_cli_create_helper": ("flext_target_ldap.target", "flext_cli_create_helper"),
    "get_flext_target_ldap_container": (
        "flext_target_ldap.infrastructure.di_container",
        "get_flext_target_ldap_container",
    ),
    "get_flext_target_ldap_service": (
        "flext_target_ldap.infrastructure.di_container",
        "get_flext_target_ldap_service",
    ),
    "h": ("flext_ldap", "h"),
    "infrastructure": ("flext_target_ldap.infrastructure", ""),
    "logger": ("flext_target_ldap.transformation", "logger"),
    "m": ("flext_target_ldap.models", "FlextTargetLdapModels"),
    "main": ("flext_target_ldap.target", "main"),
    "p": ("flext_target_ldap.protocols", "FlextTargetLdapProtocols"),
    "patterns": ("flext_target_ldap.patterns", ""),
    "r": ("flext_target_ldap.sinks", "LDAPProcessingResult"),
    "s": ("flext_target_ldap.target_services", "LdapConnectionService"),
    "singer": ("flext_target_ldap.singer", ""),
    "t": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
    "u": ("flext_target_ldap.utilities", "FlextTargetLdapUtilities"),
    "validate_ldap_config": ("flext_target_ldap.settings", "validate_ldap_config"),
    "validate_ldap_target_config": (
        "flext_target_ldap.target_config",
        "validate_ldap_target_config",
    ),
    "x": ("flext_ldap", "x"),
}

__all__ = [
    "DataTransformationEngine",
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapConstants",
    "FlextTargetLdapError",
    "FlextTargetLdapModels",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSettings",
    "FlextTargetLdapSettingsurationError",
    "FlextTargetLdapTimeoutError",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapValidationError",
    "GroupsSink",
    "LDAPBaseSink",
    "LDAPClient",
    "LDAPConnection",
    "LDAPConnectionSettings",
    "LDAPDataTransformer",
    "LDAPEntryManager",
    "LDAPOperationSettings",
    "LDAPProcessingResult",
    "LDAPSchemaMapper",
    "LDAPSearchEntry",
    "LDAPStreamProcessingStats",
    "LDAPTargetOrchestrator",
    "LDAPTypeConverter",
    "LdapAttributeMappingModel",
    "LdapBaseSink",
    "LdapBatchProcessingModel",
    "LdapConnectionService",
    "LdapEntryModel",
    "LdapGroupsSink",
    "LdapOperationStatisticsModel",
    "LdapOrganizationalUnitsSink",
    "LdapProcessingCounters",
    "LdapProcessingResult",
    "LdapSearchEntry",
    "LdapTargetApiService",
    "LdapTargetClient",
    "LdapTargetOrchestrator",
    "LdapTargetService",
    "LdapTransformationResultModel",
    "LdapTransformationService",
    "LdapUsersSink",
    "MigrationValidator",
    "OrganizationalUnitsSink",
    "SingerLDAPCatalogEntry",
    "SingerLDAPCatalogManager",
    "SingerLDAPStreamProcessor",
    "SingerPropertyDefinition",
    "SingerSchemaDefinition",
    "SingerTargetLDAP",
    "Sink",
    "Target",
    "TargetLDAP",
    "TargetLdap",
    "TransformationResult",
    "TransformationRule",
    "UsersSink",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "application",
    "build_singer_catalog",
    "c",
    "configure_flext_target_ldap_dependencies",
    "create_default_ldap_target_config",
    "d",
    "e",
    "flext_cli_create_helper",
    "get_flext_target_ldap_container",
    "get_flext_target_ldap_service",
    "h",
    "infrastructure",
    "logger",
    "m",
    "main",
    "p",
    "patterns",
    "r",
    "s",
    "singer",
    "t",
    "u",
    "validate_ldap_config",
    "validate_ldap_target_config",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
