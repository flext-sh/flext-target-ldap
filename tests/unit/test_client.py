"""Observable behavior of the public target-ldap client contract.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
tests/unit/test_client
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_target_ldap import settings
from tests import p, t, tm


class TestsFlextTargetLdapClient:
    """Behavior contract for the public client factory."""

    @staticmethod
    def test_client_reflects_production_settings(
        ldap_client: p.TargetLdap.Client,
    ) -> None:
        """Test client reflects production settings."""
        configured = settings.TargetLdap
        tm.that(ldap_client.host, eq=configured.host)
        tm.that(ldap_client.port, eq=configured.port)
        tm.that(ldap_client.bind_dn, eq=configured.bind_dn)
        tm.that(ldap_client.password, eq=configured.bind_password)
        tm.that(ldap_client.use_ssl, eq=configured.use_ssl)
        tm.that(ldap_client.timeout, eq=configured.timeout)

    @staticmethod
    def test_server_uri_reflects_production_settings(
        ldap_client: p.TargetLdap.Client,
    ) -> None:
        """Test server uri reflects production settings."""
        configured = settings.TargetLdap
        scheme = "ldaps" if configured.use_ssl else "ldap"
        tm.that(
            ldap_client.server_uri,
            eq=f"{scheme}://{configured.host}:{configured.port}",
        )

    @staticmethod
    @pytest.mark.docker
    @pytest.mark.integration
    def test_connect_and_disconnect_reach_configured_runtime(
        ldap_runtime_client: p.TargetLdap.Client,
    ) -> None:
        """Test connect and disconnect reach configured runtime."""
        connected = ldap_runtime_client.connect()
        tm.ok(connected)
        tm.that(connected.value, eq=True)

        disconnected = ldap_runtime_client.disconnect()
        tm.ok(disconnected)
        tm.that(disconnected.value, eq=True)

    @staticmethod
    @pytest.mark.docker
    @pytest.mark.integration
    def test_entry_lifecycle_is_observable_in_configured_runtime(
        ldap_runtime_client: p.TargetLdap.Client,
        ldap_base_dn: str,
    ) -> None:
        """Test entry lifecycle is observable in configured runtime."""
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

            changes: t.Ldap.OperationAttributes = {"mail": f"{identifier}@flext.local"}
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
