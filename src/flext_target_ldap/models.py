"""FLEXT Target LDAP Models - Consolidated domain models following [Project]Models patterns.

This module implements the FlextTargetLdapModels class that extends FlextModels,
providing unified LDAP target domain models with nested classes for composition
and validation reuse. Follows the FLEXT ecosystem unified models standard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Annotated

from flext_ldap import m
from flext_meltano import FlextMeltanoModels
from flext_target_ldap import t, u

if TYPE_CHECKING:
    from collections.abc import MutableSequence


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
                u.Field(..., description="Singer field name from source data"),
            ]
            ldap_attribute_name: Annotated[
                t.NonEmptyStr, u.Field(..., description="Target LDAP attribute name")
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
                    default=None, description="Default value if source field is missing"
                ),
            ]

        class Entry(m.Entity):
            """LDAP entry representation with validation and business rules.

            Immutable value object representing a complete LDAP entry with
            DN, object classes, and attributes, including validation rules.
            """

            distinguished_name: Annotated[
                t.NonEmptyStr, u.Field(..., description="LDAP Distinguished Name (DN)")
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
                cls, v: MutableSequence[str]
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
                rdn_part: str = distinguished_name.split(",", 1)[0].strip()
                return rdn_part

            def has_object_class(self, object_class: str) -> bool:
                """Check if entry has a specific object class."""
                present: bool = u.Ldap.norm_in(object_class, self.object_classes)
                return present

        class TransformationRule(m.Value):
            """Rule for transforming LDAP data with pattern matching and replacement."""

            name: Annotated[
                t.NonEmptyStr,
                u.Field(description="Unique name identifying this transformation rule"),
            ]
            pattern: Annotated[
                t.NonEmptyStr,
                u.Field(description="Regex pattern to match in source data"),
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


m = FlextTargetLdapModels

__all__: list[str] = ["FlextTargetLdapModels", "m"]
