"""Tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from flext_target_ldap import (
    LdapBaseSink,
    LdapGroupsSink,
    LdapUsersSink,
    TargetLdap,
    t,
)
from flext_target_ldap.sinks import Sink, Target
from flext_target_ldap.target import _default_cli_helper


class TestTargetLDAPUnit:
    """Unit tests for TargetLDAP."""

    @pytest.fixture
    def config(self) -> dict[str, t.GeneralValueType]:
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

    def test_target_initialization(self, config: dict[str, t.GeneralValueType]) -> None:
        """Test target LDAP initialization with name and config."""
        target = TargetLdap(config=config)
        if target.name != "target-ldap":
            msg: str = f"Expected {'target-ldap'}, got {target.name}"
            raise AssertionError(msg)
        assert target.config == config

    def test_get_sink_class_users(self, config: dict[str, t.GeneralValueType]) -> None:
        """Test getting users sink class."""
        target = TargetLdap(config=config)
        sink_class = target.get_sink_class("users")

        # Create a sink instance with mock data

        if sink_class != LdapUsersSink:
            msg: str = f"Expected {LdapUsersSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_get_sink_class_groups(self, config: dict[str, t.GeneralValueType]) -> None:
        """Test getting groups sink class."""
        target = TargetLdap(config=config)
        sink_class = target.get_sink_class("groups")

        # Create a sink instance with mock data

        if sink_class != LdapGroupsSink:
            msg: str = f"Expected {LdapGroupsSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_get_sink_class_generic(
        self,
        config: dict[str, t.GeneralValueType],
    ) -> None:
        """Test getting generic sink class for unknown stream."""
        target = TargetLdap(config=config)
        sink_class = target.get_sink_class("custom_stream")

        # Should return the default sink class

        if sink_class != LdapBaseSink:
            msg: str = f"Expected {LdapBaseSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_dn_template_processing(
        self,
        config: dict[str, t.GeneralValueType],
    ) -> None:
        """Test DN template configuration processing."""
        config["dn_templates"] = {"users": "uid={uid},ou=people,dc=test,dc=com"}

        target = TargetLdap(config=config)
        target.get_sink("users")

        assert (
            target.config["users_dn_template"] == "uid={uid},ou=people,dc=test,dc=com"
        )

    def test_object_classes_processing(
        self,
        config: dict[str, t.GeneralValueType],
    ) -> None:
        """Test default object classes configuration processing."""
        config["default_object_classes"] = {"users": ["customPerson", "top"]}

        target = TargetLdap(config=config)
        target.get_sink("users")

        if target.config["users_object_classes"] != ["customPerson", "top"]:
            msg: str = f"Expected {['customPerson', 'top']}, got {target.config['users_object_classes']}"
            raise AssertionError(msg)

    @patch("target_ldap.sinks.LDAPClient")
    def test_process_record(
        self,
        mock_client_class: MagicMock,
        config: dict[str, t.GeneralValueType],
    ) -> None:
        """Test processing a record through the LDAP target."""
        # Mock LDAP client
        mock_client = MagicMock()
        mock_client.upsert_entry.return_value = (True, "add")
        mock_client_class.return_value = mock_client

        target = TargetLdap(config=config)
        sink = target.get_sink("users")

        record = {
            "dn": "uid=jdoe,ou=users,dc=test,dc=com",
            "uid": "jdoe",
            "cn": "John Doe",
            "mail": "jdoe@test.com",
            "objectClass": ["inetOrgPerson", "person"],
        }

        sink.process_record(record, {})

        # Verify upsert was called
        mock_client.upsert_entry.assert_called_once()
        call_args = mock_client.upsert_entry.call_args
        if call_args[0][0] != "uid=jdoe,ou=users,dc=test,dc=com":
            msg = (
                f"Expected {'uid=jdoe,ou=users,dc=test,dc=com'}, got {call_args[0][0]}"
            )
            raise AssertionError(msg)
        if "inetOrgPerson" not in call_args[0][1]:
            msg: str = f"Expected {'inetOrgPerson'} in {call_args[0][1]}"
            raise AssertionError(msg)

    @patch("target_ldap.sinks.LDAPClient")
    def test_process_delete_record(
        self,
        mock_client_class: MagicMock,
        config: dict[str, t.GeneralValueType],
    ) -> None:
        """Test processing a delete record through the LDAP target."""
        # Mock LDAP client
        mock_client = MagicMock()
        mock_client.entry_exists.return_value = True
        mock_client.delete_entry.return_value = True
        mock_client_class.return_value = mock_client

        target = TargetLdap(config=config)
        sink = target.get_sink("users")

        record = {
            "dn": "uid=jdoe,ou=users,dc=test,dc=com",
            "_sdc_deleted_at": "2024-01-15T10:30:00Z",
        }

        sink.process_record(record, {})

        # Verify delete was called
        mock_client.entry_exists.assert_called_once_with(
            "uid=jdoe,ou=users,dc=test,dc=com",
        )
        mock_client.delete_entry.assert_called_once_with(
            "uid=jdoe,ou=users,dc=test,dc=com",
        )


def test_default_cli_helper_logs_with_flext_logger() -> None:
    mock_logger = MagicMock()
    with patch("flext_target_ldap.target.FlextLogger", return_value=mock_logger):
        helper = _default_cli_helper(quiet=False)
        helper.print("state-line")

    mock_logger.info.assert_called_once_with("%s", "state-line")


def test_sink_process_record_delegates_to_target_handler() -> None:
    class _ProcessTarget(Target):
        def __init__(self) -> None:
            super().__init__({"base_dn": "dc=test,dc=com"})
            self.calls: list[tuple[dict[str, str], dict[str, str]]] = []

        def process_record(
            self,
            record: dict[str, str],
            context: dict[str, str],
        ) -> bool:
            self.calls.append((record, context))
            return True

    target = _ProcessTarget()
    sink = Sink(
        target=target,
        stream_name="users",
        schema={"type": "object"},
        key_properties=["id"],
    )

    result = sink.process_record({"id": "42"}, {"batch": "1"})

    assert result.is_success
    assert target.calls == [({"id": "42"}, {"batch": "1"})]
