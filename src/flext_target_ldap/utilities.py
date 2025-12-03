"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import ClassVar, override

from flext_core import FlextResult, u

from flext_target_ldap.constants import FlextTargetLdapConstants


class FlextTargetLdapUtilities(u):
    """Single unified utilities class for Singer target LDAP operations.

    Follows FLEXT unified class pattern with nested helper classes for
    domain-specific Singer target functionality with LDAP directory operations.
    Extends urget-specific operations.
    """

    LDAP_DEFAULT_PORT: ClassVar[int] = 389
    LDAPS_DEFAULT_PORT: ClassVar[int] = 636

    @override
    def __init__(self) -> None:
        """Initialize LDAP target utilities."""
        super().__init__()

    class SingerUtilities:
        """Singer protocol utilities for target operations."""

        @staticmethod
        def parse_singer_message(line: str) -> FlextResult[dict[str, object]]:
            """Parse Singer message from input line.

            Args:
            line: JSON line from Singer tap

            Returns:
            FlextResult[dict[str, object]]: Parsed message or error

            """
            if not line or not line.strip():
                return FlextResult[dict[str, object]].fail("Empty input line")

            try:
                message = json.loads(line.strip())
                if not isinstance(message, dict):
                    return FlextResult[dict[str, object]].fail(
                        "Message must be a JSON object"
                    )

                if "type" not in message:
                    return FlextResult[dict[str, object]].fail(
                        "Message missing required 'type' field"
                    )

                return FlextResult[dict[str, object]].ok(message)

            except json.JSONDecodeError as e:
                return FlextResult[dict[str, object]].fail(f"Invalid JSON: {e}")

        @staticmethod
        def validate_record_message(
            message: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Singer RECORD message structure.

            Args:
            message: Singer message to validate

            Returns:
            FlextResult[dict[str, object]]: Validated record or error

            """
            if message.get("type") != "RECORD":
                return FlextResult[dict[str, object]].fail(
                    "Message type must be RECORD"
                )

            required_fields = ["stream", "record"]
            for field in required_fields:
                if field not in message:
                    return FlextResult[dict[str, object]].fail(
                        f"RECORD message missing '{field}' field"
                    )

            record = message["record"]
            if not isinstance(record, dict):
                return FlextResult[dict[str, object]].fail(
                    "Record data must be a dictionary"
                )

            return FlextResult[dict[str, object]].ok(message)

        @staticmethod
        def validate_schema_message(
            message: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Singer SCHEMA message structure.

            Args:
            message: Singer message to validate

            Returns:
            FlextResult[dict[str, object]]: Validated schema or error

            """
            if message.get("type") != "SCHEMA":
                return FlextResult[dict[str, object]].fail(
                    "Message type must be SCHEMA"
                )

            required_fields = ["stream", "schema"]
            for field in required_fields:
                if field not in message:
                    return FlextResult[dict[str, object]].fail(
                        f"SCHEMA message missing '{field}' field"
                    )

            schema = message["schema"]
            if not isinstance(schema, dict):
                return FlextResult[dict[str, object]].fail(
                    "Schema data must be a dictionary"
                )

            return FlextResult[dict[str, object]].ok(message)

        @staticmethod
        def write_state_message(state: dict[str, object]) -> None:
            """Write Singer state message to stdout.

            Args:
            state: State data to write

            """

    class LdapDataProcessing:
        """LDAP-specific data processing utilities."""

        @staticmethod
        def build_ldap_dn(
            record: dict[str, object],
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
                    "Record, DN template, and base DN are required"
                )

            try:
                # Replace placeholders in DN template
                dn_rdn = dn_template
                for key, value in record.items():
                    placeholder = f"{{{key}}}"
                    if placeholder in dn_rdn:
                        if value is None:
                            return FlextResult[str].fail(
                                f"Cannot build DN: {key} is null"
                            )
                        dn_rdn = dn_rdn.replace(placeholder, str(value))

                # Check if all placeholders were replaced
                if "{" in dn_rdn and "}" in dn_rdn:
                    return FlextResult[str].fail(
                        f"Unresolved placeholders in DN: {dn_rdn}"
                    )

                # Combine with base DN
                full_dn = f"{dn_rdn},{base_dn}"

                # Validate DN format
                if not FlextTargetLdapUtilities.LdapDataProcessing.FlextLdifUtilities.DN.split(
                    full_dn
                ):
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
            record: dict[str, object],
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
                    "Record cannot be empty"
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
                    f"Error converting to LDAP attributes: {e}"
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
            record: dict[str, object],
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
                return FlextTargetLdapUtilities.DEFAULT_BATCH_SIZE

            calculated_size = max(1, record_count // target_batches)
            return min(calculated_size, FlextTargetLdapUtilities.DEFAULT_BATCH_SIZE)

        @staticmethod
        def validate_stream_compatibility(
            stream_name: str,
            schema: dict[str, object],
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
            properties = schema.get("properties", {})
            if not properties:
                return FlextResult[bool].fail("Schema must have properties")

            # Check for DN building capability
            has_dn_field = "dn" in properties
            has_id_fields = any(
                key in properties for key in ["id", "uid", "cn", "username", "email"]
            )

            if not has_dn_field and not has_id_fields:
                return FlextResult[bool].fail(
                    "Schema must have either 'dn' field or identifier fields (id, uid, cn, username, email)"
                )

            return FlextResult[bool].ok(True)

        @staticmethod
        def generate_ldap_stream_metadata(
            stream_name: str,
            record_count: int,
            processing_time: float,
        ) -> dict[str, object]:
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

    class ConfigValidation:
        """Configuration validation utilities."""

        @staticmethod
        def validate_ldap_connection_config(
            config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate LDAP connection configuration.

            Args:
            config: Configuration dictionary

            Returns:
            FlextResult[dict[str, object]]: Validated config or error

            """
            required_fields = ["host", "bind_dn", "bind_password", "base_dn"]
            missing_fields = [field for field in required_fields if field not in config]

            if missing_fields:
                return FlextResult[dict[str, object]].fail(
                    f"Missing required LDAP connection fields: {', '.join(missing_fields)}"
                )

            # Validate host format
            host = config["host"]
            if not isinstance(host, str) or not host.strip():
                return FlextResult[dict[str, object]].fail(
                    "Host must be a non-empty string"
                )

            # Validate bind DN format
            bind_dn = config["bind_dn"]
            if not FlextTargetLdapUtilities.LdapDataProcessing.FlextLdifUtilities.DN.split(
                bind_dn
            ):
                return FlextResult[dict[str, object]].fail(
                    f"Invalid bind DN format: {bind_dn}"
                )

            # Validate base DN format
            base_dn = config["base_dn"]
            if not FlextTargetLdapUtilities.LdapDataProcessing.FlextLdifUtilities.DN.split(
                base_dn
            ):
                return FlextResult[dict[str, object]].fail(
                    f"Invalid base DN format: {base_dn}"
                )

            # Validate port if provided
            if "port" in config:
                port = config["port"]
                if (
                    not isinstance(port, int)
                    or port <= 0
                    or port > FlextTargetLdapConstants.Connection.Ldap.MAX_PORT_NUMBER
                ):
                    return FlextResult[dict[str, object]].fail(
                        "Port must be a valid integer between 1 and 65535"
                    )

            # Validate SSL settings
            use_ssl = config.get("use_ssl", False)
            use_tls = config.get("use_tls", False)
            if use_ssl and use_tls:
                return FlextResult[dict[str, object]].fail(
                    "Cannot use both SSL and TLS simultaneously"
                )

            return FlextResult[dict[str, object]].ok(config)

        @staticmethod
        def validate_target_config(
            config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate target configuration.

            Args:
            config: Target configuration

            Returns:
            FlextResult[dict[str, object]]: Validated config or error

            """
            # Validate LDAP connection
            ldap_result = FlextTargetLdapUtilities.ConfigValidation.validate_ldap_connection_config(
                config
            )
            if ldap_result.is_failure:
                return ldap_result

            # Validate operation mode
            operation_mode = config.get("operation_mode", "upsert")
            valid_modes = ["insert", "update", "upsert", "delete"]
            if operation_mode not in valid_modes:
                return FlextResult[dict[str, object]].fail(
                    f"Invalid operation mode: {operation_mode}. Valid modes: {', '.join(valid_modes)}"
                )

            # Validate DN template if provided
            if "dn_template" in config:
                dn_template = config["dn_template"]
                if not isinstance(dn_template, str) or not dn_template.strip():
                    return FlextResult[dict[str, object]].fail(
                        "DN template must be a non-empty string"
                    )

            # Validate batch size
            batch_size = config.get(
                "batch_size", FlextTargetLdapUtilities.DEFAULT_BATCH_SIZE
            )
            if not isinstance(batch_size, int) or batch_size <= 0:
                return FlextResult[dict[str, object]].fail(
                    "Batch size must be a positive integer"
                )

            return FlextResult[dict[str, object]].ok(config)

    class StateManagement:
        """State management utilities for target operations."""

        @staticmethod
        def get_target_state(
            state: dict[str, object], stream_name: str
        ) -> dict[str, object]:
            """Get state for a specific target stream.

            Args:
            state: Complete state dictionary
            stream_name: Name of the stream

            Returns:
            dict[str, object]: Stream state

            """
            return state.get("bookmarks", {}).get(stream_name, {})

        @staticmethod
        def set_target_state(
            state: dict[str, object],
            stream_name: str,
            stream_state: dict[str, object],
        ) -> dict[str, object]:
            """Set state for a specific target stream.

            Args:
            state: Complete state dictionary
            stream_name: Name of the stream
            stream_state: State data for the stream

            Returns:
            dict[str, object]: Updated state

            """
            if "bookmarks" not in state:
                state["bookmarks"] = {}

            state["bookmarks"][stream_name] = stream_state
            return state

        @staticmethod
        def create_processing_state(
            stream_name: str,
            records_processed: int,
            last_processed_record: dict[str, object] | None = None,
        ) -> dict[str, object]:
            """Create processing state for target stream.

            Args:
            stream_name: Name of the stream
            records_processed: Number of records processed
            last_processed_record: Last processed record for checkpointing

            Returns:
            dict[str, object]: Processing state

            """
            state = {
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
            state: dict[str, object],
            stream_name: str,
            records_count: int,
        ) -> dict[str, object]:
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

            current_count = stream_state.get("records_processed", 0)
            new_count = current_count + records_count

            updated_stream_state = {
                **stream_state,
                "records_processed": new_count,
                "last_updated": datetime.now(UTC).isoformat(),
                "batch_count": stream_state.get("batch_count", 0) + 1,
            }

            return FlextTargetLdapUtilities.StateManagement.set_target_state(
                state, stream_name, updated_stream_state
            )

    # Proxy methods for backward compatibility
    @classmethod
    def parse_singer_message(cls, line: str) -> FlextResult[dict[str, object]]:
        """Proxy method for SingerUtilities.parse_singer_message()."""
        return cls.SingerUtilities.parse_singer_message(line)

    @classmethod
    def build_ldap_dn(
        cls,
        record: dict[str, object],
        dn_template: str,
        base_dn: str,
    ) -> FlextResult[str]:
        """Proxy method for LdapDataProcessing.build_ldap_dn()."""
        return cls.LdapDataProcessing.build_ldap_dn(record, dn_template, base_dn)

    @classmethod
    def convert_record_to_ldap_attributes(
        cls,
        record: dict[str, object],
        attribute_mapping: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, list[bytes]]]:
        """Proxy method for LdapDataProcessing.convert_record_to_ldap_attributes()."""
        return cls.LdapDataProcessing.convert_record_to_ldap_attributes(
            record, attribute_mapping
        )

    @classmethod
    def validate_ldap_connection_config(
        cls, config: dict[str, object]
    ) -> FlextResult[dict[str, object]]:
        """Proxy method for ConfigValidation.validate_ldap_connection_config()."""
        return cls.ConfigValidation.validate_ldap_connection_config(config)

    @classmethod
    def get_target_state(
        cls, state: dict[str, object], stream_name: str
    ) -> dict[str, object]:
        """Proxy method for StateManagement.get_target_state()."""
        return cls.StateManagement.get_target_state(state, stream_name)

    @classmethod
    def create_processing_state(
        cls,
        stream_name: str,
        records_processed: int,
        last_processed_record: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Proxy method for StateManagement.create_processing_state()."""
        return cls.StateManagement.create_processing_state(
            stream_name, records_processed, last_processed_record
        )


__all__ = [
    "FlextTargetLdapUtilities",
]
