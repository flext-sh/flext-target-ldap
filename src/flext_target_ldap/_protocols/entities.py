# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
src/flext_target_ldap/_protocols/entities
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

from flext_target_ldap import t

if TYPE_CHECKING:
    from flext_core import p


class FlextTargetLdapProtocolsEntities:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AttributeMapping(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def singer_field_name(self) -> t.NonEmptyStr:
            """Singer field name from source data."""
            ...

        @property
        def ldap_attribute_name(self) -> t.NonEmptyStr:
            """Target LDAP attribute name."""
            ...

        @property
        def is_required(self) -> bool:
            """Whether this attribute is required for LDAP entry."""
            ...

        @property
        def transformation_rule(self) -> str | None:
            """Optional transformation rule (e.g., 'lowercase', 'uppercase')."""
            ...

        @property
        def default_value(self) -> str | None:
            """Default value if source field is missing."""
            ...

    @runtime_checkable
    class Entry(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def distinguished_name(self) -> t.NonEmptyStr:
            """LDAP Distinguished Name (DN)."""
            ...

        @property
        def object_classes(self) -> MutableSequence[str]:
            """LDAP object classes for this entry."""
            ...

        @property
        def attributes(self) -> t.MutableStrSequenceMapping:
            """LDAP attributes with values."""
            ...

        @property
        def entry_type(self) -> str:
            """Type of LDAP entry (user, group, ou, etc.)."""
            ...

    @runtime_checkable
    class TransformationRule(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> t.NonEmptyStr:
            """Unique name identifying this transformation rule."""
            ...

        @property
        def pattern(self) -> t.NonEmptyStr:
            """Regex pattern to match in source data."""
            ...

        @property
        def replacement(self) -> str:
            """Replacement string applied when pattern matches."""
            ...

        @property
        def enabled(self) -> bool:
            """Whether this transformation rule is active."""
            ...


__all__: list[str] = [
    "FlextTargetLdapProtocolsEntities",
]
