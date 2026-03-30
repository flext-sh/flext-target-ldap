# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target ldap package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_target_ldap._models import _LAZY_IMPORTS as _CHILD_LAZY_0
from flext_target_ldap._utilities import _LAZY_IMPORTS as _CHILD_LAZY_1
from flext_target_ldap.application import _LAZY_IMPORTS as _CHILD_LAZY_2
from flext_target_ldap.patterns import _LAZY_IMPORTS as _CHILD_LAZY_3
from flext_target_ldap.singer import _LAZY_IMPORTS as _CHILD_LAZY_4

if TYPE_CHECKING:
    from flext_target_ldap.__version__ import *
    from flext_target_ldap._models import *
    from flext_target_ldap._utilities import *
    from flext_target_ldap.application import *
    from flext_target_ldap.catalog import *
    from flext_target_ldap.constants import *
    from flext_target_ldap.errors import *
    from flext_target_ldap.models import *
    from flext_target_ldap.patterns import *
    from flext_target_ldap.protocols import *
    from flext_target_ldap.settings import *
    from flext_target_ldap.singer import *
    from flext_target_ldap.target import *
    from flext_target_ldap.transformation import *
    from flext_target_ldap.typings import *
    from flext_target_ldap.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_CHILD_LAZY_0,
    **_CHILD_LAZY_1,
    **_CHILD_LAZY_2,
    **_CHILD_LAZY_3,
    **_CHILD_LAZY_4,
    "DataTransformationEngine": "flext_target_ldap.transformation",
    "FlextTargetLdap": "flext_target_ldap.target",
    "FlextTargetLdapAuthenticationError": "flext_target_ldap.errors",
    "FlextTargetLdapConfigurationError": "flext_target_ldap.errors",
    "FlextTargetLdapConnectionError": "flext_target_ldap.errors",
    "FlextTargetLdapConstants": "flext_target_ldap.constants",
    "FlextTargetLdapError": "flext_target_ldap.errors",
    "FlextTargetLdapModels": "flext_target_ldap.models",
    "FlextTargetLdapProcessingError": "flext_target_ldap.errors",
    "FlextTargetLdapProtocols": "flext_target_ldap.protocols",
    "FlextTargetLdapSettings": "flext_target_ldap.settings",
    "FlextTargetLdapTimeoutError": "flext_target_ldap.errors",
    "FlextTargetLdapTypes": "flext_target_ldap.typings",
    "FlextTargetLdapUtilities": "flext_target_ldap.utilities",
    "FlextTargetLdapValidationError": "flext_target_ldap.errors",
    "MigrationValidator": "flext_target_ldap.transformation",
    "__author__": "flext_target_ldap.__version__",
    "__author_email__": "flext_target_ldap.__version__",
    "__description__": "flext_target_ldap.__version__",
    "__license__": "flext_target_ldap.__version__",
    "__title__": "flext_target_ldap.__version__",
    "__url__": "flext_target_ldap.__version__",
    "__version__": "flext_target_ldap.__version__",
    "__version_info__": "flext_target_ldap.__version__",
    "_models": "flext_target_ldap._models",
    "_utilities": "flext_target_ldap._utilities",
    "application": "flext_target_ldap.application",
    "build_singer_catalog": "flext_target_ldap.catalog",
    "c": ["flext_target_ldap.constants", "FlextTargetLdapConstants"],
    "catalog": "flext_target_ldap.catalog",
    "constants": "flext_target_ldap.constants",
    "d": "flext_ldap",
    "e": "flext_ldap",
    "errors": "flext_target_ldap.errors",
    "h": "flext_ldap",
    "logger": "flext_target_ldap.target",
    "m": ["flext_target_ldap.models", "FlextTargetLdapModels"],
    "main": "flext_target_ldap.target",
    "models": "flext_target_ldap.models",
    "p": ["flext_target_ldap.protocols", "FlextTargetLdapProtocols"],
    "patterns": "flext_target_ldap.patterns",
    "processing_result": "flext_target_ldap.processing_result",
    "protocols": "flext_target_ldap.protocols",
    "r": "flext_ldap",
    "s": "flext_ldap",
    "settings": "flext_target_ldap.settings",
    "singer": "flext_target_ldap.singer",
    "sinks": "flext_target_ldap.sinks",
    "t": ["flext_target_ldap.typings", "FlextTargetLdapTypes"],
    "target": "flext_target_ldap.target",
    "target_client": "flext_target_ldap.target_client",
    "target_config": "flext_target_ldap.target_config",
    "target_services": "flext_target_ldap.target_services",
    "transformation": "flext_target_ldap.transformation",
    "typings": "flext_target_ldap.typings",
    "u": ["flext_target_ldap.utilities", "FlextTargetLdapUtilities"],
    "utilities": "flext_target_ldap.utilities",
    "validate_ldap_config": "flext_target_ldap.settings",
    "x": "flext_ldap",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
