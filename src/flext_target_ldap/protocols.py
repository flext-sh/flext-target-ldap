"""Target LDAP protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextTargetLdapProtocols:
    """Singer Target LDAP protocols with explicit re-exports from FlextProtocols foundation.

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
        class TargetProtocol(FlextProtocols.Service, Protocol):
            """Protocol for LDAP target operations."""

            def process_record(self, record: FlextTypes.Dict) -> FlextResult[None]:
                """Process a single record."""
                ...

        @runtime_checkable
        class TransformationProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Singer to LDAP transformation."""

            def transform_to_ldap(
                self, record: FlextTypes.Dict
            ) -> FlextResult[FlextTypes.Dict]:
                """Transform record to LDAP format."""
                ...

        @runtime_checkable
        class OrchestrationProtocol(FlextProtocols.Service, Protocol):
            """Protocol for LDAP loading orchestration."""

            def orchestrate_load(
                self, records: list[FlextTypes.Dict]
            ) -> FlextResult[None]:
                """Orchestrate loading of records."""
                ...

        @runtime_checkable
        class ConnectionProtocol(FlextProtocols.Service, Protocol):
            """Protocol for LDAP connection management."""

            def connect(self, config: FlextTypes.Dict) -> FlextResult[object]:
                """Connect to LDAP server."""
                ...

        @runtime_checkable
        class SingerProtocol(FlextProtocols.Service, Protocol):
            """Protocol for Singer message handling."""

            def process_singer_message(
                self, message: FlextTypes.Dict
            ) -> FlextResult[None]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextProtocols.Service, Protocol):
            """Protocol for LDAP loading performance."""

            def optimize_batch(self, batch_size: int) -> FlextResult[int]: ...

        @runtime_checkable
        class SecurityProtocol(FlextProtocols.Service, Protocol):
            """Protocol for LDAP security operations."""

            def validate_credentials(
                self, config: FlextTypes.Dict
            ) -> FlextResult[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextProtocols.Service, Protocol):
            """Protocol for LDAP loading monitoring."""

            def track_load_progress(self, records: int) -> FlextResult[None]: ...

    # ============================================================================
    # BACKWARD COMPATIBILITY ALIASES (100% COMPATIBILITY)
    # ============================================================================

    TargetProtocol = TargetLdap.TargetProtocol
    TransformationProtocol = TargetLdap.TransformationProtocol
    OrchestrationProtocol = TargetLdap.OrchestrationProtocol
    ConnectionProtocol = TargetLdap.ConnectionProtocol
    SingerProtocol = TargetLdap.SingerProtocol
    PerformanceProtocol = TargetLdap.PerformanceProtocol
    SecurityProtocol = TargetLdap.SecurityProtocol
    MonitoringProtocol = TargetLdap.MonitoringProtocol

    LdapTargetProtocol = TargetLdap.TargetProtocol
    LdapTransformationProtocol = TargetLdap.TransformationProtocol
    LdapOrchestrationProtocol = TargetLdap.OrchestrationProtocol
    LdapConnectionProtocol = TargetLdap.ConnectionProtocol
    LdapSingerProtocol = TargetLdap.SingerProtocol
    LdapPerformanceProtocol = TargetLdap.PerformanceProtocol
    LdapSecurityProtocol = TargetLdap.SecurityProtocol
    LdapMonitoringProtocol = TargetLdap.MonitoringProtocol


__all__ = [
    "FlextTargetLdapProtocols",
]
