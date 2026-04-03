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

    sinks = _flext_target_ldap__models_sinks

    _ = (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingCounters,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
        processing_result,
        sinks,
    )
_LAZY_IMPORTS = {
    "FlextTargetLdapBaseSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapGroupsSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapOrganizationalUnitsSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapProcessingCounters": "flext_target_ldap._models.processing_result",
    "FlextTargetLdapProcessingResult": "flext_target_ldap._models.sinks",
    "FlextTargetLdapSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapTarget": "flext_target_ldap._models.sinks",
    "FlextTargetLdapUsersSink": "flext_target_ldap._models.sinks",
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
