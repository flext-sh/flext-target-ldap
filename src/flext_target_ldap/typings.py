"""FLEXT Target LDAP Types - Domain-specific Singer LDAP target type definitions.

This module provides Singer LDAP target-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes

# =============================================================================
# TARGET LDAP-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Singer LDAP target operations
# =============================================================================


# Singer LDAP target domain TypeVars
class FlextTargetLdapTypes(FlextTypes):
    """Singer LDAP target-specific type definitions extending t.

    Domain-specific type system for Singer LDAP target operations.
    Contains ONLY complex LDAP target-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # SINGER TARGET TYPES - Complex Singer target protocol types
    # =========================================================================

    class SingerTarget:
        """Singer target protocol complex types."""

        type TargetConfiguration = dict[str, str | int | bool | dict[str, object]]
        type StreamConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.Json.JsonValue]
        ]
        type MessageProcessing = dict[
            str, str | list[dict[str, FlextTypes.Json.JsonValue]]
        ]
        type RecordHandling = dict[
            str, str | dict[str, FlextTypes.Json.JsonValue] | bool
        ]
        type StateManagement = dict[str, str | dict[str, FlextTypes.Json.JsonValue]]
        type BatchProcessing = dict[
            str, str | int | dict[str, FlextTypes.Json.JsonValue]
        ]

    # =========================================================================
    # LDAP DIRECTORY TYPES - Complex LDAP directory service types
    # =========================================================================

    class LdapDirectory:
        """LDAP directory service complex types."""

        type DirectoryConfiguration = dict[str, str | int | bool | dict[str, object]]
        type ConnectionManagement = dict[
            str, str | int | dict[str, FlextTypes.Json.JsonValue]
        ]
        type AuthenticationSettings = dict[str, str | bool | dict[str, object]]
        type SchemaDefinition = dict[str, str | list[str] | dict[str, object]]
        type DirectoryStructure = dict[str, str | dict[str, FlextTypes.Json.JsonValue]]
        type OperationalAttributes = dict[str, str | bool | dict[str, object]]

    # =========================================================================
    # LDAP ENTRY TYPES - Complex LDAP entry and attribute types
    # =========================================================================

    class LdapEntry:
        """LDAP entry and attribute complex types."""

        type EntryConfiguration = dict[str, str | bool | dict[str, object]]
        type AttributeMapping = dict[
            str,
            str | list[str] | dict[str, FlextTypes.Json.JsonValue],
        ]
        type ObjectClassDefinition = dict[
            str, str | dict[str, FlextTypes.Json.JsonValue]
        ]
        type DN = dict[str, str | dict[str, object]]
        type AttributeValues = dict[
            str,
            str | list[str] | dict[str, FlextTypes.Json.JsonValue],
        ]
        type EntryValidation = dict[str, bool | str | dict[str, object]]

    # =========================================================================
    # LDAP OPERATIONS TYPES - Complex LDAP operation types
    # =========================================================================

    class LdapOperations:
        """LDAP operations complex types."""

        type OperationConfiguration = dict[str, str | bool | int | dict[str, object]]
        type SearchOperations = dict[str, str | dict[str, FlextTypes.Json.JsonValue]]
        type ModifyOperations = dict[str, str | list[str] | dict[str, object]]
        type AddOperations = dict[str, dict[str, FlextTypes.Json.JsonValue]]
        type DeleteOperations = dict[str, str | bool | dict[str, object]]
        type BindOperations = dict[str, str | dict[str, object]]

    # =========================================================================
    # LDAP SECURITY TYPES - Complex LDAP security and authentication types
    # =========================================================================

    class LdapSecurity:
        """LDAP security and authentication complex types."""

        type SecurityConfiguration = dict[str, str | bool | dict[str, object]]
        type AuthenticationMethods = dict[
            str, str | dict[str, FlextTypes.Json.JsonValue]
        ]
        type TlsConfiguration = dict[str, str | bool | dict[str, object]]
        type CredentialManagement = dict[str, str | dict[str, object]]
        type AccessControl = dict[
            str, bool | str | dict[str, FlextTypes.Json.JsonValue]
        ]
        type CertificateHandling = dict[str, str | dict[str, object]]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[str, str | bool | dict[str, object]]
        type FieldMapping = dict[str, str | list[str] | dict[str, object]]
        type DataValidation = dict[str, str | dict[str, FlextTypes.Json.JsonValue]]
        type TypeConversion = dict[str, bool | str | dict[str, object]]
        type FilteringRules = dict[str, str | dict[str, FlextTypes.Json.JsonValue]]
        type TransformationResult = dict[str, dict[str, FlextTypes.Json.JsonValue]]

    # =========================================================================
    # STREAM PROCESSING TYPES - Complex stream handling types
    # =========================================================================

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[str, str | bool | int | dict[str, object]]
        type StreamMetadata = dict[str, str | dict[str, FlextTypes.Json.JsonValue]]
        type StreamRecord = dict[str, FlextTypes.Json.JsonValue | dict[str, object]]
        type StreamState = dict[str, str | int | dict[str, FlextTypes.Json.JsonValue]]
        type StreamBookmark = dict[str, str | int | dict[str, object]]
        type StreamSchema = dict[str, str | dict[str, FlextTypes.Json.JsonValue] | bool]

    # =========================================================================
    # ERROR HANDLING TYPES - Complex error management types
    # =========================================================================

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[str, bool | str | int | dict[str, object]]
        type ErrorRecovery = dict[str, str | bool | dict[str, object]]
        type ErrorReporting = dict[
            str, str | int | dict[str, FlextTypes.Json.JsonValue]
        ]
        type ErrorClassification = dict[str, str | int | dict[str, object]]
        type ErrorMetrics = dict[
            str, int | float | dict[str, FlextTypes.Json.JsonValue]
        ]
        type ErrorTracking = list[
            dict[str, str | int | dict[str, FlextTypes.Json.JsonValue]]
        ]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Convenience aliases for common patterns
    # =========================================================================

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextTargetLdapTypes.
        """

        # Common dictionary types
        type Dict = dict[str, object]
        """Type alias for generic dictionary (attribute name to value mapping)."""
        type Headers = dict[str, str]
        """Type alias for HTTP headers or attribute mapping headers."""

        # Common list types
        type StringList = list[str]
        """Type alias for list of strings (commonly used for attributes, errors, etc.)."""

    class TargetLdapCore:
        """Core Target LDAP-specific type aliases.

        Provides standardized type aliases for frequent Target LDAP patterns.
        Access parent core types via inheritance from FlextTargetLdapTypes.
        Reduces generic dict/list usage throughout the Target LDAP codebase.
        """

        # REMOVED: Simple type aliases like Dict = dict[str, object]
        # Use dict[str, object] directly instead of creating aliases
        type ErrorResultDict = dict[str, object]
        type MetricsDict = dict[str, float]

        # Target LDAP lists
        type LdapEntryList = list[dict[str, object]]
        type SingerRecordList = list[dict[str, object]]
        type StreamNameList = list[str]
        type AttributeNameList = list[str]
        type OperationList = list[str]
        type ErrorList = list[str]
        type MetricsList = list[float]
        type ResultList = list[dict[str, object]]

    # =========================================================================
    # SINGER TARGET LDAP PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project:
        """Singer Target LDAP-specific project types.

        Adds Singer target LDAP-specific project types.
        Follows domain separation principle:
        Singer target LDAP domain owns LDAP loading and Singer protocol-specific types.
        Access parent types via inheritance from FlextTargetLdapTypes.
        """

        # Singer target LDAP-specific project types extending the generic ones
        type TargetLdapProjectType = Literal[
            # Generic types inherited from t
            "library",
            "application",
            "service",
            # Singer target LDAP-specific types
            "singer-target",
            "ldap-loader",
            "directory-loader",
            "singer-target-ldap",
            "target-ldap",
            "ldap-connector",
            "directory-connector",
            "singer-protocol",
            "ldap-integration",
            "directory-service",
            "ldap-target",
            "singer-stream",
            "etl-target",
            "data-pipeline",
            "ldap-sink",
            "singer-integration",
        ]

        # Singer target LDAP-specific project configurations
        type SingerTargetLdapProjectConfig = dict[str, object]
        type LdapLoaderConfig = dict[str, str | int | bool | list[str]]
        type SingerProtocolConfig = dict[str, bool | str | dict[str, object]]
        type TargetLdapPipelineConfig = dict[str, object]

    class TargetLdap:
        """Target LDAP types namespace for cross-project access.

        Provides organized access to all Target LDAP types for other FLEXT projects.
        Usage: Other projects can reference `t.TargetLdap.SingerTarget.*`, `t.TargetLdap.Project.*`, etc.
        This enables consistent namespace patterns for cross-project type access.

        Examples:
            from flext_target_ldap.typings import t
            config: t.TargetLdap.Project.TapLdapProjectConfig = ...
            message: t.TargetLdap.SingerTarget.TargetConfiguration = ...

        Note: Namespace composition via inheritance - no aliases needed.
        Access parent namespaces directly through inheritance.

        """


# Alias for simplified usage
t = FlextTargetLdapTypes

# Namespace composition via class inheritance
# TargetLdap namespace provides access to nested classes through inheritance
# Access patterns:
# - t.TargetLdap.* for Target LDAP-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

# =============================================================================
# PUBLIC API EXPORTS - Singer LDAP target TypeVars and types
# =============================================================================

__all__ = [
    "FlextTargetLdapTypes",
    "t",
]
