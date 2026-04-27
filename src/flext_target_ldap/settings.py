"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from types import MappingProxyType
from typing import Annotated, ClassVar, Self

from flext_core import FlextSettings
from flext_target_ldap import c, m, t, u


@FlextSettings.auto_register("target-ldap")
class FlextTargetLdapSettings(FlextSettings):
    """LDAP target configuration with connection and operation settings."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix=c.TargetLdap.ENV_PREFIX, extra="ignore"
    )

    @u.model_validator(mode="before")
    @classmethod
    def normalize_flat_settings(
        cls,
        data: Mapping[str, t.JsonPayload | None] | Self,
    ) -> Mapping[str, t.JsonPayload | None] | Self:
        """Normalize flat Singer settings into the canonical nested shape."""
        if isinstance(data, cls) or not isinstance(data, Mapping):
            return data
        if "connection" in data:
            return data

        normalized: dict[str, t.JsonPayload | None] = dict(data)
        bind_password = normalized.get("bind_password", normalized.get("password"))
        search_scope = normalized.get("search_scope")
        if isinstance(search_scope, str):
            normalized["search_scope"] = search_scope.upper()
        connection_config = m.Ldap.ConnectionConfig.model_validate({
            "host": normalized.get("host", c.LOCALHOST),
            "port": normalized.get("port", c.Ldap.PORT),
            "use_ssl": normalized.get(
                "use_ssl",
                c.Ldap.DEFAULT_USE_SSL,
            ),
            "use_tls": normalized.get(
                "use_tls",
                c.Ldap.DEFAULT_USE_TLS,
            ),
            "bind_dn": normalized.get(
                "bind_dn",
                c.Ldap.DEFAULT_BIND_DN,
            ),
            "bind_password": bind_password,
            "timeout": normalized.get(
                "timeout",
                c.Ldap.TIMEOUT,
            ),
            "auto_bind": normalized.get(
                "auto_bind",
                c.Ldap.AUTO_BIND,
            ),
            "auto_range": normalized.get(
                "auto_range",
                c.Ldap.AUTO_RANGE,
            ),
        })
        for consumed_key in (
            "host",
            "port",
            "use_ssl",
            "use_tls",
            "bind_dn",
            "bind_password",
            "password",
            "timeout",
            "auto_bind",
            "auto_range",
        ):
            normalized.pop(consumed_key, None)
        normalized["connection"] = connection_config
        return normalized

    connection: Annotated[
        m.Ldap.ConnectionConfig,
        u.Field(
            description="LDAP server connection configuration",
        ),
    ]
    base_dn: Annotated[
        t.NonEmptyStr,
        u.Field(
            description="Base Distinguished Name for LDAP operations",
        ),
    ]
    search_filter: Annotated[
        str,
        u.Field(
            default=c.Ldap.ALL_ENTRIES_FILTER,
            description="LDAP search filter expression",
        ),
    ]
    search_scope: Annotated[
        t.Ldap.Ldap3SearchScope,
        u.Field(
            default=c.Ldap.DEFAULT_SCOPE,
            description="LDAP search scope (BASE, ONELEVEL, or SUBTREE)",
        ),
    ]
    connect_timeout: Annotated[
        t.PositiveInt,
        u.Field(
            default=c.Ldap.TIMEOUT,
            description="Connection timeout in seconds",
        ),
    ]
    receive_timeout: Annotated[
        t.PositiveInt,
        u.Field(
            default=c.DEFAULT_TIMEOUT_SECONDS,
            description="Receive timeout in seconds for LDAP responses",
        ),
    ]
    batch_size: Annotated[
        t.BatchSize,
        u.Field(
            default=c.DEFAULT_SIZE,
            description="Maximum number of entries per batch operation",
        ),
    ]
    max_records: Annotated[
        int | None,
        u.Field(
            default=None,
            description="Maximum total records to process, or None for unlimited",
        ),
    ]
    create_missing_entries: Annotated[
        bool,
        u.Field(
            default=c.TargetLdap.CREATE_MISSING_ENTRIES,
            description="Whether to create LDAP entries that do not exist",
        ),
    ]
    update_existing_entries: Annotated[
        bool,
        u.Field(
            default=c.TargetLdap.UPDATE_EXISTING_ENTRIES,
            description="Whether to update LDAP entries that already exist",
        ),
    ]
    delete_removed_entries: Annotated[
        bool,
        u.Field(
            default=c.TargetLdap.DELETE_REMOVED_ENTRIES,
            description="Whether to delete LDAP entries removed from source",
        ),
    ]
    attribute_mapping: Annotated[
        t.StrMapping,
        u.Field(
            description="Mapping of source field names to LDAP attribute names",
            default_factory=lambda: MappingProxyType({}),
        ),
    ]
    object_classes: Annotated[
        t.StrSequence,
        u.Field(
            description="LDAP object classes to assign to created entries",
            default_factory=lambda: list(c.TargetLdap.DEFAULT_OBJECT_CLASSES),
        ),
    ]
