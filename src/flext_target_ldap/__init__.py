# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_target_ldap.__version__ import *

if _t.TYPE_CHECKING:
    import flext_target_ldap._models as _flext_target_ldap__models
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

    _models = _flext_target_ldap__models
    import flext_target_ldap._models.processing_result as _flext_target_ldap__models_processing_result

    processing_result = _flext_target_ldap__models_processing_result
    import flext_target_ldap._models.sinks as _flext_target_ldap__models_sinks
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )

    sinks = _flext_target_ldap__models_sinks
    import flext_target_ldap._utilities as _flext_target_ldap__utilities
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )

    _utilities = _flext_target_ldap__utilities
    import flext_target_ldap._utilities.api_service as _flext_target_ldap__utilities_api_service

    api_service = _flext_target_ldap__utilities_api_service
    import flext_target_ldap._utilities.client as _flext_target_ldap__utilities_client
    from flext_target_ldap._utilities.api_service import FlextTargetLdapApiService

    client = _flext_target_ldap__utilities_client
    import flext_target_ldap._utilities.config as _flext_target_ldap__utilities_config
    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient,
        FlextTargetLdapSearchEntry,
    )

    config = _flext_target_ldap__utilities_config
    import flext_target_ldap._utilities.service_runtime as _flext_target_ldap__utilities_service_runtime
    from flext_target_ldap._utilities.config import (
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )

    service_runtime = _flext_target_ldap__utilities_service_runtime
    import flext_target_ldap._utilities.services as _flext_target_ldap__utilities_services
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime,
    )

    services = _flext_target_ldap__utilities_services
    import flext_target_ldap._utilities.transformation as _flext_target_ldap__utilities_transformation
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapConnectionService,
        FlextTargetLdapTransformationService,
    )

    transformation = _flext_target_ldap__utilities_transformation
    import flext_target_ldap.api as _flext_target_ldap_api
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
    )

    api = _flext_target_ldap_api
    import flext_target_ldap.application as _flext_target_ldap_application
    from flext_target_ldap.api import FlextTargetLdapService

    application = _flext_target_ldap_application
    import flext_target_ldap.application.orchestrator as _flext_target_ldap_application_orchestrator

    orchestrator = _flext_target_ldap_application_orchestrator
    import flext_target_ldap.catalog as _flext_target_ldap_catalog
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator

    catalog = _flext_target_ldap_catalog
    import flext_target_ldap.constants as _flext_target_ldap_constants
    from flext_target_ldap.catalog import build_singer_catalog

    constants = _flext_target_ldap_constants
    import flext_target_ldap.errors as _flext_target_ldap_errors
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants,
        FlextTargetLdapConstants as c,
    )

    errors = _flext_target_ldap_errors
    import flext_target_ldap.models as _flext_target_ldap_models
    from flext_target_ldap.errors import (
        FlextTargetLdapAuthenticationError,
        FlextTargetLdapConfigurationError,
        FlextTargetLdapConnectionError,
        FlextTargetLdapError,
        FlextTargetLdapProcessingError,
        FlextTargetLdapTimeoutError,
        FlextTargetLdapValidationError,
    )

    models = _flext_target_ldap_models
    import flext_target_ldap.patterns as _flext_target_ldap_patterns
    from flext_target_ldap.models import (
        FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )

    patterns = _flext_target_ldap_patterns
    import flext_target_ldap.patterns.ldap_patterns as _flext_target_ldap_patterns_ldap_patterns

    ldap_patterns = _flext_target_ldap_patterns_ldap_patterns
    import flext_target_ldap.protocols as _flext_target_ldap_protocols
    from flext_target_ldap.patterns.ldap_patterns import (
        FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter,
    )

    protocols = _flext_target_ldap_protocols
    import flext_target_ldap.settings as _flext_target_ldap_settings
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )

    settings = _flext_target_ldap_settings
    import flext_target_ldap.singer as _flext_target_ldap_singer
    from flext_target_ldap.settings import FlextTargetLdapSettings, validate_ldap_config

    singer = _flext_target_ldap_singer
    import flext_target_ldap.singer.stream as _flext_target_ldap_singer_stream
    from flext_target_ldap.singer.catalog import FlextTargetLdapCatalogManager

    stream = _flext_target_ldap_singer_stream
    import flext_target_ldap.target as _flext_target_ldap_target
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import FlextTargetLdapSingerTarget

    target = _flext_target_ldap_target
    import flext_target_ldap.typings as _flext_target_ldap_typings
    from flext_target_ldap.target import FlextTargetLdap, main

    typings = _flext_target_ldap_typings
    import flext_target_ldap.utilities as _flext_target_ldap_utilities
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes,
        FlextTargetLdapTypes as t,
    )

    utilities = _flext_target_ldap_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_target_ldap._models",
        "flext_target_ldap._utilities",
        "flext_target_ldap.application",
        "flext_target_ldap.patterns",
        "flext_target_ldap.singer",
    ),
    {
        "FlextTargetLdap": "flext_target_ldap.target",
        "FlextTargetLdapAuthenticationError": "flext_target_ldap.errors",
        "FlextTargetLdapConfigurationError": "flext_target_ldap.errors",
        "FlextTargetLdapConnectionError": "flext_target_ldap.errors",
        "FlextTargetLdapConstants": "flext_target_ldap.constants",
        "FlextTargetLdapError": "flext_target_ldap.errors",
        "FlextTargetLdapModels": "flext_target_ldap.models",
        "FlextTargetLdapProcessingError": "flext_target_ldap.errors",
        "FlextTargetLdapProtocols": "flext_target_ldap.protocols",
        "FlextTargetLdapService": "flext_target_ldap.api",
        "FlextTargetLdapSettings": "flext_target_ldap.settings",
        "FlextTargetLdapTimeoutError": "flext_target_ldap.errors",
        "FlextTargetLdapTypes": "flext_target_ldap.typings",
        "FlextTargetLdapUtilities": "flext_target_ldap.utilities",
        "FlextTargetLdapValidationError": "flext_target_ldap.errors",
        "__author__": "flext_target_ldap.__version__",
        "__author_email__": "flext_target_ldap.__version__",
        "__description__": "flext_target_ldap.__version__",
        "__license__": "flext_target_ldap.__version__",
        "__title__": "flext_target_ldap.__version__",
        "__url__": "flext_target_ldap.__version__",
        "__version__": "flext_target_ldap.__version__",
        "__version_info__": "flext_target_ldap.__version__",
        "_models": "flext_target_ldap._models",
        "_utilities": "flext_target_ldap._utilities",
        "api": "flext_target_ldap.api",
        "application": "flext_target_ldap.application",
        "build_singer_catalog": "flext_target_ldap.catalog",
        "c": ("flext_target_ldap.constants", "FlextTargetLdapConstants"),
        "catalog": "flext_target_ldap.catalog",
        "constants": "flext_target_ldap.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "errors": "flext_target_ldap.errors",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_target_ldap.models", "FlextTargetLdapModels"),
        "main": "flext_target_ldap.target",
        "models": "flext_target_ldap.models",
        "p": ("flext_target_ldap.protocols", "FlextTargetLdapProtocols"),
        "patterns": "flext_target_ldap.patterns",
        "protocols": "flext_target_ldap.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "settings": "flext_target_ldap.settings",
        "singer": "flext_target_ldap.singer",
        "t": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
        "target": "flext_target_ldap.target",
        "typings": "flext_target_ldap.typings",
        "u": ("flext_target_ldap.utilities", "FlextTargetLdapUtilities"),
        "utilities": "flext_target_ldap.utilities",
        "validate_ldap_config": "flext_target_ldap.settings",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

__all__ = [
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
    "FlextTargetLdapService",
    "FlextTargetLdapServiceRuntime",
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
    "api",
    "api_service",
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
    "service_runtime",
    "services",
    "settings",
    "singer",
    "sinks",
    "stream",
    "t",
    "target",
    "transformation",
    "typings",
    "u",
    "utilities",
    "validate_ldap_config",
    "validate_ldap_target_config",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
