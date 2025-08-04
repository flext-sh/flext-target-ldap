"""Singer LDAP module using flext-core patterns."""

from __future__ import annotations

# Direct imports from singer modules
from flext_target_ldap.singer.catalog import SingerLDAPCatalogManager
from flext_target_ldap.singer.stream import SingerLDAPStreamProcessor
from flext_target_ldap.singer.target import SingerTargetLDAP

__all__: list[str] = [
    "SingerLDAPCatalogManager",
    "SingerLDAPStreamProcessor",
    "SingerTargetLDAP",
]
