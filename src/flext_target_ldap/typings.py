"""Type aliases and project-specific types for the LDAP target."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes

from flext_target_ldap import c


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """FLEXT Target LDAP Types.

    Inherits standard types from FlextTypes and adds project-specific
    domain types.
    """

    class Core:
        """Core type aliases overrides."""

        type Dict = Mapping[str, FlextMeltanoTypes.NormalizedValue]
        type Headers = Mapping[str, str]
        type StringList = Sequence[str]

    class Project:
        """Project-specific type aliases for target-ldap."""

        type TargetLdapProjectType = c.TargetLdapProjectType


t = FlextTargetLdapTypes
__all__ = ["FlextTargetLdapTypes", "t"]
