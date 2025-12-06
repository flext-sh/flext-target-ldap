"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Self

from flext_core import FlextConfig, FlextConstants, FlextModels, FlextResult
from flext_ldap import FlextLdapModels
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_target_ldap.typings import FlextTargetLdapTypes


class FlextTargetLdapConfig(FlextConfig):
    """LDAP target configuration using consolidated patterns with FLEXT standards."""

    # Use real LDAP connection config from flext-ldap - no duplications
    connection: FlextLdapModels.ConnectionConfig = Field(
        ...,
        description="LDAP connection configuration",
    )

    # Target-specific settings (not duplicated)
    base_dn: str = Field(
        ...,
        description="Base DN for LDAP operations",
    )
    search_filter: str = Field("(objectClass=*)", description="Default search filter")
    search_scope: str = Field(
        "SUBTREE",
        description='Search scope: "BASE", LEVEL, or SUBTREE',
    )

    # Connection timeouts
    connect_timeout: int = Field(
        FlextConstants.Network.DEFAULT_TIMEOUT // 3,
        description="Connection timeout in seconds",
    )
    receive_timeout: int = Field(
        FlextConstants.Network.DEFAULT_TIMEOUT,
        description="Receive timeout in seconds",
    )

    # Batch processing settings
    batch_size: int = Field(
        FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
        description="Batch size for bulk operations",
    )
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
        use_enum_values=True,
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
            "connect_timeout": FlextConstants.Network.DEFAULT_TIMEOUT // 2,
            "receive_timeout": FlextConstants.Network.DEFAULT_TIMEOUT + 15,
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE // 20,
            "create_missing_entries": True,
            "update_existing_entries": True,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-ldap",
            **dev_overrides,
        )

    @classmethod
    def create_for_production(cls, **overrides: object) -> Self:
        """Create configuration for production environment."""
        prod_overrides: dict[str, object] = {
            "connect_timeout": FlextConstants.Network.DEFAULT_TIMEOUT // 3,
            "receive_timeout": FlextConstants.Network.DEFAULT_TIMEOUT,
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
            "create_missing_entries": True,
            "update_existing_entries": True,
            "delete_removed_entries": False,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-ldap",
            **prod_overrides,
        )

    @classmethod
    def create_for_testing(cls, **overrides: object) -> Self:
        """Create configuration for testing environment."""
        test_overrides: dict[str, object] = {
            "connect_timeout": FlextConstants.Network.DEFAULT_TIMEOUT // 6,
            "receive_timeout": FlextConstants.Network.DEFAULT_TIMEOUT // 2,
            "batch_size": FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
            // 100,
            "create_missing_entries": True,
            "update_existing_entries": True,
            "delete_removed_entries": True,
            **overrides,
        }
        return cls.get_or_create_shared_instance(
            project_name="flext-target-ldap",
            **test_overrides,
        )

    # Use SettingsConfigDict for Settings configuration


class LDAPConnectionSettings(FlextModels):
    """LDAP connection settings model."""

    host: str = Field(..., description="LDAP server host")
    port: int = Field(
        FlextConstants.Platform.LDAP_DEFAULT_PORT,
        description="LDAP server port",
    )
    use_ssl: bool = Field(default=False, description="Use SSL connection")
    use_tls: bool = Field(default=False, description="Use TLS connection")
    bind_dn: str | None = Field(None, description="Bind DN")
    bind_password: str | None = Field(None, description="Bind password")
    base_dn: str = Field(..., description="Base DN")
    connect_timeout: int = Field(
        FlextConstants.Network.DEFAULT_TIMEOUT // 3,
        description="Connection timeout",
    )
    receive_timeout: int = Field(
        FlextConstants.Network.DEFAULT_TIMEOUT,
        description="Receive timeout",
    )


class LDAPOperationSettings(FlextModels):
    """LDAP operation settings model."""

    batch_size: int = Field(
        FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
        description="Batch size",
    )
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


def _to_int(value: object, default: int) -> int:
    """Convert value to int."""
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
    """Convert value to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return default


def _to_str(value: object, default: str = "") -> str:
    """Convert value to string."""
    return str(value) if value is not None else default


def _build_connection_config(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextLdapModels.ConnectionConfig:
    """Build connection configuration from config dict."""
    server = _to_str(config.get("host", "localhost"), "localhost")
    port = _to_int(
        config.get("port", FlextConstants.Platform.LDAP_DEFAULT_PORT),
        FlextConstants.Platform.LDAP_DEFAULT_PORT,
    )
    use_ssl = _to_bool(config.get("use_ssl", False), default=False)
    bind_dn = _to_str(config.get("bind_dn", ""), "")
    bind_password = _to_str(config.get("password", ""), "")
    timeout = _to_int(
        config.get("timeout", FlextConstants.Network.DEFAULT_TIMEOUT),
        FlextConstants.Network.DEFAULT_TIMEOUT,
    )

    return FlextLdapModels.ConnectionConfig(
        server=server,
        port=port,
        use_ssl=use_ssl,
        bind_dn=bind_dn,
        bind_password=bind_password,
        timeout=timeout,
    )


def _extract_attribute_mapping(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextTargetLdapTypes.Core.Headers:
    """Extract attribute mapping from config."""
    raw_attr_map = config.get("attribute_mapping")
    if isinstance(raw_attr_map, dict):
        return {str(k): str(v) for k, v in raw_attr_map.items()}
    return {}


def _extract_object_classes(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextTargetLdapTypes.Core.StringList:
    """Extract object classes from config."""
    raw_object_classes = config.get("object_classes")
    if isinstance(raw_object_classes, list):
        return [str(v) for v in raw_object_classes]
    return ["top"]


def validate_ldap_config(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextResult[FlextTargetLdapConfig]:
    """Validate LDAP configuration."""
    try:
        connection_config = _build_connection_config(config)
        attribute_mapping = _extract_attribute_mapping(config)
        object_classes = _extract_object_classes(config)

        validated_config = FlextTargetLdapConfig(
            connection=connection_config,
            base_dn=_to_str(config.get("base_dn", "")),
            search_filter=_to_str(config.get("search_filter", "(objectClass=*)")),
            search_scope=_to_str(config.get("search_scope", "SUBTREE")),
            connect_timeout=_to_int(
                config.get(
                    "connect_timeout",
                    FlextConstants.Network.DEFAULT_TIMEOUT // 3,
                ),
                FlextConstants.Network.DEFAULT_TIMEOUT // 3,
            ),
            receive_timeout=_to_int(
                config.get("receive_timeout", FlextConstants.Network.DEFAULT_TIMEOUT),
                FlextConstants.Network.DEFAULT_TIMEOUT,
            ),
            batch_size=_to_int(
                config.get(
                    "batch_size",
                    FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
                ),
                FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE,
            ),
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
        return FlextResult[FlextTargetLdapConfig].ok(validated_config)
    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult[FlextTargetLdapConfig].fail(
            f"Configuration validation failed: {e}",
        )
