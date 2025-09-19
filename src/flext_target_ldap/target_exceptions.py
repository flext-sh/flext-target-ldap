"""Domain-specific exceptions for LDAP target operations using factory pattern to eliminate duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions

# Generate all standard exceptions using factory pattern
_target_ldap_exceptions = FlextExceptions.create_module_exception_classes(
    "flext_target_ldap",
)

# Export factory-created exception classes (using actual factory keys)
# create_module_exception_classes uses UPPER_SNAKE keys: MODULEPREFIXError, etc.
_PREFIX = "FLEXT_TARGET_LDAP"
FlextTargetLdapError = _target_ldap_exceptions[f"{_PREFIX}Error"]
FlextTargetLdapValidationError = _target_ldap_exceptions[f"{_PREFIX}ValidationError"]
FlextTargetLdapConfigurationError = _target_ldap_exceptions[
    f"{_PREFIX}ConfigurationError"
]
FlextTargetLdapProcessingError = _target_ldap_exceptions[f"{_PREFIX}ProcessingError"]
FlextTargetLdapConnectionError = _target_ldap_exceptions[f"{_PREFIX}ConnectionError"]
FlextTargetLdapAuthenticationError = _target_ldap_exceptions[
    f"{_PREFIX}AuthenticationError"
]
FlextTargetLdapTimeoutError = _target_ldap_exceptions[f"{_PREFIX}TimeoutError"]

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
