"""LDAP Target Models - PEP8 Consolidation.

This module consolidates LDAP target domain models with descriptive PEP8 names,
providing enterprise-grade data models for LDAP operations and transformations.

**Architecture**: Clean Architecture domain layer
**Patterns**: FlextValueObject, business rule validation
**Integration**: Complete LDAP-specific transformations and processing models

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from flext_core import FlextResult, FlextValueObject
from pydantic import Field, validator


class LdapObjectClassModel(StrEnum):
    """Standard LDAP object classes for target operations.

    Defines the common object classes used in enterprise LDAP directories
    for users, groups, and organizational structures.
    """

    # Base object classes
    TOP = "top"

    # Person object classes
    PERSON = "person"
    ORGANIZATIONAL_PERSON = "organizationalPerson"
    INET_ORG_PERSON = "inetOrgPerson"

    # Group object classes
    GROUP_OF_NAMES = "groupOfNames"
    GROUP_OF_UNIQUE_NAMES = "groupOfUniqueNames"
    POSIX_GROUP = "posixGroup"

    # Organizational object classes
    ORGANIZATION = "organization"
    ORGANIZATIONAL_UNIT = "organizationalUnit"
    ORGANIZATIONAL_ROLE = "organizationalRole"

    # System object classes
    DOMAIN = "domain"
    DOMAIN_COMPONENT = "dcObject"


class LdapAttributeMappingModel(FlextValueObject):
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate attribute mapping business rules."""
        try:
            # Validate field name format
            if not self.singer_field_name.replace("_", "").replace("-", "").isalnum():
                return FlextResult[None].fail(
                    "Singer field name must be alphanumeric with underscores/hyphens",
                )

            # Validate LDAP attribute format
            if not self.ldap_attribute_name.replace("-", "").isalnum():
                return FlextResult[None].fail(
                    "LDAP attribute name must be alphanumeric with hyphens",
                )

            # Validate transformation rule
            if self.transformation_rule:
                valid_transformations = {"lowercase", "uppercase", "trim", "normalize"}
                if self.transformation_rule not in valid_transformations:
                    return FlextResult[None].fail(
                        f"Invalid transformation rule. Must be one of {valid_transformations}",
                    )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Attribute mapping validation failed: {e}")


