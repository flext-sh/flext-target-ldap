"""Test protocol definitions for flext-target-ldap.

Provides TestsFlextTargetLdapProtocols, combining FlextTestsProtocols with
FlextTargetLdapProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap.protocols import FlextTargetLdapProtocols
from flext_tests import FlextTestsProtocols


class TestsFlextTargetLdapProtocols(FlextTestsProtocols, FlextTargetLdapProtocols):
    """Test protocols combining FlextTestsProtocols and FlextTargetLdapProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.TargetLdap.* (from FlextTargetLdapProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with TargetLdap-specific protocols.
        """

        class TargetLdap:
            """TargetLdap-specific test protocols."""


# Runtime aliases
p = TestsFlextTargetLdapProtocols
p = TestsFlextTargetLdapProtocols

__all__ = ["TestsFlextTargetLdapProtocols", "p"]
