"""Target LDAP constants facade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_ldap import c as _ldap_c
from flext_meltano import c

from ._constants.base import FlextTargetLdapConstantsBase

if TYPE_CHECKING:
    from flext_target_ldap import t


class FlextTargetLdapConstants(c, _ldap_c, FlextTargetLdapConstantsBase):
    """LDAP target constant facade."""

    class TargetLdap(FlextTargetLdapConstantsBase):
        """LDAP target constant namespace."""


c = FlextTargetLdapConstants

__all__: t.StrSequence = ("FlextTargetLdapConstants", "c")
