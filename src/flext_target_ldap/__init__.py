# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_ldap import d, e, h, r, s, x

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
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator
    from flext_target_ldap.catalog import build_singer_catalog
    from flext_target_ldap.client import (
        FlextTargetLdapLdapClient,
        FlextTargetLdapSearchEntry,
        LDAPConnection,
    )
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
        FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter,
        SingerPropertyDefinition,
        SingerSchemaDefinition,
    )
    from flext_target_ldap.processing_result import FlextTargetLdapProcessingCounters
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )
    from flext_target_ldap.settings import FlextTargetLdapSettings, validate_ldap_config
    from flext_target_ldap.singer.catalog import (
        FlextTargetLdapCatalogManager,
        SingerLDAPCatalogEntry,
    )
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import FlextTargetLdapSingerTarget
    from flext_target_ldap.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )
    from flext_target_ldap.target import FlextTargetLdap, main
    from flext_target_ldap.target_client import FlextTargetLdapClient
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
    from flext_target_ldap.target_services import (
        FlextTargetLdapApiService,
        FlextTargetLdapConnectionService,
        FlextTargetLdapTransformationService,
    )
    from flext_target_ldap.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
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

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "FlextTargetLdap": ("flext_target_ldap.target", "FlextTargetLdap"),
    "FlextTargetLdapApiService": (
        "flext_target_ldap.target_services",
        "FlextTargetLdapApiService",
    ),
    "FlextTargetLdapAuthenticationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapAuthenticationError",
    ),
    "FlextTargetLdapBaseSink": ("flext_target_ldap.sinks", "FlextTargetLdapBaseSink"),
    "FlextTargetLdapCatalogManager": (
        "flext_target_ldap.singer.catalog",
        "FlextTargetLdapCatalogManager",
    ),
    "FlextTargetLdapClient": (
        "flext_target_ldap.target_client",
        "FlextTargetLdapClient",
    ),
    "FlextTargetLdapConnectionError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapConnectionError",
    ),
    "FlextTargetLdapConnectionService": (
        "flext_target_ldap.target_services",
        "FlextTargetLdapConnectionService",
    ),
    "FlextTargetLdapConstants": (
        "flext_target_ldap.constants",
        "FlextTargetLdapConstants",
    ),
    "FlextTargetLdapDataTransformer": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapDataTransformer",
    ),
    "FlextTargetLdapEntryManager": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapEntryManager",
    ),
    "FlextTargetLdapError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapError",
    ),
    "FlextTargetLdapGroupsSink": (
        "flext_target_ldap.sinks",
        "FlextTargetLdapGroupsSink",
    ),
    "FlextTargetLdapLdapClient": (
        "flext_target_ldap.client",
        "FlextTargetLdapLdapClient",
    ),
    "FlextTargetLdapMigrationValidator": (
        "flext_target_ldap.transformation",
        "FlextTargetLdapMigrationValidator",
    ),
    "FlextTargetLdapModels": ("flext_target_ldap.models", "FlextTargetLdapModels"),
    "FlextTargetLdapOrchestrator": (
        "flext_target_ldap.application.orchestrator",
        "FlextTargetLdapOrchestrator",
    ),
    "FlextTargetLdapOrganizationalUnitsSink": (
        "flext_target_ldap.sinks",
        "FlextTargetLdapOrganizationalUnitsSink",
    ),
    "FlextTargetLdapProcessingCounters": (
        "flext_target_ldap.processing_result",
        "FlextTargetLdapProcessingCounters",
    ),
    "FlextTargetLdapProcessingError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapProcessingError",
    ),
    "FlextTargetLdapProcessingResult": (
        "flext_target_ldap.sinks",
        "FlextTargetLdapProcessingResult",
    ),
    "FlextTargetLdapProtocols": (
        "flext_target_ldap.protocols",
        "FlextTargetLdapProtocols",
    ),
    "FlextTargetLdapSchemaMapper": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapSchemaMapper",
    ),
    "FlextTargetLdapSearchEntry": (
        "flext_target_ldap.client",
        "FlextTargetLdapSearchEntry",
    ),
    "FlextTargetLdapSettings": (
        "flext_target_ldap.settings",
        "FlextTargetLdapSettings",
    ),
    "FlextTargetLdapSettingsurationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapSettingsurationError",
    ),
    "FlextTargetLdapSingerTarget": (
        "flext_target_ldap.singer.target",
        "FlextTargetLdapSingerTarget",
    ),
    "FlextTargetLdapSink": ("flext_target_ldap.sinks", "FlextTargetLdapSink"),
    "FlextTargetLdapStreamProcessingStats": (
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessingStats",
    ),
    "FlextTargetLdapStreamProcessor": (
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessor",
    ),
    "FlextTargetLdapTarget": ("flext_target_ldap.sinks", "FlextTargetLdapTarget"),
    "FlextTargetLdapTimeoutError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapTimeoutError",
    ),
    "FlextTargetLdapTransformationEngine": (
        "flext_target_ldap.transformation",
        "FlextTargetLdapTransformationEngine",
    ),
    "FlextTargetLdapTransformationService": (
        "flext_target_ldap.target_services",
        "FlextTargetLdapTransformationService",
    ),
    "FlextTargetLdapTypeConverter": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapTypeConverter",
    ),
    "FlextTargetLdapTypes": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
    "FlextTargetLdapUsersSink": ("flext_target_ldap.sinks", "FlextTargetLdapUsersSink"),
    "FlextTargetLdapUtilities": (
        "flext_target_ldap.utilities",
        "FlextTargetLdapUtilities",
    ),
    "FlextTargetLdapValidationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapValidationError",
    ),
    "LDAPConnection": ("flext_target_ldap.client", "LDAPConnection"),
    "SingerLDAPCatalogEntry": (
        "flext_target_ldap.singer.catalog",
        "SingerLDAPCatalogEntry",
    ),
    "SingerPropertyDefinition": (
        "flext_target_ldap.patterns.ldap_patterns",
        "SingerPropertyDefinition",
    ),
    "SingerSchemaDefinition": (
        "flext_target_ldap.patterns.ldap_patterns",
        "SingerSchemaDefinition",
    ),
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
    "r": ("flext_ldap", "r"),
    "s": ("flext_ldap", "s"),
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
    "FlextTargetLdap",
    "FlextTargetLdapApiService",
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapCatalogManager",
    "FlextTargetLdapClient",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapConstants",
    "FlextTargetLdapDataTransformer",
    "FlextTargetLdapEntryManager",
    "FlextTargetLdapError",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapLdapClient",
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapModels",
    "FlextTargetLdapOrchestrator",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingCounters",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSchemaMapper",
    "FlextTargetLdapSearchEntry",
    "FlextTargetLdapSettings",
    "FlextTargetLdapSettingsurationError",
    "FlextTargetLdapSingerTarget",
    "FlextTargetLdapSink",
    "FlextTargetLdapStreamProcessingStats",
    "FlextTargetLdapStreamProcessor",
    "FlextTargetLdapTarget",
    "FlextTargetLdapTimeoutError",
    "FlextTargetLdapTransformationEngine",
    "FlextTargetLdapTransformationService",
    "FlextTargetLdapTypeConverter",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUsersSink",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapValidationError",
    "LDAPConnection",
    "SingerLDAPCatalogEntry",
    "SingerPropertyDefinition",
    "SingerSchemaDefinition",
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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
