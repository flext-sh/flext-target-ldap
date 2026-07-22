# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient as FlextTargetLdapClient,
    )
    from flext_target_ldap._utilities.service_runtime import (
        FlextTargetLdapServiceRuntime as FlextTargetLdapServiceRuntime,
    )
    from flext_target_ldap._utilities.settings import (
        create_default_ldap_target_config as create_default_ldap_target_config,
        validate_ldap_target_config as validate_ldap_target_config,
    )
_LAZY_IMPORTS = build_lazy_import_map({
    ".client": ("FlextTargetLdapClient",),
    ".service_runtime": ("FlextTargetLdapServiceRuntime",),
    ".settings": ("create_default_ldap_target_config", "validate_ldap_target_config"),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
