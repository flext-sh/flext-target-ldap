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
    TargetLDAP,
    TargetLdap,
)
from flext_target_ldap.target_client import (
    LdapTargetClient as LDAPTargetClient,
)
from flext_target_ldap.target_exceptions import (
    FlextTargetLdapConnectionError as FlextTargetLDAPConnectionError,
)
from flext_target_ldap.target_exceptions import (
    FlextTargetLdapError as FlextTargetLDAPError,
)
from flext_target_ldap.target_exceptions import (
    FlextTargetLdapValidationError as FlextTargetLDAPValidationError,
)
from flext_target_ldap.target_models import (
    LdapBatchProcessingModel as LDAPTargetRecord,
)
from flext_target_ldap.target_models import (
    LdapEntryModel as LDAPTargetModel,
)
from flext_target_ldap.target_services import (
    LdapTargetApiService as FlextTargetLDAPService,
)
from flext_target_ldap.target_services import (
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
