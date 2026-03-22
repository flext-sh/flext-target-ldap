"""Test protocol definitions for flext-target-ldap.

Provides FlextTargetLdapTestProtocols, combining FlextTestsProtocols with
FlextTargetLdapProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_target_ldap.protocols import FlextTargetLdapProtocols


class FlextTargetLdapTestProtocols(FlextTestsProtocols, FlextTargetLdapProtocols):
    """Test protocols combining FlextTestsProtocols and FlextTargetLdapProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.TargetLdap.* (from FlextTargetLdapProtocols)
    """

    class Tests(FlextTestsProtocols.Tests):
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with TargetLdap-specific protocols.
        """

        class TargetLdap:
            """TargetLdap-specific test protocols."""


p = FlextTargetLdapTestProtocols
__all__ = ["FlextTargetLdapTestProtocols", "p"]
