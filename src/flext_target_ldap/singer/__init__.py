# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_target_ldap.singer.catalog import FlextTargetLdapCatalogManager
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import FlextTargetLdapSingerTarget, logger

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "FlextTargetLdapCatalogManager": ("flext_target_ldap.singer.catalog", "FlextTargetLdapCatalogManager"),
    "FlextTargetLdapSingerTarget": ("flext_target_ldap.singer.target", "FlextTargetLdapSingerTarget"),
    "FlextTargetLdapStreamProcessingStats": ("flext_target_ldap.singer.stream", "FlextTargetLdapStreamProcessingStats"),
    "FlextTargetLdapStreamProcessor": ("flext_target_ldap.singer.stream", "FlextTargetLdapStreamProcessor"),
    "logger": ("flext_target_ldap.singer.target", "logger"),
}

__all__ = [
    "FlextTargetLdapCatalogManager",
    "FlextTargetLdapSingerTarget",
    "FlextTargetLdapStreamProcessingStats",
    "FlextTargetLdapStreamProcessor",
    "logger",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
