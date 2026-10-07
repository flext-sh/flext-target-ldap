# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, td, tf, tk, tm

    from flext_target_ldap import d, e, h, r, x
    from tests import unit
    from tests.base import TestsFlextTargetLdapServiceBase, s
    from tests.constants import TestsFlextTargetLdapConstants, c
    from tests.models import TestsFlextTargetLdapModels, m
    from tests.protocols import TestsFlextTargetLdapProtocols, p
    from tests.settings import TestsFlextTargetLdapSettings
    from tests.typings import TestsFlextTargetLdapTypes, t
    from tests.utilities import TestsFlextTargetLdapUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapServiceBase",
    "TestsFlextTargetLdapSettings",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
    "api",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "unit",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextTargetLdapConstants": ".constants",
        "TestsFlextTargetLdapModels": ".models",
        "TestsFlextTargetLdapProtocols": ".protocols",
        "TestsFlextTargetLdapServiceBase": ".base",
        "TestsFlextTargetLdapSettings": ".settings",
        "TestsFlextTargetLdapTypes": ".typings",
        "TestsFlextTargetLdapUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "d": "flext_target_ldap",
        "e": "flext_target_ldap",
        "h": "flext_target_ldap",
        "m": ".models",
        "p": ".protocols",
        "r": "flext_target_ldap",
        "s": ".base",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "unit": ".unit",
        "x": "flext_target_ldap",
    }),
    public_exports=__all__,
)
