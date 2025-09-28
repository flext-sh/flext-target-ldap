"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import Self

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import (
    FlextConfig,
    FlextModels,
    FlextResult,
)
from flext_ldap import FlextLdapModels
from flext_target_ldap.typings import FlextTargetLdapTypes

# Compatibility warning for Singer adapters migration
warnings.warn(
    "🔄 ARCHITECTURE EVOLUTION: Singer adapters moved from flext-core to flext-meltano.\n"
    "💡 FUTURE PLAN: Use flext_meltano.config.SingerTargetConfig\n"
    "⚡ CURRENT: Updated to use FlextConfig.Settings from flext-core",
    DeprecationWarning,
    stacklevel=2,
)


class TargetLDAPConfig(FlextConfig):
    """LDAP target configuration using consolidated patterns."""

    # Use real LDAP connection config from flext-ldap - no duplications
    connection: FlextLdapModels.ConnectionConfig = Field(
        ...,
        description="LDAP connection configuration",
    )

    # Target-specific settings (not duplicated)
    base_dn: str = Field(
        ...,
        description="Base DN for LDAP operations",
    )  # Keep for compatibility
    search_filter: str = Field("(objectClass=*)", description="Default search filter")
    search_scope: str = Field(
        "SUBTREE",
        description='Search scope: "BASE", LEVEL, or SUBTREE',
    )

    # Connection timeouts
    connect_timeout: int = Field(10, description="Connection timeout in seconds")
    receive_timeout: int = Field(30, description="Receive timeout in seconds")

    # Batch processing settings
    batch_size: int = Field(1000, description="Batch size for bulk operations")
    max_records: int | None = Field(
        None,
        description="Maximum records to process (None for unlimited)",
    )

    # Target-specific settings
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
    attribute_mapping: FlextTargetLdapTypes.Core.Headers = Field(
        default_factory=dict,
        description="Mapping from Singer field names to LDAP attributes",
    )
    object_classes: FlextTargetLdapTypes.Core.StringList = Field(
        default_factory=lambda: ["top"],
        description="Default object classes for new entries",
    )

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TARGET_LDAP_",
        case_sensitive=False,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        frozen=False,
    )

    @classmethod
    def get_global_instance(cls) -> Self:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-target-ldap")

    @classmethod
    def create_for_development(cls, **overrides: object) -> Self:
        """Create configuration for development environment."""
        dev_overrides: dict[str, object] = {
            "connect_timeout": 15,
            "receive_timeout": 45,
            "batch_size": 50,
            "create_missing_entries": True,
            "update_existing_entries": True,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-ldap", **dev_overrides
        )

    @classmethod
    def create_for_production(cls, **overrides: object) -> Self:
        """Create configuration for production environment."""
        prod_overrides: dict[str, object] = {
            "connect_timeout": 10,
            "receive_timeout": 30,
            "batch_size": 1000,
            "create_missing_entries": True,
            "update_existing_entries": True,
            "delete_removed_entries": False,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-ldap", **prod_overrides
        )

    @classmethod
    def create_for_testing(cls, **overrides: object) -> Self:
        """Create configuration for testing environment."""
        test_overrides: dict[str, object] = {
            "connect_timeout": 5,
            "receive_timeout": 15,
            "batch_size": 10,
            "create_missing_entries": True,
            "update_existing_entries": True,
            "delete_removed_entries": True,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-ldap", **test_overrides
        )

    # Use SettingsConfigDict for Settings configuration


class LDAPConnectionSettings(FlextModels):
    """LDAP connection settings model."""

    host: str = Field(..., description="LDAP server host")
    port: int = Field(389, description="LDAP server port")
    use_ssl: bool = Field(default=False, description="Use SSL connection")
    use_tls: bool = Field(default=False, description="Use TLS connection")
    bind_dn: str | None = Field(None, description="Bind DN")
    bind_password: str | None = Field(None, description="Bind password")
    base_dn: str = Field(..., description="Base DN")
    connect_timeout: int = Field(10, description="Connection timeout")
    receive_timeout: int = Field(30, description="Receive timeout")


class LDAPOperationSettings(FlextModels):
    """LDAP operation settings model."""

    batch_size: int = Field(1000, description="Batch size")
    max_records: int | None = Field(None, description="Maximum records")
    create_missing_entries: bool = Field(
        default=True,
        description="Create missing entries",
    )
    update_existing_entries: bool = Field(
        default=True,
        description="Update existing entries",
    )
    delete_removed_entries: bool = Field(
        default=False,
        description="Delete removed entries",
    )


# Function removed - not used anywhere and caused mypy errors due to complex field typing


def validate_ldap_config(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextResult[TargetLDAPConfig]:
    """Validate LDAP configuration."""
    try:

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

        # Extract connection parameters
        connection_params = {
            "server": config.get("host", "localhost"),
            "port": config.get("port", 389),
            "use_ssl": config.get("use_ssl", False),
            "bind_dn": config.get("bind_dn", ""),
            "bind_password": config.get("password", ""),
            "timeout": config.get("timeout", 30),
        }

        # Create connection config
        server = _to_str(connection_params["server"], "localhost")
        port = _to_int(connection_params["port"], 389)
        use_ssl = _to_bool(connection_params["use_ssl"], default=False)
        bind_dn = _to_str(connection_params["bind_dn"], "")
        bind_password = _to_str(connection_params["bind_password"], "")
        timeout = _to_int(connection_params["timeout"], 30)

        connection_config = FlextLdapModels.ConnectionConfig(
            server=server,
            port=port,
            use_ssl=use_ssl,
            bind_dn=bind_dn,
            bind_password=bind_password,
            timeout=timeout,
        )

        # Build TargetLDAPConfig explicitly
        raw_attr_map = config.get("attribute_mapping")
        if isinstance(raw_attr_map, dict):
            attribute_mapping: FlextTargetLdapTypes.Core.Headers = {
                str(k): str(v) for k, v in raw_attr_map.items()
            }
        else:
            attribute_mapping = {}

        raw_object_classes = config.get("object_classes")
        if isinstance(raw_object_classes, list):
            object_classes: FlextTargetLdapTypes.Core.StringList = [
                str(v) for v in raw_object_classes
            ]
        else:
            object_classes = ["top"]

        validated_config = TargetLDAPConfig(
            connection=connection_config,
            base_dn=_to_str(config.get("base_dn", "")),
            search_filter=_to_str(config.get("search_filter", "(objectClass=*)")),
            search_scope=_to_str(config.get("search_scope", "SUBTREE")),
            connect_timeout=_to_int(config.get("connect_timeout", 10), 10),
            receive_timeout=_to_int(config.get("receive_timeout", 30), 30),
            batch_size=_to_int(config.get("batch_size", 1000), 1000),
            max_records=(
                _to_int(config.get("max_records"), 0)
                if config.get("max_records") is not None
                else None
            ),
            create_missing_entries=_to_bool(
                config.get("create_missing_entries", True),
                default=True,
            ),
            update_existing_entries=_to_bool(
                config.get("update_existing_entries", True),
                default=True,
            ),
            delete_removed_entries=_to_bool(
                config.get("delete_removed_entries", False),
                default=False,
            ),
            attribute_mapping=attribute_mapping,
            object_classes=object_classes,
        )
        return FlextResult[TargetLDAPConfig].ok(validated_config)
    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult[TargetLDAPConfig].fail(
            f"Configuration validation failed: {e}",
        )
