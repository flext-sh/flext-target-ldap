"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

from flext_ldap import FlextLdapUtilities
from flext_meltano import u
from flext_target_ldap import c, t


class FlextTargetLdapUtilities(u, FlextLdapUtilities):
    """Single unified utilities class for Singer target LDAP operations.

    Follows FLEXT unified class pattern with nested helper classes for
    domain-specific Singer target functionality with LDAP directory operations.

    Constants are accessed via constants module:
        c.Ldap.PORT (389)
        c.LDAPS_DEFAULT_PORT (636)
        c.DEFAULT_SIZE
    """

    class TargetLdap:
        """Singer protocol utilities for target operations."""

        @staticmethod
        def build_singer_catalog() -> t.TargetLdap.CatalogPayload:
            """Build the canonical Singer catalog for LDAP targets."""
            return t.Cli.JSON_MAPPING_ADAPTER.validate_python({
                "streams": [
                    {
                        "tap_stream_id": "users",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "email": {"type": "string"},
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "full_name": {"type": "string"},
                                "phone": {"type": "string"},
                                "department": {"type": "string"},
                                "title": {"type": "string"},
                            },
                            "required": ["username"],
                        },
                    },
                    {
                        "tap_stream_id": "groups",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "members": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                            },
                            "required": ["name"],
                        },
                    },
                    {
                        "tap_stream_id": "organizational_units",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["name"],
                        },
                    },
                ],
            })

        class TypeConversion:
            """Type coercion utilities for Singer settings values to typed Python values."""

            @staticmethod
            def extract_attribute_mapping(
                settings: t.TargetLdap.SettingsPayload,
            ) -> t.StrMapping:
                """Extract attribute mapping from settings."""
                raw = settings.get(c.TargetLdap.KEY_ATTRIBUTE_MAPPING, {})
                if isinstance(raw, Mapping):
                    normalized_mapping: t.MutableMappingKV[str, str] = {}
                    for key, value in raw.items():
                        normalized_key = key
                        normalized_value = str(value)
                        normalized_mapping[normalized_key] = normalized_value
                    return normalized_mapping
                msg = f"Expected Mapping for 'attribute_mapping', got {type(raw).__name__}: {raw!r}"
                raise TypeError(msg)

            @staticmethod
            def extract_object_classes(
                settings: t.TargetLdap.SettingsPayload,
            ) -> t.StrSequence:
                """Extract object classes from settings."""
                raw = settings.get(c.TargetLdap.KEY_OBJECT_CLASSES)
                if isinstance(raw, list):
                    return [str(object_class) for object_class in raw if object_class]
                if isinstance(raw, str):
                    return [raw]
                return [c.TargetLdap.DEFAULT_OBJECT_CLASS]


u = FlextTargetLdapUtilities

__all__: list[str] = ["FlextTargetLdapUtilities", "u"]
