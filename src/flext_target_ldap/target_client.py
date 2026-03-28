"""LDAP Target Client - PEP8 Consolidation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import (
    Generator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from contextlib import AbstractContextManager, contextmanager
from typing import TypeIs, override

from flext_core import FlextLogger
from flext_ldap import (
    ldap,
    m,
)

from flext_target_ldap import (
    c,
    r,
    t,
)

logger = FlextLogger(__name__)


class FlextTargetLdapSearchEntry:
    """LDAP search result entry for backward compatibility."""

    @override
    def __init__(
        self,
        dn: str,
        attributes: Mapping[str, t.ContainerValue],
    ) -> None:
        """Initialize search entry."""
        self.dn = dn
        self.attributes = attributes


class _CompatibleEntry:
    """Compatible LDAP entry t.NormalizedValue."""

    @override
    def __init__(self, dn: str, attrs: Mapping[str, t.ContainerValue]) -> None:
        """Initialize compatible entry."""
        self.entry_dn = dn
        self.entry_attributes = list(attrs.keys())
        for key, values in attrs.items():
            setattr(self, key, values)

    "LDAP connection wrapper delegating to flext-ldap API."


def _container_mapping_from_value(
    value: t.ContainerValue | None,
) -> Mapping[str, t.ContainerValue]:
    if isinstance(value, dict):
        return {str(k): v for k, v in value.items()}
    msg = f"Expected dict for attribute mapping, got {type(value).__name__}: {value!r}"
    raise TypeError(msg)


def _is_container_list(
    value: t.ContainerValue | None,
) -> TypeIs[Sequence[t.ContainerValue]]:
    return isinstance(value, list)


def _to_container_list(values: t.ContainerValue | t.StrSequence) -> t.ContainerValue:
    if isinstance(values, list):
        return [str(value) for value in values]
    return values


def _to_str_values(value: t.ContainerValue) -> t.StrSequence:
    if _is_container_list(value):
        return [str(item) for item in value]
    return [str(value)]


def _build_ldif_entry(
    dn: str,
    attributes: Mapping[str, t.ContainerValue],
    object_classes: t.StrSequence | None = None,
) -> m.Ldif.Entry:
    entry_attributes: MutableMapping[str, t.StrSequence] = {
        key: _to_str_values(value) for key, value in attributes.items()
    }
    if object_classes:
        entry_attributes["objectClass"] = [str(value) for value in object_classes]
    return m.Ldif.Entry(
        dn=m.Ldif.DN(
            value=dn,
            metadata=m.Ldif.EntryMetadata(),
        ),
        attributes=m.Ldif.Attributes.model_validate({
            "attributes": entry_attributes,
            "attribute_metadata": {},
            "metadata": None,
        }),
        changetype=None,
        metadata=None,
        validation_metadata=None,
    )


def _build_modify_changes(
    changes: Mapping[str, t.ContainerValue],
) -> t.Ldap.OperationChanges:
    return {
        key: [(c.Ldap.ModifyOperation.REPLACE, _to_str_values(value))]
        for key, value in changes.items()
    }


class _LdapConnectionWrapper:
    @override
    def __init__(
        self,
        api: ldap,
        config: m.Ldap.ConnectionConfig,
    ) -> None:
        """Initialize wrapper."""
        self.api = api
        self.config = config
        self.bound = True
        self.entries: MutableSequence[_CompatibleEntry] = []

    def add(
        self,
        dn: str,
        object_classes: t.StrSequence,
        attributes: Mapping[str, t.ContainerValue],
    ) -> bool:
        """Add entry to LDAP."""
        entry = _build_ldif_entry(dn, attributes, object_classes)
        result = self.api.add(entry)
        return result.is_success

    def bind(self) -> bool:
        """Bind to LDAP server."""
        result = self.api.connect(self.config)
        self.bound = result.is_success
        return self.bound

    def delete(self, dn: str) -> bool:
        """Delete entry from LDAP."""
        result = self.api.delete(dn)
        return result.is_success

    def modify(self, dn: str, changes: Mapping[str, t.ContainerValue]) -> bool:
        """Modify entry in LDAP."""
        result = self.api.modify(dn, _build_modify_changes(changes))
        return result.is_success

    def search(
        self,
        base_dn: str,
        search_filter: str,
        attributes: t.StrSequence | None = None,
    ) -> bool:
        """Search LDAP directory."""
        try:
            connect_result = self.api.connect(self.config)
            if connect_result.is_failure:
                self.entries = list[_CompatibleEntry]()
                return False
            search_options = m.Ldap.SearchOptions(
                base_dn=base_dn,
                filter_str=search_filter,
                attributes=attributes,
            )
            search_result = self.api.search(search_options)
            self.api.disconnect()
            if search_result.is_success and search_result.value:
                search_res = search_result.value
                entries: Sequence[Mapping[str, t.StrSequence]] = search_res.entries
                self.entries = list[_CompatibleEntry]()
                for entry in entries:
                    dn = str(entry.get("dn", ""))
                    attrs: MutableMapping[str, t.ContainerValue] = {
                        str(k): _to_container_list(v)
                        for k, v in entry.items()
                        if str(k) != "dn"
                    }
                    compat_entry = _CompatibleEntry(dn, attrs)
                    self.entries.append(compat_entry)
            else:
                self.entries = list[_CompatibleEntry]()
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
            self.entries = list[_CompatibleEntry]()
            return False

    def unbind(self) -> None:
        """Unbind from LDAP server."""
        self.api.disconnect()
        self.bound = False
        self.entries.clear()


class FlextTargetLdapClient:
    """Enterprise LDAP client using flext-ldap API for all operations.

    This client provides backward compatibility while delegating all LDAP operations
    to the flext-ldap library, eliminating code duplication.
    """

    @override
    def __init__(
        self,
        config: m.Ldap.ConnectionConfig | t.ContainerValueMapping,
    ) -> None:
        """Initialize LDAP client with connection configuration."""
        self.config: m.Ldap.ConnectionConfig
        if isinstance(config, m.Ldap.ConnectionConfig):
            self.config = config
            self._bind_dn = config.bind_dn or ""
            self._password = config.bind_password or ""
        elif isinstance(config, dict):
            config_map: Mapping[str, t.ContainerValue] = {
                str(k): v for k, v in config.items()
            }
            self.config = m.Ldap.ConnectionConfig(
                host=str(config_map.get("host", "localhost")),
                port=int(
                    str(config_map.get("port", c.Ldap.ConnectionDefaults.PORT)),
                ),
                use_ssl=bool(config_map.get("use_ssl")),
                timeout=int(str(config_map.get("timeout", 30))),
            )
            self._bind_dn = str(config_map.get("bind_dn", ""))
            self._password = str(config_map.get("password", ""))
        else:
            self.config = m.Ldap.ConnectionConfig(
                host="localhost",
                port=c.Ldap.ConnectionDefaults.PORT,
                use_ssl=False,
                timeout=30,
            )
            self._bind_dn = ""
            self._password = ""
        self._api: ldap = ldap()
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
        attributes: Mapping[str, t.ContainerValue],
        object_classes: t.StrSequence | None = None,
    ) -> r[bool]:
        """Add LDAP entry using flext-ldap API."""
        try:
            logger.info("Adding LDAP entry using flext-ldap API: %s", dn)
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                ldap_entry = _build_ldif_entry(dn, attributes, object_classes)
                result_op = self._api.add(ldap_entry)
                if result_op.is_success:
                    return r[bool].ok(value=True)
                return r[bool].fail(
                    str(result_op.error) if result_op.error else "LDAP add failed",
                )
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
        """Disconnect LDAP session through flext-ldap."""
        try:
            self._api.disconnect()
            self._current_session_id = None
            return r[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to disconnect LDAP client")
            return r[bool].fail(f"Disconnect failed: {e}")

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
                return r[bool].ok(bool(search_result.value))
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
        attributes: t.StrSequence | None = None,
    ) -> r[FlextTargetLdapSearchEntry | None]:
        """Get LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[FlextTargetLdapSearchEntry | None].fail("DN required")
            logger.info("Getting LDAP entry: %s", dn)
            search_result = self.search_entry(dn, "(objectClass=*)", attributes)
            if search_result.is_success and search_result.value:
                return r[FlextTargetLdapSearchEntry | None].ok(search_result.value[0])
            return r[FlextTargetLdapSearchEntry | None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to get entry: %s", dn)
            return r[FlextTargetLdapSearchEntry | None].fail(f"Get entry failed: {e}")

    def modify_entry(
        self,
        dn: str,
        changes: Mapping[str, t.ContainerValue],
    ) -> r[bool]:
        """Modify LDAP entry using flext-ldap API."""
        try:
            logger.info("Modifying LDAP entry using flext-ldap API: %s", dn)
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                result = self._api.modify(dn, _build_modify_changes(changes))
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
        attributes: t.StrSequence | None = None,
    ) -> r[Sequence[FlextTargetLdapSearchEntry]]:
        """Search LDAP entries using flext-ldap API."""
        try:
            if not base_dn:
                return r[Sequence[FlextTargetLdapSearchEntry]].fail("Base DN required")
            logger.info(
                "Searching LDAP entries using flext-ldap API: %s with filter %s",
                base_dn,
                search_filter,
            )
            connect_result = self._api.connect(self.config)
            if connect_result.is_failure:
                return r[Sequence[FlextTargetLdapSearchEntry]].fail(
                    f"Connection failed: {connect_result.error}",
                )
            try:
                search_options = m.Ldap.SearchOptions(
                    base_dn=base_dn,
                    filter_str=search_filter,
                    attributes=attributes,
                )
                result = self._api.search(search_options)
            finally:
                self._api.disconnect()
            if result.is_success and result.value:
                entries: MutableSequence[FlextTargetLdapSearchEntry] = []
                search_res = result.value
                ldap_entries: Sequence[Mapping[str, t.StrSequence]] = search_res.entries
                for entry in ldap_entries:
                    dn = str(entry.get("dn", ""))
                    attrs: MutableMapping[str, t.ContainerValue] = {
                        str(k): _to_container_list(v)
                        for k, v in entry.items()
                        if str(k) != "dn"
                    }
                    compat_entry = FlextTargetLdapSearchEntry(dn, attrs)
                    entries.append(compat_entry)
                logger.debug(f"Successfully found {len(entries)} LDAP entries")
                return r[Sequence[FlextTargetLdapSearchEntry]].ok(entries)
            logger.debug("No LDAP entries found")
            return r[Sequence[FlextTargetLdapSearchEntry]].ok([])
        except (RuntimeError, ValueError, TypeError) as e:
            logger.exception("Failed to search entries in %s", base_dn)
            return r[Sequence[FlextTargetLdapSearchEntry]].fail(f"Search failed: {e}")

    def _create_connection_wrapper(self, api: ldap) -> _LdapConnectionWrapper:
        """Create LDAP connection wrapper for delegation."""
        return _LdapConnectionWrapper(api, self.config)


__all__ = ["FlextTargetLdapClient", "FlextTargetLdapSearchEntry"]
