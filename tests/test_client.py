"""Tests for LDAP client using ldap3.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from ldap3.core import exceptions as ldap3_exceptions

from flext_core import FlextTypes
from flext_target_ldap import LDAPClient

# Constants
EXPECTED_DATA_COUNT = 3


class TestLDAPClient:
    """Test LDAP client functionality."""

    @pytest.fixture
    def client(self, mock_ldap_config: FlextTypes.Core.Dict) -> LDAPClient:
        """Create test LDAP client instance."""
        return LDAPClient(config=mock_ldap_config)

    def test_client_initialization(self, client: LDAPClient) -> None:
        """Test LDAP client initialization with configuration values."""
        if client.host != "test.ldap.com":
            msg: str = f"Expected {'test.ldap.com'}, got {client.host}"
            raise AssertionError(msg)
        assert client.port == 389
        if client.bind_dn != "cn=admin,dc=test,dc=com":
            msg: str = f"Expected {'cn=admin,dc=test,dc=com'}, got {client.bind_dn}"
            raise AssertionError(msg)
        assert client.password == "test_password"
        assert not client.use_ssl
        if client.timeout != 30:
            msg: str = f"Expected {30}, got {client.timeout}"
            raise AssertionError(msg)

    def test_server_uri_construction(self, client: LDAPClient) -> None:
        """Test server URI construction with and without SSL."""
        if client.server_uri != "ldap://test.ldap.com:389":
            msg: str = f"Expected {'ldap://test.ldap.com:389'}, got {client.server_uri}"
            raise AssertionError(msg)

        client.use_ssl = True
        if client.server_uri != "ldaps://test.ldap.com:389":
            msg: str = (
                f"Expected {'ldaps://test.ldap.com:389'}, got {client.server_uri}"
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

        # Verify connection was created with server pool
        mock_connection_class.assert_called_once_with(
            mock_pool,
            user=client.bind_dn,
            password=client.password,
        )

        # Verify bind was called
        mock_connection.bind.assert_called_once()

        # Verify unbind was called
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

        assert result.success
        if not (result.data):
            msg: str = f"Expected True, got {result.data}"
            raise AssertionError(msg)

        # Verify add was called correctly
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
        mock_connection.add.side_effect = (
            ldap3_exceptions.LDAPEntryAlreadyExistsResult()
        )
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

        assert result.success
        if not (result.data):
            msg: str = f"Expected True, got {result.data}"
            raise AssertionError(msg)

        # Verify modify was called
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

        assert result.success
        if not (result.data):
            msg: str = f"Expected True, got {result.data}"
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

        # Mock ldap3 entry objects
        mock_entry = MagicMock()
        mock_entry.entry_dn = "uid=test,dc=test,dc=com"
        mock_entry.entry_attributes = ["cn", "mail"]
        mock_entry.cn = ["Test User"]
        mock_entry.mail = ["test@example.com"]
        mock_connection.entries = [mock_entry]

        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        result = client.search_entry("dc=test,dc=com")

        assert result.success
        entries = result.data
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

        # Mock entry exists
        mock_entry = MagicMock()
        mock_entry.entry_dn = "uid=test,dc=test,dc=com"
        mock_entry.entry_attributes = ["cn"]
        mock_entry.cn = ["Test User"]
        mock_connection.entries = [mock_entry]

        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        result = client.entry_exists("uid=test,dc=test,dc=com")
        assert result.success
        if not (result.data):
            msg: str = f"Expected True, got {result.data}"
            raise AssertionError(msg)

        # Test entry doesn't exist
        mock_connection.entries = []
        result = client.entry_exists("uid=notfound,dc=test,dc=com")
        assert result.success
        if result.data:
            msg: str = f"Expected False, got {result.data}"
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

        # Mock entry found
        mock_entry = MagicMock()
        mock_entry.entry_dn = "uid=test,dc=test,dc=com"
        mock_entry.entry_attributes = ["cn", "mail"]
        mock_entry.cn = ["Test User"]
        mock_entry.mail = ["test@example.com"]
        mock_connection.entries = [mock_entry]

        mock_connection_class.return_value = mock_connection
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        result = client.get_entry("uid=test,dc=test,dc=com")

        assert result.success
        entry = result.data
        assert entry is not None
        if entry.dn != "uid=test,dc=test,dc=com":
            msg: str = f"Expected {'uid=test,dc=test,dc=com'}, got {entry.dn}"
            raise AssertionError(msg)
        assert entry.attributes["cn"] == ["Test User"]

        # Test entry not found
        mock_connection.entries = []
        result = client.get_entry("uid=notfound,dc=test,dc=com")
        assert result.success
        assert result.data is None

    def test_connection_error_handling(
        self,
        mock_pool_class: MagicMock,
        mock_connection_class: MagicMock,
        client: LDAPClient,
    ) -> None:
        """Test handling of LDAP connection errors."""
        # Simulate connection error
        mock_connection_class.side_effect = ldap3_exceptions.LDAPError(
            "Connection failed",
        )
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool

        with pytest.raises(ldap3_exceptions.LDAPError), client.get_connection():
            pass
