"""LDAP sinks for Singer target using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar, override

from flext_target_ldap import c, p, r, t, u
from flext_target_ldap._models.processing_result import (
    FlextTargetLdapProcessingCounters,
)
from flext_target_ldap._utilities.client import FlextTargetLdapClient


class FlextTargetLdapSink:
    """Base Sink class for Singer protocol compatibility."""

    @override
    def __init__(
        self,
        target: FlextTargetLdapTarget,
        stream_name: str,
        schema: t.TargetLdap.SchemaPayload,
        key_properties: t.StrSequence,
    ) -> None:
        """Initialize sink with Singer protocol parameters."""
        self.target = target
        self.stream_name = stream_name
        self.schema = schema
        self.key_properties = key_properties

    def process_record(
        self, _record: t.TargetLdap.RecordPayload, context: t.TargetLdap.RecordPayload
    ) -> p.Result[bool]:
        """Process a record using the target."""
        return u.guard_result(
            lambda: self.target.process_record(_record, context),
            catch=c.Meltano.SINGER_SAFE_EXCEPTIONS,
            op_name="Record processing",
        )


class FlextTargetLdapTarget:
    """Base Target class for Singer protocol compatibility."""

    settings: t.TargetLdap.SettingsPayload

    @override
    def __init__(
        self, settings: t.TargetLdap.SettingsPayload, **kwargs: t.Scalar
    ) -> None:
        """Initialize target with configuration."""
        self.settings = settings

    def process_record(
        self, _record: t.TargetLdap.RecordPayload, context: t.TargetLdap.RecordPayload
    ) -> p.Result[bool]:
        """Process a record with the concrete target runtime."""
        context_keys = tuple(sorted(key for key in context))
        return r[bool].fail(
            f"Target does not implement process_record for context keys: {context_keys}"
        )


logger = u.fetch_logger(__name__)


class FlextTargetLdapProcessingResult(FlextTargetLdapProcessingCounters):
    """Result of LDAP processing operations - mutable for performance tracking."""

    @override
    def __init__(self) -> None:
        """Initialize processing result counters."""
        self.processed_count: int = 0
        self.success_count: int = 0
        self.error_count: int = 0
        self.errors: list[str] = []


class FlextTargetLdapBaseSink(FlextTargetLdapSink):
    """Base LDAP sink with common functionality."""

    @override
    def __init__(
        self,
        target: FlextTargetLdapTarget,
        stream_name: str,
        schema: t.TargetLdap.SchemaPayload,
        key_properties: t.StrSequence,
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        self._target = target
        self.client: FlextTargetLdapClient | None = None
        self._processing_result: FlextTargetLdapProcessingResult = (
            FlextTargetLdapProcessingResult()
        )

    def build_attributes(
        self, _record: t.TargetLdap.RecordPayload
    ) -> p.Result[t.Ldap.OperationAttributes]:
        """Build LDAP attributes from record. Override in subclasses."""
        return r[t.Ldap.OperationAttributes].fail(
            "build_attributes must be implemented in subclass"
        )

    def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
        """Build distinguished name from record. Override in subclasses."""
        dn = record.get(c.TargetLdap.KEY_DN)
        if isinstance(dn, str) and dn:
            return r[str].ok(dn)
        base_dn = self._target.settings.get(
            c.TargetLdap.KEY_BASE_DN, c.TargetLdap.DEFAULT_BASE_DN
        )
        entry_id = (
            record.get(c.TargetLdap.KEY_ID)
            or record.get(c.TargetLdap.KEY_CN)
            or record.get(c.TargetLdap.KEY_NAME)
        )
        if isinstance(entry_id, str) and entry_id:
            return r[str].ok(f"{c.TargetLdap.KEY_CN}={entry_id},{base_dn}")
        return r[str].fail(
            "build_dn must be implemented in subclass: No ID or name found for generic entry"
        )

    def resolve_object_classes(
        self, record: t.TargetLdap.RecordPayload
    ) -> t.StrSequence:
        """Get object classes for entry."""
        record_classes = record.get(c.TargetLdap.KEY_OBJECT_CLASSES)
        if isinstance(record_classes, list):
            return [
                str(object_class) for object_class in record_classes if object_class
            ]
        if isinstance(record_classes, str):
            return [record_classes]
        configured_classes = self._target.settings.get(
            c.TargetLdap.KEY_GENERIC_OBJECT_CLASSES
        )
        if configured_classes is None:
            return [c.TargetLdap.DEFAULT_OBJECT_CLASS]
        return u.TargetLdap.TypeConversion.extract_object_classes({
            c.TargetLdap.KEY_OBJECT_CLASSES: configured_classes
        })

    def process_batch(self, context: t.TargetLdap.RecordPayload) -> None:
        """Process a batch of records."""
        setup_result: p.Result[FlextTargetLdapClient] = self.setup_client()
        if not setup_result.success:
            logger.error(f"Cannot process batch: {setup_result.error or ''}")
            return
        try:
            records_raw = context.get(c.TargetLdap.KEY_RECORDS, [])
            records: list[t.TargetLdap.RecordPayload] = []
            if isinstance(records_raw, list):
                records.extend(item for item in records_raw if isinstance(item, dict))
            logger.info(
                f"Processing batch of {len(records)} records for stream: {self.stream_name}"
            )
            for record in records:
                if isinstance(record, dict):
                    normalized_record: t.TargetLdap.MutableRecordPayload = {}
                    for k, v in record.items():
                        normalized_record[k] = v
                    self.process_record(normalized_record, context)
            logger.info(
                f"Batch processing completed. Success: {self._processing_result.success_count}, Errors: {self._processing_result.error_count}"
            )
        finally:
            self.teardown_client()

    @override
    def process_record(
        self, _record: t.TargetLdap.RecordPayload, context: t.TargetLdap.RecordPayload
    ) -> p.Result[bool]:
        """Process a single record. Override in subclasses."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return r[bool].fail("LDAP client not initialized")
        try:
            logger.debug(f"Processing record: {_record!r}")
            self._processing_result.add_success()
            return r[bool].ok(value=True)
        except c.EXC_RUNTIME_TYPE as e:
            error_msg: str = f"Error processing record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def setup_client(self) -> p.Result[FlextTargetLdapClient]:
        """Set up LDAP client connection."""
        try:
            connection_config = {
                c.TargetLdap.KEY_HOST: self._target.settings.get(
                    c.TargetLdap.KEY_HOST, c.TargetLdap.DEFAULT_HOST
                ),
                c.TargetLdap.KEY_PORT: self._target.settings.get(
                    c.TargetLdap.KEY_PORT, c.Ldap.PORT
                ),
                c.TargetLdap.KEY_USE_SSL: self._target.settings.get(
                    c.TargetLdap.KEY_USE_SSL, c.Ldap.DEFAULT_USE_SSL
                ),
                c.TargetLdap.KEY_BIND_DN: self._target.settings.get(
                    c.TargetLdap.KEY_BIND_DN, c.TargetLdap.DEFAULT_BIND_DN
                ),
                c.TargetLdap.KEY_BIND_PASSWORD: self._target.settings.get(
                    c.TargetLdap.KEY_PASSWORD, c.TargetLdap.DEFAULT_BIND_PASSWORD
                ),
                c.TargetLdap.KEY_TIMEOUT: self._target.settings.get(
                    c.TargetLdap.KEY_TIMEOUT, c.Ldap.TIMEOUT
                ),
            }
            self.client = FlextTargetLdapClient(connection_config)
            connect_result = self.client.connect()
            if not connect_result.success:
                return r[FlextTargetLdapClient].fail_op(
                    "LDAP connection", connect_result.error
                )
            logger.info(f"LDAP client setup successful for stream: {self.stream_name}")
            return r[FlextTargetLdapClient].ok(self.client)
        except c.EXC_RUNTIME_TYPE as e:
            error_msg: str = f"LDAP client setup failed: {e}"
            logger.exception(error_msg)
            return r[FlextTargetLdapClient].fail(error_msg)

    def teardown_client(self) -> None:
        """Teardown LDAP client connection."""
        if self.client:
            _ = self.client.disconnect()
            self.client = None
            logger.info(f"LDAP client disconnected for stream: {self.stream_name}")

    def _persist_entry(
        self,
        *,
        label: str,
        dn: str,
        attributes_dict: dict[str, list[str]],
        object_classes: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Add an LDAP entry; on conflict modify it when configured to do so."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return r[bool].fail("LDAP client not initialized")
        add_result: p.Result[bool] = self.client.add_entry(
            dn, attributes_dict, object_classes
        )
        if add_result.success:
            self._processing_result.add_success()
            logger.debug("%s entry added successfully: %s", label.capitalize(), dn)
            return r[bool].ok(value=True)
        if self._target.settings.get("update_existing_entries", False):
            modify_result: p.Result[bool] = self.client.modify_entry(
                dn, attributes_dict
            )
            if modify_result.success:
                self._processing_result.add_success()
                logger.debug(
                    "%s entry modified successfully: %s", label.capitalize(), dn
                )
                return r[bool].ok(value=True)
            err = f"Failed to modify {label} {dn}: {modify_result.error}"
            self._processing_result.add_error(err)
            return r[bool].fail(err)
        err = f"Failed to add {label} {dn}: {add_result.error}"
        self._processing_result.add_error(err)
        return r[bool].fail(err)

    def validate_entry(
        self,
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence,
    ) -> p.Result[bool]:
        """Validate LDAP entry before writing."""
        if not dn:
            return r[bool].fail("DN cannot be empty")
        if not attributes:
            return r[bool].fail("Attributes cannot be empty")
        if not object_classes:
            return r[bool].fail("Object classes cannot be empty")
        validate_fn = (
            getattr(self.client, "validate_dn", None)
            if self.client is not None
            else None
        )
        if validate_fn is not None and callable(validate_fn):
            dn_result = validate_fn(dn)
            if isinstance(dn_result, r) and dn_result.failure:
                return r[bool].fail(f"Invalid DN: {dn}")
        return r[bool].ok(value=True)


class FlextTargetLdapUsersSink(FlextTargetLdapBaseSink):
    """LDAP sink for user entries."""

    _USER_FIELD_MAP: ClassVar[t.StrMapping] = {
        "emails": "mail",
        "phone_numbers": "telephoneNumber",
    }

    @override
    def build_attributes(
        self, _record: t.TargetLdap.RecordPayload
    ) -> p.Result[t.Ldap.OperationAttributes]:
        """Build LDAP attributes for user entry."""
        attrs: dict[str, list[str]] = {}
        for k, v in _record.items():
            target_key = self._USER_FIELD_MAP.get(k, k)
            attrs[target_key] = FlextTargetLdapClient.to_str_values(v)
        return r[t.Ldap.OperationAttributes].ok(attrs)

    @override
    def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
        """Build DN for user entry."""
        rdn_attr = str(self._target.settings.get("user_rdn_attribute", "uid"))
        uid = record.get(rdn_attr)
        if not uid:
            return r[str].fail(f"No value found for RDN attribute '{rdn_attr}'")
        base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
        return r[str].ok(f"{rdn_attr}={uid},{base_dn}")

    def build_user_attributes(
        self, record: t.TargetLdap.RecordPayload
    ) -> dict[str, list[str]]:
        """Build LDAP attributes for user entry."""
        configured_object_classes = self._target.settings.get(
            "object_classes", ["inetOrgPerson", "person"]
        )
        object_classes = list(
            u.TargetLdap.TypeConversion.extract_object_classes({
                "object_classes": configured_object_classes
            })
        )
        if "inetOrgPerson" not in object_classes:
            object_classes.append("inetOrgPerson")
        if "person" not in object_classes:
            object_classes.append("person")
        attributes: dict[str, list[str]] = {"objectClass": object_classes}
        field_mapping = {
            "username": "uid",
            "email": "mail",
            "first_name": "givenName",
            "last_name": "sn",
            "full_name": "cn",
            "phone": "telephoneNumber",
            "department": "departmentNumber",
            "title": "title",
        }
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = FlextTargetLdapClient.to_str_values(value)
        mapping = u.TargetLdap.TypeConversion.extract_attribute_mapping(
            self._target.settings
        )
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[mapped_attr] = FlextTargetLdapClient.to_str_values(value)
        return attributes

    @override
    def resolve_object_classes(
        self, record: t.TargetLdap.RecordPayload
    ) -> t.StrSequence:
        """Get object classes for user entry."""
        configured = self._target.settings.get("users_object_classes")
        if configured is None:
            return ["inetOrgPerson", "organizationalPerson", "person", "top"]
        return u.TargetLdap.TypeConversion.extract_object_classes({
            "object_classes": configured
        })

    @override
    def process_record(
        self, _record: t.TargetLdap.RecordPayload, context: t.TargetLdap.RecordPayload
    ) -> p.Result[bool]:
        """Process a user record."""

        def _run_process_record() -> p.Result[bool]:
            username = (
                _record.get("username") or _record.get("uid") or _record.get("cn")
            )
            if not username:
                self._processing_result.add_error("No username found in record")
                return r[bool].fail("No username found in record")
            base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
            attributes = self.build_user_attributes(_record)
            object_classes = FlextTargetLdapClient.to_str_values(
                attributes.get("objectClass", ["inetOrgPerson", "person"])
            )
            attributes_dict: dict[str, list[str]] = {
                key: FlextTargetLdapClient.to_str_values(value)
                for key, value in attributes.items()
                if key != "objectClass"
            }
            return self._persist_entry(
                label="user",
                dn=f"uid={username},{base_dn}",
                attributes_dict=attributes_dict,
                object_classes=object_classes,
            )

        try:
            return _run_process_record()
        except c.EXC_RUNTIME_TYPE as e:
            error_msg: str = f"Error processing user record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)


class FlextTargetLdapGroupsSink(FlextTargetLdapBaseSink):
    """LDAP sink for group entries."""

    @override
    def build_attributes(
        self, _record: t.TargetLdap.RecordPayload
    ) -> p.Result[t.Ldap.OperationAttributes]:
        """Build LDAP attributes for group entry."""
        attrs: dict[str, list[str]] = {}
        field_map = {"members": "member"}
        for k, v in _record.items():
            target_key = field_map.get(k, k)
            attrs[target_key] = FlextTargetLdapClient.to_str_values(v)
        return r[t.Ldap.OperationAttributes].ok(attrs)

    @override
    def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
        """Build DN for group entry."""
        rdn_attr = str(self._target.settings.get("group_rdn_attribute", "cn"))
        cn = record.get(rdn_attr)
        if not cn:
            return r[str].fail(f"No value found for RDN attribute '{rdn_attr}'")
        base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
        return r[str].ok(f"{rdn_attr}={cn},{base_dn}")

    @override
    def resolve_object_classes(
        self, record: t.TargetLdap.RecordPayload
    ) -> t.StrSequence:
        """Get object classes for group entry."""
        configured = self._target.settings.get("groups_object_classes")
        if configured is not None:
            return u.TargetLdap.TypeConversion.extract_object_classes({
                "object_classes": configured
            })
        return ["groupOfNames", "top"]

    @override
    def process_record(
        self, _record: t.TargetLdap.RecordPayload, context: t.TargetLdap.RecordPayload
    ) -> p.Result[bool]:
        """Process a group record."""

        def _run_process_record() -> p.Result[bool]:
            group_name = _record.get("name") or _record.get("cn")
            if not group_name:
                self._processing_result.add_error("No group name found in record")
                return r[bool].fail("No group name found in record")
            base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
            attributes = self._build_group_attributes(_record)
            object_classes = FlextTargetLdapClient.to_str_values(
                attributes.get("objectClass", ["groupOfNames"])
            )
            attributes_dict: dict[str, list[str]] = {
                key: FlextTargetLdapClient.to_str_values(value)
                for key, value in attributes.items()
                if key != "objectClass"
            }
            return self._persist_entry(
                label="group",
                dn=f"cn={group_name},{base_dn}",
                attributes_dict=attributes_dict,
                object_classes=object_classes,
            )

        try:
            return _run_process_record()
        except c.EXC_RUNTIME_TYPE as e:
            error_msg: str = f"Error processing group record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_group_attributes(
        self, record: t.TargetLdap.RecordPayload
    ) -> dict[str, list[str]]:
        """Build LDAP attributes for group entry."""
        configured_object_classes = self._target.settings.get(
            "group_object_classes", ["groupOfNames"]
        )
        object_classes = list(
            u.TargetLdap.TypeConversion.extract_object_classes({
                "object_classes": configured_object_classes
            })
        )
        if "groupOfNames" not in object_classes:
            object_classes.append("groupOfNames")
        attributes: dict[str, list[str]] = {"objectClass": object_classes}
        field_mapping = {
            "name": "cn",
            "description": "description",
            "members": "member",
        }
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = FlextTargetLdapClient.to_str_values(value)
        mapping = u.TargetLdap.TypeConversion.extract_attribute_mapping(
            self._target.settings
        )
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[mapped_attr] = FlextTargetLdapClient.to_str_values(value)
        return attributes


