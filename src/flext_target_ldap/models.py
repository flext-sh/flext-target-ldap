# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Target LDAP Models - Consolidated domain models following Models patterns.

This module implements the FlextTargetLdapModels class that extends FlextModels,
providing unified LDAP target domain models with nested classes for composition
and validation reuse. Follows the FLEXT ecosystem unified models standard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_ldap import m
from flext_meltano import m as flext_meltano_m

from flext_target_ldap._models import (
    FlextTargetLdapConfigModels,
    FlextTargetLdapModelsEntities,
)


class FlextTargetLdapModels(flext_meltano_m, m):
    """Unified LDAP target models extending FlextModels with nested domain classes.

    This class consolidates all LDAP target domain models using nested classes
    for composition and validation reuse, following the [Project]Models standard.
    Integrates with flext-core patterns for enterprise LDAP data loading.
    """

    class TargetLdap(
        FlextTargetLdapConfigModels,
        FlextTargetLdapModelsEntities,
    ):
        """TargetLdap domain namespace."""


m = FlextTargetLdapModels
__all__: list[str] = ["FlextTargetLdapModels", "m"]
