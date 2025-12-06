"""Target LDAP protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextResult, p


class FlextTargetLdapProtocols:
    """Singer Target LDAP protocols with explicit re-exports from p foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TargetLdap namespace
    - 100% backward compatibility through aliases
    """

    # ============================================================================
    # RE-EXPORT FOUNDATION PROTOCOLS (EXPLICIT PATTERN)
    # ============================================================================

    # ============================================================================
    # SINGER TARGET LDAP-SPECIFIC PROTOCOLS (DOMAIN NAMESPACE)
    # ============================================================================

    class TargetLdap:
        """Singer Target LDAP domain protocols for LDAP directory loading."""

        @runtime_checkable
        class TargetProtocol(p.Service, Protocol):
            """Protocol for LDAP target operations."""

            def process_record(self, record: dict[str, object]) -> FlextResult[None]:
                """Process a single record."""
                ...

        @runtime_checkable
        class TransformationProtocol(p.Service, Protocol):
            """Protocol for Singer to LDAP transformation."""

            def transform_to_ldap(
                self,
                record: dict[str, object],
            ) -> FlextResult[dict[str, object]]:
                """Transform record to LDAP format."""
                ...

        @runtime_checkable
        class OrchestrationProtocol(p.Service, Protocol):
            """Protocol for LDAP loading orchestration."""

            def orchestrate_load(
                self,
                records: list[dict[str, object]],
            ) -> FlextResult[None]:
                """Orchestrate loading of records."""
                ...

        @runtime_checkable
        class ConnectionProtocol(p.Service, Protocol):
            """Protocol for LDAP connection management."""

            def connect(self, config: dict[str, object]) -> FlextResult[object]:
                """Connect to LDAP server."""
                ...

        @runtime_checkable
        class SingerProtocol(p.Service, Protocol):
            """Protocol for Singer message handling."""

            def process_singer_message(
                self,
                message: dict[str, object],
            ) -> FlextResult[None]:
                """Process a Singer protocol message."""
                ...

        @runtime_checkable
        class PerformanceProtocol(p.Service, Protocol):
            """Protocol for LDAP loading performance."""

            def optimize_batch(self, batch_size: int) -> FlextResult[int]:
                """Optimize batch size for LDAP loading."""
                ...

        @runtime_checkable
        class SecurityProtocol(p.Service, Protocol):
            """Protocol for LDAP security operations."""

            def validate_credentials(
                self,
                config: dict[str, object],
            ) -> FlextResult[bool]:
                """Validate LDAP credentials."""
                ...

        @runtime_checkable
        class MonitoringProtocol(p.Service, Protocol):
            """Protocol for LDAP loading monitoring."""

            def track_load_progress(self, records: int) -> FlextResult[None]:
                """Track LDAP loading progress."""
                ...

    # ============================================================================
    # BACKWARD COMPATIBILITY ALIASES (100% COMPATIBILITY)
    # ============================================================================

    @runtime_checkable
    class TargetProtocol(TargetLdap.TargetProtocol):
        """TargetProtocol - real inheritance."""

    @runtime_checkable
    class TransformationProtocol(TargetLdap.TransformationProtocol):
        """TransformationProtocol - real inheritance."""

    @runtime_checkable
    class OrchestrationProtocol(TargetLdap.OrchestrationProtocol):
        """OrchestrationProtocol - real inheritance."""

    @runtime_checkable
    class ConnectionProtocol(TargetLdap.ConnectionProtocol):
        """ConnectionProtocol - real inheritance."""

    @runtime_checkable
    class SingerProtocol(TargetLdap.SingerProtocol):
        """SingerProtocol - real inheritance."""

    @runtime_checkable
    class PerformanceProtocol(TargetLdap.PerformanceProtocol):
        """PerformanceProtocol - real inheritance."""

    @runtime_checkable
    class SecurityProtocol(TargetLdap.SecurityProtocol):
        """SecurityProtocol - real inheritance."""

    @runtime_checkable
    class MonitoringProtocol(TargetLdap.MonitoringProtocol):
        """MonitoringProtocol - real inheritance."""

    @runtime_checkable
    class LdapTargetProtocol(TargetLdap.TargetProtocol):
        """LdapTargetProtocol - real inheritance."""

    @runtime_checkable
    class LdapTransformationProtocol(TargetLdap.TransformationProtocol):
        """LdapTransformationProtocol - real inheritance."""

    @runtime_checkable
    class LdapOrchestrationProtocol(TargetLdap.OrchestrationProtocol):
        """LdapOrchestrationProtocol - real inheritance."""

    @runtime_checkable
    class LdapConnectionProtocol(TargetLdap.ConnectionProtocol):
        """LdapConnectionProtocol - real inheritance."""

    @runtime_checkable
    class LdapSingerProtocol(TargetLdap.SingerProtocol):
        """LdapSingerProtocol - real inheritance."""

    @runtime_checkable
    class LdapPerformanceProtocol(TargetLdap.PerformanceProtocol):
        """LdapPerformanceProtocol - real inheritance."""

    @runtime_checkable
    class LdapSecurityProtocol(TargetLdap.SecurityProtocol):
        """LdapSecurityProtocol - real inheritance."""

    @runtime_checkable
    class LdapMonitoringProtocol(TargetLdap.MonitoringProtocol):
        """LdapMonitoringProtocol - real inheritance."""


__all__ = [
    "FlextTargetLdapProtocols",
]
