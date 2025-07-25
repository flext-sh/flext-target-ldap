"""Singer LDAP catalog management - consolidated in flext-meltano."""

from __future__ import annotations

# Import consolidated Singer LDAP components from flext-meltano
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.singer.targets.ldap import (
    SingerLDAPCatalogEntry,
    SingerLDAPCatalogManager,
)

# Re-export for backward compatibility
__all__ = [
    "SingerLDAPCatalogEntry",
    "SingerLDAPCatalogManager",
]
