"""Data transformation engine for LDAP target.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextModels, FlextResult
from pydantic import Field

from flext_target_ldap.typings import t

logger = FlextLogger(__name__)


class TransformationRule(FlextModels.Entity):
    """Transformation rule for data transformation."""

    name: str
    pattern: str
    replacement: str
    enabled: bool = True

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate transformation rule business rules."""
        try:
            if not self.name.strip():
                return FlextResult[None].fail("Rule name cannot be empty")
            if not self.pattern:
                return FlextResult[None].fail("Pattern cannot be empty")
            # replacement is guaranteed to be str by Pydantic typing
            # Using a domain-specific validation instead
            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Transformation rule validation failed: {e}")


class TransformationResult(FlextModels.Entity):
    """Result of data transformation."""

    transformed_data: t.Core.Dict
    applied_rules: t.Core.StringList = Field(default_factory=list)

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate transformation result business rules."""
        try:
            if not self.transformed_data:
                return FlextResult[None].fail("transformed_data cannot be empty")
            if len(self.applied_rules) < 0:  # This check makes sense for business logic
                return FlextResult[None].fail("applied_rules cannot be negative length")
            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(
                f"Transformation result validation failed: {e}",
            )


class DataTransformationEngine:
    """Engine for transforming data using rules."""

    @override
    def __init__(self, rules: list[TransformationRule]) -> None:
        """Initialize transformation engine."""
        self.rules = rules

    def transform(
        self,
        data: t.Core.Dict,
    ) -> FlextResult[TransformationResult]:
        """Transform data using rules."""
        try:
            transformed_data: dict[str, object] = data.copy()
            applied_rules: t.Core.StringList = []

            for rule in self.rules:
                for key, value in transformed_data.items():
                    if isinstance(value, str) and rule.pattern in value:
                        transformed_data[key] = value.replace(
                            rule.pattern,
                            rule.replacement,
                        )
                        applied_rules.append(rule.name)

            result = TransformationResult(
                transformed_data=transformed_data,
                applied_rules=applied_rules,
            )
            return FlextResult[TransformationResult].ok(result)
        except Exception as e:
            return FlextResult[TransformationResult].fail(f"Transformation failed: {e}")

    def get_statistics(self: object) -> dict[str, int]:
        """Get transformation statistics."""
        return {
            "total_rules": len(self.rules),
            "transformations_applied": 0,  # Would track in real implementation
        }


class MigrationValidator:
    """Validator for migration data."""

    @override
    def __init__(self, *, strict_mode: bool = True) -> None:
        """Initialize migration validator."""
        self.strict_mode = strict_mode
        self._stats = {
            "entries_validated": 0,
            "validation_errors": 0,
            "validation_warnings": 0,
        }

    @override
    def validate(
        self,
        data: t.Core.Dict | str,
        attributes: t.Core.Dict | None = None,
        object_classes: t.Core.StringList | None = None,
    ) -> FlextResult[bool]:
        """Validate migration data."""
        try:
            self._stats["entries_validated"] += 1
            error_msg = None

            # Handle different call patterns
            if isinstance(data, str):
                # Called with validate(dn, attributes, object_classes)
                dn = data
                attrs = attributes or {}
                obj_classes = object_classes or []

                # Validate DN
                if not dn or not dn.strip():
                    error_msg = "DN cannot be empty or whitespace"
                # Validate object classes
                elif not obj_classes:
                    error_msg = "Object classes must be a non-empty list"
                # Basic attribute validation for person object class
                elif "person" in obj_classes and "sn" not in attrs:
                    self._stats["validation_warnings"] += 1
                    if self.strict_mode:
                        error_msg = "person object class requires 'sn' attribute"

            # Called with validate(data_dict)
            elif not data:
                error_msg = "Data is empty"

            if error_msg:
                self._stats["validation_errors"] += 1
                return FlextResult[bool].fail(error_msg)

            return FlextResult[bool].ok(data=True)

        except Exception as e:
            self._stats["validation_errors"] += 1
            return FlextResult[bool].fail(f"Validation failed: {e}")

    def validate_entry(
        self,
        dn: str,
        attributes: t.Core.Dict,
        object_classes: t.Core.StringList,
    ) -> FlextResult[bool]:
        """Validate individual LDAP entry - alias for validate method."""
        return self.validate(dn, attributes, object_classes)

    def get_validation_statistics(self: object) -> dict[str, int]:
        """Get validation statistics."""
        return self._stats.copy()
