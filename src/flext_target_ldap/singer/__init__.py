# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Singer package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextTargetLdapCatalogManager": (
        "flext_target_ldap.singer.catalog",
        "FlextTargetLdapCatalogManager",
    ),
    "FlextTargetLdapSingerTarget": (
        "flext_target_ldap.singer.target",
        "FlextTargetLdapSingerTarget",
    ),
    "FlextTargetLdapStreamProcessingStats": (
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessingStats",
    ),
    "FlextTargetLdapStreamProcessor": (
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessor",
    ),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
