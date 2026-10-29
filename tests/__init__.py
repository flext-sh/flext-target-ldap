# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, install_local_packages, td, tf, tk, tm

    from flext_target_ldap import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        config,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        ldap,
        ldif,
        main,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
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
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapServiceBase",
    "TestsFlextTargetLdapSettings",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
    "api",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "install_local_packages",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "ldap",
    "ldif",
    "m",
    "main",
    "meltano",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
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
    MappingProxyType({
        "TestsFlextTargetLdapConstants": ".constants",
        "TestsFlextTargetLdapModels": ".models",
        "TestsFlextTargetLdapProtocols": ".protocols",
        "TestsFlextTargetLdapServiceBase": ".base",
        "TestsFlextTargetLdapSettings": ".settings",
        "TestsFlextTargetLdapTypes": ".typings",
        "TestsFlextTargetLdapUtilities": ".utilities",
        "api": "flext_tests",
        "build_lazy_import_map": "flext_target_ldap",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_target_ldap",
        "cli": "flext_target_ldap",
        "config": "flext_target_ldap",
        "core": "flext_target_ldap",
        "d": "flext_target_ldap",
        "e": "flext_target_ldap",
        "h": "flext_target_ldap",
        "install_lazy_exports": "flext_target_ldap",
        "install_local_packages": "flext_tests",
        "lazy": "flext_target_ldap",
        "lazy_getattr": "flext_target_ldap",
        "lazy_member": "flext_target_ldap",
        "ldap": "flext_target_ldap",
        "ldif": "flext_target_ldap",
        "m": ".models",
        "main": "flext_target_ldap",
        "meltano": "flext_target_ldap",
        "merge_lazy_imports": "flext_target_ldap",
        "normalize_lazy_imports": "flext_target_ldap",
        "p": ".protocols",
        "r": "flext_target_ldap",
        "resolve_lazy_members": "flext_target_ldap",
        "s": ".base",
        "settings": "flext_target_ldap",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_target_ldap",
    }),
    public_exports=__all__,
)
