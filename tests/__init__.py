# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import (
        d as d,
        e as e,
        h as h,
        r as r,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        x as x,
    )

    from flext_target_ldap.tests.base import (
        TestsFlextTargetLdapServiceBase as TestsFlextTargetLdapServiceBase,
        s as s,
    )
    from flext_target_ldap.tests.constants import (
        TestsFlextTargetLdapConstants as TestsFlextTargetLdapConstants,
        c as c,
    )
    from flext_target_ldap.tests.models import (
        TestsFlextTargetLdapModels as TestsFlextTargetLdapModels,
        m as m,
    )
    from flext_target_ldap.tests.protocols import (
        TestsFlextTargetLdapProtocols as TestsFlextTargetLdapProtocols,
        p as p,
    )
    from flext_target_ldap.tests.settings import (
        TestsFlextTargetLdapSettings as TestsFlextTargetLdapSettings,
    )
    from flext_target_ldap.tests.typings import (
        TestsFlextTargetLdapTypes as TestsFlextTargetLdapTypes,
        t as t,
    )
    from flext_target_ldap.tests.unit.test_client import (
        TestsFlextTargetLdapClient as TestsFlextTargetLdapClient,
    )
    from flext_target_ldap.tests.unit.test_integration import (
        TestsFlextTargetLdapIntegration as TestsFlextTargetLdapIntegration,
    )
    from flext_target_ldap.tests.unit.test_sinks import (
        TestsFlextTargetLdapSinks as TestsFlextTargetLdapSinks,
    )
    from flext_target_ldap.tests.unit.test_target import (
        TestsFlextTargetLdapTarget as TestsFlextTargetLdapTarget,
    )
    from flext_target_ldap.tests.unit.test_transformation import (
        TestsFlextTargetLdapTransformation as TestsFlextTargetLdapTransformation,
    )
    from flext_target_ldap.tests.utilities import (
        TestsFlextTargetLdapUtilities as TestsFlextTargetLdapUtilities,
        u as u,
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
