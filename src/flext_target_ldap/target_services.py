"""LDAP Target Services - PEP8 Consolidation.

This module consolidates LDAP target application services with descriptive PEP8 names,
providing enterprise-grade orchestration, transformation, and API services.

**Architecture**: Clean Architecture application layer services
**Patterns**: Service layer, orchestration, simple API
**Integration**: Complete flext-core + flext-ldap + target models integration

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

from flext_core import FlextLogger, FlextResult
from flext_ldap import get_ldap_api

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

logger = FlextLogger(__name__)


class LdapTargetServiceProtocol(Protocol):
    """Protocol for LDAP target services."""

    async def create_target(self, config: dict[str, object]) -> FlextResult[object]:
        """Create LDAP target instance."""
        ...

    async def load_records(
        self,
        records: list[dict[str, object]],
        config: dict[str, object],
        stream_type: str = "users",
    ) -> FlextResult[int]:
        """Load records to LDAP."""
        ...


class LdapTransformationServiceProtocol(Protocol):
    """Protocol for LDAP data transformation services."""

    def transform_record(
        self,
        record: dict[str, object],
        mappings: list[LdapAttributeMappingModel],
        object_classes: list[str],
        base_dn: str,
    ) -> FlextResult[LdapTransformationResultModel]:
        """Transform Singer record to LDAP entry."""
        ...

    def validate_entry(
        self,
        entry: LdapEntryModel,
    ) -> FlextResult[None]:
        """Validate LDAP entry against business rules."""
        ...


class LdapOrchestrationServiceProtocol(Protocol):
    """Protocol for LDAP orchestration services."""

    async def orchestrate_data_loading(
        self,
        records: list[dict[str, object]],
        config: TargetLdapConfig,
    ) -> FlextResult[dict[str, object]]:
        """Orchestrate batch data loading."""
        ...

    async def validate_target_configuration(
        self,
        config: TargetLdapConfig,
    ) -> FlextResult[bool]:
        """Validate target configuration."""
        ...


# =============================================================================
# LDAP CONNECTION SERVICE
# =============================================================================


class LdapConnectionService:
    """Service for managing LDAP connections and basic operations."""

    def __init__(self, config: TargetLdapConfig) -> None:
        """Initialize connection service."""
        self._config = config
        self._ldap_api = get_ldap_api()

    async def test_connection(self) -> FlextResult[bool]:
        """Test LDAP connection with current configuration."""
        try:
            # Build server URL
            protocol = "ldaps" if self._config.connection.use_ssl else "ldap"
            server_url = f"{protocol}://{self._config.connection.server}:{self._config.connection.port}"

            # Establish and close a simple connection to validate
            async with self._ldap_api.connection(server_url, None, None) as session:
                # Optionally perform a NOOP or simple bind check if available
                _ = session  # ensure variable is used for static checkers
            logger.info("LDAP connection test successful")
            return FlextResult[bool].ok(data=True)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Connection test failed")
            return FlextResult[bool].fail(f"Connection test error: {e}")

    def get_connection_info(self) -> dict[str, object]:
        """Get connection information for logging/monitoring."""
        return {
            "host": self._config.connection.server,
            "port": self._config.connection.port,
            "use_ssl": self._config.connection.use_ssl,
            "base_dn": self._config.base_dn,
            "timeout": self._config.connection.timeout,
        }


# =============================================================================
# LDAP TRANSFORMATION SERVICE
# =============================================================================


class LdapTransformationService:
    """Service for transforming Singer records to LDAP entries."""

    def __init__(self, config: TargetLdapConfig) -> None:
        """Initialize transformation service."""
        self._config = config

    def transform_record(
        self,
        record: dict[str, object],
        mappings: list[LdapAttributeMappingModel],
        object_classes: list[str],
        base_dn: str,
    ) -> FlextResult[LdapTransformationResultModel]:
        """Transform Singer record to LDAP entry."""
        try:
            start_time = datetime.now(UTC)
            transformation_errors: list[str] = []
            applied_mappings: list[LdapAttributeMappingModel] = []

            # Build LDAP attributes from mappings
            ldap_attributes: dict[str, list[str]] = {}

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

                    # Apply transformation rule
                    if mapping.transformation_rule and value is not None:
                        value = self._apply_transformation_rule(
                            str(value),
                            mapping.transformation_rule,
                        )

                    # Convert to LDAP attribute format
                    if isinstance(value, list):
                        ldap_attributes[mapping.ldap_attribute_name] = [
                            str(v) for v in value
                        ]
                    else:
                        ldap_attributes[mapping.ldap_attribute_name] = [str(value)]

                    applied_mappings.append(mapping)

                except (RuntimeError, ValueError, TypeError) as e:
                    transformation_errors.append(
                        f"Error transforming '{mapping.singer_field_name}': {e}",
                    )

            # Determine DN based on entry type and record
            dn = self._build_distinguished_name(record, object_classes, base_dn)

            # Create LDAP entry model
            try:
                ldap_entry = LdapEntryModel(
                    distinguished_name=dn,
                    object_classes=object_classes,
                    attributes=ldap_attributes,
                    entry_type=self._determine_entry_type(object_classes),
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
                f"Transformation failed: {e}"
            )

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

    def _build_distinguished_name(
        self,
        record: dict[str, object],
        object_classes: list[str],
        base_dn: str,
    ) -> str:
        """Build DN based on record and object classes."""
        # Determine RDN based on object class
        if "person" in [oc.lower() for oc in object_classes]:
            # Use uid for person entries
            uid = record.get("username") or record.get("uid") or record.get("cn")
            if uid:
                return f"uid={uid},{base_dn}"

        elif "groupofnames" in [oc.lower() for oc in object_classes]:
            # Use cn for group entries
            cn = record.get("name") or record.get("cn")
            if cn:
                return f"cn={cn},{base_dn}"

        elif "organizationalunit" in [oc.lower() for oc in object_classes]:
            # Use ou for organizational unit entries
            ou = record.get("name") or record.get("ou")
            if ou:
                return f"ou={ou},{base_dn}"

        # Default fallback - use first available identifier
        for field in ["name", "cn", "uid", "ou"]:
            value = record.get(field)
            if value:
                return f"cn={value},{base_dn}"

        # Last resort - use timestamp
        timestamp = int(datetime.now(UTC).timestamp())
        return f"cn=entry-{timestamp},{base_dn}"

    def _determine_entry_type(self, object_classes: list[str]) -> str:
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
            mappings = []

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


# =============================================================================
# LDAP ORCHESTRATION SERVICE
# =============================================================================


class LdapTargetOrchestrator:
    """Application orchestrator for LDAP target operations using enterprise patterns."""

    def __init__(
        self,
        config: dict[str, object] | TargetLdapConfig | None = None,
    ) -> None:
        """Initialize LDAP target orchestrator."""
        if isinstance(config, dict):
            self.config = config
            self._typed_config: TargetLdapConfig | None = None
        elif isinstance(config, TargetLdapConfig):
            self._typed_config = config
            self.config = {}  # For backward compatibility
        else:
            self.config = {}
            self._typed_config = None

        # Initialize services
        self._connection_service: LdapConnectionService | None = None
        self._transformation_service: LdapTransformationService | None = None

        logger.debug("Initialized LDAP target orchestrator")

    def get_typed_config(self) -> TargetLdapConfig | None:
        """Get typed configuration if available."""
        return self._typed_config

    def get_connection_service(self) -> LdapConnectionService | None:
        """Get connection service if config is available."""
        if self._typed_config and not self._connection_service:
            self._connection_service = LdapConnectionService(self._typed_config)
        return self._connection_service

    def get_transformation_service(self) -> LdapTransformationService | None:
        """Get transformation service if config is available."""
        if self._typed_config and not self._transformation_service:
            self._transformation_service = LdapTransformationService(self._typed_config)
        return self._transformation_service

    async def orchestrate_data_loading(
        self,
        records: list[dict[str, object]],
        config: TargetLdapConfig | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Orchestrate data loading to LDAP target."""
        try:
            logger.info("Starting LDAP data loading orchestration")

            # Use provided config or stored config
            working_config = config or self._typed_config
            if not working_config:
                return FlextResult[dict[str, object]].fail(
                    "No configuration available for orchestration"
                )

            # Initialize services
            transformation_service = LdapTransformationService(working_config)

            # Process records in batches
            batch_size = working_config.batch_size
            processed_count = 0
            transformation_errors: list[str] = []

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

            result = {
                "processed_records": processed_count,
                "total_records": len(records),
                "transformation_errors": transformation_errors,
                "status": "completed"
                if not transformation_errors
                else "completed_with_errors",
            }

            logger.info(
                "LDAP data loading completed: %d/%d records",
                processed_count,
                len(records),
            )
            return FlextResult[dict[str, object]].ok(result)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP data loading orchestration failed")
            return FlextResult[dict[str, object]].fail(
                f"Data loading orchestration failed: {e}"
            )

    async def validate_target_configuration(
        self,
        config: TargetLdapConfig | None = None,
    ) -> FlextResult[bool]:
        """Validate LDAP target configuration."""
        try:
            # Use provided config or stored config
            working_config = config or self._typed_config
            if not working_config:
                return FlextResult[bool].fail(
                    "No configuration available for validation"
                )

            # Validate business rules
            validation_result = working_config.validate_business_rules()
            if not validation_result.is_success:
                return FlextResult[bool].fail(
                    f"Configuration validation failed: {validation_result.error}",
                )

            # Test connection if possible
            connection_service = LdapConnectionService(working_config)
            connection_test = await connection_service.test_connection()
            if not connection_test.is_success:
                logger.warning("Connection test failed: %s", connection_test.error)
                # Don't fail validation just because connection test fails
                # The server might not be available during configuration validation

            return FlextResult[bool].ok(data=True)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Configuration validation failed")
            return FlextResult[bool].fail(f"Configuration validation failed: {e}")


