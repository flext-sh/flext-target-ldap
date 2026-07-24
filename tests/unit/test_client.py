from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from flext_tests import r, tm

from flext_target_ldap._utilities.client import FlextTargetLdapClient
from tests import m, t


@pytest.fixture
def client(mock_ldap_config: t.TargetLdap.SettingsPayload) -> FlextTargetLdapClient:
    return FlextTargetLdapClient(settings=mock_ldap_config)


class TestsFlextTargetLdapClient:
    """Behavior contract for test_client."""

    def test_client_initialization(self, client: FlextTargetLdapClient) -> None:
        tm.that(client.host, eq="test.ldap.com")
        tm.that(client.port, eq=389)
        tm.that(client.bind_dn, eq="cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com")
        tm.that(client.password, eq="test_password")
        assert not client.use_ssl
        tm.that(client.timeout, eq=30)

    def test_server_uri_construction(self, client: FlextTargetLdapClient) -> None:
        tm.that(client.server_uri, eq="ldap://test.ldap.com:389")
        ssl_client = FlextTargetLdapClient(
            settings={
                "host": "test.ldap.com",
                "port": 389,
                "use_ssl": True,
                "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
                "password": "test_password",
                "timeout": 30,
            }
        )
        tm.that(ssl_client.server_uri, eq="ldaps://test.ldap.com:389")

    def test_connect_delegates_to_flext_ldap_api(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        result = client.connect()
        tm.ok(result)
        tm.that(result.value, eq=True)
        client._api.connect.assert_called_once_with(client.settings)
        client._api.disconnect.assert_called_once()

    def test_disconnect_calls_flext_ldap_api(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        result = client.disconnect()
        tm.ok(result)
        tm.that(result.value, eq=True)
        client._api.disconnect.assert_called_once_with()

    def test_add_entry_uses_real_ldif_entry(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.add.return_value = MagicMock(success=True, error=None)
        result = client.add_entry(
            dn="uid=test,dc=test,dc=com",
            object_classes=["inetOrgPerson", "person"],
            attributes={"cn": "Test User", "sn": "User"},
        )
        tm.ok(result)
        tm.that(result.value, eq=True)
        client._api.connect.assert_called_once_with(client.settings)
        client._api.add.assert_called_once()
        entry = client._api.add.call_args.args[0]
        tm.that(entry.dn.value, eq="uid=test,dc=test,dc=com")
        tm.that(
            entry.attributes.attributes["objectClass"], eq=["inetOrgPerson", "person"]
        )
        client._api.disconnect.assert_called_once()

    def test_modify_entry_uses_real_modify_changes(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.modify.return_value = MagicMock(success=True, error=None)
        result = client.modify_entry(
            dn="uid=test,dc=test,dc=com",
            changes={"mail": "new@test.com", "telephoneNumber": "123-456"},
        )
        tm.ok(result)
        tm.that(result.value, eq=True)
        client._api.modify.assert_called_once_with(
            "uid=test,dc=test,dc=com",
            {"mail": [(2, ["new@test.com"])], "telephoneNumber": [(2, ["123-456"])]},
        )
        client._api.disconnect.assert_called_once()

    def test_delete_entry_delegates_to_flext_ldap_api(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.delete.return_value = MagicMock(success=True, error=None)
        result = client.delete_entry("uid=test,dc=test,dc=com")
        tm.ok(result)
        tm.that(result.value, eq=True)
        client._api.delete.assert_called_once_with("uid=test,dc=test,dc=com")
        client._api.disconnect.assert_called_once()

    def test_search_entry_maps_search_results(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.search.return_value = MagicMock(
            success=True,
            value=MagicMock(
                entries=[
                    m.Ldif.Entry(
                        dn=m.Ldif.DN(value="uid=test,dc=test,dc=com"),
                        attributes=m.Ldif.Attributes(attributes={"cn": ["Test User"]}),
                    )
                ]
            ),
        )
        result = client.search_entry(
            base_dn="dc=test,dc=com", search_filter="(uid=test)", attributes=["cn"]
        )
        tm.ok(result)
        tm.that(result.value, none=False)
        tm.that(len(result.value), eq=1)
        entry = result.value[0]
        tm.that(entry, is_=m.Ldif.Entry)
        dn = entry.dn
        attributes = entry.attributes
        assert dn is not None
        assert attributes is not None
        tm.that(dn.value, eq="uid=test,dc=test,dc=com")
        tm.that(attributes.attributes, eq={"cn": ["Test User"]})

    def test_search_entry_disconnects_after_search(
        self, client: FlextTargetLdapClient
    ) -> None:
        client._api = MagicMock()
        client._api.connect.return_value = r[bool].ok(True)
        client._api.search.return_value = MagicMock(
            success=True,
            value=MagicMock(
                entries=[{"dn": "uid=test,dc=test,dc=com", "cn": ["Test User"]}]
            ),
        )
        result = client.search_entry("dc=test,dc=com")
        tm.ok(result)
        client._api.disconnect.assert_called_once()
