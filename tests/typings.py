"""Types for flext-target-ldap tests - uses t.TargetLdap.Tests.* namespace pattern.

This module provides test-specific types that extend the main flext-target-ldap types.
Uses the unified namespace pattern t.TargetLdap.Tests.* for test-only objects.
Combines FlextTestsTypes functionality with project-specific test types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_target_ldap.typings import FlextTargetLdapTypes


class FlextTargetLdapTestTypes(FlextTestsTypes, FlextTargetLdapTypes):
    """Test types for flext-target-ldap extending both test and project types."""

    class TargetLdap:
        """TargetLdap test namespace."""

        class Tests:
            """Internal tests declarations."""


t = FlextTargetLdapTestTypes
tt = FlextTargetLdapTestTypes
__all__ = ["FlextTargetLdapTestTypes", "t", "tt"]
