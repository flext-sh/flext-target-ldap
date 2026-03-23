"""Tests for LDAP client using ldap3.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from unittest.mock import MagicMock, patch

import pytest
from flext_core import t

from flext_target_ldap import LdapTargetClient
from flext_target_ldap.client import LDAPClient, LDAPSearchEntry

EXPECTED_DATA_COUNT = 3


class TestLDAPClient:
    """Test LDAP client functionality."""

    @pytest.fixture
    def client(self, mock_ldap_config: Mapping[str, t.ContainerValue]) -> LDAPClient:
        """Create test LDAPClient instance."""
        return LDAPClient(config=mock_ldap_config)

    @pytest.fixture
    def target_client(
        self, mock_ldap_config: Mapping[str, t.ContainerValue]
    ) -> LdapTargetClient:
        """Create test LdapTargetClient instance."""
        return LdapTargetClient(config=mock_ldap_config)

    def test_client_initialization(self, target_client: LdapTargetClient) -> None:
        """Test LDAP client initialization with configuration values."""
        if target_client.host != "test.ldap.com":
            msg: str = f"Expected {'test.ldap.com'}, got {target_client.host}"
            raise AssertionError(msg)
        assert target_client.port == 389
        if target_client.bind_dn != "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com":
            msg: str = f"Expected {'cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com'}, got {target_client.bind_dn}"
            raise AssertionError(msg)
        assert target_client.password == "test_password"
        assert not target_client.use_ssl
        if target_client.timeout != 30:
            msg: str = f"Expected {30}, got {target_client.timeout}"
            raise AssertionError(msg)

    def test_server_uri_construction(self, target_client: LdapTargetClient) -> None:
        """Test server URI construction with and without SSL."""
        if target_client.server_uri != "ldap://test.ldap.com:389":
            msg: str = (
                f"Expected {'ldap://test.ldap.com:389'}, got {target_client.server_uri}"
            )
            raise AssertionError(msg)
        # Create new client with SSL enabled to test LDAPS URI
        ssl_config = {
            "host": "test.ldap.com",
            "port": 389,
            "use_ssl": True,
            "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
            "password": "test_password",
            "timeout": 30,
        }
        ssl_client = LdapTargetClient(config=ssl_config)
        if ssl_client.server_uri != "ldaps://test.ldap.com:389":
            msg: str = (
                f"Expected {'ldaps://test.ldap.com:389'}, got {ssl_client.server_uri}"
            )
            raise AssertionError(msg)

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_get_connection(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test getting LDAP connection with proper binding and cleanup."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        with client.get_connection() as conn:
            if conn != mock_connection:
                msg: str = f"Expected {mock_connection}, got {conn}"
                raise AssertionError(msg)
        mock_connection_class.assert_called_once_with(
            mock_pool, user=client._bind_dn, password=client._password
        )
        mock_connection.bind.assert_called_once()
        mock_connection.unbind.assert_called_once()

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_add_entry(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test adding a new LDAP entry."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.add.return_value = True
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_classes=["inetOrgPerson", "person"],
            attributes={"cn": "Test User", "sn": "User"},
        )
        assert result.is_success
        if not result.value:
            msg: str = f"Expected True, got {result.value}"
            raise AssertionError(msg)
        mock_connection.add.assert_called_once()

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_add_entry_already_exists(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test adding an LDAP entry that already exists."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.add.side_effect = Exception("Entry already exists")
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_classes=["person"],
            attributes={"cn": "Test"},
        )
        assert not result.is_success
        assert result.error is not None
        if "Entry already exists" not in result.error:
            msg: str = f"Expected {'Entry already exists'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_modify_entry(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test modifying an existing LDAP entry."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.modify.return_value = True
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.modify_entry(
            dn="uid=test,dc=test,dc=com",
            changes={"mail": "new@test.com", "telephoneNumber": "123-456"},
        )
        assert result.is_success
        if not result.value:
            msg: str = f"Expected True, got {result.value}"
            raise AssertionError(msg)
        mock_connection.modify.assert_called_once()

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_delete_entry(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test deleting an LDAP entry."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.delete.return_value = True
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.delete_entry("uid=test,dc=test,dc=com")
        assert result.is_success
        if not result.value:
            msg: str = f"Expected True, got {result.value}"
            raise AssertionError(msg)
        mock_connection.delete.assert_called_once_with("uid=test,dc=test,dc=com")

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_search_entry(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test searching for LDAP entries."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.search.return_value = True
        mock_entry = LDAPSearchEntry(
            dn="uid=test,dc=test,dc=com",
            attributes={"cn": ["Test User"], "mail": ["test@example.com"]},
        )
        mock_connection.entries = [mock_entry]
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.search_entry("dc=test,dc=com")
        assert result.is_success
        entries = result.value
        if len(entries) != 1:
            msg: str = f"Expected {1}, got {len(entries)}"
            raise AssertionError(msg)
        assert entries[0].dn == "uid=test,dc=test,dc=com"
        if entries[0].attributes["cn"] != ["Test User"]:
            msg: str = f"Expected {['Test User']}, got {entries[0].attributes['cn']}"
            raise AssertionError(msg)
        assert entries[0].attributes["mail"] == ["test@example.com"]

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_entry_exists(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test checking if an LDAP entry exists."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.search.return_value = True
        mock_entry = LDAPSearchEntry(
            dn="uid=test,dc=test,dc=com",
            attributes={"cn": ["Test User"]},
        )
        mock_connection.entries = [mock_entry]
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.entry_exists("uid=test,dc=test,dc=com")
        assert result.is_success
        if not result.value:
            msg: str = f"Expected True, got {result.value}"
            raise AssertionError(msg)
        mock_connection.entries = Sequence[t.NormalizedValue]()
        result = client.entry_exists("uid=notfound,dc=test,dc=com")
        assert result.is_success
        if result.value:
            msg: str = f"Expected False, got {result.value}"
            raise AssertionError(msg)

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_get_entry(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test getting a specific LDAP entry."""
        mock_connection = MagicMock()
        mock_connection.bind.return_value = True
        mock_connection.bound = True
        mock_connection.search.return_value = True
        mock_entry = LDAPSearchEntry(
            dn="uid=test,dc=test,dc=com",
            attributes={"cn": ["Test User"], "mail": ["test@example.com"]},
        )
        mock_connection.entries = [mock_entry]
        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        result = client.get_entry("uid=test,dc=test,dc=com")
        assert result.is_success
        entry = result.value
        assert entry is not None
        if entry.dn != "uid=test,dc=test,dc=com":
            msg: str = f"Expected {'uid=test,dc=test,dc=com'}, got {entry.dn}"
            raise AssertionError(msg)
        assert entry.attributes["cn"] == ["Test User"]
        mock_connection.entries = Sequence[t.NormalizedValue]()
        result = client.get_entry("uid=notfound,dc=test,dc=com")
        assert result.is_success
        assert result.value is None

    @patch("flext_target_ldap.client.ldap3.Connection")
    @patch("flext_target_ldap.client.ldap3.ServerPool")
    def test_connection_error_handling(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test handling of LDAP connection errors."""
        mock_connection_class.side_effect = RuntimeError("Connection failed")
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        with pytest.raises(RuntimeError), client.get_connection():
            pass


def test_connection_wrapper_unbind_cleans_state_and_disconnects() -> None:

    class _ConnectResult:
        is_success = True

    fake_api = MagicMock()
    fake_api.connect.return_value = _ConnectResult()
    client = LDAPClient({"host": "ldap.local", "port": 389})
    client._api = fake_api
    wrapper = client._get_flext_ldap_wrapper()
    wrapper.entries = [{"dn": "cn=entry"}]
    wrapper.unbind()
    assert wrapper.bound is False
    assert wrapper.entries == []
    fake_api.disconnect.assert_called_once()
