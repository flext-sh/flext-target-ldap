"""FLEXT Target LDAP Constants - LDAP target loading constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants


class FlextTargetLdapConstants(FlextConstants):
    """LDAP target loading-specific constants following flext-core patterns."""

    # LDAP Connection Configuration
    DEFAULT_LDAP_HOST = "localhost"
    DEFAULT_LDAP_PORT = 389
    DEFAULT_LDAPS_PORT = 636
    DEFAULT_LDAP_TIMEOUT = 30

    # Singer Target Configuration
    DEFAULT_BATCH_SIZE = 1000
    MAX_BATCH_SIZE = 10000

    # LDAP Operations
    LDAP_OPERATIONS: ClassVar[list[str]] = ["ADD", "MODIFY", "DELETE", "MODDN"]


__all__ = ["FlextTargetLdapConstants"]
