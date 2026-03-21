"""Type aliases and project-specific types for the LDAP target."""

from __future__ import annotations

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes

from flext_target_ldap.constants import c


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """FLEXT Target LDAP Types.

    Inherits standard types from FlextTypes and adds project-specific
    domain types.
    """

    class Core:
        """Core type aliases overrides."""

        type Dict = dict[str, FlextMeltanoTypes.NormalizedValue]
        type Headers = dict[str, str]
        type StringList = list[str]

    class Project:
        """Project-specific type aliases for target-ldap."""

        type TargetLdapProjectType = c.TargetLdapProjectType


t = FlextTargetLdapTypes
__all__ = ["FlextTargetLdapTypes", "t"]
