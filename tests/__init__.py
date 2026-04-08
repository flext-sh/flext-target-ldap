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
    "TestsFlextTargetLdapConstants": ".constants",
    "TestsFlextTargetLdapModels": ".models",
    "TestsFlextTargetLdapProtocols": ".protocols",
    "TestsFlextTargetLdapTypes": ".typings",
    "TestsFlextTargetLdapUtilities": ".utilities",
    "c": (".constants", "TestsFlextTargetLdapConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": (".models", "TestsFlextTargetLdapModels"),
    "p": (".protocols", "TestsFlextTargetLdapProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": (".typings", "TestsFlextTargetLdapTypes"),
    "u": (".utilities", "TestsFlextTargetLdapUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextTargetLdapConstants",
    "TestsFlextTargetLdapModels",
    "TestsFlextTargetLdapProtocols",
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
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
