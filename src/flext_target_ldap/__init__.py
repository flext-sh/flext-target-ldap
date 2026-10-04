# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
from flext_target_ldap.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_meltano import d, e, h, r, s, x

    from flext_target_ldap import application
    from flext_target_ldap._config import FlextTargetLdapConfig, config
    from flext_target_ldap._settings import FlextTargetLdapSettings, settings
    from flext_target_ldap.api import FlextTargetLdap, target_ldap
    from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator
    from flext_target_ldap.constants import FlextTargetLdapConstants, c
    from flext_target_ldap.models import FlextTargetLdapModels, m
    from flext_target_ldap.protocols import FlextTargetLdapProtocols, p
    from flext_target_ldap.typings import FlextTargetLdapTypes, t
    from flext_target_ldap.utilities import FlextTargetLdapUtilities, u


__all__: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapConfig",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
    "FlextTargetLdapOrchestrator",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSettings",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "application",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "target_ldap",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextTargetLdapConfig", "config"),
            "._settings": ("FlextTargetLdapSettings", "settings"),
            ".api": ("FlextTargetLdap", "target_ldap"),
            ".application": ("application",),
            ".application.orchestrator": ("FlextTargetLdapOrchestrator",),
            ".constants": ("FlextTargetLdapConstants", "c"),
            ".models": ("FlextTargetLdapModels", "m"),
            ".protocols": ("FlextTargetLdapProtocols", "p"),
            ".typings": ("FlextTargetLdapTypes", "t"),
            ".utilities": ("FlextTargetLdapUtilities", "u"),
            "flext_meltano": ("d", "e", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
