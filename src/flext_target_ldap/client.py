"""LDAP client for flext-target-ldap using flext-ldap infrastructure.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module eliminates code duplication by using the FLEXT LDAP infrastructure
implementation from flext-ldap project.
"""

from __future__ import annotations

from flext_core import get_logger
from flext_ldap import (
    FlextLdapClient,
    FlextLdapConnectionConfig,
    FlextLdapEntry,
)

logger = get_logger(__name__)

# Use flext-ldap client instead of reimplementing LDAP functionality
LDAPClient = FlextLdapClient
LDAPConnectionConfig = FlextLdapConnectionConfig
LDAPEntry = FlextLdapEntry

__all__ = [
    "LDAPClient",
    "LDAPConnectionConfig",
    "LDAPEntry",
]
