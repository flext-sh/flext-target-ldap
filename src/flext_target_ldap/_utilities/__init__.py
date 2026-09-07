# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .client import FlextTargetLdapClient
    from .service_runtime import FlextTargetLdapServiceRuntime
    from .settings import create_default_ldap_target_config, validate_ldap_target_config
__all__: tuple[str, ...] = (
    "FlextTargetLdapClient",
    "FlextTargetLdapServiceRuntime",
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".client": ("FlextTargetLdapClient",),
            ".service_runtime": ("FlextTargetLdapServiceRuntime",),
            ".settings": (
                "create_default_ldap_target_config",
                "validate_ldap_target_config",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
