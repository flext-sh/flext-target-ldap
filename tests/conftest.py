"""Pytest configuration and fixtures for target-ldap tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import pathlib
from unittest.mock import MagicMock

import pytest
from flext_core import FlextSettings
from flext_tests import tk

from flext_target_ldap import (
    FlextTargetLdapSettings,
)
from tests import t, u


@pytest.fixture(autouse=True)
def reset_settings_singleton() -> None:
    """Reset FlextSettings singleton between tests."""
    FlextSettings.reset_for_testing()


@pytest.fixture
def target_ldap_settings() -> FlextTargetLdapSettings:
    """Provide clean FlextTargetLdapSettings for target-ldap tests."""
    return FlextTargetLdapSettings(debug=True)


@pytest.fixture(scope="session")
def shared_ldap_container(flext_docker: tk) -> str:
    """Managed LDAP container using centralized tk with docker-compose."""
    compose_file = pathlib.Path(
        "~/flext/docker/docker-compose.openldap.yml",
    ).expanduser()
    start_result = flext_docker.start_compose_stack(str(compose_file))
    if start_result.failure:
        pytest.skip(f"OpenLDAP container failed to start: {start_result.error}")
    return "flext-openldap-test"


@pytest.fixture
def mock_ldap_config() -> t.TargetLdap.SettingsPayload:
    """Create mock LDAP configuration for testing."""
    return u.TargetLdap.Tests.build_mock_ldap_config(
        bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
    )


@pytest.fixture
def sample_user_record() -> t.TargetLdap.RecordPayload:
    """Create mock LDAP configuration for testing."""
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
def sample_group_record() -> t.TargetLdap.RecordPayload:
    """Create mock LDAP configuration for testing."""
    return {
        "dn": "cn=developers,ou=groups,dc=test,dc=com",
        "cn": "developers",
        "description": "Development team",
        "member": [
            "uid=jdoe,ou=users,dc=test,dc=com",
            "uid=asmith,ou=users,dc=test,dc=com",
        ],
        "objectClass": ["groupOfNames", "top"],
    }


@pytest.fixture
def sample_ou_record() -> t.TargetLdap.RecordPayload:
    """Create mock LDAP configuration for testing."""
    return {
        "dn": "ou=engineering,dc=test,dc=com",
        "ou": "engineering",
        "description": "Engineering department",
        "objectClass": ["organizationalUnit", "top"],
    }


@pytest.fixture
def singer_message_record(sample_user_record: t.TargetLdap.RecordPayload) -> str:
    """Create mock LDAP configuration for testing."""
    message = {
        "type": "RECORD",
        "stream": "users",
        "record": sample_user_record,
        "time_extracted": "2024-01-01T12:00:00Z",
    }
    return json.dumps(message)


@pytest.fixture
def singer_message_schema() -> str:
    """Create mock LDAP configuration for testing."""
    message = {
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
    return json.dumps(message)


@pytest.fixture
def singer_message_state() -> str:
    """Create mock LDAP configuration for testing."""
    message = {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "users": {
                    "replication_key": "modifyTimestamp",
                    "replication_key_value": "20240101120000Z",
                },
            },
        },
    }
    return json.dumps(message)


@pytest.fixture
def mock_target(mock_ldap_config: t.TargetLdap.SettingsPayload) -> MagicMock:
    """Create mock LDAP configuration for testing."""
    target = MagicMock()
    target.settings = dict(mock_ldap_config)
    return target
