"""Test models module for flext-target-ldap.

Provides tm alias for test models with namespace m.Ldap.Tests.* pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.tests.models import TestsFlextTargetLdapModels

# Runtime alias for test models
m = TestsFlextTargetLdapModels

__all__ = [
    "m",
]
