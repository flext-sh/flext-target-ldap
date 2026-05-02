"""LDAP Target Client - PEP8 Consolidation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import ClassVar, override

from flext_ldap import ldap, u
from flext_target_ldap import FlextTargetLdapSettings, c, m, p, r, t


class FlextTargetLdapClient:
    """Enterprise LDAP client using flext-ldap API for all operations.

    This client delegates LDAP operations to flext-ldap without compatibility layers.
    """

    logger: ClassVar = u.fetch_logger(__name__)
    settings: m.Ldap.ConnectionConfig

    @staticmethod
    def to_str_values(
        value: t.JsonValue | t.StrSequence,
    ) -> list[str]:
        if isinstance(value, Sequence) and not isinstance(value, str | bytes):
            return [str(item) for item in value]
        return [str(value)]

    @staticmethod
    def _build_ldif_entry(
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence | None = None,
    ) -> m.Ldif.Entry:
        entry_attributes: dict[str, t.StrSequence] = {
            key: FlextTargetLdapClient.to_str_values(value)
            for key, value in attributes.items()
        }
        if object_classes:
            entry_attributes["objectClass"] = list(object_classes)
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

    @staticmethod
    def _build_modify_changes(
        changes: t.Ldap.OperationAttributes,
    ) -> dict[str, t.SequenceOf[tuple[int, t.StrSequence]]]:
        built_changes: dict[str, t.SequenceOf[tuple[int, t.StrSequence]]] = {
            key: [
                (
                    c.Ldap.ModifyOperation.REPLACE,
                    FlextTargetLdapClient.to_str_values(value),
                )
            ]
            for key, value in changes.items()
        }
        return built_changes

    @override
    def __init__(
        self,
        settings: (
            FlextTargetLdapSettings
            | m.Ldap.ConnectionConfig
            | t.TargetLdap.SettingsPayload
        ),
    ) -> None:
        """Initialize LDAP client with connection configuration."""
        connection_settings = self._resolve_connection_settings(settings)
        self.settings: m.Ldap.ConnectionConfig = connection_settings
        self._bind_dn = connection_settings.bind_dn or ""
        self._password = connection_settings.bind_password or ""
        self._api = ldap
        self._current_session_id: str | None = None
        FlextTargetLdapClient.logger.info(
            f"Initialized LDAP client using flext-ldap API for {self.settings.host}:{self.settings.port}",
        )

    @property
    def bind_dn(self) -> str:
        """Get bind DN."""
        return self._bind_dn

    @property
    def host(self) -> str:
        """Get server host."""
        host: str = self.settings.host
        return host

    @property
    def password(self) -> str:
        """Get password."""
        return self._password

    @staticmethod
    def _resolve_connection_settings(
        settings: (
            FlextTargetLdapSettings
            | m.Ldap.ConnectionConfig
            | t.TargetLdap.SettingsPayload
        ),
    ) -> m.Ldap.ConnectionConfig:
        """Resolve any supported settings payload to the connection model."""
        if isinstance(settings, m.Ldap.ConnectionConfig):
            return settings
        if isinstance(settings, FlextTargetLdapSettings):
            return settings.connection
        if isinstance(settings, Mapping):
            connection_value = settings.get("connection")
            if isinstance(connection_value, m.Ldap.ConnectionConfig):
                return connection_value
            if isinstance(connection_value, Mapping):
                return m.Ldap.ConnectionConfig.model_validate(connection_value)
            return m.Ldap.ConnectionConfig.model_validate(dict(settings))
        msg = f"Unsupported LDAP client settings type: {type(settings).__name__}"
        raise TypeError(msg)

    @property
    def port(self) -> int:
        """Get server port."""
        port: int = self.settings.port
        return port

    @property
    def server_uri(self) -> str:
        """Get server URI."""
        protocol = "ldaps" if self.settings.use_ssl else "ldap"
        return f"{protocol}://{self.settings.host}:{self.settings.port}"

    @property
    def timeout(self) -> int:
        """Get timeout."""
        timeout: int = self.settings.timeout
        return timeout

    @property
    def use_ssl(self) -> bool:
        """Get SSL usage."""
        use_ssl: bool = self.settings.use_ssl
        return use_ssl

    def add_entry(
        self,
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Add LDAP entry using flext-ldap API."""
        try:
            FlextTargetLdapClient.logger.info(
                "Adding LDAP entry using flext-ldap API: %s",
                dn,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail_op("Connection", connect_result.error)
            try:
                ldap_entry = self._build_ldif_entry(dn, attributes, object_classes)
                result_op = self._api.add(ldap_entry)
                if result_op.success:
                    return r[bool].ok(value=True)
                return r[bool].fail(
                    result_op.error or "LDAP add failed",
                )
            finally:
                self._api.disconnect()
        except c.EXC_RUNTIME_TYPE as e:
            FlextTargetLdapClient.logger.exception("Failed to add entry %s", dn)
            return r[bool].fail_op("Add entry", e)

    def connect(self) -> p.Result[bool]:
        """Validate connectivity to LDAP server using flext-ldap API."""
        try:
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail_op("Connection", connect_result.error)
            self._api.disconnect()
            FlextTargetLdapClient.logger.info(
                f"LDAP connectivity validated for {self.settings.host}:{self.settings.port}",
            )
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            error_msg = f"Connection error: {e}"
            FlextTargetLdapClient.logger.exception(error_msg)
            return r[bool].fail(error_msg)

    def delete_entry(self, dn: str) -> p.Result[bool]:
        """Delete LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[bool].fail("DN required")
            FlextTargetLdapClient.logger.info(
                "Deleting LDAP entry using flext-ldap API: %s",
                dn,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail_op("Connection", connect_result.error)
            try:
                result = self._api.delete(dn)
                if result.success:
                    FlextTargetLdapClient.logger.debug(
                        "Successfully deleted LDAP entry: %s",
                        dn,
                    )
                    return r[bool].ok(value=True)
                return r[bool].fail(result.error or "Delete failed")
            finally:
                self._api.disconnect()
        except c.EXC_RUNTIME_TYPE as e:
            FlextTargetLdapClient.logger.exception("Failed to delete entry %s", dn)
            return r[bool].fail_op("Delete entry", e)

    def disconnect(self) -> p.Result[bool]:
        """Disconnect LDAP session through flext-ldap."""
        try:
            self._api.disconnect()
            self._current_session_id = None
            return r[bool].ok(value=True)
        except c.EXC_RUNTIME_TYPE as e:
            FlextTargetLdapClient.logger.exception(
                "Failed to disconnect LDAP client",
            )
            return r[bool].fail_op("Disconnect", e)

    def entry_exists(self, dn: str) -> p.Result[bool]:
        """Check if LDAP entry exists using flext-ldap API."""
        try:
            if not dn:
                return r[bool].fail("DN required")
            FlextTargetLdapClient.logger.info("Checking if LDAP entry exists: %s", dn)
            search_result = self.search_entry(
                base_dn=dn,
                search_filter="(objectClass=*)",
                attributes=["dn"],
            )
            if search_result.success:
                return r[bool].ok(bool(search_result.value))
            return r[bool].ok(value=False)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient.logger.exception(
                "Failed to check entry existence: %s",
                dn,
            )
            return r[bool].fail_op("Entry exists check", e)

    def get_entry(
        self,
        dn: str,
        attributes: t.StrSequence | None = None,
    ) -> p.Result[m.Ldif.Entry | None]:
        """Get LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[m.Ldif.Entry | None].fail("DN required")
            FlextTargetLdapClient.logger.info("Getting LDAP entry: %s", dn)
            search_result = self.search_entry(dn, "(objectClass=*)", attributes)
            if search_result.success and search_result.value:
                return r[m.Ldif.Entry | None].ok(search_result.value[0])
            return r[m.Ldif.Entry | None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient.logger.exception("Failed to get entry: %s", dn)
            return r[m.Ldif.Entry | None].fail_op("Get entry", e)

    def modify_entry(
        self,
        dn: str,
        changes: t.Ldap.OperationAttributes,
    ) -> p.Result[bool]:
        """Modify LDAP entry using flext-ldap API."""
        try:
            FlextTargetLdapClient.logger.info(
                "Modifying LDAP entry using flext-ldap API: %s",
                dn,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail_op("Connection", connect_result.error)
            try:
                result = self._api.modify(dn, self._build_modify_changes(changes))
                if result.success:
                    FlextTargetLdapClient.logger.debug(
                        "Successfully modified LDAP entry: %s",
                        dn,
                    )
                    return r[bool].ok(value=True)
            finally:
                self._api.disconnect()
            error_msg = f"Failed to modify entry {dn}: {result.error}"
            FlextTargetLdapClient.logger.error(error_msg)
            return r[bool].fail(error_msg)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient.logger.exception("Failed to modify entry %s", dn)
            return r[bool].fail_op("Modify entry", e)

    def search_entry(
        self,
        base_dn: str,
        search_filter: str = "(objectClass=*)",
        attributes: t.StrSequence | None = None,
    ) -> p.Result[list[m.Ldif.Entry]]:
        """Search LDAP entries using flext-ldap API."""
        try:
            if not base_dn:
                return r[list[m.Ldif.Entry]].fail("Base DN required")
            FlextTargetLdapClient.logger.info(
                "Searching LDAP entries using flext-ldap API: %s with filter %s",
                base_dn,
                search_filter,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[list[m.Ldif.Entry]].fail_op(
                    "Connection",
                    connect_result.error,
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
            if result.success and result.value:
                search_res = result.value
                entries: list[m.Ldif.Entry] = list(search_res.entries)
                FlextTargetLdapClient.logger.debug(
                    "Successfully found %d LDAP entries",
                    len(entries),
                )
                return r[list[m.Ldif.Entry]].ok(entries)
            FlextTargetLdapClient.logger.debug("No LDAP entries found")
            return r[list[m.Ldif.Entry]].ok([])
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient.logger.exception(
                "Failed to search entries in %s",
                base_dn,
            )
            return r[list[m.Ldif.Entry]].fail_op("Search", e)


__all__: list[str] = ["FlextTargetLdapClient"]
