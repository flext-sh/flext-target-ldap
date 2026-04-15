# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_target_ldap.__version__ import *

if _t.TYPE_CHECKING:
    from flext_ldap import d, e, h, r, s, x
    from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase
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
    from flext_target_ldap._utilities.api_service import FlextTargetLdapApiService
    from flext_target_ldap._utilities.client import FlextTargetLdapClient
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime,
    )
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapConnectionService,
        FlextTargetLdapTransformationService,
    )
    from flext_target_ldap._utilities.settings import (
        FlextTargetLdapConfigFactory,
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
    )
    from flext_target_ldap.api import FlextTargetLdap, target_ldap
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator
    from flext_target_ldap.catalog import build_singer_catalog
    from flext_target_ldap.constants import FlextTargetLdapConstants, c
    from flext_target_ldap.errors import (
        FlextTargetLdapAuthenticationError,
        FlextTargetLdapConfigurationError,
        FlextTargetLdapConnectionError,
        FlextTargetLdapError,
        FlextTargetLdapProcessingError,
        FlextTargetLdapTimeoutError,
        FlextTargetLdapValidationError,
    )
    from flext_target_ldap.models import FlextTargetLdapModels, m
    from flext_target_ldap.patterns.ldap_patterns import (
        FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter,
    )
    from flext_target_ldap.protocols import FlextTargetLdapProtocols, p
    from flext_target_ldap.settings import FlextTargetLdapSettings
    from flext_target_ldap.singer.catalog import FlextTargetLdapCatalogManager
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import FlextTargetLdapSingerTarget
    from flext_target_ldap.typings import FlextTargetLdapTypes, t
    from flext_target_ldap.utilities import FlextTargetLdapUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._constants",
        "._models",
        "._utilities",
        ".application",
        ".patterns",
        ".singer",
    ),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            ".api": (
                "FlextTargetLdap",
                "target_ldap",
            ),
            ".catalog": ("build_singer_catalog",),
            ".constants": (
                "FlextTargetLdapConstants",
                "c",
            ),
            ".errors": (
                "FlextTargetLdapAuthenticationError",
                "FlextTargetLdapConfigurationError",
                "FlextTargetLdapConnectionError",
                "FlextTargetLdapError",
                "FlextTargetLdapProcessingError",
                "FlextTargetLdapTimeoutError",
                "FlextTargetLdapValidationError",
            ),
            ".models": (
                "FlextTargetLdapModels",
                "m",
            ),
            ".protocols": (
                "FlextTargetLdapProtocols",
                "p",
            ),
            ".settings": ("FlextTargetLdapSettings",),
            ".typings": (
                "FlextTargetLdapTypes",
                "t",
            ),
            ".utilities": (
                "FlextTargetLdapUtilities",
                "u",
            ),
            "flext_ldap": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
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
    "build_singer_catalog",
    "c",
    "create_default_ldap_target_config",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "target_ldap",
    "u",
    "validate_ldap_target_config",
    "x",
]
