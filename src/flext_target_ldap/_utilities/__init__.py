# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_ldap._utilities.api_service as _flext_target_ldap__utilities_api_service

    api_service = _flext_target_ldap__utilities_api_service
    import flext_target_ldap._utilities.client as _flext_target_ldap__utilities_client
    from flext_target_ldap._utilities.api_service import FlextTargetLdapApiService

    client = _flext_target_ldap__utilities_client
    import flext_target_ldap._utilities.config as _flext_target_ldap__utilities_config
    from flext_target_ldap._utilities.client import FlextTargetLdapClient

    config = _flext_target_ldap__utilities_config
    import flext_target_ldap._utilities.service_runtime as _flext_target_ldap__utilities_service_runtime
    from flext_target_ldap._utilities.config import (
        FlextTargetLdapConfigFactory,
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
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
    )
_LAZY_IMPORTS = {
    "FlextTargetLdapApiService": (
        "flext_target_ldap._utilities.api_service",
        "FlextTargetLdapApiService",
    ),
    "FlextTargetLdapClient": (
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapClient",
    ),
    "FlextTargetLdapConfigFactory": (
        "flext_target_ldap._utilities.config",
        "FlextTargetLdapConfigFactory",
    ),
    "FlextTargetLdapConnectionService": (
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapConnectionService",
    ),
    "FlextTargetLdapMigrationValidator": (
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapMigrationValidator",
    ),
    "FlextTargetLdapServiceRuntime": (
        "flext_target_ldap._utilities.service_runtime",
        "FlextTargetLdapServiceRuntime",
    ),
    "FlextTargetLdapTransformationEngine": (
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapTransformationEngine",
    ),
    "FlextTargetLdapTransformationService": (
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapTransformationService",
    ),
    "api_service": "flext_target_ldap._utilities.api_service",
    "client": "flext_target_ldap._utilities.client",
    "config": "flext_target_ldap._utilities.config",
    "create_default_ldap_target_config": (
        "flext_target_ldap._utilities.config",
        "create_default_ldap_target_config",
    ),
    "service_runtime": "flext_target_ldap._utilities.service_runtime",
    "services": "flext_target_ldap._utilities.services",
    "transformation": "flext_target_ldap._utilities.transformation",
    "validate_ldap_target_config": (
        "flext_target_ldap._utilities.config",
        "validate_ldap_target_config",
    ),
}

__all__ = [
    "FlextTargetLdapApiService",
    "FlextTargetLdapClient",
    "FlextTargetLdapConfigFactory",
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapServiceRuntime",
    "FlextTargetLdapTransformationEngine",
    "FlextTargetLdapTransformationService",
    "api_service",
    "client",
    "config",
    "create_default_ldap_target_config",
    "service_runtime",
    "services",
    "transformation",
    "validate_ldap_target_config",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
