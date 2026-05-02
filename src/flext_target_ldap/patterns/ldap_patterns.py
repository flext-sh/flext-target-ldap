"""LDAP pattern helpers built on flext-core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_target_ldap import c, m, p, r, t, u

logger = u.fetch_logger(__name__)


class FlextTargetLdapTypeConverter:
    """Convert Singer values to LDAP-safe string values."""

    _COMPLEX_KIND = "t.JsonValue"

    @override
    def __init__(self) -> None:
        """Initialize LDAP type converter."""

    def convert_singer_to_ldap(
        self,
        singer_type: str,
        value: t.Scalar,
    ) -> p.Result[str | None]:
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
        except c.EXC_RUNTIME_TYPE as e:
            logger.exception("Type conversion failed for %s", singer_type)
            return r[str | None].fail(f"Type conversion failed for {singer_type}: {e}")

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


class FlextTargetLdapDataTransformer:
    """Transform Singer records into LDAP-oriented records."""

    @override
    def __init__(
        self,
        type_converter: FlextTargetLdapTypeConverter | None = None,
    ) -> None:
        """Initialize LDAP data transformer."""
        self.type_converter = type_converter or FlextTargetLdapTypeConverter()

    def prepare_ldap_attributes(
        self,
        record: t.ConfigurationMapping,
        object_classes: t.StrSequence,
    ) -> p.Result[t.Ldap.OperationAttributes]:
        """Prepare attributes for LDAP entry creation."""
        try:
            attributes: t.MutableAttributeMapping = {}
            attributes["objectClass"] = list(object_classes)
            for key, value in record.items():
                attributes[key] = list(self._to_ldap_values(value))
            return r[t.Ldap.OperationAttributes].ok(attributes)
        except c.EXC_RUNTIME_TYPE as e:
            logger.exception("LDAP attribute preparation failed")
            return r[t.Ldap.OperationAttributes].fail_op("Attribute preparation", e)

    def transform_record(
        self,
        record: t.ConfigurationMapping,
        schema: m.TargetLdap.SingerSchemaDefinition
        | t.MappingKV[str, t.MappingKV[str, t.StrMapping | str]]
        | None = None,
    ) -> p.Result[t.OptionalStrMapping]:
        """Transform Singer record for LDAP storage."""
        try:
            transformed: t.MutableOptionalStrMapping = {}
            schema_model = m.TargetLdap.SingerSchemaDefinition.model_validate(
                schema or {},
            )
            for key, value in record.items():
                ldap_key = self._normalize_ldap_attribute_name(key)
                prop_def = schema_model.properties.get(key)
                singer_type = prop_def.type if prop_def is not None else "string"
                convert_result = self.type_converter.convert_singer_to_ldap(
                    singer_type,
                    value,
                )
                if convert_result.failure:
                    return r[t.OptionalStrMapping].fail(
                        f"Conversion failed for '{key}': {convert_result.error}",
                    )
                transformed[ldap_key] = convert_result.value
            return r[t.OptionalStrMapping].ok(transformed)
        except c.EXC_RUNTIME_TYPE as e:
            logger.exception("LDAP record transformation failed")
            return r[t.OptionalStrMapping].fail_op("Record transformation", e)

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


class FlextTargetLdapSchemaMapper:
    """Map Singer schema definitions to LDAP attribute syntaxes."""

    @override
    def __init__(self) -> None:
        """Initialize LDAP schema mapper."""

    def map_singer_schema_to_ldap(
        self,
        schema: m.TargetLdap.SingerSchemaDefinition
        | t.MappingKV[str, t.MappingKV[str, t.StrMapping | str]],
        object_class: str = "inetOrgPerson",
    ) -> p.Result[t.StrMapping]:
        """Map Singer schema to LDAP attribute definitions."""
        try:
            ldap_attributes: t.MutableStrMapping = {}
            schema_model = m.TargetLdap.SingerSchemaDefinition.model_validate(schema)
            for prop_name, prop_def in schema_model.properties.items():
                ldap_name = self._normalize_attribute_name(prop_name)
                ldap_type_result = self._map_singer_type_to_ldap(prop_def, object_class)
                if ldap_type_result.failure:
                    return r[t.StrMapping].fail_op(
                        f"Type mapping for '{prop_name}'",
                        ldap_type_result.error,
                    )
                mapped_type: str = ldap_type_result.value or "DirectoryString"
                ldap_attributes[ldap_name] = mapped_type
            return r[t.StrMapping].ok(ldap_attributes)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP schema mapping failed")
            return r[t.StrMapping].fail_op("Schema mapping", e)

    def _map_singer_type_to_ldap(
        self,
        prop_def: m.TargetLdap.SingerPropertyDefinition,
        _object_class: str,
    ) -> p.Result[str]:
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
            if prop_type in {"t.JsonValue", "array"}:
                return r[str].ok("OctetString")
            return r[str].ok("DirectoryString")
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP type mapping failed")
            return r[str].fail_op("LDAP type mapping", e)

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


class FlextTargetLdapEntryManager:
    """Manage entry DN, class selection, and modify payloads."""

    @override
    def __init__(self) -> None:
        """Initialize LDAP entry manager."""

    def determine_object_classes(
        self,
        record: t.ConfigurationMapping,
        stream_name: str,
    ) -> p.Result[t.StrSequence]:
        """Determine appropriate object classes for LDAP entry."""
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
            return r[t.StrSequence].fail_op("Object class determination", e)

    def generate_dn(
        self,
        record: t.ConfigurationMapping,
        base_dn: str,
        rdn_attribute: str = "cn",
    ) -> p.Result[str]:
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
            return r[str].fail_op("DN generation", e)

    def prepare_modify_changes(
        self,
        current_attrs: t.MappingKV[str, str | t.StrSequence | None],
        new_attrs: t.MappingKV[str, str | t.StrSequence | None],
    ) -> p.Result[t.Ldap.LdapModifyChanges]:
        """Prepare modification changes for LDAP entry."""
        try:
            changes: dict[str, list[tuple[c.Ldap.ModifyOperation, t.StrSequence]]] = {}
            all_attrs = set(current_attrs.keys()) | set(new_attrs.keys())
            for attr in all_attrs:
                current_value = current_attrs.get(attr)
                new_value = new_attrs.get(attr)
                if current_value != new_value:
                    if new_value is None:
                        changes[attr] = [(c.Ldap.ModifyOperation.DELETE, [])]
                    elif current_value is None:
                        values = self._normalize_modify_values(new_value)
                        changes[attr] = [(c.Ldap.ModifyOperation.ADD, values)]
                    else:
                        values = self._normalize_modify_values(new_value)
                        changes[attr] = [(c.Ldap.ModifyOperation.REPLACE, values)]
            return r[t.Ldap.LdapModifyChanges].ok(changes)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Modify changes preparation failed")
            return r[t.Ldap.LdapModifyChanges].fail_op("Modify changes preparation", e)

    def validate_entry_attributes(
        self,
        attributes: t.MappingKV[str, t.StrSequence],
        object_classes: t.StrSequence,
    ) -> p.Result[bool]:
        """Validate LDAP entry attributes against object class requirements."""
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
            return r[bool].fail_op("Entry validation", e)

    def _escape_dn_value(self, value: str) -> str:
        """Escape special characters in DN values per RFC 4514."""
        return u.Ldif.esc(value)

    def _normalize_modify_values(
        self,
        value: str | t.StrSequence | None,
    ) -> t.StrSequence:
        """Normalize modify payload values to LDAP list representation."""
        match value:
            case list() as values:
                return values
            case str() as text:
                return [text]
            case _:
                empty_values: t.MutableSequenceOf[str] = []
                return empty_values


__all__: t.StrSequence = [
    "FlextTargetLdapDataTransformer",
    "FlextTargetLdapEntryManager",
    "FlextTargetLdapSchemaMapper",
    "FlextTargetLdapTypeConverter",
]