class FlextTargetLdapOrganizationalUnitsSink(FlextTargetLdapBaseSink):
    """LDAP sink for organizational unit entries."""

    @override
    def process_record(
        self, _record: t.TargetLdap.RecordPayload, context: t.TargetLdap.RecordPayload
    ) -> p.Result[bool]:
        """Process an organizational unit record."""

        def _run_process_record() -> p.Result[bool]:
            ou_name = _record.get("name") or _record.get("ou")
            if not ou_name:
                self._processing_result.add_error("No OU name found in record")
                return r[bool].fail("No OU name found in record")
            base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
            attributes = self._build_ou_attributes(_record)
            attributes_dict: dict[str, list[str]] = {
                key: FlextTargetLdapClient.to_str_values(value)
                for key, value in attributes.items()
            }
            return self._persist_entry(
                label="OU",
                dn=f"ou={ou_name},{base_dn}",
                attributes_dict=attributes_dict,
            )

        try:
            return _run_process_record()
        except c.EXC_RUNTIME_TYPE as e:
            error_msg: str = f"Error processing OU record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_ou_attributes(
        self, record: t.TargetLdap.RecordPayload
    ) -> dict[str, list[str]]:
        """Build LDAP attributes for OU entry."""
        configured_object_classes = self._target.settings.get(
            "object_classes", ["organizationalUnit"]
        )
        object_classes = list(
            u.TargetLdap.TypeConversion.extract_object_classes({
                "object_classes": configured_object_classes
            })
        )
        if "organizationalUnit" not in object_classes:
            object_classes.append("organizationalUnit")
        attributes: dict[str, list[str]] = {"objectClass": object_classes}
        field_mapping = {"name": "ou", "description": "description"}
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = FlextTargetLdapClient.to_str_values(value)
        mapping = u.TargetLdap.TypeConversion.extract_attribute_mapping(
            self._target.settings
        )
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[mapped_attr] = FlextTargetLdapClient.to_str_values(value)
        return attributes


__all__: t.StrSequence = (
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
)
