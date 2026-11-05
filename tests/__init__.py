# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, td, tf, tk, tm

    from flext_target_ldap import (
        FlextTargetLdap,
        FlextTargetLdapConfig,
        FlextTargetLdapConstants,
        FlextTargetLdapModels,
        FlextTargetLdapProtocols,
        FlextTargetLdapSettings,
        FlextTargetLdapTypes,
        FlextTargetLdapUtilities,
        FlextTargetLdapVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        d,
        e,
        h,
        main,
        r,
        settings,
        x,
    )
    from tests.base import TestsFlextTargetLdapServiceBase, s
    from tests.constants import TestsFlextTargetLdapConstants, c
    from tests.models import TestsFlextTargetLdapModels, m
    from tests.protocols import TestsFlextTargetLdapProtocols, p
    from tests.settings import TestsFlextTargetLdapSettings
    from tests.typings import TestsFlextTargetLdapTypes, t
    from tests.utilities import TestsFlextTargetLdapUtilities, u


__all__: tuple[str, ...] = (
    "FlextTargetLdap",
    "FlextTargetLdapConfig",
    "FlextTargetLdapConstants",
    "FlextTargetLdapModels",
    "FlextTargetLdapProtocols",
    "FlextTargetLdapSettings",
    "FlextTargetLdapTypes",
    "FlextTargetLdapUtilities",
    "FlextTargetLdapVersion",
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapServiceBase",
    "TestsFlextTargetLdapSettings",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
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
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextTargetLdap": "flext_target_ldap",
        "FlextTargetLdapConfig": "flext_target_ldap",
        "FlextTargetLdapConstants": "flext_target_ldap",
        "FlextTargetLdapModels": "flext_target_ldap",
        "FlextTargetLdapProtocols": "flext_target_ldap",
        "FlextTargetLdapSettings": "flext_target_ldap",
        "FlextTargetLdapTypes": "flext_target_ldap",
        "FlextTargetLdapUtilities": "flext_target_ldap",
        "FlextTargetLdapVersion": "flext_target_ldap",
        "TestsFlextTargetLdapConstants": ".constants",
        "TestsFlextTargetLdapModels": ".models",
        "TestsFlextTargetLdapProtocols": ".protocols",
        "TestsFlextTargetLdapServiceBase": ".base",
        "TestsFlextTargetLdapSettings": ".settings",
        "TestsFlextTargetLdapTypes": ".typings",
        "TestsFlextTargetLdapUtilities": ".utilities",
        "__author__": "flext_target_ldap",
        "__author_email__": "flext_target_ldap",
        "__description__": "flext_target_ldap",
        "__license__": "flext_target_ldap",
        "__title__": "flext_target_ldap",
        "__url__": "flext_target_ldap",
        "__version__": "flext_target_ldap",
        "__version_info__": "flext_target_ldap",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_target_ldap",
        "d": "flext_target_ldap",
        "e": "flext_target_ldap",
        "h": "flext_target_ldap",
        "m": ".models",
        "main": "flext_target_ldap",
        "p": ".protocols",
        "r": "flext_target_ldap",
        "s": ".base",
        "settings": "flext_target_ldap",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_target_ldap",
    },
    public_exports=__all__,
)
