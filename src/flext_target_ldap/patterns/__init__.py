"""LDAP patterns module using flext-core patterns."""

from __future__ import annotations

# Contextual import suppression for external libraries
import contextlib

# Import from patterns module
with contextlib.suppress(ImportError):
    from flext_target_ldap.patterns.ldap_patterns import (
        LDAPDataTransformer,
        LDAPEntryManager,
        LDAPSchemaMapper,
        LDAPTypeConverter,
    )

__all__ = [
    "LDAPDataTransformer",
    "LDAPEntryManager",
    "LDAPSchemaMapper",
    "LDAPTypeConverter",
]
