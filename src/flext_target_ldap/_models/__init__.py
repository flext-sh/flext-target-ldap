# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Models package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._models.config import FlextTargetLdapConfigModels
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import FlextTargetLdapModelsSinks


__all__: tuple[str, ...] = (
    "FlextTargetLdapConfigModels",
    "FlextTargetLdapModelsSinks",
    "FlextTargetLdapProcessingCounters",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".config": ("FlextTargetLdapConfigModels",),
            ".processing_result": ("FlextTargetLdapProcessingCounters",),
            ".sinks": ("FlextTargetLdapModelsSinks",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
