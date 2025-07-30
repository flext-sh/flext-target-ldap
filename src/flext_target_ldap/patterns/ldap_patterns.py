"""LDAP patterns using flext-core patterns."""

from __future__ import annotations

import json
from typing import Any

# Import from flext-core for foundational patterns
from flext_core import FlextResult, get_logger

logger = get_logger(__name__)


class LDAPTypeConverter:
    """Convert data types for LDAP storage using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize LDAP type converter."""

    def convert_singer_to_ldap(self, singer_type: str, value: Any) -> FlextResult[Any]:
        """Convert Singer type to LDAP-compatible type."""
        try:
            if value is None:
                return FlextResult.ok(None)

            if singer_type in {"string", "text"}:
                return FlextResult.ok(str(value))
            if singer_type in {"integer", "number"}:
                return FlextResult.ok(str(value))  # LDAP stores numbers as strings
            if singer_type == "boolean":
                return FlextResult.ok("TRUE" if value else "FALSE")
            if singer_type in {"object", "array"}:
                return FlextResult.ok(json.dumps(value))
            return FlextResult.ok(str(value))

        except (RuntimeError, ValueError, TypeError) as e:
            logger.warning(f"Type conversion failed for {singer_type}: {e}")
            return FlextResult.ok(str(value))  # Fallback to string


