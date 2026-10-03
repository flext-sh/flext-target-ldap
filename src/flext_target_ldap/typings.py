"""LDAP target type facade via MRO composition."""

from __future__ import annotations

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """MRO facade composing Meltano + LDAP type namespaces."""

    class TargetLdap:
        """Target LDAP domain type namespace."""

        type SettingsPayload = FlextMeltanoTypes.JsonMapping
        type RecordPayload = FlextMeltanoTypes.JsonMapping
        type MutableRecordPayload = FlextMeltanoTypes.MutableJsonMapping
        type SchemaPayload = FlextMeltanoTypes.JsonMapping
        type MutableSchemaPayload = FlextMeltanoTypes.MutableJsonMapping
        type CatalogPayload = FlextMeltanoTypes.JsonMapping


t = FlextTargetLdapTypes

__all__: list[str] = ["FlextTargetLdapTypes", "t"]
