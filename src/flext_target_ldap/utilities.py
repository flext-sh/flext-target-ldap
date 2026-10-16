"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_ldap import FlextLdapUtilities
from flext_meltano import FlextMeltanoUtilities

from flext_target_ldap._utilities.catalog import FlextTargetLdapUtilitiesCatalog
from flext_target_ldap._utilities.client import FlextTargetLdapClient
from flext_target_ldap._utilities.service_runtime import FlextTargetLdapServiceRuntime
from flext_target_ldap._utilities.settings import FlextTargetLdapUtilitiesSettings


class FlextTargetLdapUtilities(FlextMeltanoUtilities, FlextLdapUtilities):
    """Single unified utilities class for Singer target LDAP operations.

    Follows FLEXT unified class pattern with nested helper classes for
    domain-specific Singer target functionality with LDAP directory operations.

    Constants are accessed via the constants module:
        c.Ldap.PORT
        c.LDAPS_DEFAULT_PORT
        c.DEFAULT_SIZE
    """

    class TargetLdap(
        FlextTargetLdapClient,
        FlextTargetLdapServiceRuntime,
        FlextTargetLdapUtilitiesSettings,
        FlextTargetLdapUtilitiesCatalog,
    ):
        """Singer protocol utilities for target operations."""


u = FlextTargetLdapUtilities

__all__: list[str] = ["FlextTargetLdapUtilities", "u"]