class LDAPDataTransformer:
    """Transform data for LDAP storage using flext-core patterns."""

    def __init__(self, type_converter: LDAPTypeConverter | None = None) -> None:
        """Initialize LDAP data transformer."""
        self.type_converter = type_converter or LDAPTypeConverter()

    def transform_record(
        self,
        record: dict[str, Any],
        schema: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Transform Singer record for LDAP storage."""
        try:
            transformed = {}

            for key, value in record.items():
                # LDAP-specific attribute naming
                ldap_key = self._normalize_ldap_attribute_name(key)

                # Type conversion
                if schema:
                    properties = schema.get("properties", {})
                    prop_def = properties.get(key, {})
                    singer_type = prop_def.get("type", "string")

                    convert_result = self.type_converter.convert_singer_to_ldap(
                        singer_type,
                        value,
                    )
                    if convert_result.is_success:
                        transformed[ldap_key] = convert_result.data
                    else:
                        transformed[ldap_key] = str(value)
                else:
                    transformed[ldap_key] = value

            return FlextResult.ok(transformed)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP record transformation failed")
            return FlextResult.fail(f"Record transformation failed: {e}")

    def _normalize_ldap_attribute_name(self, name: str) -> str:
        """Normalize attribute name for LDAP conventions."""
        # LDAP attribute naming conventions
        normalized = name.replace("_", "").replace("-", "")

        # Convert to camelCase for LDAP
        if "_" in name or "-" in name:
            parts = name.replace("-", "_").split("_")
            normalized = parts[0].lower() + "".join(
                word.capitalize() for word in parts[1:]
            )
        else:
            normalized = name.lower()

        return normalized

    def prepare_ldap_attributes(
        self,
        record: dict[str, Any],
        object_classes: list[str],
    ) -> FlextResult[dict[str, Any]]:
        """Prepare attributes for LDAP entry creation."""
        try:
            attributes = {}

            # Add object classes
            attributes["objectClass"] = object_classes

            # Add transformed attributes
            for key, value in record.items():
                if value is not None:
                    # Handle multi-valued attributes
                    if isinstance(value, list):
                        attributes[key] = value
                    else:
                        attributes[key] = [str(value)]

            return FlextResult.ok(attributes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP attribute preparation failed")
            return FlextResult.fail(f"Attribute preparation failed: {e}")


class LDAPSchemaMapper:
    """Map Singer schemas to LDAP schemas using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize LDAP schema mapper."""

    def map_singer_schema_to_ldap(
        self,
        schema: dict[str, Any],
        object_class: str = "inetOrgPerson",
    ) -> FlextResult[dict[str, str]]:
        """Map Singer schema to LDAP attribute definitions."""
        try:
            ldap_attributes: dict[str, str] = {}
            properties = schema.get("properties", {})

            for prop_name, prop_def in properties.items():
                ldap_name = self._normalize_attribute_name(prop_name)
                ldap_type_result = self._map_singer_type_to_ldap(prop_def, object_class)

                if ldap_type_result.is_success:
                    # ldap_type_result.data is guaranteed to be str when is_success is True
                    ldap_attributes[ldap_name] = (
                        ldap_type_result.data or "DirectoryString"
                    )
                else:
                    ldap_attributes[ldap_name] = "DirectoryString"  # Fallback

            return FlextResult.ok(ldap_attributes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP schema mapping failed")
            return FlextResult.fail(f"Schema mapping failed: {e}")

    def _normalize_attribute_name(self, name: str) -> str:
        """Normalize attribute name for LDAP."""
        # Convert to camelCase for LDAP attributes
        if "_" in name or "-" in name:
            parts = name.replace("-", "_").split("_")
            normalized = parts[0].lower() + "".join(
                word.capitalize() for word in parts[1:]
            )
        else:
            normalized = name.lower()

        return normalized

    def _map_singer_type_to_ldap(
        self,
        prop_def: dict[str, Any],
        object_class: str,
    ) -> FlextResult[str]:
        """Map Singer property definition to LDAP attribute syntax."""
        try:
            prop_type = prop_def.get("type", "string")
            prop_format = prop_def.get("format")

            if prop_format in {"date-time", "date"}:
                return FlextResult.ok("GeneralizedTime")
            if prop_type in {"integer", "number"}:
                return FlextResult.ok("Integer")
            if prop_type == "boolean":
                return FlextResult.ok("Boolean")
            if prop_type in {"object", "array"}:
                return FlextResult.ok("OctetString")
            return FlextResult.ok("DirectoryString")

        except (RuntimeError, ValueError, TypeError) as e:
            logger.warning(f"LDAP type mapping failed: {e}")
            return FlextResult.ok("DirectoryString")


class LDAPEntryManager:
    """Manage LDAP entries using flext-core patterns."""

    def __init__(self) -> None:
        """Initialize LDAP entry manager."""

    def generate_dn(
        self,
        record: dict[str, Any],
        base_dn: str,
        rdn_attribute: str = "cn",
    ) -> FlextResult[str]:
        """Generate Distinguished Name for LDAP entry."""
        try:
            # Get RDN value
            rdn_value = record.get(rdn_attribute)
            if not rdn_value:
                # Try common alternatives
                alternatives = ["commonName", "cn", "uid", "name", "id"]
                for alt in alternatives:
                    if record.get(alt):
                        rdn_value = record[alt]
                        rdn_attribute = alt
                        break

                if not rdn_value:
                    return FlextResult.fail(
                        f"No value found for RDN attribute: {rdn_attribute}",
                    )

            # Escape special characters in RDN value
            escaped_value = self._escape_dn_value(str(rdn_value))

            # Construct DN
            dn = f"{rdn_attribute}={escaped_value},{base_dn}"

            return FlextResult.ok(dn)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("DN generation failed")
            return FlextResult.fail(f"DN generation failed: {e}")

    def _escape_dn_value(self, value: str) -> str:
        """Escape special characters in DN values."""
        # LDAP DN special characters that need escaping
        special_chars = {
            ",": "\\,",
            "+": "\\+",
            '"': '\\"',
            "\\": "\\\\",
            "<": "\\<",
            ">": "\\>",
            ";": "\\;",
            "=": "\\=",
        }

        escaped = value
        for char, escaped_char in special_chars.items():
            escaped = escaped.replace(char, escaped_char)

        # Escape leading and trailing spaces
        if escaped.startswith(" "):
            escaped = "\\ " + escaped[1:]
        if escaped.endswith(" "):
            escaped = escaped[:-1] + "\\ "

        return escaped

    def determine_object_classes(
        self,
        record: dict[str, Any],
        stream_name: str,
    ) -> FlextResult[list[str]]:
        """Determine appropriate object classes for LDAP entry."""
        try:
            object_classes = ["top"]  # All entries must have 'top'

            # Determine based on stream name and record content
            stream_lower = stream_name.lower()

            if "user" in stream_lower or "person" in stream_lower:
                if "mail" in record or "email" in record:
                    object_classes.extend(
                        ["person", "organizationalPerson", "inetOrgPerson"],
                    )
                else:
                    object_classes.extend(["person", "organizationalPerson"])
            elif "group" in stream_lower:
                object_classes.append("groupOfNames")
            elif "ou" in stream_lower or "organizational" in stream_lower:
                object_classes.append("organizationalUnit")
            else:
                # Default to inetOrgPerson for flexibility
                object_classes.extend(
                    ["person", "organizationalPerson", "inetOrgPerson"],
                )

            return FlextResult.ok(object_classes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Object class determination failed")
            return FlextResult.fail(f"Object class determination failed: {e}")

    def validate_entry_attributes(
        self,
        attributes: dict[str, Any],
        object_classes: list[str],
    ) -> FlextResult[bool]:
        """Validate LDAP entry attributes against object class requirements."""
        try:
            # Basic validation - could be enhanced with schema checking
            required_attrs = set()

            for obj_class in object_classes:
                if obj_class in {"person", "organizationalPerson", "inetOrgPerson"}:
                    required_attrs.update({"cn", "sn"})
                elif obj_class == "groupOfNames":
                    required_attrs.add("member")
                elif obj_class == "organizationalUnit":
                    required_attrs.add("ou")

            # Check for required attributes
            missing_attrs = required_attrs - set(attributes.keys())
            if missing_attrs:
                return FlextResult.fail(f"Missing required attributes: {missing_attrs}")

            return FlextResult.ok(True)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Entry validation failed")
            return FlextResult.fail(f"Entry validation failed: {e}")

    def prepare_modify_changes(
        self,
        current_attrs: dict[str, Any],
        new_attrs: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Prepare modification changes for LDAP entry."""
        try:
            changes: dict[str, Any] = {}

            # Find attributes to add, modify, or delete
            all_attrs = set(current_attrs.keys()) | set(new_attrs.keys())

            for attr in all_attrs:
                current_value = current_attrs.get(attr)
                new_value = new_attrs.get(attr)

                if current_value != new_value:
                    if new_value is None:
                        # Delete attribute
                        changes[attr] = [("MODIFY_DELETE", [])]
                    elif current_value is None:
                        # Add attribute
                        values = (
                            new_value if isinstance(new_value, list) else [new_value]
                        )
                        changes[attr] = [("MODIFY_ADD", values)]
                    else:
                        # Replace attribute
                        values = (
                            new_value if isinstance(new_value, list) else [new_value]
                        )
                        changes[attr] = [("MODIFY_REPLACE", values)]

            return FlextResult.ok(changes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Modify changes preparation failed")
            return FlextResult.fail(f"Modify changes preparation failed: {e}")
