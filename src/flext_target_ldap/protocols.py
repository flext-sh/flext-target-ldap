"""Target LDAP protocol facade via MRO composition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_ldap import FlextLdapProtocols
from flext_meltano import p


class FlextTargetLdapProtocols(p, FlextLdapProtocols):
    """MRO facade composing Meltano + LDAP protocol namespaces."""

    @runtime_checkable
    class TargetLdap(FlextLdapProtocols.Ldap, Protocol):
        """Target LDAP domain protocol namespace."""


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
