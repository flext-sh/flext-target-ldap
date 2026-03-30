# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""LDAP application module using flext-core patterns.

This module provides application orchestration components for LDAP target
operations, following flext-core architectural patterns and principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap.application import orchestrator as orchestrator
    from flext_target_ldap.application.orchestrator import (
        FlextTargetLdapOrchestrator as FlextTargetLdapOrchestrator,
        logger as logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapOrchestrator": [
        "flext_target_ldap.application.orchestrator",
        "FlextTargetLdapOrchestrator",
    ],
    "logger": ["flext_target_ldap.application.orchestrator", "logger"],
    "orchestrator": ["flext_target_ldap.application.orchestrator", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextTargetLdapOrchestrator",
    "logger",
    "orchestrator",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
