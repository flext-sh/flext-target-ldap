# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
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
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_client": ("TestsFlextTargetLdapClient",),
        ".test_integration": ("TestsFlextTargetLdapIntegration",),
        ".test_sinks": ("TestsFlextTargetLdapSinks",),
        ".test_target": ("TestsFlextTargetLdapTarget",),
        ".test_transformation": ("TestsFlextTargetLdapTransformation",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
