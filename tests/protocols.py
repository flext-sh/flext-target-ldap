"""Test protocol definitions for flext-target-ldap.

Provides FlextTargetLdapTestProtocols, combining FlextTestsProtocols with
FlextTargetLdapProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_target_ldap import FlextTargetLdapProtocols


class FlextTargetLdapTestProtocols(FlextTestsProtocols, FlextTargetLdapProtocols):
    """Test protocols combining FlextTestsProtocols and FlextTargetLdapProtocols.

    Provides access to the project-local `p.TargetLdap.Tests.*` namespace while
    preserving the inherited test and domain protocol surfaces.
    """

    class TargetLdap(FlextTargetLdapProtocols.TargetLdap):
        """Target LDAP domain test protocols namespace."""

        class Tests(FlextTestsProtocols.Tests):
            """Target LDAP-specific test protocols."""


p = FlextTargetLdapTestProtocols
__all__ = ["FlextTargetLdapTestProtocols", "p"]
