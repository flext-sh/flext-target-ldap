# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Utilities package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._utilities.entries import FlextTargetLdapUtilitiesEntries
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime,
    )
    from flext_target_ldap._utilities.settings import FlextTargetLdapUtilitiesSettings


__all__: tuple[str, ...] = (
    "FlextTargetLdapServiceRuntime",
    "FlextTargetLdapUtilitiesEntries",
    "FlextTargetLdapUtilitiesSettings",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTargetLdapServiceRuntime": ".service_runtime",
        "FlextTargetLdapUtilitiesEntries": ".entries",
        "FlextTargetLdapUtilitiesSettings": ".settings",
    },
    public_exports=__all__,
    deferred_members={
        "FlextTargetLdapServiceRuntime": (
            "Target",
            "Sink",
            "normalize_flat_schema",
        ),
        "FlextTargetLdapUtilitiesEntries": (
            "to_str_values",
            "entry_profile",
            "record_dn",
            "object_class_list",
            "object_classes",
            "attribute_mapping",
            "entry_attributes",
            "validate_entry",
            "ldif_entry",
            "modify_changes",
            "connection_config",
        ),
        "FlextTargetLdapUtilitiesSettings": (
            "validate_ldap_target_config",
            "create_default_ldap_target_config",
        ),
    },
)
