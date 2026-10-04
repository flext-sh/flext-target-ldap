"""Module skeleton for TestsFlextTargetLdapConstants.

Test constants for flext-target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from typing import ClassVar

from flext_tests import FlextTestsConstants

from flext_target_ldap import FlextTargetLdapConstants


def _docker_admin_password() -> str:
    """Resolve the shared test OpenLDAP admin password (env override allowed).

    Returns:
        The resulting ``str``.
    """
    return os.getenv("FLEXT_LDAP_TEST_DOCKER_ADMIN_PASSWORD", "") or "admin123"


class TestsFlextTargetLdapConstants(FlextTargetLdapConstants, FlextTestsConstants):
    """Test constants for flext-target-ldap."""

    class TargetLdap(FlextTargetLdapConstants.TargetLdap):
        """Target LDAP domain test constants namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Target LDAP-specific test constants."""

            EXPECTED_DATA_COUNT: ClassVar[int] = 3

            # Identity provisioned by the shared OpenLDAP runtime
            # (docker/docker-compose.openldap.yml ``LDAP_BASE_DN`` /
            # ``LDAP_ADMIN_PASSWORD`` / healthcheck bind DN); mirrors the
            # flext-ldap ``c.Ldap.Tests.DOCKER_*`` constants for the same
            # container.
            DOCKER_BASE_DN: ClassVar[str] = "dc=flext,dc=local"
            DOCKER_ADMIN_DN: ClassVar[str] = "cn=admin,dc=flext,dc=local"
            DOCKER_ADMIN_PASSWORD: ClassVar[str] = _docker_admin_password()


c = TestsFlextTargetLdapConstants
__all__: list[str] = ["TestsFlextTargetLdapConstants", "c"]
