"""FLEXT Target LDAP Types - Domain-specific Singer LDAP target type definitions.

This module provides Singer LDAP target-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextCore

# =============================================================================
# TARGET LDAP-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Singer LDAP target operations
# =============================================================================


# Singer LDAP target domain TypeVars
class FlextTargetLdapTypes(FlextCore.Types):
    """Singer LDAP target-specific type definitions extending FlextCore.Types.

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
        type SchemaDefinition = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type DirectoryStructure = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type OperationalAttributes = dict[str, str | bool | FlextCore.Types.Dict]

    # =========================================================================
    # LDAP ENTRY TYPES - Complex LDAP entry and attribute types
    # =========================================================================

    class LdapEntry:
        """LDAP entry and attribute complex types."""

        type EntryConfiguration = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type AttributeMapping = dict[
            str,
            str
            | FlextCore.Types.StringList
            | dict[str, FlextTargetLdapTypes.Core.JsonValue],
        ]
        type ObjectClassDefinition = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type DistinguishedName = dict[str, str | FlextCore.Types.Dict]
        type AttributeValues = dict[
            str,
            str
            | FlextCore.Types.StringList
            | dict[str, FlextTargetLdapTypes.Core.JsonValue],
        ]
        type EntryValidation = dict[str, bool | str | FlextCore.Types.Dict]

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
        type ModifyOperations = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type AddOperations = dict[str, dict[str, FlextTargetLdapTypes.Core.JsonValue]]
        type DeleteOperations = dict[str, str | bool | FlextCore.Types.Dict]
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
        type TlsConfiguration = dict[str, str | bool | FlextCore.Types.Dict]
        type CredentialManagement = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type AccessControl = dict[
            str, bool | str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type CertificateHandling = dict[str, str | FlextCore.Types.Dict]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[
            str, str | bool | dict[str, FlextTargetLdapTypes.Core.ConfigValue]
        ]
        type FieldMapping = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type DataValidation = dict[
            str, str | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type TypeConversion = dict[str, bool | str | FlextCore.Types.Dict]
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
            str, FlextTargetLdapTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type StreamState = dict[
            str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type StreamBookmark = dict[str, str | int | FlextCore.Types.Dict]
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
        type ErrorRecovery = dict[str, str | bool | FlextCore.Types.Dict]
        type ErrorReporting = dict[
            str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type ErrorClassification = dict[str, str | int | FlextCore.Types.Dict]
        type ErrorMetrics = dict[
            str, int | float | dict[str, FlextTargetLdapTypes.Core.JsonValue]
        ]
        type ErrorTracking = list[
            dict[str, str | int | dict[str, FlextTargetLdapTypes.Core.JsonValue]]
        ]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Extending FlextCore.Types for Target LDAP domain
    # =========================================================================

    class Core(FlextCore.Types):
        """Core Target LDAP-specific type aliases extending FlextTargetLdapTypes.Core.

        Provides standardized type aliases for frequent Target LDAP patterns while
        inheriting all core types from FlextTargetLdapTypes.Core. Reduces generic dict/list
        usage throughout the Target LDAP codebase.
        """

        # Core aliases for compatibility with FlextCore.Types
        type Dict = FlextCore.Types.Dict
        type List = FlextCore.Types.List
        type StringList = FlextCore.Types.StringList
        type ConfigValue = (
            str
            | int
            | bool
            | float
            | FlextCore.Types.List
            | FlextCore.Types.Dict
            | None
        )
        type JsonValue = (
            str
            | int
            | bool
            | float
            | FlextCore.Types.List
            | FlextCore.Types.Dict
            | None
        )

        # Target LDAP configuration and data types
        type TargetLdapConfigDict = FlextCore.Types.Dict
        type LdapTargetConfigDict = FlextCore.Types.Dict
        type SingerTargetDict = FlextCore.Types.Dict
        type DirectoryConfigDict = FlextCore.Types.Dict
        type ConnectionConfigDict = FlextCore.Types.Dict
        type SecurityConfigDict = FlextCore.Types.Dict
        type OperationConfigDict = FlextCore.Types.Dict
        type LoadingConfigDict = FlextCore.Types.Dict

        # LDAP target operation types
        type LdapEntryDict = FlextCore.Types.Dict
        type LdapAttributeDict = FlextCore.Types.Dict
        type LdapOperationDict = FlextCore.Types.Dict
        type LdapResultDict = FlextCore.Types.Dict
        type DirectoryEntryDict = FlextCore.Types.Dict
        type TargetRecordDict = FlextCore.Types.Dict
        type SingerRecordDict = FlextCore.Types.Dict
        type SingerStateDict = FlextCore.Types.Dict

        # Singer protocol types for target LDAP
        type SingerMessageDict = FlextCore.Types.Dict
        type SingerSchemaDict = FlextCore.Types.Dict
        type SingerCatalogDict = FlextCore.Types.Dict
        type StreamConfigDict = FlextCore.Types.Dict
        type StreamSchemaDict = FlextCore.Types.Dict
        type StreamRecordDict = FlextCore.Types.Dict
        type StreamStateDict = FlextCore.Types.Dict

        # LDAP target processing types
        type TransformationDict = FlextCore.Types.Dict
        type ValidationDict = FlextCore.Types.Dict
        type MappingDict = FlextCore.Types.Dict
        type FilteringDict = FlextCore.Types.Dict
        type LoadingResultDict = FlextCore.Types.Dict
        type ProcessingResultDict = FlextCore.Types.Dict
        type ErrorResultDict = FlextCore.Types.Dict
        type MetricsDict = FlextCore.Types.FloatDict

        # Target LDAP lists
        type LdapEntryList = list[FlextCore.Types.Dict]
        type SingerRecordList = list[FlextCore.Types.Dict]
        type StreamNameList = FlextCore.Types.StringList
        type AttributeNameList = FlextCore.Types.StringList
        type OperationList = FlextCore.Types.StringList
        type ErrorList = FlextCore.Types.StringList
        type MetricsList = FlextCore.Types.FloatList
        type ResultList = list[FlextCore.Types.Dict]

    # =========================================================================
    # SINGER TARGET LDAP PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """Singer Target LDAP-specific project types extending FlextCore.Types.Project.

        Adds Singer target LDAP-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        Singer target LDAP domain owns LDAP loading and Singer protocol-specific types.
        """

        # Singer target LDAP-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
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
        type LdapLoaderConfig = dict[str, str | int | bool | FlextCore.Types.StringList]
        type SingerProtocolConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type TargetLdapPipelineConfig = dict[
            str, FlextTargetLdapTypes.Core.ConfigValue | object
        ]


# =============================================================================
# PUBLIC API EXPORTS - Singer LDAP target TypeVars and types
# =============================================================================

__all__: FlextCore.Types.StringList = [
    "FlextTargetLdapTypes",
]
