"""FLEXT Target LDAP - Infrastructure layer components.

LDAP infrastructure module using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

from flext_target_ldap.infrastructure.di_container import (
    configure_flext_target_ldap_dependencies,
    get_flext_target_ldap_container,
    get_flext_target_ldap_service,
)

__all__: FlextTypes.Core.StringList = [
    "configure_flext_target_ldap_dependencies",
    "get_flext_target_ldap_container",
    "get_flext_target_ldap_service",
]
