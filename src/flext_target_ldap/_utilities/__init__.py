# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-ldap."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_target_ldap._utilities.client import *
    from flext_target_ldap._utilities.config import *
    from flext_target_ldap._utilities.services import *
    from flext_target_ldap._utilities.transformation import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTargetLdapApiService": "flext_target_ldap._utilities.services",
    "FlextTargetLdapClient": "flext_target_ldap._utilities.client",
    "FlextTargetLdapConnectionService": "flext_target_ldap._utilities.services",
    "FlextTargetLdapMigrationValidator": "flext_target_ldap._utilities.transformation",
    "FlextTargetLdapOrchestrator": "flext_target_ldap._utilities.services",
    "FlextTargetLdapSearchEntry": "flext_target_ldap._utilities.client",
    "FlextTargetLdapTransformationEngine": "flext_target_ldap._utilities.transformation",
    "FlextTargetLdapTransformationService": "flext_target_ldap._utilities.services",
    "client": "flext_target_ldap._utilities.client",
    "config": "flext_target_ldap._utilities.config",
    "create_default_ldap_target_config": "flext_target_ldap._utilities.config",
    "logger": "flext_target_ldap._utilities.transformation",
    "services": "flext_target_ldap._utilities.services",
    "transformation": "flext_target_ldap._utilities.transformation",
    "validate_ldap_target_config": "flext_target_ldap._utilities.config",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
