"""FLEXT Target LDAP Types - Domain-specific Singer LDAP target type definitions.

This module provides Singer LDAP target-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

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
    """Singer LDAP target-specific type definitions extending FlextTypes.

    Domain-specific type system for Singer LDAP target operations.
    Contains ONLY complex LDAP target-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # SINGER TARGET TYPES - Complex Singer target protocol types
    # =========================================================================

    class SingerTarget:
        """Singer target protocol complex types."""

        type TargetConfiguration = dict[
            str, str | int | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type StreamConfiguration = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type MessageProcessing = dict[
            str, str | list[dict[str, FlextTargetLdapTypes.Core.JsonValue]]
        ]
        type RecordHandling = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue] | bool
        ]
        type StateManagement = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type BatchProcessing = dict[
            str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]

    # =========================================================================
    # LDAP DIRECTORY TYPES - Complex LDAP directory service types
    # =========================================================================

    class LdapDirectory:
        """LDAP directory service complex types."""

        type DirectoryConfiguration = dict[
            str, str | int | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type ConnectionManagement = dict[
            str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type AuthenticationSettings = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type SchemaDefinition = dict[str, str | list[str] | dict[str, object]]
        type DirectoryStructure = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type OperationalAttributes = dict[str, str | bool | dict[str, object]]

    # =========================================================================
    # LDAP ENTRY TYPES - Complex LDAP entry and attribute types
    # =========================================================================

    class LdapEntry:
        """LDAP entry and attribute complex types."""

        type EntryConfiguration = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type AttributeMapping = dict[
            str, str | list[str] | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type ObjectClassDefinition = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type DistinguishedName = dict[str, str | dict[str, object]]
        type AttributeValues = dict[
            str, str | list[str] | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type EntryValidation = dict[str, bool | str | dict[str, object]]

    # =========================================================================
    # LDAP OPERATIONS TYPES - Complex LDAP operation types
    # =========================================================================

    class LdapOperations:
        """LDAP operations complex types."""

        type OperationConfiguration = dict[
            str, str | bool | int | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type SearchOperations = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type ModifyOperations = dict[str, str | list[str] | dict[str, object]]
        type AddOperations = dict[str, dict[str, FlextTargetLdapTypes.Core.JsonValue]]
        type DeleteOperations = dict[str, str | bool | dict[str, object]]
        type BindOperations = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]

    # =========================================================================
    # LDAP SECURITY TYPES - Complex LDAP security and authentication types
    # =========================================================================

    class LdapSecurity:
        """LDAP security and authentication complex types."""

        type SecurityConfiguration = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type AuthenticationMethods = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type TlsConfiguration = dict[str, str | bool | dict[str, object]]
        type CredentialManagement = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type AccessControl = dict[
            str, bool | str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type CertificateHandling = dict[str, str | dict[str, object]]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type FieldMapping = dict[str, str | list[str] | dict[str, object]]
        type DataValidation = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type TypeConversion = dict[str, bool | str | dict[str, object]]
        type FilteringRules = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type TransformationResult = dict[
            str, dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]

    # =========================================================================
    # STREAM PROCESSING TYPES - Complex stream handling types
    # =========================================================================

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[
            str, str | bool | int | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type StreamMetadata = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type StreamRecord = dict[
            str, FlextTargetLdapTypes.Core.JsonValue | dict[str, object]
        ]
        type StreamState = dict[
            str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type StreamBookmark = dict[str, str | int | dict[str, object]]
        type StreamSchema = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue] | bool
        ]

    # =========================================================================
    # ERROR HANDLING TYPES - Complex error management types
    # =========================================================================

    class ErrorHandling:
        """Error handling complex types."""

        type ErrorConfiguration = dict[
            str, bool | str | int | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type ErrorRecovery = dict[str, str | bool | dict[str, object]]
        type ErrorReporting = dict[
            str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type ErrorClassification = dict[str, str | int | dict[str, object]]
        type ErrorMetrics = dict[
            str, int | float | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type ErrorTracking = list[
            dict[str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]]
        ]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Extending FlextTypes.Core for Target LDAP domain
    # =========================================================================

    class Core(FlextTypes.Core):
        """Core Target LDAP-specific type aliases extending FlextTargetLdapTypes.Core.

        Provides standardized type aliases for frequent Target LDAP patterns while
        inheriting all core types from FlextTargetLdapTypes.Core. Reduces generic dict/list
        usage throughout the Target LDAP codebase.
        """

        # Core aliases for compatibility with FlextTypes.Core
        type Dict = dict[str, object]
        type List = list[object]
        type StringList = list[str]
        type ConfigValue = (
            str | int | bool | float | list[object] | dict[str, object] | None
        )
        type JsonValue = (
            str | int | bool | float | list[object] | dict[str, object] | None
        )

        # Target LDAP configuration and data types
        type TargetLdapConfigDict = dict[str, object]
        type LdapTargetConfigDict = dict[str, object]
        type SingerTargetDict = dict[str, object]
        type DirectoryConfigDict = dict[str, object]
        type ConnectionConfigDict = dict[str, object]
        type SecurityConfigDict = dict[str, object]
        type OperationConfigDict = dict[str, object]
        type LoadingConfigDict = dict[str, object]

        # LDAP target operation types
        type LdapEntryDict = dict[str, object]
        type LdapAttributeDict = dict[str, object]
        type LdapOperationDict = dict[str, object]
        type LdapResultDict = dict[str, object]
        type DirectoryEntryDict = dict[str, object]
        type TargetRecordDict = dict[str, object]
        type SingerRecordDict = dict[str, object]
        type SingerStateDict = dict[str, object]

        # Singer protocol types for target LDAP
        type SingerMessageDict = dict[str, object]
        type SingerSchemaDict = dict[str, object]
        type SingerCatalogDict = dict[str, object]
        type StreamConfigDict = dict[str, object]
        type StreamSchemaDict = dict[str, object]
        type StreamRecordDict = dict[str, object]
        type StreamStateDict = dict[str, object]

        # LDAP target processing types
        type TransformationDict = dict[str, object]
        type ValidationDict = dict[str, object]
        type MappingDict = dict[str, object]
        type FilteringDict = dict[str, object]
        type LoadingResultDict = dict[str, object]
        type ProcessingResultDict = dict[str, object]
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
    # SINGER TARGET LDAP PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Singer Target LDAP-specific project types extending FlextTypes.Project.

        Adds Singer target LDAP-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Singer target LDAP domain owns LDAP loading and Singer protocol-specific types.
        """

        # Singer target LDAP-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
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
        type SingerTargetLdapProjectConfig = dict[
            str, FlextTargetLdapTypes.Core.ConfigValue | object
        ]
        type LdapLoaderConfig = dict[str, str | int | bool | list[str]]
        type SingerProtocolConfig = dict[str, bool | str | dict[str, object]]
        type TargetLdapPipelineConfig = dict[
            str, FlextTargetLdapTypes.Core.ConfigValue | object
        ]


# =============================================================================
# PUBLIC API EXPORTS - Singer LDAP target TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextTargetLdapTypes",
]
