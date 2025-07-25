"""LDAP connection module using flext-core patterns."""

from __future__ import annotations

# Contextual import suppression for external libraries
import contextlib

# Import from connection module
with contextlib.suppress(ImportError):
    from flext_target_ldap.connection.config import LDAPConnectionConfig
    from flext_target_ldap.connection.connection import LDAPConnection

__all__ = [
    "LDAPConnection",
    "LDAPConnectionConfig",
]
