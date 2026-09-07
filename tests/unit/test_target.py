"""Observable behavior of the public target-ldap facade."""

from __future__ import annotations

from collections.abc import Mapping

from flext_target_ldap import FlextTargetLdap
from flext_tests import tm
from tests import t


class TestsFlextTargetLdapTarget:
    """Behavior contract for the public target facade."""

    def test_target_uses_injected_settings(
        self, ldap_settings_payload: t.TargetLdap.SettingsPayload
    ) -> None:
        target = FlextTargetLdap(settings=ldap_settings_payload)
        tm.that(target.settings, eq=ldap_settings_payload)
        target.validate_config()

    def test_catalog_streams_resolve_through_public_sink_factory(
        self, ldap_settings_payload: t.TargetLdap.SettingsPayload
    ) -> None:
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

    def test_deleted_record_without_identity_fails_observably(
        self, ldap_settings_payload: t.TargetLdap.SettingsPayload
    ) -> None:
        target = FlextTargetLdap(settings=ldap_settings_payload)
        sink = target.get_sink("users")
        record: t.TargetLdap.RecordPayload = {"_sdc_deleted_at": True}
        result = sink.process_record(record, {})
        tm.fail(result)
        tm.that(result.error, has="No username found")
