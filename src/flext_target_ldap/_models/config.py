"""flext-target-ldap config models — typed business-rule shapes.

Frozen Pydantic shapes for the ``config/target_ldap.yaml`` business-rule SSOT.
The ``_config.py`` facade validates the model-less YAML slice into these
classes and exposes the ready objects under ``config.TargetLdap``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FlextTargetLdapConfigModels:
    """Namespace of typed flext-target-ldap config models."""

    class Connection(BaseModel):
        """LDAP connection defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        host: str = Field(description="Default LDAP host.")
        port: int = Field(
            ge=1,
            le=65535,
            description="Default LDAP port.",
        )
        use_ssl: bool = Field(description="Whether to use SSL by default.")
        use_tls: bool = Field(description="Whether to use TLS by default.")
        bind_dn: str = Field(description="Default bind DN.")
        bind_password: str = Field(description="Default bind password.")
        timeout: int = Field(
            ge=1,
            description="Default connection timeout in seconds.",
        )
        connect_timeout: int = Field(
            ge=1,
            description="Default connect timeout in seconds.",
        )
        receive_timeout: int = Field(
            ge=1,
            description="Default receive timeout in seconds.",
        )
        auto_bind: bool = Field(description="Whether to auto-bind by default.")
        auto_range: bool = Field(description="Whether to auto-range by default.")

    class Search(BaseModel):
        """LDAP search defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        base_dn: str = Field(description="Default base DN for searches.")
        filter: str = Field(description="Default LDAP search filter.")
        scope: str = Field(description="Default search scope (BASE/ONELEVEL/SUBTREE).")

    class Operations(BaseModel):
        """LDAP target operation defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        batch_size: int = Field(
            ge=1,
            description="Entries per batch.",
        )
        create_missing_entries: bool = Field(
            description="Whether to create LDAP entries that do not exist.",
        )
        update_existing_entries: bool = Field(
            description="Whether to update LDAP entries that already exist.",
        )
        delete_removed_entries: bool = Field(
            description="Whether to delete LDAP entries removed from source.",
        )

    class ObjectClasses(BaseModel):
        """LDAP object-class defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default: tuple[str, ...] = Field(
            description="Default object classes for new LDAP entries.",
        )

    class TargetLdap(BaseModel):
        """Root LDAP target business-rule namespace."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        connection: FlextTargetLdapConfigModels.Connection = Field(
            description="LDAP connection defaults.",
        )
        search: FlextTargetLdapConfigModels.Search = Field(
            description="LDAP search defaults.",
        )
        operations: FlextTargetLdapConfigModels.Operations = Field(
            description="LDAP target operation defaults.",
        )
        object_classes: FlextTargetLdapConfigModels.ObjectClasses = Field(
            description="LDAP object-class defaults.",
        )

    class Root(BaseModel):
        """Root flext-target-ldap config validated from ``config/*.yaml``."""

        model_config = ConfigDict(frozen=True, extra="ignore")

        TargetLdap: FlextTargetLdapConfigModels.TargetLdap = Field(
            description="LDAP target business-rule config namespace.",
        )


__all__: list[str] = ["FlextTargetLdapConfigModels"]
