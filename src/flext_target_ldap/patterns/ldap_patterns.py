"""LDAP pattern helpers built on flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import override

from flext_core import FlextLogger, r, t

from flext_target_ldap.models import m

logger = FlextLogger(__name__)

# Backward-compatible aliases
SingerPropertyDefinition = m.TargetLdap.SingerPropertyDefinition
SingerSchemaDefinition = m.TargetLdap.SingerSchemaDefinition


class LDAPTypeConverter:
    """Convert Singer values to LDAP-safe string values."""

    _COMPLEX_KIND = "t.NormalizedValue"

    @override
    def __init__(self) -> None:
        """Initialize LDAP type converter."""

    def convert_singer_to_ldap(
        self,
        singer_type: str,
        value: t.Scalar,
    ) -> r[str | None]:
        """Convert Singer scalar/list/map values for LDAP persistence."""
        try:
            if singer_type in {"string", "text", "integer", "number"}:
                result = str(value)
            elif singer_type == "boolean":
                result = self._normalize_bool(value)
            elif singer_type in {self._COMPLEX_KIND, "array"}:
                result = str(value)
            else:
                result = str(value)
            return r[str | None].ok(result)
        except (RuntimeError, ValueError, TypeError):
            logger.exception("Type conversion failed for %s", singer_type)
            return r[str | None].ok(str(value))

    def _normalize_bool(self, value: t.Scalar) -> str:
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

    def prepare_ldap_attributes(
        self,
        record: t.ConfigurationMapping,
        object_classes: t.StrSequence,
    ) -> r[Mapping[str, t.StrSequence]]:
        """Prepare attributes for LDAP entry creation."""
        try:
            attributes: Mapping[str, t.StrSequence] = {}
            attributes["objectClass"] = object_classes
            for key, value in record.items():
                attributes[key] = self._to_ldap_values(value)
            return r[Mapping[str, t.StrSequence]].ok(attributes)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP attribute preparation failed")
            return r[Mapping[str, t.StrSequence]].fail(
                f"Attribute preparation failed: {e}"
            )

    def transform_record(
        self,
        record: t.ConfigurationMapping,
        schema: SingerSchemaDefinition
        | Mapping[str, Mapping[str, t.StrMapping | str]]
        | None = None,
    ) -> r[Mapping[str, str | None]]:
        """Transform Singer record for LDAP storage."""
        try:
            transformed: Mapping[str, str | None] = {}
            schema_model = SingerSchemaDefinition.model_validate(schema or {})
            for key, value in record.items():
                ldap_key = self._normalize_ldap_attribute_name(key)
                prop_def = schema_model.properties.get(key)
                singer_type = prop_def.type if prop_def is not None else "string"
                convert_result = self.type_converter.convert_singer_to_ldap(
                    singer_type,
                    value,
                )
                converted_value: str | None = convert_result.unwrap_or(str(value))
                transformed[ldap_key] = converted_value
            return r[Mapping[str, str | None]].ok(transformed)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP record transformation failed")
            return r[Mapping[str, str | None]].fail(
                f"Record transformation failed: {e}"
            )

    def _normalize_ldap_attribute_name(self, name: str) -> str:
        """Normalize attribute name for LDAP conventions."""
        normalized = name.replace("_", "").replace("-", "")
        if "_" in name or "-" in name:
            parts = name.replace("-", "_").split("_")
            normalized = parts[0].lower() + "".join(
                word.capitalize() for word in parts[1:]
            )
        else:
            normalized = name.lower()
        return normalized

    def _to_ldap_values(self, value: t.Scalar | t.ScalarList) -> t.StrSequence:
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
        schema: SingerSchemaDefinition | Mapping[str, Mapping[str, t.StrMapping | str]],
        object_class: str = "inetOrgPerson",
    ) -> r[t.StrMapping]:
        """Map Singer schema to LDAP attribute definitions."""
        try:
            ldap_attributes: t.StrMapping = {}
            schema_model = SingerSchemaDefinition.model_validate(schema)
            for prop_name, prop_def in schema_model.properties.items():
                ldap_name = self._normalize_attribute_name(prop_name)
                ldap_type_result = self._map_singer_type_to_ldap(prop_def, object_class)
                mapped_type: str = (
                    str(ldap_type_result.value)
                    if ldap_type_result.is_success and ldap_type_result.value
                    else "DirectoryString"
                )
                ldap_attributes[ldap_name] = mapped_type
            return r[t.StrMapping].ok(ldap_attributes)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP schema mapping failed")
            return r[t.StrMapping].fail(f"Schema mapping failed: {e}")

    def _map_singer_type_to_ldap(
        self,
        prop_def: SingerPropertyDefinition,
        _object_class: str,
    ) -> r[str]:
        """Map Singer property definition to LDAP attribute syntax."""
        try:
            prop_type = prop_def.type
            prop_format = prop_def.format
            if prop_format in {"date-time", "date"}:
                return r[str].ok("GeneralizedTime")
            if prop_type in {"integer", "number"}:
                return r[str].ok("Integer")
            if prop_type == "boolean":
                return r[str].ok("Boolean")
            if prop_type in {"t.NormalizedValue", "array"}:
                return r[str].ok("OctetString")
            return r[str].ok("DirectoryString")
        except (RuntimeError, ValueError, TypeError):
            logger.exception("LDAP type mapping failed")
            return r[str].ok("DirectoryString")

    def _normalize_attribute_name(self, name: str) -> str:
        """Normalize attribute name for LDAP."""
        if "_" in name or "-" in name:
            parts = name.replace("-", "_").split("_")
            normalized = parts[0].lower() + "".join(
                word.capitalize() for word in parts[1:]
            )
        else:
            normalized = name.lower()
        return normalized


class LDAPEntryManager:
    """Manage entry DN, class selection, and modify payloads."""

    @override
    def __init__(self) -> None:
        """Initialize LDAP entry manager."""

    def determine_object_classes(
        self,
        record: t.ConfigurationMapping,
        stream_name: str,
    ) -> r[t.StrSequence]:
        """Determine appropriate t.NormalizedValue classes for LDAP entry."""
        try:
            object_classes = ["top"]
            stream_lower = stream_name.lower()
            if "user" in stream_lower or "person" in stream_lower:
                if "mail" in record or "email" in record:
                    object_classes.extend([
                        "person",
                        "organizationalPerson",
                        "inetOrgPerson",
                    ])
                else:
                    object_classes.extend(["person", "organizationalPerson"])
            elif "group" in stream_lower:
                object_classes.append("groupOfNames")
            elif "ou" in stream_lower or "organizational" in stream_lower:
                object_classes.append("organizationalUnit")
            else:
                object_classes.extend([
                    "person",
                    "organizationalPerson",
                    "inetOrgPerson",
                ])
            return r[t.StrSequence].ok(object_classes)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Object class determination failed")
            return r[t.StrSequence].fail(f"Object class determination failed: {e}")

    def generate_dn(
        self,
        record: t.ConfigurationMapping,
        base_dn: str,
        rdn_attribute: str = "cn",
    ) -> r[str]:
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
                    return r[str].fail(
                        f"No value found for RDN attribute: {rdn_attribute}",
                    )
            escaped_value = self._escape_dn_value(str(rdn_value))
            dn = f"{rdn_attribute}={escaped_value},{base_dn}"
            return r[str].ok(dn)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("DN generation failed")
            return r[str].fail(f"DN generation failed: {e}")

    def prepare_modify_changes(
        self,
        current_attrs: Mapping[str, str | t.StrSequence | None],
        new_attrs: Mapping[str, str | t.StrSequence | None],
    ) -> r[Mapping[str, Sequence[tuple[str, t.StrSequence]]]]:
        """Prepare modification changes for LDAP entry."""
        try:
            changes: Mapping[str, Sequence[tuple[str, t.StrSequence]]] = {}
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
            return r[Mapping[str, Sequence[tuple[str, t.StrSequence]]]].ok(changes)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Modify changes preparation failed")
            return r[Mapping[str, Sequence[tuple[str, t.StrSequence]]]].fail(
                f"Modify changes preparation failed: {e}",
            )

    def validate_entry_attributes(
        self,
        attributes: Mapping[str, t.StrSequence],
        object_classes: t.StrSequence,
    ) -> r[bool]:
        """Validate LDAP entry attributes against t.NormalizedValue class requirements."""
        try:
            required_attrs: set[str] = set()
            for obj_class in object_classes:
                if obj_class in {"person", "organizationalPerson", "inetOrgPerson"}:
                    required_attrs.update({"cn", "sn"})
                elif obj_class == "groupOfNames":
                    required_attrs.add("member")
                elif obj_class == "organizationalUnit":
                    required_attrs.add("ou")
            missing_attrs: set[str] = required_attrs - set(attributes.keys())
            if missing_attrs:
                return r[bool].fail(f"Missing required attributes: {missing_attrs}")
            return r[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Entry validation failed")
            return r[bool].fail(f"Entry validation failed: {e}")

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

    def _normalize_modify_values(
        self, value: str | t.StrSequence | None
    ) -> t.StrSequence:
        """Normalize modify payload values to LDAP list representation."""
        match value:
            case list() as values:
                return values
            case str() as text:
                return [text]
            case _:
                return []
