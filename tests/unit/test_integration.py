"""End-to-end behavior through the public target-ldap facade."""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_target_ldap import FlextTargetLdap
from flext_tests import tm
from tests import p, t


class TestsFlextTargetLdapIntegration:
    """Observable target-to-LDAP persistence contract."""

    @pytest.mark.integration
    def test_public_target_persists_user_record(
        self,
        target_ldap: FlextTargetLdap,
        ldap_runtime_client: p.TargetLdap.Client,
        ldap_base_dn: str,
    ) -> None:
        identifier = f"flext-target-ldap-{uuid4().hex}"
        dn = f"uid={identifier},{ldap_base_dn}"
        record: t.TargetLdap.RecordPayload = {
            "username": identifier,
            "full_name": identifier,
            "last_name": identifier,
        }
        sink = target_ldap.get_sink("users")
        created = False
        setup = sink.setup_client()
        tm.ok(setup)
        try:
            persisted = sink.process_record(record, {})
            tm.ok(persisted)
            created = True

            found = ldap_runtime_client.search_entry(
                base_dn=ldap_base_dn,
                search_filter=f"(uid={identifier})",
                attributes=("cn", "sn"),
            )
            tm.ok(found)
            tm.that(len(found.value), eq=1)
            entry_dn = tm.not_none(found.value[0].dn)
            tm.that(entry_dn.value, eq=dn)
        finally:
            sink.teardown_client()
            if created:
                tm.ok(ldap_runtime_client.delete_entry(dn))
