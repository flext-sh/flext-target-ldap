# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_ldap import ldap
    from flext_ldif import ldif
    from flext_meltano import main, meltano, s

    from flext_core import core, d, e, h, lazy_attribute, r, x

    from . import application
    from ._config import FlextTargetLdapConfig, config
    from ._settings import FlextTargetLdapSettings, settings
    from .api import FlextTargetLdap, target_ldap
    from .application.orchestrator import FlextTargetLdapOrchestrator
    from .constants import FlextTargetLdapConstants, c
    from .models import FlextTargetLdapModels, m
    from .protocols import FlextTargetLdapProtocols, p
    from .typings import FlextTargetLdapTypes, t
    from .utilities import FlextTargetLdapUtilities, u
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
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "lazy_attribute",
    "ldap",
    "ldif",
    "m",
    "main",
    "meltano",
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
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "e", "h", "lazy_attribute", "r", "x"),
            "flext_ldap": ("ldap",),
            "flext_ldif": ("ldif",),
            "flext_meltano": ("main", "meltano", "s"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