class LdapEntryModel(FlextValueObject):
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

    @validator("object_classes")
    @classmethod
    def validate_object_classes(cls, v: list[str]) -> list[str]:
        """Validate object classes contain 'top'."""
        if "top" not in v:
            v.append("top")
        return v

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate LDAP entry business rules."""
        try:
            errors: list[str] = []

            # Validate DN format
            if "=" not in self.distinguished_name or "," not in self.distinguished_name:
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
                return FlextResult[None].fail("; ".join(errors))
            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"LDAP entry validation failed: {e}")

    def get_rdn(self) -> str:
        """Get the Relative Distinguished Name (RDN) from the DN."""
        return self.distinguished_name.split(",")[0].strip()

    def get_parent_dn(self) -> str:
        """Get the parent DN by removing the RDN."""
        parts = self.distinguished_name.split(",", 1)
        return parts[1].strip() if len(parts) > 1 else ""

    def has_object_class(self, object_class: str) -> bool:
        """Check if entry has a specific object class."""
        return object_class.lower() in [oc.lower() for oc in self.object_classes]

    def get_attribute_values(self, attribute_name: str) -> list[str]:
        """Get values for a specific attribute."""
        return self.attributes.get(attribute_name, [])


class LdapTransformationResultModel(FlextValueObject):
    """Result of LDAP data transformation operations.

    Tracks transformation statistics, applied rules, and processing metrics
    for LDAP target operations.
    """

    original_record: dict[str, object] = Field(
        ...,
        description="Original Singer record before transformation",
    )
    transformed_entry: LdapEntryModel = Field(
        ...,
        description="Resulting LDAP entry after transformation",
    )
    applied_mappings: list[LdapAttributeMappingModel] = Field(
        default_factory=list,
        description="Attribute mappings that were applied",
    )
    transformation_errors: list[str] = Field(
        default_factory=list,
        description="Any errors encountered during transformation",
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate transformation result business rules."""
        try:
            # Validate we have meaningful data
            if not self.original_record:
                return FlextResult[None].fail("Original record cannot be empty")

            # Validate transformed entry is valid
            entry_validation = self.transformed_entry.validate_business_rules()
            if not entry_validation.is_success:
                return FlextResult[None].fail(
                    f"Transformed entry is invalid: {entry_validation.error}",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(
                f"Transformation result validation failed: {e}"
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


class LdapBatchProcessingModel(FlextValueObject):
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
    current_batch: list[LdapEntryModel] = Field(
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

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate batch processing business rules."""
        try:
            # Validate batch size doesn't exceed current batch
            if len(self.current_batch) > self.batch_size:
                return FlextResult[None].fail(
                    f"Current batch size ({len(self.current_batch)}) exceeds maximum ({self.batch_size})",
                )

            # Validate counters are consistent
            if (
                self.successful_operations + self.failed_operations
                > self.total_processed
            ):
                return FlextResult[None].fail(
                    "Operation counters exceed total processed count",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Batch processing validation failed: {e}")

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

    def add_entry(self, entry: LdapEntryModel) -> LdapBatchProcessingModel:
        """Add entry to current batch (immutable operation)."""
        new_batch = self.current_batch.copy()
        new_batch.append(entry)

        return self.model_copy(
            update={
                "current_batch": new_batch,
            },
        )

    def clear_batch(self) -> LdapBatchProcessingModel:
        """Clear current batch after processing (immutable operation)."""
        return self.model_copy(
            update={
                "current_batch": [],
                "total_processed": self.total_processed + len(self.current_batch),
                "last_processed_at": datetime.now(UTC),
            },
        )

    def record_success(self, count: int = 1) -> LdapBatchProcessingModel:
        """Record successful operations (immutable operation)."""
        return self.model_copy(
            update={
                "successful_operations": self.successful_operations + count,
            },
        )

    def record_failure(self, count: int = 1) -> LdapBatchProcessingModel:
        """Record failed operations (immutable operation)."""
        return self.model_copy(
            update={
                "failed_operations": self.failed_operations + count,
            },
        )


class LdapOperationStatisticsModel(FlextValueObject):
    """Statistics tracking for LDAP target operations.

    Comprehensive metrics and performance data for LDAP operations,
    including timing, success rates, and error tracking.
    """

    operation_type: str = Field(
        ...,
        description="Type of LDAP operation (add, modify, delete, search)",
        min_length=1,
        max_length=50,
    )
    total_operations: int = Field(
        default=0,
        description="Total operations attempted",
        ge=0,
    )
    successful_operations: int = Field(
        default=0,
        description="Successful operations",
        ge=0,
    )
    failed_operations: int = Field(
        default=0,
        description="Failed operations",
        ge=0,
    )
    average_duration_ms: float = Field(
        default=0.0,
        description="Average operation duration in milliseconds",
        ge=0.0,
    )
    total_duration_ms: float = Field(
        default=0.0,
        description="Total duration of all operations in milliseconds",
        ge=0.0,
    )
    error_messages: list[str] = Field(
        default_factory=list,
        description="Collected error messages",
    )
    last_operation_at: datetime | None = Field(
        default=None,
        description="Timestamp of last operation",
    )
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When statistics collection started",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate operation statistics business rules."""
        try:
            # Validate operation counts are consistent
            if (
                self.successful_operations + self.failed_operations
                != self.total_operations
            ):
                return FlextResult[None].fail(
                    "Success + failed operations must equal total operations",
                )

            # Validate timing calculations
            if (
                self.total_operations > 0
                and self.average_duration_ms == 0
                and self.total_duration_ms > 0
            ):
                # Recalculate average if missing
                calculated_avg = self.total_duration_ms / self.total_operations
                return FlextResult[None].fail(
                    f"Average duration mismatch. Should be {calculated_avg:.2f}ms",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Statistics validation failed: {e}")

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.successful_operations / self.total_operations) * 100.0

    @property
    def failure_rate(self) -> float:
        """Calculate failure rate percentage."""
        return 100.0 - self.success_rate

    @property
    def operations_per_second(self) -> float:
        """Calculate operations per second."""
        if self.total_duration_ms == 0:
            return 0.0
        return (self.total_operations * 1000.0) / self.total_duration_ms

    def record_operation(
        self,
        duration_ms: float,
        *,
        success: bool,
        error_message: str | None = None,
    ) -> LdapOperationStatisticsModel:
        """Record a new operation result (immutable operation)."""
        new_total = self.total_operations + 1
        new_total_duration = self.total_duration_ms + duration_ms
        new_avg_duration = new_total_duration / new_total

        updates = {
            "total_operations": new_total,
            "total_duration_ms": new_total_duration,
            "average_duration_ms": new_avg_duration,
            "last_operation_at": datetime.now(UTC),
        }

        if success:
            updates["successful_operations"] = self.successful_operations + 1
        else:
            updates["failed_operations"] = self.failed_operations + 1
            if error_message:
                new_errors = self.error_messages.copy()
                new_errors.append(error_message)
                updates["error_messages"] = new_errors

        return self.model_copy(update=updates)

    def get_recent_errors(self, limit: int = 10) -> list[str]:
        """Get most recent error messages."""
        return self.error_messages[-limit:] if self.error_messages else []


# Backward compatibility aliases
TransformationRule = LdapAttributeMappingModel
TransformationResult = LdapTransformationResultModel
LDAPProcessingResult = LdapBatchProcessingModel

__all__ = [
    "LDAPProcessingResult",
    # Core models
    "LdapAttributeMappingModel",
    "LdapBatchProcessingModel",
    "LdapEntryModel",
    "LdapObjectClassModel",
    "LdapOperationStatisticsModel",
    "LdapTransformationResultModel",
    "TransformationResult",
    # Backward compatibility
    "TransformationRule",
]
