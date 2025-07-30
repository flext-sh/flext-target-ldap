"""FLEXT Target LDAP - Wrapper for flext-meltano consolidated implementation.

CONSOLIDATION: This project is now a library wrapper that imports the real
Singer/Meltano/DBT consolidated implementations from flext-meltano to eliminate
code duplication across the FLEXT ecosystem.

This follows the architectural principle:
- flext-* projects are LIBRARIES, not services
- tap/target/dbt/ext are Meltano plugins
- Real implementations are in flext-meltano

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import local implementations (not from flext-meltano yet - fallback imports removed as per CLAUDE.md)
from flext_target_ldap.application.orchestrator import (
    LDAPTargetOrchestrator as FlextLDAPTargetOrchestrator,
)
from flext_target_ldap.config import TargetLDAPConfig
from flext_target_ldap.target import TargetLDAP

# Backward compatibility aliases
FlextTargetLDAP = TargetLDAP
FlextTargetLDAPConfig = TargetLDAPConfig
LDAPTarget = TargetLDAP
TargetConfig = TargetLDAPConfig

__version__ = "0.9.0-wrapper"

__all__ = [
    # Consolidated Orchestrator
    "FlextLDAPTargetOrchestrator",
    # Backward compatibility
    "FlextTargetLDAP",
    "FlextTargetLDAPConfig",
    "LDAPTarget",
    "TargetConfig",
    "TargetLDAP",
    "TargetLDAPConfig",
    "__version__",
]
