"""Backward-compatible re-export of client classes from _utilities.client."""

from __future__ import annotations

from flext_target_ldap._utilities.client import (
    FlextTargetLdapClient,
    FlextTargetLdapSearchEntry,
)

__all__ = ["FlextTargetLdapClient", "FlextTargetLdapSearchEntry"]
