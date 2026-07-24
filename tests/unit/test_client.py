"""Behavioral tests for the target-ldap client against real OpenLDAP."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_target_ldap._utilities.client import FlextTargetLdapClient
from flext_tests import tm

if TYPE_CHECKING:
    from tests import t


@pytest.fixture
def client(mock_ldap_config: t.TargetLdap.SettingsPayload) -> FlextTargetLdapClient:
    return FlextTargetLdapClient(settings=mock_ldap_config)


@pytest.fixture
def real_client(
    real_connection_config: t.TargetLdap.SettingsPayload,
) -> FlextTargetLdapClient:
    """Build a client bound to the real OpenLDAP container connection."""
    return FlextTargetLdapClient(settings=real_connection_config)


@pytest.fixture
def people_ou(real_client: FlextTargetLdapClient, real_base_dn: str) -> str:
    """Ensure the people OU exists for entry tests."""
    ou_dn = f"ou=people,{real_base_dn}"
    real_client.add_entry(
        dn=ou_dn,
        object_classes=["organizationalUnit", "top"],
        attributes={"ou": "people"},
    )
    return ou_dn


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

    @pytest.mark.integration
    def test_connect_reaches_real_ldap_server(
        self, real_client: FlextTargetLdapClient
    ) -> None:
        result = real_client.connect()
        tm.ok(result)
        tm.that(result.value, eq=True)

    @pytest.mark.integration
    def test_disconnect_reports_success(
        self, real_client: FlextTargetLdapClient
    ) -> None:
        result = real_client.disconnect()
        tm.ok(result)
        tm.that(result.value, eq=True)

    @pytest.mark.integration
    def test_add_entry_persists_to_real_server(
        self, real_client: FlextTargetLdapClient, people_ou: str
    ) -> None:
        dn = f"uid=addtest,{people_ou}"
        real_client.delete_entry(dn)
        add_result = real_client.add_entry(
            dn=dn,
            object_classes=["inetOrgPerson", "person", "top"],
            attributes={"cn": "Add Test", "sn": "Test"},
        )
        tm.ok(add_result)
        tm.that(add_result.value, eq=True)
        search_result = real_client.search_entry(
            base_dn=people_ou, search_filter="(uid=addtest)", attributes=["cn", "sn"]
        )
        tm.ok(search_result)
        tm.that(len(search_result.unwrap()), eq=1)
        real_client.delete_entry(dn)

    @pytest.mark.integration
    def test_modify_entry_updates_real_server(
        self, real_client: FlextTargetLdapClient, people_ou: str
    ) -> None:
        dn = f"uid=modtest,{people_ou}"
        real_client.delete_entry(dn)
        real_client.add_entry(
            dn=dn,
            object_classes=["inetOrgPerson", "person", "top"],
            attributes={"cn": "Mod Test", "sn": "Test"},
        )
        modify_result = real_client.modify_entry(
            dn=dn, changes={"mail": "mod@flext.local"}
        )
        tm.ok(modify_result)
        tm.that(modify_result.value, eq=True)
        search_result = real_client.search_entry(
            base_dn=people_ou, search_filter="(uid=modtest)", attributes=["mail"]
        )
        tm.ok(search_result)
        tm.that(len(search_result.unwrap()), eq=1)
        real_client.delete_entry(dn)

    @pytest.mark.integration
    def test_delete_entry_removes_from_real_server(
        self, real_client: FlextTargetLdapClient, people_ou: str
    ) -> None:
        dn = f"uid=deltest,{people_ou}"
        real_client.add_entry(
            dn=dn,
            object_classes=["inetOrgPerson", "person", "top"],
            attributes={"cn": "Del Test", "sn": "Test"},
        )
        delete_result = real_client.delete_entry(dn)
        tm.ok(delete_result)
        tm.that(delete_result.value, eq=True)
        search_result = real_client.search_entry(
            base_dn=people_ou, search_filter="(uid=deltest)", attributes=["cn"]
        )
        tm.ok(search_result)
        tm.that(len(search_result.unwrap()), eq=0)

    @pytest.mark.integration
    def test_search_entry_maps_real_results(
        self, real_client: FlextTargetLdapClient, people_ou: str
    ) -> None:
        dn = f"uid=searchtest,{people_ou}"
        real_client.delete_entry(dn)
        real_client.add_entry(
            dn=dn,
            object_classes=["inetOrgPerson", "person", "top"],
            attributes={"cn": "Search Test", "sn": "Test"},
        )
        result = real_client.search_entry(
            base_dn=people_ou, search_filter="(uid=searchtest)", attributes=["cn"]
        )
        tm.ok(result)
        entries = result.unwrap()
        tm.that(len(entries), eq=1)
        entry = entries[0]
        entry_dn = tm.not_none(entry.dn)
        tm.that(entry_dn.value, eq=dn)
        real_client.delete_entry(dn)
