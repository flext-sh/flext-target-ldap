# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_target_ldap.__version__ import *

if _t.TYPE_CHECKING:
    import flext_target_ldap._constants as _flext_target_ldap__constants

    _constants = _flext_target_ldap__constants
    import flext_target_ldap._models as _flext_target_ldap__models
    from flext_target_ldap._constants import FlextTargetLdapConstantsBase

    _models = _flext_target_ldap__models
    import flext_target_ldap._utilities as _flext_target_ldap__utilities
    from flext_target_ldap._models import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingCounters,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )

    _utilities = _flext_target_ldap__utilities
    import flext_target_ldap.api as _flext_target_ldap_api
    from flext_target_ldap._utilities import (
        FlextTargetLdapApiService,
        FlextTargetLdapClient,
        FlextTargetLdapConfigFactory,
        FlextTargetLdapConnectionService,
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapServiceRuntime,
        FlextTargetLdapTransformationEngine,
        FlextTargetLdapTransformationService,
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )

    api = _flext_target_ldap_api
    import flext_target_ldap.catalog as _flext_target_ldap_catalog
    from flext_target_ldap.api import (
        FlextTargetLdapService,
        FlextTargetLdapService as s,
    )
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
    import flext_target_ldap.protocols as _flext_target_ldap_protocols
    from flext_target_ldap.models import (
        FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )
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
    import flext_target_ldap.target as _flext_target_ldap_target
    from flext_target_ldap.settings import FlextTargetLdapSettings, validate_ldap_config
    from flext_target_ldap.singer.catalog import FlextTargetLdapCatalogManager
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
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_target_ldap._constants",
        "flext_target_ldap._models",
        "flext_target_ldap._utilities",
    ),
    {
        "FlextTargetLdap": ("flext_target_ldap.target", "FlextTargetLdap"),
        "FlextTargetLdapAuthenticationError": (
            "flext_target_ldap.errors",
            "FlextTargetLdapAuthenticationError",
        ),
        "FlextTargetLdapCatalogManager": (
            "flext_target_ldap.singer.catalog",
            "FlextTargetLdapCatalogManager",
        ),
        "FlextTargetLdapConfigurationError": (
            "flext_target_ldap.errors",
            "FlextTargetLdapConfigurationError",
        ),
        "FlextTargetLdapConnectionError": (
            "flext_target_ldap.errors",
            "FlextTargetLdapConnectionError",
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
        "FlextTargetLdapError": ("flext_target_ldap.errors", "FlextTargetLdapError"),
        "FlextTargetLdapModels": ("flext_target_ldap.models", "FlextTargetLdapModels"),
        "FlextTargetLdapOrchestrator": (
            "flext_target_ldap.application.orchestrator",
            "FlextTargetLdapOrchestrator",
        ),
        "FlextTargetLdapProcessingError": (
            "flext_target_ldap.errors",
            "FlextTargetLdapProcessingError",
        ),
        "FlextTargetLdapProtocols": (
            "flext_target_ldap.protocols",
            "FlextTargetLdapProtocols",
        ),
        "FlextTargetLdapSchemaMapper": (
            "flext_target_ldap.patterns.ldap_patterns",
            "FlextTargetLdapSchemaMapper",
        ),
        "FlextTargetLdapService": ("flext_target_ldap.api", "FlextTargetLdapService"),
        "FlextTargetLdapSettings": (
            "flext_target_ldap.settings",
            "FlextTargetLdapSettings",
        ),
        "FlextTargetLdapSingerTarget": (
            "flext_target_ldap.singer.target",
            "FlextTargetLdapSingerTarget",
        ),
        "FlextTargetLdapStreamProcessingStats": (
            "flext_target_ldap.singer.stream",
            "FlextTargetLdapStreamProcessingStats",
        ),
        "FlextTargetLdapStreamProcessor": (
            "flext_target_ldap.singer.stream",
            "FlextTargetLdapStreamProcessor",
        ),
        "FlextTargetLdapTimeoutError": (
            "flext_target_ldap.errors",
            "FlextTargetLdapTimeoutError",
        ),
        "FlextTargetLdapTypeConverter": (
            "flext_target_ldap.patterns.ldap_patterns",
            "FlextTargetLdapTypeConverter",
        ),
        "FlextTargetLdapTypes": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
        "FlextTargetLdapUtilities": (
            "flext_target_ldap.utilities",
            "FlextTargetLdapUtilities",
        ),
        "FlextTargetLdapValidationError": (
            "flext_target_ldap.errors",
            "FlextTargetLdapValidationError",
        ),
        "__author__": ("flext_target_ldap.__version__", "__author__"),
        "__author_email__": ("flext_target_ldap.__version__", "__author_email__"),
        "__description__": ("flext_target_ldap.__version__", "__description__"),
        "__license__": ("flext_target_ldap.__version__", "__license__"),
        "__title__": ("flext_target_ldap.__version__", "__title__"),
        "__url__": ("flext_target_ldap.__version__", "__url__"),
        "__version__": ("flext_target_ldap.__version__", "__version__"),
        "__version_info__": ("flext_target_ldap.__version__", "__version_info__"),
        "_constants": "flext_target_ldap._constants",
        "_models": "flext_target_ldap._models",
        "_utilities": "flext_target_ldap._utilities",
        "api": "flext_target_ldap.api",
        "build_singer_catalog": ("flext_target_ldap.catalog", "build_singer_catalog"),
        "c": ("flext_target_ldap.constants", "FlextTargetLdapConstants"),
        "catalog": "flext_target_ldap.catalog",
        "constants": "flext_target_ldap.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "errors": "flext_target_ldap.errors",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_target_ldap.models", "FlextTargetLdapModels"),
        "main": ("flext_target_ldap.target", "main"),
        "models": "flext_target_ldap.models",
        "p": ("flext_target_ldap.protocols", "FlextTargetLdapProtocols"),
        "protocols": "flext_target_ldap.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_target_ldap.api", "FlextTargetLdapService"),
        "settings": "flext_target_ldap.settings",
        "t": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
        "target": "flext_target_ldap.target",
        "typings": "flext_target_ldap.typings",
        "u": ("flext_target_ldap.utilities", "FlextTargetLdapUtilities"),
        "utilities": "flext_target_ldap.utilities",
        "validate_ldap_config": ("flext_target_ldap.settings", "validate_ldap_config"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "FlextTargetLdap",
    "FlextTargetLdapApiService",
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapCatalogManager",
    "FlextTargetLdapClient",
    "FlextTargetLdapConfigFactory",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapConstants",
    "FlextTargetLdapConstantsBase",
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
    "_constants",
    "_models",
    "_utilities",
    "api",
    "build_singer_catalog",
    "c",
    "catalog",
    "constants",
    "create_default_ldap_target_config",
    "d",
    "e",
    "errors",
    "h",
    "m",
    "main",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "settings",
    "t",
    "target",
    "typings",
    "u",
    "utilities",
    "validate_ldap_config",
    "validate_ldap_target_config",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
