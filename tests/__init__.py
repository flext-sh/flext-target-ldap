# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".base": (
                "TestsFlextTargetLdapServiceBase",
                "s",
            ),
            ".conftest": ("conftest",),
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
            ".unit": ("unit",),
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
