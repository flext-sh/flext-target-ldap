"""Target LDAP protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_ldap import FlextLdapProtocols

from flext_target_ldap import t

if TYPE_CHECKING:
    from flext_target_ldap import target_client as target_client_module
    from flext_target_ldap.models import m as _m


class FlextTargetLdapProtocols(FlextLdapProtocols):
    """Singer Target LDAP protocols extending LDAP and Meltano protocols.

    Extends both FlextLdapProtocols and FlextMeltanoProtocols via multiple inheritance
    to inherit all LDAP protocols, Meltano protocols, and foundation protocols.

    Architecture:
    - EXTENDS: FlextLdapProtocols (inherits .Ldap.* and .Ldif.* protocols)
    - EXTENDS: FlextMeltanoProtocols (inherits .Meltano.* protocols)
    - ADDS: Target LDAP-specific protocols in Target.Ldap namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_target_ldap.protocols import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # LDAP protocols (inherited)
    entry: p.Ldap.Entry

    # Meltano protocols (inherited)
    target: p.Meltano.Target

    # Target LDAP-specific protocols
    target_protocol: p.Target.Ldap.Target
    """

    class TargetLdap:
        """Singer Target domain protocols."""

        class LDAPConnection(Protocol):
            """Protocol for LDAP connection objects (ldap3.Connection or compatible)."""

            bound: bool
            entries: MutableSequence[Mapping[str, t.ContainerValue]]

            def add(
                self,
                dn: str,
                object_classes: t.StrSequence,
                attributes: Mapping[str, t.ContainerValue],
            ) -> bool:
                """Add LDAP entry."""
                ...

            def bind(self) -> bool:
                """Bind to LDAP server."""
                ...

            def delete(self, dn: str) -> bool:
                """Delete LDAP entry."""
                ...

            def modify(self, dn: str, changes: Mapping[str, t.ContainerValue]) -> bool:
                """Modify LDAP entry."""
                ...

            def search(
                self,
                base_dn: str,
                search_filter: str,
                attributes: t.StrSequence | None = None,
            ) -> bool:
                """Search LDAP entries."""
                ...

            def unbind(self) -> None:
                """Unbind from LDAP server."""
                ...

        class LdapProcessingState(Protocol):
            """Protocol for LDAP processing state tracking."""

            processed_count: int
            success_count: int
            error_count: int
            errors: MutableSequence[str]

        class LdapApi(Protocol):
            """Protocol for LDAP API operations."""

            def add(self, dn: str, record: Mapping[str, t.ContainerValue]) -> None:
                """Add LDAP entry."""
                ...

            def delete(self, dn: str) -> None:
                """Delete LDAP entry."""
                ...

            def modify(self, dn: str, record: Mapping[str, t.ContainerValue]) -> None:
                """Modify LDAP entry."""
                ...

        class LdapTargetService(Protocol):
            """Protocol for LDAP target creation and record loading."""

            def create_target(
                self,
                config: Mapping[str, t.ContainerValue],
            ) -> FlextLdapProtocols.Result[target_client_module.FlextTargetLdap]:
                """Create an LDAP target from config."""
                ...

            def load_records(
                self,
                records: Sequence[Mapping[str, t.ContainerValue]],
                config: Mapping[str, t.ContainerValue],
                stream_type: str = "users",
            ) -> FlextLdapProtocols.Result[int]:
                """Load records into the LDAP target."""
                ...

        class LdapTransformationServiceProtocol(Protocol):
            """Protocol for transforming and validating LDAP entries."""

            def transform_record(
                self,
                record: Mapping[str, t.ContainerValue],
                mappings: Sequence[_m.TargetLdap.AttributeMapping],
                object_classes: t.StrSequence,
                base_dn: str,
            ) -> FlextLdapProtocols.Result[_m.TargetLdap.TransformationResult]:
                """Transform a record for LDAP storage."""
                ...

            def validate_entry(
                self,
                entry: _m.TargetLdap.Entry,
            ) -> FlextLdapProtocols.Result[bool]:
                """Validate an LDAP entry against business rules."""
                ...

        class Ldap:
            """Singer Target LDAP domain protocols for LDAP directory loading."""

            @runtime_checkable
            class Target(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for LDAP target operations."""

                def process_record(
                    self,
                    record: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[bool]:
                    """Process a single record."""
                    ...

            @runtime_checkable
            class Transformation(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for Singer to LDAP transformation."""

                def transform_to_ldap(
                    self,
                    record: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[t.ContainerValueMapping]:
                    """Transform record to LDAP format."""
                    ...

            @runtime_checkable
            class Orchestration(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for LDAP loading orchestration."""

                def orchestrate_load(
                    self,
                    records: Sequence[Mapping[str, t.ContainerValue]],
                ) -> FlextLdapProtocols.Result[bool]:
                    """Orchestrate loading of records."""
                    ...

            @runtime_checkable
            class Connection(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for LDAP connection management."""

                def connect(
                    self,
                    config: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[t.ContainerValueMapping]:
                    """Connect to LDAP server."""
                    ...

            @runtime_checkable
            class Singer(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for Singer message handling."""

                def process_singer_message(
                    self,
                    message: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[bool]:
                    """Process a Singer protocol message."""
                    ...

            @runtime_checkable
            class Performance(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for LDAP loading performance."""

                def optimize_batch(
                    self,
                    batch_size: int,
                ) -> FlextLdapProtocols.Result[int]:
                    """Optimize batch size for LDAP loading."""
                    ...

            @runtime_checkable
            class Security(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for LDAP security operations."""

                def validate_credentials(
                    self,
                    config: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[bool]:
                    """Validate LDAP credentials."""
                    ...

            @runtime_checkable
            class Monitoring(
                FlextLdapProtocols.Service[t.ContainerValueMapping],
                Protocol,
            ):
                """Protocol for LDAP loading monitoring."""

                def track_load_progress(
                    self,
                    records: int,
                ) -> FlextLdapProtocols.Result[bool]:
                    """Track LDAP loading progress."""
                    ...


p = FlextTargetLdapProtocols
__all__ = ["FlextTargetLdapProtocols", "p"]
