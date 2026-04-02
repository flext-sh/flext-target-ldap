# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-ldap."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_target_ldap._utilities import (
        api_service,
        client,
        config,
        service_runtime,
        services,
        transformation,
    )
    from flext_target_ldap._utilities.api_service import FlextTargetLdapApiService
    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient,
        FlextTargetLdapSearchEntry,
    )
    from flext_target_ldap._utilities.config import (
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime,
    )
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapConnectionService,
        FlextTargetLdapTransformationService,
    )
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
        logger,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTargetLdapApiService": "flext_target_ldap._utilities.api_service",
    "FlextTargetLdapClient": "flext_target_ldap._utilities.client",
    "FlextTargetLdapConnectionService": "flext_target_ldap._utilities.services",
    "FlextTargetLdapMigrationValidator": "flext_target_ldap._utilities.transformation",
    "FlextTargetLdapSearchEntry": "flext_target_ldap._utilities.client",
    "FlextTargetLdapServiceRuntime": "flext_target_ldap._utilities.service_runtime",
    "FlextTargetLdapTransformationEngine": "flext_target_ldap._utilities.transformation",
    "FlextTargetLdapTransformationService": "flext_target_ldap._utilities.services",
    "api_service": "flext_target_ldap._utilities.api_service",
    "client": "flext_target_ldap._utilities.client",
    "config": "flext_target_ldap._utilities.config",
    "create_default_ldap_target_config": "flext_target_ldap._utilities.config",
    "logger": "flext_target_ldap._utilities.transformation",
    "service_runtime": "flext_target_ldap._utilities.service_runtime",
    "services": "flext_target_ldap._utilities.services",
    "transformation": "flext_target_ldap._utilities.transformation",
    "validate_ldap_target_config": "flext_target_ldap._utilities.config",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
