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

from typing import TYPE_CHECKING, Annotated, ClassVar

from flext_meltano import FlextMeltanoSettings, m


class FlextTargetLdapSettings(FlextMeltanoSettings):
    """LDAP target settings; all project fields under ``settings.TargetLdap.*``."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_TARGET_LDAP_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _TargetLdap(m.BaseModel):
        """Namespaced LDAP target settings (connection + operation)."""

        host: Annotated[str, m.Field(description="LDAP host")] = "localhost"
        port: Annotated[int, m.Field(description="LDAP port")] = 389
        use_ssl: Annotated[bool, m.Field(description="Use SSL")] = False
        use_tls: Annotated[bool, m.Field(description="Use TLS")] = False
        bind_dn: Annotated[str, m.Field(description="Bind DN")] = ""
        bind_password: Annotated[str, m.Field(description="Bind password")] = ""
        timeout: Annotated[int, m.Field(description="Connection timeout (s)")] = 30
        auto_bind: Annotated[bool, m.Field(description="Auto bind")] = True
        auto_range: Annotated[bool, m.Field(description="Auto range")] = True
        base_dn: Annotated[str, m.Field(description="Base DN")] = ""
        search_filter: Annotated[str, m.Field(description="LDAP search filter")] = (
            "(objectClass=*)"
        )
        search_scope: Annotated[
            str,
            m.Field(
                description="Search scope (BASE/ONELEVEL/SUBTREE)",
            ),
        ] = "SUBTREE"
        connect_timeout: Annotated[int, m.Field(description="Connect timeout (s)")] = 30
        receive_timeout: Annotated[int, m.Field(description="Receive timeout (s)")] = 30
        batch_size: Annotated[int, m.Field(description="Entries per batch")] = 1000
        max_records: Annotated[
            int | None,
            m.Field(
                description="Max total records, or None for unlimited",
            ),
        ] = None
        create_missing_entries: Annotated[
            bool, m.Field(description="Create LDAP entries that do not exist")
        ] = True
        update_existing_entries: Annotated[
            bool, m.Field(description="Update LDAP entries that already exist")
        ] = True
        delete_removed_entries: Annotated[
            bool,
            m.Field(
                description="Delete LDAP entries removed from source",
            ),
        ] = False
        attribute_mapping: Annotated[
            dict[str, str],
            m.Field(
                description="Source field -> LDAP attribute map",
            ),
        ] = m.Field(default_factory=dict[str, str])
        object_classes: Annotated[
            list[str], m.Field(description="LDAP object classes")
        ] = m.Field(default_factory=lambda: ["top"])

    if TYPE_CHECKING:
        TargetLdap: _TargetLdap
    else:
        TargetLdap: _TargetLdap = m.Field(
            default_factory=_TargetLdap,
            description="Namespaced LDAP target settings.",
        )


settings: FlextTargetLdapSettings = FlextTargetLdapSettings.fetch_global()
"""Pre-instantiated settings singleton — ``from flext_target_ldap import settings``."""

__all__: list[str] = ["FlextTargetLdapSettings", "settings"]
