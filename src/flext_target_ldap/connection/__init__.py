"""LDAP connection module using flext-core patterns."""

from __future__ import annotations

# Direct imports from connection module
from flext_target_ldap.connection.config import LDAPConnectionConfig
from flext_target_ldap.connection.connection import LDAPConnection

__all__ = [
    "LDAPConnection",
    "LDAPConnectionConfig",
]
