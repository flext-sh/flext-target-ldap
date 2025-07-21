"""Tests for LDAP client using python-ldap."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import ldap
import pytest

from flext_target_ldap.client import LDAPClient


class TestLDAPClient:
    """Test LDAP client functionality."""

    @pytest.fixture
    def client(self, mock_ldap_config: dict[str, Any]) -> LDAPClient:
        return LDAPClient(
            host=mock_ldap_config["host"],
            port=mock_ldap_config["port"],
            bind_dn=mock_ldap_config["bind_dn"],
            password=mock_ldap_config["password"],
            use_ssl=mock_ldap_config["use_ssl"],
            timeout=mock_ldap_config["timeout"],
        )

    def test_client_initialization(self, client: LDAPClient) -> None:
        assert client.host == "test.ldap.com"
        assert client.port == 389
        assert client.bind_dn == "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com"
        assert client.password == "test_password"
        assert not client.use_ssl
        assert client.timeout == 30

    def test_server_uri(self, client: LDAPClient) -> None:
        assert client.server_uri == "ldap://test.ldap.com:389"

        client.use_ssl = True
        assert client.server_uri == "ldaps://test.ldap.com:389"

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_get_connection(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_initialize.return_value = mock_connection

        with client.get_connection() as conn:
            assert conn == mock_connection

        # Verify connection setup
        mock_initialize.assert_called_once_with(client.server_uri)

        # Verify connection options were set
        mock_connection.set_option.assert_any_call(
            ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3,
        )
        mock_connection.set_option.assert_any_call(
            ldap.OPT_NETWORK_TIMEOUT, 30,
        )
        mock_connection.set_option.assert_any_call(ldap.OPT_REFERRALS, 0)

        # Verify bind was called
        mock_connection.simple_bind_s.assert_called_once_with(
            "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com", "test_password",
        )

        # Verify unbind
        mock_connection.unbind_s.assert_called_once()

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_add_entry(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_initialize.return_value = mock_connection

        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_class=["inetOrgPerson", "person"],
            attributes={"cn": "Test User", "sn": "User"},
        )

        assert result.is_success
        assert result.unwrap() is True

        # Verify add was called correctly
        mock_connection.add_s.assert_called_once()

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_add_entry_already_exists(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.add_s.side_effect = ldap.ALREADY_EXISTS()
        mock_initialize.return_value = mock_connection

        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_class="person",
            attributes={"cn": "Test"},
        )

        assert not result.is_success
        assert "Entry already exists" in result.error

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_modify_entry(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_initialize.return_value = mock_connection

        result = client.modify_entry(
            dn="uid=test,dc=test,dc=com",
            changes={"mail": "new@test.com", "telephoneNumber": "123-456"},
        )

        assert result.is_success
        assert result.unwrap() is True

        # Verify modify was called
        mock_connection.modify_s.assert_called_once()

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_delete_entry(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_initialize.return_value = mock_connection

        result = client.delete_entry("uid=test,dc=test,dc=com")

        assert result.is_success
        assert result.unwrap() is True
        mock_connection.delete_s.assert_called_once_with("uid=test,dc=test,dc=com")

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_search_entry(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.search_s.return_value = [
            ("uid=test,dc=test,dc=com", {
                "cn": [b"Test User"],
                "mail": [b"test@example.com"],
            }),
        ]
        mock_initialize.return_value = mock_connection

        result = client.search_entry("dc=test,dc=com")

        assert result.is_success
        entries = result.unwrap()
        assert len(entries) == 1
        assert entries[0].dn == "uid=test,dc=test,dc=com"
        assert entries[0].attributes["cn"] == ["Test User"]
        assert entries[0].attributes["mail"] == ["test@example.com"]

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_entry_exists(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.search_s.return_value = [
            ("uid=test,dc=test,dc=com", {"cn": [b"Test User"]}),
        ]
        mock_initialize.return_value = mock_connection

        result = client.entry_exists("uid=test,dc=test,dc=com")
        assert result.is_success
        assert result.unwrap() is True

        # Test entry doesn't exist
        mock_connection.search_s.return_value = []
        result = client.entry_exists("uid=notfound,dc=test,dc=com")
        assert result.is_success
        assert result.unwrap() is False

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_get_entry(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.search_s.return_value = [
            ("uid=test,dc=test,dc=com", {
                "cn": [b"Test User"],
                "mail": [b"test@example.com"],
            }),
        ]
        mock_initialize.return_value = mock_connection

        result = client.get_entry("uid=test,dc=test,dc=com")

        assert result.is_success
        entry = result.unwrap()
        assert entry is not None
        assert entry.dn == "uid=test,dc=test,dc=com"
        assert entry.attributes["cn"] == ["Test User"]

        # Test entry not found
        mock_connection.search_s.return_value = []
        result = client.get_entry("uid=notfound,dc=test,dc=com")
        assert result.is_success
        assert result.unwrap() is None

    @patch("flext_target_ldap.client.ldap.initialize")
    def test_connection_error_handling(
        self,
        mock_initialize: MagicMock,
        client: LDAPClient,
    ) -> None:
        # Simulate connection error
        mock_initialize.side_effect = ldap.LDAPError("Connection failed")

        with pytest.raises(ldap.LDAPError), client.get_connection():
            pass
