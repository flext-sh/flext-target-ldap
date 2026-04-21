"""Test protocol definitions for flext-target-ldap.

Provides TestsFlextTargetLdapProtocols, combining TestsFlextProtocols with
FlextTargetLdapProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_target_ldap import FlextTargetLdapProtocols


class TestsFlextTargetLdapProtocols(FlextTestsProtocols, FlextTargetLdapProtocols):
    """Test protocols combining TestsFlextProtocols and FlextTargetLdapProtocols.

    Provides access to the project-local `p.TargetLdap.Tests.*` namespace while
    preserving the inherited test and domain protocol surfaces.
    """

    class TargetLdap(FlextTargetLdapProtocols.TargetLdap):
        """Target LDAP local test protocols namespace."""

        class Tests:
            """Target LDAP-specific test protocols."""


p = TestsFlextTargetLdapProtocols
__all__: list[str] = ["TestsFlextTargetLdapProtocols", "p"]
