# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._typings.base import FlextTargetLdapTypingsBase


__all__: tuple[str, ...] = ("FlextTargetLdapTypingsBase",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextTargetLdapTypingsBase": ".base"}),
    public_exports=__all__,
)
