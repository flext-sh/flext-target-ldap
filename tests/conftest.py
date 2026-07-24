"""Pytest configuration and fixtures for target-ldap tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from flext_tests import reset_settings as _shared_reset_settings

from flext_cli import u as cli_u
from tests import t, u

reset_settings = _shared_reset_settings


@pytest.fixture
def mock_ldap_config() -> t.TargetLdap.SettingsPayload:
    """Create mock LDAP configuration for testing."""
    return u.TargetLdap.Tests.build_mock_ldap_config(
        bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com"
    )


@pytest.fixture
def sample_user_record() -> t.TargetLdap.RecordPayload:
    """Sample LDAP user record for testing."""
    return {
        "dn": "uid=jdoe,ou=users,dc=test,dc=com",
        "uid": "jdoe",
        "cn": "John Doe",
        "sn": "Doe",
        "givenName": "John",
        "mail": "jdoe@test.com",
        "objectClass": ["inetOrgPerson", "person", "top"],
    }


@pytest.fixture
def singer_message_record(sample_user_record: t.TargetLdap.RecordPayload) -> str:
    """Singer RECORD message for testing."""
    message: dict[str, t.JsonValue] = {
        "type": "RECORD",
        "stream": "users",
        "record": dict(sample_user_record),
        "time_extracted": "2024-01-01T12:00:00Z",
    }
    rendered: str = cli_u.Cli.json_dumps(message).unwrap()
    return rendered


@pytest.fixture
def singer_message_schema() -> str:
    """Singer SCHEMA message for testing."""
    message: dict[str, t.JsonValue] = {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "type": "object",
            "properties": {
                "dn": {"type": "string"},
                "uid": {"type": "string"},
                "cn": {"type": "string"},
                "mail": {"type": ["string", "null"]},
                "objectClass": {"type": "array", "items": {"type": "string"}},
            },
        },
        "key_properties": ["dn"],
    }
    rendered: str = cli_u.Cli.json_dumps(message).unwrap()
    return rendered


@pytest.fixture
def singer_message_state() -> str:
    """Singer STATE message for testing."""
    message: dict[str, t.JsonValue] = {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "users": {
                    "replication_key": "modifyTimestamp",
                    "replication_key_value": "20240101120000Z",
                }
            }
        },
    }
    rendered: str = cli_u.Cli.json_dumps(message).unwrap()
    return rendered


@pytest.fixture
def mock_target(mock_ldap_config: t.TargetLdap.SettingsPayload) -> MagicMock:
    """Mock target instance for testing."""
    target = MagicMock()
    target.settings = dict(mock_ldap_config)
    return target
