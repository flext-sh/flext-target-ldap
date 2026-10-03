"""Target LDAP constants facade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_ldap import FlextLdapConstants
from flext_meltano import FlextMeltanoConstants

from ._constants.base import FlextTargetLdapConstantsBase

if TYPE_CHECKING:
    from flext_target_ldap import t


class FlextTargetLdapConstants(
    FlextMeltanoConstants, FlextLdapConstants, FlextTargetLdapConstantsBase
):
    """LDAP target constant facade."""

    class TargetLdap(FlextTargetLdapConstantsBase):
        """LDAP target constant namespace."""


c = FlextTargetLdapConstants

__all__: t.StrSequence = ("FlextTargetLdapConstants", "c")
