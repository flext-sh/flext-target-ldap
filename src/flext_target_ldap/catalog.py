"""Shared Singer catalog definitions for LDAP targets."""

from __future__ import annotations

from flext_core import t


def build_singer_catalog() -> dict[str, t.ContainerValue]:
    """Build the canonical Singer catalog for LDAP targets."""
    return {
        "streams": [
            {
                "tap_stream_id": "users",
                "schema": {
                    "type": "t.NormalizedValue",
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
                    "type": "t.NormalizedValue",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "members": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["name"],
                },
            },
            {
                "tap_stream_id": "organizational_units",
                "schema": {
                    "type": "t.NormalizedValue",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["name"],
                },
            },
        ],
    }
