# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_target_ldap import (
        api_service,
        client,
        config,
        service_runtime,
        services,
        transformation,
    )
    from flext_target_ldap.api_service import FlextTargetLdapApiService
    from flext_target_ldap.client import (
        FlextTargetLdapClient,
        FlextTargetLdapSearchEntry,
    )
    from flext_target_ldap.config import (
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
    from flext_target_ldap.service_runtime import FlextTargetLdapServiceRuntime
    from flext_target_ldap.services import FlextTargetLdapConnectionService
    from flext_target_ldap.transformation import (
        FlextTargetLdapTransformationEngine,
        logger,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTargetLdapApiService": "flext_target_ldap.api_service",
    "FlextTargetLdapClient": "flext_target_ldap.client",
    "FlextTargetLdapConnectionService": "flext_target_ldap.services",
    "FlextTargetLdapSearchEntry": "flext_target_ldap.client",
    "FlextTargetLdapServiceRuntime": "flext_target_ldap.service_runtime",
    "FlextTargetLdapTransformationEngine": "flext_target_ldap.transformation",
    "api_service": "flext_target_ldap.api_service",
    "attribute_mapping": "flext_target_ldap.config",
    "base_dn": "flext_target_ldap.config",
    "batch_size": "flext_target_ldap.config",
    "client": "flext_target_ldap.client",
    "config": "flext_target_ldap.config",
    "connection": "flext_target_ldap.config",
    "connection_config": "flext_target_ldap.config",
    "create_default_ldap_target_config": "flext_target_ldap.config",
    "create_missing_entries": "flext_target_ldap.config",
    "default": "flext_target_ldap.config",
    "delete_removed_entries": "flext_target_ldap.config",
    "host": "flext_target_ldap.config",
    "logger": "flext_target_ldap.transformation",
    "max_records": "flext_target_ldap.config",
    "max_records_val": "flext_target_ldap.config",
    "object_classes": "flext_target_ldap.config",
    "port": "flext_target_ldap.config",
    "search_filter": "flext_target_ldap.config",
    "search_scope": "flext_target_ldap.config",
    "service_runtime": "flext_target_ldap.service_runtime",
    "services": "flext_target_ldap.services",
    "target_config": "flext_target_ldap.config",
    "timeout": "flext_target_ldap.config",
    "transformation": "flext_target_ldap.transformation",
    "update_existing_entries": "flext_target_ldap.config",
    "use_ssl": "flext_target_ldap.config",
    "validate_ldap_target_config": "flext_target_ldap.config",
    "validated_config": "flext_target_ldap.config",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
