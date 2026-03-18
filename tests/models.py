"""Test models for flext-target-ldap tests.

Provides TestsFlextTargetLdapModels, extending m with
flext-target-ldap-specific models using COMPOSITION INHERITANCE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import m

from flext_target_ldap.models import FlextTargetLdapModels


class TestsFlextTargetLdapModels(m, FlextTargetLdapModels):
    """Models for flext-target-ldap tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. m - for test infrastructure (.Tests.*)
    2. FlextTargetLdapModels - for domain models

    Access patterns:
    - tm.Tests.* (generic test models from m)
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
