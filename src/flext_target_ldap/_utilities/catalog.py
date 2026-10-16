"""Singer target LDAP client access and catalog utilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import t
from flext_target_ldap._utilities.client import FlextTargetLdapClient


class FlextTargetLdapUtilitiesCatalog:
    """Canonical client access and Singer catalog construction utilities."""

    @staticmethod
    def client() -> type[FlextTargetLdapClient]:
        """Return the canonical LDAP client implementation.

        Consumers (and their tests) reach it here instead of importing
        the private ``_utilities`` package directly.
        """
        return FlextTargetLdapClient

    @staticmethod
    def build_singer_catalog() -> t.TargetLdap.CatalogPayload:
        """Build the canonical Singer catalog for LDAP targets.

        Returns:
            The Singer catalog payload with the users, groups, and
            organizational_units streams.

        """
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


__all__: list[str] = ["FlextTargetLdapUtilitiesCatalog"]
