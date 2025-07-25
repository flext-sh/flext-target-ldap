"""LDAP infrastructure module using flext-core patterns."""

from __future__ import annotations

# Contextual import suppression for external libraries
import contextlib

# Import from infrastructure module
with contextlib.suppress(ImportError):
    from flext_target_ldap.infrastructure.di_container import (
        TargetLDAPContainer,
        get_target_ldap_container,
    )

__all__ = [
    "TargetLDAPContainer",
    "get_target_ldap_container",
]