# =============================================================================
# SIMPLE API SERVICE
# =============================================================================


class LdapTargetApiService:
    """Simple API service for LDAP target operations."""

    def __init__(self) -> None:
        """Initialize API service."""
        self._orchestrators: dict[str, LdapTargetOrchestrator] = {}

    async def create_ldap_target(
        self,
        config: dict[str, object],
    ) -> FlextResult[object]:
        """Create LDAP target with configuration."""
        try:
            target = target_client_module.TargetLdap(config=config)
            return FlextResult[object].ok(target)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[object].fail(f"Failed to create LDAP target: {e}")

    async def load_users_to_ldap(
        self,
        users: list[dict[str, object]],
        config: dict[str, object],
    ) -> FlextResult[int]:
        """Load user records to LDAP."""
        target_result = await self.create_ldap_target(config)
        if not target_result.is_success:
            return FlextResult[int].fail(
                f"Target creation failed: {target_result.error}"
            )

        try:
            target = target_result.data
            if target is None:
                return FlextResult[int].fail("Target creation failed")

            # Type assertion since we know target is TargetLdap
            if not isinstance(target, target_client_module.TargetLdap):
                return FlextResult[int].fail("Target is not a TargetLdap instance")

            sink = target.get_sink_class("users")(target, "users", {}, ["username"])

            # Process records
            for user in users:
                sink.process_record(user, {})

            # Return count of processed users
            return FlextResult[int].ok(len(users))

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[int].fail(f"Failed to load users: {e}")

    async def load_groups_to_ldap(
        self,
        groups: list[dict[str, object]],
        config: dict[str, object],
    ) -> FlextResult[int]:
        """Load group records to LDAP."""
        target_result = await self.create_ldap_target(config)
        if not target_result.is_success:
            return FlextResult[int].fail(
                f"Target creation failed: {target_result.error}"
            )

        try:
            target = target_result.data
            if target is None:
                return FlextResult[int].fail("Target creation failed")

            # Type assertion since we know target is TargetLdap
            if not isinstance(target, target_client_module.TargetLdap):
                return FlextResult[int].fail("Target is not a TargetLdap instance")

            sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])

            # Process records
            for group in groups:
                sink.process_record(group, {})

            # Return count of processed groups
            return FlextResult[int].ok(len(groups))

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[int].fail(f"Failed to load groups: {e}")

    async def test_ldap_connection(
        self,
        config: dict[str, object],
    ) -> FlextResult[bool]:
        """Test LDAP connection with given configuration."""
        try:
            # Create LDAP connection config
            config_result = validate_ldap_target_config(config)
            if not config_result.is_success:
                return FlextResult[bool].fail(
                    f"Configuration validation failed: {config_result.error}",
                )

            # Test connection
            if config_result.data is None:
                return FlextResult[None].fail(
                    "Configuration validation returned no data"
                )
            connection_service = LdapConnectionService(config_result.data)
            return await connection_service.test_connection()

        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[bool].fail(f"Connection test error: {e}")


# Create default API service instance for backward compatibility
_default_api_service = LdapTargetApiService()


# Convenience function aliases for backward compatibility
async def create_ldap_target(config: dict[str, object]) -> FlextResult[object]:
    """Create LDAP target with configuration."""
    return await _default_api_service.create_ldap_target(config)


async def load_users_to_ldap(
    users: list[dict[str, object]],
    config: dict[str, object],
) -> FlextResult[int]:
    """Load user records to LDAP."""
    return await _default_api_service.load_users_to_ldap(users, config)


async def load_groups_to_ldap(
    groups: list[dict[str, object]],
    config: dict[str, object],
) -> FlextResult[int]:
    """Load group records to LDAP."""
    return await _default_api_service.load_groups_to_ldap(groups, config)


async def test_ldap_connection(config: dict[str, object]) -> FlextResult[bool]:
    """Test LDAP connection with given configuration."""
    return await _default_api_service.test_ldap_connection(config)


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
