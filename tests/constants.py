"""Module skeleton for TestsFlextTargetLdapConstants.

Test constants for flext-target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdapConstants
from flext_tests import FlextTestsConstants


class TestsFlextTargetLdapConstants(FlextTargetLdapConstants, FlextTestsConstants):
    """Test constants for flext-target-ldap."""

    class TargetLdap(FlextTargetLdapConstants.TargetLdap):
        """Target LDAP domain test constants namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Target LDAP-specific test constants."""

            EXPECTED_DATA_COUNT: int = 3


c = TestsFlextTargetLdapConstants
__all__: list[str] = ["TestsFlextTargetLdapConstants", "c"]
