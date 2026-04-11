# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api_service": ("FlextTargetLdapApiService",),
        ".client": ("FlextTargetLdapClient",),
        ".service_runtime": ("FlextTargetLdapServiceRuntime",),
        ".services": (
            "FlextTargetLdapConnectionService",
            "FlextTargetLdapTransformationService",
        ),
        ".settings": (
            "FlextTargetLdapConfigFactory",
            "create_default_ldap_target_config",
            "validate_ldap_target_config",
        ),
        ".transformation": (
            "FlextTargetLdapMigrationValidator",
            "FlextTargetLdapTransformationEngine",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
