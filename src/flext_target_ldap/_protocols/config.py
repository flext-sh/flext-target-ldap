# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
src/flext_target_ldap/_protocols/config
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols


class FlextTargetLdapProtocolsConfig:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ConfigRoot(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def TargetLdap(
            self,
        ) -> FlextTargetLdapProtocolsConfig.ConfigRootConfigNamespace:
            """Open namespace exposing ``config/*.yaml`` under TargetLdap."""
            ...

    @runtime_checkable
    class ConfigRootConfigNamespace(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class EntryProfile(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def label(self) -> str:
            """Entry kind named in messages."""
            ...

        @property
        def identity_label(self) -> str:
            """Name of the missing identity in failure messages."""
            ...

        @property
        def rdn_attribute(self) -> str:
            """RDN attribute of a derived DN."""
            ...

        @property
        def identity_fields(self) -> Sequence[str]:
            """Record fields supplying the RDN value, in precedence order."""
            ...

        @property
        def default_object_classes(self) -> Sequence[str]:
            """Object classes used when neither record nor settings set any."""
            ...

        @property
        def required_object_classes(self) -> Sequence[str]:
            """Object classes every entry of the stream carries."""
            ...

        @property
        def object_classes_setting(self) -> str:
            """Settings key holding the configured object classes."""
            ...

        @property
        def field_mapping(self) -> Mapping[str, str]:
            """Record field to LDAP attribute mapping."""
            ...

        @property
        def include_unmapped_fields(self) -> bool:
            """Write every non-control record field as an attribute."""
            ...

    @runtime_checkable
    class Rules(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_entry_profile(self) -> FlextTargetLdapProtocolsConfig.EntryProfile:
            """Entry profile of streams without a declared profile."""
            ...

        @property
        def entry_profiles(
            self,
        ) -> Mapping[str, FlextTargetLdapProtocolsConfig.EntryProfile]:
            """Entry profiles keyed by Singer stream name."""
            ...


__all__: list[str] = [
    "FlextTargetLdapProtocolsConfig",
]
