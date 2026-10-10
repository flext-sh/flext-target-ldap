"""Target LDAP constants facade.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
src/flext_target_ldap/constants
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_ldap import FlextLdapConstants
from flext_meltano import FlextMeltanoConstants

from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase

if TYPE_CHECKING:
    from flext_target_ldap import t


class FlextTargetLdapConstants(FlextMeltanoConstants, FlextLdapConstants):
    """LDAP target constant facade.

    The domain constants live in the nested ``TargetLdap`` namespace, which
    derives ``FlextTargetLdapConstantsBase`` directly; the facade itself does
    not re-derive that base, so its ``Final`` members cannot collide with the
    inherited core chain under MRO.
    """

    class TargetLdap(FlextTargetLdapConstantsBase):
        """LDAP target constant namespace."""


c = FlextTargetLdapConstants

__all__: t.StrSequence = ("FlextTargetLdapConstants", "c")
