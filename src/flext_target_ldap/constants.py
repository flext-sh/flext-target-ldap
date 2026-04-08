"""FLEXT Target LDAP Constants - Thin MRO Facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_ldap import FlextLdapConstants
from flext_meltano import FlextMeltanoConstants
from flext_target_ldap import FlextTargetLdapConstantsBase


class FlextTargetLdapConstants(
    FlextMeltanoConstants,
    FlextLdapConstants,
):
    """LDAP target loading-specific constants following FLEXT unified pattern.

    This class acts as a facade, composing all constant subclasses via MRO.
    All constants are accessible via inheritance—do not duplicate parent attributes.

    Access patterns:
        - c.ENV_PREFIX, c.CONNECT_TIMEOUT, etc. (target-specific constants)
        - c.Ldap.* (inherited from FlextLdapConstants)
        - c.* (inherited from FlextLdifConstants via FlextLdapConstants)
    """

    class TargetLdap(
        FlextTargetLdapConstantsBase,
    ):
        """Class."""


c = FlextTargetLdapConstants
__all__ = ["FlextTargetLdapConstants", "c"]
