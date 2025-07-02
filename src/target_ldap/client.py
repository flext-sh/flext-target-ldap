"""LDAP client implementation for target-ldap.

This module provides the LDAP client that handles connections and operations
for loading data into LDAP directories.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

import ldap3
from ldap3 import (
    ALL,
    MODIFY_ADD,
    MODIFY_DELETE,
    MODIFY_REPLACE,
    SIMPLE,
    Connection,
    Server,
)
from ldap3.core.exceptions import LDAPException

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping


logger = logging.getLogger(__name__)


class LDAPClient:
    """LDAP client for connecting and modifying LDAP directories."""

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
        """Initialize LDAP client.

        Args:
        ----
            host: LDAP server hostname or IP
            port: LDAP server port
            bind_dn: Distinguished name for binding
            password: Password for authentication
            use_ssl: Whether to use SSL/TLS
            timeout: Connection timeout in seconds
            auto_bind: Whether to auto-bind on connection

        """
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
        """Get LDAP connection context manager.

        Yields
        ------
            Active LDAP connection

        Raises
        ------
            LDAPException: If connection fails

        """
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
            logger.info("Connected to LDAP server: %s", self.server_uri)
            yield connection
        finally:
            if connection.bound:
                connection.unbind()                logger.info("Disconnected from LDAP server")

    def add_entry(
        self,
        dn: str,
        object_class: str | list[str],
        attributes: Mapping[str, Any],
    ) -> bool:
        """Add a new entry to LDAP.

        Args:
        ----
            dn: Distinguished name of the entry
            object_class: Object class(es) for the entry
            attributes: Entry attributes

        Returns:
        -------
            True if successful

        Raises:
        ------
            LDAPException: If add operation fails

        """
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
                raise LDAPException(error_msg)

            logger.info("Successfully added entry: %s", dn)
            return True

    def modify_entry(
        self,
        dn: str,
        changes: Mapping[str, Any],
        operation: str = "replace",
    ) -> bool:
        """Modify an existing LDAP entry.

        Args:
        ----
            dn: Distinguished name of the entry
            changes: Dictionary of attribute changes
            operation: Modification operation (replace, add, delete)

        Returns:
        -------
            True if successful

        Raises:
        ------
            LDAPException: If modify operation fails

        """
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
                raise LDAPException(error_msg)

            logger.info("Successfully modified entry: %s", dn)
            return True

    def delete_entry(self, dn: str) -> bool:
        """Delete an entry from LDAP.

        Args:
        ----
            dn: Distinguished name of the entry

        Returns:
        -------
            True if successful

        Raises:
        ------
            LDAPException: If delete operation fails

        """
        with self.get_connection() as conn:
            result = conn.delete(dn)
            if not result:
                error_msg = f"Failed to delete entry {dn}: {conn.result}"
                logger.error(error_msg)
                raise LDAPException(error_msg)

            logger.info("Successfully deleted entry: %s", dn)
            return True

    def entry_exists(self, dn: str) -> bool:
        """Check if an entry exists in LDAP.

        Args:
        ----
            dn: Distinguished name of the entry

        Returns:
        -------
            True if entry exists, False otherwise

        """
        with self.get_connection() as conn:
            result = conn.search(
                search_base=dn,
                search_filter="(objectClass=*)",
                search_scope=ldap3.BASE,
                attributes=["dn"],
                size_limit=1,
            )
            return bool(result and conn.entries)

    def upsert_entry(
        self,
        dn: str,
        object_class: str | list[str],
        attributes: Mapping[str, Any],
    ) -> tuple[bool, str]:
        """Insert or update an entry (upsert operation).

        Args:
        ----
            dn: Distinguished name of the entry
            object_class: Object class(es) for the entry
            attributes: Entry attributes

        Returns:
        -------
            Tuple of (success, operation) where operation is "add" or "modify"

        Raises:
        ------
            LDAPException: If operation fails

        """
        try:
            if self.entry_exists(dn):
                # Entry exists, perform modify
                self.modify_entry(dn, attributes, operation="replace")
                return (True, "modify")
            # Entry doesn't exist, perform add
            self.add_entry(dn, object_class, attributes)
            return (True, "add")
        except LDAPException:
            raise

    def validate_dn(self, dn: str) -> bool:
        """Validate DN syntax.

        Args:
        ----
            dn: Distinguished name to validate

        Returns:
        -------
            True if DN is valid

        """
        try:
            # Simple DN validation
            parts = dn.split(",")
            for part in parts:
                if "=" not in part:
                    return False
                key, value = part.strip().split("=", 1)
                if not key or not value:
                    return False
            return True
        except Exception:
            return False
