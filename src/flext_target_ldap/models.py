"""FLEXT Target LDAP Models - Consolidated domain models following [Project]Models patterns.

This module implements the FlextTargetLdapModels class that extends FlextModels,
providing unified LDAP target domain models with nested classes for composition
and validation reuse. Follows the FLEXT ecosystem unified models standard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

from flext_core import FlextModels, FlextResult
from flext_core import t as t_core
from flext_core.utilities import u
from pydantic import Field, field_validator

from .constants import c


class FlextTargetLdapModels(FlextModels):
    """Unified LDAP target models extending FlextModels with nested domain classes.

    This class consolidates all LDAP target domain models using nested classes
    for composition and validation reuse, following the [Project]Models standard.
    Integrates with flext-core patterns for enterprise LDAP data loading.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextTargetLdapModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextTargetLdapModels is deprecated. Use FlextModels directly with composition instead.",
        )

    # ObjectClass moved to constants.py as c.TargetLdap.ObjectClass (DRY pattern)
    ObjectClass = c.TargetLdap.ObjectClass

    class TargetLdap:
        """TargetLdap domain namespace."""

        class AttributeMapping(FlextModels.Entity):
            """LDAP attribute mapping configuration with validation.

            Immutable value object defining how Singer fields map to LDAP attributes
            with business rule validation and transformation support.
            """

            singer_field_name: str = Field(
                ...,
                description="Singer field name from source data",
                min_length=1,
                max_length=255,
            )
            ldap_attribute_name: str = Field(
                ...,
                description="Target LDAP attribute name",
                min_length=1,
                max_length=255,
            )
            is_required: bool = Field(
                default=False,
                description="Whether this attribute is required for LDAP entry",
            )
            transformation_rule: str | None = Field(
                default=None,
                description="Optional transformation rule (e.g., 'lowercase', 'uppercase')",
                max_length=100,
            )
            default_value: str | None = Field(
                default=None,
                description="Default value if source field is missing",
                max_length=1000,
            )

            def validate_business_rules(self) -> FlextResult[bool]:
                """Validate attribute mapping business rules."""
                try:
                    # Validate field name format
                    if (
                        not self.singer_field_name.replace("_", "")
                        .replace("-", "")
                        .isalnum()
                    ):
                        return FlextResult[bool].fail(
                            "Singer field name must be alphanumeric with underscores/hyphens",
                        )

                    # Validate LDAP attribute format
                    if not self.ldap_attribute_name.replace("-", "").isalnum():
                        return FlextResult[bool].fail(
                            "LDAP attribute name must be alphanumeric with hyphens",
                        )

                    # Validate transformation rule
                    if self.transformation_rule:
                        valid_transformations = {
                            "lowercase",
                            "uppercase",
                            "trim",
                            "normalize",
                        }
                        if self.transformation_rule not in valid_transformations:
                            return FlextResult[bool].fail(
                                f"Invalid transformation rule. Must be one of {valid_transformations}",
                            )

                    return FlextResult[bool].ok(True)
                except Exception as e:
                    return FlextResult[bool].fail(
                        f"Attribute mapping validation failed: {e}",
                    )

        class Entry(FlextModels.Entity):
            """LDAP entry representation with validation and business rules.

            Immutable value object representing a complete LDAP entry with
            DN, object classes, and attributes, including validation rules.
            """

            distinguished_name: str = Field(
                ...,
                description="LDAP Distinguished Name (DN)",
                min_length=1,
                max_length=1000,
            )
            object_classes: list[str] = Field(
                default_factory=list,
                description="LDAP object classes",
            )
            attributes: dict[str, list[str]] = Field(
                default_factory=dict,
                description="LDAP attributes with values",
            )
            entry_type: str = Field(
                default="generic",
                description="Type of LDAP entry (user, group, ou, etc.)",
                max_length=50,
            )
            created_at: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="Entry creation timestamp",
            )

            @field_validator("object_classes")
            @classmethod
            def validate_object_classes(
                cls,
                v: list[str],
            ) -> list[str]:
                """Validate object classes contain 'top'."""
                if "top" not in v:
                    v.append("top")
                return v

            def validate_business_rules(self) -> FlextResult[bool]:
                """Validate LDAP entry business rules."""
                try:
                    errors: list[str] = []

                    # Validate DN format
                    if (
                        "=" not in self.distinguished_name
                        or "," not in self.distinguished_name
                    ):
                        errors.append(
                            "DN must contain attribute=value pairs separated by commas",
                        )

                    # Validate object classes
                    if not self.object_classes:
                        errors.append("Entry must have at least one object class")

                    # Validate person entries have required attributes
                    if "person" in self.object_classes:
                        required_attrs = {"sn", "cn"}
                        missing_attrs = required_attrs - set(self.attributes.keys())
                        if missing_attrs:
                            errors.append(
                                f"Person entries require attributes: {missing_attrs}",
                            )

                    # Validate group entries have required attributes
                    if "groupOfNames" in self.object_classes:
                        if "cn" not in self.attributes:
                            errors.append("Group entries require 'cn' attribute")
                        if "member" not in self.attributes:
                            errors.append(
                                "groupOfNames requires at least one 'member' attribute",
                            )

                    if errors:
                        return FlextResult[bool].fail("; ".join(errors))
                    return FlextResult[bool].ok(True)
                except Exception as e:
                    return FlextResult[bool].fail(f"LDAP entry validation failed: {e}")

            def get_rdn(self) -> str:
                """Get the Relative Distinguished Name (RDN) from the DN."""
                return self.distinguished_name.split(",")[0].strip()

            def get_parent_dn(self) -> str:
                """Get the parent DN by removing the RDN."""
                parts = self.distinguished_name.split(",", 1)
                return parts[1].strip() if len(parts) > 1 else ""

            def has_object_class(self, object_class: str) -> bool:
                """Check if entry has a specific object class."""
                return object_class.lower() in [
                    oc.lower() for oc in self.object_classes
                ]

            def get_attribute_values(
                self,
                attribute_name: str,
            ) -> list[str]:
                """Get values for a specific attribute."""
                return self.attributes.get(attribute_name, [])

        class TransformationResult(FlextModels.Entity):
            """Result of LDAP data transformation operations.

            Tracks transformation statistics, applied rules, and processing metrics
            for LDAP target operations.
            """

            original_record: dict[str, t_core.GeneralValueType] = Field(
                ...,
                description="Original Singer record before transformation",
            )
            transformed_entry: FlextTargetLdapModels.TargetLdap.Entry = Field(
                ...,
                description="Resulting LDAP entry after transformation",
            )
            applied_mappings: list[
                FlextTargetLdapModels.TargetLdap.AttributeMapping
            ] = Field(
                default_factory=list,
                description="Attribute mappings that were applied",
            )
            transformation_errors: list[str] = Field(
                default_factory=list,
                description="object errors encountered during transformation",
            )
            processing_time_ms: int = Field(
                default=0,
                description="Processing time in milliseconds",
                ge=0,
            )
            transformation_timestamp: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="When transformation was performed",
            )

            def validate_business_rules(self) -> FlextResult[bool]:
                """Validate transformation result business rules."""
                try:
                    # Validate we have meaningful data
                    if not self.original_record:
                        return FlextResult[bool].fail("Original record cannot be empty")

                    # Validate transformed entry is valid
                    entry_validation = self.transformed_entry.validate_business_rules()
                    if not entry_validation.is_success:
                        return FlextResult[bool].fail(
                            f"Transformed entry is invalid: {entry_validation.error}",
                        )

                    return FlextResult[bool].ok(True)
                except Exception as e:
                    return FlextResult[bool].fail(
                        f"Transformation result validation failed: {e}",
                    )

            @property
            def success_rate(self) -> float:
                """Calculate transformation success rate."""
                total_mappings = len(self.applied_mappings)
                if total_mappings == 0:
                    return 0.0

                error_count = len(self.transformation_errors)
                return ((total_mappings - error_count) / total_mappings) * 100.0

            def has_errors(self) -> bool:
                """Check if transformation has any errors."""
                return bool(self.transformation_errors)

        class BatchProcessing(FlextModels.Entity):
            """LDAP batch processing configuration and state tracking.

            Manages batching of LDAP operations for optimal performance,
            tracking batch size, processed records, and operation statistics.
            """

            stream_name: str = Field(
                ...,
                description="Singer stream being processed",
                min_length=1,
                max_length=255,
            )
            batch_size: int = Field(
                ...,
                description="Maximum records per batch",
                gt=0,
                le=10000,
            )
            current_batch: list[FlextTargetLdapModels.TargetLdap.Entry] = Field(
                default_factory=list,
                description="Current batch of LDAP entries",
            )
            total_processed: int = Field(
                default=0,
                description="Total entries processed across all batches",
                ge=0,
            )
            successful_operations: int = Field(
                default=0,
                description="Count of successful LDAP operations",
                ge=0,
            )
            failed_operations: int = Field(
                default=0,
                description="Count of failed LDAP operations",
                ge=0,
            )
            last_processed_at: datetime | None = Field(
                default=None,
                description="Timestamp of last batch processing",
            )

            def validate_business_rules(self) -> FlextResult[bool]:
                """Validate batch processing business rules."""
                try:
                    # Validate batch size doesn't exceed current batch
                    if len(self.current_batch) > self.batch_size:
                        return FlextResult[bool].fail(
                            f"Current batch size ({len(self.current_batch)}) exceeds maximum ({self.batch_size})",
                        )

                    # Validate counters are consistent
                    if (
                        self.successful_operations + self.failed_operations
                        > self.total_processed
                    ):
                        return FlextResult[bool].fail(
                            "Operation counters exceed total processed count",
                        )

                    return FlextResult[bool].ok(True)
                except Exception as e:
                    return FlextResult[bool].fail(
                        f"Batch processing validation failed: {e}",
                    )

            @property
            def is_batch_full(self) -> bool:
                """Check if current batch is full."""
                return len(self.current_batch) >= self.batch_size

            @property
            def current_batch_size(self) -> int:
                """Get current batch size."""
                return len(self.current_batch)

            @property
            def success_rate(self) -> float:
                """Calculate success rate percentage."""
                total_ops = self.successful_operations + self.failed_operations
                if total_ops == 0:
                    return 0.0
                return (self.successful_operations / total_ops) * 100.0

            def add_entry(
                self,
                entry: FlextTargetLdapModels.TargetLdap.Entry,
            ) -> Self:
                """Add entry to current batch (immutable operation)."""
                new_batch = self.current_batch.copy()
                new_batch.append(entry)

                return self.model_copy(
                    update={
                        "current_batch": new_batch,
                    },
                )

            def clear_batch(self) -> Self:
                """Clear current batch after processing (immutable operation)."""
                return self.model_copy(
                    update={
                        "current_batch": [],
                        "total_processed": self.total_processed
                        + len(self.current_batch),
                        "last_processed_at": datetime.now(UTC),
                    },
                )

            def record_success(self, count: int = 1) -> Self:
                """Record successful operations (immutable operation)."""
                return self.model_copy(
                    update={
                        "successful_operations": self.successful_operations + count,
                    },
                )

            def record_failure(self, count: int = 1) -> Self:
                """Record failed operations (immutable operation)."""
                return self.model_copy(
                    update={
                        "failed_operations": self.failed_operations + count,
                    },
                )

        class OperationStatistics(FlextModels.Entity):
            """LDAP operation statistics and performance metrics.

            Complete tracking of LDAP target operations for performance
            monitoring, reporting, and optimization analysis.
            """

            total_entries_processed: int = Field(
                default=0,
                description="Total LDAP entries processed",
                ge=0,
            )
            successful_adds: int = Field(
                default=0,
                description="Successful LDAP add operations",
                ge=0,
            )
            successful_updates: int = Field(
                default=0,
                description="Successful LDAP modify operations",
                ge=0,
            )
            successful_deletes: int = Field(
                default=0,
                description="Successful LDAP delete operations",
                ge=0,
            )
            failed_operations: int = Field(
                default=0,
                description="Total failed operations",
                ge=0,
            )
            average_processing_time_ms: float = Field(
                default=0.0,
                description="Average processing time per entry in milliseconds",
                ge=0.0,
            )
            start_time: datetime = Field(
                default_factory=lambda: datetime.now(UTC),
                description="When processing started",
            )
            end_time: datetime | None = Field(
                default=None,
                description="When processing completed",
            )

            def validate_business_rules(self) -> FlextResult[bool]:
                """Validate operation statistics business rules."""
                try:
                    # Validate that successful operations don't exceed total
                    total_successful = (
                        self.successful_adds
                        + self.successful_updates
                        + self.successful_deletes
                    )
                    if (
                        total_successful + self.failed_operations
                        > self.total_entries_processed
                    ):
                        return FlextResult[bool].fail(
                            "Total operations exceed total entries processed",
                        )

                    # Validate time range
                    if self.end_time and self.end_time < self.start_time:
                        return FlextResult[bool].fail(
                            "End time cannot be before start time",
                        )

                    return FlextResult[bool].ok(True)
                except Exception as e:
                    return FlextResult[bool].fail(
                        f"Operation statistics validation failed: {e}",
                    )

            @property
            def success_rate(self) -> float:
                """Calculate overall success rate percentage."""
                if self.total_entries_processed == 0:
                    return 0.0
                successful = (
                    self.successful_adds
                    + self.successful_updates
                    + self.successful_deletes
                )
                return (successful / self.total_entries_processed) * 100.0

            @property
            def total_duration_seconds(self) -> float:
                """Calculate total processing duration in seconds."""
                if not self.end_time:
                    return 0.0
                return (self.end_time - self.start_time).total_seconds()

            @property
            def operations_per_second(self) -> float:
                """Calculate operations per second throughput."""
                duration = self.total_duration_seconds
                if duration == 0.0:
                    return 0.0
                return self.total_entries_processed / duration

            def complete_processing(self) -> Self:
                """Mark processing as completed (immutable operation)."""
                return self.model_copy(
                    update={
                        "end_time": datetime.now(UTC),
                    },
                )


# Export the unified models class
m = FlextTargetLdapModels
m_target_ldap = FlextTargetLdapModels

__all__: list[str] = [
    "FlextTargetLdapModels",
    "m",
    "m_target_ldap",
]
