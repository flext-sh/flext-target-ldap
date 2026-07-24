# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
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
    from flext_ldap import d, e, h, r, s, x

    from ._config import FlextTargetLdapConfig, config
    from ._settings import FlextTargetLdapSettings, settings
    from .api import FlextTargetLdap, target_ldap
    from .constants import FlextTargetLdapConstants, FlextTargetLdapConstants as c
    from .models import FlextTargetLdapModels, FlextTargetLdapModels as m
    from .protocols import FlextTargetLdapProtocols, FlextTargetLdapProtocols as p
    from .typings import FlextTargetLdapTypes, FlextTargetLdapTypes as t
    from .utilities import FlextTargetLdapUtilities, FlextTargetLdapUtilities as u

    _ = (
        c,
        FlextTargetLdapConstants,
        t,
        FlextTargetLdapTypes,
        p,
        FlextTargetLdapProtocols,
        m,
        FlextTargetLdapModels,
        u,
        FlextTargetLdapUtilities,
        d,
        e,
        h,
        r,
        s,
        x,
        FlextTargetLdapConfig,
        config,
        FlextTargetLdapSettings,
        settings,
        FlextTargetLdap,
        target_ldap,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextTargetLdapConfig", "config"),
    "._settings": ("FlextTargetLdapSettings", "settings"),
    ".api": ("FlextTargetLdap", "target_ldap"),
    ".constants": ("FlextTargetLdapConstants", "c"),
    ".models": ("FlextTargetLdapModels", "m"),
    ".protocols": ("FlextTargetLdapProtocols", "p"),
    ".typings": ("FlextTargetLdapTypes", "t"),
    ".utilities": ("FlextTargetLdapUtilities", "u"),
    "flext_ldap": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapConfig",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
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
    "build_lazy_import_map",
    "c",
    "config",
    "d",
    "e",
    "h",
    "install_lazy_exports",
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

__all__: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapConfig",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
