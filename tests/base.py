"""Service base for flext-target-ldap tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_target_ldap import m
from tests.settings import TestsFlextTargetLdapSettings


class TestsFlextTargetLdapServiceBase(tests_s):
    """Target LDAP test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextTargetLdapSettings:
        """Return the typed target LDAP+Tests settings singleton."""
        return TestsFlextTargetLdapSettings.fetch_global()

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTargetLdapSettings)


s = TestsFlextTargetLdapServiceBase

__all__: list[str] = ["TestsFlextTargetLdapServiceBase", "s"]
