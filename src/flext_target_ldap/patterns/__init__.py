# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Patterns package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextTargetLdapDataTransformer": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapDataTransformer",
    ),
    "FlextTargetLdapEntryManager": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapEntryManager",
    ),
    "FlextTargetLdapSchemaMapper": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapSchemaMapper",
    ),
    "FlextTargetLdapTypeConverter": (
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapTypeConverter",
    ),
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "ldap_patterns": "flext_target_ldap.patterns.ldap_patterns",
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
