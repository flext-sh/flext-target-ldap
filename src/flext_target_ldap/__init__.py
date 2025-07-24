"""FLEXT TARGET LDAP - Singer LDAP Data Loading with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Singer LDAP Target with simplified public API:
- All common imports available from root: from flext_target_ldap import TargetLDAP
- Built on flext-core foundation for robust LDAP integration
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

# Import from flext-core for foundational patterns
# Re-export commonly used imports from flext-core
# 🚨 ARCHITECTURAL COMPLIANCE
from flext_target_ldap.infrastructure.di_container import get_service_result, get_domain_entity, get_field
ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()
BaseConfig,
BaseConfig as LDAPBaseConfig,  # Configuration base
DomainBaseModel,
DomainBaseModel as BaseModel,  # Base for LDAP models
DomainError as LDAPError,  # LDAP-specific errors
ServiceResult,
ValidationError as ValidationError,  # Validation errors
)

    # Singer Target exports - simplified imports
    from flext_target_ldap.target import TargetLDAP

    try:
    __version__ = importlib.metadata.version("flext-target-ldap")
    except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

    __version_info__= tuple(int(x) for x in __version__.split(".") if x.isdigit())


    class FlextTargetLDAPDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT TARGET LDAP import changes."""


    def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
f"⚠️  DEPRECATED IMPORT: {old_import}",
f"✅ USE INSTEAD: {new_import}",
"🔗 This will be removed in version 1.0.0",
 "📖 See FLEXT TARGET LDAP docs for migration guide",
  ]
   warnings.warn(
   "\n".join(message_parts),
    FlextTargetLDAPDeprecationWarning,
    stacklevel = 3,
    )


        # ================================
        # SIMPLIFIED PUBLIC API EXPORTS
        # ================================

        # LDAP Client exports - simplified imports
        with contextlib.suppress(ImportError):
    from flext_target_ldap.client import LDAPClient as TargetLDAPClient

        # LDAP Sinks exports - simplified imports
        with contextlib.suppress(ImportError):
    from flext_target_ldap.sinks import (
    GroupsSink as LDAPGroupSink,
    OrganizationalUnitsSink as LDAPOUSink,
    UsersSink as LDAPUserSink,
    )

        # ================================
        # PUBLIC API EXPORTS
        # ================================

        __all__ = [
    "BaseModel",  # from flext_target_ldap import BaseModel
    # Deprecation utilities
    "FlextTargetLDAPDeprecationWarning",
    # Core Patterns (from flext-core)
    "LDAPBaseConfig",  # from flext_target_ldap import LDAPBaseConfig
    "LDAPError",  # from flext_target_ldap import LDAPError
    # LDAP Sinks (simplified access)
    "LDAPGroupSink",  # from flext_target_ldap import LDAPGroupSink
    "LDAPOUSink",  # from flext_target_ldap import LDAPOUSink
    "LDAPUserSink",  # from flext_target_ldap import LDAPUserSink
    "ServiceResult",  # from flext_target_ldap import ServiceResult
    # Main Singer Target (simplified access)
    "TargetLDAP",  # from flext_target_ldap import TargetLDAP
    "TargetLDAPClient",  # from flext_target_ldap import TargetLDAPClient
    "ValidationError",  # from flext_target_ldap import ValidationError
    # Version
    "__version__",
    "__version_info__",
]
