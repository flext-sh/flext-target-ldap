# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap.singer import (
        catalog as catalog,
        stream as stream,
        target as target,
    )
    from flext_target_ldap.singer.catalog import (
        FlextTargetLdapCatalogManager as FlextTargetLdapCatalogManager,
    )
    from flext_target_ldap.singer.stream import (
        FlextTargetLdapStreamProcessingStats as FlextTargetLdapStreamProcessingStats,
        FlextTargetLdapStreamProcessor as FlextTargetLdapStreamProcessor,
    )
    from flext_target_ldap.singer.target import (
        FlextTargetLdapSingerTarget as FlextTargetLdapSingerTarget,
        logger as logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapCatalogManager": [
        "flext_target_ldap.singer.catalog",
        "FlextTargetLdapCatalogManager",
    ],
    "FlextTargetLdapSingerTarget": [
        "flext_target_ldap.singer.target",
        "FlextTargetLdapSingerTarget",
    ],
    "FlextTargetLdapStreamProcessingStats": [
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessingStats",
    ],
    "FlextTargetLdapStreamProcessor": [
        "flext_target_ldap.singer.stream",
        "FlextTargetLdapStreamProcessor",
    ],
    "catalog": ["flext_target_ldap.singer.catalog", ""],
    "logger": ["flext_target_ldap.singer.target", "logger"],
    "stream": ["flext_target_ldap.singer.stream", ""],
    "target": ["flext_target_ldap.singer.target", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextTargetLdapCatalogManager",
    "FlextTargetLdapSingerTarget",
    "FlextTargetLdapStreamProcessingStats",
    "FlextTargetLdapStreamProcessor",
    "catalog",
    "logger",
    "stream",
    "target",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
