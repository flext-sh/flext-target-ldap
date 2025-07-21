"""LDAP client implementation for target-ldap using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Provides enterprise-grade LDAP connectivity with ServiceResult pattern support
using python-ldap (the original and most stable LDAP library).
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

# Import ldap with explicit version requirement
# python-ldap 3.4.4 should work with Python 3.13
import ldap
import ldap.modlist
from flext_core.domain.pydantic_base import DomainBaseModel
from flext_core.domain.types import ServiceResult
from pydantic import Field

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping

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
    """LDAP client for connecting and modifying LDAP directories using flext-core."""

    def __init__(
        self,
        host: str,
        port: int = 389,
        bind_dn: str | None = None,
        password: str | None = None,
        *,
        use_ssl: bool = False,
        timeout: int = 30,
    ) -> None:
        """Initialize LDAP client.

        Args:
            host: LDAP server hostname
            port: LDAP server port
            bind_dn: Bind DN for authentication
            password: Bind password
            use_ssl: Use LDAPS/SSL connection
            timeout: Connection timeout in seconds

        """
        self.host = host
        self.port = port
        self.bind_dn = bind_dn
        self.password = password
        self.use_ssl = use_ssl
        self.timeout = timeout
        self._connection: ldap.ldapobject.LDAPObject | None = None

    @property
    def server_uri(self) -> str:
        """Get the LDAP server URI."""
        protocol = "ldaps" if self.use_ssl else "ldap"
        return f"{protocol}://{self.host}:{self.port}"

    @contextmanager
    def get_connection(self) -> Generator[ldap.ldapobject.LDAPObject]:
        """Context manager for LDAP connections."""
        connection = None
        try:
            # Initialize connection
            connection = ldap.initialize(self.server_uri)

            # Set connection options
            connection.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
            connection.set_option(ldap.OPT_NETWORK_TIMEOUT, self.timeout)
            connection.set_option(ldap.OPT_REFERRALS, 0)

            # Start TLS if using SSL
            if self.use_ssl:
                connection.start_tls_s()

            # Bind if credentials provided
            if self.bind_dn and self.password:
                connection.simple_bind_s(self.bind_dn, self.password)
                logger.info("Successfully bound to LDAP server as %s", self.bind_dn)
            else:
                connection.simple_bind_s()
                logger.info("Successfully bound to LDAP server anonymously")

            logger.info("Connected to LDAP server %s", self.server_uri)
            yield connection

        except ldap.LDAPError as e:
            logger.exception("Failed to connect to LDAP server %s: %s", self.server_uri, e)
            raise
        finally:
            if connection:
                try:
                    connection.unbind_s()
                    logger.info("Disconnected from LDAP server")
                except ldap.LDAPError:
                    logger.warning("Error during LDAP disconnect")

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

                # Build attributes dict - python-ldap expects bytes values
                attrs = {}
                for key, value in attributes.items():
                    if isinstance(value, list):
                        attrs[key] = [str(v).encode("utf-8") for v in value]
                    else:
                        attrs[key] = [str(value).encode("utf-8")]

                # Add objectClass
                attrs["objectClass"] = [oc.encode("utf-8") for oc in object_class]

                # Convert to modlist format
                modlist = ldap.modlist.addModlist(attrs)

                # Perform add operation
                conn.add_s(dn, modlist)
                logger.info("Successfully added entry: %s", dn)
                return ServiceResult.ok(True)

        except ldap.ALREADY_EXISTS:
            error_msg = f"Entry already exists: {dn}"
            logger.warning(error_msg)
            return ServiceResult.fail(error_msg)
        except ldap.LDAPError as e:
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
    ) -> ServiceResult[bool]:
        """Modify an existing LDAP entry."""
        try:
            with self.get_connection() as conn:
                # Build modification list
                modlist = []
                for attr_name, new_value in changes.items():
                    if new_value is None:
                        # Delete attribute
                        modlist.append((ldap.MOD_DELETE, attr_name, None))
                    elif isinstance(new_value, list):
                        # Replace attribute with list
                        values = [str(v).encode("utf-8") for v in new_value]
                        modlist.append((ldap.MOD_REPLACE, attr_name, values))  # type: ignore[arg-type]
                    else:
                        # Replace attribute with single value
                        value = [str(new_value).encode("utf-8")]
                        modlist.append((ldap.MOD_REPLACE, attr_name, value))

                # Perform modify operation
                conn.modify_s(dn, modlist)
                logger.info("Successfully modified entry: %s", dn)
                return ServiceResult.ok(True)

        except ldap.NO_SUCH_OBJECT:
            error_msg = f"Entry not found: {dn}"
            logger.warning(error_msg)
            return ServiceResult.fail(error_msg)
        except ldap.LDAPError as e:
            error_msg = f"LDAP error modifying entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error modifying entry {dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def delete_entry(self, dn: str) -> ServiceResult[bool]:
        """Delete an LDAP entry."""
        try:
            with self.get_connection() as conn:
                conn.delete_s(dn)
                logger.info("Successfully deleted entry: %s", dn)
                return ServiceResult.ok(True)

        except ldap.NO_SUCH_OBJECT:
            error_msg = f"Entry not found: {dn}"
            logger.warning(error_msg)
            return ServiceResult.fail(error_msg)
        except ldap.LDAPError as e:
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
        scope: int = ldap.SCOPE_BASE,
        attributes: list[str] | None = None,
    ) -> ServiceResult[list[LDAPEntry]]:
        """Search for LDAP entries."""
        try:
            with self.get_connection() as conn:
                result = conn.search_s(
                    base_dn,
                    scope,
                    search_filter,
                    attributes or [],
                )

                entries = []
                for dn, attrs in result:
                    if dn is None:  # Skip referrals
                        continue

                    # Convert bytes values back to strings
                    decoded_attrs = {}
                    for attr_name, values in attrs.items():
                        decoded_attrs[attr_name] = [
                            v.decode("utf-8") for v in values
                        ]

                    entries.append(LDAPEntry(dn=dn, attributes=decoded_attrs))

                logger.info("Found %d entries for search base: %s", len(entries), base_dn)
                return ServiceResult.ok(entries)

        except ldap.NO_SUCH_OBJECT:
            logger.info("No entries found for search base: %s", base_dn)
            return ServiceResult.ok([])
        except ldap.LDAPError as e:
            error_msg = f"LDAP error searching entries in {base_dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error searching entries in {base_dn}: {e}"
            logger.exception(error_msg)
            return ServiceResult.fail(error_msg)

    def entry_exists(self, dn: str) -> ServiceResult[bool]:
        """Check if an LDAP entry exists."""
        search_result = self.search_entry(dn)
        if not search_result.is_success:
            return ServiceResult.fail(search_result.error)

        exists = len(search_result.unwrap()) > 0
        return ServiceResult.ok(exists)

    def get_entry(self, dn: str, attributes: list[str] | None = None) -> ServiceResult[LDAPEntry | None]:
        """Get a single LDAP entry by DN."""
        search_result = self.search_entry(dn, attributes=attributes)
        if not search_result.is_success:
            return ServiceResult.fail(search_result.error)

        entries = search_result.unwrap()
        if not entries:
            return ServiceResult.ok(None)

        return ServiceResult.ok(entries[0])

    def upsert_entry(
        self,
        dn: str,
        object_classes: list[str],
        attributes: dict[str, list[str]],
    ) -> ServiceResult[tuple[str, str]]:
        """Add or update an LDAP entry (upsert operation).

        Returns:
            ServiceResult containing tuple of (dn, operation) where operation is "add" or "modify"

        """
        # Check if entry exists
        exists_result = self.entry_exists(dn)
        if not exists_result.is_success:
            return ServiceResult.fail(f"Failed to check if entry exists: {exists_result.error}")

        if exists_result.data:
            # Entry exists, modify it
            modify_result = self.modify_entry(dn, attributes)
            if modify_result.is_success:
                return ServiceResult.ok((dn, "modify"))
            return ServiceResult.fail(f"Modify failed: {modify_result.error}")
        # Entry doesn't exist, add it
        all_attributes = {**attributes, "objectClass": object_classes}
        add_result = self.add_entry(dn, all_attributes)
        if add_result.is_success:
            return ServiceResult.ok((dn, "add"))
        return ServiceResult.fail(f"Add failed: {add_result.error}")

    def validate_dn(self, dn: str) -> ServiceResult[bool]:
        """Validate DN format and structure.

        Args:
            dn: Distinguished Name to validate

        Returns:
            ServiceResult with True if DN is valid, False otherwise

        """
        if not dn or not isinstance(dn, str):
            return ServiceResult.fail("DN must be a non-empty string")

        # Basic DN validation - check for required components
        import re
        # DN must have at least one component with = sign
        if not re.search(r"[^=]+=.+", dn):
            return ServiceResult.fail("DN must contain at least one attribute=value component")

        # Check for common DN component patterns
        if not re.search(r"(cn|uid|ou|dc|o)=", dn.lower()):
            return ServiceResult.fail("DN should contain standard components (cn, uid, ou, dc, o)")

        return ServiceResult.ok(True)
