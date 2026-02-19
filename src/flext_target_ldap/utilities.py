"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import override

from flext_core import FlextResult, FlextTypes as t
from flext_core.utilities import FlextUtilities as u_core
from flext_ldap.models import FlextLdapModels

from flext_target_ldap.constants import c


class FlextTargetLdapUtilities(u_core):
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
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Parse Singer message from input line.

            Args:
            line: JSON line from Singer tap

            Returns:
            FlextResult[dict[str, t.GeneralValueType]]: Parsed message or error

            """
            if not line or not line.strip():
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Empty input line"
                )

            try:
                message = json.loads(line.strip())
                if not isinstance(message, dict):
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        "Message must be a JSON object",
                    )

                if "type" not in message:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        "Message missing required 'type' field",
                    )

                return FlextResult[dict[str, t.GeneralValueType]].ok(message)

            except json.JSONDecodeError as e:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Invalid JSON: {e}"
                )

        @staticmethod
        def validate_record_message(
            message: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Validate Singer RECORD message structure.

            Args:
            message: Singer message to validate

            Returns:
            FlextResult[dict[str, t.GeneralValueType]]: Validated record or error

            """
            if message.get("type") != "RECORD":
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Message type must be RECORD",
                )

            required_fields = ["stream", "record"]
            for field in required_fields:
                if field not in message:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"RECORD message missing '{field}' field",
                    )

            record = message["record"]
            if not isinstance(record, dict):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Record data must be a dictionary",
                )

            return FlextResult[dict[str, t.GeneralValueType]].ok(message)

        @staticmethod
        def validate_schema_message(
            message: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Validate Singer SCHEMA message structure.

            Args:
            message: Singer message to validate

            Returns:
            FlextResult[dict[str, t.GeneralValueType]]: Validated schema or error

            """
            if message.get("type") != "SCHEMA":
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Message type must be SCHEMA",
                )

            required_fields = ["stream", "schema"]
            for field in required_fields:
                if field not in message:
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        f"SCHEMA message missing '{field}' field",
                    )

            schema = message["schema"]
            if not isinstance(schema, dict):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Schema data must be a dictionary",
                )

            return FlextResult[dict[str, t.GeneralValueType]].ok(message)

        @staticmethod
        def write_state_message(state: dict[str, t.GeneralValueType]) -> None:
            """Write Singer state message to stdout.

            Args:
            state: State data to write

            """

    class LdapDataProcessing:
        """LDAP-specific data processing utilities."""

        @staticmethod
        def build_ldap_dn(
            record: dict[str, t.GeneralValueType],
            dn_template: str,
            base_dn: str,
        ) -> FlextResult[str]:
            """Build LDAP Distinguished Name from record data.

            Args:
            record: Record data
            dn_template: DN template with placeholders
            base_dn: Base DN for the directory

            Returns:
            FlextResult[str]: Built DN or error

            """
            if not record or not dn_template or not base_dn:
                return FlextResult[str].fail(
                    "Record, DN template, and base DN are required",
                )

            try:
                # Replace placeholders in DN template
                dn_rdn = dn_template
                for key, value in record.items():
                    placeholder = f"{{{key}}}"
                    if placeholder in dn_rdn:
                        if value is None:
                            return FlextResult[str].fail(
                                f"Cannot build DN: {key} is null",
                            )
                        dn_rdn = dn_rdn.replace(placeholder, str(value))

                # Check if all placeholders were replaced
                if "{" in dn_rdn and "}" in dn_rdn:
                    return FlextResult[str].fail(
                        f"Unresolved placeholders in DN: {dn_rdn}",
                    )

                # Combine with base DN
                full_dn = f"{dn_rdn},{base_dn}"

                # Validate DN format
                if not FlextTargetLdapUtilities.LdapDataProcessing.split(full_dn):
                    return FlextResult[str].fail(f"Invalid DN format: {full_dn}")

                return FlextResult[str].ok(full_dn)

            except Exception as e:
                return FlextResult[str].fail(f"Error building DN: {e}")

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

            # Basic DN format validation
            # Should contain at least one RDN component (attr=value)
            dn_pattern = (
                r"^[a-zA-Z][\w\-]*\s*=\s*[^,]+(?:\s*,\s*[a-zA-Z][\w\-]*\s*=\s*[^,]+)*$"
            )
            return bool(re.match(dn_pattern, dn.strip()))

        @staticmethod
        def convert_record_to_ldap_attributes(
            record: dict[str, t.GeneralValueType],
            attribute_mapping: dict[str, str] | None = None,
        ) -> FlextResult[dict[str, list[bytes]]]:
            """Convert Singer record to LDAP attributes format.

            Args:
            record: Singer record data
            attribute_mapping: Optional mapping from record keys to LDAP attributes

            Returns:
            FlextResult[dict[str, list[bytes]]]: LDAP attributes or error

            """
            if not record:
                return FlextResult[dict[str, list[bytes]]].fail(
                    "Record cannot be empty",
                )

            try:
                ldap_attrs: dict[str, list[bytes]] = {}
                mapping = attribute_mapping or {}

                for key, value in record.items():
                    if value is None:
                        continue  # Skip null values

                    # Get LDAP attribute name (use mapping or original key)
                    ldap_attr = mapping.get(key, key)

                    # Convert value to LDAP format
                    if isinstance(value, list):
                        # Multi-value attribute
                        ldap_values = [
                            str(item).encode("utf-8")
                            for item in value
                            if item is not None
                        ]
                        if ldap_values:
                            ldap_attrs[ldap_attr] = ldap_values
                    else:
                        # Single-value attribute
                        ldap_attrs[ldap_attr] = [str(value).encode("utf-8")]

                return FlextResult[dict[str, list[bytes]]].ok(ldap_attrs)

            except Exception as e:
                return FlextResult[dict[str, list[bytes]]].fail(
                    f"Error converting to LDAP attributes: {e}",
                )

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

            # Escape special LDAP characters
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

            # Remove leading/trailing whitespace
            return sanitized.strip()

        @staticmethod
        def extract_object_classes(
            record: dict[str, t.GeneralValueType],
            default_object_classes: list[str] | None = None,
        ) -> list[str]:
            """Extract object classes for LDAP entry.

            Args:
            record: Singer record data
            default_object_classes: Default object classes if not in record

            Returns:
            list[str]: List of object classes

            """
            # Check for object classes in record
            object_classes = record.get("objectClass") or record.get("objectclass")

            if object_classes:
                if isinstance(object_classes, list):
                    return [str(oc) for oc in object_classes if oc]
                return [str(object_classes)]

            # Use defaults if provided
            if default_object_classes:
                return default_object_classes

            # Fallback to basic object classes
            return ["top"]

    class StreamUtilities:
        """Stream processing utilities for Singer targets."""

        @staticmethod
        def calculate_ldap_batch_size(
            record_count: int,
            target_batches: int = 10,
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
        def validate_stream_compatibility(
            stream_name: str,
            schema: dict[str, t.GeneralValueType],
        ) -> FlextResult[bool]:
            """Validate stream compatibility with LDAP operations.

            Args:
            stream_name: Name of the stream
            schema: Stream schema

            Returns:
            FlextResult[bool]: Validation result

            """
            if not stream_name or not schema:
                return FlextResult[bool].fail("Stream name and schema are required")

            # Check if schema has required properties
            raw_props = schema.get("properties", {})
            properties: dict[str, t.GeneralValueType] = (
                raw_props if isinstance(raw_props, dict) else {}
            )
            if not properties:
                return FlextResult[bool].fail("Schema must have properties")

            # Check for DN building capability
            has_dn_field = "dn" in properties
            has_id_fields = any(
                key in properties for key in ["id", "uid", "cn", "username", "email"]
            )

            if not has_dn_field and not has_id_fields:
                return FlextResult[bool].fail(
                    "Schema must have either 'dn' field or identifier fields (id, uid, cn, username, email)",
                )

            return FlextResult[bool].ok(value=True)

        @staticmethod
        def generate_ldap_stream_metadata(
            stream_name: str,
            record_count: int,
            processing_time: float,
        ) -> dict[str, t.GeneralValueType]:
            """Generate metadata for LDAP stream processing.

            Args:
            stream_name: Name of the stream
            record_count: Number of records processed
            processing_time: Time taken for processing

            Returns:
            dict[str, t.GeneralValueType]: Stream metadata

            """
            return {
                "stream_name": stream_name,
                "records_processed": record_count,
                "processing_time_seconds": processing_time,
                "records_per_second": record_count / max(processing_time, 0.001),
                "processing_timestamp": datetime.now(UTC).isoformat(),
                "target_type": "ldap",
            }

    class ConfigValidation:
        """Configuration validation utilities."""

        @staticmethod
        def validate_ldap_connection_config(
            config: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Validate LDAP connection configuration.

            Args:
            config: Configuration dictionary

            Returns:
            FlextResult[dict[str, t.GeneralValueType]]: Validated config or error

            """
            required_fields = ["host", "bind_dn", "bind_password", "base_dn"]
            missing_fields = [field for field in required_fields if field not in config]

            if missing_fields:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Missing required LDAP connection fields: {', '.join(missing_fields)}",
                )

            # Validate host format
            host = config["host"]
            if not isinstance(host, str) or not host.strip():
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Host must be a non-empty string",
                )

            # Validate bind DN format
            bind_dn = config["bind_dn"]
            if not isinstance(bind_dn, str):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Bind DN must be a string",
                )
            if not FlextTargetLdapUtilities.LdapDataProcessing.split(bind_dn):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Invalid bind DN format: {bind_dn}",
                )

            # Validate base DN format
            base_dn = config["base_dn"]
            if not isinstance(base_dn, str):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Base DN must be a string",
                )
            if not FlextTargetLdapUtilities.LdapDataProcessing.split(base_dn):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Invalid base DN format: {base_dn}",
                )

            # Validate base DN format
            base_dn = config["base_dn"]
            if not isinstance(
                base_dn, str
            ) or not FlextTargetLdapUtilities.LdapDataProcessing.split(base_dn):
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Invalid base DN format: {base_dn}",
                )

            # Validate port if provided
            if "port" in config:
                port = config["port"]
                if (
                    not isinstance(port, int)
                    or port <= 0
                    or port > c.TargetLdap.Connection.MAX_PORT_NUMBER
                ):
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        "Port must be a valid integer between 1 and 65535",
                    )

            # Validate SSL settings
            use_ssl = config.get("use_ssl", False)
            use_tls = config.get("use_tls", False)
            if use_ssl and use_tls:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Cannot use both SSL and TLS simultaneously",
                )

            return FlextResult[dict[str, t.GeneralValueType]].ok(config)

        @staticmethod
        def validate_target_config(
            config: dict[str, t.GeneralValueType],
        ) -> FlextResult[dict[str, t.GeneralValueType]]:
            """Validate target configuration.

            Args:
            config: Target configuration

            Returns:
            FlextResult[dict[str, t.GeneralValueType]]: Validated config or error

            """
            # Validate LDAP connection
            ldap_result = FlextTargetLdapUtilities.ConfigValidation.validate_ldap_connection_config(
                config,
            )
            if ldap_result.is_failure:
                return ldap_result

            # Validate operation mode
            operation_mode = config.get("operation_mode", "upsert")
            valid_modes = ["insert", "update", "upsert", "delete"]
            if operation_mode not in valid_modes:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"Invalid operation mode: {operation_mode}. Valid modes: {', '.join(valid_modes)}",
                )

            # Validate DN template if provided
            if "dn_template" in config:
                dn_template = config["dn_template"]
                if not isinstance(dn_template, str) or not dn_template.strip():
                    return FlextResult[dict[str, t.GeneralValueType]].fail(
                        "DN template must be a non-empty string",
                    )

            # Validate batch size
            batch_size = config.get(
                "batch_size",
                c.TargetLdap.Processing.DEFAULT_BATCH_SIZE,
            )
            if not isinstance(batch_size, int) or batch_size <= 0:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Batch size must be a positive integer",
                )

            return FlextResult[dict[str, t.GeneralValueType]].ok(config)

    class StateManagement:
        """State management utilities for target operations."""

        @staticmethod
        def get_target_state(
            state: dict[str, t.GeneralValueType],
            stream_name: str,
        ) -> dict[str, t.GeneralValueType]:
            """Get state for a specific target stream.

            Args:
            state: Complete state dictionary
            stream_name: Name of the stream

            Returns:
            dict[str, t.GeneralValueType]: Stream state

            """
            bookmarks = state.get("bookmarks")
            if not isinstance(bookmarks, dict):
                return {}

            stream_state_data = bookmarks.get(stream_name)
            if isinstance(stream_state_data, dict):
                return stream_state_data
            return {}

        @staticmethod
        def set_target_state(
            state: dict[str, t.GeneralValueType],
            stream_name: str,
            stream_state: dict[str, t.GeneralValueType],
        ) -> dict[str, t.GeneralValueType]:
            """Set state for a specific target stream.

            Args:
            state: Complete state dictionary
            stream_name: Name of the stream
            stream_state: State data for the stream

            Returns:
            dict[str, t.GeneralValueType]: Updated state

            """
            bookmarks = state.get("bookmarks")
            if not isinstance(bookmarks, dict):
                bookmarks = {}
                state["bookmarks"] = bookmarks

            bookmarks[stream_name] = stream_state
            return state

        @staticmethod
        def create_processing_state(
            stream_name: str,
            records_processed: int,
            last_processed_record: dict[str, t.GeneralValueType] | None = None,
        ) -> dict[str, t.GeneralValueType]:
            """Create processing state for target stream.

            Args:
            stream_name: Name of the stream
            records_processed: Number of records processed
            last_processed_record: Last processed record for checkpointing

            Returns:
            dict[str, t.GeneralValueType]: Processing state

            """
            state: dict[str, t.GeneralValueType] = {
                "stream_name": stream_name,
                "records_processed": records_processed,
                "last_updated": datetime.now(UTC).isoformat(),
                "target_type": "ldap",
            }

            if last_processed_record:
                # Store minimal checkpoint information
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
        def update_processing_progress(
            state: dict[str, t.GeneralValueType],
            stream_name: str,
            records_count: int,
        ) -> dict[str, t.GeneralValueType]:
            """Update processing progress in state.

            Args:
            state: Current state
            stream_name: Name of the stream
            records_count: Number of records processed in this batch

            Returns:
            dict[str, t.GeneralValueType]: Updated state

            """
            stream_state = FlextTargetLdapUtilities.StateManagement.get_target_state(
                state,
                stream_name,
            )

            current_count_val = stream_state.get("records_processed", 0)
            current_count: int = (
                current_count_val if isinstance(current_count_val, int) else 0
            )
            new_count = current_count + records_count

            batch_count_val = stream_state.get("batch_count", 0)
            batch_count: int = (
                batch_count_val if isinstance(batch_count_val, int) else 0
            )

            updated_stream_state: dict[str, t.GeneralValueType] = {
                **stream_state,
                "records_processed": new_count,
                "last_updated": datetime.now(UTC).isoformat(),
                "batch_count": batch_count + 1,
            }

            return FlextTargetLdapUtilities.StateManagement.set_target_state(
                state,
                stream_name,
                updated_stream_state,
            )

    # Proxy methods for backward compatibility
    @classmethod
    def parse_singer_message(
        cls, line: str
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Proxy method for TargetLdap.parse_singer_message()."""
        return cls.TargetLdap.parse_singer_message(line)

    @classmethod
    def build_ldap_dn(
        cls,
        record: dict[str, t.GeneralValueType],
        dn_template: str,
        base_dn: str,
    ) -> FlextResult[str]:
        """Proxy method for LdapDataProcessing.build_ldap_dn()."""
        return cls.LdapDataProcessing.build_ldap_dn(record, dn_template, base_dn)

    @classmethod
    def convert_record_to_ldap_attributes(
        cls,
        record: dict[str, t.GeneralValueType],
        attribute_mapping: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, list[bytes]]]:
        """Proxy method for LdapDataProcessing.convert_record_to_ldap_attributes()."""
        return cls.LdapDataProcessing.convert_record_to_ldap_attributes(
            record,
            attribute_mapping,
        )

    @classmethod
    def validate_ldap_connection_config(
        cls,
        config: dict[str, t.GeneralValueType],
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Proxy method for ConfigValidation.validate_ldap_connection_config()."""
        return cls.ConfigValidation.validate_ldap_connection_config(config)

    @classmethod
    def get_target_state(
        cls,
        state: dict[str, t.GeneralValueType],
        stream_name: str,
    ) -> dict[str, t.GeneralValueType]:
        """Proxy method for StateManagement.get_target_state()."""
        return cls.StateManagement.get_target_state(state, stream_name)

    @classmethod
    def create_processing_state(
        cls,
        stream_name: str,
        records_processed: int,
        last_processed_record: dict[str, t.GeneralValueType] | None = None,
    ) -> dict[str, t.GeneralValueType]:
        """Proxy method for StateManagement.create_processing_state()."""
        return cls.StateManagement.create_processing_state(
            stream_name,
            records_processed,
            last_processed_record,
        )

    class TypeConversion:
        """Type conversion utilities for configuration parsing."""

        @staticmethod
        def to_int(value: t.GeneralValueType, default: int) -> int:
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
            if isinstance(value, bool):
                return default
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                try:
                    return int(value)
                except ValueError:
                    return default
            return default

        @staticmethod
        def to_bool(value: t.GeneralValueType, *, default: bool) -> bool:
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
            if isinstance(value, bool):
                return value
            if isinstance(value, int):
                return value != 0
            if isinstance(value, str):
                return value.strip().lower() in {"1", "true", "yes", "on"}
            return default

        @staticmethod
        def to_str(value: t.GeneralValueType, default: str = "") -> str:
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
            if isinstance(value, str):
                return value
            return str(value)

        @staticmethod
        def build_connection_config(
            config: dict[str, t.GeneralValueType],
        ) -> FlextLdapModels.Ldap.ConnectionConfig:
            """Build LDAP connection configuration from config dict.

            Args:
                config: Raw configuration dictionary from any source

            Returns:
                FlextLdapModels.Ldap.ConnectionConfig: Validated connection config

            """
            # Import here to avoid circular imports

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
            config: dict[str, t.GeneralValueType],
        ) -> dict[str, str]:
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
            if isinstance(raw_attr_map, dict):
                return {str(k): str(v) for k, v in raw_attr_map.items()}
            return {}

        @staticmethod
        def extract_object_classes(
            config: dict[str, t.GeneralValueType],
        ) -> list[str]:
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
            if isinstance(raw_object_classes, list):
                return [str(v) for v in raw_object_classes]
            return ["top"]


__all__ = [
    "FlextTargetLdapUtilities",
]
