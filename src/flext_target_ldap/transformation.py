"""Data transformation engine for target-ldap using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Simplified transformation capabilities for LDAP data processing with enterprise features.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from flext_core.domain.pydantic_base import DomainBaseModel
from flext_core.domain.pydantic_base import DomainValueObject
from flext_target_ldap.client import ServiceResult

logger = logging.getLogger(__name__)


class TransformationRule(DomainValueObject):
    """Represents a data transformation rule using flext-core patterns."""

    name: str
    pattern: str
    replacement: str
    enabled: bool = True

    def apply(self, value: str) -> ServiceResult[str]:
        """Apply the transformation rule to a value."""
        try:
            if not self.enabled:
                return ServiceResult.ok(value)

            # Apply regex transformation
            result = re.sub(self.pattern, self.replacement, value)
            return ServiceResult.ok(result)
        except Exception as e:
            error_msg = f"Error applying transformation rule '{self.name}': {e}"
            return ServiceResult.fail(error_msg)


class TransformationResult(DomainBaseModel):
    """Result of data transformation operations using flext-core patterns."""

    original_data: dict[str, Any]
    transformed_data: dict[str, Any]
    applied_rules: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)

    def add_applied_rule(self, rule_name: str) -> None:
        """Record that a rule was applied."""
        self.applied_rules.append(rule_name)

    @property
    def is_successful(self) -> bool:
        """Check if transformation was successful."""
        return len(self.errors) == 0

    @property
    def has_warnings(self) -> bool:
        """Check if transformation has warnings."""
        return len(self.warnings) > 0


class DataTransformationEngine:
    """Enterprise data transformation engine using flext-core patterns."""

    def __init__(self, rules: list[TransformationRule] | None = None) -> None:
        self.rules = rules or []
        self._stats = {
            "transformations_applied": 0,
            "rules_executed": 0,
            "warnings_generated": 0,
            "errors_encountered": 0,
        }

    def add_rule(self, rule: TransformationRule) -> None:
        """Add a transformation rule."""
        self.rules.append(rule)

    def transform_data(
        self, data: dict[str, Any]
    ) -> ServiceResult[TransformationResult]:
        """Transform data using configured rules."""
        try:
            result = TransformationResult(
                original_data=data.copy(),
                transformed_data=data.copy(),
            )

            # Apply transformation rules
            for rule in self.rules:
                if not rule.enabled:
                    continue

                # Apply rule to all string values in the data
                for key, value in result.transformed_data.items():
                    if isinstance(value, str):
                        transform_result = rule.apply(value)
                        if transform_result.is_success:
                            if transform_result.value != value:
                                result.transformed_data[key] = transform_result.value
                                result.add_applied_rule(rule.name)
                                self._stats["transformations_applied"] += 1
                        else:
                            result.add_error(
                                f"Rule '{rule.name}' failed for key '{key}': {transform_result.error}"
                            )
                            self._stats["errors_encountered"] += 1

                    elif isinstance(value, list):
                        # Apply rule to list items
                        transformed_list = []
                        for item in value:
                            if isinstance(item, str):
                                transform_result = rule.apply(item)
                                if transform_result.is_success:
                                    transformed_list.append(transform_result.value)
                                    if transform_result.value != item:
                                        result.add_applied_rule(rule.name)
                                        self._stats["transformations_applied"] += 1
                                else:
                                    result.add_error(
                                        f"Rule '{rule.name}' failed for list item: {transform_result.error}"
                                    )
                                    self._stats["errors_encountered"] += 1
                                    transformed_list.append(
                                        item
                                    )  # Keep original on error
                            else:
                                transformed_list.append(item)
                        result.transformed_data[key] = transformed_list

                self._stats["rules_executed"] += 1

            return ServiceResult.ok(result)

        except Exception as e:
            error_msg = f"Data transformation failed: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def get_statistics(self) -> dict[str, Any]:
        """Get transformation engine statistics."""
        return self._stats.copy()

    def reset_statistics(self) -> None:
        """Reset transformation statistics."""
        self._stats = {
            "transformations_applied": 0,
            "rules_executed": 0,
            "warnings_generated": 0,
            "errors_encountered": 0,
        }


class MigrationValidator:
    """Enterprise migration validator using flext-core patterns."""

    def __init__(self, strict_mode: bool = False) -> None:
        self.strict_mode = strict_mode
        self._validation_stats = {
            "entries_validated": 0,
            "validation_errors": 0,
            "validation_warnings": 0,
        }

    def validate_entry(
        self, dn: str, attributes: dict[str, Any], object_classes: list[str]
    ) -> ServiceResult[bool]:
        """Validate an LDAP entry before processing."""
        try:
            errors = []
            warnings = []

            # Basic DN validation
            if not dn or not isinstance(dn, str):
                errors.append("DN must be a non-empty string")

            if not dn.strip():
                errors.append("DN cannot be empty or whitespace")

            # Basic attributes validation
            if not attributes or not isinstance(attributes, dict):
                errors.append("Attributes must be a non-empty dictionary")

            # Object classes validation
            if not object_classes or not isinstance(object_classes, list):
                errors.append("Object classes must be a non-empty list")

            # Check for required attributes based on object classes
            if "inetOrgPerson" in object_classes:
                if "cn" not in attributes and "sn" not in attributes:
                    if self.strict_mode:
                        errors.append(
                            "inetOrgPerson requires either 'cn' or 'sn' attribute"
                        )
                    else:
                        warnings.append(
                            "inetOrgPerson should have 'cn' or 'sn' attribute"
                        )

            if "groupOfNames" in object_classes and "cn" not in attributes:
                if self.strict_mode:
                    errors.append("groupOfNames requires 'cn' attribute")
                else:
                    warnings.append("groupOfNames should have 'cn' attribute")

            # Update statistics
            self._validation_stats["entries_validated"] += 1
            self._validation_stats["validation_errors"] += len(errors)
            self._validation_stats["validation_warnings"] += len(warnings)

            if errors:
                error_msg = "; ".join(errors)
                return ServiceResult.fail(f"Validation failed: {error_msg}")

            if warnings:
                logger.warning(
                    "Validation warnings for %s: %s", dn, "; ".join(warnings)
                )

            return ServiceResult.ok(True)

        except Exception as e:
            error_msg = f"Validation error for {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def get_validation_statistics(self) -> dict[str, Any]:
        """Get validation statistics."""
        return self._validation_stats.copy()

    def reset_validation_statistics(self) -> None:
        """Reset validation statistics."""
        self._validation_stats = {
            "entries_validated": 0,
            "validation_errors": 0,
            "validation_warnings": 0,
        }


# Factory functions for common transformation scenarios
def create_oracle_to_ldap_transformation_rules() -> list[TransformationRule]:
    """Create transformation rules for Oracle to LDAP migration."""
    return [
        TransformationRule(
            name="normalize_email",
            pattern=r"([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})",
            replacement=r"\1@\2",
            enabled=True,
        ),
        TransformationRule(
            name="clean_phone_numbers",
            pattern=r"[^\d+\-\(\)\s]",
            replacement="",
            enabled=True,
        ),
        TransformationRule(
            name="normalize_whitespace",
            pattern=r"\s+",
            replacement=" ",
            enabled=True,
        ),
    ]


def create_development_transformation_engine() -> DataTransformationEngine:
    """Create a transformation engine with development-friendly rules."""
    rules = create_oracle_to_ldap_transformation_rules()
    return DataTransformationEngine(rules)


def create_production_transformation_engine() -> DataTransformationEngine:
    """Create a transformation engine with production-ready rules."""
    rules = create_oracle_to_ldap_transformation_rules()
    # Add more strict rules for production
    rules.extend(
        [
            TransformationRule(
                name="strip_sql_injection",
                pattern=r"[';\"\\]",
                replacement="",
                enabled=True,
            ),
        ]
    )
    return DataTransformationEngine(rules)


# Export main classes and functions
__all__ = [
    "DataTransformationEngine",
    "MigrationValidator",
    "TransformationResult",
    "TransformationRule",
    "create_development_transformation_engine",
    "create_oracle_to_ldap_transformation_rules",
    "create_production_transformation_engine",
]
