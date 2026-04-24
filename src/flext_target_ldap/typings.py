"""LDAP target type facade via MRO composition."""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
)

from flext_ldap import FlextLdapTypes
from flext_meltano import t


class FlextTargetLdapTypes(t, FlextLdapTypes):
    """MRO facade composing Meltano + LDAP type namespaces."""

    class TargetLdap:
        """Target LDAP domain type namespace."""

        type SettingsPayload = t.JsonMapping
        type MutableSettingsPayload = t.MutableJsonMapping
        type RecordPayload = t.JsonMapping
        type MutableRecordPayload = MutableMapping[str, t.JsonValue]
        type SchemaPayload = t.JsonMapping
        type MutableSchemaPayload = MutableMapping[str, t.JsonValue]
        type CatalogPayload = t.JsonMapping


t = FlextTargetLdapTypes

__all__: list[str] = ["FlextTargetLdapTypes", "t"]
