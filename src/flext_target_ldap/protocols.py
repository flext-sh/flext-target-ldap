"""Target LDAP protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_ldap.protocols import FlextLdapProtocols as p_ldap
from flext_meltano.protocols import FlextMeltanoProtocols as p_meltano


class FlextTargetLdapProtocols(p_meltano, p_ldap):
    """Singer Target LDAP protocols extending LDAP and Meltano protocols.

    Extends both FlextLdapProtocols and FlextMeltanoProtocols via multiple inheritance
    to inherit all LDAP protocols, Meltano protocols, and foundation protocols.

    Architecture:
    - EXTENDS: FlextLdapProtocols (inherits .Ldap.* and .Ldif.* protocols)
    - EXTENDS: FlextMeltanoProtocols (inherits .Meltano.* protocols)
    - ADDS: Target LDAP-specific protocols in TargetLdap namespace
    - PROVIDES: Root-level alias `p` for convenient access
    """

    class TargetLdap:
        """Singer Target LDAP domain protocols for LDAP directory loading."""

        @runtime_checkable
        class TargetProtocol(p_ldap.Service[object], Protocol):
            """Protocol for LDAP target operations."""

            def process_record(
                self, record: dict[str, object]
            ) -> p_meltano.Result[bool]:
                """Process a single record."""
                ...

        @runtime_checkable
        class TransformationProtocol(p_ldap.Service[object], Protocol):
            """Protocol for Singer to LDAP transformation."""

            def transform_to_ldap(
                self,
                record: dict[str, object],
            ) -> p_meltano.Result[dict[str, object]]:
                """Transform record to LDAP format."""
                ...

        @runtime_checkable
        class OrchestrationProtocol(p_ldap.Service[object], Protocol):
            """Protocol for LDAP loading orchestration."""

            def orchestrate_load(
                self,
                records: list[dict[str, object]],
            ) -> p_meltano.Result[bool]:
                """Orchestrate loading of records."""
                ...

        @runtime_checkable
        class ConnectionProtocol(p_ldap.Service[object], Protocol):
            """Protocol for LDAP connection management."""

            def connect(self, config: dict[str, object]) -> p_meltano.Result[object]:
                """Connect to LDAP server."""
                ...

        @runtime_checkable
        class SingerProtocol(p_ldap.Service[object], Protocol):
            """Protocol for Singer message handling."""

            def process_singer_message(
                self,
                message: dict[str, object],
            ) -> p_meltano.Result[bool]:
                """Process a Singer protocol message."""
                ...

        @runtime_checkable
        class PerformanceProtocol(p_ldap.Service[object], Protocol):
            """Protocol for LDAP loading performance."""

            def optimize_batch(self, batch_size: int) -> p_meltano.Result[int]:
                """Optimize batch size for LDAP loading."""
                ...

        @runtime_checkable
        class SecurityProtocol(p_ldap.Service[object], Protocol):
            """Protocol for LDAP security operations."""

            def validate_credentials(
                self,
                config: dict[str, object],
            ) -> p_meltano.Result[bool]:
                """Validate LDAP credentials."""
                ...

        @runtime_checkable
        class MonitoringProtocol(p_ldap.Service[object], Protocol):
            """Protocol for LDAP loading monitoring."""

            def track_load_progress(self, records: int) -> p_meltano.Result[bool]:
                """Track LDAP loading progress."""
                ...


# Runtime alias for simplified usage
p = FlextTargetLdapProtocols

__all__ = [
    "FlextTargetLdapProtocols",
    "p",
]
