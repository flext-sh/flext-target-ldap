"""LDAP application module using flext-core patterns."""

from __future__ import annotations

from flext_target_ldap.application.orchestrator import LDAPTargetOrchestrator

__all__: list[str] = [
    "LDAPTargetOrchestrator",
]
