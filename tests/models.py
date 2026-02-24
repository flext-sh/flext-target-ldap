"""Test models for flext-target-ldap tests.

Provides TestsFlextTargetLdapModels, extending FlextTestsModels with
flext-target-ldap-specific models using COMPOSITION INHERITANCE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap.models import FlextTargetLdapModels
from flext_tests.models import FlextTestsModels


class TestsFlextTargetLdapModels(FlextTestsModels, FlextTargetLdapModels):
    """Models for flext-target-ldap tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsModels - for test infrastructure (.Tests.*)
    2. FlextTargetLdapModels - for domain models

    Access patterns:
    - tm.Tests.* (generic test models from FlextTestsModels)
    - tm.* (Target LDAP domain models)
    - m.* (production models via alternative alias)
    """

    class Tests:
        """Project-specific test fixtures namespace."""

        class TargetLdap:
            """Target LDAP-specific test fixtures."""


# Short aliases per FLEXT convention
tm = TestsFlextTargetLdapModels
m = TestsFlextTargetLdapModels

__all__ = [
    "TestsFlextTargetLdapModels",
    "m",
    "tm",
]
