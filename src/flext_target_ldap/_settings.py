"""Settings for flext-target-ldap — namespaced under ``settings.TargetLdap``.

Layer-0: imports only stdlib + pydantic + ``FlextSettings``. The universal
runtime fields (``debug``/``trace``/``log_level``/``timezone``/``async_logging``)
come from ``FlextSettings`` by MRO and are NOT redeclared here. Every project
field lives inside the ``TargetLdap`` namespace group with simple scalar types
so each is settable via ``.env`` / env vars / params
(``FLEXT_TARGET_LDAP_TARGETLDAP__HOST`` …).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings


class FlextTargetLdapSettings(FlextSettings):
    """LDAP target settings; all project fields under ``settings.TargetLdap.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_TARGET_LDAP_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _TargetLdap(BaseModel):
        """Namespaced LDAP target settings (connection + operation)."""

        host: Annotated[str, Field(default="localhost", description="LDAP host")]
        port: Annotated[int, Field(default=389, description="LDAP port")]
        use_ssl: Annotated[bool, Field(default=False, description="Use SSL")]
        use_tls: Annotated[bool, Field(default=False, description="Use TLS")]
        bind_dn: Annotated[str, Field(default="", description="Bind DN")]
        bind_password: Annotated[str, Field(default="", description="Bind password")]
        timeout: Annotated[int, Field(default=30, description="Connection timeout (s)")]
        auto_bind: Annotated[bool, Field(default=True, description="Auto bind")]
        auto_range: Annotated[bool, Field(default=True, description="Auto range")]
        base_dn: Annotated[str, Field(default="", description="Base DN")]
        search_filter: Annotated[
            str,
            Field(default="(objectClass=*)", description="LDAP search filter"),
        ]
        search_scope: Annotated[
            str,
            Field(default="SUBTREE", description="Search scope (BASE/ONELEVEL/SUBTREE)"),
        ]
        connect_timeout: Annotated[int, Field(default=30, description="Connect timeout (s)")]
        receive_timeout: Annotated[int, Field(default=30, description="Receive timeout (s)")]
        batch_size: Annotated[int, Field(default=1000, description="Entries per batch")]
        max_records: Annotated[
            int | None,
            Field(default=None, description="Max total records, or None for unlimited"),
        ]
        create_missing_entries: Annotated[
            bool,
            Field(default=True, description="Create LDAP entries that do not exist"),
        ]
        update_existing_entries: Annotated[
            bool,
            Field(default=True, description="Update LDAP entries that already exist"),
        ]
        delete_removed_entries: Annotated[
            bool,
            Field(default=False, description="Delete LDAP entries removed from source"),
        ]
        attribute_mapping: Annotated[
            dict[str, str],
            Field(default_factory=dict, description="Source field -> LDAP attribute map"),
        ]
        object_classes: Annotated[
            list[str],
            Field(default_factory=lambda: ["top"], description="LDAP object classes"),
        ]

    if TYPE_CHECKING:
        TargetLdap: _TargetLdap
    else:
        TargetLdap: _TargetLdap = Field(
            default_factory=_TargetLdap,
            description="Namespaced LDAP target settings.",
        )


settings: FlextTargetLdapSettings = FlextTargetLdapSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_target_ldap import settings``."""

__all__: list[str] = ["FlextTargetLdapSettings", "settings"]
