# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_client import TestsFlextTargetLdapClient
    from .test_integration import TestsFlextTargetLdapIntegration
    from .test_sinks import TestsFlextTargetLdapSinks
    from .test_target import TestsFlextTargetLdapTarget
    from .test_transformation import TestsFlextTargetLdapTransformation
__all__: tuple[str, ...] = (
    "TestsFlextTargetLdapClient",
    "TestsFlextTargetLdapIntegration",
    "TestsFlextTargetLdapSinks",
    "TestsFlextTargetLdapTarget",
    "TestsFlextTargetLdapTransformation",
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
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_client": ("TestsFlextTargetLdapClient",),
            ".test_integration": ("TestsFlextTargetLdapIntegration",),
            ".test_sinks": ("TestsFlextTargetLdapSinks",),
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
