"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations
from flext_core import FlextTypes


"""Enterprise Singer Target for LDAP directory data loading."""
"""
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""


import importlib.metadata

# === FLEXT-CORE IMPORTS ===
from flext_core import FlextResult, FlextModels, FlextLogger

from flext_meltano import Sink, Target

# === NEW PEP8 REORGANIZED IMPORTS ===
# Configuration (consolidated and descriptive)
from flext_target_ldap.target_config import (
    LdapTargetConnectionSettings,
    LdapTargetMappingSettings,
    LdapTargetOperationSettings,
    TargetLdapConfig,
    create_default_ldap_target_config,
    validate_ldap_target_config,
)

# Client and target implementation (consolidated)
from flext_target_ldap.target_client import (
    LdapBaseSink,
    LdapGroupsSink,
    LdapOrganizationalUnitsSink,
    LdapProcessingResult,
    LdapSearchEntry,
    LdapTargetClient,
    LdapUsersSink,
    TargetLdap,
    main,
)

# Domain models (LDAP-specific)
from flext_target_ldap.target_models import (
    LdapAttributeMappingModel,
    LdapBatchProcessingModel,
    LdapEntryModel,
    LdapObjectClassModel,
    LdapOperationStatisticsModel,
    LdapTransformationResultModel,
)

# Exceptions (factory pattern - zero duplication)
from flext_target_ldap.target_exceptions import (
    FlextTargetLdapAuthenticationError,
    FlextTargetLdapConfigurationError,
    FlextTargetLdapConnectionError,
    FlextTargetLdapError,
    FlextTargetLdapLoadError,
    FlextTargetLdapProcessingError,
    FlextTargetLdapSchemaError,
    FlextTargetLdapTimeoutError,
    FlextTargetLdapValidationError,
    FlextTargetLdapWriteError,
)

# Services (orchestration, API, transformation)
from flext_target_ldap.target_services import (
    LdapConnectionService,
    LdapTargetApiService,
    LdapTargetOrchestrator,
    LdapTransformationService,
    create_ldap_target,
    load_groups_to_ldap,
    load_users_to_ldap,
    test_ldap_connection,
)

# === BACKWARD COMPATIBILITY ALIASES ===
# Maintain compatibility with existing code while using new PEP8 names internally

# Main classes (preferred new names with backward compatibility)
FlextLDAPTargetOrchestrator = LdapTargetOrchestrator
FlextTargetLDAP = TargetLdap
FlextTargetLDAPConfig = TargetLdapConfig
LDAPTarget = TargetLdap
TargetConfig = TargetLdapConfig
TargetLDAP = TargetLdap
TargetLDAPConfig = TargetLdapConfig

# Client classes (backward compatibility)
LDAPClient = LdapTargetClient
LDAPSearchEntry = LdapSearchEntry
LDAPProcessingResult = LdapProcessingResult

# Sink classes (backward compatibility)
LDAPBaseSink = LdapBaseSink
UsersSink = LdapUsersSink
GroupsSink = LdapGroupsSink
OrganizationalUnitsSink = LdapOrganizationalUnitsSink

# Model aliases (backward compatibility)
TransformationRule = LdapAttributeMappingModel
TransformationResult = LdapTransformationResultModel
LDAPConnectionSettings = LdapTargetConnectionSettings
LDAPOperationSettings = LdapTargetOperationSettings

# Function aliases (backward compatibility)
create_target = create_ldap_target
test_connection = test_ldap_connection

# Version following semantic versioning
try:
    __version__ = importlib.metadata.version("flext-target-ldap")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0-enterprise"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Complete public API exports (organized by category)
__all__: FlextTypes.Core.StringList = [
    # === FLEXT-CORE RE-EXPORTS ===
    "FlextResult",
    "FlextModels",
    "FlextLogger",
    # === FLEXT-MELTANO RE-EXPORTS ===
    "Sink",
    "Target",
    # === NEW PEP8 REORGANIZED CLASSES ===
    # Configuration
    "LdapTargetConnectionSettings",
    "LdapTargetMappingSettings",
    "LdapTargetOperationSettings",
    "TargetLdapConfig",
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
    # Client and target
    "LdapBaseSink",
    "LdapGroupsSink",
    "LdapOrganizationalUnitsSink",
    "LdapProcessingResult",
    "LdapSearchEntry",
    "LdapTargetClient",
    "LdapUsersSink",
    "TargetLdap",
    "main",
    # Domain models
    "LdapAttributeMappingModel",
    "LdapBatchProcessingModel",
    "LdapEntryModel",
    "LdapObjectClassModel",
    "LdapOperationStatisticsModel",
    "LdapTransformationResultModel",
    # Exceptions
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapError",
    "FlextTargetLdapLoadError",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapSchemaError",
    "FlextTargetLdapTimeoutError",
    "FlextTargetLdapValidationError",
    "FlextTargetLdapWriteError",
    # Services
    "LdapConnectionService",
    "LdapTargetApiService",
    "LdapTargetOrchestrator",
    "LdapTransformationService",
    "create_ldap_target",
    "load_groups_to_ldap",
    "load_users_to_ldap",
    "test_ldap_connection",
    # === BACKWARD COMPATIBILITY ALIASES ===
    "FlextLDAPTargetOrchestrator",
    "FlextTargetLDAP",
    "FlextTargetLDAPConfig",
    "LDAPTarget",
    "TargetConfig",
    "TargetLDAP",
    "TargetLDAPConfig",
    # Client aliases
    "LDAPClient",
    "LDAPSearchEntry",
    "LDAPProcessingResult",
    # Sink aliases
    "LDAPBaseSink",
    "UsersSink",
    "GroupsSink",
    "OrganizationalUnitsSink",
    # Model aliases
    "TransformationRule",
    "TransformationResult",
    "LDAPConnectionSettings",
    "LDAPOperationSettings",
    # Function aliases
    "create_target",
    "test_connection",
    # === METADATA ===
    "__version__",
    "__version_info__",
]
