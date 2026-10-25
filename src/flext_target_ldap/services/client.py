"""LDAP directory client delegating all operations to flext-ldap.

The concrete directory adapter of the target. Sinks never name it: they consume
the ``p.TargetLdap.Directory`` capability, and ``api.py`` binds this class at the
composition root.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_ldap import ldap

from flext_target_ldap import FlextTargetLdapSettings, m, p, r, t, u


class FlextTargetLdapClient:
    """Directory client using the flext-ldap API for every operation."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)
    settings: m.Ldap.ConnectionConfig

    def __init__(
        self,
        settings: (
            FlextTargetLdapSettings
            | m.Ldap.ConnectionConfig
            | t.TargetLdap.SettingsPayload
        ),
    ) -> None:
        """Initialize the client with its connection configuration."""
        connection_settings = u.TargetLdap.connection_config(settings)
        self.settings = connection_settings
        self._bind_dn = connection_settings.bind_dn or ""
        self._password = connection_settings.bind_password or ""
        self._api = ldap
        FlextTargetLdapClient.logger.info(
            "Initialized LDAP client using flext-ldap API for %s:%s",
            self.settings.host,
            self.settings.port,
        )

    @property
    def bind_dn(self) -> str:
        """The bind DN."""
        return self._bind_dn

    @property
    def host(self) -> str:
        """The server host."""
        host: str = self.settings.host
        return host

    @property
    def password(self) -> str:
        """The password."""
        return self._password

    @property
    def port(self) -> int:
        """The server port."""
        port: int = self.settings.port
        return port

    @property
    def server_uri(self) -> str:
        """The server URI."""
        protocol = "ldaps" if self.settings.use_ssl else "ldap"
        return f"{protocol}://{self.settings.host}:{self.settings.port}"

    @property
    def timeout(self) -> int:
        """The timeout."""
        timeout: int = self.settings.timeout
        return timeout

    @property
    def use_ssl(self) -> bool:
        """The SSL usage."""
        use_ssl: bool = self.settings.use_ssl
        return use_ssl

    def add_entry(
        self,
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Add one LDAP entry.

        Args:
            dn: Distinguished name of the entry to add.
            attributes: Entry attributes to write.
            object_classes: Optional object classes for the entry.

        Returns:
            The outcome of the add operation.

        """
        FlextTargetLdapClient.logger.info("Adding LDAP entry: %s", dn)
        connect_result = self._api.connect(self.settings)
        if connect_result.failure:
            return r[bool].fail_op("Connection", connect_result.error)
        try:
            result = self._api.add(
                u.TargetLdap.ldif_entry(dn, attributes, object_classes),
            )
        finally:
            self._api.disconnect()
        if result.success:
            return r[bool].ok(value=True)
        return r[bool].fail(f"LDAP add failed for {dn}: {result.error}")

    def connect(self) -> p.Result[bool]:
        """Validate connectivity to the configured LDAP server.

        Returns:
            The outcome of the connectivity check.

        """
        connect_result = self._api.connect(self.settings)
        if connect_result.failure:
            return r[bool].fail_op("Connection", connect_result.error)
        self._api.disconnect()
        FlextTargetLdapClient.logger.info(
            "LDAP connectivity validated for %s:%s",
            self.settings.host,
            self.settings.port,
        )
        return r[bool].ok(value=True)

    def delete_entry(self, dn: str) -> p.Result[bool]:
        """Delete one LDAP entry.

        Args:
            dn: Distinguished name of the entry to delete.

        Returns:
            The outcome of the delete operation.

        """
        if not dn:
            return r[bool].fail("DN required")
        FlextTargetLdapClient.logger.info("Deleting LDAP entry: %s", dn)
        connect_result = self._api.connect(self.settings)
        if connect_result.failure:
            return r[bool].fail_op("Connection", connect_result.error)
        try:
            result = self._api.delete(dn)
        finally:
            self._api.disconnect()
        if result.success:
            return r[bool].ok(value=True)
        return r[bool].fail(f"LDAP delete failed for {dn}: {result.error}")

    def disconnect(self) -> p.Result[bool]:
        """Disconnect the flext-ldap session.

        Returns:
            The outcome of the disconnect operation.

        """
        self._api.disconnect()
        return r[bool].ok(value=True)

    def modify_entry(
        self,
        dn: str,
        changes: t.Ldap.OperationAttributes,
    ) -> p.Result[bool]:
        """Replace the given attributes of one LDAP entry.

        Args:
            dn: Distinguished name of the entry to modify.
            changes: Attribute values to replace on the entry.

        Returns:
            The outcome of the modify operation.

        """
        FlextTargetLdapClient.logger.info("Modifying LDAP entry: %s", dn)
        connect_result = self._api.connect(self.settings)
        if connect_result.failure:
            return r[bool].fail_op("Connection", connect_result.error)
        try:
            result = self._api.modify(dn, u.TargetLdap.modify_changes(changes))
        finally:
            self._api.disconnect()
        if result.success:
            return r[bool].ok(value=True)
        return r[bool].fail(f"Failed to modify entry {dn}: {result.error}")

    def search_entry(
        self,
        base_dn: str,
        search_filter: str = "(objectClass=*)",
        attributes: t.StrSequence | None = None,
    ) -> p.Result[list[m.Ldif.Entry]]:
        """Search LDAP entries.

        Args:
            base_dn: Subtree root for the search.
            search_filter: LDAP search filter.
            attributes: Optional attribute names restricting each entry.

        Returns:
            The matching entries, empty when none match, or a failure
            result when the search fails.

        """
        if not base_dn:
            return r[list[m.Ldif.Entry]].fail("Base DN required")
        connect_result = self._api.connect(self.settings)
        if connect_result.failure:
            return r[list[m.Ldif.Entry]].fail_op("Connection", connect_result.error)
        try:
            result = self._api.search(
                m.Ldap.SearchOptions(
                    base_dn=base_dn,
                    filter_str=search_filter,
                    attributes=attributes,
                ),
            )
        finally:
            self._api.disconnect()
        if result.failure:
            return r[list[m.Ldif.Entry]].fail_op("Search", result.error)
        return r[list[m.Ldif.Entry]].ok(list(result.value.entries))


__all__: list[str] = ["FlextTargetLdapClient"]
