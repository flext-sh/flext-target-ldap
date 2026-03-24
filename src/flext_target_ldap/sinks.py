"""LDAP sinks for Singer target using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import ClassVar, TypeIs, override

from flext_core import FlextLogger, r

from flext_target_ldap import (
    FlextTargetLdapLdapClient,
    FlextTargetLdapProcessingCounters,
    c,
    t,
)


class FlextTargetLdapSink:
    """Base Sink class for Singer protocol compatibility."""

    @override
    def __init__(
        self,
        target: FlextTargetLdapTarget,
        stream_name: str,
        schema: Mapping[str, t.ContainerValue],
        key_properties: t.StrSequence,
    ) -> None:
        """Initialize sink with Singer protocol parameters."""
        self.target = target
        self.stream_name = stream_name
        self.schema = schema
        self.key_properties = key_properties

    def process_record(
        self,
        _record: Mapping[str, t.ContainerValue],
        _context: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Process a record using the target."""
        try:
            process_record = getattr(self.target, "process_record", None)
            if callable(process_record):
                result = process_record(_record, _context)
                if isinstance(result, r):
                    if result.is_success:
                        return r[bool].ok(value=True)
                    return r[bool].fail(result.error or "Target rejected record")
                if isinstance(result, bool):
                    if result:
                        return r[bool].ok(value=True)
                    return r[bool].fail("Target rejected record")
            process = getattr(self.target, "process", None)
            if callable(process):
                result = process(self.stream_name, _record, _context)
                if isinstance(result, r):
                    if result.is_success:
                        return r[bool].ok(value=True)
                    return r[bool].fail(result.error or "Target rejected record")
                if isinstance(result, bool):
                    if result:
                        return r[bool].ok(value=True)
                    return r[bool].fail("Target rejected record")
            return r[bool].fail(
                "Target does not provide process_record/process handlers",
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            return r[bool].fail(f"Record processing failed: {e}")


class FlextTargetLdapTarget:
    """Base Target class for Singer protocol compatibility."""

    @override
    def __init__(
        self,
        config: Mapping[str, t.ContainerValue],
        **kwargs: t.Scalar,
    ) -> None:
        """Initialize target with configuration."""
        self.config: Mapping[str, t.ContainerValue] = config


logger = FlextLogger(__name__)


def _is_container_list(
    value: t.ContainerValue | None,
) -> TypeIs[Sequence[t.ContainerValue]]:
    return isinstance(value, list)


def _container_mapping_from_value(
    value: t.ContainerValue,
) -> Mapping[str, t.ContainerValue]:
    if isinstance(value, dict):
        return {str(k): v for k, v in value.items()}
    return {}


class FlextTargetLdapProcessingResult(FlextTargetLdapProcessingCounters):
    """Result of LDAP processing operations - mutable for performance tracking."""

    @override
    def __init__(self) -> None:
        """Initialize processing result counters."""
        self.processed_count: int = 0
        self.success_count: int = 0
        self.error_count: int = 0
        self.errors: MutableSequence[str] = []


class FlextTargetLdapBaseSink(FlextTargetLdapSink):
    """Base LDAP sink with common functionality."""

    @override
    def __init__(
        self,
        target: FlextTargetLdapTarget,
        stream_name: str,
        schema: Mapping[str, t.ContainerValue],
        key_properties: t.StrSequence,
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        self._target = target
        self.client: FlextTargetLdapLdapClient | None = None
        self._client: FlextTargetLdapLdapClient | None = None
        self._processing_result: FlextTargetLdapProcessingResult = (
            FlextTargetLdapProcessingResult()
        )

    def build_attributes(
        self,
        _record: Mapping[str, t.ContainerValue],
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Build LDAP attributes from record. Override in subclasses."""
        return r[t.ContainerValueMapping].fail(
            "build_attributes must be implemented in subclass",
        )

    def build_dn(self, record: Mapping[str, t.ContainerValue]) -> r[str]:
        """Build distinguished name from record. Override in subclasses."""
        dn = record.get("dn")
        if isinstance(dn, str) and dn:
            return r[str].ok(dn)
        base_dn = self._target.config.get("base_dn", "dc=example,dc=com")
        entry_id = record.get("id") or record.get("cn") or record.get("name")
        if isinstance(entry_id, str) and entry_id:
            return r[str].ok(f"cn={entry_id},{base_dn}")
        return r[str].fail(
            "build_dn must be implemented in subclass: No ID or name found for generic entry",
        )

    def get_object_classes(
        self,
        record: Mapping[str, t.ContainerValue],
    ) -> t.StrSequence:
        """Get t.NormalizedValue classes for entry."""
        record_classes = record.get("object_classes")
        if _is_container_list(record_classes):
            return [str(c) for c in record_classes]
        if isinstance(record_classes, str):
            return [record_classes]
        configured_classes = self._target.config.get("generic_object_classes")
        if _is_container_list(configured_classes):
            return [str(c) for c in configured_classes]
        return ["top"]

    def get_processing_result(self) -> FlextTargetLdapProcessingResult:
        """Get processing results."""
        return self._processing_result

    def process_batch(self, _context: Mapping[str, t.ContainerValue]) -> None:
        """Process a batch of records."""
        setup_result: r[FlextTargetLdapLdapClient] = self.setup_client()
        if not setup_result.is_success:
            logger.error(f"Cannot process batch: {setup_result.error or ''}")
            return
        try:
            records_raw = _context.get("records", [])
            records: MutableSequence[Mapping[str, t.ContainerValue]] = []
            if isinstance(records_raw, list):
                records.extend(item for item in records_raw if isinstance(item, dict))
            logger.info(
                f"Processing batch of {len(records)} records for stream: {self.stream_name}",
            )
            for record in records:
                if isinstance(record, dict):
                    normalized_record: MutableMapping[str, t.ContainerValue] = {}
                    for k, v in record.items():
                        normalized_record[str(k)] = v
                    self.process_record(normalized_record, _context)
            logger.info(
                f"Batch processing completed. Success: {self._processing_result.success_count}, Errors: {self._processing_result.error_count}",
            )
        finally:
            self.teardown_client()

    @override
    def process_record(
        self,
        _record: Mapping[str, t.ContainerValue],
        _context: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Process a single record. Override in subclasses."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return r[bool].fail("LDAP client not initialized")
        try:
            logger.debug(f"Processing record: {_record!r}")
            self._processing_result.add_success()
            return r[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def setup_client(self) -> r[FlextTargetLdapLdapClient]:
        """Set up LDAP client connection."""
        try:
            connection_config = {
                "host": self._target.config.get("host", "localhost"),
                "port": self._target.config.get(
                    "port",
                    c.Ldap.ConnectionDefaults.PORT,
                ),
                "use_ssl": self._target.config.get("use_ssl", False),
                "bind_dn": self._target.config.get("bind_dn", ""),
                "password": self._target.config.get("password", ""),
                "timeout": self._target.config.get("timeout", 30),
            }
            self.client = FlextTargetLdapLdapClient(connection_config)
            connect_result: r[str] = self.client.connect()
            if not connect_result.is_success:
                return r[FlextTargetLdapLdapClient].fail(
                    f"LDAP connection failed: {connect_result.error}",
                )
            logger.info(f"LDAP client setup successful for stream: {self.stream_name}")
            return r[FlextTargetLdapLdapClient].ok(self.client)
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"LDAP client setup failed: {e}"
            logger.exception(error_msg)
            return r[FlextTargetLdapLdapClient].fail(error_msg)

    def teardown_client(self) -> None:
        """Teardown LDAP client connection."""
        if self.client:
            _ = self.client.disconnect()
            self.client = None
            logger.info(f"LDAP client disconnected for stream: {self.stream_name}")

    def validate_entry(
        self,
        dn: str,
        attributes: Mapping[str, t.ContainerValue],
        object_classes: t.StrSequence,
    ) -> r[bool]:
        """Validate LDAP entry before writing."""
        if not dn:
            return r[bool].fail("DN cannot be empty")
        if not attributes:
            return r[bool].fail("Attributes cannot be empty")
        if not object_classes:
            return r[bool].fail("Object classes cannot be empty")
        if self._client is not None:
            validate_dn = getattr(self._client, "validate_dn", None)
            if callable(validate_dn):
                dn_result = validate_dn(dn)
                if isinstance(dn_result, r) and dn_result.is_failure:
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
        self,
        _record: Mapping[str, t.ContainerValue],
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Build LDAP attributes for user entry."""
        attrs: MutableMapping[str, t.ContainerValue] = {}
        for k, v in _record.items():
            target_key = self._USER_FIELD_MAP.get(k, k)
            if _is_container_list(v):
                attrs[target_key] = [str(i) for i in v]
            else:
                attrs[target_key] = [str(v)]
        return r[t.ContainerValueMapping].ok(attrs)

    @override
    def build_dn(self, record: Mapping[str, t.ContainerValue]) -> r[str]:
        """Build DN for user entry."""
        rdn_attr = str(self._target.config.get("user_rdn_attribute", "uid"))
        uid = record.get(rdn_attr)
        if not uid:
            return r[str].fail(f"No value found for RDN attribute '{rdn_attr}'")
        base_dn = self._target.config.get("base_dn", "dc=example,dc=com")
        return r[str].ok(f"{rdn_attr}={uid},{base_dn}")

    def build_user_attributes(
        self,
        record: Mapping[str, t.ContainerValue],
    ) -> MutableMapping[str, t.ContainerValue]:
        """Build LDAP attributes for user entry."""
        object_classes = self._target.config.get(
            "object_classes",
            ["inetOrgPerson", "person"],
        )
        attributes: MutableMapping[str, t.ContainerValue] = {
            "objectClass": list(object_classes)
            if _is_container_list(object_classes)
            else ["inetOrgPerson", "person"],
        }
        obj_classes = attributes.get("objectClass")
        if _is_container_list(obj_classes):
            obj_classes_mut: MutableSequence[t.ContainerValue] = list(obj_classes)
            if "person" not in obj_classes_mut:
                obj_classes_mut.append("person")
            if "inetOrgPerson" not in obj_classes_mut:
                obj_classes_mut.append("inetOrgPerson")
            attributes["objectClass"] = obj_classes_mut
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
                attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping = _container_mapping_from_value(mapping_val)
        mapping: MutableMapping[str, str] = {}
        for k, v in raw_mapping.items():
            match v:
                case str():
                    mapping[k] = str(v)
                case _:
                    pass
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[mapped_attr] = [str(value)]
        return attributes

    @override
    def get_object_classes(
        self,
        record: Mapping[str, t.ContainerValue],
    ) -> t.StrSequence:
        """Get t.NormalizedValue classes for user entry."""
        configured = self._target.config.get("users_object_classes")
        if _is_container_list(configured):
            return [str(c) for c in configured]
        return ["inetOrgPerson", "organizationalPerson", "person", "top"]

    @override
    def process_record(
        self,
        _record: Mapping[str, t.ContainerValue],
        _context: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Process a user record."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return r[bool].fail("LDAP client not initialized")
        try:
            username = (
                _record.get("username") or _record.get("uid") or _record.get("cn")
            )
            if not username:
                self._processing_result.add_error("No username found in record")
                return r[bool].fail("No username found in record")
            base_dn = self._target.config.get("base_dn", "dc=example,dc=com")
            user_dn = f"uid={username},{base_dn}"
            attributes = self.build_user_attributes(_record)
            object_classes_raw = attributes.get(
                "objectClass",
                ["inetOrgPerson", "person"],
            )
            object_classes: t.StrSequence = (
                [str(oc) for oc in object_classes_raw]
                if _is_container_list(object_classes_raw)
                else ["inetOrgPerson", "person"]
            )
            attributes_dict: MutableMapping[str, t.ContainerValue] = {}
            for k, v in attributes.items():
                if k != "objectClass":
                    if _is_container_list(v):
                        attributes_dict[k] = [str(i) for i in v]
                    else:
                        attributes_dict[k] = [str(v)]
            add_result: r[bool] = self.client.add_entry(
                user_dn,
                attributes_dict,
                object_classes,
            )
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("User entry added successfully: %s", user_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result: r[bool] = self.client.modify_entry(
                    user_dn,
                    attributes_dict,
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("User entry modified successfully: %s", user_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify user {user_dn}: {modify_result.error}",
                )
                return r[bool].fail(
                    f"Failed to modify user {user_dn}: {modify_result.error}",
                )
            self._processing_result.add_error(
                f"Failed to add user {user_dn}: {add_result.error}",
            )
            return r[bool].fail(f"Failed to add user {user_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing user record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)


class FlextTargetLdapGroupsSink(FlextTargetLdapBaseSink):
    """LDAP sink for group entries."""

    @override
    def build_attributes(
        self,
        _record: Mapping[str, t.ContainerValue],
    ) -> r[Mapping[str, t.ContainerValue]]:
        """Build LDAP attributes for group entry."""
        attrs: MutableMapping[str, t.ContainerValue] = {}
        field_map = {"members": "member"}
        for k, v in _record.items():
            target_key = field_map.get(k, k)
            if _is_container_list(v):
                attrs[target_key] = [str(i) for i in v]
            else:
                attrs[target_key] = [str(v)]
        return r[t.ContainerValueMapping].ok(attrs)

    @override
    def build_dn(self, record: Mapping[str, t.ContainerValue]) -> r[str]:
        """Build DN for group entry."""
        rdn_attr = str(self._target.config.get("group_rdn_attribute", "cn"))
        cn = record.get(rdn_attr)
        if not cn:
            return r[str].fail(f"No value found for RDN attribute '{rdn_attr}'")
        base_dn = self._target.config.get("base_dn", "dc=example,dc=com")
        return r[str].ok(f"{rdn_attr}={cn},{base_dn}")

    @override
    def get_object_classes(
        self,
        record: Mapping[str, t.ContainerValue],
    ) -> t.StrSequence:
        """Get t.NormalizedValue classes for group entry."""
        configured = self._target.config.get("groups_object_classes")
        if _is_container_list(configured):
            return [str(c) for c in configured]
        return ["groupOfNames", "top"]

    @override
    def process_record(
        self,
        _record: Mapping[str, t.ContainerValue],
        _context: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Process a group record."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return r[bool].fail("LDAP client not initialized")
        try:
            group_name = _record.get("name") or _record.get("cn")
            if not group_name:
                self._processing_result.add_error("No group name found in record")
                return r[bool].fail("No group name found in record")
            group_dn = f"cn={group_name},{self._target.config.get('base_dn', 'dc=example,dc=com')}"
            attributes = self._build_group_attributes(_record)
            object_classes_raw = attributes.get("objectClass", ["groupOfNames"])
            object_classes: t.StrSequence = (
                [str(oc) for oc in object_classes_raw]
                if _is_container_list(object_classes_raw)
                else ["groupOfNames"]
            )
            attributes_dict: MutableMapping[str, t.ContainerValue] = {}
            for k, v in attributes.items():
                if k != "objectClass":
                    if _is_container_list(v):
                        attributes_dict[k] = [i for i in v]  # noqa: C416
                    else:
                        attributes_dict[k] = v
            add_result: r[bool] = self.client.add_entry(
                group_dn,
                attributes_dict,
                object_classes,
            )
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("Group entry added successfully: %s", group_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result: r[bool] = self.client.modify_entry(
                    group_dn,
                    attributes_dict,
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("Group entry modified successfully: %s", group_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify group {group_dn}: {modify_result.error}",
                )
                return r[bool].fail(
                    f"Failed to modify group {group_dn}: {modify_result.error}",
                )
            self._processing_result.add_error(
                f"Failed to add group {group_dn}: {add_result.error}",
            )
            return r[bool].fail(f"Failed to add group {group_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing group record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_group_attributes(
        self,
        record: Mapping[str, t.ContainerValue],
    ) -> MutableMapping[str, t.ContainerValue]:
        """Build LDAP attributes for group entry."""
        object_classes = self._target.config.get(
            "group_object_classes",
            ["groupOfNames"],
        )
        attributes: MutableMapping[str, t.ContainerValue] = {
            "objectClass": list(object_classes)
            if _is_container_list(object_classes)
            else ["groupOfNames"],
        }
        obj_classes = attributes.get("objectClass")
        if _is_container_list(obj_classes) and "groupOfNames" not in obj_classes:
            obj_classes_mut: MutableSequence[t.ContainerValue] = list(obj_classes)
            obj_classes_mut.append("groupOfNames")
            attributes["objectClass"] = obj_classes_mut
        field_mapping = {
            "name": "cn",
            "description": "description",
            "members": "member",
        }
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if _is_container_list(value):
                    attributes[ldap_attr] = value
                else:
                    attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping = _container_mapping_from_value(mapping_val)
        mapping: MutableMapping[str, str] = {}
        for k, v in raw_mapping.items():
            match v:
                case str():
                    mapping[k] = str(v)
                case _:
                    pass
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if _is_container_list(value):
                    attributes[mapped_attr] = value
                else:
                    attributes[mapped_attr] = [str(value)]
        return attributes


class FlextTargetLdapOrganizationalUnitsSink(FlextTargetLdapBaseSink):
    """LDAP sink for organizational unit entries."""

    @override
    def process_record(
        self,
        _record: Mapping[str, t.ContainerValue],
        _context: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Process an organizational unit record."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return r[bool].fail("LDAP client not initialized")
        try:
            ou_name = _record.get("name") or _record.get("ou")
            if not ou_name:
                self._processing_result.add_error("No OU name found in record")
                return r[bool].fail("No OU name found in record")
            ou_dn = f"ou={ou_name},{self._target.config.get('base_dn', 'dc=example,dc=com')}"
            attributes = self._build_ou_attributes(_record)
            attributes_dict: MutableMapping[str, t.ContainerValue] = {}
            for k, v in attributes.items():
                if _is_container_list(v):
                    attributes_dict[k] = [i for i in v]  # noqa: C416
                else:
                    attributes_dict[k] = v
            add_result: r[bool] = self.client.add_entry(ou_dn, attributes_dict)
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("OU entry added successfully: %s", ou_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result: r[bool] = self.client.modify_entry(
                    ou_dn,
                    attributes_dict,
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("OU entry modified successfully: %s", ou_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify OU {ou_dn}: {modify_result.error}",
                )
                return r[bool].fail(
                    f"Failed to modify OU {ou_dn}: {modify_result.error}",
                )
            self._processing_result.add_error(
                f"Failed to add OU {ou_dn}: {add_result.error}",
            )
            return r[bool].fail(f"Failed to add OU {ou_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing OU record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_ou_attributes(
        self,
        record: Mapping[str, t.ContainerValue],
    ) -> MutableMapping[str, t.ContainerValue]:
        """Build LDAP attributes for OU entry."""
        default_classes = self._target.config.get(
            "object_classes",
            ["organizationalUnit"],
        )
        attributes: MutableMapping[str, t.ContainerValue] = {
            "objectClass": list(default_classes)
            if _is_container_list(default_classes)
            else ["organizationalUnit"],
        }
        obj_classes = attributes.get("objectClass")
        if _is_container_list(obj_classes) and "organizationalUnit" not in obj_classes:
            obj_classes_mut: MutableSequence[t.ContainerValue] = list(obj_classes)
            obj_classes_mut.append("organizationalUnit")
            attributes["objectClass"] = obj_classes_mut
        field_mapping = {"name": "ou", "description": "description"}
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping = _container_mapping_from_value(mapping_val)
        mapping: MutableMapping[str, str] = {}
        for k, v in raw_mapping.items():
            match v:
                case str():
                    mapping[k] = str(v)
                case _:
                    pass
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[mapped_attr] = [str(value)]
        return attributes


# Backward-compatible aliases
GroupsSink = FlextTargetLdapGroupsSink
LDAPBaseSink = FlextTargetLdapBaseSink
LDAPProcessingResult = FlextTargetLdapProcessingResult
OrganizationalUnitsSink = FlextTargetLdapOrganizationalUnitsSink
Sink = FlextTargetLdapSink
Target = FlextTargetLdapTarget
UsersSink = FlextTargetLdapUsersSink

__all__: t.StrSequence = [
    "FlextTargetLdapBaseSink",
    "FlextTargetLdapGroupsSink",
    "FlextTargetLdapOrganizationalUnitsSink",
    "FlextTargetLdapProcessingResult",
    "FlextTargetLdapSink",
    "FlextTargetLdapTarget",
    "FlextTargetLdapUsersSink",
    "GroupsSink",
    "LDAPBaseSink",
    "LDAPProcessingResult",
    "OrganizationalUnitsSink",
    "Sink",
    "Target",
    "UsersSink",
]
