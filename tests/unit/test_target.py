"""Tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from flext_core import r
from flext_target_ldap import (
    FlextTargetLdap,
    FlextTargetLdapBaseSink,
    FlextTargetLdapGroupsSink,
    FlextTargetLdapSink,
    FlextTargetLdapUsersSink,
)
from tests import t, u


@pytest.mark.parametrize(
    ("key", "expected_cls"),
    [
        ("users", FlextTargetLdapUsersSink),
        ("groups", FlextTargetLdapGroupsSink),
        ("custom_stream", FlextTargetLdapBaseSink),
    ],
)
def test_get_sink_class(
    key: str,
    expected_cls: type[FlextTargetLdapBaseSink],
    mock_ldap_config: t.ContainerValueMapping,
) -> None:
    target = FlextTargetLdap(settings=mock_ldap_config)
    assert target.get_sink_class(key) is expected_cls


def test_target_initialization(mock_ldap_config: t.ContainerValueMapping) -> None:
    target = FlextTargetLdap(settings=mock_ldap_config)
    assert target.name == "target-ldap"
    assert target.settings == mock_ldap_config


def test_dn_template_processing(
    mock_ldap_config: t.MutableContainerValueMapping,
) -> None:
    mock_ldap_config["user_rdn_attribute"] = "uid"
    mock_ldap_config["base_dn"] = "ou=people,dc=test,dc=com"
    target = FlextTargetLdap(settings=mock_ldap_config)
    sink = target.get_sink("users")
    assert isinstance(sink, FlextTargetLdapUsersSink)
    dn_result = sink.build_dn({"uid": "jdoe"})
    assert dn_result.success
    assert dn_result.value == "uid=jdoe,ou=people,dc=test,dc=com"


def test_object_classes_processing(
    mock_ldap_config: t.MutableContainerValueMapping,
) -> None:
    mock_ldap_config["users_object_classes"] = ["customPerson", "top"]
    target = FlextTargetLdap(settings=mock_ldap_config)
    sink = target.get_sink("users")
    assert isinstance(sink, FlextTargetLdapUsersSink)
    object_classes = sink.get_object_classes({})
    assert object_classes == ["customPerson", "top"]


def test_process_record(
    mock_ldap_config: t.ContainerValueMapping,
    sample_user_record: t.ContainerValueMapping,
) -> None:
    mock_client = MagicMock()
    mock_client.add_entry.return_value = r[bool].ok(value=True)
    target = FlextTargetLdap(settings=mock_ldap_config)
    sink = target.get_sink("users")
    assert isinstance(sink, FlextTargetLdapBaseSink)
    sink.client = mock_client
    result = sink.process_record(sample_user_record, {})
    assert result.success
    mock_client.add_entry.assert_called_once()


def test_process_delete_record(mock_ldap_config: t.ContainerValueMapping) -> None:
    mock_client = MagicMock()
    mock_client.add_entry.return_value = r[bool].fail("Entry already exists")
    target = FlextTargetLdap(settings=mock_ldap_config)
    sink = target.get_sink("users")
    assert isinstance(sink, FlextTargetLdapBaseSink)
    sink.client = mock_client
    record = {
        "dn": "uid=jdoe,ou=users,dc=test,dc=com",
        "_sdc_deleted_at": "2024-01-15T10:30:00Z",
    }
    result = sink.process_record(record, {})
    assert result.failure
    assert result.error and "No username found" in result.error


def test_sink_process_record_delegates_to_target_handler() -> None:
    target = u.TargetLdap.Tests.ProcessTarget()
    sink = FlextTargetLdapSink(
        target=target,
        stream_name="users",
        schema={"type": "t.NormalizedValue"},
        key_properties=["id"],
    )
    result = sink.process_record({"id": "42"}, {"batch": "1"})
    assert result.success
    assert target.calls == [({"id": "42"}, {"batch": "1"})]
