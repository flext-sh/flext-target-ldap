"""Service base for flext-target-ldap tests."""

from __future__ import annotations

from typing import override

from flext_tests import s

from flext_target_ldap import m, p
from tests.settings import TestsFlextTargetLdapSettings


class TestsFlextTargetLdapServiceBase(s):
    """Target LDAP test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> p.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTargetLdapSettings)


s = TestsFlextTargetLdapServiceBase

__all__: list[str] = ["TestsFlextTargetLdapServiceBase", "s"]
