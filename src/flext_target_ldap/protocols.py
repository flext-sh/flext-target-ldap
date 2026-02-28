"""Target LDAP protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from flext_ldap import FlextLdapProtocols
from flext_meltano import FlextMeltanoProtocols

from flext_target_ldap.typings import t


class FlextTargetLdapProtocols(FlextMeltanoProtocols, FlextLdapProtocols):
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
    entry: p.Ldap.EntryProtocol

    # Meltano protocols (inherited)
    target: p.Meltano.TargetProtocol

    # Target LDAP-specific protocols
    target_protocol: p.Target.Ldap.TargetProtocol
    """

    class TargetLdap:
        """Singer Target domain protocols."""

        class Ldap:
            """Singer Target LDAP domain protocols for LDAP directory loading."""

            @runtime_checkable
            class TargetProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for LDAP target operations."""

                def process_record(
                    self,
                    record: Mapping[str, t.GeneralValueType],
                ) -> FlextMeltanoProtocols.Result[bool]:
                    """Process a single record."""
                    ...

            @runtime_checkable
            class TransformationProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for Singer to LDAP transformation."""

                def transform_to_ldap(
                    self,
                    record: Mapping[str, t.GeneralValueType],
                ) -> FlextMeltanoProtocols.Result[Mapping[str, t.GeneralValueType]]:
                    """Transform record to LDAP format."""
                    ...

            @runtime_checkable
            class OrchestrationProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for LDAP loading orchestration."""

                def orchestrate_load(
                    self,
                    records: Sequence[Mapping[str, t.GeneralValueType]],
                ) -> FlextMeltanoProtocols.Result[bool]:
                    """Orchestrate loading of records."""
                    ...

            @runtime_checkable
            class ConnectionProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for LDAP connection management."""

                def connect(
                    self,
                    config: Mapping[str, t.GeneralValueType],
                ) -> FlextMeltanoProtocols.Result[t.GeneralValueType]:
                    """Connect to LDAP server."""
                    ...

            @runtime_checkable
            class SingerProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for Singer message handling."""

                def process_singer_message(
                    self,
                    message: Mapping[str, t.GeneralValueType],
                ) -> FlextMeltanoProtocols.Result[bool]:
                    """Process a Singer protocol message."""
                    ...

            @runtime_checkable
            class PerformanceProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for LDAP loading performance."""

                def optimize_batch(
                    self,
                    batch_size: int,
                ) -> FlextMeltanoProtocols.Result[int]:
                    """Optimize batch size for LDAP loading."""
                    ...

            @runtime_checkable
            class SecurityProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for LDAP security operations."""

                def validate_credentials(
                    self,
                    config: Mapping[str, t.GeneralValueType],
                ) -> FlextMeltanoProtocols.Result[bool]:
                    """Validate LDAP credentials."""
                    ...

            @runtime_checkable
            class MonitoringProtocol(
                FlextLdapProtocols.Service[t.GeneralValueType],
                Protocol,
            ):
                """Protocol for LDAP loading monitoring."""

                def track_load_progress(
                    self,
                    records: int,
                ) -> FlextMeltanoProtocols.Result[bool]:
                    """Track LDAP loading progress."""
                    ...


# Runtime alias for simplified usage
p = FlextTargetLdapProtocols

__all__ = [
    "FlextTargetLdapProtocols",
    "p",
]
