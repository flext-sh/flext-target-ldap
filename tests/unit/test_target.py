"""Tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pydantic import BaseModel

from flext_target_ldap import FlextTargetLdap
from flext_target_ldap._models.sinks import (
    FlextTargetLdapBaseSink,
    FlextTargetLdapGroupsSink,
    FlextTargetLdapSink,
    FlextTargetLdapUsersSink,
)
from flext_tests import tm
from tests import u
from tests.base import s
from tests.settings import TestsFlextTargetLdapSettings as TargetLdapTestSettings

if TYPE_CHECKING:
    from tests import t


class TestsFlextTargetLdapTarget:
    """Behavior contract for test_target."""

    @pytest.mark.parametrize(
        ("key", "expected_cls"),
        [
            ("users", FlextTargetLdapUsersSink),
            ("groups", FlextTargetLdapGroupsSink),
            ("custom_stream", FlextTargetLdapBaseSink),
        ],
    )
    def test_get_sink_class(
        self,
        key: str,
        expected_cls: type[FlextTargetLdapBaseSink],
        mock_ldap_config: t.TargetLdap.SettingsPayload,
    ) -> None:
        target = FlextTargetLdap(settings=mock_ldap_config)
        assert target.get_sink_class(key) is expected_cls

    def test_target_initialization(
        self, mock_ldap_config: t.TargetLdap.SettingsPayload
    ) -> None:
        target = FlextTargetLdap(settings=mock_ldap_config)
        tm.that(target.name, eq="target-ldap")
        tm.that(target.settings, eq=mock_ldap_config)

    def test_test_service_settings_include_tests_namespace(self) -> None:
        settings = s.fetch_settings()
        assert isinstance(settings, TargetLdapTestSettings)

        tm.that(settings.Tests, is_=BaseModel)
        tm.that(settings, is_=TargetLdapTestSettings)
        assert settings.base_dn

    def test_dn_template_processing(
        self, mock_ldap_config: t.TargetLdap.SettingsPayload
    ) -> None:
        updated_settings: t.TargetLdap.SettingsPayload = {
            **mock_ldap_config,
            "user_rdn_attribute": "uid",
            "base_dn": "ou=people,dc=test,dc=com",
        }
        target = FlextTargetLdap(settings=updated_settings)
        sink = target.get_sink("users")
        tm.that(sink, is_=FlextTargetLdapUsersSink)
        assert isinstance(sink, FlextTargetLdapUsersSink)
        dn_result = sink.build_dn({"uid": "jdoe"})
        tm.ok(dn_result)
        tm.that(dn_result.value, eq="uid=jdoe,ou=people,dc=test,dc=com")

    def test_object_classes_processing(
        self, mock_ldap_config: t.TargetLdap.SettingsPayload
    ) -> None:
        updated_settings: t.TargetLdap.SettingsPayload = {
            **mock_ldap_config,
            "users_object_classes": ["customPerson", "top"],
        }
        target = FlextTargetLdap(settings=updated_settings)
        sink = target.get_sink("users")
        tm.that(sink, is_=FlextTargetLdapUsersSink)
        assert isinstance(sink, FlextTargetLdapUsersSink)
        object_classes = sink.resolve_object_classes({})
        tm.that(object_classes, eq=["customPerson", "top"])

    @pytest.mark.integration
    def test_process_record(
        self,
        real_target_config: t.TargetLdap.SettingsPayload,
        real_base_dn: str,
    ) -> None:
        singer_record: t.TargetLdap.RecordPayload = {
            "username": "processrec",
            "full_name": "Process Record",
            "last_name": "Record",
        }
        target = FlextTargetLdap(settings=real_target_config)
        sink = target.get_sink("users")
        tm.that(sink, is_=FlextTargetLdapBaseSink)
        assert isinstance(sink, FlextTargetLdapBaseSink)
        setup_result = sink.setup_client()
        tm.ok(setup_result)
        try:
            client = sink.client
            assert client is not None
            dn = f"uid=processrec,{real_base_dn}"
            client.delete_entry(dn)
            result = sink.process_record(singer_record, {})
            tm.ok(result)
            client.delete_entry(dn)
        finally:
            sink.teardown_client()

    def test_process_delete_record(
        self, mock_ldap_config: t.TargetLdap.SettingsPayload
    ) -> None:
        target = FlextTargetLdap(settings=mock_ldap_config)
        sink = target.get_sink("users")
        tm.that(sink, is_=FlextTargetLdapBaseSink)
        assert isinstance(sink, FlextTargetLdapBaseSink)
        record: t.TargetLdap.RecordPayload = {
            "dn": "uid=jdoe,ou=users,dc=test,dc=com",
            "_sdc_deleted_at": "2024-01-15T10:30:00Z",
        }
        result = sink.process_record(record, {})
        tm.fail(result)
        assert result.error
        assert "No username found" in result.error

    def test_sink_process_record_delegates_to_target_handler(self) -> None:
        target = u.TargetLdap.Tests.ProcessTarget()
        sink = FlextTargetLdapSink(
            target=target,
            stream_name="users",
            schema={"type": "object"},
            key_properties=["id"],
        )
        result = sink.process_record({"id": "42"}, {"batch": "1"})
        tm.ok(result)
        tm.that(target.calls, eq=[({"id": "42"}, {"batch": "1"})])
