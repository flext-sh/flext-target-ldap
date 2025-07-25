"""Singer LDAP module using flext-core patterns."""

from __future__ import annotations

# Contextual import suppression for external libraries
import contextlib

# Import from singer module
with contextlib.suppress(ImportError):
    from flext_target_ldap.singer.catalog import SingerLDAPCatalogManager
    from flext_target_ldap.singer.stream import SingerLDAPStreamProcessor
    from flext_target_ldap.singer.target import SingerTargetLDAP

__all__ = [
    "SingerLDAPCatalogManager",
    "SingerLDAPStreamProcessor",
    "SingerTargetLDAP",
]
