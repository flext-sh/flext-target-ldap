"""LDAP Target Configuration - PEP8 Consolidation.

This module consolidates all LDAP target configuration classes with descriptive PEP8 names,
removing duplication and using proper flext-core + flext-ldap integration.

**Architecture**: Clean Architecture configuration layer
**Patterns**: FlextSettings, FlextValueObject, FlextResult validation
**Integration**: Complete flext-ldap connection config reuse

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_core import (
    FlextResult,
    FlextSettings as BaseSettings,
    FlextValueObject as FlextDomainBaseModel,
)
from flext_ldap import FlextLdapConnectionConfig
from pydantic import Field

# Compatibility warning for Singer adapters migration
warnings.warn(
    "🔄 ARCHITECTURE EVOLUTION: Singer adapters moved from flext-core to flext-meltano.\n"
    "💡 FUTURE PLAN: Use flext_meltano.config.SingerTargetConfig\n"
    "⚡ CURRENT: Temporary compatibility using BaseSettings",
    DeprecationWarning,
    stacklevel=2,
)


class LdapTargetConnectionSettings(FlextDomainBaseModel):
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate LDAP connection business rules."""
        try:
            # Mutual exclusivity validation
            if self.use_ssl and self.use_tls:
                return FlextResult.fail("Cannot use both SSL and TLS simultaneously")

            # Authentication validation
            if self.bind_dn and not self.bind_password:
                return FlextResult.fail(
                    "Bind password required when bind DN is provided",
                )

            # Port validation for protocol
            ldap_standard_port = 389
            ldaps_standard_port = 636

            if self.use_ssl and self.port == ldap_standard_port:
                return FlextResult.fail("SSL typically uses port 636, not 389")
            if (
                not self.use_ssl
                and not self.use_tls
                and self.port == ldaps_standard_port
            ):
                return FlextResult.fail("Port 636 typically requires SSL")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Connection settings validation failed: {e}")


class LdapTargetOperationSettings(FlextDomainBaseModel):
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate operation settings business rules."""
        try:
            # Logical consistency validation
            if not self.create_missing_entries and not self.update_existing_entries:
                return FlextResult.fail(
                    "At least one of create_missing_entries or update_existing_entries must be True",
                )

            # Safety validation for destructive operations
            if self.delete_removed_entries:
                # This is a destructive operation - could add additional validation
                pass

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Operation settings validation failed: {e}")


class LdapTargetMappingSettings(FlextDomainBaseModel):
    """LDAP attribute mapping and transformation settings."""

    attribute_mapping: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping from Singer field names to LDAP attributes",
    )
    object_classes: list[str] = Field(
        default_factory=lambda: ["top"],
        description="Default object classes for new entries",
    )
    search_filter: str = Field(
        "(objectClass=*)",
        description="Default search filter",
    )
    search_scope: str = Field(
        "SUBTREE",
        description="Search scope: BASE, LEVEL, or SUBTREE",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate mapping settings business rules."""
        try:
            # Object class validation
            if not self.object_classes:
                return FlextResult.fail("Object classes cannot be empty")
            if "top" not in self.object_classes:
                # Add 'top' as it's required for all LDAP entries
                self.object_classes.append("top")

            # Search scope validation
            valid_scopes = {"BASE", "LEVEL", "SUBTREE"}
            if self.search_scope.upper() not in valid_scopes:
                return FlextResult.fail(f"Search scope must be one of {valid_scopes}")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Mapping settings validation failed: {e}")


