# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Models package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._models.config import FlextTargetLdapModelsConfig
    from flext_target_ldap._models.entities import FlextTargetLdapModelsEntities


__all__: tuple[str, ...] = (
    "FlextTargetLdapModelsConfig",
    "FlextTargetLdapModelsEntities",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTargetLdapModelsConfig": ".config",
        "FlextTargetLdapModelsEntities": ".entities",
    },
    public_exports=__all__,
)
