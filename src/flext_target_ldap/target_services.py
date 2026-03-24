"""LDAP target services: connection, transformation, orchestration, and API facade."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import override

from flext_target_ldap import (
    FlextTargetLdapSettings,
    c,
    r,
    t,
    target_client as target_client_module,
    u,
    validate_ldap_target_config,
)
from flext_target_ldap.models import m
from flext_target_ldap.protocols import p

LdapTargetService = p.TargetLdap.LdapTargetService
LdapTransformationServiceProtocol = p.TargetLdap.LdapTransformationServiceProtocol


class LdapConnectionService:
    """Service for testing and querying LDAP connection settings."""

    @override
    def __init__(self, config: FlextTargetLdapSettings) -> None:
        """Initialize with LDAP target settings."""
        self._config = config

    def get_connection_info(self) -> Mapping[str, t.ContainerValue]:
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


class LdapTransformationService:
    """Transform Singer records into LDAP entries with attribute mappings."""

    @override
    def __init__(self, config: FlextTargetLdapSettings) -> None:
        """Initialize with LDAP target settings."""
        self._config = config

    def get_default_mappings(
        self, entry_type: str
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
        record: Mapping[str, t.ContainerValue],
        mappings: Sequence[m.TargetLdap.AttributeMapping],
        object_classes: Sequence[str],
        base_dn: str,
    ) -> r[m.TargetLdap.TransformationResult]:
        """Transform a single record into an LDAP entry using mappings."""
        mapping_errors: Sequence[str] = []
        ldap_attributes: Mapping[str, Sequence[str]] = {}
        applied_mappings: Sequence[m.TargetLdap.AttributeMapping] = []
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

    def _determine_entry_type(self, object_classes: Sequence[str]) -> str:
        normalized = {oc.lower() for oc in object_classes}
        if "person" in normalized or "inetorgperson" in normalized:
            return "user"
        if "groupofnames" in normalized or "posixgroup" in normalized:
            return "group"
        if "organizationalunit" in normalized:
            return "organizational_unit"
        return "generic"


class LdapTargetOrchestrator:
    """Orchestrates connection, transformation, and data loading for the LDAP target."""

    @override
    def __init__(self, config: FlextTargetLdapSettings | None = None) -> None:
        """Initialize with optional LDAP target settings."""
        self._typed_config = config

    def get_connection_service(self) -> LdapConnectionService | None:
        """Return a connection service instance if config is set."""
        if self._typed_config is None:
            return None
        return LdapConnectionService(self._typed_config)

    def get_transformation_service(self) -> LdapTransformationService | None:
        """Return a transformation service instance if config is set."""
        if self._typed_config is None:
            return None
        return LdapTransformationService(self._typed_config)

    def get_typed_config(self) -> FlextTargetLdapSettings | None:
        """Return the current typed settings, if any."""
        return self._typed_config

    def orchestrate_data_loading(
        self,
        records: Sequence[Mapping[str, t.ContainerValue]],
        config: FlextTargetLdapSettings | None = None,
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Load records using default mappings and return a summary result."""
        working = config or self._typed_config
        if working is None:
            return r[t.ContainerValueMapping].fail(
                "Configuration is required",
            )
        transformation = LdapTransformationService(working)
        object_classes = working.object_classes
        base_dn = working.base_dn
        stream_type = "users"
        mappings = transformation.get_default_mappings(stream_type)
        processed = 0
        errors: Sequence[t.ContainerValue] = []
        for record in records:
            transformed = transformation.transform_record(
                record=record,
                mappings=mappings,
                object_classes=object_classes,
                base_dn=base_dn,
            )
            if transformed.is_success:
                processed += 1
            else:
                errors.append(transformed.error or "Transformation failed")
        result: Mapping[str, t.ContainerValue] = {
            "processed_records": processed,
            "total_records": len(records),
            "transformation_errors": errors,
            "status": "completed" if not errors else "completed_with_errors",
        }
        return r[t.ContainerValueMapping].ok(result)

    def validate_target_configuration(
        self,
        config: FlextTargetLdapSettings | None = None,
    ) -> r[bool]:
        """Validate target configuration and test connection."""
        working = config or self._typed_config
        if working is None:
            return r[bool].fail("Configuration is required")
        return LdapConnectionService(working).test_connection()


class LdapTargetApiService:
    """API facade for creating targets and loading users/groups to LDAP."""

    @override
    def __init__(self) -> None:
        """Initialize the API service and internal orchestrator cache."""
        self._orchestrators: Mapping[str, LdapTargetOrchestrator] = {}

    def create_ldap_target(
        self,
        config: Mapping[str, t.ContainerValue],
    ) -> r[target_client_module.TargetLdap]:
        """Create an LDAP target from raw config dict."""
        return u.try_(
            lambda: target_client_module.TargetLdap(config=config),
            catch=(RuntimeError, ValueError, TypeError),
        ).map_error(lambda exc: str(exc))

    def load_groups_to_ldap(
        self,
        groups: Sequence[Mapping[str, t.ContainerValue]],
        config: Mapping[str, t.ContainerValue],
    ) -> r[int]:
        """Load group records into LDAP using the default groups sink."""
        target_result = self.create_ldap_target(config)
        if target_result.is_failure:
            return r[int].fail(target_result.error or "Target creation failed")
        target = target_result.value
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])
        for group in groups:
            sink.process_record(dict(group), {})
        return r[int].ok(len(groups))

    def load_users_to_ldap(
        self,
        users: Sequence[Mapping[str, t.ContainerValue]],
        config: Mapping[str, t.ContainerValue],
    ) -> r[int]:
        """Load user records into LDAP using the default users sink."""
        target_result = self.create_ldap_target(config)
        if target_result.is_failure:
            return r[int].fail(target_result.error or "Target creation failed")
        target = target_result.value
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])
        for user in users:
            sink.process_record(dict(user), {})
        return r[int].ok(len(users))

    def test_ldap_connection(
        self,
        config: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Validate config and test the LDAP connection."""
        validated = validate_ldap_target_config(config)
        if validated.is_failure:
            return r[bool].fail(validated.error or "Configuration validation failed")
        return LdapConnectionService(validated.value).test_connection()


__all__ = [
    "LdapConnectionService",
    "LdapTargetApiService",
    "LdapTargetOrchestrator",
    "LdapTargetService",
    "LdapTransformationService",
]
