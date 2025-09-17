"""LDAP patterns module using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes
from flext_target_ldap.patterns.ldap_patterns import (
    LDAPDataTransformer,
    LDAPEntryManager,
    LDAPSchemaMapper,
    LDAPTypeConverter,
)

__all__: FlextTypes.Core.StringList = [
    "LDAPDataTransformer",
    "LDAPEntryManager",
    "LDAPSchemaMapper",
    "LDAPTypeConverter",
]
