"""Test types facade via MRO composition."""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_target_ldap import FlextTargetLdapTypes


class TestsFlextTargetLdapTypes(FlextTestsTypes, FlextTargetLdapTypes):
    """Test types facade for flext-target-ldap."""

    class TargetLdap(FlextTargetLdapTypes.TargetLdap):
        """TargetLdap test types namespace."""

        class Tests(FlextTestsTypes.Tests):
            """TargetLdap-specific test type aliases."""


t = TestsFlextTargetLdapTypes
__all__: list[str] = ["TestsFlextTargetLdapTypes", "t"]
