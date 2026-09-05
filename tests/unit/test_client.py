"""Observable behavior of the public target-ldap client contract."""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_target_ldap import settings
from flext_tests import tm
from tests import p, t


class TestsFlextTargetLdapClient:
    """Behavior contract for the public client factory."""

    def test_client_reflects_production_settings(
        self, ldap_client: p.TargetLdap.Client
    ) -> None:
        configured = settings.TargetLdap
        tm.that(ldap_client.host, eq=configured.host)
        tm.that(ldap_client.port, eq=configured.port)
        tm.that(ldap_client.bind_dn, eq=configured.bind_dn)
        tm.that(ldap_client.password, eq=configured.bind_password)
        tm.that(ldap_client.use_ssl, eq=configured.use_ssl)
        tm.that(ldap_client.timeout, eq=configured.timeout)

    def test_server_uri_reflects_production_settings(
        self, ldap_client: p.TargetLdap.Client
    ) -> None:
        configured = settings.TargetLdap
        scheme = "ldaps" if configured.use_ssl else "ldap"
        tm.that(
            ldap_client.server_uri,
            eq=f"{scheme}://{configured.host}:{configured.port}",
        )

    @pytest.mark.integration
    def test_connect_and_disconnect_reach_configured_runtime(
        self, ldap_runtime_client: p.TargetLdap.Client
    ) -> None:
        connected = ldap_runtime_client.connect()
        tm.ok(connected)
        tm.that(connected.value, eq=True)

        disconnected = ldap_runtime_client.disconnect()
        tm.ok(disconnected)
        tm.that(disconnected.value, eq=True)

    @pytest.mark.integration
    def test_entry_lifecycle_is_observable_in_configured_runtime(
        self,
        ldap_runtime_client: p.TargetLdap.Client,
        ldap_base_dn: str,
    ) -> None:
        identifier = f"flext-target-ldap-{uuid4().hex}"
        dn = f"uid={identifier},{ldap_base_dn}"
        created = False
        try:
            added = ldap_runtime_client.add_entry(
                dn=dn,
                object_classes=("inetOrgPerson", "person", "top"),
                attributes={"cn": identifier, "sn": identifier},
            )
            tm.ok(added)
            created = True

            changes: t.Ldap.OperationAttributes = {
                "mail": f"{identifier}@flext.local"
            }
            modified = ldap_runtime_client.modify_entry(dn=dn, changes=changes)
            tm.ok(modified)

            found = ldap_runtime_client.search_entry(
                base_dn=ldap_base_dn,
                search_filter=f"(uid={identifier})",
                attributes=("cn", "mail"),
            )
            tm.ok(found)
            entries = found.value
            tm.that(len(entries), eq=1)
            entry_dn = tm.not_none(entries[0].dn)
            tm.that(entry_dn.value, eq=dn)

            deleted = ldap_runtime_client.delete_entry(dn)
            tm.ok(deleted)
            created = False

            absent = ldap_runtime_client.search_entry(
                base_dn=ldap_base_dn,
                search_filter=f"(uid={identifier})",
                attributes=("cn",),
            )
            tm.ok(absent)
            tm.that(absent.value, empty=True)
        finally:
            if created:
                tm.ok(ldap_runtime_client.delete_entry(dn))
