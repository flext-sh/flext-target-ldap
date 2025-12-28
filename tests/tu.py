"""Test utilities module for flext-target-ldap.

Provides tu alias for test utilities with namespace u.Ldap.Tests.* pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.tests.utilities import TestsFlextTargetLdapUtilities

# Runtime alias for test utilities
u = TestsFlextTargetLdapUtilities

__all__ = [
    "u",
]
