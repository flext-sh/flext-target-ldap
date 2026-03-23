"""Type aliases and project-specific types for the LDAP target."""

from __future__ import annotations

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """FLEXT Target LDAP Types.

    Inherits standard types from FlextTypes and adds project-specific
    domain types.
    """


t = FlextTargetLdapTypes
__all__ = ["FlextTargetLdapTypes", "t"]
