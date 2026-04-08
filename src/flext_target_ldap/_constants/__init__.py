# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Constants package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_ldap._constants.base as _flext_target_ldap__constants_base

    base = _flext_target_ldap__constants_base
    from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase
_LAZY_IMPORTS = {
    "FlextTargetLdapConstantsBase": (
        "flext_target_ldap._constants.base",
        "FlextTargetLdapConstantsBase",
    ),
    "base": "flext_target_ldap._constants.base",
}

__all__ = [
    "FlextTargetLdapConstantsBase",
    "base",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
