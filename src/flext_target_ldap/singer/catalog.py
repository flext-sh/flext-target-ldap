"""Singer LDAP catalog management - consolidated in flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, r
from pydantic import BaseModel, Field

logger = FlextLogger(__name__)


class SingerLDAPCatalogEntry(BaseModel):
    """Singer LDAP catalog entry with stream metadata."""

    tap_stream_id: str = Field(min_length=1)
    stream: str = Field(min_length=1)
    stream_schema: dict[str, object] = Field(default_factory=dict)


class SingerLDAPCatalogManager:
    """Manage Singer LDAP catalog operations using flext-core patterns."""

    @override
    def __init__(self) -> None:
        """Initialize Singer LDAP catalog manager."""
        self._catalog_entries: dict[str, SingerLDAPCatalogEntry] = {}

    def add_stream(self, stream_name: str, schema: dict[str, object]) -> r[bool]:
        """Add LDAP stream to catalog."""
        try:
            entry = SingerLDAPCatalogEntry(
                tap_stream_id=stream_name, stream=stream_name, stream_schema=schema
            )
            self._catalog_entries[stream_name] = entry
            logger.info("Added LDAP stream to catalog: %s", stream_name)
            return r[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to add LDAP stream to catalog: %s", stream_name)
            return r[bool].fail(f"Stream addition failed: {e}")

    def get_stream(self, stream_name: str) -> r[SingerLDAPCatalogEntry]:
        """Get LDAP stream from catalog."""
        if stream_name not in self._catalog_entries:
            return r[SingerLDAPCatalogEntry].fail(
                f"LDAP stream not found: {stream_name}"
            )
        return r[SingerLDAPCatalogEntry].ok(self._catalog_entries[stream_name])


__all__: list[str] = ["SingerLDAPCatalogEntry", "SingerLDAPCatalogManager"]
