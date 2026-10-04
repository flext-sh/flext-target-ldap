# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextTargetLdapServiceBase", "s"),
            ".constants": ("TestsFlextTargetLdapConstants", "c"),
            ".models": ("TestsFlextTargetLdapModels", "m"),
            ".protocols": ("TestsFlextTargetLdapProtocols", "p"),
            ".settings": ("TestsFlextTargetLdapSettings",),
            ".typings": ("TestsFlextTargetLdapTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextTargetLdapUtilities", "u"),
            "flext_target_ldap": ("d", "e", "h", "r", "x"),
            "flext_tests": ("api", "td", "tf", "tk", "tm"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
