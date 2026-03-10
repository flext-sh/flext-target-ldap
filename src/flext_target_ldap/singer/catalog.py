"""Singer LDAP catalog management - consolidated in flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextResult

from flext_target_ldap.typings import t

logger = FlextLogger(__name__)


class SingerLDAPCatalogManager:
    """Manage Singer LDAP catalog operations using flext-core patterns."""

    @override
    def __init__(self) -> None:
        """Initialize Singer LDAP catalog manager."""
        self._catalog_entries: dict[str, SingerLDAPCatalogEntry] = {}  # noqa: F821

    def add_stream(
        self, stream_name: str, schema: dict[str, t.ContainerValue]
    ) -> FlextResult[bool]:
        """Add LDAP stream to catalog."""
        try:
            entry = SingerLDAPCatalogEntry(  # noqa: F821
                tap_stream_id=stream_name, stream=stream_name, stream_schema=schema
            )
            self._catalog_entries[stream_name] = entry
            logger.info("Added LDAP stream to catalog: %s", stream_name)
            return FlextResult[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to add LDAP stream to catalog: %s", stream_name)
            return FlextResult[bool].fail(f"Stream addition failed: {e}")

    def get_stream(self, stream_name: str) -> FlextResult[SingerLDAPCatalogEntry]:  # noqa: F821
        """Get LDAP stream from catalog."""
        if stream_name not in self._catalog_entries:
            return FlextResult[SingerLDAPCatalogEntry].fail(  # noqa: F821
                f"LDAP stream not found: {stream_name}"
            )
        return FlextResult[SingerLDAPCatalogEntry].ok(  # noqa: F821
            self._catalog_entries[stream_name]
        )


__all__: list[str] = ["SingerLDAPCatalogEntry", "SingerLDAPCatalogManager"]  # noqa: F822
