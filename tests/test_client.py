"""Tests for the canonical LDAP target client."""

from __future__ import annotations

from collections.abc import Mapping
from unittest.mock import MagicMock

import pytest
from flext_core import r

from flext_target_ldap import FlextTargetLdapClient, FlextTargetLdapSearchEntry
from tests import t


class TestLDAPClient:
    """Test LDAP client functionality through flext-ldap."""

    @pytest.fixture
    def client(
        self,
        mock_ldap_config: Mapping[str, t.ContainerValue],
    ) -> FlextTargetLdapClient:
        """Create test target client instance."""
        return FlextTargetLdapClient(config=mock_ldap_config)

    def test_client_initialization(self, client: FlextTargetLdapClient) -> None:
        """Test LDAP client initialization with configuration values."""
        assert client.host == "test.ldap.com"
        assert client.port == 389
        assert client.bind_dn == "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com"
        assert client.password == "test_password"
        assert not client.use_ssl
        assert client.timeout == 30

    def test_server_uri_construction(self, client: FlextTargetLdapClient) -> None:
        """Test server URI construction with and without SSL."""
        assert client.server_uri == "ldap://test.ldap.com:389"
        ssl_client = FlextTargetLdapClient(
            config={
                "host": "test.ldap.com",
                "port": 389,
                "use_ssl": True,
                "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
                "password": "test_password",
                "timeout": 30,
            },
        )
        assert ssl_client.server_uri == "ldaps://test.ldap.com:389"

    def test_connect_delegates_to_flext_ldap_api(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test connect delegates to the flext-ldap facade."""
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)

        result = client.connect()

        assert result.is_success
        assert result.value is True
        client._api.connect.assert_called_once_with(client.config)
        client._api.disconnect.assert_called_once()

    def test_disconnect_calls_flext_ldap_api(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test disconnect delegates to the flext-ldap facade."""
        client._api = MagicMock()

        result = client.disconnect()

        assert result.is_success
        assert result.value is True
        client._api.disconnect.assert_called_once_with()

    def test_add_entry_uses_real_ldif_entry(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test add_entry converts payloads into real LDIF entries."""
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.add.return_value = MagicMock(is_success=True, error=None)

        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_classes=["inetOrgPerson", "person"],
            attributes={"cn": "Test User", "sn": "User"},
        )

        assert result.is_success
        assert result.value is True
        client._api.connect.assert_called_once_with(client.config)
        client._api.add.assert_called_once()
        entry = client._api.add.call_args.args[0]
        assert entry.dn.value == "uid=test,dc=test,dc=com"
        assert entry.attributes.attributes["objectClass"] == [
            "inetOrgPerson",
            "person",
        ]
        client._api.disconnect.assert_called_once()

    def test_modify_entry_uses_real_modify_changes(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test modify_entry delegates actual LDAP modify operations."""
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.modify.return_value = MagicMock(is_success=True, error=None)

        result = client.modify_entry(
            dn="uid=test,dc=test,dc=com",
            changes={"mail": "new@test.com", "telephoneNumber": "123-456"},
        )

        assert result.is_success
        assert result.value is True
        client._api.modify.assert_called_once_with(
            "uid=test,dc=test,dc=com",
            {
                "mail": [(2, ["new@test.com"])],
                "telephoneNumber": [(2, ["123-456"])],
            },
        )
        client._api.disconnect.assert_called_once()

    def test_delete_entry_delegates_to_flext_ldap_api(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test delete_entry delegates actual LDAP delete operations."""
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.delete.return_value = MagicMock(is_success=True, error=None)

        result = client.delete_entry("uid=test,dc=test,dc=com")

        assert result.is_success
        assert result.value is True
        client._api.delete.assert_called_once_with("uid=test,dc=test,dc=com")
        client._api.disconnect.assert_called_once()

    def test_search_entry_maps_search_results(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test search_entry converts LDAP results to target search entries."""
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.search.return_value = MagicMock(
            is_success=True,
            value=MagicMock(
                entries=[
                    {
                        "dn": "uid=test,dc=test,dc=com",
                        "cn": ["Test User"],
                    },
                ],
            ),
        )

        result = client.search_entry(
            base_dn="dc=test,dc=com",
            search_filter="(uid=test)",
            attributes=["cn"],
        )

        assert result.is_success
        assert result.value is not None
        assert len(result.value) == 1
        entry = result.value[0]
        assert isinstance(entry, FlextTargetLdapSearchEntry)
        assert entry.dn == "uid=test,dc=test,dc=com"
        assert entry.attributes == {"cn": ["Test User"]}

    def test_get_connection_returns_real_wrapper(
        self,
        client: FlextTargetLdapClient,
    ) -> None:
        """Test get_connection exposes a live wrapper around flext-ldap."""
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)

        with client.get_connection() as wrapper:
            assert wrapper.bind() is True
            assert wrapper.bound

        client._api.disconnect.assert_called_once()


__all__ = ["TestLDAPClient"]
