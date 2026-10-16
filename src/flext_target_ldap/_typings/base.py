"""LDAP target type alias declarations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoTypes


class FlextTargetLdapTypingsBase:
    """LDAP target payload type aliases composed into ``t.TargetLdap``."""

    type SettingsPayload = FlextMeltanoTypes.JsonMapping
    type RecordPayload = FlextMeltanoTypes.JsonMapping
    type MutableRecordPayload = FlextMeltanoTypes.MutableJsonMapping
    type SchemaPayload = FlextMeltanoTypes.JsonMapping
    type MutableSchemaPayload = FlextMeltanoTypes.MutableJsonMapping
    type CatalogPayload = FlextMeltanoTypes.JsonMapping


__all__: list[str] = [
    "CatalogPayload",
    "FlextTargetLdapTypingsBase",
    "MutableRecordPayload",
    "MutableSchemaPayload",
    "RecordPayload",
    "SchemaPayload",
    "SettingsPayload",
]
