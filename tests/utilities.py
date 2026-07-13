"""Utilities for flext-target-ldap tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from flext_tests import FlextTestsUtilities

from flext_target_ldap import FlextTargetLdapUtilities, p, r
from flext_target_ldap._models.sinks import FlextTargetLdapTarget

if TYPE_CHECKING:
    from collections.abc import (
        MutableSequence,
    )

    from tests import t


class TestsFlextTargetLdapUtilities(FlextTestsUtilities, FlextTargetLdapUtilities):
    """Test utilities for flext-target-ldap extending both test and project utilities."""

    class TargetLdap(FlextTargetLdapUtilities.TargetLdap):
        """TargetLdap test namespace."""

        class Tests(FlextTestsUtilities.Tests):
            """TargetLdap-specific test utilities."""

            @staticmethod
            def build_mock_ldap_config(
                *,
                bind_dn: str,
            ) -> t.TargetLdap.SettingsPayload:
                """Build a standard mock LDAP configuration for testing."""
                return {
                    "connection": {
                        "host": "test.ldap.com",
                        "port": 389,
                        "bind_dn": bind_dn,
                        "bind_password": "test_password",
                        "use_ssl": False,
                        "timeout": 30,
                    },
                    "base_dn": "dc=test,dc=com",
                    "object_classes": ["inetOrgPerson", "person", "top"],
                }

            class ProcessTarget(FlextTargetLdapTarget):
                """Target stub that records delegated sink calls."""

                def __init__(self) -> None:
                    """Initialize the recording target with minimal settings."""
                    super().__init__({"base_dn": "dc=test,dc=com"})
                    self.calls: MutableSequence[
                        tuple[t.TargetLdap.RecordPayload, t.TargetLdap.RecordPayload]
                    ] = []

                @override
                def process_record(
                    self,
                    _record: t.TargetLdap.RecordPayload,
                    context: t.TargetLdap.RecordPayload,
                ) -> p.Result[bool]:
                    """Record the delegated call and report success."""
                    self.calls.append((_record, context))
                    return r[bool].ok(value=True)


u = TestsFlextTargetLdapUtilities
__all__: list[str] = ["TestsFlextTargetLdapUtilities", "u"]
