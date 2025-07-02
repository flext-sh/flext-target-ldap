"""Enterprise sink implementations for target-ldap.

This module defines comprehensive sinks for loading different types of
data into LDAP directories with enterprise features: Oracle compatibility,
transformation engine, validation, batch processing, error recovery.
"""

from __future__ import annotations

import logging
import operator
from typing import TYPE_CHECKING, Any

from singer_sdk.sinks import Sink

from target_ldap.client import LDAPClient
from target_ldap.transformation import DataTransformationEngine, MigrationValidator

if TYPE_CHECKING:
    from singer_sdk.target_base import Target


logger = logging.getLogger(__name__)


class LDAPSink(Sink):
    """Base class for LDAP sinks."""

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: list[str] | None,
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        self._client: LDAPClient | None = None
        self._transformation_engine: DataTransformationEngine | None = None
        self._validator: MigrationValidator | None = None
        self._processing_stats = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "transformed": 0,
            "validated": 0,
            "dry_run_simulated": 0,
            "batch_processed": 0,
            "oracle_entries": 0,
            "schema_errors": 0,
            "dependency_resolved": 0,
        }

        # Enterprise configuration
        self._enable_transformation = self.config.get("enable_transformation", False)
        self._enable_validation = self.config.get("enable_validation", True)
        self._dry_run_mode = self.config.get("dry_run_mode", False)
        self._batch_size = self.config.get("batch_size", 100)
        self._max_errors = self.config.get("max_errors", 10)
        self._oracle_oid_mode = self.config.get("oracle_oid_mode", False)
        self._merge_mode = self.config.get("merge_mode", "update")
        self._dependency_resolution = self.config.get("dependency_resolution", True)

        # Enterprise state tracking
        self._error_count = 0
        self._batch_buffer: list[dict[str, Any]] = []
        self._dependency_map: dict[str, list[str]] = {}
        self._failed_entries: list[dict[str, Any]] = []

    @property
    def client(self) -> LDAPClient:
        """Get LDAP client instance."""
        if self._client is None:
            config = self.config
            self._client = LDAPClient(
                host=config["host"],
                port=config.get("port", 389),
                bind_dn=config.get("bind_dn"),
                password=config.get("password"),
                use_ssl=config.get("use_ssl", False),
                timeout=config.get("timeout", 30),
            )
        return self._client

    @property
    def transformation_engine(self) -> DataTransformationEngine:
        """Get transformation engine instance."""
        if self._transformation_engine is None:
            config = dict(self.config)
            self._transformation_engine = DataTransformationEngine(config)
        return self._transformation_engine

    @property
    def validator(self) -> MigrationValidator:
        """Get migration validator instance."""
        if self._validator is None:
            config = dict(self.config)
            self._validator = MigrationValidator(config)
        return self._validator

    def get_dn_from_record(self, record: dict[str, Any]) -> str:
        """Extract DN from record.

        Args:
        ----
            record: Record data

        Returns:
        -------
            Distinguished name

        Raises:
        ------
            ValueError: If DN cannot be determined

        """
        # First, check if DN is explicitly provided
        if "dn" in record:
            return str(record["dn"])

        # Otherwise, try to construct DN from components
        dn_template = self.config.get(f"{self.stream_name}_dn_template")
        if dn_template and isinstance(dn_template, str):
            try:
                return str(dn_template.format(**record))
            except KeyError as e:
                msg = f"Missing required field for DN template: {e}"
                raise ValueError(msg) from e

        # Last resort: use RDN attribute + base DN
        rdn_attribute = self.get_rdn_attribute()
        if rdn_attribute and rdn_attribute in record:
            base_dn = self.config.get("base_dn", "")
            rdn_value = str(record[rdn_attribute])
            return f"{rdn_attribute}={rdn_value},{base_dn}"

        msg = "Cannot determine DN from record"
        raise ValueError(msg)

    def get_rdn_attribute(self) -> str:
        """Get the RDN attribute for this stream.

        Returns
        -------
            RDN attribute name

        """
        # Override in subclasses
        return "cn"

    def get_object_classes(self, record: dict[str, Any]) -> list[str]:
        """Get object classes for the record.

        Args:
        ----
            record: Record data

        Returns:
        -------
            List of object class names

        """
        # Check if objectClass is in the record
        if "objectClass" in record:
            obj_class = record["objectClass"]
            return obj_class if isinstance(obj_class, list) else [obj_class]

        # Return default object classes for the stream
        return self.get_default_object_classes()

    def get_default_object_classes(self) -> list[str]:
        """Get default object classes for this stream.

        Returns
        -------
            List of object class names

        """
        # Override in subclasses
        return ["top"]

    def prepare_attributes(self, record: dict[str, Any]) -> dict[str, Any]:
        """Prepare attributes for LDAP operation.

        Args:
        ----
            record: Record data

        Returns:
        -------
            Prepared attributes dict

        """
        # Remove special fields
        attributes = {
            k: v
            for k, v in record.items()
            if k not in {"dn", "objectClass", "_sdc_deleted_at"}
        }

        # Handle multi-valued attributes
        for key, value in attributes.items():
            if (
                isinstance(value, list)
                and len(value) == 1
                and key not in self.get_multi_valued_attributes()
            ):
                # Single-item lists can be flattened for some attributes
                attributes[key] = value[0]

        return attributes

    def get_multi_valued_attributes(self) -> set[str]:
        """Get set of multi-valued attributes.

        Returns
        -------
            Set of attribute names that should remain as lists

        """
        return {"member", "memberOf", "memberUid", "mail", "telephoneNumber"}

    def process_record(self, record: dict[str, Any], context: dict[str, Any]) -> None:
        """Process a single record with transformation and validation.

        Args:
        ----
            record: Record data
            context: Stream context

        """
        self._processing_stats["processed"] += 1

        try:
            # Check for deletion marker
            if record.get("_sdc_deleted_at"):
                self.process_delete(record)
                return

            # Apply data transformation if enabled
            working_record = record.copy()
            transformation_result = None

            if self.config.get("enable_transformation", False):
                transformation_result = self.transformation_engine.transform_entry(
                    working_record,
                )

                if transformation_result.success:
                    working_record = transformation_result.transformed_entry
                    if transformation_result.applied_rules:
                        self._processing_stats["transformed"] += 1
                        logger.info(
                            "Applied transformations to %s: %s",
                            working_record.get("dn", "unknown"),
                            transformation_result.applied_rules,
                        )
                else:
                    error_msg = f"Transformation failed: {transformation_result.errors}"
                    if not self.config.get("ignore_transformation_errors", True):
                        logger.error(error_msg)
                        raise ValueError(error_msg)
                    logger.warning(error_msg)

            # Validate entry if enabled
            validation_result = None
            if self.config.get("enable_validation", True):
                validation_result = self.validator.validate_entry(working_record)
                self._processing_stats["validated"] += 1

                if not validation_result["valid"]:
                    error_msg = (
                        f"Validation failed for {working_record.get('dn', 'unknown')}: "
                        f"{validation_result['errors']}"
                    )
                    if self.config.get("validation_strict_mode", False):
                        logger.error(error_msg)
                        raise ValueError(error_msg)
                    logger.warning(error_msg)

                if validation_result["warnings"]:
                    logger.info(
                        "Validation warnings for %s: %s",
                        working_record.get("dn", "unknown"),
                        validation_result["warnings"],
                    )

            # Handle dry run mode
            if self.config.get("dry_run_mode", False):
                self._process_dry_run(
                    working_record,
                    transformation_result,
                    validation_result,
                )
                return

            # Normal processing: extract DN, object classes, and attributes
            dn = self.get_dn_from_record(working_record)
            object_classes = self.get_object_classes(working_record)
            attributes = self.prepare_attributes(working_record)

            # Perform LDAP operation
            success, operation = self.client.upsert_entry(
                dn,
                object_classes,
                attributes,
            )

            if success:
                self._processing_stats["successful"] += 1
                logger.debug("Successfully performed %s for %s", operation, dn)

                # Log transformation/validation metadata
                if transformation_result and transformation_result.applied_rules:
                    logger.info(
                        "Entry %s processed with transformations: %s",
                        dn,
                        transformation_result.applied_rules,
                    )

            else:
                self._processing_stats["failed"] += 1
                logger.error("Failed to process record for %s", dn)

        except Exception as e:
            self._processing_stats["failed"] += 1
            logger.exception("Error processing record: %s", e)

            # Check if we should stop on errors
            if self._processing_stats["failed"] >= self.config.get("max_errors", 10):
                logger.exception("Maximum error count reached, stopping processing")
                raise

            # Re-raise if not ignoring errors
            if not self.config.get("ignore_transformation_errors", True):
                raise

    def _process_dry_run(
        self,
        record: dict[str, Any],
        transformation_result: dict[str, Any] | None = None,
        validation_result: dict[str, Any] | None = None,
    ) -> None:
        """Process entry in dry run mode (simulation only).

        Args:
        ----
            record: Record data
            transformation_result: Result of transformation
            validation_result: Result of validation

        """
        self._processing_stats["dry_run_simulated"] += 1

        dn = record.get("dn", "unknown")

        # Log what would be done
        logger.info("DRY RUN: Would process entry %s", dn)

        if (
            transformation_result
            and hasattr(transformation_result, "applied_rules")
            and transformation_result.applied_rules
        ):
            logger.info(
                "DRY RUN: Transformations that would be applied: %s",
                transformation_result.applied_rules,
            )

            # Log key changes
            if hasattr(transformation_result, "original_entry") and hasattr(
                transformation_result, "transformed_entry"
            ):
                original_dn = transformation_result.original_entry.get("dn")
                transformed_dn = transformation_result.transformed_entry.get("dn")
                if original_dn != transformed_dn:
                    logger.info(
                        "DRY RUN: DN would change from %s to %s",
                        original_dn,
                        transformed_dn,
                    )

        if validation_result:
            if validation_result["valid"]:
                logger.info("DRY RUN: Entry %s would pass validation", dn)
            else:
                logger.warning(
                    "DRY RUN: Entry %s would fail validation: %s",
                    dn,
                    validation_result["errors"],
                )

        # Simulate LDAP operation
        object_classes = self.get_object_classes(record)
        attributes = self.prepare_attributes(record)

        logger.info(
            "DRY RUN: Would upsert entry %s with object classes %s and %d attributes",
            dn,
            object_classes,
            len(attributes),
        )

    def get_processing_statistics(self) -> dict[str, Any]:
        """Get processing statistics for this sink.

        Returns
        -------
            Dictionary with processing statistics

        """
        stats = dict(self._processing_stats)

        # Add calculated metrics
        total = stats["processed"]
        if total > 0:
            stats["success_rate"] = (stats["successful"] / total) * 100
            stats["failure_rate"] = (stats["failed"] / total) * 100
            stats["transformation_rate"] = (stats["transformed"] / total) * 100
        else:
            stats["success_rate"] = 0
            stats["failure_rate"] = 0
            stats["transformation_rate"] = 0

        # Add engine statistics if available
        if self._transformation_engine:
            stats["transformation_engine"] = (
                self._transformation_engine.get_statistics()
            )

        if self._validator:
            stats["validation_engine"] = self._validator.get_validation_statistics()

        return stats

    def reset_statistics(self) -> None:
        """Reset processing statistics."""
        self._processing_stats = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "transformed": 0,
            "validated": 0,
            "dry_run_simulated": 0,
        }

        if self._transformation_engine:
            self._transformation_engine.reset_statistics()

        if self._validator:
            self._validator.validation_stats = {
                "total_validated": 0,
                "validation_passed": 0,
                "validation_failed": 0,
                "errors": [],
                "warnings": [],
            }

    def process_batch(
        self,
        records: list[dict[str, Any]],
        context: dict[str, Any],
    ) -> None:
        """Process records in batches for enterprise performance.

        Args:
        ----
            records: List of records to process
            context: Stream context

        """
        if not self._batch_size or len(records) <= 1:
            # Process individually if batch size not configured
            for record in records:
                self.process_record(record, context)
            return

        # Process in configured batch sizes
        for i in range(0, len(records), self._batch_size):
            batch = records[i : i + self._batch_size]
            self._process_enterprise_batch(batch, context)
            self._processing_stats["batch_processed"] += 1

    def _process_enterprise_batch(
        self,
        batch: list[dict[str, Any]],
        context: dict[str, Any],
    ) -> None:
        """Process a batch with enterprise features.

        Args:
        ----
            batch: Batch of records to process
            context: Stream context

        """
        if self._dependency_resolution:
            # Sort batch by dependency order
            batch = self._sort_by_dependencies(batch)

        # Process each record in the sorted batch
        for record in batch:
            try:
                if self._oracle_oid_mode:
                    record = self._process_oracle_compatibility(record)
                    self._processing_stats["oracle_entries"] += 1

                self.process_record(record, context)

            except Exception as e:
                self._error_count += 1
                self._failed_entries.append({"record": record, "error": str(e)})

                if self._error_count >= self._max_errors:
                    logger.exception(
                        "Maximum error threshold reached in batch processing",
                    )
                    raise

                logger.warning("Failed to process record in batch: %s", e)

    def _sort_by_dependencies(
        self,
        batch: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Sort batch by LDAP dependency order (parents before children).

        Args:
        ----
            batch: Unsorted batch of records

        Returns:
        -------
            Sorted batch with dependencies resolved

        """
        sorted_records: list[Any] = []
        remaining_records = batch.copy()

        # Extract DNs and build dependency map
        dn_to_record: dict[str, Any] = {}
        for record in batch:
            try:
                dn = self.get_dn_from_record(record)
                dn_to_record[dn] = record
            except ValueError:
                # If DN cannot be determined, process at the end
                sorted_records.append(record)
                if record in remaining_records:
                    remaining_records.remove(record)

        # Sort by DN depth (fewer commas = higher in hierarchy)
        dn_depth_pairs = [(dn, dn.count(",")) for dn in dn_to_record]
        dn_depth_pairs.sort(key=operator.itemgetter(1))  # Sort by depth (parents first)

        # Add records in dependency order
        for dn, _ in dn_depth_pairs:
            if dn in dn_to_record:
                sorted_records.append(dn_to_record[dn])
                self._processing_stats["dependency_resolved"] += 1

        return sorted_records

    def _process_oracle_compatibility(self, record: dict[str, Any]) -> dict[str, Any]:
        """Apply Oracle OID compatibility transformations.

        Args:
        ----
            record: Original record

        Returns:
        -------
            Record with Oracle compatibility applied

        """
        processed_record = record.copy()

        # Handle Oracle-specific object classes
        if "objectClass" in processed_record:
            obj_classes = processed_record["objectClass"]
            if isinstance(obj_classes, str):
                obj_classes = [obj_classes]

            # Convert orclContainer to organizationalUnit
            if "orclContainer" in obj_classes:
                if "organizationalUnit" not in obj_classes:
                    obj_classes.append("organizationalUnit")
                logger.debug("Added organizationalUnit for Oracle compatibility")

            processed_record["objectClass"] = obj_classes

        # Handle Oracle password attributes
        if "orclPassword" in processed_record:
            processed_record["userPassword"] = processed_record["orclPassword"]
            logger.debug("Converted orclPassword to userPassword")

        # Handle Oracle privilege groups
        if "orclPrivilegeGroup" in processed_record.get(
            "objectClass",
            [],
        ) and "groupOfNames" not in processed_record.get("objectClass", []):
            # Special handling for Oracle privilege groups
            processed_record["objectClass"].append("groupOfNames")

        return processed_record

    def get_failed_entries(self) -> list[dict[str, Any]]:
        """Get list of entries that failed processing.

        Returns
        -------
            List of failed entries with error information

        """
        return self._failed_entries.copy()

    def retry_failed_entries(self, context: dict[str, Any]) -> int:
        """Retry processing of failed entries.

        Args:
        ----
            context: Stream context

        Returns:
        -------
            Number of entries successfully retried

        """
        if not self._failed_entries:
            return 0

        retry_success_count = 0
        remaining_failures: list[Any] = []

        for failed_entry in self._failed_entries:
            try:
                record = failed_entry["record"]
                self.process_record(record, context)
                retry_success_count += 1
                logger.info("Successfully retried failed entry")

            except Exception as e:
                # Still failing, keep in failed list
                remaining_failures.append(
                    {
                        "record": failed_entry["record"],
                        "error": str(e),
                        "retry_attempted": True,
                    },
                )
                logger.warning("Retry failed for entry: %s", e)

        self._failed_entries = remaining_failures
        return retry_success_count

    def process_delete(self, record: dict[str, Any]) -> None:
        """Process record deletion (soft delete marker).

        Args:
        ----
            record: Record with deletion marker

        """
        try:
            dn = self.get_dn_from_record(record)

            if self._dry_run_mode:
                logger.info("DRY RUN: Would delete entry %s", dn)
                self._processing_stats["dry_run_simulated"] += 1
                return

            # Perform actual deletion
            success = self.client.delete_entry(dn)

            if success:
                self._processing_stats["successful"] += 1
                logger.info("Successfully deleted entry %s", dn)
            else:
                self._processing_stats["failed"] += 1
                logger.error("Failed to delete entry %s", dn)

        except Exception as e:
            self._processing_stats["failed"] += 1
            logger.exception("Error deleting record: %s", e)
            raise


class UsersSink(LDAPSink):
    """Sink for loading user entries into LDAP."""

    def get_rdn_attribute(self) -> str:
        """Get RDN attribute for users."""
        return self.config.get("user_rdn_attribute", "uid")

    def get_default_object_classes(self) -> list[str]:
        """Get default object classes for users."""
        return self.config.get(
            "user_object_classes",
            ["inetOrgPerson", "organizationalPerson", "person", "top"],
        )


class GroupsSink(LDAPSink):
    """Sink for group entries."""

    def get_rdn_attribute(self) -> str:
        """Get RDN attribute for groups."""
        return self.config.get("group_rdn_attribute", "cn")

    def get_default_object_classes(self) -> list[str]:
        """Get default object classes for groups."""
        return ["groupOfNames", "top"]

    def prepare_attributes(self, record: dict[str, Any]) -> dict[str, Any]:
        """Prepare group attributes, ensuring member attribute is present."""
        attributes = super().prepare_attributes(record)

        # groupOfNames requires at least one member
        if "member" not in attributes or not attributes["member"]:
            # Add a placeholder member if none exists
            attributes["member"] = [f"cn=placeholder,{self.config.get('base_dn', '')}"]

        return attributes


class OrganizationalUnitsSink(LDAPSink):
    """Sink for organizational unit entries."""

    def get_rdn_attribute(self) -> str:
        """Get RDN attribute for OUs."""
        return "ou"

    def get_default_object_classes(self) -> list[str]:
        """Get default object classes for OUs."""
        return ["organizationalUnit", "top"]


class GenericSink(LDAPSink):
    """Generic sink for any LDAP entries."""

    def get_rdn_attribute(self) -> str:
        """Get RDN attribute from config or default to cn."""
        return self.config.get(f"{self.stream_name}_rdn_attribute", "cn")

    def get_default_object_classes(self) -> list[str]:
        """Get default object classes from config."""
        return self.config.get(f"{self.stream_name}_object_classes", ["top"])
