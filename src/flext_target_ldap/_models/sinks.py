"""LDAP sinks for Singer target using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import override

from flext_ldap import r, u

from flext_target_ldap import c, p, t
from flext_target_ldap._models.processing_result import (
    FlextTargetLdapProcessingCounters,
)
from flext_target_ldap._utilities.client import FlextTargetLdapClient


class FlextTargetLdapModelsSinks:
    """Canonical namespace owner."""

    logger = u.fetch_logger(__name__)

    class FlextTargetLdapModels:
        """Models namespace for the LDAP target family."""

        class FlextTargetLdapSink:
            """Base Sink class for Singer protocol compatibility."""

            def __init__(
                self,
                target: (
                    FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapTarget
                ),
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
                self,
                _record: t.TargetLdap.RecordPayload,
                context: t.TargetLdap.RecordPayload,
            ) -> p.Result[bool]:
                """Process a record using the target.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                return u.guard_result(
                    lambda: self.target.process_record(_record, context),
                    catch=c.Meltano.SINGER_SAFE_EXCEPTIONS,
                    op_name="Record processing",
                )

        class FlextTargetLdapTarget:
            """Base Target class for Singer protocol compatibility."""

            settings: t.TargetLdap.SettingsPayload

            def __init__(
                self,
                *,
                settings: t.TargetLdap.SettingsPayload | None = None,
                **_kwargs: t.Scalar,
            ) -> None:
                """Initialize target with configuration."""
                self.settings = settings or {}

            @staticmethod
            def process_record(
                _record: t.TargetLdap.RecordPayload,
                context: t.TargetLdap.RecordPayload,
            ) -> p.Result[bool]:
                """Process a record with the concrete target runtime.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                context_keys = tuple(sorted(key for key in context))
                return r[bool].fail(
                    f"Target does not implement process_record "
                    f"for context keys: {context_keys}",
                )

        class FlextTargetLdapProcessingResult(FlextTargetLdapProcessingCounters):
            """Result of LDAP processing operations - mutable for perf tracking."""

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
                target: (
                    FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapTarget
                ),
                stream_name: str,
                schema: t.TargetLdap.SchemaPayload,
                key_properties: t.StrSequence,
            ) -> None:
                """Initialize LDAP sink."""
                super().__init__(target, stream_name, schema, key_properties)
                self._target = target
                self.client: FlextTargetLdapClient | None = None
                result_models = FlextTargetLdapModelsSinks.FlextTargetLdapModels
                self._processing_result = (
                    result_models.FlextTargetLdapProcessingResult()
                )

            @staticmethod
            def extract_attribute_mapping(
                settings: t.TargetLdap.SettingsPayload,
            ) -> t.StrMapping:
                """Extract the configured Singer-to-LDAP attribute mapping.

                Returns:
                    The resulting ``t.StrMapping``.

                Raises:
                    TypeError: If the configured mapping is not a Mapping.
                """
                raw = settings.get(c.TargetLdap.KEY_ATTRIBUTE_MAPPING, {})
                if isinstance(raw, Mapping):
                    return {key: str(value) for key, value in raw.items()}
                msg = (
                    f"Expected Mapping for 'attribute_mapping', "
                    f"got {type(raw).__name__}: {raw!r}"
                )
                raise TypeError(msg)

            @staticmethod
            def extract_object_classes(
                settings: t.TargetLdap.SettingsPayload,
            ) -> t.StrSequence:
                """Extract configured object classes.

                Returns:
                    The resulting ``t.StrSequence``.
                """
                raw = settings.get(c.TargetLdap.KEY_OBJECT_CLASSES)
                if isinstance(raw, list):
                    return [str(object_class) for object_class in raw if object_class]
                if isinstance(raw, str):
                    return [raw]
                return [c.TargetLdap.DEFAULT_OBJECT_CLASS]

            def _apply_attribute_mapping(
                self,
                attributes: dict[str, list[str]],
                record: t.TargetLdap.RecordPayload,
                field_mapping: t.MappingKV[str, str],
            ) -> dict[str, list[str]]:
                """Apply the fixed and configured field mappings onto ``attributes``.

                Returns:
                    The resulting ``dict[str, list[str]]``.
                """
                for singer_field, ldap_attr in field_mapping.items():
                    value = record.get(singer_field)
                    if value is not None:
                        attributes[ldap_attr] = FlextTargetLdapClient.to_str_values(
                            value,
                        )
                mapping = self.extract_attribute_mapping(
                    self._target.settings,
                )
                for singer_field, mapped_attr in mapping.items():
                    value = record.get(singer_field)
                    if value is not None:
                        attributes[mapped_attr] = FlextTargetLdapClient.to_str_values(
                            value,
                        )
                return attributes

            @staticmethod
            def build_attributes(
                _record: t.TargetLdap.RecordPayload,
            ) -> p.Result[t.Ldap.OperationAttributes]:
                """Build LDAP attributes from record. Override in subclasses.

                Returns:
                    The resulting ``p.Result[t.Ldap.OperationAttributes]``.
                """
                return r[t.Ldap.OperationAttributes].fail(
                    "build_attributes must be implemented in subclass",
                )

            def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
                """Build distinguished name from record. Override in subclasses.

                Returns:
                    The resulting ``p.Result[str]``.
                """
                dn = record.get(c.TargetLdap.KEY_DN)
                if isinstance(dn, str) and dn:
                    return r[str].ok(dn)
                base_dn = self._target.settings.get(
                    c.TargetLdap.KEY_BASE_DN,
                    c.TargetLdap.DEFAULT_BASE_DN,
                )
                entry_id = (
                    record.get(c.TargetLdap.KEY_ID)
                    or record.get(c.TargetLdap.KEY_CN)
                    or record.get(c.TargetLdap.KEY_NAME)
                )
                if isinstance(entry_id, str) and entry_id:
                    return r[str].ok(f"{c.TargetLdap.KEY_CN}={entry_id},{base_dn}")
                return r[str].fail(
                    "build_dn must be implemented in subclass: "
                    "No ID or name found for generic entry",
                )

            def resolve_object_classes(
                self,
                record: t.TargetLdap.RecordPayload,
            ) -> t.StrSequence:
                """Get object classes for entry.

                Returns:
                    The resulting ``t.StrSequence``.
                """
                record_classes = record.get(c.TargetLdap.KEY_OBJECT_CLASSES)
                if isinstance(record_classes, list):
                    return [
                        str(object_class)
                        for object_class in record_classes
                        if object_class
                    ]
                if isinstance(record_classes, str):
                    return [record_classes]
                configured_classes = self._target.settings.get(
                    c.TargetLdap.KEY_GENERIC_OBJECT_CLASSES,
                )
                if configured_classes is None:
                    return [c.TargetLdap.DEFAULT_OBJECT_CLASS]
                classes: t.StrSequence = self.extract_object_classes({
                    c.TargetLdap.KEY_OBJECT_CLASSES: configured_classes,
                })
                return classes

            def process_batch(self, context: t.TargetLdap.RecordPayload) -> None:
                """Process a batch of records.

                Raises:
                    RuntimeError: If Cannot process batch.
                """
                setup_result: p.Result[FlextTargetLdapClient] = self.setup_client()
                if not setup_result.success:
                    msg = f"Cannot process batch: {setup_result.error or ''}"
                    FlextTargetLdapModelsSinks.logger.error(msg)
                    raise RuntimeError(msg)
                try:
                    records_raw = context.get(c.TargetLdap.KEY_RECORDS, [])
                    records: list[t.TargetLdap.RecordPayload] = []
                    if isinstance(records_raw, list):
                        records.extend(
                            item for item in records_raw if isinstance(item, dict)
                        )
                    FlextTargetLdapModelsSinks.logger.info(
                        f"Processing batch of {len(records)} records "
                        f"for stream: {self.stream_name}",
                    )
                    for record in records:
                        if isinstance(record, dict):
                            normalized_record: t.TargetLdap.MutableRecordPayload = {}
                            for k, v in record.items():
                                normalized_record[k] = v
                            self.process_record(normalized_record, context)
                    FlextTargetLdapModelsSinks.logger.info(
                        f"Batch processing completed. "
                        f"Success: {self._processing_result.success_count}, "
                        f"Errors: {self._processing_result.error_count}",
                    )
                finally:
                    self.teardown_client()

            @override
            def process_record(
                self,
                _record: t.TargetLdap.RecordPayload,
                context: t.TargetLdap.RecordPayload,
            ) -> p.Result[bool]:
                """Process a single record. Override in subclasses.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                if not self.client:
                    self._processing_result.add_error("LDAP client not initialized")
                    return r[bool].fail("LDAP client not initialized")
                try:
                    FlextTargetLdapModelsSinks.logger.debug(
                        f"Processing record: {_record!r}",
                    )
                    self._processing_result.add_success()
                    return r[bool].ok(value=True)
                except c.EXC_RUNTIME_TYPE as e:
                    error_msg: str = f"Error processing record: {e}"
                    FlextTargetLdapModelsSinks.logger.exception(error_msg)
                    self._processing_result.add_error(error_msg)
                    return r[bool].fail(error_msg)

            def setup_client(self) -> p.Result[FlextTargetLdapClient]:
                """Set up LDAP client connection.

                Returns:
                    The resulting ``p.Result[FlextTargetLdapClient]``.
                """
                try:
                    connection_config = {
                        c.TargetLdap.KEY_HOST: self._target.settings.get(
                            c.TargetLdap.KEY_HOST,
                            c.TargetLdap.DEFAULT_HOST,
                        ),
                        c.TargetLdap.KEY_PORT: self._target.settings.get(
                            c.TargetLdap.KEY_PORT,
                            c.Ldap.PORT,
                        ),
                        c.TargetLdap.KEY_USE_SSL: self._target.settings.get(
                            c.TargetLdap.KEY_USE_SSL,
                            c.Ldap.DEFAULT_USE_SSL,
                        ),
                        c.TargetLdap.KEY_BIND_DN: self._target.settings.get(
                            c.TargetLdap.KEY_BIND_DN,
                            c.TargetLdap.DEFAULT_BIND_DN,
                        ),
                        c.TargetLdap.KEY_BIND_CREDENTIAL: self._target.settings.get(
                            c.TargetLdap.KEY_BIND_CREDENTIAL,
                            c.TargetLdap.DEFAULT_BIND_PASSWORD,
                        ),
                        c.TargetLdap.KEY_TIMEOUT: self._target.settings.get(
                            c.TargetLdap.KEY_TIMEOUT,
                            c.Ldap.TIMEOUT,
                        ),
                    }
                    self.client = FlextTargetLdapClient(connection_config)
                    connect_result = self.client.connect()
                    if not connect_result.success:
                        return r[FlextTargetLdapClient].fail_op(
                            "LDAP connection",
                            connect_result.error,
                        )
                    FlextTargetLdapModelsSinks.logger.info(
                        f"LDAP client setup successful for stream: {self.stream_name}",
                    )
                    return r[FlextTargetLdapClient].ok(self.client)
                except c.EXC_RUNTIME_TYPE as e:
                    error_msg: str = f"LDAP client setup failed: {e}"
                    FlextTargetLdapModelsSinks.logger.exception(error_msg)
                    return r[FlextTargetLdapClient].fail(error_msg)

            def teardown_client(self) -> None:
                """Teardown LDAP client connection."""
                if self.client:
                    _ = self.client.disconnect()
                    self.client = None
                    FlextTargetLdapModelsSinks.logger.info(
                        f"LDAP client disconnected for stream: {self.stream_name}",
                    )

            def _persist_typed_entry(
                self,
                *,
                label: str,
                dn: str,
                attributes: dict[str, list[str]],
                default_object_classes: t.StrSequence,
            ) -> p.Result[bool]:
                """Split object classes from attributes and persist one entry.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                object_classes = FlextTargetLdapClient.to_str_values(
                    attributes.get("objectClass", list(default_object_classes)),
                )
                attributes_dict: dict[str, list[str]] = {
                    key: FlextTargetLdapClient.to_str_values(value)
                    for key, value in attributes.items()
                    if key != "objectClass"
                }
                return self._persist_entry(
                    label=label,
                    dn=dn,
                    attributes_dict=attributes_dict,
                    object_classes=object_classes,
                )

            def _persist_entry(
                self,
                *,
                label: str,
                dn: str,
                attributes_dict: dict[str, list[str]],
                object_classes: t.StrSequence | None = None,
            ) -> p.Result[bool]:
                """Add an LDAP entry; on conflict modify it when configured to do so.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                if not self.client:
                    self._processing_result.add_error("LDAP client not initialized")
                    return r[bool].fail("LDAP client not initialized")
                add_result: p.Result[bool] = self.client.add_entry(
                    dn,
                    attributes_dict,
                    object_classes,
                )
                if add_result.success:
                    self._processing_result.add_success()
                    FlextTargetLdapModelsSinks.logger.debug(
                        "%s entry added successfully: %s",
                        label.capitalize(),
                        dn,
                    )
                    return r[bool].ok(value=True)
                if self._target.settings.get("update_existing_entries", False):
                    modify_result: p.Result[bool] = self.client.modify_entry(
                        dn,
                        attributes_dict,
                    )
                    if modify_result.success:
                        self._processing_result.add_success()
                        FlextTargetLdapModelsSinks.logger.debug(
                            "%s entry modified successfully: %s",
                            label.capitalize(),
                            dn,
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
                """Validate LDAP entry before writing.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
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

            @override
            @staticmethod
            def build_attributes(
                _record: t.TargetLdap.RecordPayload,
            ) -> p.Result[t.Ldap.OperationAttributes]:
                """Build LDAP attributes for user entry.

                Returns:
                    The resulting ``p.Result[t.Ldap.OperationAttributes]``.
                """
                attrs: dict[str, list[str]] = {}
                field_map = {
                    "emails": "mail",
                    "phone_numbers": "telephoneNumber",
                }
                for k, v in _record.items():
                    target_key = field_map.get(k, k)
                    attrs[target_key] = FlextTargetLdapClient.to_str_values(v)
                return r[t.Ldap.OperationAttributes].ok(attrs)

            @override
            def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
                """Build DN for user entry.

                Returns:
                    The resulting ``p.Result[str]``.
                """
                rdn_attr = str(self._target.settings.get("user_rdn_attribute", "uid"))
                uid = record.get(rdn_attr)
                if not uid:
                    return r[str].fail(f"No value found for RDN attribute '{rdn_attr}'")
                base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
                return r[str].ok(f"{rdn_attr}={uid},{base_dn}")

            def build_user_attributes(
                self,
                record: t.TargetLdap.RecordPayload,
            ) -> dict[str, list[str]]:
                """Build LDAP attributes for user entry.

                Returns:
                    The resulting ``dict[str, list[str]]``.
                """
                configured_object_classes = self._target.settings.get(
                    "object_classes",
                    ["inetOrgPerson", "person"],
                )
                object_classes = list(
                    self.extract_object_classes({
                        "object_classes": configured_object_classes,
                    }),
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
                return self._apply_attribute_mapping(attributes, record, field_mapping)

            @override
            def resolve_object_classes(
                self,
                record: t.TargetLdap.RecordPayload,
            ) -> t.StrSequence:
                """Get object classes for user entry.

                Returns:
                    The resulting ``t.StrSequence``.
                """
                configured = self._target.settings.get("users_object_classes")
                if configured is None:
                    return ["inetOrgPerson", "organizationalPerson", "person", "top"]
                classes: t.StrSequence = self.extract_object_classes({
                    "object_classes": configured,
                })
                return classes

            @override
            def process_record(
                self,
                _record: t.TargetLdap.RecordPayload,
                context: t.TargetLdap.RecordPayload,
            ) -> p.Result[bool]:
                """Process a user record.

                Returns:
                    The resulting ``p.Result[bool]``.
                """

                def _run_process_record() -> p.Result[bool]:
                    username = (
                        _record.get("username")
                        or _record.get("uid")
                        or _record.get("cn")
                    )
                    if not username:
                        self._processing_result.add_error("No username found in record")
                        return r[bool].fail("No username found in record")
                    base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
                    attributes = self.build_user_attributes(_record)
                    return self._persist_typed_entry(
                        label="user",
                        dn=f"uid={username},{base_dn}",
                        attributes=attributes,
                        default_object_classes=("inetOrgPerson", "person"),
                    )

                try:
                    return _run_process_record()
                except c.EXC_RUNTIME_TYPE as e:
                    error_msg: str = f"Error processing user record: {e}"
                    FlextTargetLdapModelsSinks.logger.exception(error_msg)
                    self._processing_result.add_error(error_msg)
                    return r[bool].fail(error_msg)

        class FlextTargetLdapGroupsSink(FlextTargetLdapBaseSink):
            """LDAP sink for group entries."""

            @override
            @staticmethod
            def build_attributes(
                _record: t.TargetLdap.RecordPayload,
            ) -> p.Result[t.Ldap.OperationAttributes]:
                """Build LDAP attributes for group entry.

                Returns:
                    The resulting ``p.Result[t.Ldap.OperationAttributes]``.
                """
                attrs: dict[str, list[str]] = {}
                field_map = {"members": "member"}
                for k, v in _record.items():
                    target_key = field_map.get(k, k)
                    attrs[target_key] = FlextTargetLdapClient.to_str_values(v)
                return r[t.Ldap.OperationAttributes].ok(attrs)

            @override
            def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
                """Build DN for group entry.

                Returns:
                    The resulting ``p.Result[str]``.
                """
                rdn_attr = str(self._target.settings.get("group_rdn_attribute", "cn"))
                cn = record.get(rdn_attr)
                if not cn:
                    return r[str].fail(f"No value found for RDN attribute '{rdn_attr}'")
                base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
                return r[str].ok(f"{rdn_attr}={cn},{base_dn}")

            @override
            def resolve_object_classes(
                self,
                record: t.TargetLdap.RecordPayload,
            ) -> t.StrSequence:
                """Get object classes for group entry.

                Returns:
                    The resulting ``t.StrSequence``.
                """
                configured = self._target.settings.get("groups_object_classes")
                if configured is not None:
                    classes: t.StrSequence = self.extract_object_classes({
                        "object_classes": configured,
                    })
                    return classes
                return ["groupOfNames", "top"]

            @override
            def process_record(
                self,
                _record: t.TargetLdap.RecordPayload,
                context: t.TargetLdap.RecordPayload,
            ) -> p.Result[bool]:
                """Process a group record.

                Returns:
                    The resulting ``p.Result[bool]``.
                """

                def _run_process_record() -> p.Result[bool]:
                    group_name = _record.get("name") or _record.get("cn")
                    if not group_name:
                        self._processing_result.add_error(
                            "No group name found in record",
                        )
                        return r[bool].fail("No group name found in record")
                    base_dn = self._target.settings.get("base_dn", "dc=example,dc=com")
                    attributes = self._build_group_attributes(_record)
                    return self._persist_typed_entry(
                        label="group",
                        dn=f"cn={group_name},{base_dn}",
                        attributes=attributes,
                        default_object_classes=("groupOfNames",),
                    )

                try:
                    return _run_process_record()
                except c.EXC_RUNTIME_TYPE as e:
                    error_msg: str = f"Error processing group record: {e}"
                    FlextTargetLdapModelsSinks.logger.exception(error_msg)
                    self._processing_result.add_error(error_msg)
                    return r[bool].fail(error_msg)

            def _build_group_attributes(
                self,
                record: t.TargetLdap.RecordPayload,
            ) -> dict[str, list[str]]:
                """Build LDAP attributes for group entry.

                Returns:
                    The resulting ``dict[str, list[str]]``.
                """
                configured_object_classes = self._target.settings.get(
                    "group_object_classes",
                    ["groupOfNames"],
                )
                object_classes = list(
                    self.extract_object_classes({
                        "object_classes": configured_object_classes,
                    }),
                )
                if "groupOfNames" not in object_classes:
                    object_classes.append("groupOfNames")
                attributes: dict[str, list[str]] = {"objectClass": object_classes}
                field_mapping = {
                    "name": "cn",
                    "description": "description",
                    "members": "member",
                }
                return self._apply_attribute_mapping(attributes, record, field_mapping)

        class FlextTargetLdapOrganizationalUnitsSink(FlextTargetLdapBaseSink):
            """LDAP sink for organizational unit entries."""

            @override
            def process_record(
                self,
                _record: t.TargetLdap.RecordPayload,
                context: t.TargetLdap.RecordPayload,
            ) -> p.Result[bool]:
                """Process an organizational unit record.

                Returns:
                    The resulting ``p.Result[bool]``.
                """

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
                    FlextTargetLdapModelsSinks.logger.exception(error_msg)
                    self._processing_result.add_error(error_msg)
                    return r[bool].fail(error_msg)

            def _build_ou_attributes(
                self,
                record: t.TargetLdap.RecordPayload,
            ) -> dict[str, list[str]]:
                """Build LDAP attributes for OU entry.

                Returns:
                    The resulting ``dict[str, list[str]]``.
                """
                configured_object_classes = self._target.settings.get(
                    "object_classes",
                    ["organizationalUnit"],
                )
                object_classes = list(
                    self.extract_object_classes({
                        "object_classes": configured_object_classes,
                    }),
                )
                if "organizationalUnit" not in object_classes:
                    object_classes.append("organizationalUnit")
                attributes: dict[str, list[str]] = {"objectClass": object_classes}
                field_mapping = {"name": "ou", "description": "description"}
                return self._apply_attribute_mapping(attributes, record, field_mapping)

    FlextTargetLdapSink = FlextTargetLdapModels.FlextTargetLdapSink

    FlextTargetLdapTarget = FlextTargetLdapModels.FlextTargetLdapTarget

    FlextTargetLdapProcessingResult = (
        FlextTargetLdapModels.FlextTargetLdapProcessingResult
    )

    FlextTargetLdapBaseSink = FlextTargetLdapModels.FlextTargetLdapBaseSink

    FlextTargetLdapUsersSink = FlextTargetLdapModels.FlextTargetLdapUsersSink

    FlextTargetLdapGroupsSink = FlextTargetLdapModels.FlextTargetLdapGroupsSink

    FlextTargetLdapOrganizationalUnitsSink = (
        FlextTargetLdapModels.FlextTargetLdapOrganizationalUnitsSink
    )


__all__: t.StrSequence = ("FlextTargetLdapModelsSinks",)
