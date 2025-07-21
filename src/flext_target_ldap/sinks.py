"""Enterprise sink implementations for target-ldap using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Comprehensive sinks for loading different types of data into LDAP directories with
enterprise features: Oracle compatibility, transformation engine, validation,
batch processing.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from flext_core.domain.pydantic_base import DomainBaseModel
from flext_core.domain.types import ServiceResult
from pydantic import Field
from singer_sdk.sinks import Sink

from flext_target_ldap.client import LDAPClient

if TYPE_CHECKING:
    from singer_sdk.target_base import Target

logger = logging.getLogger(__name__)


class LDAPProcessingResult(DomainBaseModel):
    """Result of LDAP processing operations using flext-core patterns."""

    processed_count: int = 0
    successful_count: int = 0
    failed_count: int = 0
    error_messages: list[str] = Field(default_factory=list)

    def add_success(self) -> None:
        """Record a successful operation."""
        self.processed_count += 1
        self.successful_count += 1

    def add_failure(self, error: str) -> None:
        """Record a failed operation."""
        self.processed_count += 1
        self.failed_count += 1
        self.error_messages.append(error)

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.processed_count == 0:
            return 0.0
        return (self.successful_count / self.processed_count) * 100.0


class LDAPSink(Sink):
    """Base class for LDAP sinks using flext-core patterns."""

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: list[str] | None,
    ) -> None:
        super().__init__(target, stream_name, schema, key_properties)
        self._client: LDAPClient | None = None
        self._processing_result = LDAPProcessingResult()

        # Configuration from target
        self._enable_validation = self.config.get("enable_validation", True)
        self._dry_run_mode = self.config.get("dry_run_mode", False)
        self._batch_size = self.config.get("batch_size", 100)
        self._max_errors = self.config.get("max_errors", 10)

    @property
    def client(self) -> LDAPClient:
        """Get or create LDAP client."""
        if self._client is None:
            config = self.config
            self._client = LDAPClient(
                host=config["host"],
                port=config.get("port", 389),
                bind_dn=config.get("bind_dn"),
                password=config.get("password"),
                use_ssl=config.get("use_ssl", False),
                timeout=config.get("timeout", 30),
            )
        return self._client

    def process_record(self, record: dict[str, Any], context: dict[str, Any]) -> None:
        try:
            # Build DN for the entry
            dn_result = self.build_dn(record)
            if not dn_result.is_success:
                self._processing_result.add_failure(
                    f"DN building failed: {dn_result.error}",
                )
                return

            dn = dn_result.value

            # Build attributes
            attributes_result = self.build_attributes(record)
            if not attributes_result.is_success:
                self._processing_result.add_failure(
                    f"Attribute building failed: {attributes_result.error}",
                )
                return

            attributes = attributes_result.value

            # Get object classes
            object_classes = self.get_object_classes(record)

            # Validate if enabled
            if self._enable_validation:
                if dn is None or attributes is None:
                    self._processing_result.add_failure(
                        "DN or attributes cannot be None",
                    )
                    return
                validation_result = self.validate_entry(dn, attributes, object_classes)
                if not validation_result.is_success:
                    self._processing_result.add_failure(
                        f"Validation failed: {validation_result.error}",
                    )
                    return

            # Skip actual LDAP operations in dry run mode
            if self._dry_run_mode:
                logger.info(
                    "DRY RUN: Would upsert entry %s with attributes: %s",
                    dn,
                    attributes,
                )
                self._processing_result.add_success()
                return

            # Perform upsert operation
            if dn is None or attributes is None:
                self._processing_result.add_failure("DN or attributes cannot be None")
                return
            upsert_result = self.client.upsert_entry(dn, object_classes, attributes)
            if upsert_result.is_success:
                if upsert_result.value is not None:
                    operation = upsert_result.value[1]  # "add" or "modify"
                    logger.info("Successfully %s entry: %s", operation, dn)
                self._processing_result.add_success()
            else:
                self._processing_result.add_failure(
                    f"Upsert failed: {upsert_result.error}",
                )
        except Exception as e:
            error_msg = f"Unexpected error processing record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_failure(error_msg)

    def build_dn(self, record: dict[str, Any]) -> ServiceResult[str]:
        """Build distinguished name for the record. Override in subclasses."""
        return ServiceResult.fail("build_dn method must be implemented in subclass")

    def build_attributes(self, record: dict[str, Any]) -> ServiceResult[dict[str, Any]]:
        """Build LDAP attributes from record. Override in subclasses."""
        return ServiceResult.fail(
            "build_attributes method must be implemented in subclass",
        )

    def get_object_classes(self, record: dict[str, Any]) -> list[str]:
        """Get object classes for the entry. Override in subclasses."""
        return ["top"]

    def validate_entry(
        self,
        dn: str,
        attributes: dict[str, Any],
        object_classes: list[str],
    ) -> ServiceResult[bool]:
        """Validate entry before processing."""
        # Basic validation - check required attributes
        if not dn:
            return ServiceResult.fail("DN cannot be empty")

        if not attributes:
            return ServiceResult.fail("Attributes cannot be empty")

        if not object_classes:
            return ServiceResult.fail("Object classes cannot be empty")

        # Validate DN format
        dn_validation = self.client.validate_dn(dn)
        if not dn_validation.is_success:
            return ServiceResult.fail(f"Invalid DN format: {dn_validation.error}")

        return ServiceResult.ok(True)

    def process_batch(self, records: dict[Any, Any]) -> None:
        """Process a batch of records."""
        # Convert to list - records is expected to be a dict by the type annotation
        records_list = [records]
        try:
            for record in records_list:
                self.process_record(record, {})

                # Check error threshold
                if self._processing_result.failed_count >= self._max_errors:
                    logger.error(
                        "Maximum error count (%d) reached, stopping processing",
                        self._max_errors,
                    )
                    break
        except Exception as e:
            error_msg = f"Error in batch processing: {e}"
            logger.exception(error_msg)
            self._processing_result.add_failure(error_msg)

    def get_processing_summary(self) -> dict[str, Any]:
        """Get processing summary statistics."""
        return {
            "processed": self._processing_result.processed_count,
            "successful": self._processing_result.successful_count,
            "failed": self._processing_result.failed_count,
            "success_rate": self._processing_result.success_rate,
            "errors": self._processing_result.error_messages,
        }


class UsersSink(LDAPSink):
    """Sink for processing user entries using flext-core patterns."""

    def build_dn(self, record: dict[str, Any]) -> ServiceResult[str]:
        """Build DN for user entries."""
        try:
            # Get RDN attribute (usually uid or cn)
            rdn_attr = self.config.get("user_rdn_attribute", "uid")
            rdn_value = (
                record.get(rdn_attr) or record.get("id") or record.get("username")
            )

            if not rdn_value:
                return ServiceResult.fail(
                    f"No value found for RDN attribute '{rdn_attr}'",
                )

            base_dn = self.config["base_dn"]
            dn = f"{rdn_attr}={rdn_value},{base_dn}"

            return ServiceResult.ok(dn)
        except Exception as e:
            return ServiceResult.fail(f"Error building user DN: {e}")

    def build_attributes(self, record: dict[str, Any]) -> ServiceResult[dict[str, Any]]:
        """Build LDAP attributes for user entries."""
        try:
            attributes: dict[str, Any] = {}

            # Standard user attributes
            attribute_mapping = {
                "uid": ["uid", "id", "username"],
                "cn": ["cn", "common_name", "full_name"],
                "sn": ["sn", "surname", "last_name"],
                "givenName": ["givenName", "given_name", "first_name"],
                "mail": ["mail", "email", "email_address"],
                "telephoneNumber": ["telephoneNumber", "phone", "phone_number"],
                "title": ["title", "job_title"],
                "department": ["department", "dept"],
                "employeeNumber": ["employeeNumber", "employee_number", "employee_id"],
                "manager": ["manager", "manager_dn"],
                "description": ["description", "desc"],
            }

            for ldap_attr, source_fields in attribute_mapping.items():
                for field in source_fields:
                    if record.get(field):
                        value = record[field]
                        if isinstance(value, list):
                            attributes[ldap_attr] = value
                        else:
                            attributes[ldap_attr] = [str(value)]
                        break

            # Handle multi-valued attributes
            if "emails" in record:
                attributes["mail"] = (
                    record["emails"]
                    if isinstance(record["emails"], list)
                    else [record["emails"]]
                )

            if "phone_numbers" in record:
                attributes["telephoneNumber"] = (
                    record["phone_numbers"]
                    if isinstance(record["phone_numbers"], list)
                    else [record["phone_numbers"]]
                )

            return ServiceResult.ok(attributes)
        except Exception as e:
            return ServiceResult.fail(f"Error building user attributes: {e}")

    def get_object_classes(self, record: dict[str, Any]) -> list[str]:
        """Get object classes for user entries."""
        return self.config.get(
            "users_object_classes",
            ["inetOrgPerson", "organizationalPerson", "person", "top"],
        )


class GroupsSink(LDAPSink):
    """Sink for processing group entries using flext-core patterns."""

    def build_dn(self, record: dict[str, Any]) -> ServiceResult[str]:
        """Build DN for group entries."""
        try:
            # Get RDN attribute (usually cn)
            rdn_attr = self.config.get("group_rdn_attribute", "cn")
            rdn_value = record.get(rdn_attr) or record.get("id") or record.get("name")

            if not rdn_value:
                return ServiceResult.fail(
                    f"No value found for RDN attribute '{rdn_attr}'",
                )

            base_dn = self.config["base_dn"]
            dn = f"{rdn_attr}={rdn_value},{base_dn}"

            return ServiceResult.ok(dn)
        except Exception as e:
            return ServiceResult.fail(f"Error building group DN: {e}")

    def build_attributes(self, record: dict[str, Any]) -> ServiceResult[dict[str, Any]]:
        """Build LDAP attributes for group entries."""
        try:
            attributes: dict[str, Any] = {}

            # Standard group attributes
            attribute_mapping = {
                "cn": ["cn", "name", "group_name"],
                "description": ["description", "desc"],
                "member": ["members", "member_dns"],
                "uniqueMember": ["unique_members", "unique_member_dns"],
            }

            for ldap_attr, source_fields in attribute_mapping.items():
                for field in source_fields:
                    if record.get(field):
                        value = record[field]
                        if isinstance(value, list):
                            attributes[ldap_attr] = value
                        else:
                            attributes[ldap_attr] = [str(value)]
                        break

            return ServiceResult.ok(attributes)
        except Exception as e:
            return ServiceResult.fail(f"Error building group attributes: {e}")

    def get_object_classes(self, record: dict[str, Any]) -> list[str]:
        """Get object classes for group entries."""
        return self.config.get("groups_object_classes", ["groupOfNames", "top"])


class OrganizationalUnitsSink(LDAPSink):
    """Sink for processing organizational unit entries using flext-core patterns."""

    def build_dn(self, record: dict[str, Any]) -> ServiceResult[str]:
        """Build DN for OU entries."""
        try:
            # Get OU name
            ou_name = record.get("ou") or record.get("name") or record.get("id")

            if not ou_name:
                return ServiceResult.fail("No OU name found in record")

            base_dn = self.config["base_dn"]
            dn = f"ou={ou_name},{base_dn}"

            return ServiceResult.ok(dn)
        except Exception as e:
            return ServiceResult.fail(f"Error building OU DN: {e}")

    def build_attributes(self, record: dict[str, Any]) -> ServiceResult[dict[str, Any]]:
        """Build LDAP attributes for OU entries."""
        try:
            attributes: dict[str, Any] = {}

            # Standard OU attributes
            attribute_mapping = {
                "ou": ["ou", "name"],
                "description": ["description", "desc"],
                "telephoneNumber": ["telephoneNumber", "phone"],
                "facsimileTelephoneNumber": ["fax", "fax_number"],
                "street": ["street", "street_address"],
                "l": ["l", "locality", "city"],
                "st": ["st", "state", "province"],
                "postalCode": ["postalCode", "zip_code", "postal_code"],
            }

            for ldap_attr, source_fields in attribute_mapping.items():
                for field in source_fields:
                    if record.get(field):
                        value = record[field]
                        if isinstance(value, list):
                            attributes[ldap_attr] = value
                        else:
                            attributes[ldap_attr] = [str(value)]
                        break

            return ServiceResult.ok(attributes)
        except Exception as e:
            return ServiceResult.fail(f"Error building OU attributes: {e}")

    def get_object_classes(self, record: dict[str, Any]) -> list[str]:
        """Get object classes for OU entries."""
        return self.config.get(
            "organizational_units_object_classes",
            ["organizationalUnit", "top"],
        )


class GenericSink(LDAPSink):
    """Generic sink for processing custom entries using flext-core patterns."""

    def build_dn(self, record: dict[str, Any]) -> ServiceResult[str]:
        """Build DN for generic entries."""
        try:
            # Try to get DN directly from record
            if "dn" in record:
                return ServiceResult.ok(record["dn"])

            # Try to build from id and base_dn
            entry_id = record.get("id") or record.get("name")
            if not entry_id:
                return ServiceResult.fail("No ID or name found for generic entry")

            base_dn = self.config["base_dn"]
            dn = f"cn={entry_id},{base_dn}"

            return ServiceResult.ok(dn)
        except Exception as e:
            return ServiceResult.fail(f"Error building generic DN: {e}")

    def build_attributes(self, record: dict[str, Any]) -> ServiceResult[dict[str, Any]]:
        """Build LDAP attributes for generic entries."""
        try:
            attributes: dict[str, Any] = {}

            # Copy all record fields as attributes, excluding special fields
            exclude_fields = {
                "dn",
                "object_classes",
                "_sdc_table_version",
                "_sdc_received_at",
                "_sdc_sequence",
            }

            for key, value in record.items():
                if key not in exclude_fields and value is not None:
                    if isinstance(value, list):
                        attributes[key] = value
                    else:
                        attributes[key] = [str(value)]

            return ServiceResult.ok(attributes)
        except Exception as e:
            return ServiceResult.fail(f"Error building generic attributes: {e}")

    def get_object_classes(self, record: dict[str, Any]) -> list[str]:
        """Get object classes for generic entries."""
        # Use object classes from record if available
        if "object_classes" in record:
            obj_classes = record["object_classes"]
            if isinstance(obj_classes, list):
                return obj_classes
            return [str(obj_classes)]

        # Use configured default for stream
        stream_key = f"{self.stream_name}_object_classes"
        return self.config.get(stream_key, ["top"])


# Export main sink classes
__all__ = [
    "GenericSink",
    "GroupsSink",
    "LDAPProcessingResult",
    "LDAPSink",
    "OrganizationalUnitsSink",
    "UsersSink",
]
