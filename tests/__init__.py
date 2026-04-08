# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests import (
        conftest,
        constants,
        models,
        protocols,
        test_client,
        test_integration,
        test_sinks,
        test_target,
        test_transformation,
        typings,
        utilities,
    )
    from tests.constants import (
        TestsFlextTargetLdapConstants,
        TestsFlextTargetLdapConstants as c,
    )
    from tests.models import TestsFlextTargetLdapModels, TestsFlextTargetLdapModels as m
    from tests.protocols import (
        TestsFlextTargetLdapProtocols,
        TestsFlextTargetLdapProtocols as p,
    )
    from tests.typings import TestsFlextTargetLdapTypes, TestsFlextTargetLdapTypes as t
    from tests.utilities import (
        TestsFlextTargetLdapUtilities,
        TestsFlextTargetLdapUtilities as u,
    )
_LAZY_IMPORTS = {
    "TestsFlextTargetLdapConstants": (
        "tests.constants",
        "TestsFlextTargetLdapConstants",
    ),
    "TestsFlextTargetLdapModels": ("tests.models", "TestsFlextTargetLdapModels"),
    "TestsFlextTargetLdapProtocols": (
        "tests.protocols",
        "TestsFlextTargetLdapProtocols",
    ),
    "TestsFlextTargetLdapTypes": ("tests.typings", "TestsFlextTargetLdapTypes"),
    "TestsFlextTargetLdapUtilities": (
        "tests.utilities",
        "TestsFlextTargetLdapUtilities",
    ),
    "c": ("tests.constants", "TestsFlextTargetLdapConstants"),
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "TestsFlextTargetLdapModels"),
    "models": "tests.models",
    "p": ("tests.protocols", "TestsFlextTargetLdapProtocols"),
    "protocols": "tests.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "TestsFlextTargetLdapTypes"),
    "test_client": "tests.test_client",
    "test_integration": "tests.test_integration",
    "test_sinks": "tests.test_sinks",
    "test_target": "tests.test_target",
    "test_transformation": "tests.test_transformation",
    "typings": "tests.typings",
    "u": ("tests.utilities", "TestsFlextTargetLdapUtilities"),
    "utilities": "tests.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
    "TestsFlextTargetLdapTypes",
    "TestsFlextTargetLdapUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "t",
    "test_client",
    "test_integration",
    "test_sinks",
    "test_target",
    "test_transformation",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
