"""Target LDAP protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextCore


class FlextTargetLdapProtocols:
    """Singer Target LDAP protocols with explicit re-exports from FlextCore.Protocols foundation.

    Domain Extension Pattern (Phase 3):
    - Explicit re-export of foundation protocols (not inheritance)
    - Domain-specific protocols organized in TargetLdap namespace
    - 100% backward compatibility through aliases
    """

    # ============================================================================
    # RE-EXPORT FOUNDATION PROTOCOLS (EXPLICIT PATTERN)
    # ============================================================================

    Foundation = FlextCore.Protocols.Foundation
    Domain = FlextCore.Protocols.Domain
    Application = FlextCore.Protocols.Application
    Infrastructure = FlextCore.Protocols.Infrastructure
    Extensions = FlextCore.Protocols.Extensions
    Commands = FlextCore.Protocols.Commands

    # ============================================================================
    # SINGER TARGET LDAP-SPECIFIC PROTOCOLS (DOMAIN NAMESPACE)
    # ============================================================================

    class TargetLdap:
        """Singer Target LDAP domain protocols for LDAP directory loading."""

        @runtime_checkable
        class TargetProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for LDAP target operations."""

            def process_record(
                self, record: FlextCore.Types.Dict
            ) -> FlextCore.Result[None]:
                """Process a single record."""
                ...

        @runtime_checkable
        class TransformationProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Singer to LDAP transformation."""

            def transform_to_ldap(
                self, record: FlextCore.Types.Dict
            ) -> FlextCore.Result[FlextCore.Types.Dict]:
                """Transform record to LDAP format."""
                ...

        @runtime_checkable
        class OrchestrationProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for LDAP loading orchestration."""

            def orchestrate_load(
                self, records: list[FlextCore.Types.Dict]
            ) -> FlextCore.Result[None]:
                """Orchestrate loading of records."""
                ...

        @runtime_checkable
        class ConnectionProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for LDAP connection management."""

            def connect(self, config: FlextCore.Types.Dict) -> FlextCore.Result[object]:
                """Connect to LDAP server."""
                ...

        @runtime_checkable
        class SingerProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for Singer message handling."""

            def process_singer_message(
                self, message: FlextCore.Types.Dict
            ) -> FlextCore.Result[None]: ...

        @runtime_checkable
        class PerformanceProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for LDAP loading performance."""

            def optimize_batch(self, batch_size: int) -> FlextCore.Result[int]: ...

        @runtime_checkable
        class SecurityProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for LDAP security operations."""

            def validate_credentials(
                self, config: FlextCore.Types.Dict
            ) -> FlextCore.Result[bool]: ...

        @runtime_checkable
        class MonitoringProtocol(FlextCore.Protocols.Domain.Service, Protocol):
            """Protocol for LDAP loading monitoring."""

            def track_load_progress(self, records: int) -> FlextCore.Result[None]: ...

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
