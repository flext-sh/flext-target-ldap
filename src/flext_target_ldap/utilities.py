"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import override

from flext_core import r, t
from flext_ldap import FlextLdapModels, FlextLdapUtilities
from flext_meltano import FlextMeltanoUtilities
from pydantic import TypeAdapter

from flext_target_ldap.constants import c


class FlextTargetLdapUtilities(FlextMeltanoUtilities, FlextLdapUtilities):
    """Single unified utilities class for Singer target LDAP operations.

    Follows FLEXT unified class pattern with nested helper classes for
    domain-specific Singer target functionality with LDAP directory operations.

    Constants are accessed via constants module:
        c.TargetLdap.Connection.DEFAULT_PORT (389)
        c.TargetLdap.Connection.Ldaps.DEFAULT_PORT (636)
        c.TargetLdap.Processing.DEFAULT_BATCH_SIZE
    """

    @override
    def __init__(self) -> None:
        """Initialize LDAP target utilities."""
        super().__init__()

    class TargetLdap:
        """Singer protocol utilities for target operations."""

        @staticmethod
        def parse_singer_message(
            line: str,
        ) -> r[Mapping[str, object]]:
            """Parse Singer message from input line.

            Args:
            line: JSON line from Singer tap

            Returns:
            r[dict[str, object]]: Parsed message or error

            """
            if not line or not line.strip():
                return r[t.ConfigurationMapping].fail("Empty input line")
            try:
                message = json.loads(line.strip())
                if not u.is_dict_like(message):
                    return r[Mapping[str, object]].fail("Message must be a JSON object")
                if "type" not in message:
                    return r[Mapping[str, object]].fail(
                        "Message missing required 'type' field"
                    )
                validated: Mapping[str, object] = TypeAdapter(
                    Mapping[str, object]
                ).validate_python(message)
                return r[Mapping[str, object]].ok(validated)
            except json.JSONDecodeError as e:
                return r[Mapping[str, object]].fail(f"Invalid JSON: {e}")

        @staticmethod
        def validate_record_message(
            message: Mapping[str, object],
        ) -> r[Mapping[str, object]]:
            """Validate Singer RECORD message structure.

            Args:
            message: Singer message to validate

            Returns:
            r[dict[str, object]]: Validated record or error

            """
            if message.get("type") != "RECORD":
                return r[t.ConfigurationMapping].fail("Message type must be RECORD")
            required_fields = ["stream", "record"]
            for field in required_fields:
                if field not in message:
                    return r[t.ConfigurationMapping].fail(
                        f"RECORD message missing '{field}' field"
                    )
            record = message["record"]
            if not u.is_dict_like(record):
                return r[t.ConfigurationMapping].fail(
                    "Record data must be a dictionary"
                )
            return r[t.ConfigurationMapping].ok(message)

        @staticmethod
        def validate_schema_message(
            message: Mapping[str, object],
        ) -> r[Mapping[str, object]]:
            """Validate Singer SCHEMA message structure.

            Args:
            message: Singer message to validate

            Returns:
            r[dict[str, object]]: Validated schema or error

            """
            if message.get("type") != "SCHEMA":
                return r[t.ConfigurationMapping].fail("Message type must be SCHEMA")
            required_fields = ["stream", "schema"]
            for field in required_fields:
                if field not in message:
                    return r[t.ConfigurationMapping].fail(
                        f"SCHEMA message missing '{field}' field"
                    )
            schema = message["schema"]
            if not u.is_dict_like(schema):
                return r[t.ConfigurationMapping].fail(
                    "Schema data must be a dictionary"
                )
            return r[t.ConfigurationMapping].ok(message)

        @staticmethod
        def write_state_message(_state: Mapping[str, object]) -> None:
            """Write Singer state message to stdout.

            Args:
            state: State data to write

            """

    class LdapDataProcessing:
        """LDAP-specific data processing utilities."""

        @staticmethod
        def build_ldap_dn(
            record: Mapping[str, object], dn_template: str, base_dn: str
        ) -> r[str]:
            """Build LDAP Distinguished Name from record data.

            Args:
            record: Record data
            dn_template: DN template with placeholders
            base_dn: Base DN for the directory

            Returns:
            r[str]: Built DN or error

            """
            if not record or not dn_template or (not base_dn):
                return r[str].fail("Record, DN template, and base DN are required")
            try:
                dn_rdn = dn_template
                for key, value in record.items():
                    placeholder = f"{{{key}}}"
                    if placeholder in dn_rdn:
                        if value is None:
                            return r[str].fail(f"Cannot build DN: {key} is null")
                        dn_rdn = dn_rdn.replace(placeholder, str(value))
                if "{" in dn_rdn and "}" in dn_rdn:
                    return r[str].fail(f"Unresolved placeholders in DN: {dn_rdn}")
                full_dn = f"{dn_rdn},{base_dn}"
                if not FlextTargetLdapUtilities.LdapDataProcessing.split(full_dn):
                    return r[str].fail(f"Invalid DN format: {full_dn}")
                return r[str].ok(full_dn)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[str].fail(f"Error building DN: {e}")

        @staticmethod
        def convert_record_to_ldap_attributes(
            record: Mapping[str, object],
            attribute_mapping: Mapping[str, str] | None = None,
        ) -> r[Mapping[str, list[bytes]]]:
            """Convert Singer record to LDAP attributes format.

            Args:
            record: Singer record data
            attribute_mapping: Optional mapping from record keys to LDAP attributes

            Returns:
            r[dict[str, list[bytes]]]: LDAP attributes or error

            """
            if not record:
                return r[Mapping[str, list[bytes]]].fail("Record cannot be empty")
            try:
                ldap_attrs: dict[str, list[bytes]] = {}
                mapping = attribute_mapping or {}
                for key, value in record.items():
                    if value is None:
                        continue
                    ldap_attr = mapping.get(key, key)
                    if u.Guards.is_list(value):
                        ldap_values = [
                            str(item).encode("utf-8")
                            for item in value
                            if item is not None
                        ]
                        if ldap_values:
                            ldap_attrs[ldap_attr] = ldap_values
                    else:
                        ldap_attrs[ldap_attr] = [str(value).encode("utf-8")]
                return r[Mapping[str, list[bytes]]].ok(ldap_attrs)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                return r[Mapping[str, list[bytes]]].fail(
                    f"Error converting to LDAP attributes: {e}"
                )

        @staticmethod
        def extract_object_classes(
            record: Mapping[str, object],
            default_object_classes: list[str] | None = None,
        ) -> list[str]:
            """Extract object classes for LDAP entry.

            Args:
            record: Singer record data
            default_object_classes: Default object classes if not in record

            Returns:
            list[str]: List of object classes

            """
            object_classes = record.get("objectClass") or record.get("objectclass")
            if object_classes:
                if u.Guards.is_list(object_classes):
                    return [str(oc) for oc in object_classes if oc]
                return [str(object_classes)]
            if default_object_classes:
                return default_object_classes
            return ["top"]

        @staticmethod
        def sanitize_ldap_value(value: str) -> str:
            """Sanitize value for LDAP attribute insertion.

            Args:
            value: Value to sanitize

            Returns:
            str: Sanitized value

            """
            if not value:
                return ""
            ldap_escapes = {
                "\\": "\\5c",
                "*": "\\2a",
                "(": "\\28",
                ")": "\\29",
                "\x00": "\\00",
            }
            sanitized = value
            for char, escape in ldap_escapes.items():
                sanitized = sanitized.replace(char, escape)
            return sanitized.strip()

        @staticmethod
        def split(dn: str) -> bool:
            """Validate LDAP Distinguished Name format.

            Args:
            dn: Distinguished Name to validate

            Returns:
            bool: True if valid, False otherwise

            """
            if not dn:
                return False
            dn_pattern = "^[a-zA-Z][\\w\\-]*\\s*=\\s*[^,]+(?:\\s*,\\s*[a-zA-Z][\\w\\-]*\\s*=\\s*[^,]+)*$"
            return bool(re.match(dn_pattern, dn.strip()))

    class StreamUtilities:
        """Stream processing utilities for Singer targets."""

        @staticmethod
        def calculate_ldap_batch_size(
            record_count: int, target_batches: int = 10
        ) -> int:
            """Calculate optimal batch size for LDAP operations.

            Args:
            record_count: Total number of records
            target_batches: Target number of batches

            Returns:
            int: Optimal batch size

            """
            if record_count <= 0:
                return c.TargetLdap.Processing.DEFAULT_BATCH_SIZE
            calculated_size = max(1, record_count // target_batches)
            return min(calculated_size, c.TargetLdap.Processing.DEFAULT_BATCH_SIZE)

        @staticmethod
        def generate_ldap_stream_metadata(
            stream_name: str, record_count: int, processing_time: float
        ) -> Mapping[str, object]:
            """Generate metadata for LDAP stream processing.

            Args:
            stream_name: Name of the stream
            record_count: Number of records processed
            processing_time: Time taken for processing

            Returns:
            dict[str, object]: Stream metadata

            """
            return {
                "stream_name": stream_name,
                "records_processed": record_count,
                "processing_time_seconds": processing_time,
                "records_per_second": record_count / max(processing_time, 0.001),
                "processing_timestamp": datetime.now(UTC).isoformat(),
                "target_type": "ldap",
            }

        @staticmethod
        def validate_stream_compatibility(
            stream_name: str, schema: Mapping[str, object]
        ) -> r[bool]:
            """Validate stream compatibility with LDAP operations.

            Args:
            stream_name: Name of the stream
            schema: Stream schema

            Returns:
            r[bool]: Validation result

            """
            if not stream_name or not schema:
                return r[bool].fail("Stream name and schema are required")
            raw_props = schema.get("properties", {})
            properties: dict[str, object] = {}
            if isinstance(raw_props, Mapping):
                for k, v in raw_props.items():
                    properties[str(k)] = v
            if not properties:
                return r[bool].fail("Schema must have properties")
            has_dn_field = "dn" in properties
            has_id_fields = any(
                key in properties for key in ["id", "uid", "cn", "username", "email"]
            )
            if not has_dn_field and (not has_id_fields):
                return r[bool].fail(
                    "Schema must have either 'dn' field or identifier fields (id, uid, cn, username, email)"
                )
            return r[bool].ok(value=True)

    class ConfigValidation:
        """Configuration validation utilities."""

        @staticmethod
        def validate_ldap_connection_config(
            config: Mapping[str, object],
        ) -> r[Mapping[str, object]]:
            """Validate LDAP connection configuration.

            Args:
            config: Configuration dictionary

            Returns:
            r[dict[str, object]]: Validated config or error

            """
            required_fields = ["host", "bind_dn", "bind_password", "base_dn"]
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                return r[t.ConfigurationMapping].fail(
                    f"Missing required LDAP connection fields: {', '.join(missing_fields)}"
                )
            host = config["host"]
            match host:
                case str() if host.strip():
                    pass
                case _:
                    return r[t.ConfigurationMapping].fail(
                        "Host must be a non-empty string"
                    )
            bind_dn = config["bind_dn"]
            match bind_dn:
                case str():
                    pass
                case _:
                    return r[t.ConfigurationMapping].fail("Bind DN must be a string")
            if not FlextTargetLdapUtilities.LdapDataProcessing.split(bind_dn):
                return r[t.ConfigurationMapping].fail(
                    f"Invalid bind DN format: {bind_dn}"
                )
            base_dn = config["base_dn"]
            match base_dn:
                case str():
                    pass
                case _:
                    return r[t.ConfigurationMapping].fail("Base DN must be a string")
            if not FlextTargetLdapUtilities.LdapDataProcessing.split(base_dn):
                return r[t.ConfigurationMapping].fail(
                    f"Invalid base DN format: {base_dn}"
                )
            base_dn = config["base_dn"]
            match base_dn:
                case str() if FlextTargetLdapUtilities.LdapDataProcessing.split(
                    base_dn
                ):
                    pass
                case _:
                    return r[t.ConfigurationMapping].fail(
                        f"Invalid base DN format: {base_dn}"
                    )
            if "port" in config:
                port = config["port"]
                match port:
                    case bool():
                        return r[t.ConfigurationMapping].fail(
                            "Port must be a valid integer between 1 and 65535"
                        )
                    case int() if 0 < port <= c.TargetLdap.Connection.MAX_PORT_NUMBER:
                        pass
                    case _:
                        return r[t.ConfigurationMapping].fail(
                            "Port must be a valid integer between 1 and 65535"
                        )
            use_ssl = config.get("use_ssl", False)
            use_tls = config.get("use_tls", False)
            if use_ssl and use_tls:
                return r[t.ConfigurationMapping].fail(
                    "Cannot use both SSL and TLS simultaneously"
                )
            return r[t.ConfigurationMapping].ok(config)

        @staticmethod
        def validate_target_config(
            config: Mapping[str, object],
        ) -> r[Mapping[str, object]]:
            """Validate target configuration.

            Args:
            config: Target configuration

            Returns:
            r[dict[str, object]]: Validated config or error

            """
            ldap_result = FlextTargetLdapUtilities.ConfigValidation.validate_ldap_connection_config(
                config
            )
            if ldap_result.is_failure:
                return ldap_result
            operation_mode = config.get("operation_mode", "upsert")
            valid_modes = ["insert", "update", "upsert", "delete"]
            if operation_mode not in valid_modes:
                return r[t.ConfigurationMapping].fail(
                    f"Invalid operation mode: {operation_mode}. Valid modes: {', '.join(valid_modes)}"
                )
            if "dn_template" in config:
                dn_template = config["dn_template"]
                match dn_template:
                    case str() if dn_template.strip():
                        pass
                    case _:
                        return r[t.ConfigurationMapping].fail(
                            "DN template must be a non-empty string"
                        )
            batch_size = config.get(
                "batch_size", c.TargetLdap.Processing.DEFAULT_BATCH_SIZE
            )
            match batch_size:
                case bool():
                    return r[t.ConfigurationMapping].fail(
                        "Batch size must be a positive integer"
                    )
                case int() if batch_size > 0:
                    pass
                case _:
                    return r[t.ConfigurationMapping].fail(
                        "Batch size must be a positive integer"
                    )
            return r[t.ConfigurationMapping].ok(config)

    class StateManagement:
        """State management utilities for target operations."""

        @staticmethod
        def create_processing_state(
            stream_name: str,
            records_processed: int,
            last_processed_record: Mapping[str, object] | None = None,
        ) -> Mapping[str, object]:
            """Create processing state for target stream.

            Args:
            stream_name: Name of the stream
            records_processed: Number of records processed
            last_processed_record: Last processed record for checkpointing

            Returns:
            dict[str, object]: Processing state

            """
            state: dict[str, object] = {
                "stream_name": stream_name,
                "records_processed": records_processed,
                "last_updated": datetime.now(UTC).isoformat(),
                "target_type": "ldap",
            }
            if last_processed_record:
                checkpoint_data = {
                    "id": last_processed_record.get("id"),
                    "dn": last_processed_record.get("dn"),
                    "timestamp": last_processed_record.get("_timestamp"),
                }
                state["checkpoint"] = {
                    k: v for k, v in checkpoint_data.items() if v is not None
                }
            return state

        @staticmethod
        def get_target_state(
            state: Mapping[str, object], stream_name: str
        ) -> Mapping[str, object]:
            """Get state for a specific target stream.

            Args:
            state: Complete state dictionary
            stream_name: Name of the stream

            Returns:
            dict[str, object]: Stream state

            """
            bookmarks = state.get("bookmarks")
            if not isinstance(bookmarks, Mapping):
                return {}
            bookmarks_map: Mapping[str, object] = {
                str(k): v for k, v in bookmarks.items()
            }
            stream_state_data = bookmarks_map.get(stream_name)
            if isinstance(stream_state_data, Mapping):
                return {str(k): v for k, v in stream_state_data.items()}
            return {}

        @staticmethod
        def set_target_state(
            state: Mapping[str, object],
            stream_name: str,
            stream_state: Mapping[str, object],
        ) -> Mapping[str, object]:
            """Set state for a specific target stream.

            Args:
            state: Complete state dictionary
            stream_name: Name of the stream
            stream_state: State data for the stream

            Returns:
            dict[str, object]: Updated state

            """
            state_dict = dict(state)
            bookmarks = state_dict.get("bookmarks")
            bookmarks_dict: dict[str, object] = {}
            if isinstance(bookmarks, Mapping):
                for k, v in bookmarks.items():
                    bookmarks_dict[str(k)] = v
            bookmarks_dict[stream_name] = dict(stream_state)
            state_dict["bookmarks"] = bookmarks_dict
            return state_dict

        @staticmethod
        def update_processing_progress(
            state: Mapping[str, object], stream_name: str, records_count: int
        ) -> Mapping[str, object]:
            """Update processing progress in state.

            Args:
            state: Current state
            stream_name: Name of the stream
            records_count: Number of records processed in this batch

            Returns:
            dict[str, object]: Updated state

            """
            stream_state = FlextTargetLdapUtilities.StateManagement.get_target_state(
                state, stream_name
            )
            current_count_val = stream_state.get("records_processed", 0)
            match current_count_val:
                case bool():
                    current_count = 0
                case int():
                    current_count = current_count_val
                case _:
                    current_count = 0
            new_count = current_count + records_count
            batch_count_val = stream_state.get("batch_count", 0)
            match batch_count_val:
                case bool():
                    batch_count = 0
                case int():
                    batch_count = batch_count_val
                case _:
                    batch_count = 0
            updated_stream_state: dict[str, object] = {
                **stream_state,
                "records_processed": new_count,
                "last_updated": datetime.now(UTC).isoformat(),
                "batch_count": batch_count + 1,
            }
            return FlextTargetLdapUtilities.StateManagement.set_target_state(
                state, stream_name, updated_stream_state
            )

    @classmethod
    def build_ldap_dn(
        cls, record: Mapping[str, object], dn_template: str, base_dn: str
    ) -> r[str]:
        """Proxy method for LdapDataProcessing.build_ldap_dn()."""
        return cls.LdapDataProcessing.build_ldap_dn(record, dn_template, base_dn)

    @classmethod
    def convert_record_to_ldap_attributes(
        cls,
        record: Mapping[str, object],
        attribute_mapping: Mapping[str, str] | None = None,
    ) -> r[Mapping[str, list[bytes]]]:
        """Proxy method for LdapDataProcessing.convert_record_to_ldap_attributes()."""
        return cls.LdapDataProcessing.convert_record_to_ldap_attributes(
            record, attribute_mapping
        )

    @classmethod
    def create_processing_state(
        cls,
        stream_name: str,
        records_processed: int,
        last_processed_record: Mapping[str, object] | None = None,
    ) -> Mapping[str, object]:
        """Proxy method for StateManagement.create_processing_state()."""
        return cls.StateManagement.create_processing_state(
            stream_name, records_processed, last_processed_record
        )

    @classmethod
    def get_target_state(
        cls, state: Mapping[str, object], stream_name: str
    ) -> Mapping[str, object]:
        """Proxy method for StateManagement.get_target_state()."""
        return cls.StateManagement.get_target_state(state, stream_name)

    @classmethod
    def parse_singer_message(cls, line: str) -> r[Mapping[str, object]]:
        """Proxy method for TargetLdap.parse_singer_message()."""
        return cls.TargetLdap.parse_singer_message(line)

    @classmethod
    def validate_ldap_connection_config(
        cls, config: Mapping[str, object]
    ) -> r[Mapping[str, object]]:
        """Proxy method for ConfigValidation.validate_ldap_connection_config()."""
        return cls.ConfigValidation.validate_ldap_connection_config(config)

    class TypeConversion:
        """Type conversion utilities for configuration parsing."""

        @staticmethod
        def build_connection_config(
            config: Mapping[str, object],
        ) -> FlextLdapModels.Ldap.ConnectionConfig:
            """Build LDAP connection configuration from config dict.

            Args:
                config: Raw configuration dictionary from any source

            Returns:
                FlextLdapModels.Ldap.ConnectionConfig: Validated connection config

            """
            server = FlextTargetLdapUtilities.TypeConversion.to_str(
                config.get("host", "localhost"), "localhost"
            )
            port = FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("port", c.TargetLdap.Connection.DEFAULT_PORT),
                c.TargetLdap.Connection.DEFAULT_PORT,
            )
            use_ssl = FlextTargetLdapUtilities.TypeConversion.to_bool(
                config.get("use_ssl", False), default=False
            )
            bind_dn = FlextTargetLdapUtilities.TypeConversion.to_str(
                config.get("bind_dn", ""), ""
            )
            bind_password = FlextTargetLdapUtilities.TypeConversion.to_str(
                config.get("password", ""), ""
            )
            timeout = FlextTargetLdapUtilities.TypeConversion.to_int(
                config.get("timeout", c.Network.DEFAULT_TIMEOUT),
                c.Network.DEFAULT_TIMEOUT,
            )
            return FlextLdapModels.Ldap.ConnectionConfig(
                host=server,
                port=port,
                use_ssl=use_ssl,
                bind_dn=bind_dn,
                bind_password=bind_password,
                timeout=timeout,
            )

        @staticmethod
        def extract_attribute_mapping(
            config: Mapping[str, object],
        ) -> Mapping[str, str]:
            """Extract attribute mapping from configuration dict.

            Business Rule: Attribute Mapping Extraction
            ==========================================
            LDAP attribute mappings define how Singer record fields map to LDAP
            attributes. This method safely extracts and validates attribute mappings
            from configuration, ensuring type safety.

            Validation Rules:
            - Must be a dictionary
            - Keys and values converted to strings
            - Invalid mappings are silently ignored (empty dict returned)

            Args:
                config: Configuration dictionary containing attribute_mapping

            Returns:
                dict[str, str]: Validated attribute mapping or empty dict

            """
            raw_attr_map = config.get("attribute_mapping")
            if isinstance(raw_attr_map, Mapping):
                extracted_mapping: dict[str, str] = {}
                for k, v in raw_attr_map.items():
                    extracted_mapping[str(k)] = str(v)
                return extracted_mapping
            return {}

        @staticmethod
        def extract_object_classes(config: Mapping[str, object]) -> list[str]:
            """Extract object classes from configuration dict.

            Business Rule: Object Classes Configuration
            ==========================================
            LDAP object classes define the schema for directory entries. This method
            extracts object class lists from configuration with safe defaults.

            Validation Rules:
            - Must be a list
            - All items converted to strings
            - Default to ["top"] if invalid or missing

            Args:
                config: Configuration dictionary containing object_classes

            Returns:
                list[str]: List of object classes or ["top"] default

            """
            raw_object_classes = config.get("object_classes")
            if u.Guards.is_list(raw_object_classes):
                return [str(v) for v in raw_object_classes]
            return ["top"]

        @staticmethod
        def to_bool(value: object, *, default: bool) -> bool:
            """Convert value to bool with safe defaults.

            Business Rule: Boolean Configuration Conversion
            ==============================================
            Boolean configuration values can come as strings ("true", "1", "yes"),
            integers (0/1), or actual booleans. This method standardizes conversion
            with clear rules to avoid ambiguity.

            Conversion Rules:
            - bool values pass through unchanged
            - int values: non-zero = True, zero = False
            - str values: case-insensitive check for "1", "true", "yes", "on"
            - All other types return default

            Args:
                value: Value to convert
                default: Default value if conversion fails

            Returns:
                bool: Converted value or default

            """
            match value:
                case bool():
                    return value
                case int():
                    return value != 0
                case str():
                    return value.strip().lower() in {"1", "true", "yes", "on"}
                case _:
                    return default

        @staticmethod
        def to_int(value: object, default: int) -> int:
            """Convert value to int with safe defaults.

            Business Rule: Safe Type Conversion
            ===================================
            Configuration values can come from various sources (env vars, config files,
            command line args) and may not have the expected type. This method provides
            safe conversion with sensible defaults to prevent runtime errors.

            Conversion Rules:
            - bool values return default (avoid 0/1 confusion)
            - int values pass through unchanged
            - str values attempt int() conversion, fallback to default on error
            - All other types return default

            Args:
                value: Value to convert (from any source)
                default: Default value if conversion fails

            Returns:
                int: Converted value or default

            """
            match value:
                case bool():
                    return default
                case int():
                    return value
                case str():
                    try:
                        return int(value)
                    except ValueError:
                        return default
                case _:
                    return default

        @staticmethod
        def to_str(value: object, default: str = "") -> str:
            """Convert value to str with safe defaults.

            Business Rule: String Configuration Conversion
            =============================================
            String configuration values need consistent handling regardless of source.
            This method ensures all values can be safely converted to strings.

            Conversion Rules:
            - str values pass through unchanged
            - None becomes empty string (unless default provided)
            - All other types use str() conversion

            Args:
                value: Value to convert
                default: Default value if value is None

            Returns:
                str: Converted string or default for None

            """
            if value is None:
                return default
            match value:
                case str():
                    return value
                case _:
                    pass
            return str(value)


u = FlextTargetLdapUtilities
__all__ = ["FlextTargetLdapUtilities", "u"]
