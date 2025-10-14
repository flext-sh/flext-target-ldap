"""Singer LDAP catalog management - consolidated in flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar, override

from flext_core import FlextCore
from pydantic import Field

from flext_target_ldap.typings import FlextTargetLdapTypes

logger = FlextCore.Logger(__name__)


# Local LDAP catalog classes (no fallbacks - real implementation)
class SingerLDAPCatalogEntry(FlextCore.Models.Entity):
    """Singer LDAP catalog entry using flext-core patterns."""

    tap_stream_id: str
    stream: str
    stream_schema: FlextTargetLdapTypes.Core.Dict = Field(
        ..., description="Singer stream schema"
    )
    metadata: list[FlextTargetLdapTypes.Core.Dict] = Field(default_factory=list)
    key_properties: ClassVar[FlextTargetLdapTypes.Core.StringList] = []
    bookmark_properties: ClassVar[FlextTargetLdapTypes.Core.StringList] = []

    def validate_business_rules(self: object) -> FlextCore.Result[None]:
        """Validate catalog entry business rules."""
        try:
            if not self.tap_stream_id.strip():
                return FlextCore.Result[None].fail("tap_stream_id cannot be empty")
            if not self.stream.strip():
                return FlextCore.Result[None].fail("stream cannot be empty")
            if not self.stream_schema:
                return FlextCore.Result[None].fail("stream_schema cannot be empty")
            return FlextCore.Result[None].ok(None)
        except Exception as e:
            return FlextCore.Result[None].fail(f"Catalog entry validation failed: {e}")


class SingerLDAPCatalogManager:
    """Manage Singer LDAP catalog operations using flext-core patterns."""

    @override
    def __init__(self: object) -> None:
        """Initialize Singer LDAP catalog manager."""
        self._catalog_entries: dict[str, SingerLDAPCatalogEntry] = {}

    def add_stream(
        self,
        stream_name: str,
        schema: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextCore.Result[None]:
        """Add LDAP stream to catalog."""
        try:
            entry = SingerLDAPCatalogEntry(
                tap_stream_id=stream_name,
                stream=stream_name,
                stream_schema=schema,
            )
            self._catalog_entries[stream_name] = entry
            logger.info("Added LDAP stream to catalog: %s", stream_name)
            return FlextCore.Result[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to add LDAP stream to catalog: %s", stream_name)
            return FlextCore.Result[None].fail(f"Stream addition failed: {e}")

    def get_stream(self, stream_name: str) -> FlextCore.Result[SingerLDAPCatalogEntry]:
        """Get LDAP stream from catalog."""
        if stream_name not in self._catalog_entries:
            return FlextCore.Result[SingerLDAPCatalogEntry].fail(
                f"LDAP stream not found: {stream_name}",
            )
        return FlextCore.Result[SingerLDAPCatalogEntry].ok(
            self._catalog_entries[stream_name],
        )


# Re-export for backward compatibility
__all__: FlextTargetLdapTypes.Core.StringList = [
    "SingerLDAPCatalogEntry",
    "SingerLDAPCatalogManager",
]
