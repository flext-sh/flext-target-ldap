"""Utilities for flext-target-ldap tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdapUtilities
from flext_tests import FlextTestsUtilities


class TestsFlextTargetLdapUtilities(FlextTestsUtilities, FlextTargetLdapUtilities):
    """Test utilities for flext-target-ldap extending both test and project utilities."""


u = TestsFlextTargetLdapUtilities
__all__: list[str] = ["TestsFlextTargetLdapUtilities", "u"]
