# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Constants package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase


__all__: tuple[str, ...] = ("FlextTargetLdapConstantsBase",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextTargetLdapConstantsBase": ".base"}),
    public_exports=__all__,
)
