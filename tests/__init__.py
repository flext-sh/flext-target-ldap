# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_ldap import adapters, ldap, ldif
    from flext_meltano import main, meltano
    from flext_tests import (
        api,
        cli,
        core,
        d,
        e,
        h,
        install_local_packages,
        lazy_attribute,
        load_infra_report,
        r,
        services,
        td,
        tf,
        tk,
        tm,
        tv,
        x,
    )

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
    "adapters",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
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
    "services",
    "settings",
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
            "flext_ldap": ("adapters", "ldap", "ldif"),
            "flext_meltano": ("main", "meltano"),
            "flext_target_ldap": ("config", "settings", "target_ldap"),
            "flext_tests": (
                "api",
                "cli",
                "core",
                "d",
                "e",
                "h",
                "install_local_packages",
                "lazy_attribute",
                "load_infra_report",
                "r",
                "services",
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
