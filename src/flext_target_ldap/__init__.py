# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_ldap import d, e, h, r, s, x

    from flext_target_ldap import (
        _models,
        _utilities,
        api,
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
    from flext_target_ldap._utilities import (
        FlextTargetLdapApiService,
        FlextTargetLdapClient,
        FlextTargetLdapConnectionService,
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapSearchEntry,
        FlextTargetLdapTransformationEngine,
        FlextTargetLdapTransformationService,
        client,
        config,
        create_default_ldap_target_config,
        services,
        validate_ldap_target_config,
    )
    from flext_target_ldap.api import FlextTargetLdapService
    from flext_target_ldap.application import FlextTargetLdapOrchestrator, orchestrator
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
    from flext_target_ldap.patterns import (
        FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter,
        ldap_patterns,
    )
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )
    from flext_target_ldap.settings import FlextTargetLdapSettings, validate_ldap_config
    from flext_target_ldap.singer import (
        FlextTargetLdapCatalogManager,
        FlextTargetLdapSingerTarget,
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
        stream,
    )
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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "flext_target_ldap._models",
        "flext_target_ldap._utilities",
        "flext_target_ldap.application",
        "flext_target_ldap.patterns",
        "flext_target_ldap.singer",
    ),
    {
        "DataTransformationEngine": "flext_target_ldap.transformation",
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
        "MigrationValidator": "flext_target_ldap.transformation",
        "_models": "flext_target_ldap._models",
        "_utilities": "flext_target_ldap._utilities",
        "api": "flext_target_ldap.api",
        "application": "flext_target_ldap.application",
        "build_singer_catalog": "flext_target_ldap.catalog",
        "c": ("flext_target_ldap.constants", "FlextTargetLdapConstants"),
        "catalog": "flext_target_ldap.catalog",
        "constants": "flext_target_ldap.constants",
        "d": "flext_ldap",
        "e": "flext_ldap",
        "errors": "flext_target_ldap.errors",
        "h": "flext_ldap",
        "logger": "flext_target_ldap.target",
        "m": ("flext_target_ldap.models", "FlextTargetLdapModels"),
        "main": "flext_target_ldap.target",
        "models": "flext_target_ldap.models",
        "p": ("flext_target_ldap.protocols", "FlextTargetLdapProtocols"),
        "patterns": "flext_target_ldap.patterns",
        "processing_result": "flext_target_ldap.processing_result",
        "protocols": "flext_target_ldap.protocols",
        "r": "flext_ldap",
        "s": "flext_ldap",
        "settings": "flext_target_ldap.settings",
        "singer": "flext_target_ldap.singer",
        "sinks": "flext_target_ldap.sinks",
        "t": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
        "target": "flext_target_ldap.target",
        "target_client": "flext_target_ldap.target_client",
        "target_config": "flext_target_ldap.target_config",
        "target_services": "flext_target_ldap.target_services",
        "transformation": "flext_target_ldap.transformation",
        "typings": "flext_target_ldap.typings",
        "u": ("flext_target_ldap.utilities", "FlextTargetLdapUtilities"),
        "utilities": "flext_target_ldap.utilities",
        "validate_ldap_config": "flext_target_ldap.settings",
        "x": "flext_ldap",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
