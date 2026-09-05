# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_client import TestsFlextTargetLdapClient, client, people_ou, real_client
    from .test_integration import (
        TestsFlextTargetLdapIntegration,
        config_file,
        real_config,
    )
    from .test_sinks import (
        TestsFlextTargetLdapSinks,
        generic_sink,
        groups_sink,
        ldap_base_sink,
        ou_sink,
        users_sink,
    )
    from .test_target import TestsFlextTargetLdapTarget
    from .test_transformation import TestsFlextTargetLdapTransformation
__all__: tuple[str, ...] = (
    "TestsFlextTargetLdapClient",
    "TestsFlextTargetLdapIntegration",
    "TestsFlextTargetLdapSinks",
    "TestsFlextTargetLdapTarget",
    "TestsFlextTargetLdapTransformation",
    "c",
    "client",
    "config_file",
    "d",
    "e",
    "generic_sink",
    "groups_sink",
    "h",
    "ldap_base_sink",
    "m",
    "ou_sink",
    "p",
    "people_ou",
    "r",
    "real_client",
    "real_config",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "users_sink",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_client": (
                "TestsFlextTargetLdapClient",
                "client",
                "people_ou",
                "real_client",
            ),
            ".test_integration": (
                "TestsFlextTargetLdapIntegration",
                "config_file",
                "real_config",
            ),
            ".test_sinks": (
                "TestsFlextTargetLdapSinks",
                "generic_sink",
                "groups_sink",
                "ldap_base_sink",
                "ou_sink",
                "users_sink",
            ),
            ".test_target": ("TestsFlextTargetLdapTarget",),
            ".test_transformation": ("TestsFlextTargetLdapTransformation",),
            "flext_tests": (
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
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
