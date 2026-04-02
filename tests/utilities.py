"""Utilities for flext-target-ldap tests - uses u.TargetLdap.Tests.* namespace pattern.

This module provides test-specific utilities that extend the main flext-target-ldap utilities.
Uses the unified namespace pattern u.TargetLdap.Tests.* for test-only objects.
Combines FlextTestsUtilities functionality with project-specific test utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import MutableSequence

from flext_tests import FlextTestsUtilities

from flext_target_ldap import FlextTargetLdapTarget, FlextTargetLdapUtilities
from tests.typings import FlextTargetLdapTestTypes


class FlextTargetLdapTestUtilities(FlextTestsUtilities, FlextTargetLdapUtilities):
    """Test utilities for flext-target-ldap extending both test and project utilities."""

    class TargetLdap(FlextTargetLdapUtilities.TargetLdap):
        """TargetLdap test namespace."""

        class Tests:
            """Target LDAP-specific test helpers."""

            class ProcessTarget(FlextTargetLdapTarget):
                """Target stub that records delegated sink calls."""

                def __init__(self) -> None:
                    """Initialize the recording target with minimal config."""
                    super().__init__({"base_dn": "dc=test,dc=com"})
                    self.calls: MutableSequence[
                        FlextTargetLdapTestTypes.TargetLdap.Tests.ProcessCall
                    ] = []

                def process_record(
                    self,
                    record: FlextTargetLdapTestTypes.StrMapping,
                    context: FlextTargetLdapTestTypes.StrMapping,
                ) -> bool:
                    """Record the delegated call and report success."""
                    self.calls.append((record, context))
                    return True


u = FlextTargetLdapTestUtilities
__all__ = ["FlextTargetLdapTestUtilities", "u"]
