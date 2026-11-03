# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Protocols package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._protocols.base import FlextTargetLdapProtocolsBase
    from flext_target_ldap._protocols.config import FlextTargetLdapProtocolsConfig
    from flext_target_ldap._protocols.entities import FlextTargetLdapProtocolsEntities


__all__: tuple[str, ...] = (
    "FlextTargetLdapProtocolsBase",
    "FlextTargetLdapProtocolsConfig",
    "FlextTargetLdapProtocolsEntities",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTargetLdapProtocolsBase": ".base",
        "FlextTargetLdapProtocolsConfig": ".config",
        "FlextTargetLdapProtocolsEntities": ".entities",
    },
    public_exports=__all__,
)
