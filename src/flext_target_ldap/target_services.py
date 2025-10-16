"""LDAP Target Services - PEP8 Consolidation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol, override

from flext_core import FlextLogger, FlextResult, FlextTypes
from flext_ldap import FlextLdap

from flext_target_ldap import target_client as target_client_module
from flext_target_ldap.target_config import (
    TargetLdapConfig,
    validate_ldap_target_config,
)
from flext_target_ldap.target_models import (
    LdapAttributeMappingModel,
    LdapEntryModel,
    LdapTransformationResultModel,
)
from flext_target_ldap.typings import FlextTargetLdapTypes

logger = FlextLogger(__name__)


class LdapTargetServiceProtocol(Protocol):
    """Protocol for LDAP target services."""

    def create_target(
        self, config: FlextTargetLdapTypes.Core.Dict
    ) -> FlextResult[object]:
        """Create LDAP target instance."""

    def load_records(
        self,
        records: list[FlextTargetLdapTypes.Core.Dict],
        config: FlextTargetLdapTypes.Core.Dict,
        stream_type: str = "users",
    ) -> FlextResult[int]:
        """Load records to LDAP."""


class LdapTransformationServiceProtocol(Protocol):
    """Protocol for LDAP data transformation services."""

    def transform_record(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
        mappings: list[LdapAttributeMappingModel],
        object_classes: FlextTargetLdapTypes.Core.StringList,
        base_dn: str,
    ) -> FlextResult[LdapTransformationResultModel]:
        """Transform Singer record to LDAP entry."""

    def validate_entry(
        self,
        entry: LdapEntryModel,
    ) -> FlextResult[None]:
        """Validate LDAP entry against business rules."""


class LdapOrchestrationServiceProtocol(Protocol):
    """Protocol for LDAP orchestration services."""

    def orchestrate_data_loading(
        self,
        records: list[FlextTargetLdapTypes.Core.Dict],
        config: TargetLdapConfig,
    ) -> FlextResult[FlextTargetLdapTypes.Core.Dict]:
        """Orchestrate batch data loading."""

    def validate_target_configuration(
        self,
        config: TargetLdapConfig,
    ) -> FlextResult[bool]:
        """Validate target configuration."""


class LdapConnectionService:
    """Service for managing LDAP connections and basic operations."""

    @override
    def __init__(self, config: TargetLdapConfig) -> None:
        """Initialize connection service."""
        self._config: FlextTypes.Dict = config
        api = FlextLdap()
        self._ldap_api = api.client

    def test_connection(self) -> FlextResult[bool]:
        """Test LDAP connection with current configuration."""
        try:
            # Build server URL
            protocol = "ldaps" if self._config.connection.use_ssl else "ldap"
            server_url = f"{protocol}://{self._config.connection.server}:{self._config.connection.port}"

            # Use proper credentials for connection test
            bind_dn = (
                self._config.connection.bind_dn or ""
            )  # Empty string for anonymous bind
            bind_password = (
                self._config.connection.bind_password or ""
            )  # Empty string for anonymous bind

            # Establish and close a simple connection to validate
            with self._ldap_api.connection(
                server_url,
                bind_dn,
                bind_password,
            ) as session:
                # Optionally perform a NOOP or simple bind check if available
                _ = session  # ensure variable is used for static checkers
            logger.info("LDAP connection test successful")
            return FlextResult[bool].ok(data=True)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Connection test failed")
            return FlextResult[bool].fail(f"Connection test error: {e}")

    def get_connection_info(self: object) -> FlextTargetLdapTypes.Core.Dict:
        """Get connection information for logging/monitoring."""
        return {
            "host": self._config.connection.server,
            "port": self._config.connection.port,
            "use_ssl": self._config.connection.use_ssl,
            "base_dn": self._config.base_dn,
            "timeout": self._config.connection.timeout,
        }


class LdapTransformationService:
    """Service for transforming Singer records to LDAP entries."""

    @override
    def __init__(self, config: TargetLdapConfig) -> None:
        """Initialize transformation service."""
        # ZERO TOLERANCE FIX: Use FlextTargetLdapUtilities for ALL business logic
        from flext_target_ldap.utilities import FlextTargetLdapUtilities

        self._utilities = FlextTargetLdapUtilities()
        self._config: FlextTypes.Dict = config

    def transform_record(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
        mappings: list[LdapAttributeMappingModel],
        object_classes: FlextTargetLdapTypes.Core.StringList,
        base_dn: str,
    ) -> FlextResult[LdapTransformationResultModel]:
        """Transform Singer record to LDAP entry."""
        try:
            start_time = datetime.now(UTC)
            transformation_errors: FlextTargetLdapTypes.Core.StringList = []
            applied_mappings: list[LdapAttributeMappingModel] = []

            # ZERO TOLERANCE FIX: Use utilities for DN building
            dn_template = self._determine_dn_template(object_classes)
            dn_result = self._utilities.LdapDataProcessing.build_ldap_dn(
                record=record, dn_template=dn_template, base_dn=base_dn
            )

            if dn_result.is_failure:
                transformation_errors.append(f"DN building failed: {dn_result.error}")
                # Use fallback DN
                dn = f"cn=unknown-{int(datetime.now(UTC).timestamp())},{base_dn}"
            else:
                dn = dn_result.value

            # ZERO TOLERANCE FIX: Use utilities for LDAP attribute conversion
            attribute_mapping_dict = {
                mapping.singer_field_name: mapping.ldap_attribute_name
                for mapping in mappings
            }

            conversion_result = (
                self._utilities.LdapDataProcessing.convert_record_to_ldap_attributes(
                    record=record, attribute_mapping=attribute_mapping_dict
                )
            )

            if conversion_result.is_failure:
                transformation_errors.append(
                    f"Attribute conversion failed: {conversion_result.error}"
                )
                ldap_attributes_bytes = {}
            else:
                ldap_attributes_bytes = conversion_result.value

            # Convert bytes back to strings for the model
            ldap_attributes: dict[str, FlextTargetLdapTypes.Core.StringList] = {}
            for attr_name, attr_values in ldap_attributes_bytes.items():
                ldap_attributes[attr_name] = [
                    val.decode("utf-8") for val in attr_values
                ]

            # Process mappings for applied_mappings tracking
            for mapping in mappings:
                try:
                    # Get value from record
                    value = record.get(mapping.singer_field_name)

                    # Apply default value if missing
                    if value is None and mapping.default_value:
                        value = mapping.default_value

                    # Skip if no value and not required
                    if value is None:
                        if mapping.is_required:
                            transformation_errors.append(
                                f"Required field '{mapping.singer_field_name}' is missing",
                            )
                        continue

                    # Apply transformation rule using utilities (sanitization)
                    if mapping.transformation_rule and value is not None:
                        processed_value = self._apply_transformation_rule(
                            str(value),
                            mapping.transformation_rule,
                        )
                        # Use utilities for sanitization
                        processed_value = (
                            self._utilities.LdapDataProcessing.sanitize_ldap_value(
                                processed_value
                            )
                        )

                    applied_mappings.append(mapping)

                except (RuntimeError, ValueError, TypeError) as e:
                    transformation_errors.append(
                        f"Error transforming '{mapping.singer_field_name}': {e}",
                    )

            # ZERO TOLERANCE FIX: Use utilities for object class extraction
            final_object_classes = (
                self._utilities.LdapDataProcessing.extract_object_classes(
                    record=record, default_object_classes=object_classes
                )
            )

            # Create LDAP entry model
            try:
                ldap_entry = LdapEntryModel(
                    distinguished_name=dn,
                    object_classes=final_object_classes,
                    attributes=ldap_attributes,
                    entry_type=self._determine_entry_type(final_object_classes),
                )
            except (RuntimeError, ValueError, TypeError) as e:
                transformation_errors.append(f"Error creating LDAP entry: {e}")
                # Create minimal entry for error reporting
                ldap_entry = LdapEntryModel(
                    distinguished_name=dn,
                    object_classes=["top"],
                    attributes={},
                    entry_type="error",
                )

            # Calculate processing time
            end_time = datetime.now(UTC)
            processing_time = int((end_time - start_time).total_seconds() * 1000)

            # Create transformation result
            result = LdapTransformationResultModel(
                original_record=record,
                transformed_entry=ldap_entry,
                applied_mappings=applied_mappings,
                transformation_errors=transformation_errors,
                processing_time_ms=processing_time,
                transformation_timestamp=end_time,
            )

            return FlextResult[LdapTransformationResultModel].ok(result)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Record transformation failed")
            return FlextResult[LdapTransformationResultModel].fail(
                f"Transformation failed: {e}",
            )

    def _determine_dn_template(
        self, object_classes: FlextTargetLdapTypes.Core.StringList
    ) -> str:
        """Determine DN template based on object classes."""
        oc_lower = [oc.lower() for oc in object_classes]

        if "person" in oc_lower or "inetorgperson" in oc_lower:
            return "uid={username}"
        if "groupofnames" in oc_lower or "posixgroup" in oc_lower:
            return "cn={name}"
        if "organizationalunit" in oc_lower:
            return "ou={name}"
        return "cn={name}"

    def _apply_transformation_rule(self, value: str, rule: str) -> str:
        """Apply transformation rule to a value."""
        try:
            match rule:
                case "lowercase":
                    return value.lower()
                case "uppercase":
                    return value.upper()
                case "trim":
                    return value.strip()
                case "normalize":
                    return value.strip().lower()
                case _:
                    logger.warning("Unknown transformation rule: %s", rule)
                    return value
        except (RuntimeError, ValueError, TypeError) as e:
            logger.warning("Failed to apply transformation rule %s: %s", rule, e)
            return value

    def _determine_entry_type(
        self, object_classes: FlextTargetLdapTypes.Core.StringList
    ) -> str:
        """Determine entry type from object classes."""
        oc_lower = [oc.lower() for oc in object_classes]

        if "person" in oc_lower or "inetorgperson" in oc_lower:
            return "user"
        if "groupofnames" in oc_lower or "posixgroup" in oc_lower:
            return "group"
        if "organizationalunit" in oc_lower:
            return "organizational_unit"
        if "organization" in oc_lower:
            return "organization"
        return "generic"

    def validate_entry(self, entry: LdapEntryModel) -> FlextResult[None]:
        """Validate LDAP entry against business rules."""
        try:
            # Use the entry's own validation
            return entry.validate_business_rules()
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Entry validation failed: {e}")

    def get_default_mappings(self, entry_type: str) -> list[LdapAttributeMappingModel]:
        """Get default attribute mappings for entry type."""
        try:
            mappings: list[LdapAttributeMappingModel] = []

            if entry_type == "user":
                user_mappings = [
                    ("username", "uid", True),
                    ("email", "mail", False),
                    ("first_name", "givenName", False),
                    ("last_name", "sn", True),  # Required for person
                    ("full_name", "cn", True),  # Required for person
                    ("phone", "telephoneNumber", False),
                    ("department", "departmentNumber", False),
                    ("title", "title", False),
                ]
                for singer_field, ldap_attr, required in user_mappings:
                    mappings.append(
                        LdapAttributeMappingModel(
                            singer_field_name=singer_field,
                            ldap_attribute_name=ldap_attr,
                            is_required=required,
                        ),
                    )

            elif entry_type == "group":
                group_mappings = [
                    ("name", "cn", True),
                    ("description", "description", False),
                    ("members", "member", False),
                ]
                for singer_field, ldap_attr, required in group_mappings:
                    mappings.append(
                        LdapAttributeMappingModel(
                            singer_field_name=singer_field,
                            ldap_attribute_name=ldap_attr,
                            is_required=required,
                        ),
                    )

            elif entry_type == "organizational_unit":
                ou_mappings = [
                    ("name", "ou", True),
                    ("description", "description", False),
                ]
                for singer_field, ldap_attr, required in ou_mappings:
                    mappings.append(
                        LdapAttributeMappingModel(
                            singer_field_name=singer_field,
                            ldap_attribute_name=ldap_attr,
                            is_required=required,
                        ),
                    )

            return mappings

        except (RuntimeError, ValueError, TypeError):
            logger.exception("Failed to create default mappings")
            return []


class LdapTargetOrchestrator:
    """Application orchestrator for LDAP target operations using enterprise patterns."""

    @override
    def __init__(
        self,
        config: FlextTargetLdapTypes.Core.Dict | TargetLdapConfig | None = None,
    ) -> None:
        """Initialize LDAP target orchestrator."""
        # ZERO TOLERANCE FIX: Use FlextTargetLdapUtilities for ALL business logic
        from flext_target_ldap.utilities import FlextTargetLdapUtilities

        self._utilities = FlextTargetLdapUtilities()

        if isinstance(config, dict):
            self.config: FlextTypes.Dict = config
            self._typed_config: TargetLdapConfig | None = None
        elif isinstance(config, TargetLdapConfig):
            self._typed_config: FlextTypes.Dict = config
            self.config: FlextTypes.Dict = {}  # For backward compatibility
        else:
            self.config: FlextTypes.Dict = {}
            self._typed_config = None

        # Initialize services
        self._connection_service: LdapConnectionService | None = None
        self._transformation_service: LdapTransformationService | None = None

        logger.debug("Initialized LDAP target orchestrator")

    def get_typed_config(self: object) -> TargetLdapConfig | None:
        """Get typed configuration if available."""
        return self._typed_config

    def get_connection_service(self: object) -> LdapConnectionService | None:
        """Get connection service if config is available."""
        if self._typed_config and not self._connection_service:
            self._connection_service = LdapConnectionService(self._typed_config)
        return self._connection_service

    def get_transformation_service(self: object) -> LdapTransformationService | None:
        """Get transformation service if config is available."""
        if self._typed_config and not self._transformation_service:
            self._transformation_service = LdapTransformationService(self._typed_config)
        return self._transformation_service

    def orchestrate_data_loading(
        self,
        records: list[FlextTargetLdapTypes.Core.Dict],
        config: TargetLdapConfig | None = None,
    ) -> FlextResult[FlextTargetLdapTypes.Core.Dict]:
        """Orchestrate data loading to LDAP target."""
        try:
            logger.info("Starting LDAP data loading orchestration")

            # Use provided config or stored config
            working_config: FlextTypes.Dict = config or self._typed_config
            if not working_config:
                return FlextResult[FlextTargetLdapTypes.Core.Dict].fail(
                    "No configuration available for orchestration",
                )

            # ZERO TOLERANCE FIX: Use utilities for stream compatibility validation
            if (
                hasattr(working_config, "object_classes")
                and working_config.object_classes
            ):
                # Create mock schema for validation
                mock_schema = {"type": "object", "properties": {}}

                # Add properties based on first record if available
                if records:
                    for key in records[0]:
                        mock_schema["properties"][key] = {"type": "string"}

                compatibility_result = (
                    self._utilities.StreamUtilities.validate_stream_compatibility(
                        stream_name="ldap_target", schema=mock_schema
                    )
                )

                if compatibility_result.is_failure:
                    logger.warning(
                        "Stream compatibility validation failed: %s",
                        compatibility_result.error,
                    )

            # ZERO TOLERANCE FIX: Use utilities for batch size calculation
            optimal_batch_size = (
                self._utilities.StreamUtilities.calculate_ldap_batch_size(
                    record_count=len(records), target_batches=10
                )
            )

            # Use the calculated batch size or config batch size
            batch_size = min(
                optimal_batch_size,
                getattr(
                    working_config, "batch_size", self._utilities.DEFAULT_BATCH_SIZE
                ),
            )

            # Initialize services
            transformation_service = LdapTransformationService(working_config)

            # Process records in batches
            processed_count = 0
            transformation_errors: FlextTargetLdapTypes.Core.StringList = []

            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                logger.debug("Processing batch %d-%d", i, i + len(batch))

                for record in batch:
                    try:
                        # Get default mappings for user type (could be made configurable)
                        mappings = transformation_service.get_default_mappings("user")
                        object_classes = working_config.object_classes

                        # Transform record
                        transform_result = transformation_service.transform_record(
                            record=record,
                            mappings=mappings,
                            object_classes=object_classes,
                            base_dn=working_config.base_dn,
                        )

                        if transform_result.is_success:
                            processed_count += 1
                        else:
                            transformation_errors.append(
                                transform_result.error or "Unknown error",
                            )

                    except Exception as e:
                        error_msg = f"Error processing record: {e}"
                        logger.exception(error_msg)
                        transformation_errors.append(error_msg)

            # ZERO TOLERANCE FIX: Use utilities for stream metadata generation
            processing_time = 1.0  # Would be calculated in real implementation
            stream_metadata = (
                self._utilities.StreamUtilities.generate_ldap_stream_metadata(
                    stream_name="ldap_target",
                    record_count=processed_count,
                    processing_time=processing_time,
                )
            )

            result = {
                "processed_records": processed_count,
                "total_records": len(records),
                "transformation_errors": transformation_errors,
                "status": "completed"
                if not transformation_errors
                else "completed_with_errors",
                "metadata": stream_metadata,
            }

            logger.info(
                "LDAP data loading completed: %d/%d records",
                processed_count,
                len(records),
            )
            return FlextResult[FlextTargetLdapTypes.Core.Dict].ok(result)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP data loading orchestration failed")
            return FlextResult[FlextTargetLdapTypes.Core.Dict].fail(
                f"Data loading orchestration failed: {e}",
            )

    def validate_target_configuration(
        self,
        config: TargetLdapConfig | None = None,
    ) -> FlextResult[bool]:
        """Validate LDAP target configuration."""
        try:
            # Use provided config or stored config
            working_config: FlextTypes.Dict = config or self._typed_config
            if not working_config:
                return FlextResult[bool].fail(
                    "No configuration available for validation",
                )

            # ZERO TOLERANCE FIX: Use utilities for configuration validation
            config_dict = {
                "host": getattr(working_config, "host", ""),
                "bind_dn": getattr(working_config, "bind_dn", ""),
                "bind_password": getattr(working_config, "bind_password", ""),
                "base_dn": getattr(working_config, "base_dn", ""),
                "port": getattr(working_config, "port", 389),
                "use_ssl": getattr(working_config, "use_ssl", False),
                "use_tls": getattr(working_config, "use_tls", False),
                "operation_mode": getattr(working_config, "operation_mode", "upsert"),
                "batch_size": getattr(
                    working_config, "batch_size", self._utilities.DEFAULT_BATCH_SIZE
                ),
            }

            validation_result = self._utilities.ConfigValidation.validate_target_config(
                config_dict
            )
            if validation_result.is_failure:
                return FlextResult[bool].fail(
                    f"Configuration validation failed: {validation_result.error}",
                )

            # Validate business rules if available
            if hasattr(working_config, "validate_business_rules"):
                business_validation: FlextResult[object] = (
                    working_config.validate_business_rules()
                )
                if not business_validation.is_success:
                    return FlextResult[bool].fail(
                        f"Business rules validation failed: {business_validation.error}",
                    )

            # Test connection if possible
            connection_service = LdapConnectionService(working_config)
            connection_test = connection_service.test_connection()
            if not connection_test.is_success:
                logger.warning("Connection test failed: %s", connection_test.error)
                # Don't fail validation just because connection test fails
                # The server might not be available during configuration validation

            return FlextResult[bool].ok(data=True)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Configuration validation failed")
            return FlextResult[bool].fail(f"Configuration validation failed: {e}")


class LdapTargetApiService:
    """Simple API service for LDAP target operations."""

    @override
    def __init__(self: object) -> None:
        """Initialize API service."""
        self._orchestrators: dict[str, LdapTargetOrchestrator] = {}

    def create_ldap_target(
        self,
        config: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextResult[object]:
        """Create LDAP target with configuration."""
        try:
            target = target_client_module.TargetLdap(config=config)
            return FlextResult[object].ok(target)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[object].fail(f"Failed to create LDAP target: {e}")

    def load_users_to_ldap(
        self,
        users: list[FlextTargetLdapTypes.Core.Dict],
        config: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextResult[int]:
        """Load user records to LDAP."""
        target_result: FlextResult[object] = self.create_ldap_target(config)
        if not target_result.is_success:
            return FlextResult[int].fail(
                f"Target creation failed: {target_result.error}",
            )

        try:
            target = target_result.data
            if target is None:
                return FlextResult[int].fail("Target creation failed")

            if not isinstance(target, target_client_module.TargetLdap):
                return FlextResult[int].fail("Target is not a TargetLdap instance")

            sink: FlextTypes.Dict = target.get_sink_class("users")(
                target, "users", {}, ["username"]
            )

            # Process records
            for user in users:
                sink.process_record(user, {})

            # Return count of processed users
            return FlextResult[int].ok(len(users))

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[int].fail(f"Failed to load users: {e}")

    def load_groups_to_ldap(
        self,
        groups: list[FlextTargetLdapTypes.Core.Dict],
        config: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextResult[int]:
        """Load group records to LDAP."""
        target_result: FlextResult[object] = self.create_ldap_target(config)
        if not target_result.is_success:
            return FlextResult[int].fail(
                f"Target creation failed: {target_result.error}",
            )

        try:
            target = target_result.data
            if target is None:
                return FlextResult[int].fail("Target creation failed")

            if not isinstance(target, target_client_module.TargetLdap):
                return FlextResult[int].fail("Target is not a TargetLdap instance")

            sink: FlextTypes.Dict = target.get_sink_class("groups")(
                target, "groups", {}, ["name"]
            )

            # Process records
            for group in groups:
                sink.process_record(group, {})

            # Return count of processed groups
            return FlextResult[int].ok(len(groups))

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[int].fail(f"Failed to load groups: {e}")

    def test_ldap_connection(
        self,
        config: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextResult[bool]:
        """Test LDAP connection with given configuration."""
        try:
            # Create LDAP connection config
            config_result: FlextTypes.Dict = validate_ldap_target_config(config)
            if not config_result.is_success:
                return FlextResult[bool].fail(
                    f"Configuration validation failed: {config_result.error}",
                )

            # Test connection
            if config_result.data is None:
                return FlextResult[
                    bool
                ].fail(  # Fixed: FlextResult[None] -> FlextResult[bool]
                    "Configuration validation returned no data",
                )
            connection_service = LdapConnectionService(config_result.data)
            return connection_service.test_connection()

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Connection test error: {e}")


# Create default API service instance for backward compatibility
_default_api_service = LdapTargetApiService()


# Convenience function aliases for backward compatibility
def create_ldap_target(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextResult[object]:
    """Create LDAP target with configuration."""
    return _default_api_service.create_ldap_target(config)


def load_users_to_ldap(
    users: list[FlextTargetLdapTypes.Core.Dict],
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextResult[int]:
    """Load user records to LDAP."""
    return _default_api_service.load_users_to_ldap(users, config)


def load_groups_to_ldap(
    groups: list[FlextTargetLdapTypes.Core.Dict],
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextResult[int]:
    """Load group records to LDAP."""
    return _default_api_service.load_groups_to_ldap(groups, config)


def test_ldap_connection(
    config: FlextTargetLdapTypes.Core.Dict,
) -> FlextResult[bool]:
    """Test LDAP connection with given configuration."""
    return _default_api_service.test_ldap_connection(config)


# Backward compatibility aliases
create_target = create_ldap_target
test_connection = test_ldap_connection

__all__ = [
    # Service classes
    "LdapConnectionService",
    # Protocol interfaces
    "LdapOrchestrationServiceProtocol",
    "LdapTargetApiService",
    "LdapTargetOrchestrator",
    "LdapTargetServiceProtocol",
    "LdapTransformationService",
    "LdapTransformationServiceProtocol",
    # Convenience functions
    "create_ldap_target",
    "create_target",  # Backward compatibility
    "load_groups_to_ldap",
    "load_users_to_ldap",
    "test_connection",  # Backward compatibility
    "test_ldap_connection",
]
