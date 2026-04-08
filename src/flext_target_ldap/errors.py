"""Domain-specific exceptions for LDAP target operations using factory pattern to eliminate duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import e


class FlextTargetLdapError(e.BaseError):
    """Generic LDAP target errors."""


class FlextTargetLdapValidationError(e.ValidationError):
    """LDAP target validation-specific errors."""


class FlextTargetLdapConfigurationError(e.ConfigurationError):
    """LDAP target configuration-specific errors."""


class FlextTargetLdapProcessingError(e.OperationError):
    """LDAP target processing-specific errors."""


class FlextTargetLdapConnectionError(e.ConnectionError):
    """LDAP target connection-specific errors."""


class FlextTargetLdapAuthenticationError(e.AuthenticationError):
    """LDAP target authentication-specific errors."""


class FlextTargetLdapTimeoutError(e.TimeoutError):
    """LDAP target timeout-specific errors."""


__all__ = [
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapError",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapTimeoutError",
    "FlextTargetLdapValidationError",
]
