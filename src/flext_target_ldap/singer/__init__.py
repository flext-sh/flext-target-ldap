"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

from flext_target_ldap.singer.catalog import SingerLDAPCatalogManager
from flext_target_ldap.singer.stream import SingerLDAPStreamProcessor
from flext_target_ldap.singer.target import SingerTargetLDAP

__all__: FlextTypes.Core.StringList = [
    "SingerLDAPCatalogManager",
    "SingerLDAPStreamProcessor",
    "SingerTargetLDAP",
]
