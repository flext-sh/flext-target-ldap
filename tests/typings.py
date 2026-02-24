"""Types for flext-target-ldap tests - uses t.Ldap.Tests.* namespace pattern.

This module provides test-specific types that extend the main flext-target-ldap types.
Uses the unified namespace pattern t.Ldap.Tests.* for test-only objects.
Combines FlextTestsTypes functionality with project-specific test types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.typings import FlextTargetLdapTypes
from flext_tests import FlextTestsTypes


class TestsFlextTargetLdapTypes(FlextTestsTypes, FlextTargetLdapTypes):
    """Test types for flext-target-ldap extending both test and project types."""

    class TargetLdap(FlextTargetLdapTypes.TargetLdap):
        """TargetLdap test namespace."""

        class Tests:
            """Internal tests declarations."""


t = TestsFlextTargetLdapTypes
tt = TestsFlextTargetLdapTypes

__all__ = ["TestsFlextTargetLdapTypes", "t", "tt"]
