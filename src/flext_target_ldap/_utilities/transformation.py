"""Data transformation engine for LDAP target.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)
from typing import override

from flext_meltano import u

from flext_target_ldap import c, m, p, r, t

logger = u.fetch_logger(__name__)


class FlextTargetLdapTransformationEngine:
    """Engine for transforming data using rules."""

    @override
    def __init__(self, rules: Sequence[m.TargetLdap.TransformationRule]) -> None:
        """Initialize transformation engine."""
        self.rules = rules

    def get_statistics(self) -> t.IntMapping:
        """Get transformation statistics."""
        return {"total_rules": len(self.rules), "transformations_applied": 0}

    def transform(
        self,
        data: t.TargetLdap.RecordPayload,
    ) -> p.Result[m.TargetLdap.DataTransformationResult]:
        """Transform data using rules."""
        try:
            transformed_data: t.TargetLdap.MutableRecordPayload = {
                str(key): value for key, value in data.items()
            }
            applied_rules: MutableSequence[str] = []
            for rule in self.rules:
                if not rule.enabled:
                    continue
                for key, value in list(transformed_data.items()):
                    match value:
                        case str() as text if rule.pattern in text:
                            transformed_data[key] = text.replace(
                                rule.pattern,
                                rule.replacement,
                            )
                            applied_rules.append(rule.name)
                        case list() as items:
                            new_items: list[t.JsonValue] = []
                            matched = False
                            for item in items:
                                if isinstance(item, str) and rule.pattern in item:
                                    new_items.append(
                                        item.replace(rule.pattern, rule.replacement),
                                    )
                                    matched = True
                                else:
                                    new_items.append(u.Cli.normalize_json_value(item))
                            if matched:
                                transformed_data[key] = new_items
                                applied_rules.append(rule.name)
                        case _:
                            pass
            result = m.TargetLdap.DataTransformationResult.model_validate({
                "transformed_data": transformed_data,
                "applied_rules": list(applied_rules),
            })
            return r[m.TargetLdap.DataTransformationResult].ok(result)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
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

    def get_validation_statistics(self) -> t.IntMapping:
        """Get validation statistics."""
        return self._stats.copy()

    def validate(
        self,
        data: t.TargetLdap.RecordPayload | str,
        attributes: t.TargetLdap.RecordPayload | None = None,
        object_classes: t.StrSequence | None = None,
    ) -> p.Result[bool]:
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
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self._stats["validation_errors"] += 1
            return r[bool].fail(f"Validation failed: {e}")

    def validate_entry(
        self,
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence,
    ) -> p.Result[bool]:
        """Validate individual LDAP entry - alias for validate method."""
        attributes_payload: t.TargetLdap.MutableRecordPayload = {}
        for key, value in attributes.items():
            value_list: list[t.JsonValue] = [str(v) for v in value]
            attributes_payload[str(key)] = value_list
        return self.validate(dn, attributes_payload, object_classes)


__all__: t.StrSequence = [
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapTransformationEngine",
]
