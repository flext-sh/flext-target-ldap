"""FLEXT LDAP Target for Meltano.

Enterprise LDAP target for loading data into LDAP directories with FLEXT ecosystem integration.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata

from flext_core import FlextLogger, FlextModels, FlextResult, FlextTypes
from flext_meltano import Sink, Target

from flext_target_ldap.target_client import FlextTargetLDAP, LDAPTargetClient
from flext_target_ldap.target_config import FlextTargetLDAPConfig, LDAPTargetConstants
from flext_target_ldap.target_exceptions import (
    FlextTargetLDAPConnectionError,
    FlextTargetLDAPError,
    FlextTargetLDAPValidationError,
)
from flext_target_ldap.target_models import LDAPTargetModel, LDAPTargetRecord
from flext_target_ldap.target_services import FlextTargetLDAPService

try:
    __version__ = importlib.metadata.version("flext-target-ldap")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTypes.Core.StringList = [
    # FLEXT ecosystem integration
    "FlextLogger",
    "FlextModels",
    "FlextResult",
    # Core target functionality
    "FlextTargetLDAP",
    # Configuration
    "FlextTargetLDAPConfig",
    # Exceptions
    "FlextTargetLDAPConnectionError",
    "FlextTargetLDAPError",
    "FlextTargetLDAPService",
    "FlextTargetLDAPValidationError",
    "FlextTypes",
    "LDAPTargetClient",
    "LDAPTargetConstants",
    # Models
    "LDAPTargetModel",
    "LDAPTargetRecord",
    # Meltano integration
    "Sink",
    "Target",
    # Version info
    "__version__",
    "__version_info__",
]
