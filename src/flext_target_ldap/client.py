"""LDAP client implementation for target-ldap using flext-core patterns.

MIGRATED TO LDAP3:
Provides enterprise-grade LDAP connectivity with ServiceResult pattern support
using ldap3 (modern, typed LDAP library with better Python 3.13 support).
"""

from __future__ import annotations

import contextlib
import logging
from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, Any, Literal

import ldap3

# 🚨 ARCHITECTURAL COMPLIANCE
from flext_target_ldap.infrastructure.di_container import (
    get_domain_entity,
    get_field,
    get_service_result,
)

ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()
from ldap3.core import exceptions as ldap3_exceptions
from pydantic import Field

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator, Mapping
logger = logging.getLogger(__name__)


class LDAPEntry(DomainBaseModel):
    """LDAP entry model using flext-core patterns."""

    dn: str
    attributes: dict[str, list[str]] = Field(default_factory=dict)

    def add_attribute(self, name: str, values: list[str] | str) -> None:
        """Add attribute values to the entry."""
        if isinstance(values, str):
            values = [values]
        self.attributes[name] = values

    def remove_attribute(self, name: str) -> None:
        """Remove attribute from the entry."""
        self.attributes.pop(name, None)


class LDAPClient:
    """LDAP client for connecting and modifying LDAP directories using flext-core and ldap3."""

    def __init__(
        self,
        host: str,
        port: int = 389,
        bind_dn: str | None = None,
        password: str | None = None,
        *,
        use_ssl: bool = False,
        use_start_tls: bool = False,
        timeout: int = 30,
        pool_size: int = 5,
        pool_keepalive: int = 10,
    ) -> None:
        """Initialize LDAP client with ldap3.

        Args:
            host: LDAP server hostname
            port: LDAP server port
            bind_dn: Bind DN for authentication
            password: Bind password
            use_ssl: Use LDAPS/SSL connection
            use_start_tls: Use StartTLS for secure connection
            timeout: Connection timeout in seconds
            pool_size: Connection pool size
            pool_keepalive: Connection pool keepalive in seconds

        """
        self.host = host
        self.port = port
        self.bind_dn = bind_dn
        self.password = password
        self.use_ssl = use_ssl
        self.use_start_tls = use_start_tls
        self.timeout = timeout
        self.pool_size = pool_size
        self.pool_keepalive = pool_keepalive
        # Create server object
        self._server = ldap3.Server(
            host=self.host,
            port=self.port,
            use_ssl=self.use_ssl,
            get_info=ldap3.ALL,
            connect_timeout=self.timeout,
        )
        # Server pool for connection reuse
        self._server_pool: ldap3.ServerPool | None = None

    @property
    def server_uri(self) -> str:
        """Get the LDAP server URI."""
        protocol = "ldaps" if self.use_ssl else "ldap"
        return f"{protocol}://{self.host}:{self.port}"

    def _create_server_pool(self) -> ldap3.ServerPool:
        """Create server pool for efficient connection reuse."""
        if self._server_pool is None:
            self._server_pool = ldap3.ServerPool(
                servers=[self._server],
                pool_strategy=ldap3.ROUND_ROBIN,
                active=True,
                exhaust=False,
            )
        return self._server_pool

    @contextmanager
    def get_connection(self) -> Generator[ldap3.Connection]:
        """Context manager for LDAP connections using ldap3."""
        # Use server pool for better performance
        server_pool = self._create_server_pool()
        connection = ldap3.Connection(
            server_pool,
            user=self.bind_dn,
            password=self.password,
        )
        try:
            # Open connection
            if not connection.bind():
                msg = f"Failed to bind to LDAP server: {connection.result}"
                raise ldap3_exceptions.LDAPBindError(
                    msg,
                )
            # Handle StartTLS if requested
            if self.use_start_tls and not self.use_ssl:
                if not connection.start_tls():
                    msg = f"Failed to start TLS: {connection.result}"
                    raise ldap3_exceptions.LDAPException(
                        msg,
                    )
            logger.info("Successfully connected to LDAP server %s", self.server_uri)
            yield connection
        except ldap3_exceptions.LDAPException as e:
            logger.exception("LDAP connection error for %s: %s", self.server_uri, e)
            raise
        except Exception as e:
            logger.exception(
                "Unexpected connection error for %s: %s",
                self.server_uri,
                e,
            )
            raise
        finally:
            try:
                if connection.bound:
                    connection.unbind()
                    logger.debug("Disconnected from LDAP server")
            except ldap3_exceptions.LDAPException:
                logger.warning("Error during LDAP disconnect")

    @asynccontextmanager
    async def get_async_connection(self) -> AsyncGenerator[ldap3.Connection]:
        """Async context manager for LDAP connections."""
        # ldap3 doesn't have native async support, but we can wrap it
        connection = ldap3.Connection(
            self._server,
            user=self.bind_dn,
            password=self.password,
        )
        try:
            if not connection.bind():
                msg = f"Failed to bind to LDAP server: {connection.result}"
                raise ldap3_exceptions.LDAPBindError(
                    msg,
                )
            if self.use_start_tls and not self.use_ssl:
                if not connection.start_tls():
                    msg = f"Failed to start TLS: {connection.result}"
                    raise ldap3_exceptions.LDAPException(
                        msg,
                    )
            logger.info(
                "Successfully connected to async LDAP server %s",
                self.server_uri,
            )
            yield connection
        except ldap3_exceptions.LDAPException as e:
            logger.exception(
                "Async LDAP connection error for %s: %s",
                self.server_uri,
                e,
            )
            raise
        finally:
            try:
                if connection.bound:
                    connection.unbind()
                    logger.debug("Disconnected from async LDAP server")
            except ldap3_exceptions.LDAPException:
                logger.warning("Error during async LDAP disconnect")

    def add_entry(
        self,
        dn: str,
        object_class: str | list[str],
        attributes: Mapping[str, Any],
    ) -> ServiceResult[Any]:
        """Add an entry to LDAP using ldap3."""
        try:
            with self.get_connection() as conn:
                # Ensure object_class is a list
                if isinstance(object_class, str):
                    object_class = [object_class]
                # Build attributes dict - ldap3 handles string/list conversion automatically
                attrs = dict(attributes)
                # Ensure objectClass is properly set
                attrs["objectClass"] = object_class
                # Perform add operation
                success = conn.add(dn, attributes=attrs)
                if success:
                    logger.info("Successfully added entry: %s", dn)
                    return ServiceResult.ok(True)
                error_msg = f"Failed to add entry {dn}: {conn.result}"
                logger.error(error_msg)
                return ServiceResult.fail(error_msg)
        except ldap3_exceptions.LDAPEntryAlreadyExistsResult:
            error_msg = f"Entry already exists: {dn}"
            logger.warning(error_msg)
            return ServiceResult.fail(error_msg)
        except ldap3_exceptions.LDAPException as e:
            error_msg = f"LDAP error adding entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error adding entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def modify_entry(
        self,
        dn: str,
        changes: Mapping[str, Any],
    ) -> ServiceResult[Any]:
        """Modify an existing LDAP entry using ldap3."""
        try:
            with self.get_connection() as conn:
                # Build modification dict using ldap3 format
                modifications: dict[str, Any] = {}
                for attr_name, new_value in changes.items():
                    if new_value is None:
                        # Delete attribute
                        modifications[attr_name] = [(ldap3.MODIFY_DELETE, [])]
                    elif isinstance(new_value, list):
                        # Replace attribute with list
                        modifications[attr_name] = [(ldap3.MODIFY_REPLACE, new_value)]
                    else:
                        # Replace attribute with single value
                        modifications[attr_name] = [(ldap3.MODIFY_REPLACE, [new_value])]
                # Perform modify operation
                success = conn.modify(dn, modifications)
                if success:
                    logger.info("Successfully modified entry: %s", dn)
                    return ServiceResult.ok(True)
                error_msg = f"Failed to modify entry {dn}: {conn.result}"
                logger.error(error_msg)
                return ServiceResult.fail(error_msg)
        except ldap3_exceptions.LDAPNoSuchObjectResult:
            error_msg = f"Entry not found: {dn}"
            logger.warning(error_msg)
            return ServiceResult.fail(error_msg)
        except ldap3_exceptions.LDAPException as e:
            error_msg = f"LDAP error modifying entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error modifying entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def delete_entry(self, dn: str) -> ServiceResult[Any]:
        """Delete an LDAP entry using ldap3."""
        try:
            with self.get_connection() as conn:
                success = conn.delete(dn)
                if success:
                    logger.info("Successfully deleted entry: %s", dn)
                    return ServiceResult.ok(True)
                error_msg = f"Failed to delete entry {dn}: {conn.result}"
                logger.error(error_msg)
                return ServiceResult.fail(error_msg)
        except ldap3_exceptions.LDAPNoSuchObjectResult:
            error_msg = f"Entry not found: {dn}"
            logger.warning(error_msg)
            return ServiceResult.fail(error_msg)
        except ldap3_exceptions.LDAPException as e:
            error_msg = f"LDAP error deleting entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error deleting entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def search_entry(
        self,
        base_dn: str,
        search_filter: str = "(objectClass=*)",
        scope: Literal["BASE", "LEVEL", "SUBTREE"] = "BASE",
        attributes: list[str] | None = None,
    ) -> ServiceResult[Any]:
        """Search for LDAP entries using ldap3."""
        try:
            with self.get_connection() as conn:
                success = conn.search(
                    search_base=base_dn,
                    search_filter=search_filter,
                    search_scope=scope,
                    attributes=attributes or ldap3.ALL_ATTRIBUTES,
                )
                if not success:
                    error_msg = f"Search failed for base {base_dn}: {conn.result}"
                    logger.error(error_msg)
                    return ServiceResult.fail(error_msg)
                entries = []
                for entry in conn.entries:
                    # Convert ldap3 entry to our LDAPEntry format
                    attrs = {}
                    for attr_name in entry.entry_attributes:
                        attr_values = getattr(entry, attr_name)
                        if isinstance(attr_values, list):
                            attrs[attr_name] = [str(v) for v in attr_values]
                        else:
                            attrs[attr_name] = [str(attr_values)]
                    entries.append(LDAPEntry(dn=str(entry.entry_dn), attributes=attrs))
                logger.info(
                    "Found %d entries for search base: %s",
                    len(entries),
                    base_dn,
                )
                return ServiceResult.ok(entries)
        except ldap3_exceptions.LDAPNoSuchObjectResult:
            logger.info("No entries found for search base: %s", base_dn)
            return ServiceResult.ok([])
        except ldap3_exceptions.LDAPException as e:
            error_msg = f"LDAP error searching entries in {base_dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error searching entries in {base_dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def entry_exists(self, dn: str) -> ServiceResult[Any]:
        """Check if an LDAP entry exists using ldap3."""
        search_result = self.search_entry(dn, scope="BASE")
        if not search_result.success:
            error_msg = (
                search_result.error or "Unknown error during entry existence check"
            )
            return ServiceResult.fail(error_msg)

        # Check if data exists and is not None before using len
        if search_result.data is None:
            return ServiceResult.ok(False)

        # Type cast to ensure data is treated as a list
        data_list = search_result.data if isinstance(search_result.data, list) else []
        exists = len(data_list) > 0
        return ServiceResult.ok(exists)

    def get_entry(
        self,
        dn: str,
        attributes: list[str] | None = None,
    ) -> ServiceResult[Any]:
        """Get a single LDAP entry by DN using ldap3."""
        search_result = self.search_entry(dn, scope="BASE", attributes=attributes)
        if not search_result.success:
            error_msg = search_result.error or "Unknown error during entry retrieval"
            return ServiceResult.fail(error_msg)
        entries = search_result.data
        if not entries:
            return ServiceResult.ok(None)
        return ServiceResult.ok(entries[0])

    def upsert_entry(
        self,
        dn: str,
        object_classes: list[str],
        attributes: dict[str, list[str]],
    ) -> ServiceResult[Any]:
        """Add or update an LDAP entry (upsert operation) using ldap3.

        Returns:
            ServiceResult containing tuple of (dn, operation) where operation is "add" or "modify"

        """
        # Check if entry exists
        exists_result = self.entry_exists(dn)
        if not exists_result.success:
            return ServiceResult.fail(
                f"Failed to check if entry exists: {exists_result.error}",
            )
        if exists_result.data:
            # Entry exists, modify it
            modify_result = self.modify_entry(dn, attributes)
            if modify_result.success:
                return ServiceResult.ok(dn)
            return ServiceResult(
                success=True,
                error=f"Modify failed: {modify_result.error}",
            )
        # Entry doesn't exist, add it
        add_result = self.add_entry(dn, object_classes, attributes)
        if add_result.success:
            return ServiceResult.ok(dn)
        return ServiceResult.fail(f"Add failed: {add_result.error}")

    def validate_dn(self, dn: str) -> ServiceResult[Any]:
        """Validate DN format and structure using ldap3 utilities.

        Args:
            dn: Distinguished Name to validate
        Returns:
            ServiceResult with True if DN is valid, False otherwise

        """
        if not dn or not isinstance(dn, str):
            return ServiceResult.fail("DN must be a non-empty string")
        try:
            # Use ldap3's DN parsing capabilities for validation
            from ldap3.utils import dn as ldap3_dn

            parsed_dn = ldap3_dn.parse_dn(dn)
            if not parsed_dn:
                return ServiceResult.fail("DN could not be parsed")
            # Check for at least one component
            if len(parsed_dn) == 0:
                return ServiceResult.fail(
                    "DN must contain at least one component",
                )
            # Validate that we have standard LDAP attributes
            valid_attributes = {"cn", "uid", "ou", "dc", "o", "c", "street", "l", "st"}
            has_valid_attr = any(
                component[0].lower() in valid_attributes for component in parsed_dn
            )
            if not has_valid_attr:
                return ServiceResult.fail(
                    "DN should contain standard LDAP attributes",
                )
            return ServiceResult.ok(True)
        except Exception as e:
            return ServiceResult.fail(f"DN validation failed: {e}")

    def close_server_pool(self) -> None:
        """Close the server pool and cleanup resources."""
        if self._server_pool:
            try:
                # ldap3 server pools are automatically cleaned up
                self._server_pool = None
                # Only log if logger is still available
                with contextlib.suppress(ValueError, OSError):
                    logger.info("LDAP server pool closed")
            except Exception as e:
                # Log exception during shutdown if possible
                with contextlib.suppress(Exception):
                    logger.warning(f"Error during LDAP cleanup: {e}")

    def __del__(self) -> None:
        """Cleanup server pool on object destruction."""
        self.close_server_pool()
