# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_TARGET_LDAP_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._constants.base": ("FlextTargetLdapConstantsBase",),
        "._models.processing_result": ("FlextTargetLdapProcessingCounters",),
        "._models.sinks": (
            "FlextTargetLdapBaseSink",
            "FlextTargetLdapGroupsSink",
            "FlextTargetLdapOrganizationalUnitsSink",
            "FlextTargetLdapProcessingResult",
            "FlextTargetLdapSink",
            "FlextTargetLdapTarget",
            "FlextTargetLdapUsersSink",
        ),
        "._utilities.client": ("FlextTargetLdapClient",),
        "._utilities.service_runtime": ("FlextTargetLdapServiceRuntime",),
        "._utilities.settings": (
            "create_default_ldap_target_config",
            "validate_ldap_target_config",
        ),
        ".api": (
            "FlextTargetLdap",
            "target_ldap",
        ),
        ".application.orchestrator": ("FlextTargetLdapOrchestrator",),
        ".constants": (
            "FlextTargetLdapConstants",
            "c",
        ),
        ".models": (
            "FlextTargetLdapModels",
            "m",
        ),
        ".protocols": (
            "FlextTargetLdapProtocols",
            "p",
        ),
        ".settings": ("FlextTargetLdapSettings",),
        ".typings": (
            "FlextTargetLdapTypes",
            "t",
        ),
        ".utilities": (
            "FlextTargetLdapUtilities",
            "u",
        ),
    },
)

__all__: list[str] = ["FLEXT_TARGET_LDAP_LAZY_IMPORTS_PART_01"]