class TargetLdapConfig(BaseSettings):
    """Consolidated LDAP target configuration using enterprise patterns.

    This configuration class consolidates all LDAP target settings while
    leveraging flext-ldap for connection configuration to eliminate duplication.
    """

    # Use real LDAP connection config from flext-ldap - no duplications
    connection: FlextLdapConnectionConfig = Field(
        ...,
        description="LDAP connection configuration from flext-ldap",
    )

    # Target-specific settings (not duplicated) - use composition
    base_dn: str = Field(
        ...,
        description="Base DN for LDAP operations",
        min_length=1,
    )

    # Operation settings
    batch_size: int = Field(1000, description="Batch size for bulk operations", ge=1)
    max_records: int | None = Field(
        None,
        description="Maximum records to process (None for unlimited)",
        ge=1,
    )

    # Entry operation flags
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

    # Mapping and transformation
    attribute_mapping: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping from Singer field names to LDAP attributes",
    )
    object_classes: list[str] = Field(
        default_factory=lambda: ["top"],
        description="Default object classes for new entries",
    )

    # Search settings
    search_filter: str = Field(
        "(objectClass=*)",
        description="Default search filter",
    )
    search_scope: str = Field(
        "SUBTREE",
        description="Search scope: BASE, LEVEL, or SUBTREE",
    )

    class Config:
        """Pydantic configuration."""

        env_prefix = "TARGET_LDAP_"
        case_sensitive = False

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate complete LDAP target configuration business rules."""
        try:
            # Validate operation consistency
            if not self.create_missing_entries and not self.update_existing_entries:
                return FlextResult.fail(
                    "At least one of create_missing_entries or update_existing_entries must be True",
                )

            # Validate object classes
            if not self.object_classes:
                return FlextResult.fail("Object classes cannot be empty")
            if "top" not in self.object_classes:
                self.object_classes.append("top")

            # Validate search scope
            valid_scopes = {"BASE", "LEVEL", "SUBTREE"}
            if self.search_scope.upper() not in valid_scopes:
                return FlextResult.fail(f"Search scope must be one of {valid_scopes}")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Target configuration validation failed: {e}")


def validate_ldap_target_config(
    config: dict[str, object],
) -> FlextResult[TargetLdapConfig]:
    """Validate and create LDAP target configuration with proper error handling."""
    try:
        # Helpers to safely coerce basic types from object
        def _to_int(value: object, default: int) -> int:
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

        def _to_bool(value: object, *, default: bool) -> bool:
            if isinstance(value, bool):
                return value
            if isinstance(value, int):
                return value != 0
            if isinstance(value, str):
                return value.strip().lower() in {"1", "true", "yes", "on"}
            return default

        def _to_str(value: object, default: str = "") -> str:
            return str(value) if value is not None else default

        def _to_str_list(value: object, default: list[str]) -> list[str]:
            if isinstance(value, list):
                return [str(v) for v in value]
            return default

        # Extract connection parameters for FlextLdapConnectionConfig
        connection_params = {
            # Map external dict keys to FlextLdapConnectionConfig fields
            "server": config.get("host", "localhost"),
            "port": config.get("port", 389),
            "use_ssl": config.get("use_ssl", False),
            "bind_dn": config.get("bind_dn", ""),
            "bind_password": config.get("password", ""),
            "timeout": config.get("timeout", 30),
        }

        # Create connection config using flext-ldap with strict coercion
        server = _to_str(connection_params["server"], "localhost")
        port = _to_int(connection_params["port"], 389)
        use_ssl = _to_bool(connection_params["use_ssl"], default=False)
        bind_dn = _to_str(connection_params["bind_dn"], "")
        bind_password = _to_str(connection_params["bind_password"], "")
        timeout = _to_int(connection_params["timeout"], 30)

        connection_config = FlextLdapConnectionConfig(
            server=server,
            port=port,
            use_ssl=use_ssl,
            bind_dn=bind_dn,
            bind_password=bind_password,
            timeout=timeout,
        )

        # Build TargetLdapConfig explicitly with proper coercion
        base_dn = _to_str(config.get("base_dn", ""))
        batch_size = _to_int(config.get("batch_size", 1000), 1000)
        max_records_val = config.get("max_records")
        if isinstance(max_records_val, bool):
            max_records: int | None = None
        elif isinstance(max_records_val, int):
            max_records = max_records_val
        elif isinstance(max_records_val, str):
            try:
                max_records = int(max_records_val)
            except ValueError:
                max_records = None
        else:
            max_records = None

        create_missing_entries = _to_bool(
            config.get("create_missing_entries", True),
            default=True,
        )
        update_existing_entries = _to_bool(
            config.get("update_existing_entries", True),
            default=True,
        )
        delete_removed_entries = _to_bool(
            config.get("delete_removed_entries", False),
            default=False,
        )

        raw_attr_map = config.get("attribute_mapping", {})
        attribute_mapping: dict[str, str] = (
            {str(k): str(v) for k, v in raw_attr_map.items()}
            if isinstance(raw_attr_map, dict)
            else {}
        )
        object_classes = _to_str_list(
            config.get("object_classes", ["top"]),
            ["top"],
        )
        search_filter = _to_str(config.get("search_filter", "(objectClass=*)"))
        search_scope = _to_str(config.get("search_scope", "SUBTREE"))

        # Create final config
        validated_config = TargetLdapConfig(
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

        # Run business rules validation
        validation_result = validated_config.validate_business_rules()
        if not validation_result.is_success:
            return FlextResult.fail(validation_result.error or "Invalid configuration")

        return FlextResult.ok(validated_config)

    except (ValueError, TypeError, RuntimeError) as e:
        return FlextResult.fail(f"Configuration validation failed: {e}")


def create_default_ldap_target_config(
    host: str,
    base_dn: str,
    *,
    port: int = 389,
    use_ssl: bool = False,
) -> FlextResult[TargetLdapConfig]:
    """Create default LDAP target configuration with minimal parameters."""
    try:
        # Create connection config
        connection_config = FlextLdapConnectionConfig(
            server=host,
            port=port,
            use_ssl=use_ssl,
            timeout=30,
        )

        # Create target config
        target_config = TargetLdapConfig(
            connection=connection_config,
            base_dn=base_dn,
        )

        # Validate business rules
        validation_result = target_config.validate_business_rules()
        if not validation_result.is_success:
            return FlextResult.fail(validation_result.error or "Invalid configuration")

        return FlextResult.ok(target_config)

    except (ValueError, TypeError, RuntimeError) as e:
        return FlextResult.fail(f"Default configuration creation failed: {e}")


# Backward compatibility aliases
TargetLDAPConfig = TargetLdapConfig
LDAPConnectionSettings = LdapTargetConnectionSettings
LDAPOperationSettings = LdapTargetOperationSettings

__all__ = [
    "LDAPConnectionSettings",  # Backward compatibility
    "LDAPOperationSettings",  # Backward compatibility
    "LdapTargetConnectionSettings",
    "LdapTargetMappingSettings",
    "LdapTargetOperationSettings",
    "TargetLDAPConfig",  # Backward compatibility
    "TargetLdapConfig",
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
]
