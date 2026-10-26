# AUTO-GENERATED FILE — Regenerate with: make gen
"""Target LDAP protocol facade via MRO composition.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_ldap import p
from flext_meltano import p as flext_meltano_p

from flext_target_ldap._protocols import FlextTargetLdapProtocolsBase


class FlextTargetLdapProtocols(flext_meltano_p, p):
    """MRO facade composing Meltano + LDAP protocol namespaces."""

    class TargetLdap(FlextTargetLdapProtocolsBase):
        """Target LDAP domain protocol namespace."""


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
