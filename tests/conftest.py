"""Pytest configuration and fixtures for target-ldap tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from flext_cli import u as cli_u
from flext_ldap import u as ldap_u
from flext_target_ldap._models.sinks import FlextTargetLdapTarget
from flext_tests import reset_settings as _shared_reset_settings, tk
from tests import u

_LDAP_CONTAINER_NAME = "flext-openldap-test"
_LDAP_ADMIN_DN = "cn=admin,dc=flext,dc=local"
_LDAP_ADMIN_PASSWORD = "admin123"
_LDAP_BASE_DN = "dc=flext,dc=local"
_LDAP_HOST = "localhost"
_LDAP_PORT = 3390
_LDAP_BIND_READY_TIMEOUT = 60.0

if TYPE_CHECKING:
    from tests import t

reset_settings = _shared_reset_settings


@pytest.fixture(scope="session")
def ldap_container() -> t.TargetLdap.SettingsPayload:
    """Start the shared OpenLDAP container and return a real connection config.

    Skips (never fakes) when the shared compose is unavailable or the server
    does not become bind-ready, honoring the no-mock law: either the real
    container serves the test or the test is skipped.
    """
    docker = tk.shared(
        _LDAP_CONTAINER_NAME,
        workspace_root=Path(__file__).resolve().parents[2],
    )
    execute_result = docker.execute()
    if execute_result.failure:
        pytest.skip(
            f"OpenLDAP container {_LDAP_CONTAINER_NAME} unavailable: "
            f"{execute_result.error}",
        )
    waited: float = 0.0
    while waited < _LDAP_BIND_READY_TIMEOUT:
        server = ldap_u.Ldap.create_server_from_url(
            f"ldap://{_LDAP_HOST}:{_LDAP_PORT}",
        )
        connection = ldap_u.Ldap.create_connection(
            server,
            user=_LDAP_ADMIN_DN,
            password=_LDAP_ADMIN_PASSWORD,
            auto_bind=True,
            receive_timeout=1,
        )
        if connection.bound:
            connection.unbind()
            break
        time.sleep(1.0)
        waited += 1.0
    else:
        pytest.skip(
            f"OpenLDAP container {_LDAP_CONTAINER_NAME} did not become "
            f"bind-ready within {_LDAP_BIND_READY_TIMEOUT}s",
        )
    return {
        "connection": {
            "host": _LDAP_HOST,
            "port": _LDAP_PORT,
            "bind_dn": _LDAP_ADMIN_DN,
            "bind_password": _LDAP_ADMIN_PASSWORD,
            "use_ssl": False,
            "timeout": 30,
        },
        "base_dn": _LDAP_BASE_DN,
        "object_classes": ["inetOrgPerson", "person", "top"],
    }


@pytest.fixture
def real_connection_config(
    ldap_container: t.TargetLdap.SettingsPayload,
) -> t.TargetLdap.SettingsPayload:
    """Flat client connection payload bound to the real container (bind_password)."""
    _ = ldap_container
    return {
        "host": _LDAP_HOST,
        "port": _LDAP_PORT,
        "bind_dn": _LDAP_ADMIN_DN,
        "bind_password": _LDAP_ADMIN_PASSWORD,
        "use_ssl": False,
        "timeout": 30,
        "base_dn": _LDAP_BASE_DN,
    }


@pytest.fixture
def real_target_config(
    ldap_container: t.TargetLdap.SettingsPayload,
) -> t.TargetLdap.SettingsPayload:
    """Flat target/sink payload bound to the real container (password key)."""
    _ = ldap_container
    return {
        "host": _LDAP_HOST,
        "port": _LDAP_PORT,
        "bind_dn": _LDAP_ADMIN_DN,
        "password": _LDAP_ADMIN_PASSWORD,
        "use_ssl": False,
        "timeout": 30,
        "base_dn": _LDAP_BASE_DN,
    }


@pytest.fixture
def real_base_dn() -> str:
    """The real container base DN as a plain string."""
    return _LDAP_BASE_DN


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
def ldap_target(
    mock_ldap_config: t.TargetLdap.SettingsPayload,
    ) -> FlextTargetLdapTarget:
    """Return a real target instance carrying the test connection settings."""
    return FlextTargetLdapTarget(dict(mock_ldap_config))
