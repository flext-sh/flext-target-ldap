"""Validated TargetLdap config models for flext-target-ldap.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import m, t


class FlextModelsTargetLdapConfig:
    """Field-only declarations for the TargetLdap config singleton."""

    class ConfigRoot(m.FrozenModel):
        """Validated root loaded by the private config composition."""

        model_config = m.ConfigDict(frozen=True, extra="ignore")

        class ConfigNamespace(m.BaseModel):
            """Open namespace loaded from ``config/target-ldap.yaml``."""

            model_config = m.ConfigDict(frozen=True, extra="allow")

        TargetLdap: ConfigNamespace = m.Field(
            description="Open namespace exposing ``config/*.yaml`` under TargetLdap.",
        )

    class EntryProfile(m.FrozenModel):
        """How one Singer stream's records become LDAP entries."""

        label: str = m.Field(description="Entry kind named in messages")
        identity_label: str = m.Field(
            description="Name of the missing identity in failure messages",
        )
        rdn_attribute: str = m.Field(description="RDN attribute of a derived DN")
        identity_fields: t.StrSequence = m.Field(
            description="Record fields supplying the RDN value, in precedence order",
        )
        default_object_classes: t.StrSequence = m.Field(
            description="Object classes used when neither record nor settings set any",
        )
        required_object_classes: t.StrSequence = m.Field(
            description="Object classes every entry of the stream carries",
        )
        object_classes_setting: str = m.Field(
            description="Settings key holding the configured object classes",
        )
        field_mapping: t.StrMapping = m.Field(
            description="Record field to LDAP attribute mapping",
        )
        include_unmapped_fields: bool = m.Field(
            description="Write every non-control record field as an attribute",
        )

    class Rules(m.FrozenModel):
        """TargetLdap business rules from ``config/target-ldap.yaml``."""

        model_config = m.ConfigDict(frozen=True, extra="ignore")

        default_entry_profile: FlextModelsTargetLdapConfig.EntryProfile = m.Field(
            description="Entry profile of streams without a declared profile",
        )
        entry_profiles: t.MappingKV[str, FlextModelsTargetLdapConfig.EntryProfile] = (
            m.Field(
                description="Entry profiles keyed by Singer stream name",
            )
        )


__all__: list[str] = ["FlextModelsTargetLdapConfig"]
