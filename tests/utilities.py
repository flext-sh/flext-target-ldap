"""Utilities for flext-target-ldap tests - uses u.TargetLdap.Tests.* namespace pattern.

This module provides test-specific utilities that extend the main flext-target-ldap utilities.
Uses the unified namespace pattern u.TargetLdap.Tests.* for test-only objects.
Combines TestsFlextUtilities functionality with project-specific test utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
)
from typing import override

from flext_tests import FlextTestsUtilities

from flext_target_ldap import FlextTargetLdapTarget, FlextTargetLdapUtilities, p, r
from tests import TestsFlextTargetLdapTypes


class TestsFlextTargetLdapUtilities(FlextTestsUtilities, FlextTargetLdapUtilities):
    """Test utilities for flext-target-ldap extending both test and project utilities."""

    class TargetLdap(FlextTargetLdapUtilities.TargetLdap):
        """TargetLdap test namespace."""

        class Tests:
            """Target LDAP-specific test helpers."""

            @staticmethod
            def build_mock_ldap_config(
                *,
                bind_dn: str,
            ) -> TestsFlextTargetLdapTypes.TargetLdap.MutableSettingsPayload:
                """Build a standard mock LDAP configuration for testing."""
                return {
                    "host": "test.ldap.com",
                    "port": 389,
                    "bind_dn": bind_dn,
                    "password": "test_password",
                    "base_dn": "dc=test,dc=com",
                    "use_ssl": False,
                    "timeout": 30,
                    "validate_records": True,
                    "user_rdn_attribute": "uid",
                    "group_rdn_attribute": "cn",
                    "dn_templates": {
                        "users": "uid={uid},ou=users,dc=test,dc=com",
                        "groups": "cn={cn},ou=groups,dc=test,dc=com",
                    },
                    "default_object_classes": {
                        "users": ["inetOrgPerson", "person", "top"],
                        "groups": ["groupOfNames", "top"],
                    },
                }

            class ProcessTarget(FlextTargetLdapTarget):
                """Target stub that records delegated sink calls."""

                def __init__(self) -> None:
                    """Initialize the recording target with minimal settings."""
                    super().__init__({"base_dn": "dc=test,dc=com"})
                    self.calls: MutableSequence[
                        TestsFlextTargetLdapTypes.TargetLdap.Tests.ProcessCall
                    ] = []

                @override
                def process_record(
                    self,
                    _record: TestsFlextTargetLdapTypes.TargetLdap.RecordPayload,
                    _context: TestsFlextTargetLdapTypes.TargetLdap.RecordPayload,
                ) -> p.Result[bool]:
                    """Record the delegated call and report success."""
                    self.calls.append((_record, _context))
                    return r[bool].ok(value=True)


u = TestsFlextTargetLdapUtilities
__all__: list[str] = ["TestsFlextTargetLdapUtilities", "u"]
