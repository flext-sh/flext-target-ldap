"""Backward-compatible re-export of processing result from _models.processing_result."""

from __future__ import annotations

from flext_target_ldap._models.processing_result import (
    FlextTargetLdapProcessingCounters,
)

__all__ = ["FlextTargetLdapProcessingCounters"]
