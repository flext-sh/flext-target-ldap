"""LDAP connection management using flext-core patterns."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Import from flext-core for foundational patterns
from flext_core import FlextResult, get_logger
from ldap3 import Connection, Server

if TYPE_CHECKING:
    from flext_target_ldap.connection.config import LDAPConnectionConfig

logger = get_logger(__name__)


class LDAPConnection:
    """LDAP connection using flext-core patterns."""

    def __init__(self, config: LDAPConnectionConfig) -> None:
        """Initialize LDAP connection."""
        self.config = config
        self._connection = None

    def connect(self) -> FlextResult[None]:
        """Establish LDAP connection."""
        try:
            # ldap3 already imported at module level
            # Check if Connection and Server are available
            if not Connection or not Server:
                return FlextResult.fail("ldap3 package not properly imported")

            if self._connection:
                return FlextResult.ok(None)

            # Create server and connection
            server = Server(
                self.config.build_connection_string(),
                use_ssl=self.config.use_tls,
                connect_timeout=self.config.connection_timeout,
            )

            self._connection = Connection(
                server,
                user=self.config.bind_dn,
                password=self.config.bind_password,
                auto_bind=True,
                raise_exceptions=True,
            )

            logger.info(f"Connected to LDAP server: {self.config.server_url}")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP connection failed")
            return FlextResult.fail(f"Connection failed: {e}")

    def disconnect(self) -> FlextResult[None]:
        """Close LDAP connection."""
        try:
            if self._connection:
                self._connection.unbind()
                self._connection = None
                logger.info("LDAP connection closed")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP disconnect failed")
            return FlextResult.fail(f"Disconnect failed: {e}")

    def test_connection(self) -> FlextResult[bool]:
        """Test LDAP connection."""
        try:
            if not self._connection:
                connect_result = self.connect()
                if not connect_result.is_success:
                    return FlextResult.fail(connect_result.error)

            # Test with simple search
            search_result = self._connection.search(
                self.config.base_dn,
                "(objectClass=*)",
                search_scope="BASE",
                attributes=["objectClass"],
            )

            if search_result:
                return FlextResult.ok(True)
            return FlextResult.fail("Connection test search failed")

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP connection test failed")
            return FlextResult.fail(f"Connection test failed: {e}")

    def search(
        self,
        search_base: str,
        search_filter: str,
        attributes: list[str] | None = None,
        search_scope: str = "SUBTREE",
    ) -> FlextResult[list[dict[str, Any]]]:
        """Execute LDAP search and return results."""
        try:
            if not self._connection:
                connect_result = self.connect()
                if not connect_result.is_success:
                    return FlextResult.fail(connect_result.error)

            search_result = self._connection.search(
                search_base,
                search_filter,
                search_scope=search_scope,
                attributes=attributes or [],
                paged_size=self.config.page_size,
                time_limit=self.config.search_timeout,
            )

            if not search_result:
                return FlextResult.ok([])

            # Convert entries to dictionaries
            results = []
            for entry in self._connection.entries:
                entry_dict = {"dn": str(entry.entry_dn)}
                for attr_name in entry.entry_attributes:
                    entry_dict[attr_name] = entry[attr_name].values
                results.append(entry_dict)

            return FlextResult.ok(results)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP search failed: {search_filter}")
            return FlextResult.fail(f"Search failed: {e}")

    def add_entry(self, dn: str, attributes: dict[str, Any]) -> FlextResult[bool]:
        """Add new LDAP entry."""
        try:
            if not self._connection:
                connect_result = self.connect()
                if not connect_result.is_success:
                    return FlextResult.fail(connect_result.error)

            add_result = self._connection.add(dn, attributes=attributes)

            if add_result:
                logger.info(f"Added LDAP entry: {dn}")
                return FlextResult.ok(True)

            error_msg = f"Add failed: {self._connection.result}"
            return FlextResult.fail(error_msg)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP add entry failed: {dn}")
            return FlextResult.fail(f"Add entry failed: {e}")

    def modify_entry(self, dn: str, changes: dict[str, Any]) -> FlextResult[bool]:
        """Modify existing LDAP entry."""
        try:
            if not self._connection:
                connect_result = self.connect()
                if not connect_result.is_success:
                    return FlextResult.fail(connect_result.error)

            modify_result = self._connection.modify(dn, changes)

            if modify_result:
                logger.info(f"Modified LDAP entry: {dn}")
                return FlextResult.ok(True)

            error_msg = f"Modify failed: {self._connection.result}"
            return FlextResult.fail(error_msg)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP modify entry failed: {dn}")
            return FlextResult.fail(f"Modify entry failed: {e}")

    def delete_entry(self, dn: str) -> FlextResult[bool]:
        """Delete LDAP entry."""
        try:
            if not self._connection:
                connect_result = self.connect()
                if not connect_result.is_success:
                    return FlextResult.fail(connect_result.error)

            delete_result = self._connection.delete(dn)

            if delete_result:
                logger.info(f"Deleted LDAP entry: {dn}")
                return FlextResult.ok(True)

            error_msg = f"Delete failed: {self._connection.result}"
            return FlextResult.fail(error_msg)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP delete entry failed: {dn}")
            return FlextResult.fail(f"Delete entry failed: {e}")

    @property
    def is_connected(self) -> bool:
        """Check if connection is active."""
        return self._connection is not None and self._connection.bound
