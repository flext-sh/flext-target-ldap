"""FLEXT Target LDAP Constants - LDAP target loading constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from flext_ldap import c
from flext_ldap.constants import FlextLdapConstants
from flext_ldif.constants import FlextLdifConstants as ldif_c


class FlextTargetLdapConstants(FlextLdapConstants):
    """LDAP target loading-specific constants following FLEXT unified pattern with nested domains.

    Extends FlextLdapConstants to inherit all LDAP and LDIF constants, adding
    target-specific constants in the TargetLdap namespace.

    Hierarchy:
        FlextConstants (flext-core)
        └── FlextLdifConstants (flext-ldif)
            └── FlextLdapConstants (flext-ldap)
                └── FlextTargetLdapConstants (this module)

    Access patterns:
        - c.TargetLdap.* (target-specific constants)
        - c.Ldap.* (inherited from FlextLdapConstants)
        - c.* (inherited from FlextLdifConstants via FlextLdapConstants)
        - c.Network.*, c.Errors.*, etc. (inherited from FlextConstants)
    """

    class TargetLdap:
        """Target LDAP domain-specific constants namespace."""

        class ObjectClass(StrEnum):
            """Standard LDAP object classes for target operations.

            Defines the common object classes used in enterprise LDAP directories
            for users, groups, and organizational structures.

            DRY Pattern:
                StrEnum is the single source of truth. Use ObjectClass.PERSON.value
                or ObjectClass.PERSON directly - no base strings needed.
            """

            # Base object classes
            TOP = "top"

            # Person object classes
            PERSON = "person"
            ORGANIZATIONAL_PERSON = "organizationalPerson"
            INET_ORG_PERSON = "inetOrgPerson"

            # Group object classes
            GROUP_OF_NAMES = "groupOfNames"
            GROUP_OF_UNIQUE_NAMES = "groupOfUniqueNames"
            POSIX_GROUP = "posixGroup"

            # Organizational object classes
            ORGANIZATION = "organization"
            ORGANIZATIONAL_UNIT = "organizationalUnit"
            ORGANIZATIONAL_ROLE = "organizationalRole"

            # System object classes
            DOMAIN = "domain"
            DOMAIN_COMPONENT = "dcObject"

        class Connection:
            """LDAP connection configuration constants for target operations."""

            DEFAULT_HOST: Final[str] = c.Platform.DEFAULT_HOST
            DEFAULT_PORT: Final[int] = c.Ldap.ConnectionDefaults.PORT
            DEFAULT_TIMEOUT: Final[int] = c.Ldap.ConnectionDefaults.TIMEOUT
            MAX_PORT_NUMBER: Final[int] = 65535

            class Ldaps:
                """Secure LDAP connection settings."""

                DEFAULT_PORT: Final[int] = 636

        class Processing:
            """Singer target data processing configuration.

            Note: Does not override parent Processing class to avoid inheritance conflicts.
            """

            DEFAULT_BATCH_SIZE: Final[int] = c.Performance.BatchProcessing.DEFAULT_SIZE
            MAX_BATCH_SIZE: Final[int] = c.Performance.BatchProcessing.MAX_ITEMS
            DEFAULT_PAGE_SIZE: Final[int] = c.Pagination.DEFAULT_PAGE_SIZE

        class Operations:
            """LDAP operation types and commands.

            Note: For type-safe operation handling, use c.Ldap.OperationType
            StrEnum instead of this list. This list is kept for backward compatibility.

            DRY Pattern:
                TYPES tuple is generated from OperationType StrEnum members to eliminate
                string duplication. The StrEnum is the single source of truth.
            """

            # Generate tuple from OperationType StrEnum members (eliminates string duplication)
            # Only include operations relevant for target operations: ADD, MODIFY, DELETE, MODIFY_DN
            TYPES: Final[tuple[str, ...]] = tuple(
                member.name
                for member in (
                    c.Ldap.OperationType.ADD,
                    c.Ldap.OperationType.MODIFY,
                    c.Ldap.OperationType.DELETE,
                    c.Ldap.OperationType.MODIFY,
                )
            )

        class Loading:
            """Target-specific loading configuration."""

            DEFAULT_LOAD_TIMEOUT: Final[int] = c.Ldap.ConnectionDefaults.TIMEOUT
            MAX_LOAD_RETRIES: Final[int] = c.Reliability.MAX_RETRY_ATTEMPTS
            LOAD_RETRY_DELAY: Final[float] = c.Reliability.DEFAULT_RETRY_DELAY_SECONDS

        class Validation:
            """Target-specific validation configuration.

            Note: Does not override parent Validation class to avoid inheritance conflicts.
            """

            # Validation constants from flext-ldif (parent of flext-ldap)
            MAX_DN_LENGTH: Final[int] = ldif_c.Ldif.LdifValidation.MAX_DN_LENGTH


c = FlextTargetLdapConstants

__all__ = ["FlextTargetLdapConstants", "c"]
