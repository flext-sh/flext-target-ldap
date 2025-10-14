"""Domain-specific exceptions for LDAP target operations using factory pattern to eliminate duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextCore


# ✅ DIRECT EXCEPTION CLASSES: Use direct inheritance instead of factory pattern
class FlextTargetLdapError(FlextCore.Exceptions.Error):
    """Generic LDAP target errors."""


class FlextTargetLdapValidationError(FlextCore.Exceptions.ValidationError):
    """LDAP target validation-specific errors."""


class FlextTargetLdapConfigurationError(FlextCore.Exceptions.ConfigurationError):
    """LDAP target configuration-specific errors."""


class FlextTargetLdapProcessingError(FlextCore.Exceptions.ProcessingError):
    """LDAP target processing-specific errors."""


class FlextTargetLdapConnectionError(FlextCore.Exceptions.ConnectionError):
    """LDAP target connection-specific errors."""


class FlextTargetLdapAuthenticationError(FlextCore.Exceptions.AuthenticationError):
    """LDAP target authentication-specific errors."""


class FlextTargetLdapTimeoutError(FlextCore.Exceptions.TimeoutError):
    """LDAP target timeout-specific errors."""


# Create backward-compatible aliases for existing code
FlextTargetLdapLoadError = FlextTargetLdapProcessingError  # Load errors are processing
FlextTargetLdapSchemaError = FlextTargetLdapValidationError  # Schema is validation
FlextTargetLdapWriteError = FlextTargetLdapProcessingError  # Write is processing


__all__ = [
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapError",
    "FlextTargetLdapLoadError",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapSchemaError",
    "FlextTargetLdapTimeoutError",
    "FlextTargetLdapValidationError",
    "FlextTargetLdapWriteError",
]
