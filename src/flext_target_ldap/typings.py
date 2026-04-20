"""Type aliases and project-specific types for the LDAP target."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes
from flext_target_ldap import m, u


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """FLEXT Target LDAP Types.

    Inherits standard types from FlextTypes and adds project-specific
    domain types.
    """

    class TargetLdap:
        """Target LDAP-specific types and centralized adapters."""

        STRING_ADAPTER: u.TypeAdapter[FlextMeltanoTypes.TextValue] = u.TypeAdapter(
            FlextMeltanoTypes.TextValue,
        )
        INTEGER_ADAPTER: u.TypeAdapter[FlextMeltanoTypes.IntegerValue] = u.TypeAdapter(
            FlextMeltanoTypes.IntegerValue,
        )
        STR_MAPPING_ADAPTER: u.TypeAdapter[FlextMeltanoTypes.StrMapping] = (
            u.TypeAdapter(
                FlextMeltanoTypes.StrMapping,
            )
        )
        STR_SEQUENCE_ADAPTER: u.TypeAdapter[FlextMeltanoTypes.StrSequence] = (
            u.TypeAdapter(
                FlextMeltanoTypes.StrSequence,
            )
        )
        CONFIG_MAP_ADAPTER: u.TypeAdapter[Mapping[str, FlextMeltanoTypes.ConfigMap]] = (
            u.TypeAdapter(
                Mapping[str, FlextMeltanoTypes.ConfigMap],
            )
        )
        SINGER_MESSAGE_ADAPTER: u.TypeAdapter[
            FlextMeltanoTypes.RecursiveContainerMapping
        ] = u.TypeAdapter(
            FlextMeltanoTypes.RecursiveContainerMapping,
            config=m.ConfigDict(strict=False),
        )
        CONTAINER_VALUE_MAP_ADAPTER: u.TypeAdapter[
            FlextMeltanoTypes.ContainerValueMapping
        ] = u.TypeAdapter(
            FlextMeltanoTypes.ContainerValueMapping,
        )


t = FlextTargetLdapTypes
__all__: list[str] = ["FlextTargetLdapTypes", "t"]
