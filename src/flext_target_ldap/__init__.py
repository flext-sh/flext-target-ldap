# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
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
        api_service,
        application,
        catalog,
        client,
        config,
        constants,
        errors,
        ldap_patterns,
        models,
        orchestrator,
        patterns,
        processing_result,
        protocols,
        service_runtime,
        services,
        settings,
        singer,
        sinks,
        stream,
        target,
        transformation,
        typings,
        utilities,
    )
    from flext_target_ldap._models import (
        FlextTargetLdapProcessingCounters,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        msg,
    )
    from flext_target_ldap._utilities import (
        FlextTargetLdapApiService,
        FlextTargetLdapClient,
        FlextTargetLdapConnectionService,
        FlextTargetLdapSearchEntry,
        FlextTargetLdapServiceRuntime,
        FlextTargetLdapTransformationEngine,
        attribute_mapping,
        base_dn,
        batch_size,
        connection,
        connection_config,
        create_default_ldap_target_config,
        create_missing_entries,
        default,
        delete_removed_entries,
        host,
        max_records,
        max_records_val,
        object_classes,
        port,
        search_filter,
        search_scope,
        target_config,
        timeout,
        update_existing_entries,
        use_ssl,
        validate_ldap_target_config,
        validated_config,
    )
    from flext_target_ldap.api import FlextTargetLdapService
    from flext_target_ldap.application import FlextTargetLdapOrchestrator
    from flext_target_ldap.catalog import build_singer_catalog
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants,
        FlextTargetLdapConstants as c,
    )
    from flext_target_ldap.errors import FlextTargetLdapError
    from flext_target_ldap.models import (
        FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )
    from flext_target_ldap.patterns import FlextTargetLdapTypeConverter
    from flext_target_ldap.protocols import (
        FlextTargetLdapProtocols,
        FlextTargetLdapProtocols as p,
    )
    from flext_target_ldap.settings import FlextTargetLdapSettings
    from flext_target_ldap.singer import (
        FlextTargetLdapCatalogManager,
        FlextTargetLdapSingerTarget,
        FlextTargetLdapStreamProcessingStats,
        logger,
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
        "FlextTargetLdapConstants": "flext_target_ldap.constants",
        "FlextTargetLdapError": "flext_target_ldap.errors",
        "FlextTargetLdapModels": "flext_target_ldap.models",
        "FlextTargetLdapProtocols": "flext_target_ldap.protocols",
        "FlextTargetLdapService": "flext_target_ldap.api",
        "FlextTargetLdapSettings": "flext_target_ldap.settings",
        "FlextTargetLdapTypes": "flext_target_ldap.typings",
        "FlextTargetLdapUtilities": "flext_target_ldap.utilities",
        "_models": "flext_target_ldap._models",
        "_utilities": "flext_target_ldap._utilities",
        "api": "flext_target_ldap.api",
        "api_service": "flext_target_ldap.api_service",
        "application": "flext_target_ldap.application",
        "build_singer_catalog": "flext_target_ldap.catalog",
        "c": ("flext_target_ldap.constants", "FlextTargetLdapConstants"),
        "catalog": "flext_target_ldap.catalog",
        "client": "flext_target_ldap.client",
        "config": "flext_target_ldap.config",
        "constants": "flext_target_ldap.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "errors": "flext_target_ldap.errors",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "ldap_patterns": "flext_target_ldap.ldap_patterns",
        "m": ("flext_target_ldap.models", "FlextTargetLdapModels"),
        "main": "flext_target_ldap.target",
        "models": "flext_target_ldap.models",
        "orchestrator": "flext_target_ldap.orchestrator",
        "p": ("flext_target_ldap.protocols", "FlextTargetLdapProtocols"),
        "patterns": "flext_target_ldap.patterns",
        "processing_result": "flext_target_ldap.processing_result",
        "protocols": "flext_target_ldap.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "service_runtime": "flext_target_ldap.service_runtime",
        "services": "flext_target_ldap.services",
        "settings": "flext_target_ldap.settings",
        "singer": "flext_target_ldap.singer",
        "sinks": "flext_target_ldap.sinks",
        "stream": "flext_target_ldap.stream",
        "t": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
        "target": "flext_target_ldap.target",
        "transformation": "flext_target_ldap.transformation",
        "typings": "flext_target_ldap.typings",
        "u": ("flext_target_ldap.utilities", "FlextTargetLdapUtilities"),
        "utilities": "flext_target_ldap.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
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
