"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextModels, r
from flext_ldap import FlextLdapModels
from pydantic import Field

from .constants import c
from .utilities import FlextTargetLdapUtilities


class FlextTargetLdapSettings(FlextModels.Entity):
    """LDAP target configuration with connection and operation settings."""

    connection: FlextLdapModels.Ldap.ConnectionConfig
    base_dn: str
    search_filter: str = "(objectClass=*)"
    search_scope: str = "SUBTREE"
    connect_timeout: int = c.Network.DEFAULT_TIMEOUT // 3
    receive_timeout: int = c.Network.DEFAULT_TIMEOUT
    batch_size: int = c.Performance.BatchProcessing.DEFAULT_SIZE
    max_records: int | None = None
    create_missing_entries: bool = True
    update_existing_entries: bool = True
    delete_removed_entries: bool = False
    attribute_mapping: dict[str, str] = Field(default_factory=dict)
    object_classes: list[str] = Field(default_factory=lambda: ["top"])


class LDAPConnectionSettings(FlextModels.Entity):
    """LDAP connection settings model."""

    host: str = Field(..., description="LDAP server host")
    port: int = Field(
        c.TargetLdap.Connection.DEFAULT_PORT, description="LDAP server port"
    )
    use_ssl: bool = Field(default=False, description="Use SSL connection")
    use_tls: bool = Field(default=False, description="Use TLS connection")
    bind_dn: str | None = Field(None, description="Bind DN")
    bind_password: str | None = Field(None, description="Bind password")
    base_dn: str = Field(..., description="Base DN")
    connect_timeout: int = Field(
        c.Network.DEFAULT_TIMEOUT // 3, description="Connection timeout"
    )
    receive_timeout: int = Field(
        c.Network.DEFAULT_TIMEOUT, description="Receive timeout"
    )


class LDAPOperationSettings(FlextModels.Entity):
    """LDAP operation settings model."""

    batch_size: int = Field(
        c.Performance.BatchProcessing.DEFAULT_SIZE, description="Batch size"
    )
    max_records: int | None = Field(None, description="Maximum records")
    create_missing_entries: bool = Field(
        default=True, description="Create missing entries"
    )
    update_existing_entries: bool = Field(
        default=True, description="Update existing entries"
    )
    delete_removed_entries: bool = Field(
        default=False, description="Delete removed entries"
    )


def validate_ldap_config(
    config: dict[str, object],
) -> r[FlextTargetLdapSettings]:
    """Validate LDAP configuration."""
    try:
        connection_config = (
            FlextTargetLdapUtilities.TypeConversion.build_connection_config(config)
        )
        attribute_mapping = (
            FlextTargetLdapUtilities.TypeConversion.extract_attribute_mapping(config)
        )
        object_classes = FlextTargetLdapUtilities.TypeConversion.extract_object_classes(
            config
        )
        validated_config = FlextTargetLdapSettings(
            connection=connection_config,
            base_dn=FlextTargetLdapUtilities.TypeConversion.to_str(
                config.get("base_dn", "")
            ),
            search_filter=FlextTargetLdapUtilities.TypeConversion.to_str(
                config.get("search_filter", "(objectClass=*)")
            ),
            search_scope=FlextTargetLdapUtilities.TypeConversion.to_str(
                config.get("search_scope", "SUBTREE")
            ),
            connect_timeout=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("connect_timeout", c.Network.DEFAULT_TIMEOUT // 3),
                c.Network.DEFAULT_TIMEOUT // 3,
            ),
            receive_timeout=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("receive_timeout", c.Network.DEFAULT_TIMEOUT),
                c.Network.DEFAULT_TIMEOUT,
            ),
            batch_size=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("batch_size", c.Performance.BatchProcessing.DEFAULT_SIZE),
                c.Performance.BatchProcessing.DEFAULT_SIZE,
            ),
            max_records=FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("max_records"), 0
            ),
            create_missing_entries=FlextTargetLdapUtilities.TypeConversion.to_bool(
                config.get("create_missing_entries", True), default=True
            ),
            update_existing_entries=FlextTargetLdapUtilities.TypeConversion.to_bool(
                config.get("update_existing_entries", True), default=True
            ),
            delete_removed_entries=FlextTargetLdapUtilities.TypeConversion.to_bool(
                config.get("delete_removed_entries", False), default=False
            ),
            attribute_mapping=dict(attribute_mapping),
            object_classes=object_classes,
        )
        return r[FlextTargetLdapSettings].ok(validated_config)
    except (RuntimeError, ValueError, TypeError) as e:
        return r[FlextTargetLdapSettings].fail(f"Configuration validation failed: {e}")
