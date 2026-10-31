# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap.services package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap.services.client import FlextTargetLdapClient
    from flext_target_ldap.services.sinks import FlextTargetLdapSinks


__all__: tuple[str, ...] = ("FlextTargetLdapClient", "FlextTargetLdapSinks")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetLdapClient": ".client",
        "FlextTargetLdapSinks": ".sinks",
    }),
    public_exports=__all__,
)
