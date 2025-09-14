"""Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

from flext_target_ldap.application.orchestrator import LDAPTargetOrchestrator

"""LDAP application module using flext-core patterns.

This module provides application orchestration components for LDAP target
operations, following flext-core architectural patterns and principles.
"""


__all__: FlextTypes.Core.StringList = [
    "LDAPTargetOrchestrator",
]
