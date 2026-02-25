"""Singer LDAP catalog management - consolidated in flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar, override

from flext_core import FlextLogger, FlextModels, FlextResult
from pydantic import Field

from flext_target_ldap.typings import t

logger = FlextLogger(__name__)


# Local LDAP catalog classes (no fallbacks - real implementation)
class SingerLDAPCatalogEntry(FlextModels.Entity):
    """Singer LDAP catalog entry using flext-core patterns."""

    tap_stream_id: str
    stream: str
    stream_schema: t.Core.Dict = Field(
        ...,
        description="Singer stream schema",
    )
    metadata: list[t.Core.Dict] = Field(default_factory=list)
    key_properties: ClassVar[t.Core.StringList] = []
    bookmark_properties: ClassVar[t.Core.StringList] = []

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate catalog entry business rules."""
        try:
            if not self.tap_stream_id.strip():
                return FlextResult[bool].fail("tap_stream_id cannot be empty")
            if not self.stream.strip():
                return FlextResult[bool].fail("stream cannot be empty")
            if not self.stream_schema:
                return FlextResult[bool].fail("stream_schema cannot be empty")
            return FlextResult[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return FlextResult[bool].fail(f"Catalog entry validation failed: {e}")


class SingerLDAPCatalogManager:
    """Manage Singer LDAP catalog operations using flext-core patterns."""

    @override
    def __init__(self) -> None:
        """Initialize Singer LDAP catalog manager."""
        self._catalog_entries: dict[str, SingerLDAPCatalogEntry] = {}

    def add_stream(
        self,
        stream_name: str,
        schema: t.Core.Dict,
    ) -> FlextResult[bool]:
        """Add LDAP stream to catalog."""
        try:
            entry = SingerLDAPCatalogEntry(
                tap_stream_id=stream_name,
                stream=stream_name,
                stream_schema=schema,
            )
            self._catalog_entries[stream_name] = entry
            logger.info("Added LDAP stream to catalog: %s", stream_name)
            return FlextResult[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to add LDAP stream to catalog: %s", stream_name)
            return FlextResult[bool].fail(f"Stream addition failed: {e}")

    def get_stream(self, stream_name: str) -> FlextResult[SingerLDAPCatalogEntry]:
        """Get LDAP stream from catalog."""
        if stream_name not in self._catalog_entries:
            return FlextResult[SingerLDAPCatalogEntry].fail(
                f"LDAP stream not found: {stream_name}",
            )
        return FlextResult[SingerLDAPCatalogEntry].ok(
            self._catalog_entries[stream_name],
        )


# Re-export for backward compatibility
__all__: list[str] = [
    "SingerLDAPCatalogEntry",
    "SingerLDAPCatalogManager",
]
