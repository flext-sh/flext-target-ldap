# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import unit as unit
    from flext_target_ldap import FlextTargetLdapConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from .base import (
        TestsFlextTargetLdapServiceBase,
        TestsFlextTargetLdapServiceBase as s,
    )
    from .constants import (
        TestsFlextTargetLdapConstants,
        TestsFlextTargetLdapConstants as c,
    )
    from .models import TestsFlextTargetLdapModels, TestsFlextTargetLdapModels as m
    from .protocols import (
        TestsFlextTargetLdapProtocols,
        TestsFlextTargetLdapProtocols as p,
    )
    from .settings import TestsFlextTargetLdapSettings
    from .typings import TestsFlextTargetLdapTypes, TestsFlextTargetLdapTypes as t
    from .utilities import (
        TestsFlextTargetLdapUtilities,
        TestsFlextTargetLdapUtilities as u,
    )
__all__: tuple[str, ...] = (
    "FlextTargetLdapConstants",
    "FlextTestsConstants",
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapServiceBase",
    "TestsFlextTargetLdapSettings",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
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
    "tv",
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
            "flext_target_ldap": ("FlextTargetLdapConstants",),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
