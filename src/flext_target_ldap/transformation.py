"""Data transformation engine for LDAP target.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, override

from flext_core import FlextLogger, r, t
from pydantic import BaseModel, Field

logger = FlextLogger(__name__)


class TransformationRule(BaseModel):
    """Rule for transforming LDAP data with pattern matching and replacement."""

    name: Annotated[str, Field(min_length=1)]
    pattern: Annotated[str, Field(min_length=1)]
    replacement: str
    enabled: bool = True


class TransformationResult(BaseModel):
    """Result of data transformation with applied rules."""

    transformed_data: Annotated[
        dict[str, t.ContainerValue],
        Field(default_factory=dict),
    ]
    applied_rules: Annotated[list[str], Field(default_factory=list)]


class DataTransformationEngine:
    """Engine for transforming data using rules."""

    @override
    def __init__(self, rules: list[TransformationRule]) -> None:
        """Initialize transformation engine."""
        self.rules = rules

    def get_statistics(self) -> Mapping[str, int]:
        """Get transformation statistics."""
        return {"total_rules": len(self.rules), "transformations_applied": 0}

    def transform(self, data: dict[str, t.ContainerValue]) -> r[TransformationResult]:
        """Transform data using rules."""
        try:
            transformed_data: dict[str, t.ContainerValue] = data.copy()
            applied_rules: list[str] = []
            for rule in self.rules:
                if not rule.enabled:
                    continue
                for key, value in transformed_data.items():
                    match value:
                        case str() as text if rule.pattern in text:
                            transformed_data[key] = text.replace(
                                rule.pattern,
                                rule.replacement,
                            )
                            applied_rules.append(rule.name)
                        case _:
                            pass
            result = TransformationResult(
                transformed_data=transformed_data,
                applied_rules=applied_rules,
            )
            return r[TransformationResult].ok(result)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[TransformationResult].fail(f"Transformation failed: {e}")


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

    def get_validation_statistics(self) -> Mapping[str, int]:
        """Get validation statistics."""
        return self._stats.copy()

    def validate(
        self,
        data: dict[str, t.ContainerValue] | str,
        attributes: dict[str, t.ContainerValue] | None = None,
        object_classes: list[str] | None = None,
    ) -> r[bool]:
        """Validate migration data."""
        try:
            self._stats["entries_validated"] += 1
            error_msg = None
            match data:
                case str() as dn:
                    attrs = attributes or {}
                    obj_classes = object_classes or []
                    if not dn or not dn.strip():
                        error_msg = "DN cannot be empty or whitespace"
                    elif not obj_classes:
                        error_msg = "Object classes must be a non-empty list"
                    elif "person" in obj_classes and "sn" not in attrs:
                        self._stats["validation_warnings"] += 1
                        if self.strict_mode:
                            error_msg = "person object class requires 'sn' attribute"
                case _:
                    if not data:
                        error_msg = "Data is empty"
            if error_msg:
                self._stats["validation_errors"] += 1
                return r[bool].fail(error_msg)
            return r[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self._stats["validation_errors"] += 1
            return r[bool].fail(f"Validation failed: {e}")

    def validate_entry(
        self,
        dn: str,
        attributes: dict[str, t.ContainerValue],
        object_classes: list[str],
    ) -> r[bool]:
        """Validate individual LDAP entry - alias for validate method."""
        return self.validate(dn, attributes, object_classes)
