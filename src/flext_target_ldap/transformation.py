"""Backward-compatible re-export of transformation classes from _utilities.transformation."""

from __future__ import annotations

from flext_core import FlextLogger

from flext_target_ldap._utilities.transformation import (
    FlextTargetLdapMigrationValidator,
    FlextTargetLdapTransformationEngine,
)

logger = FlextLogger(__name__)

DataTransformationEngine = FlextTargetLdapTransformationEngine
MigrationValidator = FlextTargetLdapMigrationValidator

__all__ = [
    "DataTransformationEngine",
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapTransformationEngine",
    "MigrationValidator",
    "logger",
]
