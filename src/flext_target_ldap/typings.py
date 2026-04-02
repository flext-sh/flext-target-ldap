"""Type aliases and project-specific types for the LDAP target."""

from __future__ import annotations

from collections.abc import Mapping

from pydantic import ConfigDict, TypeAdapter

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """FLEXT Target LDAP Types.

    Inherits standard types from FlextTypes and adds project-specific
    domain types.
    """

    class TargetLdap:
        """Target LDAP-specific types and centralized adapters."""

        STRING_ADAPTER: TypeAdapter[FlextMeltanoTypes.TextValue] = TypeAdapter(
            FlextMeltanoTypes.TextValue,
        )
        INTEGER_ADAPTER: TypeAdapter[FlextMeltanoTypes.IntegerValue] = TypeAdapter(
            FlextMeltanoTypes.IntegerValue,
        )
        STR_MAPPING_ADAPTER: TypeAdapter[FlextMeltanoTypes.StrMapping] = TypeAdapter(
            FlextMeltanoTypes.StrMapping,
        )
        STR_SEQUENCE_ADAPTER: TypeAdapter[FlextMeltanoTypes.StrSequence] = TypeAdapter(
            FlextMeltanoTypes.StrSequence,
        )
        CONFIG_MAP_ADAPTER: TypeAdapter[Mapping[str, FlextMeltanoTypes.ConfigMap]] = (
            TypeAdapter(
                Mapping[str, FlextMeltanoTypes.ConfigMap],
            )
        )
        SINGER_MESSAGE_ADAPTER: TypeAdapter[FlextMeltanoTypes.ContainerMapping] = (
            TypeAdapter(
                FlextMeltanoTypes.ContainerMapping,
                config=ConfigDict(strict=False),
            )
        )
        CONTAINER_VALUE_MAP_ADAPTER: TypeAdapter[
            FlextMeltanoTypes.ContainerValueMapping
        ] = TypeAdapter(
            FlextMeltanoTypes.ContainerValueMapping,
        )


t = FlextTargetLdapTypes
__all__ = ["FlextTargetLdapTypes", "t"]
