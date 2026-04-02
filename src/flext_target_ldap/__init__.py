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
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
        protocols,
        settings,
        singer,
        target,
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
        processing_result,
        sinks,
    )
    from flext_target_ldap._utilities import (
        FlextTargetLdapApiService,
        FlextTargetLdapClient,
        FlextTargetLdapConnectionService,
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapSearchEntry,
        FlextTargetLdapServiceRuntime,
        FlextTargetLdapTransformationEngine,
        FlextTargetLdapTransformationService,
        api_service,
        client,
        config,
        create_default_ldap_target_config,
        service_runtime,
        services,
        transformation,
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
    from flext_target_ldap.target import FlextTargetLdap, main
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes,
        FlextTargetLdapTypes as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
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
