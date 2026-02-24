"""LDAP pattern helpers built on flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import override

from flext_core import FlextLogger, FlextResult
from pydantic import BaseModel, Field

logger = FlextLogger(__name__)

type Primitive = str | int | float | bool | None
type SingerValue = Primitive | list[Primitive] | dict[str, Primitive | list[Primitive]]
type SingerRecord = dict[str, SingerValue]
type TransformedRecord = dict[str, str | None]
type LdapAttributeMap = dict[str, list[str]]
type ModifyValues = list[str]
type ModifyAction = tuple[str, ModifyValues]
type ModifyMap = dict[str, list[ModifyAction]]


class SingerPropertyDefinition(BaseModel):
    """Singer field descriptor with normalized typing."""

    type: str = "string"
    format: str | None = None


class SingerSchemaDefinition(BaseModel):
    """Singer schema shape used by LDAP mapping."""

    properties: dict[str, SingerPropertyDefinition] = Field(default_factory=dict)


class LDAPTypeConverter:
    """Convert Singer values to LDAP-safe string values."""

    _COMPLEX_KIND = "object"

    @override
    def __init__(self) -> None:
        """Initialize LDAP type converter."""

    def convert_singer_to_ldap(
        self,
        singer_type: str,
        value: SingerValue,
    ) -> FlextResult[str | None]:
        """Convert Singer scalar/list/map values for LDAP persistence."""
        try:
            if value is None:
                result = None
            elif singer_type in {"string", "text"} or singer_type in {
                "integer",
                "number",
            }:
                result = str(value)
            elif singer_type == "boolean":
                result = self._normalize_bool(value)
            elif singer_type in {self._COMPLEX_KIND, "array"}:
                result = json.dumps(value)
            else:
                result = str(value)

            return FlextResult[str | None].ok(result)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.warning(f"Type conversion failed for {singer_type}: {e}")
            return FlextResult[str | None].ok(str(value))

    def _normalize_bool(self, value: SingerValue) -> str:
        """Normalize multiple boolean-like forms to LDAP literals."""
        match value:
            case bool() as flag:
                return "TRUE" if flag else "FALSE"
            case int() as number:
                return "TRUE" if number != 0 else "FALSE"
            case str() as text:
                lowered = text.strip().lower()
                truthy = lowered in {"1", "true", "yes", "on"}
                return "TRUE" if truthy else "FALSE"
            case _:
                return "TRUE" if bool(value) else "FALSE"


class LDAPDataTransformer:
    """Transform Singer records into LDAP-oriented records."""

    @override
    def __init__(self, type_converter: LDAPTypeConverter | None = None) -> None:
        """Initialize LDAP data transformer."""
        self.type_converter = type_converter or LDAPTypeConverter()

    def transform_record(
        self,
        record: SingerRecord,
        schema: SingerSchemaDefinition
        | Mapping[str, Mapping[str, Mapping[str, str] | str]]
        | None = None,
    ) -> FlextResult[TransformedRecord]:
        """Transform Singer record for LDAP storage."""
        try:
            transformed: TransformedRecord = {}
            schema_model = SingerSchemaDefinition.model_validate(schema or {})

            for key, value in record.items():
                ldap_key = self._normalize_ldap_attribute_name(key)
                prop_def = schema_model.properties.get(key)
                singer_type = prop_def.type if prop_def is not None else "string"

                convert_result = self.type_converter.convert_singer_to_ldap(
                    singer_type,
                    value,
                )
                transformed[ldap_key] = (
                    convert_result.data if convert_result.is_success else str(value)
                )

            return FlextResult[TransformedRecord].ok(transformed)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP record transformation failed")
            return FlextResult[TransformedRecord].fail(
                f"Record transformation failed: {e}",
            )

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
        record: SingerRecord,
        object_classes: list[str],
    ) -> FlextResult[LdapAttributeMap]:
        """Prepare attributes for LDAP entry creation."""
        try:
            attributes: dict[str, list[str]] = {}

            attributes["objectClass"] = object_classes

            for key, value in record.items():
                if value is not None:
                    attributes[key] = self._to_ldap_values(value)

            return FlextResult[LdapAttributeMap].ok(
                attributes,
            )

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP attribute preparation failed")
            return FlextResult[LdapAttributeMap].fail(
                f"Attribute preparation failed: {e}",
            )

    def _to_ldap_values(self, value: SingerValue) -> list[str]:
        """Normalize incoming Singer value to LDAP list values."""
        match value:
            case list() as values:
                return [str(item) for item in values]
            case _:
                return [str(value)]


class LDAPSchemaMapper:
    """Map Singer schema definitions to LDAP attribute syntaxes."""

    @override
    def __init__(self) -> None:
        """Initialize LDAP schema mapper."""

    def map_singer_schema_to_ldap(
        self,
        schema: SingerSchemaDefinition
        | Mapping[str, Mapping[str, Mapping[str, str] | str]],
        object_class: str = "inetOrgPerson",
    ) -> FlextResult[Mapping[str, str]]:
        """Map Singer schema to LDAP attribute definitions."""
        try:
            ldap_attributes: dict[str, str] = {}
            schema_model = SingerSchemaDefinition.model_validate(schema)

            for prop_name, prop_def in schema_model.properties.items():
                ldap_name = self._normalize_attribute_name(prop_name)
                ldap_type_result = self._map_singer_type_to_ldap(
                    prop_def,
                    object_class,
                )
                ldap_attributes[ldap_name] = (
                    ldap_type_result.data
                    if ldap_type_result.is_success and ldap_type_result.data
                    else "DirectoryString"
                )

            return FlextResult[Mapping[str, str]].ok(ldap_attributes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP schema mapping failed")
            return FlextResult[Mapping[str, str]].fail(
                f"Schema mapping failed: {e}",
            )

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
        prop_def: SingerPropertyDefinition,
        _object_class: str,
    ) -> FlextResult[str]:
        """Map Singer property definition to LDAP attribute syntax."""
        try:
            prop_type = prop_def.type
            prop_format = prop_def.format

            if prop_format in {"date-time", "date"}:
                return FlextResult[str].ok("GeneralizedTime")
            if prop_type in {"integer", "number"}:
                return FlextResult[str].ok("Integer")
            if prop_type == "boolean":
                return FlextResult[str].ok("Boolean")
            if prop_type in {"object", "array"}:
                return FlextResult[str].ok("OctetString")
            return FlextResult[str].ok("DirectoryString")

        except (RuntimeError, ValueError, TypeError) as e:
            logger.warning(f"LDAP type mapping failed: {e}")
            return FlextResult[str].ok("DirectoryString")


class LDAPEntryManager:
    """Manage entry DN, class selection, and modify payloads."""

    @override
    def __init__(self) -> None:
        """Initialize LDAP entry manager."""

    def generate_dn(
        self,
        record: SingerRecord,
        base_dn: str,
        rdn_attribute: str = "cn",
    ) -> FlextResult[str]:
        """Generate Distinguished Name for LDAP entry."""
        try:
            rdn_value = record.get(rdn_attribute)
            if not rdn_value:
                alternatives = ["commonName", "cn", "uid", "name", "id"]
                for alt in alternatives:
                    if record.get(alt):
                        rdn_value = record[alt]
                        rdn_attribute = alt
                        break

                if not rdn_value:
                    return FlextResult[str].fail(
                        f"No value found for RDN attribute: {rdn_attribute}",
                    )

            escaped_value = self._escape_dn_value(str(rdn_value))
            dn = f"{rdn_attribute}={escaped_value},{base_dn}"

            return FlextResult[str].ok(dn)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("DN generation failed")
            return FlextResult[str].fail(f"DN generation failed: {e}")

    def _escape_dn_value(self, value: str) -> str:
        """Escape special characters in DN values."""
        special_chars = {
            ",": "\\,",
            "+": "\\+",
            '"': "\\'",
            "\\": "\\",
            "<": "\\<",
            ">": "\\>",
            ";": "\\;",
            "=": "\\=",
        }

        escaped = value
        for char, escaped_char in special_chars.items():
            escaped = escaped.replace(char, escaped_char)

        if escaped.startswith(" "):
            escaped = "\\ " + escaped[1:]
        if escaped.endswith(" "):
            escaped = escaped[:-1] + "\\ "

        return escaped

    def determine_object_classes(
        self,
        record: SingerRecord,
        stream_name: str,
    ) -> FlextResult[list[str]]:
        """Determine appropriate object classes for LDAP entry."""
        try:
            object_classes = ["top"]  # All entries must have 'top'

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
                object_classes.extend(
                    ["person", "organizationalPerson", "inetOrgPerson"],
                )

            return FlextResult[list[str]].ok(object_classes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Object class determination failed")
            return FlextResult[list[str]].fail(
                f"Object class determination failed: {e}",
            )

    def validate_entry_attributes(
        self,
        attributes: LdapAttributeMap,
        object_classes: list[str],
    ) -> FlextResult[bool]:
        """Validate LDAP entry attributes against object class requirements."""
        try:
            required_attrs = set()

            for obj_class in object_classes:
                if obj_class in {"person", "organizationalPerson", "inetOrgPerson"}:
                    required_attrs.update({"cn", "sn"})
                elif obj_class == "groupOfNames":
                    required_attrs.add("member")
                elif obj_class == "organizationalUnit":
                    required_attrs.add("ou")

            missing_attrs = required_attrs - set(attributes.keys())
            if missing_attrs:
                return FlextResult[bool].fail(
                    f"Missing required attributes: {missing_attrs}",
                )

            return FlextResult[bool].ok(value=True)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Entry validation failed")
            return FlextResult[bool].fail(f"Entry validation failed: {e}")

    def prepare_modify_changes(
        self,
        current_attrs: Mapping[str, str | list[str] | None],
        new_attrs: Mapping[str, str | list[str] | None],
    ) -> FlextResult[ModifyMap]:
        """Prepare modification changes for LDAP entry."""
        try:
            changes: ModifyMap = {}

            all_attrs = set(current_attrs.keys()) | set(new_attrs.keys())

            for attr in all_attrs:
                current_value = current_attrs.get(attr)
                new_value = new_attrs.get(attr)

                if current_value != new_value:
                    if new_value is None:
                        changes[attr] = [("MODIFY_DELETE", [])]
                    elif current_value is None:
                        values = self._normalize_modify_values(new_value)
                        changes[attr] = [("MODIFY_ADD", values)]
                    else:
                        values = self._normalize_modify_values(new_value)
                        changes[attr] = [("MODIFY_REPLACE", values)]

            return FlextResult[ModifyMap].ok(changes)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Modify changes preparation failed")
            return FlextResult[ModifyMap].fail(
                f"Modify changes preparation failed: {e}",
            )

    def _normalize_modify_values(self, value: str | list[str] | None) -> list[str]:
        """Normalize modify payload values to LDAP list representation."""
        match value:
            case list() as values:
                return values
            case str() as text:
                return [text]
            case _:
                return []
