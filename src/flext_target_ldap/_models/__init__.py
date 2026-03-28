# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal models subpackage for flext-target-ldap."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
        logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapBaseSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapBaseSink"],
    "FlextTargetLdapGroupsSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapGroupsSink"],
    "FlextTargetLdapOrganizationalUnitsSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapOrganizationalUnitsSink"],
    "FlextTargetLdapProcessingCounters": ["flext_target_ldap._models.processing_result", "FlextTargetLdapProcessingCounters"],
    "FlextTargetLdapProcessingResult": ["flext_target_ldap._models.sinks", "FlextTargetLdapProcessingResult"],
    "FlextTargetLdapSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapSink"],
    "FlextTargetLdapTarget": ["flext_target_ldap._models.sinks", "FlextTargetLdapTarget"],
    "FlextTargetLdapUsersSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapUsersSink"],
    "logger": ["flext_target_ldap._models.sinks", "logger"],
}

__all__ = [
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingCounters",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
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
