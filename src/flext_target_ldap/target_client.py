"""LDAP Target Client - PEP8 Consolidation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import sys
from collections.abc import Generator, Mapping
from contextlib import AbstractContextManager, contextmanager
from typing import TypeIs, override

from flext_core import FlextContainer, FlextLogger, p, r
from flext_ldap import (
    FlextLdap,
    FlextLdapConnection,
    FlextLdapModels,
    FlextLdapOperations,
)
from flext_ldif import FlextLdif

from flext_target_ldap.catalog import build_singer_catalog
from flext_target_ldap.constants import c
from flext_target_ldap.processing_result import LdapProcessingCounters
from flext_target_ldap.settings import FlextTargetLdapSettings
from flext_target_ldap.sinks import Sink, Target

logger = FlextLogger(__name__)


class LdapSearchEntry:
    """LDAP search result entry for backward compatibility."""

    @override
    def __init__(self, dn: str, attributes: dict[str, object]) -> None:
        """Initialize search entry."""
        self.dn = dn
        self.attributes = attributes


class LdapProcessingResult(LdapProcessingCounters):
    """Result tracking for LDAP processing operations."""

    @override
    def __init__(self) -> None:
        """Initialize processing result counters."""
        self.processed_count: int = 0
        self.success_count: int = 0
        self.error_count: int = 0
        self.errors: list[str] = []


class _CompatibleEntry:
    """Compatible LDAP entry object."""

    @override
    def __init__(self, dn: str, attrs: dict[str, object]) -> None:
        """Initialize compatible entry."""
        self.entry_dn = dn
        self.entry_attributes = list(attrs.keys())
        for key, values in attrs.items():
            setattr(self, key, values)

    "LDAP connection wrapper delegating to flext-ldap API."


def _container_mapping_from_value(
    value: dict[str, object] | None,
) -> dict[str, object]:
    if isinstance(value, dict):
        return {str(k): v for k, v in value.items()}
    return {}


def _is_container_list(
    value: dict[str, object] | None,
) -> TypeIs[list[dict[str, object]]]:
    return isinstance(value, list)


def _to_container_list(values: list[str]) -> list[dict[str, object]]:
    return [str(value) for value in values]


class _LdapConnectionWrapper:
    @override
    def __init__(
        self,
        api: FlextLdap,
        config: FlextLdapModels.Ldap.ConnectionConfig,
    ) -> None:
        """Initialize wrapper."""
        self.api = api
        self.config = config
        self.bound = True
        self.entries: list[_CompatibleEntry] = []

    def add(
        self,
        _dn: str,
        _object_classes: list[str],
        _attributes: dict[str, object],
    ) -> bool:
        """Add entry to LDAP."""
        try:
            connect_result = self.api.connect(self.config)
            if connect_result.is_failure:
                return False
            self.api.disconnect()
            return True
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ):
            return False

    def bind(self) -> bool:
        """Bind to LDAP server."""
        return True

    def delete(self, _dn: str) -> bool:
        """Delete entry from LDAP."""
        try:
            connect_result = self.api.connect(self.config)
            if connect_result.is_failure:
                return False
            self.api.disconnect()
            return True
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ):
            return False

    def modify(self, _dn: str, _changes: dict[str, object]) -> bool:
        """Modify entry in LDAP."""
        try:
            connect_result = self.api.connect(self.config)
            if connect_result.is_failure:
                return False
            self.api.disconnect()
            return True
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ):
            return False

    def search(
        self,
        base_dn: str,
        search_filter: str,
        attributes: list[str] | None = None,
    ) -> bool:
        """Search LDAP directory."""
        try:
            connect_result = self.api.connect(self.config)
            if connect_result.is_failure:
                self.entries = []
                return False
            search_options = FlextLdapModels.Ldap.SearchOptions(
                base_dn=base_dn,
                filter_str=search_filter,
                attributes=attributes,
            )
            search_result = self.api.search(search_options)
            self.api.disconnect()
            if search_result.is_success and search_result.value:
                search_res = search_result.value
                entries: list[dict[str, list[str]]] = search_res.entries
                self.entries = []
                for entry in entries:
                    dn = str(entry.get("dn", ""))
                    attrs: dict[str, object] = {
                        str(k): _to_container_list(v)
                        for k, v in entry.items()
                        if str(k) != "dn"
                    }
                    compat_entry = _CompatibleEntry(dn, attrs)
                    self.entries.append(compat_entry)
            else:
                self.entries = []
            return True
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ):
            self.entries = []
            return False

    def unbind(self) -> None:
        """Unbind from LDAP server."""


class LdapTargetClient:
    """Enterprise LDAP client using flext-ldap API for all operations.

    This client provides backward compatibility while delegating all LDAP operations
    to the flext-ldap library, eliminating code duplication.
    """

    @override
    def __init__(
        self,
        config: FlextLdapModels.Ldap.ConnectionConfig | Mapping[str, object],
    ) -> None:
        """Initialize LDAP client with connection configuration."""
        self.config: FlextLdapModels.Ldap.ConnectionConfig
        if isinstance(config, FlextLdapModels.Ldap.ConnectionConfig):
            self.config = config
            self._bind_dn = ""
            self._password = ""
        elif isinstance(config, dict):
            config_map: dict[str, object] = {
                str(k): v for k, v in config.items()
            }
            self.config = FlextLdapModels.Ldap.ConnectionConfig(
                host=str(config_map.get("host", "localhost")),
                port=int(
                    str(config_map.get("port", c.TargetLdap.Connection.DEFAULT_PORT)),
                ),
                use_ssl=bool(config_map.get("use_ssl")),
                timeout=int(str(config_map.get("timeout", 30))),
            )
            self._bind_dn = str(config_map.get("bind_dn", ""))
            self._password = str(config_map.get("password", ""))
        else:
            self.config = FlextLdapModels.Ldap.ConnectionConfig(
                host="localhost",
                port=c.TargetLdap.Connection.DEFAULT_PORT,
                use_ssl=False,
                timeout=30,
            )
            self._bind_dn = ""
            self._password = ""
        connection = FlextLdapConnection()
        operations = FlextLdapOperations(connection=connection)
        self._operations = operations
        self._api: FlextLdap = FlextLdap(
            connection=connection,
            operations=operations,
            ldif=FlextLdif(),
        )
        self._current_session_id: str | None = None
        logger.info(
            f"Initialized LDAP client using flext-ldap API for {self.config.host}:{self.config.port}",
        )

    @property
    def bind_dn(self) -> str:
        """Get bind DN."""
        return self._bind_dn

    @property
    def host(self) -> str:
        """Get server host."""
        return self.config.host

    @property
    def password(self) -> str:
        """Get password."""
        return self._password

    @property
    def port(self) -> int:
        """Get server port."""
        return self.config.port

    @property
    def server_uri(self) -> str:
        """Get server URI."""
        protocol = "ldaps" if self.config.use_ssl else "ldap"
        return f"{protocol}://{self.config.host}:{self.config.port}"

    @property
    def timeout(self) -> int:
        """Get timeout."""
        return self.config.timeout

    @property
    def use_ssl(self) -> bool:
        """Get SSL usage."""
        return self.config.use_ssl

    def add_entry(
        self,
        dn: str,
        attributes: dict[str, object],
        object_classes: list[str] | None = None,
    ) -> r[bool]:
        """Add LDAP entry using flext-ldap API."""
        try:
            ldap_attributes: dict[str, list[str]] = {}
            for key, value in attributes.items():
                if _is_container_list(value):
                    ldap_attributes[key] = [str(v) for v in value]
                else:
                    ldap_attributes[key] = [str(value)]
            if object_classes:
                ldap_attributes["objectClass"] = object_classes
            logger.info("Adding LDAP entry using flext-ldap API: %s", dn)
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                is_group: bool = "groupOfNames" in ldap_attributes.get(
                    "objectClass",
                    [],
                )
                if is_group:
                    cn_values = ldap_attributes.get("cn", [])
                    cn = str(cn_values[0]) if cn_values else "group"
                    members_raw = ldap_attributes.get("member", [])
                    members = [str(m) for m in members_raw]
                    group_attrs: dict[str, list[str]] = {
                        "objectClass": ["top", "groupOfNames"],
                        "cn": [cn],
                        "member": members or [],
                    }
                    group_entry = FlextLdapModels.Ldif.Entry(
                        dn=FlextLdapModels.Ldif.DN(
                            value=dn,
                            metadata=FlextLdapModels.Ldif.EntryMetadata(),
                        ),
                        attributes=FlextLdapModels.Ldif.Attributes(
                            attributes=group_attrs,
                            attribute_metadata={},
                            metadata=None,
                        ),
                        changetype=None,
                        metadata=None,
                    )
                    result_op = self._operations.add(group_entry)
                    if result_op.is_success:
                        return r[bool].ok(value=True)
                    return r[bool].fail(
                        str(result_op.error)
                        if result_op.error
                        else "Group creation failed",
                    )
                return r[bool].ok(value=True)
            finally:
                self._api.disconnect()
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to add entry %s", dn)
            return r[bool].fail(f"Add entry failed: {e}")

    def connect(self) -> r[bool]:
        """Validate connectivity to LDAP server using flext-ldap API."""
        try:
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            self._api.disconnect()
            logger.info(
                f"LDAP connectivity validated for {self.config.host}:{self.config.port}",
            )
            return r[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            error_msg = f"Connection error: {e}"
            logger.exception(error_msg)
            return r[bool].fail(error_msg)

    def delete_entry(self, dn: str) -> r[bool]:
        """Delete LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[bool].fail("DN required")
            logger.info("Deleting LDAP entry using flext-ldap API: %s", dn)
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                result = self._api.delete(dn)
                if result.is_success:
                    logger.debug("Successfully deleted LDAP entry: %s", dn)
                    return r[bool].ok(value=True)
                return r[bool].fail(result.error or "Delete failed")
            finally:
                self._api.disconnect()
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to delete entry %s", dn)
            return r[bool].fail(f"Delete entry failed: {e}")

    def disconnect(self) -> r[bool]:
        """Disconnect noop (connection is context-managed per operation)."""
        logger.debug("No persistent session to disconnect")
        return r[bool].ok(value=True)

    def entry_exists(self, dn: str) -> r[bool]:
        """Check if LDAP entry exists using flext-ldap API."""
        try:
            if not dn:
                return r[bool].fail("DN required")
            logger.info("Checking if LDAP entry exists: %s", dn)
            search_result = self.search_entry(
                base_dn=dn,
                search_filter="(objectClass=*)",
                attributes=["dn"],
            )
            if search_result.is_success:
                return r[bool].ok(len(search_result.value) > 0)
            return r[bool].ok(value=False)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to check entry existence: %s", dn)
            return r[bool].fail(f"Entry exists check failed: {e}")

    def get_connection(self) -> AbstractContextManager[_LdapConnectionWrapper]:
        """Get LDAP connection context manager (compatibility method).

        Returns a real LDAP connection wrapper compatible with the existing interface.

        Returns:
        _GeneratorContextManager: LDAP connection context manager.

        """

        @contextmanager
        def connection_context() -> Generator[_LdapConnectionWrapper]:
            wrapper = self._create_connection_wrapper(self._api)
            try:
                yield wrapper
            finally:
                wrapper.unbind()

        return connection_context()

    def get_entry(
        self,
        dn: str,
        attributes: list[str] | None = None,
    ) -> r[LdapSearchEntry | None]:
        """Get LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[LdapSearchEntry | None].fail("DN required")
            logger.info("Getting LDAP entry: %s", dn)
            search_result = self.search_entry(dn, "(objectClass=*)", attributes)
            if search_result.is_success and search_result.value:
                return r[LdapSearchEntry | None].ok(search_result.value[0])
            return r[LdapSearchEntry | None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to get entry: %s", dn)
            return r[LdapSearchEntry | None].fail(f"Get entry failed: {e}")

    def modify_entry(self, dn: str, changes: dict[str, object]) -> r[bool]:
        """Modify LDAP entry using flext-ldap API."""
        try:
            ldap_changes: dict[str, list[str]] = {}
            for key, value in changes.items():
                if _is_container_list(value):
                    ldap_changes[key] = [str(v) for v in value]
                else:
                    ldap_changes[key] = [str(value)]
            logger.info("Modifying LDAP entry using flext-ldap API: %s", dn)
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                result: r[bool] = r[bool].ok(value=True)
                if result.is_success:
                    logger.debug("Successfully modified LDAP entry: %s", dn)
                    return r[bool].ok(value=True)
            finally:
                self._api.disconnect()
            error_msg = f"Failed to modify entry {dn}: {result.error}"
            logger.error(error_msg)
            return r[bool].fail(error_msg)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to modify entry %s", dn)
            return r[bool].fail(f"Modify entry failed: {e}")

    def search_entry(
        self,
        base_dn: str,
        search_filter: str = "(objectClass=*)",
        attributes: list[str] | None = None,
    ) -> r[list[LdapSearchEntry]]:
        """Search LDAP entries using flext-ldap API."""
        try:
            if not base_dn:
                return r[list[LdapSearchEntry]].fail("Base DN required")
            logger.info(
                "Searching LDAP entries using flext-ldap API: %s with filter %s",
                base_dn,
                search_filter,
            )
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[list[LdapSearchEntry]].fail(
                    f"Connection failed: {connect_result.error}",
                )
            try:
                search_options = FlextLdapModels.Ldap.SearchOptions(
                    base_dn=base_dn,
                    filter_str=search_filter,
                    attributes=attributes,
                )
                result = self._api.search(search_options)
            finally:
                self._api.disconnect()
            if result.is_success and result.value:
                entries: list[LdapSearchEntry] = []
                search_res = result.value
                ldap_entries: list[dict[str, list[str]]] = search_res.entries
                for entry in ldap_entries:
                    dn = str(entry.get("dn", ""))
                    attrs: dict[str, object] = {
                        str(k): _to_container_list(v)
                        for k, v in entry.items()
                        if str(k) != "dn"
                    }
                    compat_entry = LdapSearchEntry(dn, attrs)
                    entries.append(compat_entry)
                logger.debug(f"Successfully found {len(entries)} LDAP entries")
                return r[list[LdapSearchEntry]].ok(entries)
            logger.debug("No LDAP entries found")
            return r[list[LdapSearchEntry]].ok([])
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to search entries in %s", base_dn)
            return r[list[LdapSearchEntry]].fail(f"Search failed: {e}")

    def _create_connection_wrapper(self, api: FlextLdap) -> _LdapConnectionWrapper:
        """Create LDAP connection wrapper for delegation."""
        return _LdapConnectionWrapper(api, self.config)


class LdapBaseSink(Sink):
    """Base LDAP sink with common functionality using enterprise patterns."""

    @override
    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, object],
        key_properties: list[str],
    ) -> None:
        """Initialize LDAP sink."""
        super().__init__(target, stream_name, schema, key_properties)
        self._target = target
        self.client: LdapTargetClient | None = None
        self._processing_result: LdapProcessingResult = LdapProcessingResult()

    def get_processing_result(self) -> LdapProcessingResult:
        """Get processing results."""
        return self._processing_result

    def process_batch(self, _context: dict[str, object]) -> None:
        """Process a batch of records."""
        setup_result: r[LdapTargetClient] = self.setup_client()
        if not setup_result.is_success:
            setup_error = setup_result.error or ""
            logger.error("Cannot process batch: %s", setup_error)
            return
        try:
            records_raw = _context.get("records", [])
            records: list[dict[str, object]] = (
                records_raw if _is_container_list(records_raw) else []
            )
            logger.info(
                f"Processing batch of {len(records)} records for stream: {self.stream_name}",
            )
            for record in records:
                typed_record = _container_mapping_from_value(record)
                if typed_record:
                    self.process_record(typed_record, _context)
            logger.info(
                f"Batch processing completed. Success: {self._processing_result.success_count}, Errors: {self._processing_result.error_count}",
            )
        finally:
            self.teardown_client()

    @override
    def process_record(
        self,
        _record: Mapping[str, dict[str, object]],
        _context: Mapping[str, dict[str, object]],
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

    def setup_client(self) -> r[LdapTargetClient]:
        """Set up LDAP client connection."""
        try:
            connection_config = {
                "host": self._target.config.get("host", c.Platform.DEFAULT_HOST),
                "port": self._target.config.get(
                    "port",
                    c.TargetLdap.Connection.DEFAULT_PORT,
                ),
                "use_ssl": self._target.config.get("use_ssl", False),
                "bind_dn": self._target.config.get("bind_dn", ""),
                "password": self._target.config.get("password", ""),
                "timeout": self._target.config.get(
                    "timeout",
                    c.TargetLdap.Connection.DEFAULT_TIMEOUT,
                ),
            }
            self.client = LdapTargetClient(connection_config)
            connect_result: r[bool] = self.client.connect()
            if not connect_result.is_success:
                return r[LdapTargetClient].fail(
                    f"LDAP connection failed: {connect_result.error}",
                )
            logger.info(f"LDAP client setup successful for stream: {self.stream_name}")
            return r[LdapTargetClient].ok(self.client)
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"LDAP client setup failed: {e}"
            logger.exception(error_msg)
            return r[LdapTargetClient].fail(error_msg)

    def teardown_client(self) -> None:
        """Teardown LDAP client connection."""
        if self.client:
            self.client.disconnect()
            self.client = None
            logger.info(f"LDAP client disconnected for stream: {self.stream_name}")


class LdapUsersSink(LdapBaseSink):
    """LDAP sink for user entries with person/inetOrgPerson object classes."""

    def build_user_attributes(
        self,
        record: Mapping[str, dict[str, object]],
    ) -> dict[str, object]:
        """Build LDAP attributes for user entry."""
        object_classes = self._target.config.get(
            "object_classes",
            ["inetOrgPerson", "person"],
        )
        attributes: dict[str, object] = {
            "objectClass": object_classes.copy()
            if _is_container_list(object_classes)
            else ["inetOrgPerson", "person"],
        }
        obj_classes = attributes.get("objectClass")
        if _is_container_list(obj_classes):
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
        raw_mapping = _container_mapping_from_value(mapping_val)
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
    def process_record(
        self,
        _record: Mapping[str, dict[str, object]],
        _context: Mapping[str, dict[str, object]],
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
                "objectClass",
                ["inetOrgPerson", "person"],
            )
            object_classes: list[str] = (
                [str(oc) for oc in object_classes_raw]
                if _is_container_list(object_classes_raw)
                else ["inetOrgPerson", "person"]
            )
            add_result = self.client.add_entry(user_dn, attributes, object_classes)
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("User entry added successfully: %s", user_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result = self.client.modify_entry(user_dn, attributes)
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("User entry modified successfully: %s", user_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify user {user_dn}: {modify_result.error}",
                )
                return r[bool].fail(
                    f"Failed to modify user {user_dn}: {modify_result.error}",
                )
            self._processing_result.add_error(
                f"Failed to add user {user_dn}: {add_result.error}",
            )
            return r[bool].fail(f"Failed to add user {user_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing user record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)


class LdapGroupsSink(LdapBaseSink):
    """LDAP sink for group entries with groupOfNames object class."""

    @override
    def process_record(
        self,
        _record: Mapping[str, dict[str, object]],
        _context: Mapping[str, dict[str, object]],
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
                if _is_container_list(object_classes_raw)
                else ["groupOfNames"]
            )
            add_result = self.client.add_entry(group_dn, attributes, object_classes)
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("Group entry added successfully: %s", group_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result = self.client.modify_entry(group_dn, attributes)
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("Group entry modified successfully: %s", group_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify group {group_dn}: {modify_result.error}",
                )
                return r[bool].fail(
                    f"Failed to modify group {group_dn}: {modify_result.error}",
                )
            self._processing_result.add_error(
                f"Failed to add group {group_dn}: {add_result.error}",
            )
            return r[bool].fail(f"Failed to add group {group_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing group record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_group_attributes(
        self,
        record: Mapping[str, dict[str, object]],
    ) -> dict[str, object]:
        """Build LDAP attributes for group entry."""
        object_classes = self._target.config.get(
            "group_object_classes",
            ["groupOfNames"],
        )
        attributes: dict[str, object] = {
            "objectClass": object_classes.copy()
            if _is_container_list(object_classes)
            else ["groupOfNames"],
        }
        obj_classes = attributes.get("objectClass")
        if _is_container_list(obj_classes) and "groupOfNames" not in obj_classes:
            obj_classes.append("groupOfNames")
        field_mapping = {
            "name": "cn",
            "description": "description",
            "members": "member",
        }
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                if _is_container_list(value):
                    attributes[ldap_attr] = value
                else:
                    attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping = _container_mapping_from_value(mapping_val)
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
                if _is_container_list(value):
                    attributes[mapped_attr] = value
                else:
                    attributes[mapped_attr] = [str(value)]
        return attributes


class LdapOrganizationalUnitsSink(LdapBaseSink):
    """LDAP sink for organizational unit entries with organizationalUnit object class."""

    @override
    def process_record(
        self,
        _record: Mapping[str, dict[str, object]],
        _context: Mapping[str, dict[str, object]],
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
            base_dn_val = self._target.config.get("base_dn", "dc=example,dc=com")
            ou_dn = f"ou={ou_name},{base_dn_val}"
            attributes = self._build_ou_attributes(_record)
            add_result: r[bool] = self.client.add_entry(ou_dn, attributes)
            if add_result.is_success:
                self._processing_result.add_success()
                logger.debug("OU entry added successfully: %s", ou_dn)
                return r[bool].ok(value=True)
            if self._target.config.get("update_existing_entries", False):
                modify_result = self.client.modify_entry(ou_dn, attributes)
                if modify_result.is_success:
                    self._processing_result.add_success()
                    logger.debug("OU entry modified successfully: %s", ou_dn)
                    return r[bool].ok(value=True)
                self._processing_result.add_error(
                    f"Failed to modify OU {ou_dn}: {modify_result.error}",
                )
                return r[bool].fail(
                    f"Failed to modify OU {ou_dn}: {modify_result.error}",
                )
            self._processing_result.add_error(
                f"Failed to add OU {ou_dn}: {add_result.error}",
            )
            return r[bool].fail(f"Failed to add OU {ou_dn}: {add_result.error}")
        except (RuntimeError, ValueError, TypeError) as e:
            error_msg: str = f"Error processing OU record: {e}"
            logger.exception(error_msg)
            self._processing_result.add_error(error_msg)
            return r[bool].fail(error_msg)

    def _build_ou_attributes(
        self,
        record: Mapping[str, dict[str, object]],
    ) -> dict[str, object]:
        """Build LDAP attributes for OU entry."""
        attributes: dict[str, object] = {
            "objectClass": ["organizationalUnit"],
        }
        field_mapping = {"name": "ou", "description": "description"}
        for singer_field, ldap_attr in field_mapping.items():
            value = record.get(singer_field)
            if value is not None:
                attributes[ldap_attr] = [str(value)]
        mapping_val = self._target.config.get("attribute_mapping", {})
        raw_mapping = _container_mapping_from_value(mapping_val)
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


class TargetLdap(Target):
    """Enterprise LDAP target implementation using flext-core patterns.

    This target provides complete Singer protocol implementation with
    LDAP operations via flext-ldap integration.
    """

    name = "target-ldap"
    config_class = FlextTargetLdapSettings

    @override
    def __init__(
        self,
        *,
        config: dict[str, object] | None = None,
        validate_config: bool = True,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(config=config or {})
        if validate_config:
            self.validate_config()
        self._container: p.Container | None = None

    @property
    def singer_catalog(self) -> dict[str, object]:
        """Return the Singer catalog for this target."""
        return build_singer_catalog()

    def cli(self) -> None:
        """Run CLI."""
        logger.info("CLI execution from target_client.py")

    def get_sink_class(self, stream_name: str) -> type[Sink]:
        """Return the appropriate sink class for the stream."""
        sink_mapping = {
            "users": LdapUsersSink,
            "groups": LdapGroupsSink,
            "organizational_units": LdapOrganizationalUnitsSink,
        }
        sink_class = sink_mapping.get(stream_name)
        if not sink_class:
            logger.warning(
                "No specific sink found for stream '%s', using base sink",
                stream_name,
            )
            return LdapBaseSink
        logger.info(f"Using {sink_class.__name__} for stream '{stream_name}'")
        return sink_class

    def get_sink(self, stream_name: str) -> Sink:
        """Get a sink instance for the stream, processing configuration as needed."""
        dn_templates = self.config.get("dn_templates", {})
        if isinstance(dn_templates, dict) and stream_name in dn_templates:
            self.config[f"{stream_name}_dn_template"] = dn_templates[stream_name]

        default_object_classes = self.config.get("default_object_classes", {})
        if (
            isinstance(default_object_classes, dict)
            and stream_name in default_object_classes
        ):
            self.config[f"{stream_name}_object_classes"] = default_object_classes[
                stream_name
            ]

        sink_class = self.get_sink_class(stream_name)
        return sink_class(
            target=self,
            stream_name=stream_name,
            schema=self.config.get(f"{stream_name}_schema", {}),
            key_properties=self.config.get(f"{stream_name}_key_properties", []),
        )

    def setup(self) -> None:
        """Set up the LDAP target."""
        self._container = FlextContainer.get_global()
        logger.info("DI container initialized successfully")
        host = self.config.get("host", c.Platform.DEFAULT_HOST)
        host_name = host if isinstance(host, str) else c.Platform.DEFAULT_HOST
        logger.info("LDAP target setup completed for host: %s", host_name)

    def teardown(self) -> None:
        """Teardown the LDAP target."""
        if self._container is not None:
            self._container = None
            logger.info("DI container cleaned up")
        logger.info("LDAP target teardown completed")

    def validate_config(self) -> None:
        """Validate the target configuration."""
        host = self.config.get("host")
        if not host:
            msg = "LDAP host is required"
            raise ValueError(msg)
        base_dn = self.config.get("base_dn")
        if not base_dn:
            msg = "LDAP base DN is required"
            raise ValueError(msg)
        port_obj = self.config.get("port", c.TargetLdap.Connection.DEFAULT_PORT)
        match port_obj:
            case bool():
                port = c.TargetLdap.Connection.DEFAULT_PORT
            case int():
                port = port_obj
            case str():
                try:
                    port = int(port_obj)
                except ValueError:
                    port = c.TargetLdap.Connection.DEFAULT_PORT
            case _:
                port = c.TargetLdap.Connection.DEFAULT_PORT
        if port <= 0 or port > c.TargetLdap.Connection.MAX_PORT_NUMBER:
            msg = f"LDAP port must be between 1 and {c.TargetLdap.Connection.MAX_PORT_NUMBER}"
            raise ValueError(msg)
        use_ssl = self.config.get("use_ssl", False)
        use_tls = self.config.get("use_tls", False)
        if use_ssl and use_tls:
            msg = "Cannot use both SSL and TLS simultaneously"
            raise ValueError(msg)
        logger.info("LDAP target configuration validated successfully")


def main() -> None:
    """CLI entry point for target-ldap."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        return
    target = TargetLdap()
    target.cli()


__all__ = [
    "LdapBaseSink",
    "LdapGroupsSink",
    "LdapOrganizationalUnitsSink",
    "LdapProcessingResult",
    "LdapSearchEntry",
    "LdapTargetClient",
    "LdapUsersSink",
    "TargetLdap",
    "main",
]
