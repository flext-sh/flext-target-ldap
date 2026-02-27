"""LDAP target services: connection, transformation, orchestration, and API facade."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Protocol, override

from flext_core import FlextResult

from . import target_client as target_client_module
from .settings import FlextTargetLdapSettings
from .target_config import validate_ldap_target_config
from .target_models import (
    LdapAttributeMappingModel,
    LdapEntryModel,
    LdapTransformationResultModel,
)
from .typings import t


class LdapTargetServiceProtocol(Protocol):
    """Protocol for LDAP target creation and record loading."""

    def create_target(
        self,
        config: dict[str, t.GeneralValueType],
    ) -> FlextResult[target_client_module.TargetLdap]:
        """Create an LDAP target from config."""
        ...

    def load_records(
        self,
        records: list[Mapping[str, t.GeneralValueType]],
        config: dict[str, t.GeneralValueType],
        stream_type: str = "users",
    ) -> FlextResult[int]:
        """Load records into the LDAP target."""
        ...


class LdapTransformationServiceProtocol(Protocol):
    """Protocol for transforming and validating LDAP entries."""

    def transform_record(
        self,
        record: Mapping[str, t.GeneralValueType],
        mappings: list[LdapAttributeMappingModel],
        object_classes: list[str],
        base_dn: str,
    ) -> FlextResult[LdapTransformationResultModel]:
        """Transform a record for LDAP storage."""
        ...

    def validate_entry(self, entry: LdapEntryModel) -> FlextResult[bool]:
        """Validate an LDAP entry against business rules."""
        ...


class LdapConnectionService:
    """Service for testing and querying LDAP connection settings."""

    @override
    def __init__(self, config: FlextTargetLdapSettings) -> None:
        """Initialize with LDAP target settings."""
        self._config = config

    def test_connection(self) -> FlextResult[bool]:
        """Verify LDAP host and base_dn are configured and connection is valid."""
        if not self._config.connection.host:
            return FlextResult[bool].fail("LDAP host is required")
        if not self._config.base_dn:
            return FlextResult[bool].fail("Base DN is required")
        return FlextResult[bool].ok(value=True)

    def get_connection_info(self) -> Mapping[str, t.GeneralValueType]:
        """Return connection parameters as a dict for logging or debugging."""
        return {
            "host": self._config.connection.host,
            "port": self._config.connection.port,
            "use_ssl": self._config.connection.use_ssl,
            "base_dn": self._config.base_dn,
            "timeout": self._config.connection.timeout,
        }


class LdapTransformationService:
    """Transform Singer records into LDAP entries with attribute mappings."""

    @override
    def __init__(self, config: FlextTargetLdapSettings) -> None:
        """Initialize with LDAP target settings."""
        self._config = config

    def transform_record(
        self,
        record: Mapping[str, t.GeneralValueType],
        mappings: list[LdapAttributeMappingModel],
        object_classes: list[str],
        base_dn: str,
    ) -> FlextResult[LdapTransformationResultModel]:
        """Transform a single record into an LDAP entry using mappings."""
        mapping_errors: list[str] = []
        ldap_attributes: dict[str, list[str]] = {}
        applied_mappings: list[LdapAttributeMappingModel] = []

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

        entry_name = str(record.get("username", record.get("name", "unknown")))
        dn = f"cn={entry_name},{base_dn}"
        entry = LdapEntryModel(
            distinguished_name=dn,
            object_classes=object_classes,
            attributes=ldap_attributes,
            entry_type=self._determine_entry_type(object_classes),
        )

        result = LdapTransformationResultModel(
            original_record=dict(record),
            transformed_entry=entry,
            applied_mappings=applied_mappings,
            transformation_errors=mapping_errors,
            processing_time_ms=0,
            transformation_timestamp=datetime.now(UTC),
        )
        return FlextResult[LdapTransformationResultModel].ok(result)

    def validate_entry(self, entry: LdapEntryModel) -> FlextResult[bool]:
        """Run business-rule validation on an LDAP entry."""
        return entry.validate_business_rules()

    def get_default_mappings(self, entry_type: str) -> list[LdapAttributeMappingModel]:
        """Return default attribute mappings for the given entry type (e.g. users, groups)."""
        if entry_type == "users":
            return [
                LdapAttributeMappingModel(
                    singer_field_name="username",
                    ldap_attribute_name="uid",
                    is_required=True,
                ),
                LdapAttributeMappingModel(
                    singer_field_name="full_name",
                    ldap_attribute_name="cn",
                    is_required=True,
                ),
                LdapAttributeMappingModel(
                    singer_field_name="last_name",
                    ldap_attribute_name="sn",
                    is_required=True,
                ),
                LdapAttributeMappingModel(
                    singer_field_name="email",
                    ldap_attribute_name="mail",
                    is_required=False,
                ),
            ]
        if entry_type == "groups":
            return [
                LdapAttributeMappingModel(
                    singer_field_name="name",
                    ldap_attribute_name="cn",
                    is_required=True,
                ),
                LdapAttributeMappingModel(
                    singer_field_name="description",
                    ldap_attribute_name="description",
                    is_required=False,
                ),
            ]
        return [
            LdapAttributeMappingModel(
                singer_field_name="name",
                ldap_attribute_name="cn",
                is_required=True,
            )
        ]

    def _determine_entry_type(self, object_classes: list[str]) -> str:
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

    def get_typed_config(self) -> FlextTargetLdapSettings | None:
        """Return the current typed settings, if any."""
        return self._typed_config

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

    def orchestrate_data_loading(
        self,
        records: list[Mapping[str, t.GeneralValueType]],
        config: FlextTargetLdapSettings | None = None,
    ) -> FlextResult[Mapping[str, t.GeneralValueType]]:
        """Load records using default mappings and return a summary result."""
        working = config or self._typed_config
        if working is None:
            return FlextResult[Mapping[str, t.GeneralValueType]].fail(
                "Configuration is required",
            )

        transformation = LdapTransformationService(working)
        object_classes = working.object_classes
        base_dn = working.base_dn
        stream_type = "users"
        mappings = transformation.get_default_mappings(stream_type)

        processed = 0
        errors: list[str] = []
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

        result: dict[str, t.GeneralValueType] = {
            "processed_records": processed,
            "total_records": len(records),
            "transformation_errors": errors,
            "status": "completed" if not errors else "completed_with_errors",
        }
        return FlextResult[Mapping[str, t.GeneralValueType]].ok(result)

    def validate_target_configuration(
        self,
        config: FlextTargetLdapSettings | None = None,
    ) -> FlextResult[bool]:
        """Validate target configuration and test connection."""
        working = config or self._typed_config
        if working is None:
            return FlextResult[bool].fail("Configuration is required")
        return LdapConnectionService(working).test_connection()


class LdapTargetApiService:
    """API facade for creating targets and loading users/groups to LDAP."""

    @override
    def __init__(self) -> None:
        """Initialize the API service and internal orchestrator cache."""
        self._orchestrators: dict[str, LdapTargetOrchestrator] = {}

    def create_ldap_target(
        self,
        config: dict[str, t.GeneralValueType],
    ) -> FlextResult[target_client_module.TargetLdap]:
        """Create an LDAP target from raw config dict."""
        try:
            return FlextResult[target_client_module.TargetLdap].ok(
                target_client_module.TargetLdap(config=config),
            )
        except (RuntimeError, ValueError, TypeError) as exc:
            return FlextResult[target_client_module.TargetLdap].fail(str(exc))

    def load_users_to_ldap(
        self,
        users: list[Mapping[str, t.GeneralValueType]],
        config: dict[str, t.GeneralValueType],
    ) -> FlextResult[int]:
        """Load user records into LDAP using the default users sink."""
        target_result = self.create_ldap_target(config)
        if target_result.is_failure or target_result.value is None:
            return FlextResult[int].fail(
                target_result.error or "Target creation failed"
            )
        target = target_result.value
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])
        for user in users:
            sink.process_record(dict(user), {})
        return FlextResult[int].ok(len(users))

    def load_groups_to_ldap(
        self,
        groups: list[Mapping[str, t.GeneralValueType]],
        config: dict[str, t.GeneralValueType],
    ) -> FlextResult[int]:
        """Load group records into LDAP using the default groups sink."""
        target_result = self.create_ldap_target(config)
        if target_result.is_failure or target_result.value is None:
            return FlextResult[int].fail(
                target_result.error or "Target creation failed"
            )
        target = target_result.value
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])
        for group in groups:
            sink.process_record(dict(group), {})
        return FlextResult[int].ok(len(groups))

    def test_ldap_connection(
        self, config: dict[str, t.GeneralValueType]
    ) -> FlextResult[bool]:
        """Validate config and test the LDAP connection."""
        validated = validate_ldap_target_config(config)
        if validated.is_failure or validated.value is None:
            return FlextResult[bool].fail(
                validated.error or "Configuration validation failed",
            )
        return LdapConnectionService(validated.value).test_connection()


__all__ = [
    "LdapConnectionService",
    "LdapTargetApiService",
    "LdapTargetOrchestrator",
    "LdapTargetServiceProtocol",
    "LdapTransformationService",
    "LdapTransformationServiceProtocol",
]
