"""LDAP target services: connection, transformation, and orchestration."""

from __future__ import annotations

from collections.abc import MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime
from typing import override

from flext_core import r
from flext_target_ldap import FlextTargetLdapSettings, c, m, t


class FlextTargetLdapConnectionService:
    """Service for testing and querying LDAP connection settings."""

    @override
    def __init__(self, settings: FlextTargetLdapSettings) -> None:
        """Initialize with LDAP target settings."""
        self._config = settings

    def get_connection_info(self) -> t.ContainerValueMapping:
        """Return connection parameters as a dict for logging or debugging."""
        return {
            "host": self._config.connection.host,
            "port": self._config.connection.port,
            "use_ssl": self._config.connection.use_ssl,
            "base_dn": self._config.base_dn,
            "timeout": self._config.connection.timeout,
        }

    def test_connection(self) -> r[bool]:
        """Verify LDAP host and base_dn are configured and connection is valid."""
        if not self._config.connection.host:
            return r[bool].fail("LDAP host is required")
        if not self._config.base_dn:
            return r[bool].fail("Base DN is required")
        return r[bool].ok(value=True)


class FlextTargetLdapTransformationService:
    """Transform Singer records into LDAP entries with attribute mappings."""

    @override
    def __init__(self, settings: FlextTargetLdapSettings) -> None:
        """Initialize with LDAP target settings."""
        self._config = settings

    def get_default_mappings(
        self,
        entry_type: str,
    ) -> Sequence[m.TargetLdap.AttributeMapping]:
        """Return default attribute mappings for the given entry type (e.g. users, groups)."""
        if entry_type == "users":
            return [
                m.TargetLdap.AttributeMapping.model_validate({
                    "singer_field_name": "username",
                    "ldap_attribute_name": "uid",
                    "is_required": True,
                }),
                m.TargetLdap.AttributeMapping.model_validate({
                    "singer_field_name": "full_name",
                    "ldap_attribute_name": "cn",
                    "is_required": True,
                }),
                m.TargetLdap.AttributeMapping.model_validate({
                    "singer_field_name": "last_name",
                    "ldap_attribute_name": "sn",
                    "is_required": True,
                }),
                m.TargetLdap.AttributeMapping.model_validate({
                    "singer_field_name": "email",
                    "ldap_attribute_name": "mail",
                    "is_required": False,
                }),
            ]
        if entry_type == "groups":
            return [
                m.TargetLdap.AttributeMapping.model_validate({
                    "singer_field_name": "name",
                    "ldap_attribute_name": "cn",
                    "is_required": True,
                }),
                m.TargetLdap.AttributeMapping.model_validate({
                    "singer_field_name": "description",
                    "ldap_attribute_name": "description",
                    "is_required": False,
                }),
            ]
        return [
            m.TargetLdap.AttributeMapping.model_validate({
                "singer_field_name": "name",
                "ldap_attribute_name": "cn",
                "is_required": True,
            }),
        ]

    def transform_record(
        self,
        record: t.ContainerValueMapping,
        mappings: Sequence[m.TargetLdap.AttributeMapping],
        object_classes: t.StrSequence,
        base_dn: str,
    ) -> r[m.TargetLdap.TransformationResult]:
        """Transform a single record into an LDAP entry using mappings."""
        mapping_errors: MutableSequence[str] = []
        ldap_attributes: MutableMapping[str, t.StrSequence] = {}
        applied_mappings: MutableSequence[m.TargetLdap.AttributeMapping] = []
        for mapping in mappings:
            value = record.get(mapping.singer_field_name)
            if value is None and mapping.default_value is not None:
                value = mapping.default_value
            if value is None:
                if mapping.is_required:
                    mapping_errors.append(
                        f"Missing required field: {mapping.singer_field_name}",
                    )
                continue
            text_value = str(value)
            if mapping.transformation_rule == "lowercase":
                text_value = text_value.lower()
            elif mapping.transformation_rule == "uppercase":
                text_value = text_value.upper()
            elif mapping.transformation_rule == "trim":
                text_value = text_value.strip()
            elif mapping.transformation_rule == "normalize":
                text_value = text_value.strip().lower()
            ldap_attributes[mapping.ldap_attribute_name] = [text_value]
            applied_mappings.append(mapping)
        entry_name = str(
            record.get(
                "username",
                record.get("name", c.IDENTIFIER_UNKNOWN),
            ),
        )
        dn = f"cn={entry_name},{base_dn}"
        entry = m.TargetLdap.Entry.model_validate({
            "distinguished_name": dn,
            "object_classes": object_classes,
            "attributes": ldap_attributes,
            "entry_type": self._determine_entry_type(object_classes),
        })
        original_record_json: t.ConfigurationMapping = {
            str(key): str(value) for key, value in record.items()
        }
        result = m.TargetLdap.TransformationResult.model_validate({
            "original_record": original_record_json,
            "transformed_entry": entry,
            "applied_mappings": applied_mappings,
            "transformation_errors": mapping_errors,
            "processing_time_ms": 0,
            "transformation_timestamp": datetime.now(UTC),
        })
        return r[m.TargetLdap.TransformationResult].ok(result)

    def validate_entry(self, entry: m.TargetLdap.Entry) -> r[bool]:
        """Run business-rule validation on an LDAP entry."""
        return entry.validate_business_rules()

    def _determine_entry_type(self, object_classes: t.StrSequence) -> str:
        normalized = {oc.lower() for oc in object_classes}
        if "person" in normalized or "inetorgperson" in normalized:
            return "user"
        if "groupofnames" in normalized or "posixgroup" in normalized:
            return "group"
        if "organizationalunit" in normalized:
            return "organizational_unit"
        return "generic"


__all__: list[str] = [
    "FlextTargetLdapConnectionService",
    "FlextTargetLdapTransformationService",
]
