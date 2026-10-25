# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Models package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._models.config import FlextTargetLdapConfigModels
    from flext_target_ldap._models.entities import FlextTargetLdapModelsEntities


__all__: tuple[str, ...] = (
    "FlextTargetLdapConfigModels",
    "FlextTargetLdapModelsEntities",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetLdapConfigModels": ".config",
        "FlextTargetLdapModelsEntities": ".entities",
    }),
    public_exports=__all__,
)
