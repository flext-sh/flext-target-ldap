"""Backward-compatible re-export of sink classes from _models.sinks."""

from __future__ import annotations

from flext_target_ldap._models.sinks import (
    FlextTargetLdapBaseSink,
    FlextTargetLdapGroupsSink,
    FlextTargetLdapOrganizationalUnitsSink,
    FlextTargetLdapProcessingResult,
    FlextTargetLdapSink,
    FlextTargetLdapTarget,
    FlextTargetLdapUsersSink,
)

__all__ = [
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
]
