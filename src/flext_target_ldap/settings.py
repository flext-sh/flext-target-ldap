"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, ClassVar

from pydantic import Field, ValidationError
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings, r
from flext_target_ldap import c, m, t


@FlextSettings.auto_register("target-ldap")
class FlextTargetLdapSettings(FlextSettings):
    """LDAP target configuration with connection and operation settings."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix=c.ENV_PREFIX,
        extra=c.EXTRA_IGNORE,
    )

    connection: Annotated[
        m.Ldap.ConnectionConfig,
        Field(
            description="LDAP server connection configuration",
        ),
    ]
    base_dn: Annotated[
        t.NonEmptyStr,
        Field(
            description="Base Distinguished Name for LDAP operations",
        ),
    ]
    search_filter: Annotated[
        str,
        Field(
            default=c.Ldap.Filters.ALL_ENTRIES_FILTER,
            description="LDAP search filter expression",
        ),
    ]
    search_scope: Annotated[
        t.Ldap.Ldap3SearchScope,
        Field(
            default=c.Ldap.SearchDefaults.DEFAULT_SCOPE,
            description="LDAP search scope (BASE, ONELEVEL, or SUBTREE)",
        ),
    ]
    connect_timeout: Annotated[
        t.PositiveInt,
        Field(
            default=c.TargetLdap.CONNECT_TIMEOUT,
            description="Connection timeout in seconds",
        ),
    ]
    receive_timeout: Annotated[
        t.PositiveInt,
        Field(
            default=c.DEFAULT_TIMEOUT_SECONDS,
            description="Receive timeout in seconds for LDAP responses",
        ),
    ]
    batch_size: Annotated[
        t.BatchSize,
        Field(
            default=c.DEFAULT_SIZE,
            description="Maximum number of entries per batch operation",
        ),
    ]
    max_records: Annotated[
        int | None,
        Field(
            default=None,
            description="Maximum total records to process, or None for unlimited",
        ),
    ]
    create_missing_entries: Annotated[
        bool,
        Field(
            default=c.TargetLdap.CREATE_MISSING_ENTRIES,
            description="Whether to create LDAP entries that do not exist",
        ),
    ]
    update_existing_entries: Annotated[
        bool,
        Field(
            default=c.TargetLdap.UPDATE_EXISTING_ENTRIES,
            description="Whether to update LDAP entries that already exist",
        ),
    ]
    delete_removed_entries: Annotated[
        bool,
        Field(
            default=c.TargetLdap.DELETE_REMOVED_ENTRIES,
            description="Whether to delete LDAP entries removed from source",
        ),
    ]
    attribute_mapping: Annotated[
        t.StrMapping,
        Field(
            description="Mapping of source field names to LDAP attribute names",
            default_factory=dict,
        ),
    ]
    object_classes: Annotated[
        t.StrSequence,
        Field(
            description="LDAP object classes to assign to created entries",
            default_factory=lambda: list(c.TargetLdap.DEFAULT_OBJECT_CLASSES),
        ),
    ]

    @staticmethod
    def validate_ldap_config(
        config: Mapping[str, t.ContainerValue | t.ConfigMap],
    ) -> r[FlextTargetLdapSettings]:
        """Validate LDAP configuration."""
        try:
            validated_config = FlextTargetLdapSettings.model_validate({
                "connection": {
                    "host": config.get("host", c.LOCALHOST),
                    "port": config.get("port", c.Ldap.ConnectionDefaults.PORT),
                    "use_ssl": config.get("use_ssl", False),
                    "bind_dn": config.get("bind_dn", ""),
                    "bind_password": config.get("password", ""),
                    "timeout": config.get(
                        "timeout",
                        c.Ldap.ConnectionDefaults.TIMEOUT,
                    ),
                },
                "base_dn": config.get("base_dn", ""),
                "search_filter": config.get(
                    "search_filter",
                    c.Ldap.Filters.ALL_ENTRIES_FILTER,
                ),
                "search_scope": config.get(
                    "search_scope",
                    c.Ldap.SearchDefaults.DEFAULT_SCOPE,
                ),
                "connect_timeout": config.get(
                    "connect_timeout",
                    c.TargetLdap.CONNECT_TIMEOUT,
                ),
                "receive_timeout": config.get(
                    "receive_timeout",
                    c.DEFAULT_TIMEOUT_SECONDS,
                ),
                "batch_size": config.get("batch_size", c.DEFAULT_SIZE),
                "max_records": config.get("max_records"),
                "create_missing_entries": config.get(
                    "create_missing_entries",
                    c.TargetLdap.CREATE_MISSING_ENTRIES,
                ),
                "update_existing_entries": config.get(
                    "update_existing_entries",
                    c.TargetLdap.UPDATE_EXISTING_ENTRIES,
                ),
                "delete_removed_entries": config.get(
                    "delete_removed_entries",
                    c.TargetLdap.DELETE_REMOVED_ENTRIES,
                ),
                "attribute_mapping": config.get("attribute_mapping", {}),
                "object_classes": config.get(
                    "object_classes",
                    list(c.TargetLdap.DEFAULT_OBJECT_CLASSES),
                ),
            })
            return r[FlextTargetLdapSettings].ok(validated_config)
        except ValidationError as e:
            return r[FlextTargetLdapSettings].fail(
                f"Configuration validation failed: {e}",
            )
