# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_target_ldap.singer.catalog import *
    from flext_target_ldap.singer.stream import *
    from flext_target_ldap.singer.target import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTargetLdapCatalogManager": "flext_target_ldap.singer.catalog",
    "FlextTargetLdapSingerTarget": "flext_target_ldap.singer.target",
    "FlextTargetLdapStreamProcessingStats": "flext_target_ldap.singer.stream",
    "FlextTargetLdapStreamProcessor": "flext_target_ldap.singer.stream",
    "catalog": "flext_target_ldap.singer.catalog",
    "logger": "flext_target_ldap.singer.target",
    "stream": "flext_target_ldap.singer.stream",
    "target": "flext_target_ldap.singer.target",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
