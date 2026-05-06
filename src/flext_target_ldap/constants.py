"""Target LDAP constants facade."""

from __future__ import annotations

from flext_meltano import t
from flext_target_ldap._constants.base import FlextTargetLdapConstants

c = FlextTargetLdapConstants

__all__: t.StrSequence = ("FlextTargetLdapConstants", "c")
