"""LDAP sinks for Singer target using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar, override

from flext_core import FlextLogger, r, t, u

from flext_target_ldap.client import LDAPClient
from flext_target_ldap.constants import c


class Sink:
    """Base Sink class for Singer protocol compatibility."""

    @override
    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: Mapping[str, t.ContainerValue],
        key_properties: list[str],
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
            if not u.is_dict_like(_record):
                return r[bool].fail("Record must be a mapping")
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
                "Target does not provide process_record/process handlers"
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


class Target:
    """Base Target class for Singer protocol compatibility."""

    @override
    def __init__(
        self, config: dict[str, t.ContainerValue], **kwargs: t.Scalar
    ) -> None:
        """Initialize target with configuration."""
        self.config: dict[str, t.ContainerValue] = config


logger = FlextLogger(__name__)


class LDAPProcessingResult:
    """Result of LDAP processing operations - mutable for performance tracking."""

    @override
    def __init__(self) -> None:
        """Initialize processing result counters."""
        self.processed_count: int = 0
        self.success_count: int = 0
        self.error_count: int = 0
        self.errors: list[str] = []

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.processed_count == 0:
            return 0.0
        return self.success_count / self.processed_count * 100.0

    def add_error(self, error_message: str) -> None:
        """Record a failed operation."""
        self.processed_count += 1
        self.error_count += 1
        self.errors.append(error_message)

    def add_success(self) -> None:
        """Record a successful operation."""
        self.processed_count += 1
        self.success_count += 1


class LDAPBaseSink(Sink):
    """Base LDAP sink with common functionality."""

    @override
    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: Mapping[str, t.ContainerValue],
        key_properties: list[str],
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        self._target = target
        self.client: LDAPClient | None = None
        self._client: LDAPClient | None = None
        self._processing_result: LDAPProcessingResult = LDAPProcessingResult()

    def build_attributes(
        self, _record: Mapping[str, t.ContainerValue]
    ) -> r[dict[str, t.ContainerValue]]:
        """Build LDAP attributes from record. Override in subclasses."""
        return r[dict[str, t.ContainerValue]].fail(
            "build_attributes must be implemented in subclass"
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
            "build_dn must be implemented in subclass: No ID or name found for generic entry"
        )

    def get_object_classes(self, record: Mapping[str, t.ContainerValue]) -> list[str]:
        """Get object classes for entry."""
        record_classes = record.get("object_classes")
        if u.is_list(record_classes):
            return [str(c) for c in record_classes]
        if isinstance(record_classes, str):
            return [record_classes]
        configured_classes = self._target.config.get("generic_object_classes")
        if u.is_list(configured_classes):
            return [str(c) for c in configured_classes]
        return ["top"]

    def get_processing_result(self) -> LDAPProcessingResult:
        """Get processing results."""
        return self._processing_result

    def process_batch(self, _context: Mapping[str, t.ContainerValue]) -> None:
        """Process a batch of records."""
        setup_result: r[LDAPClient] = self.setup_client()
        if not setup_result.is_success:
            logger.error("Cannot process batch: %s", setup_result.error or "")
            return
        try:
            records_raw = _context.get("records", [])
            records: list[t.ContainerValue] = (
                records_raw if u.is_list(records_raw) else []
            )
            logger.info(
                "Processing batch of %d records for stream: %s",
                len(records),
                self.stream_name,
            )
            for record in records:
                if u.is_dict_like(record):
                    normalized_record: dict[str, t.ContainerValue] = {}
                    for k, v in record.items():
                        normalized_record[str(k)] = v
                    self.process_record(normalized_record, _context)
            logger.info(
                "Batch processing completed. Success: %d, Errors: %d",
                self._processing_result.success_count,
                self._processing_result.error_count,
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

    def setup_client(self) -> r[LDAPClient]:
        """Set up LDAP client connection."""
        try:
            connection_config = {
                "host": self._target.config.get("host", "localhost"),
                "port": self._target.config.get(
                    "port", c.TargetLdap.Connection.DEFAULT_PORT
                ),
                "use_ssl": self._target.config.get("use_ssl", False),
                "bind_dn": self._target.config.get("bind_dn", ""),
                "password": self._target.config.get("password", ""),
                "timeout": self._target.config.get("timeout", 30),
            }
            self.client = LDAPClient(connection_config)
            connect_result: r[str] = self.client.connect()
            if not connect_result.is_success:
                return r[LDAPClient].fail(
                    f"LDAP connection failed: {connect_result.error}"
                )
            logger.info("LDAP client setup successful for stream: %s", self.stream_name)
            return r[LDAPClient].ok(self.client)
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"LDAP client setup failed: {e}"
            logger.exception(error_msg)
            return r[LDAPClient].fail(error_msg)

    def teardown_client(self) -> None:
        """Teardown LDAP client connection."""
        if self.client:
            _ = self.client.disconnect()
            self.client = None
            logger.info("LDAP client disconnected for stream: %s", self.stream_name)

    def validate_entry(
        self,
        dn: str,
        attributes: dict[str, t.ContainerValue],
        object_classes: list[str],
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


class UsersSink(LDAPBaseSink):
    """LDAP sink for user entries."""

    _USER_FIELD_MAP: ClassVar[dict[str, str]] = {
        "emails": "mail",
        "phone_numbers": "telephoneNumber",
    }

    @override
    def build_attributes(
        self, _record: Mapping[str, t.ContainerValue]
    ) -> r[dict[str, t.ContainerValue]]:
        """Build LDAP attributes for user entry."""
        attrs: dict[str, t.ContainerValue] = {}
        for k, v in _record.items():
            target_key = self._USER_FIELD_MAP.get(k, k)
            if u.is_list(v):
                attrs[target_key] = [str(i) for i in v]
            elif v is not None:
                attrs[target_key] = [str(v)]
        return r[dict[str, t.ContainerValue]].ok(attrs)

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
        self, record: Mapping[str, t.ContainerValue]
    ) -> dict[str, t.ContainerValue]:
        """Build LDAP attributes for user entry."""
        object_classes = self._target.config.get(
            "object_classes", ["inetOrgPerson", "person"]
        )
        attributes: dict[str, t.ContainerValue] = {
            "objectClass": object_classes.copy()
            if u.is_list(object_classes)
            else ["inetOrgPerson", "person"]
        }
        obj_classes = attributes.get("objectClass")
        if u.is_list(obj_classes):
            if "person" not in obj_classes:
                obj_classes.append("person")
            if "inetOrgPerson" not in obj_classes:
                obj_classes.append("inetOrgPerson")
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
        raw_mapping: dict[str, t.ContainerValue] = {}
        if u.is_dict_like(mapping_val):
            for k, v in mapping_val.items():
                raw_mapping[str(k)] = v
        mapping: dict[str, str] = {}
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
    def get_object_classes(self, record: Mapping[str, t.ContainerValue]) -> list[str]:
        """Get object classes for user entry."""
        configured = self._target.config.get("users_object_classes")
        if u.is_list(configured):
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
                "objectClass", ["inetOrgPerson", "person"]
            )
            object_classes: list[str] = (
                [str(oc) for oc in object_classes_raw]
                if u.is_list(object_classes_raw)
                else ["inetOrgPerson", "person"]
            )
            attributes_dict: dict[str, t.ContainerValue] = {}
            for k, v in attributes.items():
                if k != "objectClass":
                    if u.is_list(v):
                        attributes_dict[k] = [str(i) for i in v]
                    else:
                        attributes_dict[k] = [str(v)]
            add_result: r[bool] = self.client.add_entry(
                user_dn, attributes_dict, object_classes
            )
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("User entry added successfully: %s", user_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result: r[bool] = self.client.modify_entry(
                    user_dn, attributes_dict
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("User entry modified successfully: %s", user_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify user {user_dn}: {modify_result.error}"
                )
                return r[bool].fail(
                    f"Failed to modify user {user_dn}: {modify_result.error}"
                )
            self._processing_result.add_error(
                f"Failed to add user {user_dn}: {add_result.error}"
            )
            return r[bool].fail(f"Failed to add user {user_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing user record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)


class GroupsSink(LDAPBaseSink):
    """LDAP sink for group entries."""

    @override
    def build_attributes(
        self, _record: Mapping[str, t.ContainerValue]
    ) -> r[dict[str, t.ContainerValue]]:
        """Build LDAP attributes for group entry."""
        attrs: dict[str, t.ContainerValue] = {}
        field_map = {"members": "member"}
        for k, v in _record.items():
            target_key = field_map.get(k, k)
            if u.is_list(v):
                attrs[target_key] = [str(i) for i in v]
            elif v is not None:
                attrs[target_key] = [str(v)]
        return r[dict[str, t.ContainerValue]].ok(attrs)

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
    def get_object_classes(self, record: Mapping[str, t.ContainerValue]) -> list[str]:
        """Get object classes for group entry."""
        configured = self._target.config.get("groups_object_classes")
        if u.is_list(configured):
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
            object_classes: list[str] = (
                [str(oc) for oc in object_classes_raw]
                if u.is_list(object_classes_raw)
                else ["groupOfNames"]
            )
            attributes_dict: dict[str, t.ContainerValue] = {}
            for k, v in attributes.items():
                if k != "objectClass":
                    if u.is_list(v):
                        attributes_dict[k] = list(v)
                    else:
                        attributes_dict[k] = v
            add_result: r[bool] = self.client.add_entry(
                group_dn, attributes_dict, object_classes
            )
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("Group entry added successfully: %s", group_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result: r[bool] = self.client.modify_entry(
                    group_dn, attributes_dict
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("Group entry modified successfully: %s", group_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify group {group_dn}: {modify_result.error}"
                )
                return r[bool].fail(
                    f"Failed to modify group {group_dn}: {modify_result.error}"
                )
            self._processing_result.add_error(
                f"Failed to add group {group_dn}: {add_result.error}"
            )
            return r[bool].fail(f"Failed to add group {group_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing group record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_group_attributes(
        self, record: Mapping[str, t.ContainerValue]
    ) -> dict[str, t.ContainerValue]:
        """Build LDAP attributes for group entry."""
        object_classes = self._target.config.get(
            "group_object_classes", ["groupOfNames"]
        )
        attributes: dict[str, t.ContainerValue] = {
            "objectClass": object_classes.copy()
            if u.is_list(object_classes)
            else ["groupOfNames"]
        }
        obj_classes = attributes.get("objectClass")
        if u.is_list(obj_classes) and "groupOfNames" not in obj_classes:
            obj_classes.append("groupOfNames")
        field_mapping = {
            "name": "cn",
            "description": "description",
            "members": "member",
        }
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if u.is_list(value):
                    attributes[ldap_attr] = value
                else:
                    attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping: dict[str, t.ContainerValue] = {}
        if u.is_dict_like(mapping_val):
            for k, v in mapping_val.items():
                raw_mapping[str(k)] = v
        mapping: dict[str, str] = {}
        for k, v in raw_mapping.items():
            match v:
                case str():
                    mapping[k] = str(v)
                case _:
                    pass
        for singer_field, mapped_attr in mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if u.is_list(value):
                    attributes[mapped_attr] = value
                else:
                    attributes[mapped_attr] = [str(value)]
        return attributes


class OrganizationalUnitsSink(LDAPBaseSink):
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
            attributes_dict: dict[str, t.ContainerValue] = {}
            for k, v in attributes.items():
                if u.is_list(v):
                    attributes_dict[k] = list(v)
                else:
                    attributes_dict[k] = v
            add_result: r[bool] = self.client.add_entry(ou_dn, attributes_dict)
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("OU entry added successfully: %s", ou_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result: r[bool] = self.client.modify_entry(
                    ou_dn, attributes_dict
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("OU entry modified successfully: %s", ou_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify OU {ou_dn}: {modify_result.error}"
                )
                return r[bool].fail(
                    f"Failed to modify OU {ou_dn}: {modify_result.error}"
                )
            self._processing_result.add_error(
                f"Failed to add OU {ou_dn}: {add_result.error}"
            )
            return r[bool].fail(f"Failed to add OU {ou_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing OU record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_ou_attributes(
        self, record: Mapping[str, t.ContainerValue]
    ) -> dict[str, t.ContainerValue]:
        """Build LDAP attributes for OU entry."""
        default_classes = self._target.config.get(
            "object_classes", ["organizationalUnit"]
        )
        attributes: dict[str, t.ContainerValue] = {
            "objectClass": default_classes.copy()
            if u.is_list(default_classes)
            else ["organizationalUnit"]
        }
        obj_classes = attributes.get("objectClass")
        if u.is_list(obj_classes) and "organizationalUnit" not in obj_classes:
            obj_classes.append("organizationalUnit")
        field_mapping = {"name": "ou", "description": "description"}
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping: dict[str, t.ContainerValue] = {}
        if u.is_dict_like(mapping_val):
            for k, v in mapping_val.items():
                raw_mapping[str(k)] = v
        mapping: dict[str, str] = {}
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
