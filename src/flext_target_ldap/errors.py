"""Domain-specific exceptions for LDAP target operations using factory pattern to eliminate duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextExceptions


class FlextTargetLdapError(FlextExceptions.BaseError):
    """Generic LDAP target errors."""


class FlextTargetLdapValidationError(FlextExceptions.ValidationError):
    """LDAP target validation-specific errors."""


class FlextTargetLdapConfigurationError(FlextExceptions.ConfigurationError):
    """LDAP target configuration-specific errors."""


class FlextTargetLdapProcessingError(FlextExceptions.OperationError):
    """LDAP target processing-specific errors."""


class FlextTargetLdapConnectionError(FlextExceptions.ConnectionError):
    """LDAP target connection-specific errors."""


class FlextTargetLdapAuthenticationError(FlextExceptions.AuthenticationError):
    """LDAP target authentication-specific errors."""


class FlextTargetLdapTimeoutError(FlextExceptions.TimeoutError):
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
