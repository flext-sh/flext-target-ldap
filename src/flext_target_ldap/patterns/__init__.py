# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""LDAP patterns module using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap.patterns import ldap_patterns as ldap_patterns
    from flext_target_ldap.patterns.ldap_patterns import (
        FlextTargetLdapDataTransformer as FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager as FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper as FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter as FlextTargetLdapTypeConverter,
        logger as logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapDataTransformer": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapDataTransformer",
    ],
    "FlextTargetLdapEntryManager": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapEntryManager",
    ],
    "FlextTargetLdapSchemaMapper": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapSchemaMapper",
    ],
    "FlextTargetLdapTypeConverter": [
        "flext_target_ldap.patterns.ldap_patterns",
        "FlextTargetLdapTypeConverter",
    ],
    "ldap_patterns": ["flext_target_ldap.patterns.ldap_patterns", ""],
    "logger": ["flext_target_ldap.patterns.ldap_patterns", "logger"],
}

_EXPORTS: Sequence[str] = [
    "FlextTargetLdapDataTransformer",
    "FlextTargetLdapEntryManager",
    "FlextTargetLdapSchemaMapper",
    "FlextTargetLdapTypeConverter",
    "ldap_patterns",
    "logger",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
