"""Target LDAP protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextTargetLdapProtocols(FlextProtocols):
    """Target LDAP protocols extending FlextProtocols with LDAP target-specific interfaces.

    This class provides protocol definitions for Singer target operations with LDAP directory integration,
    data transformation, connection management, and enterprise LDAP authentication patterns.
    """

    @runtime_checkable
    class TargetProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP target operations."""

        def create_target(self, config: dict[str, object]) -> FlextResult[object]:
            """Create LDAP target instance.

            Args:
                config: Target configuration parameters

            Returns:
                FlextResult[object]: Target instance or error

            """

        def load_records(
            self,
            records: list[dict[str, object]],
            config: dict[str, object],
            *,
            stream_type: str = "users",
        ) -> FlextResult[int]:
            """Load records to LDAP directory.

            Args:
                records: Records to load into LDAP
                config: LDAP target configuration
                stream_type: Type of stream being processed

            Returns:
                FlextResult[int]: Number of records loaded or error

            """

        def validate_target_config(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate LDAP target configuration.

            Args:
                config: Configuration to validate

            Returns:
                FlextResult[bool]: Configuration validation status

            """

        def get_target_capabilities(self) -> FlextResult[dict[str, object]]:
            """Get LDAP target capabilities.

            Returns:
                FlextResult[dict[str, object]]: Target capabilities or error

            """

    @runtime_checkable
    class TransformationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP data transformation operations."""

        def transform_record(
            self,
            record: dict[str, object],
            mappings: list[dict[str, object]],
            object_classes: list[str],
            base_dn: str,
        ) -> FlextResult[dict[str, object]]:
            """Transform Singer record to LDAP entry.

            Args:
                record: Singer record to transform
                mappings: LDAP attribute mappings
                object_classes: LDAP object classes
                base_dn: Base DN for LDAP entry

            Returns:
                FlextResult[dict[str, object]]: Transformed LDAP entry or error

            """

        def validate_entry(self, entry: dict[str, object]) -> FlextResult[bool]:
            """Validate LDAP entry against business rules.

            Args:
                entry: LDAP entry to validate

            Returns:
                FlextResult[bool]: Entry validation status

            """

        def build_dn_from_template(
            self, template: str, record: dict[str, object], base_dn: str
        ) -> FlextResult[str]:
            """Build LDAP DN from template and record data.

            Args:
                template: DN template with placeholders
                record: Record data for DN construction
                base_dn: Base DN for LDAP operations

            Returns:
                FlextResult[str]: Constructed DN or error

            """

        def map_singer_to_ldap_attributes(
            self, record: dict[str, object], attribute_mapping: dict[str, str]
        ) -> FlextResult[dict[str, list[str]]]:
            """Map Singer record attributes to LDAP attributes.

            Args:
                record: Singer record with source data
                attribute_mapping: Mapping configuration

            Returns:
                FlextResult[dict[str, list[str]]]: LDAP attributes or error

            """

    @runtime_checkable
    class OrchestrationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP orchestration operations."""

        def orchestrate_data_loading(
            self, records: list[dict[str, object]], config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Orchestrate batch data loading to LDAP.

            Args:
                records: Records to load
                config: Target configuration

            Returns:
                FlextResult[dict[str, object]]: Loading result or error

            """

        def validate_target_configuration(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate complete target configuration.

            Args:
                config: Configuration to validate

            Returns:
                FlextResult[bool]: Configuration validation status

            """

        def process_singer_stream(
            self,
            stream_name: str,
            schema: dict[str, object],
            records: list[dict[str, object]],
            config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Process complete Singer stream to LDAP.

            Args:
                stream_name: Name of the Singer stream
                schema: Stream schema definition
                records: Stream records
                config: Processing configuration

            Returns:
                FlextResult[dict[str, object]]: Stream processing result or error

            """

        def manage_ldap_transaction(
            self, operations: list[dict[str, object]], config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Manage LDAP transaction with rollback capabilities.

            Args:
                operations: LDAP operations to execute
                config: Transaction configuration

            Returns:
                FlextResult[dict[str, object]]: Transaction result or error

            """

    @runtime_checkable
    class ConnectionProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP connection management operations."""

        def establish_connection(
            self, config: dict[str, object]
        ) -> FlextResult[object]:
            """Establish LDAP connection.

            Args:
                config: Connection configuration

            Returns:
                FlextResult[object]: Connection instance or error

            """

        def test_connection(
            self, config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Test LDAP connection.

            Args:
                config: Connection configuration

            Returns:
                FlextResult[dict[str, object]]: Connection test result or error

            """

        def close_connection(self, connection: object) -> FlextResult[bool]:
            """Close LDAP connection.

            Args:
                connection: Connection to close

            Returns:
                FlextResult[bool]: Close operation success status

            """

        def validate_credentials(self, config: dict[str, object]) -> FlextResult[bool]:
            """Validate LDAP credentials.

            Args:
                config: Configuration with credentials

            Returns:
                FlextResult[bool]: Credential validation status

            """

        def get_connection_status(
            self, connection: object
        ) -> FlextResult[dict[str, object]]:
            """Get LDAP connection status.

            Args:
                connection: Connection instance

            Returns:
                FlextResult[dict[str, object]]: Connection status or error

            """

    @runtime_checkable
    class SingerProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Singer protocol operations."""

        def process_schema_message(
            self, message: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process Singer SCHEMA message.

            Args:
                message: Singer SCHEMA message

            Returns:
                FlextResult[dict[str, object]]: Schema processing result or error

            """

        def process_record_message(
            self, message: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process Singer RECORD message.

            Args:
                message: Singer RECORD message

            Returns:
                FlextResult[dict[str, object]]: Record processing result or error

            """

        def process_state_message(
            self, message: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Process Singer STATE message.

            Args:
                message: Singer STATE message

            Returns:
                FlextResult[dict[str, object]]: State processing result or error

            """

        def validate_singer_message(
            self, message: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate Singer message format.

            Args:
                message: Singer message to validate

            Returns:
                FlextResult[bool]: Message validation status

            """

        def get_singer_capabilities(self) -> FlextResult[dict[str, object]]:
            """Get Singer target capabilities.

            Returns:
                FlextResult[dict[str, object]]: Singer capabilities or error

            """

    @runtime_checkable
    class PerformanceProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP performance optimization operations."""

        def optimize_batch_size(
            self,
            current_metrics: dict[str, object],
            target_performance: dict[str, object],
        ) -> FlextResult[int]:
            """Optimize LDAP batch size based on performance metrics.

            Args:
                current_metrics: Current performance metrics
                target_performance: Target performance goals

            Returns:
                FlextResult[int]: Optimal batch size or error

            """

        def manage_connection_pool(
            self, pool_config: dict[str, object], usage_metrics: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Manage LDAP connection pool for optimal performance.

            Args:
                pool_config: Connection pool configuration
                usage_metrics: Pool usage metrics

            Returns:
                FlextResult[dict[str, object]]: Pool management result or error

            """

        def cache_ldap_operations(
            self, operation_type: str, cache_config: dict[str, object]
        ) -> FlextResult[bool]:
            """Cache LDAP operations for performance optimization.

            Args:
                operation_type: Type of operation to cache
                cache_config: Cache configuration

            Returns:
                FlextResult[bool]: Caching setup success status

            """

        def monitor_performance_metrics(self) -> FlextResult[dict[str, object]]:
            """Monitor LDAP performance metrics.

            Returns:
                FlextResult[dict[str, object]]: Performance metrics or error

            """

    @runtime_checkable
    class SecurityProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP security operations."""

        def encrypt_credentials(
            self, credentials: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Encrypt LDAP credentials for secure storage.

            Args:
                credentials: Raw credentials to encrypt

            Returns:
                FlextResult[dict[str, object]]: Encrypted credentials or error

            """

        def validate_ssl_connection(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate SSL/TLS connection configuration.

            Args:
                config: SSL connection configuration

            Returns:
                FlextResult[bool]: SSL validation status

            """

        def audit_ldap_operations(
            self, operation: str, details: dict[str, object]
        ) -> FlextResult[bool]:
            """Audit LDAP operations for security compliance.

            Args:
                operation: Operation being audited
                details: Operation details

            Returns:
                FlextResult[bool]: Audit logging success status

            """

        def validate_access_permissions(
            self, user_dn: str, operation: str, target_dn: str
        ) -> FlextResult[bool]:
            """Validate user access permissions for LDAP operations.

            Args:
                user_dn: User DN performing operation
                operation: Type of operation
                target_dn: Target DN for operation

            Returns:
                FlextResult[bool]: Permission validation status

            """

    @runtime_checkable
    class MonitoringProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for LDAP monitoring operations."""

        def track_operation_metrics(
            self, operation: str, duration: float, *, success: bool
        ) -> FlextResult[bool]:
            """Track LDAP operation metrics.

            Args:
                operation: Operation name
                duration: Operation duration in seconds
                success: Operation success status

            Returns:
                FlextResult[bool]: Metric tracking success status

            """

        def get_health_status(self) -> FlextResult[dict[str, object]]:
            """Get LDAP target health status.

            Returns:
                FlextResult[dict[str, object]]: Health status or error

            """

        def create_performance_report(
            self, time_range: str, *, include_details: bool = False
        ) -> FlextResult[dict[str, object]]:
            """Create LDAP performance report.

            Args:
                time_range: Time range for report
                include_details: Include detailed metrics

            Returns:
                FlextResult[dict[str, object]]: Performance report or error

            """

        def alert_on_threshold_breach(
            self, metric_name: str, threshold: float, current_value: float
        ) -> FlextResult[bool]:
            """Alert when performance thresholds are breached.

            Args:
                metric_name: Name of the metric
                threshold: Threshold value
                current_value: Current metric value

            Returns:
                FlextResult[bool]: Alert creation success status

            """

    # Convenience aliases for easier downstream usage
    LdapTargetProtocol = TargetProtocol
    LdapTransformationProtocol = TransformationProtocol
    LdapOrchestrationProtocol = OrchestrationProtocol
    LdapConnectionProtocol = ConnectionProtocol
    LdapSingerProtocol = SingerProtocol
    LdapPerformanceProtocol = PerformanceProtocol
    LdapSecurityProtocol = SecurityProtocol
    LdapMonitoringProtocol = MonitoringProtocol


__all__ = [
    "FlextTargetLdapProtocols",
]
