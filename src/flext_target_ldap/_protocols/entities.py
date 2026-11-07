# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
src/flext_target_ldap/_protocols/entities
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_core import p

    from flext_target_ldap import t


class FlextTargetLdapProtocolsEntities:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class AttributeMapping(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        version: t.NonNegativeInt
        unique_id: t.NonEmptyStr

        @property
        def created_at(self) -> datetime:
            """Creation timestamp (configured timezone)."""
            ...

        updated_at: datetime | None

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        singer_field_name: t.NonEmptyStr
        ldap_attribute_name: t.NonEmptyStr
        is_required: bool
        transformation_rule: str | None
        default_value: str | None

    @runtime_checkable
    class Entry(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        version: t.NonNegativeInt
        unique_id: t.NonEmptyStr

        @property
        def created_at(self) -> datetime:
            """Creation timestamp (configured timezone)."""
            ...

        updated_at: datetime | None

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        distinguished_name: t.NonEmptyStr
        object_classes: MutableSequence[str]
        attributes: t.MutableStrSequenceMapping
        entry_type: str

    @runtime_checkable
    class TransformationRule(FlextMeltanoProtocols.BaseModel, Protocol):
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
