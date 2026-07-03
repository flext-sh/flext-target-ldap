# AUTO-GENERATED FILE — Regenerate with: make gen
"""Constants package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._constants.base import (
        FlextTargetLdapConstantsBase as FlextTargetLdapConstantsBase,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".base": ("FlextTargetLdapConstantsBase",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
