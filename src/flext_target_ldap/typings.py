from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes


class FlextTargetLdapTypes(FlextTypes):
    """FLEXT Target LDAP Types.

    Inherits standard types from FlextTypes and adds project-specific
    domain types.
    """

    class Core:
        """Core type aliases overrides."""

        # Use dict[str, GeneralValueType] for strict typing without RootModel overhead
        # This satisfies "no Any" while maintaining compatibility with standard dict usage
        type Dict = dict[str, FlextTypes.GeneralValueType]
        type Headers = dict[str, str]
        type StringList = list[str]

    class Project:
        type TargetLdapProjectType = Literal[
            "library",
            "application",
            "service",
            "singer-target",
            "ldap-loader",
            "directory-loader",
            "singer-target-ldap",
            "target-ldap",
            "ldap-connector",
            "directory-connector",
            "singer-protocol",
            "ldap-integration",
            "directory-service",
            "ldap-target",
            "singer-stream",
            "etl-target",
            "data-pipeline",
            "ldap-sink",
            "singer-integration",
        ]


t = FlextTargetLdapTypes

__all__ = ["FlextTargetLdapTypes", "t"]
