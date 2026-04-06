# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_ldap._models.processing_result as _flext_target_ldap__models_processing_result

    processing_result = _flext_target_ldap__models_processing_result
    import flext_target_ldap._models.sinks as _flext_target_ldap__models_sinks
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )

    sinks = _flext_target_ldap__models_sinks
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )
_LAZY_IMPORTS = {
    "FlextTargetLdapBaseSink": (
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapBaseSink",
    ),
    "FlextTargetLdapGroupsSink": (
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapGroupsSink",
    ),
    "FlextTargetLdapOrganizationalUnitsSink": (
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapOrganizationalUnitsSink",
    ),
    "FlextTargetLdapProcessingCounters": (
        "flext_target_ldap._models.processing_result",
        "FlextTargetLdapProcessingCounters",
    ),
    "FlextTargetLdapProcessingResult": (
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapProcessingResult",
    ),
    "FlextTargetLdapSink": ("flext_target_ldap._models.sinks", "FlextTargetLdapSink"),
    "FlextTargetLdapTarget": (
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapTarget",
    ),
    "FlextTargetLdapUsersSink": (
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapUsersSink",
    ),
    "processing_result": "flext_target_ldap._models.processing_result",
    "sinks": "flext_target_ldap._models.sinks",
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
    "processing_result",
    "sinks",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
