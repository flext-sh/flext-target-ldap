"""FLEXT service orchestrator for target-ldap.

Thin facade — all infrastructure from ``FlextMeltanoTargetServiceBase`` via MRO.
Only domain-specific sink creation defined here.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoTargetServiceBase
from flext_target_ldap import t


class FlextTargetLdapApi(FlextMeltanoTargetServiceBase):
    """MRO facade for target-ldap service operations."""

    target_name: t.NonEmptyStr = "target-ldap"


__all__ = ["FlextTargetLdapApi"]
