"""LDAP application module using flext-core patterns."""

from __future__ import annotations

# Contextual import suppression for external libraries
import contextlib

# Import from application module
with contextlib.suppress(ImportError):
    from flext_target_ldap.application.orchestrator import LDAPTargetOrchestrator

__all__ = [
    "LDAPTargetOrchestrator",
]
