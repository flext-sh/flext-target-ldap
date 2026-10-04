# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap.application package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator


__all__: tuple[str, ...] = ("FlextTargetLdapOrchestrator",)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({".orchestrator": ("FlextTargetLdapOrchestrator",)}),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
