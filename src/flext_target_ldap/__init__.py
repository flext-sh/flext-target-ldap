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

from flext_meltano.orchestration.targets import FlextLDAPTargetOrchestrator

# Import consolidated implementations from flext-meltano
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.targets.ldap import TargetLDAP, TargetLDAPConfig

# Backward compatibility aliases
FlextTargetLDAP = TargetLDAP
FlextTargetLDAPConfig = TargetLDAPConfig
LDAPTarget = TargetLDAP
TargetConfig = TargetLDAPConfig

__version__ = "0.8.0-wrapper"

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
