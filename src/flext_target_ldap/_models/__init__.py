# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Models package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .processing_result import FlextTargetLdapProcessingCounters
    from .sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )
__all__: tuple[str, ...] = (
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingCounters",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
