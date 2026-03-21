# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Target LDAP - Infrastructure layer components.

LDAP infrastructure module using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_target_ldap.infrastructure.di_container import (
        configure_flext_target_ldap_dependencies,
        get_flext_target_ldap_container,
        get_flext_target_ldap_service,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "configure_flext_target_ldap_dependencies": ("flext_target_ldap.infrastructure.di_container", "configure_flext_target_ldap_dependencies"),
    "get_flext_target_ldap_container": ("flext_target_ldap.infrastructure.di_container", "get_flext_target_ldap_container"),
    "get_flext_target_ldap_service": ("flext_target_ldap.infrastructure.di_container", "get_flext_target_ldap_service"),
}

__all__ = [
    "configure_flext_target_ldap_dependencies",
    "get_flext_target_ldap_container",
    "get_flext_target_ldap_service",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
