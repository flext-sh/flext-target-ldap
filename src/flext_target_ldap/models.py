# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Target LDAP Models - Consolidated domain models following Models patterns.

This module implements the FlextTargetLdapModels class that extends FlextModels,
providing unified LDAP target domain models with nested classes for composition
and validation reuse. Follows the FLEXT ecosystem unified models standard.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeAlias

from flext_ldap import FlextLdapModels
from flext_meltano import FlextMeltanoModels

from flext_target_ldap._models import (
    FlextTargetLdapConfigModels,
    FlextTargetLdapModelsEntities,
    FlextTargetLdapModelsSinks,
    FlextTargetLdapProcessingCounters,
)


class FlextTargetLdapModels(FlextMeltanoModels, FlextLdapModels):
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

        # Sink and target implementations are part of the public model
        # surface: consumers (and their tests) reach them through this
        # facade instead of importing the private _models package.
        Sink: TypeAlias = FlextTargetLdapModelsSinks.FlextTargetLdapSink
        Target: TypeAlias = FlextTargetLdapModelsSinks.FlextTargetLdapTarget
        BaseSink: TypeAlias = FlextTargetLdapModelsSinks.FlextTargetLdapBaseSink
        UsersSink: TypeAlias = FlextTargetLdapModelsSinks.FlextTargetLdapUsersSink
        GroupsSink: TypeAlias = FlextTargetLdapModelsSinks.FlextTargetLdapGroupsSink
        OrganizationalUnitsSink: TypeAlias = (
            FlextTargetLdapModelsSinks.FlextTargetLdapOrganizationalUnitsSink
        )
        ProcessingCounters: TypeAlias = FlextTargetLdapProcessingCounters
        ProcessingResult: TypeAlias = (
            FlextTargetLdapModelsSinks.FlextTargetLdapProcessingResult
        )


m = FlextTargetLdapModels
__all__: list[str] = ["FlextTargetLdapModels", "m"]
