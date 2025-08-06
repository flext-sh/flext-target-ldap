"""Singer LDAP catalog management - consolidated in flext-meltano."""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextResult, FlextValueObject, get_logger
from pydantic import Field

logger = get_logger(__name__)


# Local LDAP catalog classes (no fallbacks - real implementation)
class SingerLDAPCatalogEntry(FlextValueObject):
    """Singer LDAP catalog entry using flext-core patterns."""

    tap_stream_id: str
    stream: str
    stream_schema: dict[str, object] = Field(..., description="Singer stream schema")
    metadata: list[dict[str, object]] = Field(default_factory=list)
    key_properties: ClassVar[list[str]] = []
    bookmark_properties: ClassVar[list[str]] = []

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate catalog entry domain rules."""
        try:
            if not self.tap_stream_id.strip():
                return FlextResult.fail("tap_stream_id cannot be empty")
            if not self.stream.strip():
                return FlextResult.fail("stream cannot be empty")
            if not self.stream_schema:
                return FlextResult.fail("stream_schema cannot be empty")
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Catalog entry validation failed: {e}")


class SingerLDAPCatalogManager:
    """Manage Singer LDAP catalog operations using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize Singer LDAP catalog manager."""
        self._catalog_entries: dict[str, SingerLDAPCatalogEntry] = {}

    def add_stream(
        self,
        stream_name: str,
        schema: dict[str, object],
    ) -> FlextResult[None]:
        """Add LDAP stream to catalog."""
        try:
            entry = SingerLDAPCatalogEntry(
                tap_stream_id=stream_name,
                stream=stream_name,
                stream_schema=schema,
            )
            self._catalog_entries[stream_name] = entry
            logger.info(f"Added LDAP stream to catalog: {stream_name}")
            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"Failed to add LDAP stream to catalog: {stream_name}")
            return FlextResult.fail(f"Stream addition failed: {e}")

    def get_stream(self, stream_name: str) -> FlextResult[SingerLDAPCatalogEntry]:
        """Get LDAP stream from catalog."""
        if stream_name not in self._catalog_entries:
            return FlextResult.fail(f"LDAP stream not found: {stream_name}")
        return FlextResult.ok(self._catalog_entries[stream_name])


# Re-export for backward compatibility
__all__: list[str] = [
    "SingerLDAPCatalogEntry",
    "SingerLDAPCatalogManager",
]
