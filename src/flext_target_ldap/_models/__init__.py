# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .processing_result import (
        FlextTargetLdapProcessingCounters as FlextTargetLdapProcessingCounters,
    )
    from .sinks import FlextTargetLdapBaseSink as FlextTargetLdapBaseSink
    from .sinks import FlextTargetLdapGroupsSink as FlextTargetLdapGroupsSink
    from .sinks import (
        FlextTargetLdapOrganizationalUnitsSink as FlextTargetLdapOrganizationalUnitsSink,
    )
    from .sinks import (
        FlextTargetLdapProcessingResult as FlextTargetLdapProcessingResult,
    )
    from .sinks import FlextTargetLdapSink as FlextTargetLdapSink
    from .sinks import FlextTargetLdapTarget as FlextTargetLdapTarget
    from .sinks import FlextTargetLdapUsersSink as FlextTargetLdapUsersSink

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".processing_result": ("FlextTargetLdapProcessingCounters",),
    ".sinks": (
        "FlextTargetLdapBaseSink",
        "FlextTargetLdapGroupsSink",
        "FlextTargetLdapOrganizationalUnitsSink",
        "FlextTargetLdapProcessingResult",
        "FlextTargetLdapSink",
        "FlextTargetLdapTarget",
        "FlextTargetLdapUsersSink",
    ),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingCounters",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
