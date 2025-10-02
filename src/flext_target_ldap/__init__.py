"""FLEXT LDAP Target for Meltano.

Enterprise LDAP target for loading data into LDAP directories with FLEXT ecosystem integration.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata
from typing import Final

from flext_core import FlextLogger, FlextModels, FlextResult, FlextTypes
from flext_target_ldap.config import FlextTargetLdapConfig as FlextTargetLDAPConfig
from flext_target_ldap.models import FlextTargetLdapModels
from flext_target_ldap.protocols import FlextTargetLdapProtocols
from flext_target_ldap.sinks import (
    GroupsSink,
    LDAPBaseSink,
    LDAPProcessingResult,
    OrganizationalUnitsSink,
    Sink,
    Target,
    UsersSink,
)
from flext_target_ldap.target_client import (
    LDAPClient,
    LdapTargetClient as LDAPTargetClient,
    TargetLDAP,
    TargetLdap,
)
from flext_target_ldap.target_exceptions import (
    FlextTargetLdapConnectionError as FlextTargetLDAPConnectionError,
    FlextTargetLdapError as FlextTargetLDAPError,
    FlextTargetLdapValidationError as FlextTargetLDAPValidationError,
)
from flext_target_ldap.target_models import (
    LdapBatchProcessingModel as LDAPTargetRecord,
    LdapEntryModel as LDAPTargetModel,
)
from flext_target_ldap.target_services import (
    LdapTargetApiService as FlextTargetLDAPService,
    LdapTransformationService,
    LdapTransformationServiceProtocol,
)
from flext_target_ldap.typings import FlextTargetLdapTypes
from flext_target_ldap.utilities import FlextTargetLdapUtilities
from flext_target_ldap.version import VERSION, FlextTargetLdapVersion

try:
    __version__ = importlib.metadata.version("flext-target-ldap")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

PROJECT_VERSION: Final[FlextTargetLdapVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "FlextLogger",
    "FlextModels",
    "FlextResult",
    "FlextTargetLDAPConfig",
    "FlextTargetLDAPConnectionError",
    "FlextTargetLDAPError",
    "FlextTargetLDAPService",
    "FlextTargetLDAPValidationError",
    "FlextTargetLdapModels",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapVersion",
    "FlextTypes",
    "GroupsSink",
    "LDAPBaseSink",
    "LDAPClient",
    "LDAPProcessingResult",
    "LDAPTargetClient",
    "LDAPTargetModel",
    "LDAPTargetRecord",
    "LdapTransformationService",
    "LdapTransformationServiceProtocol",
    "OrganizationalUnitsSink",
    "Sink",
    "Target",
    "TargetLDAP",
    "TargetLdap",
    "UsersSink",
    "__version__",
    "__version_info__",
]
