"""Re-export shim — canonical implementation lives in _utilities.target."""

from __future__ import annotations

from flext_target_ldap._utilities.target import FlextTargetLdap, logger, main

__all__ = ["FlextTargetLdap", "logger", "main"]
