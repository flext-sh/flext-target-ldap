"""Observable behavior of the public target-ldap facade.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
tests/unit/test_target
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_tests import tm

from flext_target_ldap import FlextTargetLdap
from tests import t


class TestsFlextTargetLdapTarget:
    """Behavior contract for the public target facade."""

    @staticmethod
    def test_target_uses_injected_settings(
        ldap_settings_payload: t.TargetLdap.SettingsPayload,
    ) -> None:
        """Test target uses injected settings."""
        target = FlextTargetLdap(settings=ldap_settings_payload)
        tm.that(target.settings, eq=ldap_settings_payload)
        target.validate_config()

    @staticmethod
    def test_catalog_streams_resolve_through_public_sink_factory(
        ldap_settings_payload: t.TargetLdap.SettingsPayload,
    ) -> None:
        """Test catalog streams resolve through public sink factory.

        Raises:
            TypeError: If Singer catalog must expose a streams list; or if Singer
                catalog stream must be a mapping; or if Singer catalog stream must
                expose tap_stream_id.
        """
        target = FlextTargetLdap(settings=ldap_settings_payload)
        streams = target.singer_catalog.get("streams")
        if not isinstance(streams, list):
            msg = "Singer catalog must expose a streams list"
            raise TypeError(msg)
        for stream in streams:
            if not isinstance(stream, Mapping):
                msg = "Singer catalog stream must be a mapping"
                raise TypeError(msg)
            stream_name = stream.get("tap_stream_id")
            if not isinstance(stream_name, str) or not stream_name:
                msg = "Singer catalog stream must expose tap_stream_id"
                raise TypeError(msg)
            sink = target.get_sink(stream_name)
            tm.that(sink.stream_name, eq=stream_name)

    @staticmethod
    def test_deleted_record_without_identity_fails_observably(
        ldap_settings_payload: t.TargetLdap.SettingsPayload,
    ) -> None:
        """Test deleted record without identity fails observably."""
        target = FlextTargetLdap(settings=ldap_settings_payload)
        sink = target.get_sink("users")
        record: t.TargetLdap.RecordPayload = {"_sdc_deleted_at": True}
        result = sink.process_record(record, {})
        tm.fail(result)
        tm.that(result.error, has="No username found")
