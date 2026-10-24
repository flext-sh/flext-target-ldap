# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Utilities package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._utilities.catalog import FlextTargetLdapUtilitiesCatalog
    from flext_target_ldap._utilities.client import FlextTargetLdapClient
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime,
    )
    from flext_target_ldap._utilities.settings import FlextTargetLdapUtilitiesSettings


__all__: tuple[str, ...] = (
    "FlextTargetLdapClient",
    "FlextTargetLdapServiceRuntime",
    "FlextTargetLdapUtilitiesCatalog",
    "FlextTargetLdapUtilitiesSettings",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetLdapClient": ".client",
        "FlextTargetLdapServiceRuntime": ".service_runtime",
        "FlextTargetLdapUtilitiesCatalog": ".catalog",
        "FlextTargetLdapUtilitiesSettings": ".settings",
    }),
    public_exports=__all__,
)
