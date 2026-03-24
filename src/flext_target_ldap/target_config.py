"""LDAP Target Configuration - PEP8 Consolidation.

This module consolidates all LDAP target configuration classes with descriptive PEP8 names,
removing duplication and using proper flext-core + flext-ldap integration.

Architecture: Clean Architecture configuration layer
Patterns: "FlextSettings", FlextModels, r validation
Integration: Complete flext-ldap connection config reuse

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import r

from flext_target_ldap import FlextTargetLdapSettings, c, m, t, u


def validate_ldap_target_config(
    config: Mapping[str, t.ContainerValue],
) -> r[FlextTargetLdapSettings]:
    """Validate and create LDAP target configuration with proper error handling."""
    try:
        connection_config = u.TypeConversion.build_connection_config(config)
        base_dn = u.TypeConversion.to_str(config.get("base_dn", ""))
        batch_size = u.TypeConversion.to_int(config.get("batch_size", 1000), 1000)
        max_records_val = config.get("max_records")
        max_records: int | None
        match max_records_val:
            case bool():
                max_records = None
            case int():
                max_records = max_records_val
            case str():
                try:
                    max_records = int(max_records_val)
                except ValueError:
                    max_records = None
            case _:
                max_records = None
        create_missing_entries = u.TypeConversion.to_bool(
            config.get("create_missing_entries", True),
            default=True,
        )
        update_existing_entries = u.TypeConversion.to_bool(
            config.get("update_existing_entries", True),
            default=True,
        )
        delete_removed_entries = u.TypeConversion.to_bool(
            config.get("delete_removed_entries", False),
            default=False,
        )
        attribute_mapping = u.TypeConversion.extract_attribute_mapping(config)
        object_classes = u.TypeConversion.extract_object_classes(config)
        search_filter = u.TypeConversion.to_str(
            config.get("search_filter", "(objectClass=*)"),
        )
        search_scope = u.TypeConversion.to_str(config.get("search_scope", "SUBTREE"))
        validated_config = FlextTargetLdapSettings.model_validate({
            "connection": connection_config,
            "base_dn": base_dn,
            "batch_size": batch_size,
            "max_records": max_records,
            "create_missing_entries": create_missing_entries,
            "update_existing_entries": update_existing_entries,
            "delete_removed_entries": delete_removed_entries,
            "attribute_mapping": attribute_mapping,
            "object_classes": object_classes,
            "search_filter": search_filter,
            "search_scope": search_scope,
        })
        return r[FlextTargetLdapSettings].ok(validated_config)
    except (ValueError, TypeError, RuntimeError) as e:
        return r[FlextTargetLdapSettings].fail(f"Configuration validation failed: {e}")


def create_default_ldap_target_config(
    host: str,
    base_dn: str,
    *,
    port: int = c.Ldap.ConnectionDefaults.PORT,
    use_ssl: bool = False,
) -> r[FlextTargetLdapSettings]:
    """Create default LDAP target configuration with minimal parameters."""
    try:
        connection_config = m.Ldap.ConnectionConfig(
            host=host,
            port=port,
            use_ssl=use_ssl,
            timeout=30,
        )
        target_config = FlextTargetLdapSettings(
            connection=connection_config,
            base_dn=base_dn,
            batch_size=1000,
            max_records=None,
            search_filter="(objectClass=*)",
            search_scope="SUBTREE",
            attribute_mapping={},
            object_classes=["top"],
        )
        return r[FlextTargetLdapSettings].ok(target_config)
    except (ValueError, TypeError, RuntimeError) as e:
        return r[FlextTargetLdapSettings].fail(
            f"Default configuration creation failed: {e}",
        )


__all__ = [
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
]
