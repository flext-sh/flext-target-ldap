"""LDAP target type facade via MRO composition."""

from __future__ import annotations

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """MRO facade composing Meltano + LDAP type namespaces."""


t = FlextTargetLdapTypes
__all__: list[str] = ["FlextTargetLdapTypes", "t"]
