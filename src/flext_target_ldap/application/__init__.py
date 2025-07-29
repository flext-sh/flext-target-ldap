"""LDAP application module using flext-core patterns."""

from __future__ import annotations

# Direct import from application module
from flext_target_ldap.application.orchestrator import LDAPTargetOrchestrator

__all__ = [
    "LDAPTargetOrchestrator",
]
