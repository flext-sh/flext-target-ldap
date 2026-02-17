"""LDAP Target Configuration - PEP8 Consolidation.

This module consolidates all LDAP target configuration classes with descriptive PEP8 names,
removing duplication and using proper flext-core + flext-ldap integration.

Architecture: Clean Architecture configuration layer
Patterns: "FlextSettings", FlextModels, FlextResult validation
Integration: Complete flext-ldap connection config reuse

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult, FlextSettings
from flext_ldap import FlextLdapModels
from pydantic import Field

from .settings import FlextTargetLdapSettings
from .typings import t


class LdapTargetConnectionSettings(FlextSettings):
    """LDAP connection settings domain model with business validation."""

    host: str = Field(..., description="LDAP server host", min_length=1)
    port: int = Field(389, description="LDAP server port", ge=1, le=65535)
    use_ssl: bool = Field(default=False, description="Use SSL connection")
    use_tls: bool = Field(default=False, description="Use TLS connection")
    bind_dn: str | None = Field(None, description="Bind DN for authentication")
    bind_password: str | None = Field(None, description="Bind password")
    base_dn: str = Field(..., description="Base DN for operations", min_length=1)
    connect_timeout: int = Field(10, description="Connection timeout in seconds", ge=1)
    receive_timeout: int = Field(30, description="Receive timeout in seconds", ge=1)

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate LDAP connection business rules."""
        try:
            # Mutual exclusivity validation
            if self.use_ssl and self.use_tls:
                return FlextResult[bool].fail(
                    "Cannot use both SSL and TLS simultaneously",
                )

            # Authentication validation
            if self.bind_dn and not self.bind_password:
                return FlextResult[bool].fail(
                    "Bind password required when bind DN is provided",
                )

            # Port validation for protocol
            ldap_standard_port = 389
            ldaps_standard_port = 636

            if self.use_ssl and self.port == ldap_standard_port:
                return FlextResult[bool].fail("SSL typically uses port 636, not 389")
            if (
                not self.use_ssl
                and not self.use_tls
                and self.port == ldaps_standard_port
            ):
                return FlextResult[bool].fail("Port 636 typically requires SSL")

            return FlextResult[bool].ok(value=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Connection settings validation failed: {e}")


class LdapTargetOperationSettings(FlextSettings):
    """LDAP operation settings domain model with business validation."""

    batch_size: int = Field(1000, description="Batch size for bulk operations", ge=1)
    max_records: int | None = Field(
        None,
        description="Maximum records to process (None for unlimited)",
        ge=1,
    )
    create_missing_entries: bool = Field(
        default=True,
        description="Create entries that don't exist",
    )
    update_existing_entries: bool = Field(
        default=True,
        description="Update existing entries",
    )
    delete_removed_entries: bool = Field(
        default=False,
        description="Delete entries not in source",
    )

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate operation settings business rules."""
        try:
            # Logical consistency validation
            if not self.create_missing_entries and not self.update_existing_entries:
                return FlextResult[bool].fail(
                    "At least one of create_missing_entries or update_existing_entries must be True",
                )

            # Safety validation for destructive operations
            if self.delete_removed_entries:
                # This is a destructive operation - could add additional validation
                pass

            return FlextResult[bool].ok(value=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Operation settings validation failed: {e}")


class LdapTargetMappingSettings(FlextSettings):
    """LDAP attribute mapping and transformation settings."""

    attribute_mapping: t.Core.Headers = Field(
        default_factory=dict,
        description="Mapping from Singer field names to LDAP attributes",
    )
    object_classes: t.Core.StringList = Field(
        default_factory=lambda: ["top"],
        description="Default object classes for new entries",
    )
    search_filter: str = Field(
        "(objectClass=*)",
        description="Default search filter",
    )
    search_scope: str = Field(
        "SUBTREE",
        description='Search scope: "BASE", LEVEL, or SUBTREE',
    )

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate mapping settings business rules."""
        try:
            # Object class validation
            if not self.object_classes:
                return FlextResult[bool].fail("Object classes cannot be empty")
            if "top" not in self.object_classes:
                # Add 'top' as it's required for all LDAP entries
                self.object_classes.append("top")

            # Search scope validation
            valid_scopes = {"BASE", "LEVEL", "SUBTREE"}
            if self.search_scope.upper() not in valid_scopes:
                return FlextResult[bool].fail(
                    f"Search scope must be one of {valid_scopes}",
                )

            return FlextResult[bool].ok(value=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Mapping settings validation failed: {e}")


def _target_config_to_int(value: t.GeneralValueType, default: int) -> int:
    """Convert value to int for target config."""
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


def _target_config_to_bool(
    value: t.GeneralValueType,
    *,
    default: bool,
) -> bool:
    """Convert value to bool for target config."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return default


def _target_config_to_str(value: t.GeneralValueType, default: str = "") -> str:
    """Convert value to str for target config."""
    return str(value) if value is not None else default


def _target_config_to_str_list(
    value: t.GeneralValueType,
    default: t.Core.StringList,
) -> t.Core.StringList:
    """Convert value to string list."""
    if isinstance(value, list):
        return [str(v) for v in value]
    return default


def _build_target_connection_config(
    config: t.Core.Dict,
) -> FlextLdapModels.Ldap.ConnectionConfig:
    """Build connection config for target."""
    server = _target_config_to_str(config.get("host", "localhost"), "localhost")
    port = _target_config_to_int(config.get("port", 389), 389)
    use_ssl = _target_config_to_bool(config.get("use_ssl", False), default=False)
    bind_dn = _target_config_to_str(config.get("bind_dn", ""), "")
    bind_password = _target_config_to_str(config.get("password", ""), "")
    timeout = _target_config_to_int(config.get("timeout", 30), 30)

    return FlextLdapModels.Ldap.ConnectionConfig(
        host=server,
        port=port,
        use_ssl=use_ssl,
        bind_dn=bind_dn,
        bind_password=bind_password,
        timeout=timeout,
    )


def _extract_target_max_records(config: t.Core.Dict) -> int | None:
    """Extract max records from config."""
    max_records_val = config.get("max_records")
    if isinstance(max_records_val, bool):
        return None
    if isinstance(max_records_val, int):
        return max_records_val
    if isinstance(max_records_val, str):
        try:
            return int(max_records_val)
        except ValueError:
            return None
    return None


def validate_ldap_target_config(
    config: t.Core.Dict,
) -> FlextResult[FlextTargetLdapSettings]:
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

        raw_attr_map_value: t.GeneralValueType = config.get("attribute_mapping", {})
        attribute_mapping: t.Core.Headers = (
            {str(k): str(v) for k, v in raw_attr_map_value.items()}
            if isinstance(raw_attr_map_value, dict)
            else {}
        )
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

        return FlextResult[FlextTargetLdapSettings].ok(validated_config)

    except (ValueError, TypeError, RuntimeError) as e:
        return FlextResult[FlextTargetLdapSettings].fail(
            f"Configuration validation failed: {e}",
        )


def create_default_ldap_target_config(
    host: str,
    base_dn: str,
    *,
    port: int = 389,
    use_ssl: bool = False,
) -> FlextResult[FlextTargetLdapSettings]:
    """Create default LDAP target configuration with minimal parameters."""
    try:
        # Create connection config
        connection_config = FlextLdapModels.Ldap.ConnectionConfig(
            host=host,
            port=port,
            use_ssl=use_ssl,
            timeout=30,
        )

        # Create target config
        target_config = FlextTargetLdapSettings(
            connection=connection_config,
            base_dn=base_dn,
            batch_size=1000,
            max_records=None,
            search_filter="(objectClass=*)",
            search_scope="SUBTREE",
        )

        return FlextResult[FlextTargetLdapSettings].ok(target_config)

    except (ValueError, TypeError, RuntimeError) as e:
        return FlextResult[FlextTargetLdapSettings].fail(
            f"Default configuration creation failed: {e}",
        )


__all__ = [
    "LdapTargetConnectionSettings",
    "LdapTargetMappingSettings",
    "LdapTargetOperationSettings",
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
]
