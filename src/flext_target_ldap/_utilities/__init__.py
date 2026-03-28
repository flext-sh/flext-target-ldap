# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-ldap."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient,
        FlextTargetLdapSearchEntry,
    )
    from flext_target_ldap._utilities.config import (
        create_default_ldap_target_config,
        validate_ldap_target_config,
    )
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapApiService,
        FlextTargetLdapConnectionService,
        FlextTargetLdapOrchestrator,
        FlextTargetLdapTransformationService,
    )
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine,
        logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapApiService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapApiService",
    ],
    "FlextTargetLdapClient": [
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapClient",
    ],
    "FlextTargetLdapConnectionService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapConnectionService",
    ],
    "FlextTargetLdapMigrationValidator": [
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapMigrationValidator",
    ],
    "FlextTargetLdapOrchestrator": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapOrchestrator",
    ],
    "FlextTargetLdapSearchEntry": [
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapSearchEntry",
    ],
    "FlextTargetLdapTransformationEngine": [
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapTransformationEngine",
    ],
    "FlextTargetLdapTransformationService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapTransformationService",
    ],
    "create_default_ldap_target_config": [
        "flext_target_ldap._utilities.config",
        "create_default_ldap_target_config",
    ],
    "logger": ["flext_target_ldap._utilities.transformation", "logger"],
    "validate_ldap_target_config": [
        "flext_target_ldap._utilities.config",
        "validate_ldap_target_config",
    ],
}

__all__ = [
    "FlextTargetLdapApiService",
    "FlextTargetLdapClient",
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapOrchestrator",
    "FlextTargetLdapSearchEntry",
    "FlextTargetLdapTransformationEngine",
    "FlextTargetLdapTransformationService",
    "create_default_ldap_target_config",
    "logger",
    "validate_ldap_target_config",
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
