"""LDAP target type facade via MRO composition."""

from __future__ import annotations

from flext_ldap import FlextLdapTypes
from flext_meltano import t


class FlextTargetLdapTypes(t, FlextLdapTypes):
    """MRO facade composing Meltano + LDAP type namespaces."""

    class TargetLdap:
        """Target LDAP domain type namespace."""


t = FlextTargetLdapTypes

__all__: list[str] = ["FlextTargetLdapTypes", "t"]
