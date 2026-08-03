# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .client import FlextTargetLdapClient as FlextTargetLdapClient
    from .service_runtime import (
        FlextTargetLdapServiceRuntime as FlextTargetLdapServiceRuntime,
    )
    from .settings import (
        create_default_ldap_target_config as create_default_ldap_target_config,
    )
    from .settings import validate_ldap_target_config as validate_ldap_target_config

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".client": ("FlextTargetLdapClient",),
    ".service_runtime": ("FlextTargetLdapServiceRuntime",),
    ".settings": ("create_default_ldap_target_config", "validate_ldap_target_config"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextTargetLdapClient",
    "FlextTargetLdapServiceRuntime",
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
