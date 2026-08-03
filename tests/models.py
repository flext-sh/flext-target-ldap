"""Test models for flext-target-ldap tests.

Provides TestsFlextTargetLdapModels, extending TestsFlextModels with
flext-target-ldap-specific models using COMPOSITION INHERITANCE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap import FlextTargetLdapModels
from flext_tests import FlextTestsModels


class TestsFlextTargetLdapModels(FlextTestsModels, FlextTargetLdapModels):
    """Models for flext-target-ldap tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. TestsFlextModels - for test infrastructure (.Tests.*)
    2. FlextTargetLdapModels - for domain models

    Access patterns:
    - m.TargetLdap.Tests.* (project-local Domain.Tests fixtures)
    - m.* (Target LDAP domain models via shared MRO)
    """

    class TargetLdap(FlextTargetLdapModels.TargetLdap):
        """Target LDAP domain test models namespace."""

        class Tests(FlextTestsModels.Tests):
            """Target LDAP-specific test fixtures."""


m = TestsFlextTargetLdapModels

__all__: list[str] = ["TestsFlextTargetLdapModels", "m"]
