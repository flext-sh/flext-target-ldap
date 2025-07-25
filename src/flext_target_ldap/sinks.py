"""LDAP sinks for Singer target using flext-core patterns.

REFACTORED:
Uses flext-core patterns for type-safe LDAP operations.
Zero tolerance for code duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Import from flext-core for foundational patterns
from flext_core import (
    FlextResult,
    FlextValueObject as FlextDomainBaseModel,
    get_logger,
)

# MIGRATED: from flext_meltano import Sink -> use flext_meltano
from flext_meltano import Sink
from pydantic import Field

from flext_target_ldap.client import LDAPClient

if TYPE_CHECKING:
    from flext_target_ldap.config import TargetLDAPConfig

logger = get_logger(__name__)


class LDAPProcessingResult(FlextDomainBaseModel):
    """Result of LDAP processing operations using flext-core patterns."""

    processed_count: int = Field(0, description="Number of records processed")
    success_count: int = Field(0, description="Number of successful operations")
    error_count: int = Field(0, description="Number of failed operations")
    errors: list[str] = Field(
        default_factory=list,
        description="List of error messages",
    )

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.processed_count == 0:
            return 0.0
        return (self.success_count / self.processed_count) * 100.0

    def add_success(self) -> None:
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

    def __init__(
        self,
        target: Any,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: list[str],
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        self.config: TargetLDAPConfig = target.config
        self.client: LDAPClient | None = None
        self._processing_result = LDAPProcessingResult()

    def setup_client(self) -> FlextResult[LDAPClient]:
        """Setup LDAP client connection."""
        try:
            from flext_target_ldap.client import LDAPConnectionConfig

            connection_config = LDAPConnectionConfig(
                host=self.config.host,
                port=self.config.port,
                use_ssl=self.config.use_ssl,
                use_tls=self.config.use_tls,
                bind_dn=self.config.bind_dn,
                bind_password=self.config.bind_password,
                base_dn=self.config.base_dn,
                connect_timeout=self.config.connect_timeout,
                receive_timeout=self.config.receive_timeout,
            )

            self.client = LDAPClient(connection_config)
            connect_result = self.client.connect()

            if not connect_result.is_success:
                return FlextResult.fail(
                    f"LDAP connection failed: {connect_result.error}",
                )

            logger.info(f"LDAP client setup successful for stream: {self.stream_name}")
            return FlextResult.ok(self.client)

        except Exception as e:
            error_msg = f"LDAP client setup failed: {e}"
            logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def teardown_client(self) -> None:
        """Teardown LDAP client connection."""
        if self.client:
            self.client.disconnect()
            self.client = None
            logger.info(f"LDAP client disconnected for stream: {self.stream_name}")

    def process_batch(self, context: dict[str, Any]) -> None:
        """Process a batch of records."""
        setup_result = self.setup_client()
        if not setup_result.is_success:
            logger.error(f"Cannot process batch: {setup_result.error}")
            return

        try:
            records = context.get("records", [])
            logger.info(
                f"Processing batch of {len(records)} records for stream: {self.stream_name}",
            )

            for record in records:
                self.process_record(record)

            logger.info(
                f"Batch processing completed. Success: {self._processing_result.success_count}, "
                f"Errors: {self._processing_result.error_count}",
            )

        finally:
            self.teardown_client()

    def process_record(self, record: dict[str, Any]) -> None:
        """Process a single record. Override in subclasses."""
        msg = "Subclasses must implement process_record"
        raise NotImplementedError(msg)

    def get_processing_result(self) -> LDAPProcessingResult:
        """Get processing results."""
        return self._processing_result


class UsersSink(LDAPBaseSink):
    """LDAP sink for user entries."""

    def process_record(self, record: dict[str, Any]) -> None:
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
            user_dn = f"uid={username},{self.config.base_dn}"

            # Build LDAP attributes from record
            attributes = self._build_user_attributes(record)

            # Try to add the user entry
            add_result = self.client.add_entry(user_dn, attributes)

            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug(f"User entry added successfully: {user_dn}")
            # If add failed, try to modify existing entry
            elif self.config.update_existing_entries:
                modify_result = self.client.modify_entry(user_dn, attributes)
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug(f"User entry modified successfully: {user_dn}")
                else:
                    self._processing_result.add_error(
                        f"Failed to modify user {user_dn}: {modify_result.error}",
                    )
            else:
                self._processing_result.add_error(
                    f"Failed to add user {user_dn}: {add_result.error}",
                )

        except Exception as e:
            error_msg = f"Error processing user record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def _build_user_attributes(self, record: dict[str, Any]) -> dict[str, Any]:
        """Build LDAP attributes for user entry."""
        attributes = {"objectClass": self.config.object_classes.copy()}

        # Add person-specific object classes
        if "person" not in attributes["objectClass"]:
            attributes["objectClass"].append("person")
        if "inetOrgPerson" not in attributes["objectClass"]:
            attributes["objectClass"].append("inetOrgPerson")

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
                attributes[ldap_attr] = str(value)

        # Apply custom attribute mapping
        for singer_field, ldap_attr in self.config.attribute_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = str(value)

        return attributes


class GroupsSink(LDAPBaseSink):
    """LDAP sink for group entries."""

    def process_record(self, record: dict[str, Any]) -> None:
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
            group_dn = f"cn={group_name},{self.config.base_dn}"

            # Build LDAP attributes from record
            attributes = self._build_group_attributes(record)

            # Try to add the group entry
            add_result = self.client.add_entry(group_dn, attributes)

            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug(f"Group entry added successfully: {group_dn}")
            # If add failed, try to modify existing entry
            elif self.config.update_existing_entries:
                modify_result = self.client.modify_entry(group_dn, attributes)
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug(f"Group entry modified successfully: {group_dn}")
                else:
                    self._processing_result.add_error(
                        f"Failed to modify group {group_dn}: {modify_result.error}",
                    )
            else:
                self._processing_result.add_error(
                    f"Failed to add group {group_dn}: {add_result.error}",
                )

        except Exception as e:
            error_msg = f"Error processing group record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def _build_group_attributes(self, record: dict[str, Any]) -> dict[str, Any]:
        """Build LDAP attributes for group entry."""
        attributes = {"objectClass": self.config.object_classes.copy()}

        # Add group-specific object classes
        if "groupOfNames" not in attributes["objectClass"]:
            attributes["objectClass"].append("groupOfNames")

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
                    attributes[ldap_attr] = str(value)

        # Apply custom attribute mapping
        for singer_field, ldap_attr in self.config.attribute_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if isinstance(value, list):
                    attributes[ldap_attr] = value
                else:
                    attributes[ldap_attr] = str(value)

        return attributes


class OrganizationalUnitsSink(LDAPBaseSink):
    """LDAP sink for organizational unit entries."""

    def process_record(self, record: dict[str, Any]) -> None:
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
            ou_dn = f"ou={ou_name},{self.config.base_dn}"

            # Build LDAP attributes from record
            attributes = self._build_ou_attributes(record)

            # Try to add the OU entry
            add_result = self.client.add_entry(ou_dn, attributes)

            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug(f"OU entry added successfully: {ou_dn}")
            # If add failed, try to modify existing entry
            elif self.config.update_existing_entries:
                modify_result = self.client.modify_entry(ou_dn, attributes)
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug(f"OU entry modified successfully: {ou_dn}")
                else:
                    self._processing_result.add_error(
                        f"Failed to modify OU {ou_dn}: {modify_result.error}",
                    )
            else:
                self._processing_result.add_error(
                    f"Failed to add OU {ou_dn}: {add_result.error}",
                )

        except Exception as e:
            error_msg = f"Error processing OU record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)

    def _build_ou_attributes(self, record: dict[str, Any]) -> dict[str, Any]:
        """Build LDAP attributes for OU entry."""
        attributes = {"objectClass": self.config.object_classes.copy()}

        # Add OU-specific object classes
        if "organizationalUnit" not in attributes["objectClass"]:
            attributes["objectClass"].append("organizationalUnit")

        # Map Singer fields to LDAP attributes
        field_mapping = {
            "name": "ou",
            "description": "description",
        }

        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = str(value)

        # Apply custom attribute mapping
        for singer_field, ldap_attr in self.config.attribute_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = str(value)

        return attributes
