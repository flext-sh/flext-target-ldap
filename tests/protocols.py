"""Test protocol definitions for flext-target-ldap.

Provides TestsFlextTargetLdapProtocols, combining p with
FlextTargetLdapProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_target_ldap.protocols import FlextTargetLdapProtocols


class TestsFlextTargetLdapProtocols(p, FlextTargetLdapProtocols):
    """Test protocols combining p and FlextTargetLdapProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.TargetLdap.* (from FlextTargetLdapProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends p.Tests with TargetLdap-specific protocols.
        """

        class TargetLdap:
            """TargetLdap-specific test protocols."""


__all__ = ["TestsFlextTargetLdapProtocols", "p"]

p = TestsFlextTargetLdapProtocols
