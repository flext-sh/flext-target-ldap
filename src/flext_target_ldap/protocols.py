"""Target LDAP protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from flext_core.typings import t
from flext_ldap import FlextLdapProtocols


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

        class Ldap:
            """Singer Target LDAP domain protocols for LDAP directory loading."""

            @runtime_checkable
            class Target(
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]],
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
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]],
                Protocol,
            ):
                """Protocol for Singer to LDAP transformation."""

                def transform_to_ldap(
                    self,
                    record: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[Mapping[str, t.ContainerValue]]:
                    """Transform record to LDAP format."""
                    ...

            @runtime_checkable
            class Orchestration(
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]], Protocol
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
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]], Protocol
            ):
                """Protocol for LDAP connection management."""

                def connect(
                    self,
                    config: Mapping[str, t.ContainerValue],
                ) -> FlextLdapProtocols.Result[Mapping[str, t.ContainerValue]]:
                    """Connect to LDAP server."""
                    ...

            @runtime_checkable
            class Singer(
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]],
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
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]], Protocol
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
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]],
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
                FlextLdapProtocols.Service[Mapping[str, t.ContainerValue]], Protocol
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
