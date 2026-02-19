"""FLEXT LDAP Target for Meltano.

Enterprise LDAP target for loading data into LDAP directories with FLEXT ecosystem integration.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# from flext_core import  FlextLogger, FlextModels, FlextResult  # Temporarily disabled
from flext_target_ldap.__version__ import (
    __version__,
    __version_info__,
)

# from flext_target_ldap.config import FlextTargetLdapSettings as FlextTargetLDAPSettings  # Temporarily disabled
from flext_target_ldap.models import (
    FlextTargetLdapModels,
    m,
    m_target_ldap,
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
from flext_target_ldap.utilities import (
    FlextTargetLdapUtilities,
)

__all__ = [
    "FlextTargetLDAPConnectionError",
    "FlextTargetLDAPError",
    "FlextTargetLDAPService",
    "FlextTargetLDAPValidationError",
    "FlextTargetLdapModels",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
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
    "m",
    "m_target_ldap",
]
