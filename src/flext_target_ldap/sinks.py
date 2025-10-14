"""LDAP sinks for Singer target using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from asyncio import run
from typing import override

from flext_core import FlextCore

from flext_target_ldap.client import LDAPClient
from flext_target_ldap.typings import FlextTargetLdapTypes


# Placeholder classes until flext-meltano provides proper Singer protocol classes
class Sink:
    """Placeholder Sink base class for Singer protocol compatibility."""

    @override
    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: FlextTargetLdapTypes.Core.Dict,
        key_properties: FlextTargetLdapTypes.Core.StringList,
    ) -> None:
        """Initialize sink with Singer protocol parameters."""
        self.target = target
        self.stream_name = stream_name
        self.schema = schema
        self.key_properties = key_properties

    def process_record(
        self,
        _record: FlextTargetLdapTypes.Core.Dict,
        _context: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextCore.Result[None]:
        """Process a record using the target."""
        # Implementation will delegate to target's process method
        try:
            # Basic processing - this is a placeholder implementation
            # Real implementation would transform and load the record to LDAP
            return FlextCore.Result[None].ok(None)
        except Exception as e:
            return FlextCore.Result[None].fail(f"Record processing failed: {e}")


class Target:
    """Placeholder Target base class for Singer protocol compatibility."""

    @override
    def __init__(self, config: FlextTargetLdapTypes.Core.Dict) -> None:
        """Initialize target with configuration."""
        self.config: FlextCore.Types.Dict = config


logger = FlextCore.Logger(__name__)


class LDAPProcessingResult:
    """Result of LDAP processing operations - mutable for performance tracking."""

    @override
    def __init__(self: object) -> None:
        """Initialize processing result counters."""
        self.processed_count: int = 0
        self.success_count: int = 0
        self.error_count: int = 0
        self.errors: FlextTargetLdapTypes.Core.StringList = []

    @property
    def success_rate(self: object) -> float:
        """Calculate success rate as percentage."""
        if self.processed_count == 0:
            return 0.0
        return (self.success_count / self.processed_count) * 100.0

    def add_success(self: object) -> None:
        """Record a successful operation."""
        self.processed_count += 1
        self.success_count += 1

    def add_error(self, error_message: str) -> None:
        """Record a failed operation."""
        self.processed_count += 1
        self.error_count += 1
        self.errors.append(error_message)


class LDAPBaseSink(Sink):
    """Base LDAP sink with common functionality."""

    @override
    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: FlextTargetLdapTypes.Core.Dict,
        key_properties: FlextTargetLdapTypes.Core.StringList,
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        # Store target reference for config access
        self._target = target
        self.client: LDAPClient | None = None
        self._processing_result: FlextCore.Result[object] = LDAPProcessingResult()

    def setup_client(self) -> FlextCore.Result[LDAPClient]:
        """Set up LDAP client connection."""
        try:
            # Create dict[str, object] configuration for LDAPClient compatibility
            connection_config = {
                "host": self._target.config.get("host", "localhost"),
                "port": self._target.config.get("port", 389),
                "use_ssl": self._target.config.get("use_ssl", False),
                "bind_dn": self._target.config.get("bind_dn", ""),
                "password": self._target.config.get("password", ""),
                "timeout": self._target.config.get("timeout", 30),
            }

            self.client = LDAPClient(connection_config)
            connect_result: FlextCore.Result[object] = self.client.connect()

            if not connect_result.is_success:
                return FlextCore.Result[LDAPClient].fail(
                    f"LDAP connection failed: {connect_result.error}",
                )

            logger.info("LDAP client setup successful for stream: %s", self.stream_name)
            return FlextCore.Result[LDAPClient].ok(self.client)

        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"LDAP client setup failed: {e}"
            logger.exception(error_msg)
            return FlextCore.Result[LDAPClient].fail(error_msg)

    def teardown_client(self: object) -> None:
        """Teardown LDAP client connection."""
        if self.client:
            # Disconnect using client API (sync)
            _ = self.client.disconnect()
            self.client = None
            logger.info("LDAP client disconnected for stream: %s", self.stream_name)

    def process_batch(self, context: FlextTargetLdapTypes.Core.Dict) -> None:
        """Process a batch of records."""
        setup_result: FlextCore.Result[object] = run(self.setup_client())
        if not setup_result.is_success:
            logger.error("Cannot process batch: %s", setup_result.error)
            return

        try:
            records_raw: FlextCore.Types.List = context.get("records", [])

            records: FlextCore.Types.List = (
                records_raw if isinstance(records_raw, list) else []
            )
            logger.info(
                "Processing batch of %d records for stream: %s",
                len(records),
                self.stream_name,
            )

            for record in records:
                self.process_record(record, context)

            logger.info(
                "Batch processing completed. Success: %d, Errors: %d",
                self._processing_result.success_count,
                self._processing_result.error_count,
            )

        finally:
            self.teardown_client()

    def process_record(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
        _context: FlextTargetLdapTypes.Core.Dict,
    ) -> None:
        """Process a single record. Override in subclasses."""
        # Base implementation - can be overridden in subclasses for specific behavior
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return

        try:
            # Generic record processing - log and mark as processed
            logger.debug("Processing record: %s", record)
            self._processing_result.add_success()
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def get_processing_result(self: object) -> LDAPProcessingResult:
        """Get processing results."""
        return self._processing_result


class UsersSink(LDAPBaseSink):
    """LDAP sink for user entries."""

    def process_record(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
        _context: FlextTargetLdapTypes.Core.Dict,
    ) -> None:
        """Process a user record."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return

        try:
            # Extract user information from record
            username = record.get("username") or record.get("uid") or record.get("cn")
            if not username:
                self._processing_result.add_error("No username found in record")
                return

            # Build DN for user
            base_dn = self._target.config.get("base_dn", "dc=example,dc=com")
            user_dn = f"uid={username},{base_dn}"

            # Build LDAP attributes from record
            attributes = self.build_user_attributes(record)

            # Extract object classes for the add_entry call
            object_classes_raw = attributes.pop(
                "objectClass",
                ["inetOrgPerson", "person"],
            )
            object_classes = (
                object_classes_raw
                if isinstance(object_classes_raw, list)
                else ["inetOrgPerson", "person"]
            )

            # Try to add the user entry
            add_result: FlextCore.Result[bool] = self.client.add_entry(
                user_dn,
                attributes,
                object_classes,
            )

            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("User entry added successfully: %s", user_dn)
            # If add failed, try to modify existing entry
            elif self._target.config.get("update_existing_entries", False):
                modify_result: FlextCore.Result[bool] = self.client.modify_entry(
                    user_dn,
                    attributes,
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("User entry modified successfully: %s", user_dn)
                else:
                    self._processing_result.add_error(
                        f"Failed to modify user {user_dn}: {modify_result.error}",
                    )
            else:
                self._processing_result.add_error(
                    f"Failed to add user {user_dn}: {add_result.error}",
                )

        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing user record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def build_user_attributes(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextTargetLdapTypes.Core.Dict:
        """Build LDAP attributes for user entry."""
        object_classes = self._target.config.get(
            "object_classes",
            ["inetOrgPerson", "person"],
        )
        attributes: FlextTargetLdapTypes.Core.Dict = {
            "objectClass": object_classes.copy()
            if isinstance(object_classes, list)
            else ["inetOrgPerson", "person"],
        }

        # Add person-specific object classes
        obj_classes = attributes.get("objectClass")
        if isinstance(obj_classes, list):
            if "person" not in obj_classes:
                obj_classes.append("person")
            if "inetOrgPerson" not in obj_classes:
                obj_classes.append("inetOrgPerson")

        # Map Singer fields to LDAP attributes
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

        # Apply custom attribute mapping
        mapping_obj: FlextCore.Types.Dict = self._target.config.get(
            "attribute_mapping", {}
        )
        if isinstance(mapping_obj, dict):
            for singer_field, ldap_attr in mapping_obj.items():
                value = record.get(singer_field)
                if value is not None:
                    attributes[ldap_attr] = [str(value)]

        return attributes


class GroupsSink(LDAPBaseSink):
    """LDAP sink for group entries."""

    def process_record(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
        _context: FlextTargetLdapTypes.Core.Dict,
    ) -> None:
        """Process a group record."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return

        try:
            # Extract group information from record
            group_name = record.get("name") or record.get("cn")
            if not group_name:
                self._processing_result.add_error("No group name found in record")
                return

            # Build DN for group
            group_dn = f"cn={group_name},{self._target.config.get('base_dn', 'dc=example,dc=com')}"

            # Build LDAP attributes from record
            attributes = self._build_group_attributes(record)

            # Extract object classes for the add_entry call
            object_classes_raw = attributes.pop("objectClass", ["groupOfNames"])
            object_classes = (
                object_classes_raw
                if isinstance(object_classes_raw, list)
                else ["groupOfNames"]
            )

            # Try to add the group entry
            add_result: FlextCore.Result[bool] = self.client.add_entry(
                group_dn,
                attributes,
                object_classes,
            )

            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("Group entry added successfully: %s", group_dn)
            # If add failed, try to modify existing entry
            elif self._target.config.get("update_existing_entries", False):
                modify_result: FlextCore.Result[bool] = self.client.modify_entry(
                    group_dn,
                    attributes,
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("Group entry modified successfully: %s", group_dn)
                else:
                    self._processing_result.add_error(
                        f"Failed to modify group {group_dn}: {modify_result.error}",
                    )
            else:
                self._processing_result.add_error(
                    f"Failed to add group {group_dn}: {add_result.error}",
                )

        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing group record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def _build_group_attributes(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextTargetLdapTypes.Core.Dict:
        """Build LDAP attributes for group entry."""
        object_classes = self._target.config.get(
            "group_object_classes",
            ["groupOfNames"],
        )
        attributes: FlextTargetLdapTypes.Core.Dict = {
            "objectClass": object_classes.copy()
            if isinstance(object_classes, list)
            else ["groupOfNames"],
        }

        # Add group-specific object classes
        obj_classes = attributes.get("objectClass")
        if isinstance(obj_classes, list) and "groupOfNames" not in obj_classes:
            obj_classes.append("groupOfNames")

        # Map Singer fields to LDAP attributes
        field_mapping = {
            "name": "cn",
            "description": "description",
            "members": "member",
        }

        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if isinstance(value, list):
                    attributes[ldap_attr] = value
                else:
                    attributes[ldap_attr] = [str(value)]

        # Apply custom attribute mapping
        mapping_obj: FlextCore.Types.Dict = self._target.config.get(
            "attribute_mapping", {}
        )
        if isinstance(mapping_obj, dict):
            for singer_field, ldap_attr in mapping_obj.items():
                value = record.get(singer_field)
                if value is not None:
                    if isinstance(value, list):
                        attributes[ldap_attr] = value
                    else:
                        attributes[ldap_attr] = [str(value)]

        return attributes


class OrganizationalUnitsSink(LDAPBaseSink):
    """LDAP sink for organizational unit entries."""

    def process_record(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
        _context: FlextTargetLdapTypes.Core.Dict,
    ) -> None:
        """Process an organizational unit record."""
        if not self.client:
            self._processing_result.add_error("LDAP client not initialized")
            return

        try:
            # Extract OU information from record
            ou_name = record.get("name") or record.get("ou")
            if not ou_name:
                self._processing_result.add_error("No OU name found in record")
                return

            # Build DN for OU
            ou_dn = f"ou={ou_name},{self._target.config.get('base_dn', 'dc=example,dc=com')}"

            # Build LDAP attributes from record
            attributes = self._build_ou_attributes(record)

            # Try to add the OU entry
            add_result: FlextCore.Result[bool] = self.client.add_entry(
                ou_dn, attributes
            )

            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("OU entry added successfully: %s", ou_dn)
            # If add failed, try to modify existing entry
            elif self._target.config.get("update_existing_entries", False):
                modify_result: FlextCore.Result[bool] = self.client.modify_entry(
                    ou_dn,
                    attributes,
                )
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("OU entry modified successfully: %s", ou_dn)
                else:
                    self._processing_result.add_error(
                        f"Failed to modify OU {ou_dn}: {modify_result.error}",
                    )
            else:
                self._processing_result.add_error(
                    f"Failed to add OU {ou_dn}: {add_result.error}",
                )

        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing OU record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def _build_ou_attributes(
        self,
        record: FlextTargetLdapTypes.Core.Dict,
    ) -> FlextTargetLdapTypes.Core.Dict:
        """Build LDAP attributes for OU entry."""
        default_classes = self._target.config.get(
            "object_classes",
            ["organizationalUnit"],
        )
        attributes: FlextTargetLdapTypes.Core.Dict = {
            "objectClass": default_classes.copy()
            if isinstance(default_classes, list)
            else ["organizationalUnit"],
        }

        # Add OU-specific object classes
        obj_classes = attributes.get("objectClass")
        if isinstance(obj_classes, list) and "organizationalUnit" not in obj_classes:
            obj_classes.append("organizationalUnit")

        # Map Singer fields to LDAP attributes
        field_mapping = {
            "name": "ou",
            "description": "description",
        }

        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = [str(value)]

        # Apply custom attribute mapping
        mapping_obj: FlextCore.Types.Dict = self._target.config.get(
            "attribute_mapping", {}
        )
        if isinstance(mapping_obj, dict):
            for singer_field, ldap_attr in mapping_obj.items():
                value = record.get(singer_field)
                if value is not None:
                    attributes[ldap_attr] = [str(value)]

        return attributes
