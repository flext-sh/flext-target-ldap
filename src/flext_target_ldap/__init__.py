# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports
from flext_target_ldap.__version__ import __version__

if TYPE_CHECKING:
    from flext_meltano import d, e, h, r, s, x

    from flext_target_ldap import _constants, _models, _utilities, application
    from flext_target_ldap.__version__ import (
        FlextTargetLdapVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version_info__,
    )
    from flext_target_ldap._config import FlextTargetLdapConfig, config
    from flext_target_ldap._settings import FlextTargetLdapSettings, settings
    from flext_target_ldap.api import FlextTargetLdap
    from flext_target_ldap.cli import FlextTargetLdapCli, main
    from flext_target_ldap.constants import FlextTargetLdapConstants, c
    from flext_target_ldap.models import FlextTargetLdapModels, m
    from flext_target_ldap.protocols import FlextTargetLdapProtocols, p
    from flext_target_ldap.typings import FlextTargetLdapTypes, t
    from flext_target_ldap.utilities import FlextTargetLdapUtilities, u


__all__: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapCli",
    "FlextTargetLdapConfig",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSettings",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_constants",
    "_models",
    "_utilities",
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
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetLdap": ".api",
        "FlextTargetLdapCli": ".cli",
        "FlextTargetLdapConfig": "._config",
        "FlextTargetLdapConstants": ".constants",
        "FlextTargetLdapModels": ".models",
        "FlextTargetLdapProtocols": ".protocols",
        "FlextTargetLdapSettings": "._settings",
        "FlextTargetLdapTypes": ".typings",
        "FlextTargetLdapUtilities": ".utilities",
        "FlextTargetLdapVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "_constants": "._constants",
        "_models": "._models",
        "_utilities": "._utilities",
        "application": ".application",
        "c": ".constants",
        "config": "._config",
        "d": "flext_meltano",
        "e": "flext_meltano",
        "h": "flext_meltano",
        "m": ".models",
        "main": ".cli",
        "p": ".protocols",
        "r": "flext_meltano",
        "s": "flext_meltano",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)
