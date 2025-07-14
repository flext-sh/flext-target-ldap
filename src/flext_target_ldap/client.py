"""LDAP client implementation for target-ldap using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Provides enterprise-grade LDAP connectivity with ServiceResult pattern support.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING
from typing import Any

import ldap3
from ldap3 import ALL
from ldap3 import MODIFY_ADD
from ldap3 import MODIFY_DELETE
from ldap3 import MODIFY_REPLACE
from ldap3 import SIMPLE
from ldap3 import Connection
from ldap3 import Server
from ldap3.core.exceptions import LDAPException

from flext_core.domain.pydantic_base import DomainBaseModel

if TYPE_CHECKING:
    from collections.abc import Generator
    from collections.abc import Mapping

logger = logging.getLogger(__name__)


# Use centralized ServiceResult from flext-core - ELIMINATE DUPLICATION
from flext_core.domain.types import ServiceResult


class LDAPEntry(DomainBaseModel):
    """Represents an LDAP entry for target operations using flext-core patterns."""

    dn: str
    attributes: dict[str, Any]
    object_classes: list[str]

    def add_attribute(self, name: str, values: list[str] | str) -> None:
        """Add attribute values to the entry."""
        if isinstance(values, str):
            values = [values]
        self.attributes[name] = values

    def remove_attribute(self, name: str) -> None:
        """Remove attribute from the entry."""
        self.attributes.pop(name, None)


class LDAPClient:
    """LDAP client for connecting and modifying LDAP directories using flext-core patterns."""

    def __init__(
        self,
        host: str,
        port: int = 389,
        bind_dn: str | None = None,
        password: str | None = None,
        *,
        use_ssl: bool = False,
        timeout: int = 30,
        auto_bind: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.bind_dn = bind_dn
        self.password = password
        self.use_ssl = use_ssl
        self.timeout = timeout
        self.auto_bind = auto_bind
        self._connection: Connection | None = None

    @property
    def server_uri(self) -> str:
        """Get the LDAP server URI."""
        protocol = "ldaps" if self.use_ssl else "ldap"
        return f"{protocol}://{self.host}:{self.port}"

    @contextmanager
    def get_connection(self) -> Generator[Connection]:
        """Context manager for LDAP connections."""
        server = Server(
            self.host,
            port=self.port,
            use_ssl=self.use_ssl,
            get_info=ALL,
            connect_timeout=self.timeout,
        )

        connection = Connection(
            server,
            user=self.bind_dn,
            password=self.password,
            authentication=SIMPLE if self.bind_dn else None,
            auto_bind=self.auto_bind,
            raise_exceptions=True,
        )

        try:
            logger.info("Connected to LDAP server %s", self.server_uri)
            yield connection
        finally:
            if connection.bound:
                connection.unbind()
                logger.info("Disconnected from LDAP server")

    def add_entry(
        self,
        dn: str,
        object_class: str | list[str],
        attributes: Mapping[str, Any],
    ) -> ServiceResult[bool]:
        """Add an entry to LDAP."""
        try:
            with self.get_connection() as conn:
                # Ensure object_class is a list
                if isinstance(object_class, str):
                    object_class = [object_class]

                # Build attributes dict
                attrs = dict(attributes)
                attrs["objectClass"] = object_class

                # Perform add operation
                result = conn.add(dn, attributes=attrs)
                if not result:
                    error_msg = f"Failed to add entry {dn}: {conn.result}"
                    logger.error(error_msg)
                    return ServiceResult.fail(error_msg)

                logger.info("Successfully added entry: %s", dn)
                return ServiceResult.ok(True)
        except LDAPException as e:
            error_msg = f"LDAP error adding entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def modify_entry(
        self,
        dn: str,
        changes: Mapping[str, Any],
        operation: str = "replace",
    ) -> ServiceResult[bool]:
        """Modify an entry in LDAP."""
        try:
            with self.get_connection() as conn:
                # Map operation names to LDAP constants
                op_map = {
                    "replace": MODIFY_REPLACE,
                    "add": MODIFY_ADD,
                    "delete": MODIFY_DELETE,
                }

                mod_op = op_map.get(operation.lower(), MODIFY_REPLACE)

                # Build modification list
                mod_list: dict[str, list[Any]] = {}
                for attr, value in changes.items():
                    # Skip empty values for delete operations
                    if operation == "delete" and not value:
                        mod_list[attr] = [(mod_op, [])]
                    else:
                        mod_list[attr] = [(mod_op, value)]

                # Perform modify operation
                result = conn.modify(dn, mod_list)
                if not result:
                    error_msg = f"Failed to modify entry {dn}: {conn.result}"
                    logger.error(error_msg)
                    return ServiceResult.fail(error_msg)

                logger.info("Successfully modified entry: %s", dn)
                return ServiceResult.ok(True)
        except LDAPException as e:
            error_msg = f"LDAP error modifying entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def delete_entry(self, dn: str) -> ServiceResult[bool]:
        """Delete an entry from LDAP."""
        try:
            with self.get_connection() as conn:
                result = conn.delete(dn)
                if not result:
                    error_msg = f"Failed to delete entry {dn}: {conn.result}"
                    logger.error(error_msg)
                    return ServiceResult.fail(error_msg)

                logger.info("Successfully deleted entry: %s", dn)
                return ServiceResult.ok(True)
        except LDAPException as e:
            error_msg = f"LDAP error deleting entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def entry_exists(self, dn: str) -> ServiceResult[bool]:
        """Check if an entry exists in LDAP."""
        try:
            with self.get_connection() as conn:
                result = conn.search(
                    search_base=dn,
                    search_filter="(objectClass=*)",
                    search_scope=ldap3.BASE,
                    attributes=["dn"],
                    size_limit=1,
                )
                exists = bool(result and conn.entries)
                return ServiceResult.ok(exists)
        except LDAPException as e:
            error_msg = f"LDAP error checking entry existence {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def upsert_entry(
        self,
        dn: str,
        object_class: str | list[str],
        attributes: Mapping[str, Any],
    ) -> ServiceResult[tuple[bool, str]]:
        """Insert or update an entry (upsert operation)."""
        try:
            exists_result = self.entry_exists(dn)
            if not exists_result.is_success:
                return ServiceResult.fail(exists_result.error or "Entry check failed")

            if exists_result.value:
                # Entry exists, perform modify
                modify_result = self.modify_entry(dn, attributes, operation="replace")
                if not modify_result.is_success:
                    return ServiceResult.fail(
                        modify_result.error or "Modify operation failed"
                    )
                return ServiceResult.ok((True, "modify"))

            # Entry doesn't exist, perform add
            add_result = self.add_entry(dn, object_class, attributes)
            if not add_result.is_success:
                return ServiceResult.fail(add_result.error or "Add operation failed")
            return ServiceResult.ok((True, "add"))

        except Exception as e:
            error_msg = f"Error during upsert operation for {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def validate_dn(self, dn: str) -> ServiceResult[bool]:
        """Validate a distinguished name format."""
        try:
            # Simple DN validation
            parts = dn.split(",")
            for part in parts:
                if "=" not in part:
                    return ServiceResult.fail(f"Invalid DN part: {part}")
                key, value = part.strip().split("=", 1)
                if not key or not value:
                    return ServiceResult.fail(f"Empty key or value in DN part: {part}")
            return ServiceResult.ok(True)
        except Exception as e:
            error_msg = f"Error validating DN {dn}: {e}"
            return ServiceResult.fail(error_msg)

    def test_connection(self) -> ServiceResult[bool]:
        """Test the LDAP connection."""
        try:
            with self.get_connection() as conn:
                # Perform a simple search to test the connection
                conn.search(
                    search_base="",
                    search_filter="(objectClass=*)",
                    search_scope=ldap3.BASE,
                    attributes=["namingContexts"],
                    size_limit=1,
                )
                return ServiceResult.ok(True)
        except Exception as e:
            error_msg = f"Connection test failed: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)


# Export main classes and functions
__all__ = [
    "LDAPClient",
    "LDAPEntry",
    "ServiceResult",
]
