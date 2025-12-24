"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Self

from flext_ldap import FlextLdapModels
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext import FlextModels, FlextResult, FlextSettings
from flext_target_ldap.constants import c
from flext_target_ldap.typings import t
from flext_target_ldap.utilities import FlextTargetLdapUtilities


class FlextTargetLdapSettings(FlextSettings):
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
        c.Network.DEFAULT_TIMEOUT // 3,
        description="Connection timeout in seconds",
    )
    receive_timeout: int = Field(
        c.Network.DEFAULT_TIMEOUT,
        description="Receive timeout in seconds",
    )

    # Batch processing settings
    batch_size: int = Field(
        c.Performance.BatchProcessing.DEFAULT_SIZE,
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
    attribute_mapping: t.Core.Headers = Field(
        default_factory=dict,
        description="Mapping from Singer field names to LDAP attributes",
    )
    object_classes: t.Core.StringList = Field(
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
        """Get the global singleton instance using enhanced FlextSettings pattern."""
        return cls.get_or_create_shared_instance(project_name="flext-target-ldap")

    @classmethod
    def create_for_development(cls, **overrides: object) -> Self:
        """Create configuration for development environment."""
        dev_overrides: dict[str, object] = {
            "connect_timeout": c.Network.DEFAULT_TIMEOUT // 2,
            "receive_timeout": c.Network.DEFAULT_TIMEOUT + 15,
            "batch_size": c.Performance.BatchProcessing.DEFAULT_SIZE // 20,
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
            "connect_timeout": c.Network.DEFAULT_TIMEOUT // 3,
            "receive_timeout": c.Network.DEFAULT_TIMEOUT,
            "batch_size": c.Performance.BatchProcessing.DEFAULT_SIZE,
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
            "connect_timeout": c.Network.DEFAULT_TIMEOUT // 6,
            "receive_timeout": c.Network.DEFAULT_TIMEOUT // 2,
            "batch_size": c.Performance.BatchProcessing.DEFAULT_SIZE // 100,
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
        c.TargetLdap.Connection.DEFAULT_PORT,
        description="LDAP server port",
    )
    use_ssl: bool = Field(default=False, description="Use SSL connection")
    use_tls: bool = Field(default=False, description="Use TLS connection")
    bind_dn: str | None = Field(None, description="Bind DN")
    bind_password: str | None = Field(None, description="Bind password")
    base_dn: str = Field(..., description="Base DN")
    connect_timeout: int = Field(
        c.Network.DEFAULT_TIMEOUT // 3,
        description="Connection timeout",
    )
    receive_timeout: int = Field(
        c.Network.DEFAULT_TIMEOUT,
        description="Receive timeout",
    )


class LDAPOperationSettings(FlextModels):
    """LDAP operation settings model."""

    batch_size: int = Field(
        c.Performance.BatchProcessing.DEFAULT_SIZE,
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

    """Convert value to string."""
    return str(value) if value is not None else default


def validate_ldap_config(
    config: t.Core.Dict,
) -> FlextResult[FlextTargetLdapSettings]:
    """Validate LDAP configuration."""
    try:
        connection_config = FlextTargetLdapUtilities.TypeConversion.build_connection_config(config)
        attribute_mapping = FlextTargetLdapUtilities.TypeConversion.extract_attribute_mapping(config)
        object_classes = FlextTargetLdapUtilities.TypeConversion.extract_object_classes(config)

        validated_config = FlextTargetLdapSettings(
            connection=connection_config,
            base_dn=FlextTargetLdapUtilities.TypeConversion.to_str(config.get("base_dn", "")),
            search_filter=FlextTargetLdapUtilities.TypeConversion.to_str(config.get("search_filter", "(objectClass=*)")),
            search_scope=FlextTargetLdapUtilities.TypeConversion.to_str(config.get("search_scope", "SUBTREE")),
            connect_timeout=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get(
                    "connect_timeout",
                    c.Network.DEFAULT_TIMEOUT // 3,
                ),
                c.Network.DEFAULT_TIMEOUT // 3,
            ),
            receive_timeout=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("receive_timeout", c.Network.DEFAULT_TIMEOUT),
                c.Network.DEFAULT_TIMEOUT,
            ),
            batch_size=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get(
                    "batch_size",
                    c.Performance.DEFAULT_BATCH_SIZE,
                ),
                c.Performance.DEFAULT_BATCH_SIZE,
            ),
            max_records=FlextTargetLdapUtilities.TypeConversion.to_int(config.get("max_records"), 0),
            create_missing_entries=FlextTargetLdapUtilities.TypeConversion.to_bool(
                config.get("create_missing_entries", True),
                default=True,
            ),
            update_existing_entries=FlextTargetLdapUtilities.TypeConversion.to_bool(
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
        return FlextResult[FlextTargetLdapSettings].ok(validated_config)
    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult[FlextTargetLdapSettings].fail(
            f"Configuration validation failed: {e}",
        )
