"""FLEXT LDAP Target for Meltano.

Enterprise LDAP target for loading data into LDAP directories with FLEXT ecosystem integration.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata

from flext_core import FlextLogger, FlextModels, FlextResult, FlextTypes
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
from flext_target_ldap.target_config import TargetLdapConfig as FlextTargetLDAPConfig
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
)

try:
    __version__ = importlib.metadata.version("flext-target-ldap")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTypes.Core.StringList = [
    "FlextLogger",
    "FlextModels",
    "FlextResult",
    "FlextTargetLDAPConfig",
    "FlextTargetLDAPConnectionError",
    "FlextTargetLDAPError",
    "FlextTargetLDAPService",
    "FlextTargetLDAPValidationError",
    "FlextTypes",
    "GroupsSink",
    "LDAPBaseSink",
    "LDAPClient",
    "LDAPProcessingResult",
    "LDAPTargetClient",
    "LDAPTargetModel",
    "LDAPTargetRecord",
    "OrganizationalUnitsSink",
    "Sink",
    "Target",
    "TargetLDAP",
    "TargetLdap",
    "UsersSink",
    "__version__",
    "__version_info__",
]
