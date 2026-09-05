# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

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
    from . import application as application
    from flext_ldap import FlextLdapConstants, d, e, h, r, s, x
    from typing import TYPE_CHECKING

    from ._config import FlextTargetLdapConfig, config
    from ._settings import FlextTargetLdapSettings, settings
    from .api import FlextTargetLdap, target_ldap
    from .application.orchestrator import FlextTargetLdapOrchestrator
    from .constants import FlextTargetLdapConstants, FlextTargetLdapConstants as c
    from .models import FlextTargetLdapModels, FlextTargetLdapModels as m
    from .protocols import FlextTargetLdapProtocols, FlextTargetLdapProtocols as p
    from .target import main
    from .typings import FlextTargetLdapTypes, FlextTargetLdapTypes as t
    from .utilities import FlextTargetLdapUtilities, FlextTargetLdapUtilities as u
__all__: tuple[str, ...] = (
    "TYPE_CHECKING",
    "FlextLdapConstants",
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
    "main",
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
            ".target": ("main",),
            ".typings": ("FlextTargetLdapTypes", "t"),
            ".utilities": ("FlextTargetLdapUtilities", "u"),
            "flext_ldap": ("FlextLdapConstants", "d", "e", "h", "r", "s", "x"),
            "typing": ("TYPE_CHECKING",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
