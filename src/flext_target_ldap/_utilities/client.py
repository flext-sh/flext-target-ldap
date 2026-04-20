"""LDAP Target Client - PEP8 Consolidation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
    MutableSequence,
    Sequence,
)
from typing import ClassVar, override

from flext_ldap import ldap, u

from flext_target_ldap import FlextTargetLdapSettings, c, m, p, r, t


class FlextTargetLdapClient:
    """Enterprise LDAP client using flext-ldap API for all operations.

    This client delegates LDAP operations to flext-ldap without compatibility layers.
    """

    _logger: ClassVar = u.fetch_logger(__name__)

    @staticmethod
    def to_str_values(value: t.Container) -> t.StrSequence:
        if isinstance(value, list):
            return [str(item) for item in value]
        return [str(value)]

    @staticmethod
    def _build_ldif_entry(
        dn: str,
        attributes: t.ContainerValueMapping,
        object_classes: t.StrSequence | None = None,
    ) -> m.Ldif.Entry:
        entry_attributes: MutableMapping[str, t.StrSequence] = {
            key: FlextTargetLdapClient.to_str_values(value)
            for key, value in attributes.items()
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

    @staticmethod
    def _build_modify_changes(
        changes: t.ContainerValueMapping,
    ) -> dict[str, Sequence[tuple[int, t.StrSequence]]]:
        built_changes: dict[str, Sequence[tuple[int, t.StrSequence]]] = {
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
            FlextTargetLdapSettings | m.Ldap.ConnectionConfig | t.ContainerValueMapping
        ),
    ) -> None:
        """Initialize LDAP client with connection configuration."""
        connection_settings: m.Ldap.ConnectionConfig
        if isinstance(settings, m.Ldap.ConnectionConfig):
            connection_settings = settings
        elif isinstance(settings, FlextTargetLdapSettings):
            connection_settings = settings.connection
        elif isinstance(settings, dict):
            connection_settings = FlextTargetLdapSettings.model_validate(
                settings,
            ).connection
        else:
            msg = f"Unsupported LDAP client settings type: {type(settings).__name__}"
            raise TypeError(msg)
        self.settings = connection_settings
        self._bind_dn = connection_settings.bind_dn or ""
        self._password = connection_settings.bind_password or ""
        self._api = ldap
        self._current_session_id: str | None = None
        FlextTargetLdapClient._logger.info(
            f"Initialized LDAP client using flext-ldap API for {self.settings.host}:{self.settings.port}",
        )

    @property
    def bind_dn(self) -> str:
        """Get bind DN."""
        return self._bind_dn

    @property
    def host(self) -> str:
        """Get server host."""
        return self.settings.host

    @property
    def password(self) -> str:
        """Get password."""
        return self._password

    @property
    def port(self) -> int:
        """Get server port."""
        return self.settings.port

    @property
    def server_uri(self) -> str:
        """Get server URI."""
        protocol = "ldaps" if self.settings.use_ssl else "ldap"
        return f"{protocol}://{self.settings.host}:{self.settings.port}"

    @property
    def timeout(self) -> int:
        """Get timeout."""
        return self.settings.timeout

    @property
    def use_ssl(self) -> bool:
        """Get SSL usage."""
        return self.settings.use_ssl

    def add_entry(
        self,
        dn: str,
        attributes: t.ContainerValueMapping,
        object_classes: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Add LDAP entry using flext-ldap API."""
        try:
            FlextTargetLdapClient._logger.info(
                "Adding LDAP entry using flext-ldap API: %s",
                dn,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                ldap_entry = self._build_ldif_entry(dn, attributes, object_classes)
                result_op = self._api.add(ldap_entry)
                if result_op.success:
                    return r[bool].ok(value=True)
                return r[bool].fail(
                    str(result_op.error) if result_op.error else "LDAP add failed",
                )
            finally:
                self._api.disconnect()
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception("Failed to add entry %s", dn)
            return r[bool].fail(f"Add entry failed: {e}")

    def connect(self) -> p.Result[bool]:
        """Validate connectivity to LDAP server using flext-ldap API."""
        try:
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            self._api.disconnect()
            FlextTargetLdapClient._logger.info(
                f"LDAP connectivity validated for {self.settings.host}:{self.settings.port}",
            )
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            error_msg = f"Connection error: {e}"
            FlextTargetLdapClient._logger.exception(error_msg)
            return r[bool].fail(error_msg)

    def delete_entry(self, dn: str) -> p.Result[bool]:
        """Delete LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[bool].fail("DN required")
            FlextTargetLdapClient._logger.info(
                "Deleting LDAP entry using flext-ldap API: %s",
                dn,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                result = self._api.delete(dn)
                if result.success:
                    FlextTargetLdapClient._logger.debug(
                        "Successfully deleted LDAP entry: %s",
                        dn,
                    )
                    return r[bool].ok(value=True)
                return r[bool].fail(result.error or "Delete failed")
            finally:
                self._api.disconnect()
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception("Failed to delete entry %s", dn)
            return r[bool].fail(f"Delete entry failed: {e}")

    def disconnect(self) -> p.Result[bool]:
        """Disconnect LDAP session through flext-ldap."""
        try:
            self._api.disconnect()
            self._current_session_id = None
            return r[bool].ok(value=True)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception(
                "Failed to disconnect LDAP client",
            )
            return r[bool].fail(f"Disconnect failed: {e}")

    def entry_exists(self, dn: str) -> p.Result[bool]:
        """Check if LDAP entry exists using flext-ldap API."""
        try:
            if not dn:
                return r[bool].fail("DN required")
            FlextTargetLdapClient._logger.info("Checking if LDAP entry exists: %s", dn)
            search_result = self.search_entry(
                base_dn=dn,
                search_filter="(objectClass=*)",
                attributes=["dn"],
            )
            if search_result.success:
                return r[bool].ok(bool(search_result.value))
            return r[bool].ok(value=False)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception(
                "Failed to check entry existence: %s",
                dn,
            )
            return r[bool].fail(f"Entry exists check failed: {e}")

    def get_entry(
        self,
        dn: str,
        attributes: t.StrSequence | None = None,
    ) -> p.Result[m.Ldif.Entry | None]:
        """Get LDAP entry using flext-ldap API."""
        try:
            if not dn:
                return r[m.Ldif.Entry | None].fail("DN required")
            FlextTargetLdapClient._logger.info("Getting LDAP entry: %s", dn)
            search_result = self.search_entry(dn, "(objectClass=*)", attributes)
            if search_result.success and search_result.value:
                return r[m.Ldif.Entry | None].ok(search_result.value[0])
            return r[m.Ldif.Entry | None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception("Failed to get entry: %s", dn)
            return r[m.Ldif.Entry | None].fail(f"Get entry failed: {e}")

    def modify_entry(
        self,
        dn: str,
        changes: t.ContainerValueMapping,
    ) -> p.Result[bool]:
        """Modify LDAP entry using flext-ldap API."""
        try:
            FlextTargetLdapClient._logger.info(
                "Modifying LDAP entry using flext-ldap API: %s",
                dn,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[bool].fail(f"Connection failed: {connect_result.error}")
            try:
                result = self._api.modify(dn, self._build_modify_changes(changes))
                if result.success:
                    FlextTargetLdapClient._logger.debug(
                        "Successfully modified LDAP entry: %s",
                        dn,
                    )
                    return r[bool].ok(value=True)
            finally:
                self._api.disconnect()
            error_msg = f"Failed to modify entry {dn}: {result.error}"
            FlextTargetLdapClient._logger.error(error_msg)
            return r[bool].fail(error_msg)
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception("Failed to modify entry %s", dn)
            return r[bool].fail(f"Modify entry failed: {e}")

    def search_entry(
        self,
        base_dn: str,
        search_filter: str = "(objectClass=*)",
        attributes: t.StrSequence | None = None,
    ) -> p.Result[Sequence[m.Ldif.Entry]]:
        """Search LDAP entries using flext-ldap API."""
        try:
            if not base_dn:
                return r[Sequence[m.Ldif.Entry]].fail("Base DN required")
            FlextTargetLdapClient._logger.info(
                "Searching LDAP entries using flext-ldap API: %s with filter %s",
                base_dn,
                search_filter,
            )
            connect_result = self._api.connect(self.settings)
            if connect_result.failure:
                return r[Sequence[m.Ldif.Entry]].fail(
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
            if result.success and result.value:
                entries: MutableSequence[m.Ldif.Entry] = []
                search_res = result.value
                ldap_entries: Sequence[t.MappingKV[str, t.StrSequence]] = (
                    search_res.entries
                )
                for entry in ldap_entries:
                    entries.append(u.Ldif.as_entry(entry))
                FlextTargetLdapClient._logger.debug(
                    "Successfully found %d LDAP entries",
                    len(entries),
                )
                return r[Sequence[m.Ldif.Entry]].ok(entries)
            FlextTargetLdapClient._logger.debug("No LDAP entries found")
            return r[Sequence[m.Ldif.Entry]].ok([])
        except (RuntimeError, ValueError, TypeError) as e:
            FlextTargetLdapClient._logger.exception(
                "Failed to search entries in %s",
                base_dn,
            )
            return r[Sequence[m.Ldif.Entry]].fail(f"Search failed: {e}")


__all__: list[str] = ["FlextTargetLdapClient"]
