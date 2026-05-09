# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import d, e, h, r, td, tf, tk, tm, tv, x

    from tests.base import TestsFlextTargetLdapServiceBase, s
    from tests.constants import TestsFlextTargetLdapConstants, c
    from tests.models import TestsFlextTargetLdapModels, m
    from tests.protocols import TestsFlextTargetLdapProtocols, p
    from tests.settings import TestsFlextTargetLdapSettings
    from tests.typings import TestsFlextTargetLdapTypes, t
    from tests.unit.test_client import TestsFlextTargetLdapClient
    from tests.unit.test_integration import TestsFlextTargetLdapIntegration
    from tests.unit.test_sinks import TestsFlextTargetLdapSinks
    from tests.unit.test_target import TestsFlextTargetLdapTarget
    from tests.unit.test_transformation import TestsFlextTargetLdapTransformation
    from tests.utilities import TestsFlextTargetLdapUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextTargetLdapServiceBase",
                "s",
            ),
            ".constants": (
                "TestsFlextTargetLdapConstants",
                "c",
            ),
            ".models": (
                "TestsFlextTargetLdapModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextTargetLdapProtocols",
                "p",
            ),
            ".settings": ("TestsFlextTargetLdapSettings",),
            ".typings": (
                "TestsFlextTargetLdapTypes",
                "t",
            ),
            ".unit.test_client": ("TestsFlextTargetLdapClient",),
            ".unit.test_integration": ("TestsFlextTargetLdapIntegration",),
            ".unit.test_sinks": ("TestsFlextTargetLdapSinks",),
            ".unit.test_target": ("TestsFlextTargetLdapTarget",),
            ".unit.test_transformation": ("TestsFlextTargetLdapTransformation",),
            ".utilities": (
                "TestsFlextTargetLdapUtilities",
                "u",
            ),
            "flext_tests": (
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
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextTargetLdapClient",
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapIntegration",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapServiceBase",
    "TestsFlextTargetLdapSettings",
    "TestsFlextTargetLdapSinks",
    "TestsFlextTargetLdapTarget",
    "TestsFlextTargetLdapTransformation",
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
    "x",
]
