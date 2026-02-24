"""Test protocol definitions for flext-target-ldap.

Provides TestsFlextTargetLdapProtocols, combining FlextTestsProtocols with
FlextTargetLdapProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_ldap.protocols import FlextTargetLdapProtocols
from flext_tests.protocols import FlextTestsProtocols


class TestsFlextTargetLdapProtocols(FlextTestsProtocols, FlextTargetLdapProtocols):
    """Test protocols combining FlextTestsProtocols and FlextTargetLdapProtocols.

    Provides access to:
    - tp.Tests.Docker.* (from FlextTestsProtocols)
    - tp.Tests.Factory.* (from FlextTestsProtocols)
    - tp.TargetLdap.* (from FlextTargetLdapProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with TargetLdap-specific protocols.
        """

        class TargetLdap:
            """TargetLdap-specific test protocols."""


# Runtime aliases
p = TestsFlextTargetLdapProtocols
tp = TestsFlextTargetLdapProtocols

__all__ = ["TestsFlextTargetLdapProtocols", "p", "tp"]
