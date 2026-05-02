"""Singer LDAP catalog management - consolidated in flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_target_ldap import c, e, m, p, r, t, u

logger = u.fetch_logger(__name__)


class FlextTargetLdapCatalogManager:
    """Manage Singer LDAP catalog operations using flext-core patterns."""

    @override
    def __init__(self) -> None:
        """Initialize Singer LDAP catalog manager."""
        self._catalog_entries: dict[
            str,
            m.TargetLdap.SingerLDAPCatalogEntry,
        ] = {}

    def add_stream(
        self,
        stream_name: str,
        schema: t.TargetLdap.SchemaPayload,
    ) -> p.Result[bool]:
        """Add LDAP stream to catalog."""
        try:
            entry = m.TargetLdap.SingerLDAPCatalogEntry(
                tap_stream_id=stream_name,
                stream=stream_name,
                stream_schema=dict(schema.items()),
            )
            self._catalog_entries[stream_name] = entry
            logger.info("Added LDAP stream to catalog: %s", stream_name)
            return r[bool].ok(value=True)
        except c.EXC_RUNTIME_TYPE as e:
            logger.exception("Failed to add LDAP stream to catalog: %s", stream_name)
            return r[bool].fail_op("Stream addition", e)

    def get_stream(
        self, stream_name: str
    ) -> p.Result[m.TargetLdap.SingerLDAPCatalogEntry]:
        """Get LDAP stream from catalog."""
        if stream_name not in self._catalog_entries:
            return e.fail_not_found(
                "LDAP stream",
                stream_name,
                result_type=r[m.TargetLdap.SingerLDAPCatalogEntry],
            )
        return r[m.TargetLdap.SingerLDAPCatalogEntry].ok(
            self._catalog_entries[stream_name],
        )


__all__: t.StrSequence = [
    "FlextTargetLdapCatalogManager",
]
