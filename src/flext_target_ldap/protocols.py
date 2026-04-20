"""Target LDAP protocol facade via MRO composition."""

from __future__ import annotations

from flext_ldap import FlextLdapProtocols
from flext_meltano import FlextMeltanoProtocols


class FlextTargetLdapProtocols(FlextMeltanoProtocols, FlextLdapProtocols):
    """MRO facade composing Meltano + LDAP protocol namespaces."""


p = FlextTargetLdapProtocols
__all__: list[str] = ["FlextTargetLdapProtocols", "p"]
