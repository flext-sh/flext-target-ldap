from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from flext_core import FlextTypes


class FlextTargetLdapTypes(FlextTypes):
    class Core:
        type Dict = Mapping[str, FlextTypes.GeneralValueType]
        type Headers = Mapping[str, str]
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
