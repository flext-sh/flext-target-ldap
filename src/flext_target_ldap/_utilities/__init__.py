# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-ldap."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._utilities import (
        client as client,
        config as config,
        services as services,
        transformation as transformation,
    )
    from flext_target_ldap._utilities.client import (
        FlextTargetLdapClient as FlextTargetLdapClient,
        FlextTargetLdapSearchEntry as FlextTargetLdapSearchEntry,
    )
    from flext_target_ldap._utilities.config import (
        create_default_ldap_target_config as create_default_ldap_target_config,
        validate_ldap_target_config as validate_ldap_target_config,
    )
    from flext_target_ldap._utilities.services import (
        FlextTargetLdapApiService as FlextTargetLdapApiService,
        FlextTargetLdapConnectionService as FlextTargetLdapConnectionService,
        FlextTargetLdapOrchestrator as FlextTargetLdapOrchestrator,
        FlextTargetLdapTransformationService as FlextTargetLdapTransformationService,
    )
    from flext_target_ldap._utilities.transformation import (
        FlextTargetLdapMigrationValidator as FlextTargetLdapMigrationValidator,
        FlextTargetLdapTransformationEngine as FlextTargetLdapTransformationEngine,
        logger as logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapApiService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapApiService",
    ],
    "FlextTargetLdapClient": [
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapClient",
    ],
    "FlextTargetLdapConnectionService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapConnectionService",
    ],
    "FlextTargetLdapMigrationValidator": [
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapMigrationValidator",
    ],
    "FlextTargetLdapOrchestrator": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapOrchestrator",
    ],
    "FlextTargetLdapSearchEntry": [
        "flext_target_ldap._utilities.client",
        "FlextTargetLdapSearchEntry",
    ],
    "FlextTargetLdapTransformationEngine": [
        "flext_target_ldap._utilities.transformation",
        "FlextTargetLdapTransformationEngine",
    ],
    "FlextTargetLdapTransformationService": [
        "flext_target_ldap._utilities.services",
        "FlextTargetLdapTransformationService",
    ],
    "client": ["flext_target_ldap._utilities.client", ""],
    "config": ["flext_target_ldap._utilities.config", ""],
    "create_default_ldap_target_config": [
        "flext_target_ldap._utilities.config",
        "create_default_ldap_target_config",
    ],
    "logger": ["flext_target_ldap._utilities.transformation", "logger"],
    "services": ["flext_target_ldap._utilities.services", ""],
    "transformation": ["flext_target_ldap._utilities.transformation", ""],
    "validate_ldap_target_config": [
        "flext_target_ldap._utilities.config",
        "validate_ldap_target_config",
    ],
}

_EXPORTS: Sequence[str] = [
    "FlextTargetLdapApiService",
    "FlextTargetLdapClient",
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapMigrationValidator",
    "FlextTargetLdapOrchestrator",
    "FlextTargetLdapSearchEntry",
    "FlextTargetLdapTransformationEngine",
    "FlextTargetLdapTransformationService",
    "client",
    "config",
    "create_default_ldap_target_config",
    "logger",
    "services",
    "transformation",
    "validate_ldap_target_config",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
