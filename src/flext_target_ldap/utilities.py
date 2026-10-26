# AUTO-GENERATED FILE — Regenerate with: make gen
"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_ldap import u
from flext_meltano import u as flext_meltano_u

from flext_target_ldap._utilities import (
    FlextTargetLdapServiceRuntime,
    FlextTargetLdapUtilitiesEntries,
    FlextTargetLdapUtilitiesSettings,
)


class FlextTargetLdapUtilities(flext_meltano_u, u):
    """Single unified utilities class for Singer target LDAP operations.

    Follows FLEXT unified class pattern with nested helper classes for
    domain-specific Singer target functionality with LDAP directory operations.

    Constants are accessed via the constants module:
        c.Ldap.PORT
        c.LDAPS_DEFAULT_PORT
        c.DEFAULT_SIZE
    """

    class TargetLdap(
        FlextTargetLdapUtilitiesEntries,
        FlextTargetLdapServiceRuntime,
        FlextTargetLdapUtilitiesSettings,
    ):
        """Singer protocol utilities for target operations."""


u = FlextTargetLdapUtilities
__all__: list[str] = ["FlextTargetLdapUtilities", "u"]
