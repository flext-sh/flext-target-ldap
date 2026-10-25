"""End-to-end persistence through the public target-ldap stream sink.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
tests/unit/test_integration
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from flext_target_ldap.services import FlextTargetLdapSinks
from tests import p, t, tm, u


class TestsFlextTargetLdapIntegration:
    """Observable target-to-LDAP persistence contract."""

    @staticmethod
    @pytest.mark.docker
    @pytest.mark.integration
    def test_users_record_is_added_modified_and_deleted(
        ldap_runtime_settings_payload: t.TargetLdap.SettingsPayload,
        ldap_runtime_client: p.TargetLdap.Client,
        ldap_base_dn: str,
    ) -> None:
        """Test a user record is added, modified on repeat, then deleted."""
        profile = u.TargetLdap.entry_profile("users")
        identifier = f"flext-target-ldap-{uuid4().hex}"
        dn = f"{profile.rdn_attribute}={identifier},{ldap_base_dn}"
        record: t.TargetLdap.RecordPayload = dict.fromkeys(
            profile.field_mapping, identifier
        )
        sink = FlextTargetLdapSinks.runtime_sink(
            stream_name="users",
            schema={},
            target_config=ldap_runtime_settings_payload,
            directory=ldap_runtime_client,
        )
        created = False
        try:
            tm.ok(sink.process_record(record, {}))
            created = True
            tm.ok(sink.process_record(record, {}))

            found = ldap_runtime_client.search_entry(
                base_dn=ldap_base_dn,
                search_filter=f"({profile.rdn_attribute}={identifier})",
                attributes=(profile.rdn_attribute,),
            )
            tm.that(len(tm.ok(found)), eq=1)
            tm.that(found.value[0].dn_str, eq=dn)

            tm.ok(sink.process_record({**record, "_sdc_deleted_at": True}, {}))
            created = False
            absent = ldap_runtime_client.search_entry(
                base_dn=ldap_base_dn,
                search_filter=f"({profile.rdn_attribute}={identifier})",
                attributes=(profile.rdn_attribute,),
            )
            tm.that(tm.ok(absent), empty=True)
        finally:
            if created:
                tm.ok(ldap_runtime_client.delete_entry(dn))
