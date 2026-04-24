"""FLEXT Target LDAP Constants - Thin MRO Facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_ldap import c as ldap_c
from flext_meltano import c

from flext_target_ldap import FlextTargetLdapConstantsBase


class FlextTargetLdapConstants(
    c,
    ldap_c,
):
    """LDAP target loading-specific constants following FLEXT unified pattern.

    This class acts as a facade, composing all constant subclasses via MRO.
    All constants are accessible via inheritance—do not duplicate parent attributes.

    Access patterns:
        - c.TargetLdap.ENV_PREFIX, c.CONNECT_TIMEOUT, etc. (target-specific constants)
        - c.Ldap.* (inherited from c)
        - c.* (inherited from FlextLdifConstants via c)
    """

    class TargetLdap(
        FlextTargetLdapConstantsBase,
    ):
        """Class."""


c = FlextTargetLdapConstants

__all__: list[str] = ["FlextTargetLdapConstants", "c"]
