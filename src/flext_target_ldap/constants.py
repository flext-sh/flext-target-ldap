# AUTO-GENERATED FILE — Regenerate with: make gen
"""Target LDAP constants facade.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_ldap import c as flext_ldap_c
from flext_meltano import c as flext_meltano_c

from flext_target_ldap._constants import FlextTargetLdapConstantsBase


class FlextTargetLdapConstants(flext_meltano_c, flext_ldap_c):
    """LDAP target constant facade.

    The domain constants live in the nested ``TargetLdap`` namespace, which
    derives ``FlextTargetLdapConstantsBase`` directly; the facade itself does
    not re-derive that base, so its ``Final`` members cannot collide with the
    inherited core chain under MRO.
    """

    class TargetLdap(FlextTargetLdapConstantsBase):
        """LDAP target constant namespace."""


c = FlextTargetLdapConstants
__all__: list[str] = ["FlextTargetLdapConstants", "c"]
