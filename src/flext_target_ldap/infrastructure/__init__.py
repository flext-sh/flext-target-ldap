"""LDAP infrastructure module using flext-core patterns."""

from __future__ import annotations

from flext_target_ldap.infrastructure.di_container import (
    configure_flext_target_ldap_dependencies,
    get_flext_target_ldap_container,
    get_flext_target_ldap_service,
)

__all__: list[str] = [
    "configure_flext_target_ldap_dependencies",
    "get_flext_target_ldap_container",
    "get_flext_target_ldap_service",
]
