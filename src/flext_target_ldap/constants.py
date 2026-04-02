"""FLEXT Target LDAP Constants - LDAP target loading constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Final

from flext_ldap import FlextLdapConstants
from flext_meltano import FlextMeltanoConstants


class FlextTargetLdapConstants(FlextMeltanoConstants, FlextLdapConstants):
    """LDAP target loading-specific constants following FLEXT unified pattern with nested domains.

    Extends FlextLdapConstants to inherit all LDAP and LDIF constants, adding
    target-specific constants in the TargetLdap namespace.

    Hierarchy:
        FlextConstants (flext-core)
        └── FlextLdifConstants (flext-ldif)
            └── FlextLdapConstants (flext-ldap)
                └── FlextTargetLdapConstants (this module)

    Access patterns:
        - c.TargetLdap.* (target-specific constants)
        - c.Ldap.* (inherited from FlextLdapConstants)
        - c.* (inherited from FlextLdifConstants via FlextLdapConstants)
        - c.*, c.*, etc. (inherited from FlextConstants)
    """

    class TargetLdap:
        """Target LDAP domain-specific constants namespace."""

        class Connection:
            """LDAP connection configuration constants for target operations."""

            CONNECT_TIMEOUT: Final[int] = 10
            MAX_PORT_NUMBER: Final[int] = 65535
            LDAPS_DEFAULT_PORT: Final[int] = 636


c = FlextTargetLdapConstants
__all__ = ["FlextTargetLdapConstants", "c"]
