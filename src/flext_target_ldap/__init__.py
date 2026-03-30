# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

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
    from flext_ldap import *

    from flext_target_ldap import (
        catalog,
        constants,
        errors,
        models,
        processing_result,
        protocols,
        settings,
        sinks,
        target,
        target_client,
        target_config,
        target_services,
        transformation,
        typings,
        utilities,
    )
    from flext_target_ldap._models import *
    from flext_target_ldap._utilities import *
    from flext_target_ldap.application import *
    from flext_target_ldap.catalog import *
    from flext_target_ldap.constants import *
    from flext_target_ldap.errors import *
    from flext_target_ldap.models import *
    from flext_target_ldap.patterns import *
    from flext_target_ldap.protocols import *
    from flext_target_ldap.settings import *
    from flext_target_ldap.singer import *
    from flext_target_ldap.target import *
    from flext_target_ldap.transformation import *
    from flext_target_ldap.typings import *
    from flext_target_ldap.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "DataTransformationEngine": "flext_target_ldap.transformation",
    "FlextTargetLdap": "flext_target_ldap.target",
    "FlextTargetLdapApiService": "flext_target_ldap._utilities.services",
    "FlextTargetLdapAuthenticationError": "flext_target_ldap.errors",
    "FlextTargetLdapBaseSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapCatalogManager": "flext_target_ldap.singer.catalog",
    "FlextTargetLdapClient": "flext_target_ldap._utilities.client",
    "FlextTargetLdapConfigurationError": "flext_target_ldap.errors",
    "FlextTargetLdapConnectionError": "flext_target_ldap.errors",
    "FlextTargetLdapConnectionService": "flext_target_ldap._utilities.services",
    "FlextTargetLdapConstants": "flext_target_ldap.constants",
    "FlextTargetLdapDataTransformer": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapEntryManager": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapError": "flext_target_ldap.errors",
    "FlextTargetLdapGroupsSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapMigrationValidator": "flext_target_ldap._utilities.transformation",
    "FlextTargetLdapModels": "flext_target_ldap.models",
    "FlextTargetLdapOrchestrator": "flext_target_ldap.application.orchestrator",
    "FlextTargetLdapOrganizationalUnitsSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapProcessingCounters": "flext_target_ldap._models.processing_result",
    "FlextTargetLdapProcessingError": "flext_target_ldap.errors",
    "FlextTargetLdapProcessingResult": "flext_target_ldap._models.sinks",
    "FlextTargetLdapProtocols": "flext_target_ldap.protocols",
    "FlextTargetLdapSchemaMapper": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapSearchEntry": "flext_target_ldap._utilities.client",
    "FlextTargetLdapSettings": "flext_target_ldap.settings",
    "FlextTargetLdapSingerTarget": "flext_target_ldap.singer.target",
    "FlextTargetLdapSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapStreamProcessingStats": "flext_target_ldap.singer.stream",
    "FlextTargetLdapStreamProcessor": "flext_target_ldap.singer.stream",
    "FlextTargetLdapTarget": "flext_target_ldap._models.sinks",
    "FlextTargetLdapTimeoutError": "flext_target_ldap.errors",
    "FlextTargetLdapTransformationEngine": "flext_target_ldap._utilities.transformation",
    "FlextTargetLdapTransformationService": "flext_target_ldap._utilities.services",
    "FlextTargetLdapTypeConverter": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapTypes": "flext_target_ldap.typings",
    "FlextTargetLdapUsersSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapUtilities": "flext_target_ldap.utilities",
    "FlextTargetLdapValidationError": "flext_target_ldap.errors",
    "MigrationValidator": "flext_target_ldap.transformation",
    "_models": "flext_target_ldap._models",
    "_utilities": "flext_target_ldap._utilities",
    "application": "flext_target_ldap.application",
    "build_singer_catalog": "flext_target_ldap.catalog",
    "c": ["flext_target_ldap.constants", "FlextTargetLdapConstants"],
    "catalog": "flext_target_ldap.catalog",
    "client": "flext_target_ldap._utilities.client",
    "config": "flext_target_ldap._utilities.config",
    "constants": "flext_target_ldap.constants",
    "create_default_ldap_target_config": "flext_target_ldap._utilities.config",
    "d": "flext_ldap",
    "e": "flext_ldap",
    "errors": "flext_target_ldap.errors",
    "h": "flext_ldap",
    "ldap_patterns": "flext_target_ldap.patterns.ldap_patterns",
    "logger": "flext_target_ldap.target",
    "m": ["flext_target_ldap.models", "FlextTargetLdapModels"],
    "main": "flext_target_ldap.target",
    "models": "flext_target_ldap.models",
    "orchestrator": "flext_target_ldap.application.orchestrator",
    "p": ["flext_target_ldap.protocols", "FlextTargetLdapProtocols"],
    "patterns": "flext_target_ldap.patterns",
    "processing_result": "flext_target_ldap.processing_result",
    "protocols": "flext_target_ldap.protocols",
    "r": "flext_ldap",
    "s": "flext_ldap",
    "services": "flext_target_ldap._utilities.services",
    "settings": "flext_target_ldap.settings",
    "singer": "flext_target_ldap.singer",
    "sinks": "flext_target_ldap.sinks",
    "stream": "flext_target_ldap.singer.stream",
    "t": ["flext_target_ldap.typings", "FlextTargetLdapTypes"],
    "target": "flext_target_ldap.target",
    "target_client": "flext_target_ldap.target_client",
    "target_config": "flext_target_ldap.target_config",
    "target_services": "flext_target_ldap.target_services",
    "transformation": "flext_target_ldap.transformation",
    "typings": "flext_target_ldap.typings",
    "u": ["flext_target_ldap.utilities", "FlextTargetLdapUtilities"],
    "utilities": "flext_target_ldap.utilities",
    "validate_ldap_config": "flext_target_ldap.settings",
    "validate_ldap_target_config": "flext_target_ldap._utilities.config",
    "x": "flext_ldap",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
