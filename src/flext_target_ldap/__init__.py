"""FLEXT LDAP Target for Meltano.

Enterprise LDAP target for loading data into LDAP directories with FLEXT ecosystem integration.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_target_ldap.__version__ import __version__, __version_info__
    from flext_target_ldap.constants import (
        FlextTargetLdapConstants,
        FlextTargetLdapConstants as c,
    )
    from flext_target_ldap.models import (
        FlextTargetLdapModels,
        FlextTargetLdapModels as m,
    )
    from flext_target_ldap.protocols import FlextTargetLdapProtocols
    from flext_target_ldap.sinks import (
        GroupsSink,
        GroupsSink as LdapGroupsSink,
        LDAPBaseSink,
        LDAPBaseSink as LdapBaseSink,
        LDAPProcessingResult,
        OrganizationalUnitsSink,
        Sink,
        Target,
        UsersSink,
        UsersSink as LdapUsersSink,
    )
    from flext_target_ldap.target_client import LdapTargetClient, TargetLdap
    from flext_target_ldap.target_exceptions import (
        FlextTargetLdapConnectionError,
        FlextTargetLdapError,
        FlextTargetLdapValidationError,
    )
    from flext_target_ldap.target_models import LdapBatchProcessingModel, LdapEntryModel
    from flext_target_ldap.target_services import (
        LdapTargetApiService,
        LdapTransformationService,
        LdapTransformationServiceProtocol,
    )
    from flext_target_ldap.typings import (
        FlextTargetLdapTypes,
        FlextTargetLdapTypes as t,
    )
    from flext_target_ldap.utilities import (
        FlextTargetLdapUtilities,
        FlextTargetLdapUtilities as u,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextTargetLdapConnectionError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapConnectionError",
    ),
    "FlextTargetLdapConstants": (
        "flext_target_ldap.constants",
        "FlextTargetLdapConstants",
    ),
    "FlextTargetLdapError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapError",
    ),
    "FlextTargetLdapModels": ("flext_target_ldap.models", "FlextTargetLdapModels"),
    "FlextTargetLdapProtocols": (
        "flext_target_ldap.protocols",
        "FlextTargetLdapProtocols",
    ),
    "FlextTargetLdapTypes": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
    "FlextTargetLdapUtilities": (
        "flext_target_ldap.utilities",
        "FlextTargetLdapUtilities",
    ),
    "FlextTargetLdapValidationError": (
        "flext_target_ldap.target_exceptions",
        "FlextTargetLdapValidationError",
    ),
    "GroupsSink": ("flext_target_ldap.sinks", "GroupsSink"),
    "LDAPBaseSink": ("flext_target_ldap.sinks", "LDAPBaseSink"),
    "LDAPProcessingResult": ("flext_target_ldap.sinks", "LDAPProcessingResult"),
    "LdapBaseSink": ("flext_target_ldap.sinks", "LDAPBaseSink"),
    "LdapBatchProcessingModel": (
        "flext_target_ldap.target_models",
        "LdapBatchProcessingModel",
    ),
    "LdapEntryModel": ("flext_target_ldap.target_models", "LdapEntryModel"),
    "LdapGroupsSink": ("flext_target_ldap.sinks", "GroupsSink"),
    "LdapTargetApiService": (
        "flext_target_ldap.target_services",
        "LdapTargetApiService",
    ),
    "LdapTargetClient": ("flext_target_ldap.target_client", "LdapTargetClient"),
    "LdapTransformationService": (
        "flext_target_ldap.target_services",
        "LdapTransformationService",
    ),
    "LdapTransformationServiceProtocol": (
        "flext_target_ldap.target_services",
        "LdapTransformationServiceProtocol",
    ),
    "LdapUsersSink": ("flext_target_ldap.sinks", "UsersSink"),
    "OrganizationalUnitsSink": ("flext_target_ldap.sinks", "OrganizationalUnitsSink"),
    "Sink": ("flext_target_ldap.sinks", "Sink"),
    "Target": ("flext_target_ldap.sinks", "Target"),
    "TargetLdap": ("flext_target_ldap.target_client", "TargetLdap"),
    "UsersSink": ("flext_target_ldap.sinks", "UsersSink"),
    "__version__": ("flext_target_ldap.__version__", "__version__"),
    "__version_info__": ("flext_target_ldap.__version__", "__version_info__"),
    "c": ("flext_target_ldap.constants", "FlextTargetLdapConstants"),
    "m": ("flext_target_ldap.models", "FlextTargetLdapModels"),
    "t": ("flext_target_ldap.typings", "FlextTargetLdapTypes"),
    "u": ("flext_target_ldap.utilities", "FlextTargetLdapUtilities"),
}

__all__ = [
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapConstants",
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
    "u",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
