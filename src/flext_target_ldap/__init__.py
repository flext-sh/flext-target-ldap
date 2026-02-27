"""FLEXT LDAP Target for Meltano.

Enterprise LDAP target for loading data into LDAP directories with FLEXT ecosystem integration.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap.__version__ import (
    __version__,
    __version_info__,
)

from flext_target_ldap.constants import FlextTargetLdapConstants, c
# from flext_target_ldap.config import FlextTargetLdapSettings as FlextTargetLDAPSettings  # Temporarily disabled
# from flext_target_ldap.config import FlextTargetLdapSettings as FlextTargetLDAPSettings  # Temporarily disabled
from flext_target_ldap.models import (
    FlextTargetLdapModels,
    m,
)
from flext_target_ldap.protocols import (
    FlextTargetLdapProtocols,
)
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
    LdapTargetClient,
    TargetLdap,
)
from flext_target_ldap.target_exceptions import (
    FlextTargetLdapConnectionError,
    FlextTargetLdapError,
    FlextTargetLdapValidationError,
)
from flext_target_ldap.target_models import (
    LdapBatchProcessingModel,
    LdapEntryModel,
)
from flext_target_ldap.target_services import (
    LdapTargetApiService,
    LdapTransformationService,
    LdapTransformationServiceProtocol,
)
from flext_target_ldap.typings import FlextTargetLdapTypes, t
from flext_target_ldap.utilities import (
    FlextTargetLdapUtilities,
)

# Backward compatibility aliases
LdapBaseSink = LDAPBaseSink
LdapGroupsSink = GroupsSink
LdapUsersSink = UsersSink

__all__ = [
    "FlextTargetLdapConstants",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapError",
    "FlextTargetLdapModels",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapValidationError",
    "GroupsSink",
    "LDAPBaseSink",
    "LDAPProcessingResult",
    "LdapBaseSink",
    "LdapBatchProcessingModel",
    "LdapEntryModel",
    "LdapGroupsSink",
    "LdapTargetApiService",
    "LdapTargetClient",
    "LdapTransformationService",
    "LdapTransformationServiceProtocol",
    "LdapUsersSink",
    "OrganizationalUnitsSink",
    "Sink",
    "Target",
    "TargetLdap",
    "UsersSink",
    "__version__",
    "__version_info__",
    "c",
    "m",
    "t",
]
