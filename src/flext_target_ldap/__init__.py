# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_ldap import d as d
    from flext_ldap import e as e
    from flext_ldap import h as h
    from flext_ldap import r as r
    from flext_ldap import s as s
    from flext_ldap import x as x

    from ._config import FlextTargetLdapConfig as FlextTargetLdapConfig
    from ._config import config as config
    from ._settings import FlextTargetLdapSettings as FlextTargetLdapSettings
    from ._settings import settings as settings
    from .api import FlextTargetLdap as FlextTargetLdap
    from .api import target_ldap as target_ldap
    from .constants import FlextTargetLdapConstants as FlextTargetLdapConstants

    c: type[FlextTargetLdapConstants]
    from .models import FlextTargetLdapModels as FlextTargetLdapModels

    m: type[FlextTargetLdapModels]
    from .protocols import FlextTargetLdapProtocols as FlextTargetLdapProtocols

    p: type[FlextTargetLdapProtocols]
    from .typings import FlextTargetLdapTypes as FlextTargetLdapTypes

    t: type[FlextTargetLdapTypes]
    from .utilities import FlextTargetLdapUtilities as FlextTargetLdapUtilities

    u: type[FlextTargetLdapUtilities]

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

_PUBLIC_EXPORTS: tuple[str, ...] = (
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

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
