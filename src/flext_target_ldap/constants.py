"""FLEXT Target LDAP Constants - LDAP target loading constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants, FlextTypes
from flext_ldap.constants import FlextLDAPConstants


class FlextTargetLdapConstants(FlextConstants):
    """LDAP target loading-specific constants following FLEXT unified pattern with nested domains.

    Composes with FlextLDAPConstants to avoid duplication and ensure consistency.
    """

    class Connection:
        """LDAP connection configuration constants."""

        class Ldap:
            """Standard LDAP connection settings."""

            DEFAULT_HOST = (
                FlextLDAPConstants.Protocol.DEFAULT_HOST
                if hasattr(FlextLDAPConstants.Protocol, "DEFAULT_HOST")
                else FlextConstants.Platform.DEFAULT_HOST
            )
            DEFAULT_PORT = FlextLDAPConstants.Protocol.DEFAULT_PORT
            DEFAULT_TIMEOUT = FlextLDAPConstants.Protocol.DEFAULT_TIMEOUT_SECONDS
            MAX_PORT_NUMBER = 65535

        class Ldaps:
            """Secure LDAP connection settings."""

            DEFAULT_PORT = FlextLDAPConstants.Protocol.DEFAULT_SSL_PORT

    class Processing:
        """Singer target data processing configuration."""

        DEFAULT_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        MAX_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.MAX_ITEMS
        DEFAULT_PAGE_SIZE = FlextLDAPConstants.Connection.DEFAULT_PAGE_SIZE

    class Operations:
        """LDAP operation types and commands."""

        TYPES: ClassVar[FlextTypes.StringList] = ["ADD", "MODIFY", "DELETE", "MODDN"]

    class Loading:
        """Target-specific loading configuration."""

        DEFAULT_LOAD_TIMEOUT = FlextLDAPConstants.DEFAULT_TIMEOUT
        MAX_LOAD_RETRIES = FlextLDAPConstants.LdapRetry.CONNECTION_MAX_RETRIES
        LOAD_RETRY_DELAY = FlextLDAPConstants.LdapRetry.CONNECTION_RETRY_DELAY

    class Validation:
        """Target-specific validation configuration."""

        DN_VALIDATION_PATTERN = FlextLDAPConstants.Validation.DN_PATTERN
        FILTER_VALIDATION_PATTERN = FlextLDAPConstants.Validation.FILTER_PATTERN
        MAX_DN_LENGTH = FlextLDAPConstants.Validation.MAX_DN_LENGTH


__all__ = ["FlextTargetLdapConstants"]
