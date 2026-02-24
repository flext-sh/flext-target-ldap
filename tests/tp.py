"""Test protocols module for flext-target-ldap.

Provides p alias for test protocols with namespace p.Ldap.Tests.* pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_ldap.tests.protocols import TestsFlextTargetLdapProtocols

# Runtime alias for test protocols
p = TestsFlextTargetLdapProtocols

__all__ = [
    "p",
]
