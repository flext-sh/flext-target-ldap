# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import (
        TestsFlextTargetLdapConstants,
        TestsFlextTargetLdapConstants as c,
    )

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import TestsFlextTargetLdapModels, TestsFlextTargetLdapModels as m

    protocols = _tests_protocols
    import tests.test_client as _tests_test_client
    from tests.protocols import (
        TestsFlextTargetLdapProtocols,
        TestsFlextTargetLdapProtocols as p,
    )

    test_client = _tests_test_client
    import tests.test_integration as _tests_test_integration

    test_integration = _tests_test_integration
    import tests.test_sinks as _tests_test_sinks

    test_sinks = _tests_test_sinks
    import tests.test_target as _tests_test_target

    test_target = _tests_test_target
    import tests.test_transformation as _tests_test_transformation

    test_transformation = _tests_test_transformation
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.utilities as _tests_utilities
    from tests.typings import TestsFlextTargetLdapTypes, TestsFlextTargetLdapTypes as t

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
