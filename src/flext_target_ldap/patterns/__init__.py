"""LDAP patterns module using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.patterns.ldap_patterns import (
    LDAPDataTransformer,
    LDAPEntryManager,
    LDAPSchemaMapper,
    LDAPTypeConverter,
)
from flext_target_ldap.typings import FlextTargetLdapTypes

__all__: FlextTargetLdapTypes.Core.StringList = [
    "FlextTypes.Dict",
    "LDAPDataTransformer",
    "LDAPEntryManager",
    "LDAPSchemaMapper",
    "LDAPTypeConverter",
]
