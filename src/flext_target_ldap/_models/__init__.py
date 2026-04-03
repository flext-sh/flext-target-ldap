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
    from flext_target_ldap import processing_result, sinks
    from flext_target_ldap.processing_result import FlextTargetLdapProcessingCounters
    from flext_target_ldap.sinks import (
        FlextTargetLdapProcessingResult,
        FlextTargetLdapSink,
        logger,
        msg,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTargetLdapProcessingCounters": "flext_target_ldap.processing_result",
    "FlextTargetLdapProcessingResult": "flext_target_ldap.sinks",
    "FlextTargetLdapSink": "flext_target_ldap.sinks",
    "logger": "flext_target_ldap.sinks",
    "msg": "flext_target_ldap.sinks",
    "processing_result": "flext_target_ldap.processing_result",
    "sinks": "flext_target_ldap.sinks",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
