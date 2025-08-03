"""LDAP connection management using flext-core patterns."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

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
        self._connection: Connection | None = None

    def connect(self) -> FlextResult[None]:
        """Establish LDAP connection."""
        try:
            # Check if already connected
            if self._connection is not None:
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
                self._connection.unbind()  # type: ignore[no-untyped-call]
                self._connection = None
                logger.info("LDAP connection closed")

            return FlextResult.ok(None)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP disconnect failed")
            return FlextResult.fail(f"Disconnect failed: {e}")

    def test_connection(self) -> FlextResult[bool]:
        """Test LDAP connection."""
        try:
            if self._connection is None:
                connect_result = self.connect()
                if not connect_result.is_success:
                    error_msg = connect_result.error or "Connection failed"
                    return FlextResult.fail(error_msg)

            # Test with simple search (connection is guaranteed to be not None after successful connect)
            assert self._connection is not None  # noqa: S101, "Connection should not be None after successful connect"
            search_result = self._connection.search(
                self.config.base_dn,
                "(objectClass=*)",
                search_scope="BASE",
                attributes=["objectClass"],
            )

            if search_result:
                return FlextResult.ok(data=True)
            return FlextResult.fail("Connection test search failed")

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("LDAP connection test failed")
            return FlextResult.fail(f"Connection test failed: {e}")

    def search(
        self,
        search_base: str,
        search_filter: str,
        attributes: list[str] | None = None,
        search_scope: Literal["BASE", "LEVEL", "SUBTREE"] = "SUBTREE",
    ) -> FlextResult[list[dict[str, object]]]:
        """Execute LDAP search and return results."""
        try:
            if self._connection is None:
                connect_result = self.connect()
                if not connect_result.is_success:
                    error_msg = connect_result.error or "Connection failed"
                    return FlextResult.fail(error_msg)

            # Connection is guaranteed to be not None after successful connect
            assert self._connection is not None  # noqa: S101, "Connection should not be None after successful connect"
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
            assert self._connection is not None  # noqa: S101, "Connection should not be None after successful search"
            results = []
            for entry in self._connection.entries:
                entry_dict = {"dn": str(entry.entry_dn)}
                for attr_name in entry.entry_attributes:
                    entry_dict[attr_name] = entry[attr_name].values
                results.append(entry_dict)

            return FlextResult.ok(results)  # type: ignore[arg-type]

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP search failed: {search_filter}")
            return FlextResult.fail(f"Search failed: {e}")

    def add_entry(self, dn: str, attributes: dict[str, object]) -> FlextResult[bool]:
        """Add new LDAP entry."""
        try:
            if self._connection is None:
                connect_result = self.connect()
                if not connect_result.is_success:
                    error_msg = connect_result.error or "Connection failed"
                    return FlextResult.fail(error_msg)

            # Connection is guaranteed to be not None after successful connect
            assert self._connection is not None  # noqa: S101, "Connection should not be None after successful connect"
            add_result = self._connection.add(dn, attributes=attributes)  # type: ignore[no-untyped-call]

            if add_result:
                logger.info(f"Added LDAP entry: {dn}")
                return FlextResult.ok(data=True)

            assert self._connection is not None  # noqa: S101, "Connection should not be None after operation"
            error_msg = f"Add failed: {self._connection.result}"
            return FlextResult.fail(error_msg)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP add entry failed: {dn}")
            return FlextResult.fail(f"Add entry failed: {e}")

    def modify_entry(self, dn: str, changes: dict[str, object]) -> FlextResult[bool]:
        """Modify existing LDAP entry."""
        try:
            if self._connection is None:
                connect_result = self.connect()
                if not connect_result.is_success:
                    error_msg = connect_result.error or "Connection failed"
                    return FlextResult.fail(error_msg)

            # Connection is guaranteed to be not None after successful connect
            assert self._connection is not None  # noqa: S101, "Connection should not be None after successful connect"
            modify_result = self._connection.modify(dn, changes)  # type: ignore[no-untyped-call]

            if modify_result:
                logger.info(f"Modified LDAP entry: {dn}")
                return FlextResult.ok(data=True)

            assert self._connection is not None  # noqa: S101, "Connection should not be None after operation"
            error_msg = f"Modify failed: {self._connection.result}"
            return FlextResult.fail(error_msg)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP modify entry failed: {dn}")
            return FlextResult.fail(f"Modify entry failed: {e}")

    def delete_entry(self, dn: str) -> FlextResult[bool]:
        """Delete LDAP entry."""
        try:
            if self._connection is None:
                connect_result = self.connect()
                if not connect_result.is_success:
                    error_msg = connect_result.error or "Connection failed"
                    return FlextResult.fail(error_msg)

            # Connection is guaranteed to be not None after successful connect
            assert self._connection is not None  # noqa: S101, "Connection should not be None after successful connect"
            delete_result = self._connection.delete(dn)  # type: ignore[no-untyped-call]

            if delete_result:
                logger.info(f"Deleted LDAP entry: {dn}")
                return FlextResult.ok(data=True)

            assert self._connection is not None  # noqa: S101, "Connection should not be None after operation"
            error_msg = f"Delete failed: {self._connection.result}"
            return FlextResult.fail(error_msg)

        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception(f"LDAP delete entry failed: {dn}")
            return FlextResult.fail(f"Delete entry failed: {e}")

    @property
    def is_connected(self) -> bool:
        """Check if connection is active."""
        return self._connection is not None and self._connection.bound
