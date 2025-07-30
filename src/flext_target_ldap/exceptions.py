"""LDAP target exception hierarchy using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for LDAP target operations inheriting from flext-core.
"""

from __future__ import annotations

from flext_core.exceptions import (
    FlextAuthenticationError,
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextValidationError,
)


class FlextTargetLdapError(FlextError):
    """Base exception for LDAP target operations."""

    def __init__(
        self,
        message: str = "LDAP target error",
        ldap_server: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target error with context."""
        context = kwargs.copy()
        if ldap_server is not None:
            context["ldap_server"] = ldap_server

        super().__init__(message, error_code="LDAP_TARGET_ERROR", context=context)


class FlextTargetLdapConnectionError(FlextConnectionError):
    """LDAP target connection errors."""

    def __init__(
        self,
        message: str = "LDAP target connection failed",
        ldap_server: str | None = None,
        port: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target connection error with context."""
        context = kwargs.copy()
        if ldap_server is not None:
            context["ldap_server"] = ldap_server
        if port is not None:
            context["port"] = port

        super().__init__(f"LDAP target connection: {message}", **context)


class FlextTargetLdapAuthenticationError(FlextAuthenticationError):
    """LDAP target authentication errors."""

    def __init__(
        self,
        message: str = "LDAP target authentication failed",
        bind_dn: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target authentication error with context."""
        context = kwargs.copy()
        if bind_dn is not None:
            context["bind_dn"] = bind_dn

        super().__init__(f"LDAP target auth: {message}", **context)


class FlextTargetLdapValidationError(FlextValidationError):
    """LDAP target validation errors."""

    def __init__(
        self,
        message: str = "LDAP target validation failed",
        field: str | None = None,
        value: object = None,
        entry_dn: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target validation error with context."""
        validation_details = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if entry_dn is not None:
            context["entry_dn"] = entry_dn

        super().__init__(
            f"LDAP target validation: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextTargetLdapConfigurationError(FlextConfigurationError):
    """LDAP target configuration errors."""

    def __init__(
        self,
        message: str = "LDAP target configuration error",
        config_key: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key

        super().__init__(f"LDAP target config: {message}", **context)


class FlextTargetLdapProcessingError(FlextProcessingError):
    """LDAP target processing errors."""

    def __init__(
        self,
        message: str = "LDAP target processing failed",
        operation: str | None = None,
        entry_dn: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target processing error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if entry_dn is not None:
            context["entry_dn"] = entry_dn

        super().__init__(f"LDAP target processing: {message}", **context)


class FlextTargetLdapOperationError(FlextTargetLdapError):
    """LDAP target directory operation errors."""

    def __init__(
        self,
        message: str = "LDAP target operation failed",
        operation_type: str | None = None,
        entry_dn: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target operation error with context."""
        context = kwargs.copy()
        if operation_type is not None:
            context["operation_type"] = operation_type
        if entry_dn is not None:
            context["entry_dn"] = entry_dn

        super().__init__(f"LDAP target operation: {message}", **context)


class FlextTargetLdapBindError(FlextTargetLdapError):
    """LDAP target bind operation errors."""

    def __init__(
        self,
        message: str = "LDAP target bind failed",
        bind_dn: str | None = None,
        bind_type: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target bind error with context."""
        context = kwargs.copy()
        if bind_dn is not None:
            context["bind_dn"] = bind_dn
        if bind_type is not None:
            context["bind_type"] = bind_type

        super().__init__(f"LDAP target bind: {message}", **context)


class FlextTargetLdapSchemaError(FlextValidationError):
    """LDAP target schema validation errors."""

    def __init__(
        self,
        message: str = "LDAP target schema error",
        attribute_name: str | None = None,
        object_class: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target schema error with context."""
        validation_details = {}
        if attribute_name is not None:
            validation_details["field"] = attribute_name

        context = kwargs.copy()
        if object_class is not None:
            context["object_class"] = object_class

        super().__init__(
            f"LDAP target schema: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextTargetLdapWriteError(FlextTargetLdapError):
    """LDAP target write operation errors."""

    def __init__(
        self,
        message: str = "LDAP target write failed",
        operation: str | None = None,
        entry_dn: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDAP target write error with context."""
        context = kwargs.copy()
        if operation is not None:
            context["operation"] = operation
        if entry_dn is not None:
            context["entry_dn"] = entry_dn

        super().__init__(f"LDAP target write: {message}", **context)


__all__ = [
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapBindError",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapError",
    "FlextTargetLdapOperationError",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapSchemaError",
    "FlextTargetLdapValidationError",
    "FlextTargetLdapWriteError",
]
