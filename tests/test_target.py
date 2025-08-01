"""Tests for target-ldap."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from flext_target_ldap.sinks import GroupsSink, LDAPBaseSink, UsersSink
from flext_target_ldap.target import TargetLDAP

# Alias for backward compatibility
GenericSink = LDAPBaseSink

# Note: get_target_test_class is not available - would need to implement basic target tests manually


class TestTargetLDAPUnit:
    """Unit tests for TargetLDAP."""

    @pytest.fixture
    def config(self) -> dict[str, object]:
        return {
            "host": "test.ldap.com",
            "port": 389,
            "base_dn": "dc=test,dc=com",
            "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
            "password": "test_password",
            "use_ssl": False,
            "timeout": 30,
        }

    def test_target_initialization(self, config: dict[str, object]) -> None:
        target = TargetLDAP(config=config)
        if target.name != "target-ldap":
            msg = f"Expected {'target-ldap'}, got {target.name}"
            raise AssertionError(msg)
        assert target.config == config

    def test_get_sink_users(self, config: dict[str, object]) -> None:
        target = TargetLDAP(config=config)
        sink_class = target.get_sink_class("users")

        # Create a sink instance with mock data

        if sink_class != UsersSink:
            msg = f"Expected {UsersSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_get_sink_groups(self, config: dict[str, object]) -> None:
        target = TargetLDAP(config=config)
        sink_class = target.get_sink_class("groups")

        # Create a sink instance with mock data

        if sink_class != GroupsSink:
            msg = f"Expected {GroupsSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_get_sink_generic(self, config: dict[str, object]) -> None:
        target = TargetLDAP(config=config)
        sink_class = target.get_sink_class("custom_stream")

        # Should return the default sink class

        if sink_class != GenericSink:
            msg = f"Expected {GenericSink}, got {sink_class}"
            raise AssertionError(msg)

    def test_dn_template_configuration(self, config: dict[str, object]) -> None:
        config["dn_templates"] = {"users": "uid={uid},ou=people,dc=test,dc=com"}

        target = TargetLDAP(config=config)
        target.get_sink("users")

        assert (
            target.config["users_dn_template"] == "uid={uid},ou=people,dc=test,dc=com"
        )

    def test_object_class_configuration(self, config: dict[str, object]) -> None:
        config["default_object_classes"] = {"users": ["customPerson", "top"]}

        target = TargetLDAP(config=config)
        target.get_sink("users")

        if target.config["users_object_classes"] != ["customPerson", "top"]:
            msg = f"Expected {['customPerson', 'top']}, got {target.config['users_object_classes']}"
            raise AssertionError(msg)

    @patch("target_ldap.sinks.LDAPClient")
    def test_process_record(
        self,
        mock_client_class: MagicMock,
        config: dict[str, object],
    ) -> None:
        # Mock LDAP client
        mock_client = MagicMock()
        mock_client.upsert_entry.return_value = (True, "add")
        mock_client_class.return_value = mock_client

        target = TargetLDAP(config=config)
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
            msg = f"Expected {'inetOrgPerson'} in {call_args[0][1]}"
            raise AssertionError(msg)

    @patch("target_ldap.sinks.LDAPClient")
    def test_process_delete_record(
        self,
        mock_client_class: MagicMock,
        config: dict[str, object],
    ) -> None:
        # Mock LDAP client
        mock_client = MagicMock()
        mock_client.entry_exists.return_value = True
        mock_client.delete_entry.return_value = True
        mock_client_class.return_value = mock_client

        target = TargetLDAP(config=config)
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
