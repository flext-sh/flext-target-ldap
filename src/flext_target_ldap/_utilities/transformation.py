"""Data transformation engine for LDAP target.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import override

from flext_core import FlextLogger, r

from flext_target_ldap.models import m
from flext_target_ldap.typings import t

logger = FlextLogger(__name__)


class FlextTargetLdapTransformationEngine:
    """Engine for transforming data using rules."""

    @override
    def __init__(self, rules: Sequence[m.TargetLdap.TransformationRule]) -> None:
        """Initialize transformation engine."""
        self.rules = rules

    def get_statistics(self) -> Mapping[str, int]:
        """Get transformation statistics."""
        return {"total_rules": len(self.rules), "transformations_applied": 0}

    def transform(
        self,
        data: Mapping[str, t.ContainerValue],
    ) -> r[m.TargetLdap.DataTransformationResult]:
        """Transform data using rules."""
        try:
            transformed_data: MutableMapping[str, t.ContainerValue] = dict(data)
            applied_rules: MutableSequence[str] = []
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
                        case list() as items:
                            new_items: MutableSequence[t.ContainerValue] = []
                            matched = False
                            for item in items:
                                if isinstance(item, str) and rule.pattern in item:
                                    new_items.append(
                                        item.replace(rule.pattern, rule.replacement),
                                    )
                                    matched = True
                                else:
                                    new_items.append(item)
                            if matched:
                                transformed_data[key] = new_items
                                applied_rules.append(rule.name)
                        case _:
                            pass
            result = m.TargetLdap.DataTransformationResult(
                transformed_data=transformed_data,
                applied_rules=applied_rules,
            )
            return r[m.TargetLdap.DataTransformationResult].ok(result)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[m.TargetLdap.DataTransformationResult].fail(
                f"Transformation failed: {e}",
            )


class FlextTargetLdapMigrationValidator:
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
        data: Mapping[str, t.ContainerValue] | str,
        attributes: Mapping[str, t.ContainerValue] | None = None,
        object_classes: Sequence[t.ContainerValue] | None = None,
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
                            error_msg = (
                                "person t.NormalizedValue class requires 'sn' attribute"
                            )
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
        attributes: Mapping[str, t.ContainerValue],
        object_classes: t.StrSequence,
    ) -> r[bool]:
        """Validate individual LDAP entry - alias for validate method."""
        return self.validate(dn, attributes, object_classes)


__all__: t.StrSequence = [
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapTransformationEngine",
]
