"""FLEXT Target LDAP Models - Consolidated domain models following [Project]Models patterns.

This module implements the FlextTargetLdapModels class that extends FlextModels,
providing unified LDAP target domain models with nested classes for composition
and validation reuse. Follows the FLEXT ecosystem unified models standard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
    MutableSequence,
)
from types import MappingProxyType
from typing import Annotated

from flext_ldap import m
from flext_meltano import FlextMeltanoModels
from flext_target_ldap import c, p, r, t, u


class FlextTargetLdapModels(FlextMeltanoModels, m):
    """Unified LDAP target models extending FlextModels with nested domain classes.

    This class consolidates all LDAP target domain models using nested classes
    for composition and validation reuse, following the [Project]Models standard.
    Integrates with flext-core patterns for enterprise LDAP data loading.
    """

    class TargetLdap:
        """TargetLdap domain namespace."""

        class AttributeMapping(m.Entity):
            """LDAP attribute mapping configuration with validation.

            Immutable value object defining how Singer fields map to LDAP attributes
            with business rule validation and transformation support.
            """

            singer_field_name: Annotated[
                t.NonEmptyStr,
                u.Field(
                    ...,
                    description="Singer field name from source data",
                ),
            ]
            ldap_attribute_name: Annotated[
                t.NonEmptyStr,
                u.Field(
                    ...,
                    description="Target LDAP attribute name",
                ),
            ]
            is_required: Annotated[
                bool,
                u.Field(
                    default=False,
                    description="Whether this attribute is required for LDAP entry",
                ),
            ]
            transformation_rule: Annotated[
                str | None,
                u.Field(
                    default=None,
                    description="Optional transformation rule (e.g., 'lowercase', 'uppercase')",
                ),
            ]
            default_value: Annotated[
                str | None,
                u.Field(
                    default=None,
                    description="Default value if source field is missing",
                ),
            ]

            def validate_business_rules(self) -> p.Result[bool]:
                """Validate attribute mapping business rules."""
                try:
                    # Validate field name format
                    if (
                        not self.singer_field_name
                        .replace("_", "")
                        .replace("-", "")
                        .isalnum()
                    ):
                        return r[bool].fail(
                            "Singer field name must be alphanumeric with underscores/hyphens",
                        )

                    # Validate LDAP attribute format
                    if not self.ldap_attribute_name.replace("-", "").isalnum():
                        return r[bool].fail(
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
                            return r[bool].fail(
                                f"Invalid transformation rule. Must be one of {valid_transformations}",
                            )

                    return r[bool].ok(value=True)
                except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                    return r[bool].fail_op("Attribute mapping validation", e)

        class Entry(m.Entity):
            """LDAP entry representation with validation and business rules.

            Immutable value object representing a complete LDAP entry with
            DN, object classes, and attributes, including validation rules.
            """

            distinguished_name: Annotated[
                t.NonEmptyStr,
                u.Field(
                    ...,
                    description="LDAP Distinguished Name (DN)",
                ),
            ]
            object_classes: Annotated[
                MutableSequence[str],
                u.Field(
                    description="LDAP object classes for this entry",
                    default_factory=list,
                ),
            ]
            attributes: Annotated[
                t.MutableStrSequenceMapping,
                u.Field(
                    description="LDAP attributes with values",
                    default_factory=lambda: MappingProxyType({}),
                ),
            ]
            entry_type: Annotated[
                str,
                u.Field(
                    default="generic",
                    description="Type of LDAP entry (user, group, ou, etc.)",
                ),
            ]

            @u.field_validator("object_classes")
            @classmethod
            def validate_object_classes(
                cls,
                v: MutableSequence[str],
            ) -> MutableSequence[str]:
                """Validate object classes contain 'top'."""
                if "top" not in v:
                    v.append("top")
                return v

            @u.computed_field(return_type=str)
            @property
            def parent_dn(self) -> str:
                """Parent DN derived from the distinguished name."""
                distinguished_name = self.distinguished_name
                parts = distinguished_name.split(",", 1)
                return parts[1].strip() if len(parts) > 1 else ""

            @u.computed_field(return_type=str)
            @property
            def rdn(self) -> str:
                """Relative distinguished name derived from the DN."""
                distinguished_name = self.distinguished_name
                return distinguished_name.split(",", 1)[0].strip()

            def has_object_class(self, object_class: str) -> bool:
                """Check if entry has a specific object class."""
                return u.Ldap.norm_in(object_class, self.object_classes)

            def validate_business_rules(self) -> p.Result[bool]:
                """Validate LDAP entry business rules."""
                try:
                    errors: MutableSequence[str] = []

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
                        errors.append(
                            "Entry must have at least one object class",
                        )

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
                        return r[bool].fail("; ".join(errors))
                    return r[bool].ok(value=True)
                except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                    return r[bool].fail_op("LDAP entry validation", e)

        class SingerPropertyDefinition(m.Value):
            """Singer property definition for LDAP schema mapping."""

            type: Annotated[
                str,
                u.Field(
                    default="string",
                    description="Singer property data type",
                ),
            ]
            format: Annotated[
                str | None,
                u.Field(
                    default=None,
                    description="Optional format qualifier for the property type",
                ),
            ]

        class SingerSchemaDefinition(m.Value):
            """Singer schema definition mapping properties to LDAP attributes."""

            properties: MutableMapping[
                str,
                FlextTargetLdapModels.TargetLdap.SingerPropertyDefinition,
            ] = u.Field(
                default_factory=dict,
                description="Mapping of property names to their Singer definitions",
            )

        class SingerLDAPCatalogEntry(m.Entity):
            """Singer LDAP catalog entry with stream metadata."""

            tap_stream_id: Annotated[
                t.NonEmptyStr,
                u.Field(
                    description="Unique identifier for the Singer tap stream",
                ),
            ]
            stream: Annotated[
                t.NonEmptyStr,
                u.Field(
                    description="Singer stream name for this catalog entry",
                ),
            ]
            stream_schema: Annotated[
                t.TargetLdap.MutableSchemaPayload,
                u.Field(
                    description="Schema definition for the Singer stream",
                    default_factory=lambda: MappingProxyType({}),
                ),
            ]

        class TransformationRule(m.Value):
            """Rule for transforming LDAP data with pattern matching and replacement."""

            name: Annotated[
                t.NonEmptyStr,
                u.Field(
                    description="Unique name identifying this transformation rule",
                ),
            ]
            pattern: Annotated[
                t.NonEmptyStr,
                u.Field(
                    description="Regex pattern to match in source data",
                ),
            ]
            replacement: Annotated[
                str,
                u.Field(
                    default="",
                    description="Replacement string applied when pattern matches",
                ),
            ]
            enabled: Annotated[
                bool,
                u.Field(
                    default=True,
                    description="Whether this transformation rule is active",
                ),
            ]

        class DataTransformationResult(m.Value):
            """Lightweight result of data transformation engine operations."""

            transformed_data: Annotated[
                t.TargetLdap.MutableRecordPayload,
                u.Field(
                    description="Data after applying transformation rules",
                    default_factory=lambda: MappingProxyType({}),
                ),
            ]
            applied_rules: Annotated[
                MutableSequence[str],
                u.Field(
                    description="Names of transformation rules that were applied",
                    default_factory=list,
                ),
            ]


m = FlextTargetLdapModels

__all__: list[str] = [
    "FlextTargetLdapModels",
    "m",
]
