# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_ldap import ldap
    from flext_ldif import ldif
    from flext_meltano import main, meltano
    from flext_tests import (
        active_rules,
        api,
        discover_repository_root,
        install_local_packages,
        load_infra_report,
        split_csv,
        td,
        tf,
        tk,
        tm,
        tv,
    )

    from flext_core import core, d, e, h, lazy_attribute, r, x
    from flext_target_ldap import config, settings, target_ldap

    from . import unit
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
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapServiceBase",
    "TestsFlextTargetLdapSettings",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
    "active_rules",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "discover_repository_root",
    "e",
    "h",
    "install_local_packages",
    "lazy_attribute",
    "ldap",
    "ldif",
    "load_infra_report",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "settings",
    "split_csv",
    "t",
    "target_ldap",
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
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "e", "h", "lazy_attribute", "r", "x"),
            "flext_ldap": ("ldap",),
            "flext_ldif": ("ldif",),
            "flext_meltano": ("main", "meltano"),
            "flext_target_ldap": ("config", "settings", "target_ldap"),
            "flext_tests": (
                "active_rules",
                "api",
                "discover_repository_root",
                "install_local_packages",
                "load_infra_report",
                "split_csv",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
