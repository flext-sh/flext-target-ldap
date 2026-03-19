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

from flext_target_ldap import FlextTargetLdapSettings, c, m, r, t, u


def _target_config_to_int(value: t.ContainerValue, default: int) -> int:
    """Convert value to int for target config."""
    match value:
        case bool():
            return default
        case int():
            return value
        case str():
            try:
                return int(value)
            except ValueError:
                return default
        case _:
            return default


def _target_config_to_bool(value: t.ContainerValue, *, default: bool) -> bool:
    """Convert value to bool for target config."""
    match value:
        case bool():
            return value
        case int():
            return value != 0
        case str():
            return value.strip().lower() in {"1", "true", "yes", "on"}
        case _:
            return default


def _target_config_to_str(value: t.ContainerValue, default: str = "") -> str:
    """Convert value to str for target config."""
    return str(value) if value is not None else default


def _target_config_to_str_list(
    value: t.ContainerValue,
    default: list[str],
) -> list[str]:
    """Convert value to string list."""
    if u.is_list(value):
        return [str(v) for v in value]
    return default


def _build_target_connection_config(
    config: dict[str, t.ContainerValue],
) -> m.Ldap.ConnectionConfig:
    """Build connection config for target."""
    server = _target_config_to_str(config.get("host", "localhost"), "localhost")
    port = _target_config_to_int(config.get("port", 389), 389)
    use_ssl = _target_config_to_bool(config.get("use_ssl", False), default=False)
    bind_dn = _target_config_to_str(config.get("bind_dn", ""), "")
    bind_password = _target_config_to_str(config.get("password", ""), "")
    timeout = _target_config_to_int(config.get("timeout", 30), 30)
    return m.Ldap.ConnectionConfig(
        host=server,
        port=port,
        use_ssl=use_ssl,
        bind_dn=bind_dn,
        bind_password=bind_password,
        timeout=timeout,
    )


def _extract_target_max_records(config: dict[str, t.ContainerValue]) -> int | None:
    """Extract max records from config."""
    max_records_val = config.get("max_records")
    match max_records_val:
        case bool():
            return None
        case int():
            return max_records_val
        case str():
            try:
                return int(max_records_val)
            except ValueError:
                return None
        case _:
            return None


def validate_ldap_target_config(
    config: dict[str, t.ContainerValue],
) -> r[FlextTargetLdapSettings]:
    """Validate and create LDAP target configuration with proper error handling."""
    try:
        connection_config = _build_target_connection_config(config)
        base_dn = _target_config_to_str(config.get("base_dn", ""))
        batch_size = _target_config_to_int(config.get("batch_size", 1000), 1000)
        max_records = _extract_target_max_records(config)
        create_missing_entries = _target_config_to_bool(
            config.get("create_missing_entries", True),
            default=True,
        )
        update_existing_entries = _target_config_to_bool(
            config.get("update_existing_entries", True),
            default=True,
        )
        delete_removed_entries = _target_config_to_bool(
            config.get("delete_removed_entries", False),
            default=False,
        )
        attribute_mapping: dict[str, str] = {}
        raw_attr_map_obj = config.get("attribute_mapping")
        match raw_attr_map_obj:
            case Mapping() as mapping_value:
                for k, v in mapping_value.items():
                    attribute_mapping[str(k)] = str(v)
            case _:
                pass
        object_classes = _target_config_to_str_list(
            config.get("object_classes", ["top"]),
            ["top"],
        )
        search_filter = _target_config_to_str(
            config.get("search_filter", "(objectClass=*)"),
        )
        search_scope = _target_config_to_str(config.get("search_scope", "SUBTREE"))
        validated_config = FlextTargetLdapSettings(
            connection=connection_config,
            base_dn=base_dn,
            batch_size=batch_size,
            max_records=max_records,
            create_missing_entries=create_missing_entries,
            update_existing_entries=update_existing_entries,
            delete_removed_entries=delete_removed_entries,
            attribute_mapping=attribute_mapping,
            object_classes=object_classes,
            search_filter=search_filter,
            search_scope=search_scope,
        )
        return r[FlextTargetLdapSettings].ok(validated_config)
    except (ValueError, TypeError, RuntimeError) as e:
        return r[FlextTargetLdapSettings].fail(f"Configuration validation failed: {e}")


def create_default_ldap_target_config(
    host: str,
    base_dn: str,
    *,
    port: int = c.TargetLdap.Connection.DEFAULT_PORT,
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
