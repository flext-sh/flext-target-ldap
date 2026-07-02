"""Target LDAP constants facade."""

from __future__ import annotations

from flext_ldap import FlextLdapConstants
from flext_meltano import c
from flext_target_ldap import t
from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase


class FlextTargetLdapConstants(c, FlextLdapConstants):
    """LDAP target constant facade."""

    class TargetLdap(FlextTargetLdapConstantsBase):
        """LDAP target constant namespace."""


c = FlextTargetLdapConstants

__all__: t.StrSequence = ("FlextTargetLdapConstants", "c")
