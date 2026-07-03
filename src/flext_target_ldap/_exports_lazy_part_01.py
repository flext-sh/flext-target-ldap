# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_TARGET_LDAP_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._constants": ("_constants",),
        "._models": ("_models",),
        "._utilities": ("_utilities",),
        ".api": (
            "FlextTargetLdap",
            "target_ldap",
        ),
        ".application": ("application",),
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
        "flext_core": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)

__all__: list[str] = ["FLEXT_TARGET_LDAP_LAZY_IMPORTS_PART_01"]
