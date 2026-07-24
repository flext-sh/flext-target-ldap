# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters as FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink as FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink as FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink as FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult as FlextTargetLdapProcessingResult,
        FlextTargetLdapSink as FlextTargetLdapSink,
        FlextTargetLdapTarget as FlextTargetLdapTarget,
        FlextTargetLdapUsersSink as FlextTargetLdapUsersSink,
    )
_LAZY_IMPORTS = build_lazy_import_map({
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
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
