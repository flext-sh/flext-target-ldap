"""Module skeleton for FlextTargetLdapTestConstants.

Test constants for flext-target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_target_ldap import FlextTargetLdapConstants


class FlextTargetLdapTestConstants(FlextTestsConstants, FlextTargetLdapConstants):
    """Test constants for flext-target-ldap."""

    class TargetLdap(FlextTargetLdapConstants.TargetLdap):
        """Target LDAP domain test constants namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Target LDAP-specific test constants."""


c = FlextTargetLdapTestConstants
__all__ = ["FlextTargetLdapTestConstants", "c"]
