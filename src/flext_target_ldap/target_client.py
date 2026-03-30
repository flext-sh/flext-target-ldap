"""Backward-compatible re-export of client classes from _utilities.client."""

from __future__ import annotations

from flext_target_ldap import (
    FlextTargetLdapClient,
    FlextTargetLdapSearchEntry,
)

__all__ = ["FlextTargetLdapClient", "FlextTargetLdapSearchEntry"]
