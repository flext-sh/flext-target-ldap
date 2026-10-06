# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Models package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._models._target_ldap_namespace import (
        FlextTargetLdapModelsTargetLdapNamespace,
    )
    from flext_target_ldap._models.config import FlextTargetLdapConfigModels
    from flext_target_ldap._models.processing_result import (
        FlextTargetLdapProcessingCounters,
    )
    from flext_target_ldap._models.sinks import FlextTargetLdapModelsSinks


__all__: tuple[str, ...] = (
    "FlextTargetLdapConfigModels",
    "FlextTargetLdapModelsSinks",
    "FlextTargetLdapModelsTargetLdapNamespace",
    "FlextTargetLdapProcessingCounters",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetLdapConfigModels": ".config",
        "FlextTargetLdapModelsSinks": ".sinks",
        "FlextTargetLdapModelsTargetLdapNamespace": "._target_ldap_namespace",
        "FlextTargetLdapProcessingCounters": ".processing_result",
    }),
    public_exports=__all__,
)
