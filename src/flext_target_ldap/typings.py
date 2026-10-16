"""LDAP target type facade via MRO composition.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_ldap import FlextLdapTypes
from flext_meltano import FlextMeltanoTypes

from flext_target_ldap._typings.base import FlextTargetLdapTypingsBase


class FlextTargetLdapTypes(FlextMeltanoTypes, FlextLdapTypes):
    """MRO facade composing Meltano + LDAP type namespaces."""

    class TargetLdap:
        """Target LDAP domain type namespace."""

        SettingsPayload = FlextTargetLdapTypingsBase.SettingsPayload
        RecordPayload = FlextTargetLdapTypingsBase.RecordPayload
        MutableRecordPayload = FlextTargetLdapTypingsBase.MutableRecordPayload
        SchemaPayload = FlextTargetLdapTypingsBase.SchemaPayload
        MutableSchemaPayload = FlextTargetLdapTypingsBase.MutableSchemaPayload
        CatalogPayload = FlextTargetLdapTypingsBase.CatalogPayload


t = FlextTargetLdapTypes

__all__: list[str] = ["FlextTargetLdapTypes", "t"]
