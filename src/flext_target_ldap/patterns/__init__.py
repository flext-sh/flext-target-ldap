# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""LDAP patterns module using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_target_ldap.patterns import ldap_patterns
    from flext_target_ldap.patterns.ldap_patterns import (
        FlextTargetLdapDataTransformer,
        FlextTargetLdapEntryManager,
        FlextTargetLdapSchemaMapper,
        FlextTargetLdapTypeConverter,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTargetLdapDataTransformer": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapEntryManager": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapSchemaMapper": "flext_target_ldap.patterns.ldap_patterns",
    "FlextTargetLdapTypeConverter": "flext_target_ldap.patterns.ldap_patterns",
    "ldap_patterns": "flext_target_ldap.patterns.ldap_patterns",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
