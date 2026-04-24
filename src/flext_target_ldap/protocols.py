"""Target LDAP protocol facade via MRO composition."""

from __future__ import annotations

from typing import Protocol

from flext_ldap import p as ldap_p
from flext_meltano import p


class FlextTargetLdapProtocols(p, ldap_p):
    """MRO facade composing Meltano + LDAP protocol namespaces."""

    class TargetLdap(ldap_p.Ldap, Protocol):
        """Target LDAP domain protocol namespace."""


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
