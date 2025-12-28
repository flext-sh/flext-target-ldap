"""Test types module for flext-target-ldap.

Provides tt alias for test types with namespace t.Ldap.Tests.* pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.tests.typings import TestsFlextTargetLdapTypes

# Runtime alias for test types
t = TestsFlextTargetLdapTypes

__all__ = [
    "t",
]
