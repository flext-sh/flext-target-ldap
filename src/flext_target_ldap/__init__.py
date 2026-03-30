# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

from flext_target_ldap.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_ldap import d, e, h, r, s, x

    from flext_target_ldap import (
        _models,
        _utilities,
        application,
        catalog,
        constants,
        errors,
        models,
        patterns,
        processing_result,
        protocols,
        settings,
        singer,
        sinks,
        target,
        target_client,
        target_config,
        target_services,
        transformation,
        typings,
        utilities,
    )
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )
    from flext_target_ldap._utilities import client, config, services
    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient,
        FlextTargetLdapSearchEntry,
    )
    from flext_target_ldap._utilities.config import (
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapApiService,
        FlextTargetLdapConnectionService,
        FlextTargetLdapTransformationService,
    )
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
    )
    from flext_target_ldap.application import orchestrator
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator
    from flext_target_ldap.catalog import build_singer_catalog
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants,
        FlextTargetLdapConstants as c,
    )
    from flext_target_ldap.errors import (
        FlextTargetLdapAuthenticationError,
        FlextTargetLdapConfigurationError,
        FlextTargetLdapConnectionError,
        FlextTargetLdapError,
        FlextTargetLdapProcessingError,
        FlextTargetLdapTimeoutError,
        FlextTargetLdapValidationError,
    )
    from flext_target_ldap.models import (
        FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )
    from flext_target_ldap.patterns import ldap_patterns
    from flext_target_ldap.patterns.ldap_patterns import (
        FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter,
    )
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )
    from flext_target_ldap.settings import FlextTargetLdapSettings, validate_ldap_config
    from flext_target_ldap.singer import stream
    from flext_target_ldap.singer.catalog import FlextTargetLdapCatalogManager
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import FlextTargetLdapSingerTarget
    from flext_target_ldap.target import FlextTargetLdap, logger, main
    from flext_target_ldap.transformation import (
        DataTransformationEngine,
        MigrationValidator,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes,
        FlextTargetLdapTypes as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "DataTransformationEngine": [
        "flext_target_ldap.transformation",
        "DataTransformationEngine",
    ],
    "FlextTargetLdap": ["flext_target_ldap.target", "FlextTargetLdap"],
    "FlextTargetLdapApiService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapApiService",
    ],
    "FlextTargetLdapAuthenticationError": [
        "flext_target_ldap.errors",
        "FlextTargetLdapAuthenticationError",
    ],
    "FlextTargetLdapBaseSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapBaseSink",
    ],
    "FlextTargetLdapCatalogManager": [
        "flext_target_ldap.singer.catalog",
        "FlextTargetLdapCatalogManager",
    ],
    "FlextTargetLdapClient": [
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapClient",
    ],
    "FlextTargetLdapConfigurationError": [
        "flext_target_ldap.errors",
        "FlextTargetLdapConfigurationError",
    ],
    "FlextTargetLdapConnectionError": [
        "flext_target_ldap.errors",
        "FlextTargetLdapConnectionError",
    ],
    "FlextTargetLdapConnectionService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapConnectionService",
    ],
    "FlextTargetLdapConstants": [
        "flext_target_ldap.constants",
        "FlextTargetLdapConstants",
    ],
    "FlextTargetLdapDataTransformer": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapDataTransformer",
    ],
    "FlextTargetLdapEntryManager": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapEntryManager",
    ],
    "FlextTargetLdapError": ["flext_target_ldap.errors", "FlextTargetLdapError"],
    "FlextTargetLdapGroupsSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapGroupsSink",
    ],
    "FlextTargetLdapMigrationValidator": [
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapMigrationValidator",
    ],
    "FlextTargetLdapModels": ["flext_target_ldap.models", "FlextTargetLdapModels"],
    "FlextTargetLdapOrchestrator": [
        "flext_target_ldap.application.orchestrator",
        "FlextTargetLdapOrchestrator",
    ],
    "FlextTargetLdapOrganizationalUnitsSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapOrganizationalUnitsSink",
    ],
    "FlextTargetLdapProcessingCounters": [
        "flext_target_ldap._models.processing_result",
        "FlextTargetLdapProcessingCounters",
    ],
    "FlextTargetLdapProcessingError": [
        "flext_target_ldap.errors",
        "FlextTargetLdapProcessingError",
    ],
    "FlextTargetLdapProcessingResult": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapProcessingResult",
    ],
    "FlextTargetLdapProtocols": [
        "flext_target_ldap.protocols",
        "FlextTargetLdapProtocols",
    ],
    "FlextTargetLdapSchemaMapper": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapSchemaMapper",
    ],
    "FlextTargetLdapSearchEntry": [
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapSearchEntry",
    ],
    "FlextTargetLdapSettings": [
        "flext_target_ldap.settings",
        "FlextTargetLdapSettings",
    ],
    "FlextTargetLdapSingerTarget": [
        "flext_target_ldap.singer.target",
        "FlextTargetLdapSingerTarget",
    ],
    "FlextTargetLdapSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapSink"],
    "FlextTargetLdapStreamProcessingStats": [
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessingStats",
    ],
    "FlextTargetLdapStreamProcessor": [
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessor",
    ],
    "FlextTargetLdapTarget": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapTarget",
    ],
    "FlextTargetLdapTimeoutError": [
        "flext_target_ldap.errors",
        "FlextTargetLdapTimeoutError",
    ],
    "FlextTargetLdapTransformationEngine": [
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapTransformationEngine",
    ],
    "FlextTargetLdapTransformationService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapTransformationService",
    ],
    "FlextTargetLdapTypeConverter": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapTypeConverter",
    ],
    "FlextTargetLdapTypes": ["flext_target_ldap.typings", "FlextTargetLdapTypes"],
    "FlextTargetLdapUsersSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapUsersSink",
    ],
    "FlextTargetLdapUtilities": [
        "flext_target_ldap.utilities",
        "FlextTargetLdapUtilities",
    ],
    "FlextTargetLdapValidationError": [
        "flext_target_ldap.errors",
        "FlextTargetLdapValidationError",
    ],
    "MigrationValidator": ["flext_target_ldap.transformation", "MigrationValidator"],
    "_models": ["flext_target_ldap._models", ""],
    "_utilities": ["flext_target_ldap._utilities", ""],
    "application": ["flext_target_ldap.application", ""],
    "build_singer_catalog": ["flext_target_ldap.catalog", "build_singer_catalog"],
    "c": ["flext_target_ldap.constants", "FlextTargetLdapConstants"],
    "catalog": ["flext_target_ldap.catalog", ""],
    "client": ["flext_target_ldap._utilities.client", ""],
    "config": ["flext_target_ldap._utilities.config", ""],
    "constants": ["flext_target_ldap.constants", ""],
    "create_default_ldap_target_config": [
        "flext_target_ldap._utilities.config",
        "create_default_ldap_target_config",
    ],
    "d": ["flext_ldap", "d"],
    "e": ["flext_ldap", "e"],
    "errors": ["flext_target_ldap.errors", ""],
    "h": ["flext_ldap", "h"],
    "ldap_patterns": ["flext_target_ldap.patterns.ldap_patterns", ""],
    "logger": ["flext_target_ldap.target", "logger"],
    "m": ["flext_target_ldap.models", "FlextTargetLdapModels"],
    "main": ["flext_target_ldap.target", "main"],
    "models": ["flext_target_ldap.models", ""],
    "orchestrator": ["flext_target_ldap.application.orchestrator", ""],
    "p": ["flext_target_ldap.protocols", "FlextTargetLdapProtocols"],
    "patterns": ["flext_target_ldap.patterns", ""],
    "processing_result": ["flext_target_ldap.processing_result", ""],
    "protocols": ["flext_target_ldap.protocols", ""],
    "r": ["flext_ldap", "r"],
    "s": ["flext_ldap", "s"],
    "services": ["flext_target_ldap._utilities.services", ""],
    "settings": ["flext_target_ldap.settings", ""],
    "singer": ["flext_target_ldap.singer", ""],
    "sinks": ["flext_target_ldap.sinks", ""],
    "stream": ["flext_target_ldap.singer.stream", ""],
    "t": ["flext_target_ldap.typings", "FlextTargetLdapTypes"],
    "target": ["flext_target_ldap.target", ""],
    "target_client": ["flext_target_ldap.target_client", ""],
    "target_config": ["flext_target_ldap.target_config", ""],
    "target_services": ["flext_target_ldap.target_services", ""],
    "transformation": ["flext_target_ldap.transformation", ""],
    "typings": ["flext_target_ldap.typings", ""],
    "u": ["flext_target_ldap.utilities", "FlextTargetLdapUtilities"],
    "utilities": ["flext_target_ldap.utilities", ""],
    "validate_ldap_config": ["flext_target_ldap.settings", "validate_ldap_config"],
    "validate_ldap_target_config": [
        "flext_target_ldap._utilities.config",
        "validate_ldap_target_config",
    ],
    "x": ["flext_ldap", "x"],
}

__all__ = [
    "DataTransformationEngine",
    "FlextTargetLdap",
    "FlextTargetLdapApiService",
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapCatalogManager",
    "FlextTargetLdapClient",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapConstants",
    "FlextTargetLdapDataTransformer",
    "FlextTargetLdapEntryManager",
    "FlextTargetLdapError",
    "FlextTargetLdapGroupsSink",
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
    "MigrationValidator",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_models",
    "_utilities",
    "application",
    "build_singer_catalog",
    "c",
    "catalog",
    "client",
    "config",
    "constants",
    "create_default_ldap_target_config",
    "d",
    "e",
    "errors",
    "h",
    "ldap_patterns",
    "logger",
    "m",
    "main",
    "models",
    "orchestrator",
    "p",
    "patterns",
    "processing_result",
    "protocols",
    "r",
    "s",
    "services",
    "settings",
    "singer",
    "sinks",
    "stream",
    "t",
    "target",
    "target_client",
    "target_config",
    "target_services",
    "transformation",
    "typings",
    "u",
    "utilities",
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
