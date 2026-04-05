"""Tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from flext_core import r
from flext_target_ldap import (
    FlextTargetLdap,
    FlextTargetLdapBaseSink as LdapBaseSink,
    FlextTargetLdapGroupsSink as LdapGroupsSink,
    FlextTargetLdapSink as Sink,
    FlextTargetLdapUsersSink as LdapUsersSink,
)
from tests import t, u


class TestTargetLDAPUnit:
    """Unit tests for TargetLDAP."""

    @pytest.fixture
    def config(self) -> t.MutableContainerValueMapping:
        """Create test configuration for LDAP target."""
        return {
            "host": "test.ldap.com",
            "port": 389,
            "base_dn": "dc=test,dc=com",
            "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
            "password": "test_password",
            "use_ssl": False,
            "timeout": 30,
        }

    def test_target_initialization(
        self,
        config: t.ContainerValueMapping,
    ) -> None:
        """Test target LDAP initialization with name and config."""
        target = FlextTargetLdap(config=config)
        if target.name != "target-ldap":
            msg: str = f"Expected {'target-ldap'}, got {target.name}"
            raise AssertionError(msg)
        assert target.config == config

    def test_get_sink_class_users(self, config: t.ContainerValueMapping) -> None:
        """Test getting users sink class."""
        target = FlextTargetLdap(config=config)
        sink_class = target.get_sink_class("users")
        if sink_class != LdapUsersSink:
            msg: str = f"Expected {LdapUsersSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_get_sink_class_groups(
        self,
        config: t.ContainerValueMapping,
    ) -> None:
        """Test getting groups sink class."""
        target = FlextTargetLdap(config=config)
        sink_class = target.get_sink_class("groups")
        if sink_class != LdapGroupsSink:
            msg: str = f"Expected {LdapGroupsSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_get_sink_class_generic(
        self,
        config: t.ContainerValueMapping,
    ) -> None:
        """Test getting generic sink class for unknown stream."""
        target = FlextTargetLdap(config=config)
        sink_class = target.get_sink_class("custom_stream")
        if sink_class != LdapBaseSink:
            msg: str = f"Expected {LdapBaseSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_dn_template_processing(
        self,
        config: t.MutableContainerValueMapping,
    ) -> None:
        """Test DN template configuration via user_rdn_attribute."""
        config["user_rdn_attribute"] = "uid"
        config["base_dn"] = "ou=people,dc=test,dc=com"
        target = FlextTargetLdap(config=config)
        sink = target.get_sink("users")
        assert isinstance(sink, LdapUsersSink)
        dn_result = sink.build_dn({"uid": "jdoe"})
        assert dn_result.is_success
        assert dn_result.value == "uid=jdoe,ou=people,dc=test,dc=com"

    def test_object_classes_processing(
        self,
        config: t.MutableContainerValueMapping,
    ) -> None:
        """Test object classes configuration read by UsersSink."""
        config["users_object_classes"] = ["customPerson", "top"]
        target = FlextTargetLdap(config=config)
        sink = target.get_sink("users")
        assert isinstance(sink, LdapUsersSink)
        object_classes = sink.get_object_classes({})
        assert object_classes == ["customPerson", "top"]

    def test_process_record(self, config: t.ContainerValueMapping) -> None:
        """Test processing a record through the LDAP target."""
        mock_client = MagicMock()
        mock_client.add_entry.return_value = r[bool].ok(value=True)
        target = FlextTargetLdap(config=config)
        sink = target.get_sink("users")
        assert isinstance(sink, LdapBaseSink)
        sink.client = mock_client
        record: t.ContainerValueMapping = {
            "dn": "uid=jdoe,ou=users,dc=test,dc=com",
            "uid": "jdoe",
            "cn": "John Doe",
            "mail": "jdoe@test.com",
            "objectClass": ["inetOrgPerson", "person"],
        }
        result = sink.process_record(record, {})
        assert result.is_success
        mock_client.add_entry.assert_called_once()
        call_args = mock_client.add_entry.call_args
        dn_arg = call_args[0][0]
        if dn_arg != "uid=jdoe,dc=test,dc=com":
            msg = f"Expected 'uid=jdoe,dc=test,dc=com', got {dn_arg}"
            raise AssertionError(msg)

    def test_process_delete_record(
        self,
        config: t.ContainerValueMapping,
    ) -> None:
        """Test processing a delete record through the LDAP target.

        Note: UsersSink.process_record performs add/modify operations.
        Delete records without a username are rejected with an error.
        """
        mock_client = MagicMock()
        mock_client.add_entry.return_value = r[bool].fail("Entry already exists")
        target = FlextTargetLdap(config=config)
        sink = target.get_sink("users")
        assert isinstance(sink, LdapBaseSink)
        sink.client = mock_client
        record: t.ContainerValueMapping = {
            "dn": "uid=jdoe,ou=users,dc=test,dc=com",
            "_sdc_deleted_at": "2024-01-15T10:30:00Z",
        }
        result = sink.process_record(record, {})
        assert result.is_failure
        assert result.error is not None
        assert "No username found" in result.error


def test_default_cli_helper_logs_with_flext_logger() -> None:
    mock_logger = MagicMock()
    helper = FlextTargetLdap._create_cli_helper(quiet=False)
    with patch.object(helper, "_logger", mock_logger):
        helper.print("state-line")
    mock_logger.info.assert_called_once_with("state-line")


def test_sink_process_record_delegates_to_target_handler() -> None:
    target = u.TargetLdap.Tests.ProcessTarget()
    sink = Sink(
        target=target,
        stream_name="users",
        schema={"type": "t.NormalizedValue"},
        key_properties=["id"],
    )
    result = sink.process_record({"id": "42"}, {"batch": "1"})
    assert result.is_success
    assert target.calls == [({"id": "42"}, {"batch": "1"})]
