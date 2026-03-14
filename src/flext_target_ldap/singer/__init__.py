# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_target_ldap.singer.catalog import (
        SingerLDAPCatalogEntry,
        SingerLDAPCatalogManager,
    )
    from flext_target_ldap.singer.stream import (
        LDAPStreamProcessingStats,
        SingerLDAPStreamProcessor,
    )
    from flext_target_ldap.singer.target import SingerTargetLDAP, logger

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "LDAPStreamProcessingStats": (
        "flext_target_ldap.singer.stream",
        "LDAPStreamProcessingStats",
    ),
    "SingerLDAPCatalogEntry": (
        "flext_target_ldap.singer.catalog",
        "SingerLDAPCatalogEntry",
    ),
    "SingerLDAPCatalogManager": (
        "flext_target_ldap.singer.catalog",
        "SingerLDAPCatalogManager",
    ),
    "SingerLDAPStreamProcessor": (
        "flext_target_ldap.singer.stream",
        "SingerLDAPStreamProcessor",
    ),
    "SingerTargetLDAP": ("flext_target_ldap.singer.target", "SingerTargetLDAP"),
    "logger": ("flext_target_ldap.singer.target", "logger"),
}

__all__ = [
    "LDAPStreamProcessingStats",
    "SingerLDAPCatalogEntry",
    "SingerLDAPCatalogManager",
    "SingerLDAPStreamProcessor",
    "SingerTargetLDAP",
    "logger",
]


def __getattr__(name: str) -> t.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
