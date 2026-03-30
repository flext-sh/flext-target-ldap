# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal models subpackage for flext-target-ldap."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._models import (
        processing_result as processing_result,
        sinks as sinks,
    )
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters as FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink as FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink as FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink as FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult as FlextTargetLdapProcessingResult,
        FlextTargetLdapSink as FlextTargetLdapSink,
        FlextTargetLdapTarget as FlextTargetLdapTarget,
        FlextTargetLdapUsersSink as FlextTargetLdapUsersSink,
        logger as logger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTargetLdapBaseSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapBaseSink",
    ],
    "FlextTargetLdapGroupsSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapGroupsSink",
    ],
    "FlextTargetLdapOrganizationalUnitsSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapOrganizationalUnitsSink",
    ],
    "FlextTargetLdapProcessingCounters": [
        "flext_target_ldap._models.processing_result",
        "FlextTargetLdapProcessingCounters",
    ],
    "FlextTargetLdapProcessingResult": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapProcessingResult",
    ],
    "FlextTargetLdapSink": ["flext_target_ldap._models.sinks", "FlextTargetLdapSink"],
    "FlextTargetLdapTarget": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapTarget",
    ],
    "FlextTargetLdapUsersSink": [
        "flext_target_ldap._models.sinks",
        "FlextTargetLdapUsersSink",
    ],
    "logger": ["flext_target_ldap._models.sinks", "logger"],
    "processing_result": ["flext_target_ldap._models.processing_result", ""],
    "sinks": ["flext_target_ldap._models.sinks", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingCounters",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
    "logger",
    "processing_result",
    "sinks",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
