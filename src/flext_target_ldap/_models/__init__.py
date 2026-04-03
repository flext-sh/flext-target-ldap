# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_target_ldap._models import processing_result, sinks
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import (
        FlextTargetLdapBaseSink,
        FlextTargetLdapGroupsSink,
        FlextTargetLdapOrganizationalUnitsSink,
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        FlextTargetLdapTarget,
        FlextTargetLdapUsersSink,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTargetLdapBaseSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapGroupsSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapOrganizationalUnitsSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapProcessingCounters": "flext_target_ldap._models.processing_result",
    "FlextTargetLdapProcessingResult": "flext_target_ldap._models.sinks",
    "FlextTargetLdapSink": "flext_target_ldap._models.sinks",
    "FlextTargetLdapTarget": "flext_target_ldap._models.sinks",
    "FlextTargetLdapUsersSink": "flext_target_ldap._models.sinks",
    "processing_result": "flext_target_ldap._models.processing_result",
    "sinks": "flext_target_ldap._models.sinks",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
