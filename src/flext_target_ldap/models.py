"""FLEXT Target LDAP Models - Consolidated domain models following Models patterns.

This module implements the FlextTargetLdapModels class that extends FlextModels,
providing unified LDAP target domain models with nested classes for composition
and validation reuse. Follows the FLEXT ecosystem unified models standard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_ldap import FlextLdapModels
from flext_meltano import FlextMeltanoModels

from flext_target_ldap import t
from flext_target_ldap._models.config import FlextTargetLdapConfigModels
from flext_target_ldap._models.processing_result import (
    FlextTargetLdapProcessingCounters,
)
from flext_target_ldap._models.sinks import FlextTargetLdapModelsSinks


class FlextTargetLdapModels(FlextMeltanoModels, FlextLdapModels):
    """Unified LDAP target models extending FlextModels with nested domain classes.

    This class consolidates all LDAP target domain models using nested classes
    for composition and validation reuse, following the [Project]Models standard.
    Integrates with flext-core patterns for enterprise LDAP data loading.
    """

    class TargetLdap(
        FlextTargetLdapConfigModels,
        FlextTargetLdapProcessingCounters,
        FlextTargetLdapModelsSinks,
    ):
        """TargetLdap domain namespace."""

        # Sink and target implementations are part of the public model
        # surface: consumers (and their tests) reach them through this
        # facade instead of importing the private _models package.
        Sink = FlextTargetLdapModelsSinks.FlextTargetLdapSink
        Target = FlextTargetLdapModelsSinks.FlextTargetLdapTarget
        BaseSink = FlextTargetLdapModelsSinks.FlextTargetLdapBaseSink
        UsersSink = FlextTargetLdapModelsSinks.FlextTargetLdapUsersSink
        GroupsSink = FlextTargetLdapModelsSinks.FlextTargetLdapGroupsSink
        OrganizationalUnitsSink = (
            FlextTargetLdapModelsSinks.FlextTargetLdapOrganizationalUnitsSink
        )
        ProcessingCounters = FlextTargetLdapProcessingCounters
        ProcessingResult = FlextTargetLdapModelsSinks.FlextTargetLdapProcessingResult

        class AttributeMapping(FlextLdapModels.Entity):
            """LDAP attribute mapping configuration with validation.

            Immutable value object defining how Singer fields map to LDAP attributes
            with business rule validation and transformation support.
            """

            singer_field_name: Annotated[
                t.NonEmptyStr,
                FlextMeltanoModels.Field(
                    ..., description="Singer field name from source data"
                ),
            ]
            ldap_attribute_name: Annotated[
                t.NonEmptyStr,
                FlextMeltanoModels.Field(..., description="Target LDAP attribute name"),
            ]
            is_required: Annotated[
                bool,
                FlextMeltanoModels.Field(
                    default=False,
                    description="Whether this attribute is required for LDAP entry",
                ),
            ]
            transformation_rule: Annotated[
                str | None,
                FlextMeltanoModels.Field(
                    default=None,
                    description=(
                        "Optional transformation rule (e.g., 'lowercase', 'uppercase')"
                    ),
                ),
            ]
            default_value: Annotated[
                str | None,
                FlextMeltanoModels.Field(
                    default=None,
                    description="Default value if source field is missing",
                ),
            ]

        class Entry(FlextLdapModels.Entity):
            """LDAP entry representation with validation and business rules.

            Immutable value object representing a complete LDAP entry with
            DN, object classes, and attributes, including validation rules.
            """

            distinguished_name: Annotated[
                t.NonEmptyStr,
                FlextMeltanoModels.Field(
                    ..., description="LDAP Distinguished Name (DN)"
                ),
            ]
            object_classes: Annotated[
                t.MutableSequenceOf[str],
                FlextMeltanoModels.Field(
                    description="LDAP object classes for this entry",
                    default_factory=list,
                ),
            ]
            attributes: Annotated[
                t.MutableStrSequenceMapping,
                FlextMeltanoModels.Field(
                    description="LDAP attributes with values",
                    default_factory=dict,
                ),
            ]
            entry_type: Annotated[
                str,
                FlextMeltanoModels.Field(
                    default="generic",
                    description="Type of LDAP entry (user, group, ou, etc.)",
                ),
            ]

            @FlextMeltanoModels.field_validator("object_classes")
            @classmethod
            def validate_object_classes(
                cls,
                v: t.MutableSequenceOf[str],
            ) -> t.MutableSequenceOf[str]:
                """Validate object classes contain 'top'.

                Appends the required ``top`` class when it is absent.

                Args:
                    v: Object classes declared on the entry.

                Returns:
                    The object classes, with ``top`` ensured.

                """
                if "top" not in v:
                    v.append("top")
                return v

            @FlextMeltanoModels.computed_field
            @property
            def parent_dn(self) -> str:
                """Parent DN derived from the distinguished name."""
                distinguished_name = self.distinguished_name
                parts = distinguished_name.split(",", 1)
                return parts[1].strip() if len(parts) > 1 else ""

            @FlextMeltanoModels.computed_field
            @property
            def rdn(self) -> str:
                """Relative distinguished name derived from the DN."""
                distinguished_name = self.distinguished_name
                rdn_part: str = distinguished_name.split(",", 1)[0].strip()
                return rdn_part

        class TransformationRule(FlextLdapModels.Value):
            """Rule for transforming LDAP data with pattern matching and replacement."""

            name: Annotated[
                t.NonEmptyStr,
                FlextMeltanoModels.Field(
                    description="Unique name identifying this transformation rule"
                ),
            ]
            pattern: Annotated[
                t.NonEmptyStr,
                FlextMeltanoModels.Field(
                    description="Regex pattern to match in source data"
                ),
            ]
            replacement: Annotated[
                str,
                FlextMeltanoModels.Field(
                    default="",
                    description="Replacement string applied when pattern matches",
                ),
            ]
            enabled: Annotated[
                bool,
                FlextMeltanoModels.Field(
                    default=True,
                    description="Whether this transformation rule is active",
                ),
            ]


m = FlextTargetLdapModels

__all__: list[str] = ["FlextTargetLdapModels", "m"]
