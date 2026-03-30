# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_target_ldap.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_ldap import d, e, h, r, s, x

    from flext_target_ldap import (
        _models as _models,
        _utilities as _utilities,
        application as application,
        catalog as catalog,
        constants as constants,
        errors as errors,
        models as models,
        patterns as patterns,
        processing_result as processing_result,
        protocols as protocols,
        settings as settings,
        singer as singer,
        sinks as sinks,
        target as target,
        target_client as target_client,
        target_config as target_config,
        target_services as target_services,
        transformation as transformation,
        typings as typings,
        utilities as utilities,
    )
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters as FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink as FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink as FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink as FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult as FlextTargetLdapProcessingResult,
        FlextTargetLdapSink as FlextTargetLdapSink,
        FlextTargetLdapTarget as FlextTargetLdapTarget,
        FlextTargetLdapUsersSink as FlextTargetLdapUsersSink,
    )
    from flext_target_ldap._utilities import (
        client as client,
        config as config,
        services as services,
    )
    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient as FlextTargetLdapClient,
        FlextTargetLdapSearchEntry as FlextTargetLdapSearchEntry,
    )
    from flext_target_ldap._utilities.config import (
        create_default_ldap_target_config as create_default_ldap_target_config,
        validate_ldap_target_config as validate_ldap_target_config,
    )
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapApiService as FlextTargetLdapApiService,
        FlextTargetLdapConnectionService as FlextTargetLdapConnectionService,
        FlextTargetLdapTransformationService as FlextTargetLdapTransformationService,
    )
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator as FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine as FlextTargetLdapTransformationEngine,
    )
    from flext_target_ldap.application import orchestrator as orchestrator
    from flext_target_ldap.application.orchestrator import (
        FlextTargetLdapOrchestrator as FlextTargetLdapOrchestrator,
    )
    from flext_target_ldap.catalog import build_singer_catalog as build_singer_catalog
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants as FlextTargetLdapConstants,
        FlextTargetLdapConstants as c,
    )
    from flext_target_ldap.errors import (
        FlextTargetLdapAuthenticationError as FlextTargetLdapAuthenticationError,
        FlextTargetLdapConfigurationError as FlextTargetLdapConfigurationError,
        FlextTargetLdapConnectionError as FlextTargetLdapConnectionError,
        FlextTargetLdapError as FlextTargetLdapError,
        FlextTargetLdapProcessingError as FlextTargetLdapProcessingError,
        FlextTargetLdapTimeoutError as FlextTargetLdapTimeoutError,
        FlextTargetLdapValidationError as FlextTargetLdapValidationError,
    )
    from flext_target_ldap.models import (
        FlextTargetLdapModels as FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )
    from flext_target_ldap.patterns import ldap_patterns as ldap_patterns
    from flext_target_ldap.patterns.ldap_patterns import (
        FlextTargetLdapDataTransformer as FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager as FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper as FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter as FlextTargetLdapTypeConverter,
    )
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols as FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )
    from flext_target_ldap.settings import (
        FlextTargetLdapSettings as FlextTargetLdapSettings,
        validate_ldap_config as validate_ldap_config,
    )
    from flext_target_ldap.singer import stream as stream
    from flext_target_ldap.singer.catalog import (
        FlextTargetLdapCatalogManager as FlextTargetLdapCatalogManager,
    )
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats as FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor as FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import (
        FlextTargetLdapSingerTarget as FlextTargetLdapSingerTarget,
    )
    from flext_target_ldap.target import (
        FlextTargetLdap as FlextTargetLdap,
        logger as logger,
        main as main,
    )
    from flext_target_ldap.transformation import (
        DataTransformationEngine as DataTransformationEngine,
        MigrationValidator as MigrationValidator,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes as FlextTargetLdapTypes,
        FlextTargetLdapTypes as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities as FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "DataTransformationEngine": ["flext_target_ldap.transformation", "DataTransformationEngine"],
    "FlextTargetLdap": ["flext_target_ldap.target", "FlextTargetLdap"],
    "FlextTargetLdapApiService": ["flext_target_ldap._utilities.services", "FlextTargetLdapApiService"],
    "FlextTargetLdapAuthenticationError": ["flext_target_ldap.errors", "FlextTargetLdapAuthenticationError"],
    "FlextTargetLdapBaseSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapBaseSink"],
    "FlextTargetLdapCatalogManager": ["flext_target_ldap.singer.catalog", "FlextTargetLdapCatalogManager"],
    "FlextTargetLdapClient": ["flext_target_ldap._utilities.client", "FlextTargetLdapClient"],
    "FlextTargetLdapConfigurationError": ["flext_target_ldap.errors", "FlextTargetLdapConfigurationError"],
    "FlextTargetLdapConnectionError": ["flext_target_ldap.errors", "FlextTargetLdapConnectionError"],
    "FlextTargetLdapConnectionService": ["flext_target_ldap._utilities.services", "FlextTargetLdapConnectionService"],
    "FlextTargetLdapConstants": ["flext_target_ldap.constants", "FlextTargetLdapConstants"],
    "FlextTargetLdapDataTransformer": ["flext_target_ldap.patterns.ldap_patterns", "FlextTargetLdapDataTransformer"],
    "FlextTargetLdapEntryManager": ["flext_target_ldap.patterns.ldap_patterns", "FlextTargetLdapEntryManager"],
    "FlextTargetLdapError": ["flext_target_ldap.errors", "FlextTargetLdapError"],
    "FlextTargetLdapGroupsSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapGroupsSink"],
    "FlextTargetLdapMigrationValidator": ["flext_target_ldap._utilities.transformation", "FlextTargetLdapMigrationValidator"],
    "FlextTargetLdapModels": ["flext_target_ldap.models", "FlextTargetLdapModels"],
    "FlextTargetLdapOrchestrator": ["flext_target_ldap.application.orchestrator", "FlextTargetLdapOrchestrator"],
    "FlextTargetLdapOrganizationalUnitsSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapOrganizationalUnitsSink"],
    "FlextTargetLdapProcessingCounters": ["flext_target_ldap._models.processing_result", "FlextTargetLdapProcessingCounters"],
    "FlextTargetLdapProcessingError": ["flext_target_ldap.errors", "FlextTargetLdapProcessingError"],
    "FlextTargetLdapProcessingResult": ["flext_target_ldap._models.sinks", "FlextTargetLdapProcessingResult"],
    "FlextTargetLdapProtocols": ["flext_target_ldap.protocols", "FlextTargetLdapProtocols"],
    "FlextTargetLdapSchemaMapper": ["flext_target_ldap.patterns.ldap_patterns", "FlextTargetLdapSchemaMapper"],
    "FlextTargetLdapSearchEntry": ["flext_target_ldap._utilities.client", "FlextTargetLdapSearchEntry"],
    "FlextTargetLdapSettings": ["flext_target_ldap.settings", "FlextTargetLdapSettings"],
    "FlextTargetLdapSingerTarget": ["flext_target_ldap.singer.target", "FlextTargetLdapSingerTarget"],
    "FlextTargetLdapSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapSink"],
    "FlextTargetLdapStreamProcessingStats": ["flext_target_ldap.singer.stream", "FlextTargetLdapStreamProcessingStats"],
    "FlextTargetLdapStreamProcessor": ["flext_target_ldap.singer.stream", "FlextTargetLdapStreamProcessor"],
    "FlextTargetLdapTarget": ["flext_target_ldap._models.sinks", "FlextTargetLdapTarget"],
    "FlextTargetLdapTimeoutError": ["flext_target_ldap.errors", "FlextTargetLdapTimeoutError"],
    "FlextTargetLdapTransformationEngine": ["flext_target_ldap._utilities.transformation", "FlextTargetLdapTransformationEngine"],
    "FlextTargetLdapTransformationService": ["flext_target_ldap._utilities.services", "FlextTargetLdapTransformationService"],
    "FlextTargetLdapTypeConverter": ["flext_target_ldap.patterns.ldap_patterns", "FlextTargetLdapTypeConverter"],
    "FlextTargetLdapTypes": ["flext_target_ldap.typings", "FlextTargetLdapTypes"],
    "FlextTargetLdapUsersSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapUsersSink"],
    "FlextTargetLdapUtilities": ["flext_target_ldap.utilities", "FlextTargetLdapUtilities"],
    "FlextTargetLdapValidationError": ["flext_target_ldap.errors", "FlextTargetLdapValidationError"],
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
    "create_default_ldap_target_config": ["flext_target_ldap._utilities.config", "create_default_ldap_target_config"],
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
    "validate_ldap_target_config": ["flext_target_ldap._utilities.config", "validate_ldap_target_config"],
    "x": ["flext_ldap", "x"],
}

_EXPORTS: Sequence[str] = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
