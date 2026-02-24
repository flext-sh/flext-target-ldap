"""Utilities for flext-target-ldap tests - uses u.TargetLdap.Tests.* namespace pattern.

This module provides test-specific utilities that extend the main flext-target-ldap utilities.
Uses the unified namespace pattern u.TargetLdap.Tests.* for test-only objects.
Combines FlextTestsUtilities functionality with project-specific test utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.utilities import FlextTargetLdapUtilities
from flext_tests import FlextTestsUtilities


class TestsFlextTargetLdapUtilities(FlextTestsUtilities, FlextTargetLdapUtilities):
    """Test utilities for flext-target-ldap extending both test and project utilities."""

    class TargetLdap(FlextTargetLdapUtilities.TargetLdap):
        """TargetLdap test namespace."""

        class Tests:
            """Internal tests declarations."""


u = TestsFlextTargetLdapUtilities
tu = TestsFlextTargetLdapUtilities

__all__ = ["TestsFlextTargetLdapUtilities", "tu", "u"]
