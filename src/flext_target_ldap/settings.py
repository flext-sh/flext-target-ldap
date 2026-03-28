"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import r
from pydantic import Field, ValidationError

from flext_target_ldap import c, m, t


class FlextTargetLdapSettings(m.Entity):
    """LDAP target configuration with connection and operation settings."""

    connection: m.Ldap.ConnectionConfig
    base_dn: t.NonEmptyStr
    search_filter: str = "(objectClass=*)"
    search_scope: str = "SUBTREE"
    connect_timeout: t.PositiveInt = c.DEFAULT_TIMEOUT_SECONDS // 3
    receive_timeout: t.PositiveInt = c.DEFAULT_TIMEOUT_SECONDS
    batch_size: t.BatchSize = c.DEFAULT_SIZE
    max_records: int | None = None
    create_missing_entries: bool = True
    update_existing_entries: bool = True
    delete_removed_entries: bool = False
    attribute_mapping: t.StrMapping = Field(default_factory=dict)
    object_classes: t.StrSequence = Field(default_factory=lambda: ["top"])

    @staticmethod
    def validate_ldap_config(
        config: Mapping[str, t.ContainerValue | t.ConfigMap],
    ) -> r[FlextTargetLdapSettings]:
        """Validate LDAP configuration."""
        try:
            validated_config = FlextTargetLdapSettings.model_validate({
                "connection": {
                    "host": config.get("host", "localhost"),
                    "port": config.get("port", c.Ldap.ConnectionDefaults.PORT),
                    "use_ssl": config.get("use_ssl", False),
                    "bind_dn": config.get("bind_dn", ""),
                    "bind_password": config.get("password", ""),
                    "timeout": config.get("timeout", c.DEFAULT_TIMEOUT_SECONDS),
                },
                "base_dn": config.get("base_dn", ""),
                "search_filter": config.get("search_filter", "(objectClass=*)"),
                "search_scope": config.get("search_scope", "SUBTREE"),
                "connect_timeout": config.get(
                    "connect_timeout", c.DEFAULT_TIMEOUT_SECONDS // 3
                ),
                "receive_timeout": config.get(
                    "receive_timeout", c.DEFAULT_TIMEOUT_SECONDS
                ),
                "batch_size": config.get("batch_size", c.DEFAULT_SIZE),
                "max_records": config.get("max_records"),
                "create_missing_entries": config.get("create_missing_entries", True),
                "update_existing_entries": config.get("update_existing_entries", True),
                "delete_removed_entries": config.get("delete_removed_entries", False),
                "attribute_mapping": config.get("attribute_mapping", {}),
                "object_classes": config.get("object_classes", ["top"]),
            })
            return r[FlextTargetLdapSettings].ok(validated_config)
        except ValidationError as e:
            return r[FlextTargetLdapSettings].fail(
                f"Configuration validation failed: {e}",
            )


def validate_ldap_config(
    config: Mapping[str, t.ContainerValue | t.ConfigMap],
) -> r[FlextTargetLdapSettings]:
    """Validate LDAP configuration - delegates to FlextTargetLdapSettings.validate_ldap_config."""
    return FlextTargetLdapSettings.validate_ldap_config(config)
