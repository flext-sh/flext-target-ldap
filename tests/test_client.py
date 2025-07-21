"""Tests for LDAP client."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from ldap3.core.exceptions import LDAPException

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
        assert client.auto_bind

    def test_server_uri(self, client: LDAPClient) -> None:
        assert client.server_uri == "ldap://test.ldap.com:389"

        client.use_ssl = True
        assert client.server_uri == "ldaps://test.ldap.com:389"

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_get_connection(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_server = MagicMock()
        mock_server_class.return_value = mock_server

        mock_connection = MagicMock()
        mock_connection.bound = True
        mock_connection_class.return_value = mock_connection

        with client.get_connection() as conn:
            assert conn == mock_connection

        # Verify connection setup
        mock_server_class.assert_called_once_with(
            "test.ldap.com",
            port=389,
            use_ssl=False,
            get_info=True,
            connect_timeout=30,
        )

        mock_connection_class.assert_called_once_with(
            mock_server,
            user="cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
            password="test_password",
            authentication=1,  # SIMPLE
            auto_bind=True,
            raise_exceptions=True,
        )

        # Verify unbind
        mock_connection.unbind.assert_called_once()

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_add_entry(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.bound = True
        mock_connection.add.return_value = True
        mock_connection_class.return_value = mock_connection

        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_class=["inetOrgPerson", "person"],
            attributes={"cn": "Test User", "sn": "User"},
        )

        assert result.is_success
        assert result.data is True

        # Verify add was called correctly
        mock_connection.add.assert_called_once_with(
            "uid=test,dc=test,dc=com",
            attributes={
                "cn": "Test User",
                "sn": "User",
                "objectClass": ["inetOrgPerson", "person"],
            },
        )

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_add_entry_failure(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.bound = True
        mock_connection.add.return_value = False
        mock_connection.result = {"description": "Entry already exists"}
        mock_connection_class.return_value = mock_connection

        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_class="person",
            attributes={"cn": "Test"},
        )

        assert not result.is_success
        assert result.error
        assert "Failed to add entry" in result.error

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_modify_entry(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.bound = True
        mock_connection.modify.return_value = True
        mock_connection_class.return_value = mock_connection

        result = client.modify_entry(
            dn="uid=test,dc=test,dc=com",
            changes={"mail": "new@test.com", "telephoneNumber": "123-456"},
            operation="replace",
        )

        assert result.is_success
        assert result.data is True

        # Verify modify was called
        expected_changes = {
            "mail": [(2, "new@test.com")],  # MODIFY_REPLACE = 2
            "telephoneNumber": [(2, "123-456")],
        }
        mock_connection.modify.assert_called_once_with(
            "uid=test,dc=test,dc=com",
            expected_changes,
        )

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_delete_entry(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.bound = True
        mock_connection.delete.return_value = True
        mock_connection_class.return_value = mock_connection

        result = client.delete_entry("uid=test,dc=test,dc=com")

        assert result.is_success
        assert result.data is True
        mock_connection.delete.assert_called_once_with("uid=test,dc=test,dc=com")

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_entry_exists(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.bound = True
        mock_connection.search.return_value = True

        # Entry exists
        mock_connection.entries = [MagicMock()]
        mock_connection_class.return_value = mock_connection

        result = client.entry_exists("uid=test,dc=test,dc=com")
        assert result.is_success
        assert result.data is True

        # Entry doesn't exist
        mock_connection.entries = []
        result = client.entry_exists("uid=notfound,dc=test,dc=com")
        assert result.is_success
        assert result.data is False

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_upsert_entry(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        mock_connection = MagicMock()
        mock_connection.bound = True

        # First call: entry doesn't exist
        mock_connection.search.return_value = True
        mock_connection.entries = []
        mock_connection.add.return_value = True

        mock_connection_class.return_value = mock_connection

        result = client.upsert_entry(
            dn="uid=test,dc=test,dc=com",
            object_class="person",
            attributes={"cn": "Test"},
        )

        assert result.is_success
        assert result.data is not None
        success, operation = result.data
        assert success is True
        assert operation == "add"
        mock_connection.add.assert_called_once()

    def test_validate_dn(self, client: LDAPClient) -> None:
        # Valid DNs
        result = client.validate_dn("uid=test,dc=example,dc=com")
        assert result.is_success
        assert result.data is True
        result = client.validate_dn("cn=Test User,ou=users,dc=example,dc=com")
        assert result.is_success
        assert result.data is True
        result = client.validate_dn("o=Example Corp")
        assert result.is_success
        assert result.data is True

        # Invalid DNs
        result = client.validate_dn("")
        assert not result.is_success
        result = client.validate_dn("invalid")
        assert not result.is_success
        result = client.validate_dn("uid=,dc=test")
        assert not result.is_success
        result = client.validate_dn("=test,dc=com")
        assert not result.is_success
        result = client.validate_dn("uid=test,")
        assert not result.is_success

    @patch("flext_target_ldap.client.Connection")
    @patch("flext_target_ldap.client.Server")
    def test_connection_error_handling(
        self,
        mock_server_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        # Simulate connection error
        mock_connection_class.side_effect = LDAPException("Connection failed")

        with pytest.raises(LDAPException) as exc_info, client.get_connection():
            pass

        assert "Connection failed" in str(exc_info.value)
