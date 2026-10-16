# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._protocols.base import FlextTargetLdapProtocolsBase


__all__: tuple[str, ...] = ("FlextTargetLdapProtocolsBase",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextTargetLdapProtocolsBase": ".base"}),
    public_exports=__all__,
)
