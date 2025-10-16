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
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type StreamConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.JsonValue]
        ]
        type MessageProcessing = dict[str, str | list[dict[str, FlextTypes.JsonValue]]]
        type RecordHandling = dict[str, str | dict[str, FlextTypes.JsonValue] | bool]
        type StateManagement = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type BatchProcessing = dict[str, str | int | dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # LDAP DIRECTORY TYPES - Complex LDAP directory service types
    # =========================================================================

    class LdapDirectory:
        """LDAP directory service complex types."""

        type DirectoryConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type ConnectionManagement = dict[
            str, str | int | dict[str, FlextTypes.JsonValue]
        ]
        type AuthenticationSettings = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type SchemaDefinition = dict[str, str | FlextTypes.StringList | FlextTypes.Dict]
        type DirectoryStructure = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type OperationalAttributes = dict[str, str | bool | FlextTypes.Dict]

    # =========================================================================
    # LDAP ENTRY TYPES - Complex LDAP entry and attribute types
    # =========================================================================

    class LdapEntry:
        """LDAP entry and attribute complex types."""

        type EntryConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type AttributeMapping = dict[
            str,
            str | FlextTypes.StringList | dict[str, FlextTypes.JsonValue],
        ]
        type ObjectClassDefinition = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type DistinguishedName = dict[str, str | FlextTypes.Dict]
        type AttributeValues = dict[
            str,
            str | FlextTypes.StringList | dict[str, FlextTypes.JsonValue],
        ]
        type EntryValidation = dict[str, bool | str | FlextTypes.Dict]

    # =========================================================================
    # LDAP OPERATIONS TYPES - Complex LDAP operation types
    # =========================================================================

    class LdapOperations:
        """LDAP operations complex types."""

        type OperationConfiguration = dict[
            str, str | bool | int | dict[str, FlextTypes.ConfigValue]
        ]
        type SearchOperations = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type ModifyOperations = dict[str, str | FlextTypes.StringList | FlextTypes.Dict]
        type AddOperations = dict[str, dict[str, FlextTypes.JsonValue]]
        type DeleteOperations = dict[str, str | bool | FlextTypes.Dict]
        type BindOperations = dict[str, str | dict[str, FlextTypes.ConfigValue]]

    # =========================================================================
    # LDAP SECURITY TYPES - Complex LDAP security and authentication types
    # =========================================================================

    class LdapSecurity:
        """LDAP security and authentication complex types."""

        type SecurityConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type AuthenticationMethods = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type TlsConfiguration = dict[str, str | bool | FlextTypes.Dict]
        type CredentialManagement = dict[str, str | dict[str, FlextTypes.ConfigValue]]
        type AccessControl = dict[str, bool | str | dict[str, FlextTypes.JsonValue]]
        type CertificateHandling = dict[str, str | FlextTypes.Dict]

    # =========================================================================
    # DATA TRANSFORMATION TYPES - Complex data transformation types
    # =========================================================================

    class DataTransformation:
        """Data transformation complex types."""

        type TransformationConfiguration = dict[
            str, str | bool | dict[str, FlextTypes.ConfigValue]
        ]
        type FieldMapping = dict[str, str | FlextTypes.StringList | FlextTypes.Dict]
        type DataValidation = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type TypeConversion = dict[str, bool | str | FlextTypes.Dict]
        type FilteringRules = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type TransformationResult = dict[str, dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # STREAM PROCESSING TYPES - Complex stream handling types
    # =========================================================================

    class StreamProcessing:
        """Stream processing complex types."""

        type StreamConfiguration = dict[
            str, str | bool | int | dict[str, FlextTypes.ConfigValue]
        ]
        type StreamMetadata = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type StreamRecord = dict[str, FlextTypes.JsonValue | FlextTypes.Dict]
        type StreamState = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type StreamBookmark = dict[str, str | int | FlextTypes.Dict]
        type StreamSchema = dict[str, str | dict[str, FlextTypes.JsonValue] | bool]

    # =========================================================================
    # ERROR HANDLING TYPES - Complex error management types
    # =========================================================================

    class ErrorHandling(FlextTypes.ErrorHandling):
        """Error handling complex types extending FlextTypes.ErrorHandling."""

        type ErrorConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.ConfigValue]
        ]
        type ErrorRecovery = dict[str, str | bool | FlextTypes.Dict]
        type ErrorReporting = dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        type ErrorClassification = dict[str, str | int | FlextTypes.Dict]
        type ErrorMetrics = dict[str, int | float | dict[str, FlextTypes.JsonValue]]
        type ErrorTracking = list[
            dict[str, str | int | dict[str, FlextTypes.JsonValue]]
        ]

    # =========================================================================
    # CORE COMMONLY USED TYPES - Extending FlextTypes for Target LDAP domain
    # =========================================================================

    class Core(FlextTypes.Core):
        """Core Target LDAP-specific type aliases extending FlextTypes.Core.

        Provides standardized type aliases for frequent Target LDAP patterns while
        inheriting all core types from FlextTypes.Core. Reduces generic dict/list
        usage throughout the Target LDAP codebase.
        """

        # REMOVED: Simple type aliases like Dict = FlextTypes.Dict
        # Use FlextTypes.Dict directly instead of creating aliases
        type ErrorResultDict = FlextTypes.Dict
        type MetricsDict = FlextTypes.FloatDict

        # Target LDAP lists
        type LdapEntryList = list[FlextTypes.Dict]
        type SingerRecordList = list[FlextTypes.Dict]
        type StreamNameList = FlextTypes.StringList
        type AttributeNameList = FlextTypes.StringList
        type OperationList = FlextTypes.StringList
        type ErrorList = FlextTypes.StringList
        type MetricsList = FlextTypes.FloatList
        type ResultList = list[FlextTypes.Dict]

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
        type TargetLdapProjectType = Literal[
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
        type SingerTargetLdapProjectConfig = dict[str, FlextTypes.ConfigValue | object]
        type LdapLoaderConfig = dict[str, str | int | bool | FlextTypes.StringList]
        type SingerProtocolConfig = dict[str, bool | str | FlextTypes.Dict]
        type TargetLdapPipelineConfig = dict[str, FlextTypes.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Singer LDAP target TypeVars and types
# =============================================================================

__all__: FlextTypes.StringList = [
    "FlextTargetLdapTypes",
]
