"""Version information for flext-target-ldap package.

This module contains version information for the flext-target-ldap package.
"""

from __future__ import annotations

# Import from centralized version management system
# 🚨 ARCHITECTURAL COMPLIANCE
from flext_target_ldap.infrastructure.di_container import (
    get_domain_entity,
    get_field,
    get_service_result,
)

ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()

__version__ = get_version()
__version_info__ = get_version_info()

# FLEXT Enterprise - Unified Versioning System
# Version is managed centrally in flext_core.version
# This maintains backward compatibility while eliminating duplication.
