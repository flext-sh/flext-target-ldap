"""Pytest configuration and fixtures for target-ldap tests."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import pytest

from flext_target_ldap.client import LDAPClient


@pytest.fixture
def mock_ldap_config() -> dict[str, Any]:
    return {
        "host": "test.ldap.com",
        "port": 389,
        "bind_dn": "cn=admin,dc=test,dc=com",
        "password": "test_password",
        "base_dn": "dc=test,dc=com",
        "use_ssl": False,
        "timeout": 30,
        "validate_records": True,
        "user_rdn_attribute": "uid",
        "group_rdn_attribute": "cn",
        "dn_templates": {
            "users": "uid={uid},ou=users,dc=test,dc=com",
            "groups": "cn={cn},ou=groups,dc=test,dc=com",
        },
        "default_object_classes": {
            "users": ["inetOrgPerson", "person", "top"],
            "groups": ["groupOfNames", "top"],
        },
    }


@pytest.fixture
def sample_user_record() -> dict[str, Any]:
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
def sample_group_record() -> dict[str, Any]:
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
def sample_ou_record() -> dict[str, Any]:
        return {
        "dn": "ou=engineering,dc=test,dc=com",
        "ou": "engineering",
        "description": "Engineering department",
        "objectClass": ["organizationalUnit", "top"],
    }


@pytest.fixture
def singer_message_record(sample_user_record: dict[str, Any]) -> str:
    message = {
        "type": "RECORD",
        "stream": "users",
        "record": sample_user_record,
        "time_extracted": "2024-01-01T12:00:00Z",
    }
    return json.dumps(message)


@pytest.fixture
def singer_message_schema() -> str:
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
def mock_ldap_client() -> MagicMock:
    client = MagicMock(spec=LDAPClient)
    client.validate_dn.return_value = True
    client.entry_exists.return_value = False
    client.add_entry.return_value = True
    client.modify_entry.return_value = True
    client.delete_entry.return_value = True
    client.upsert_entry.return_value = (True, "add")
    return client


@pytest.fixture
def mock_target(mock_ldap_config: dict[str, Any]) -> MagicMock:
    target = MagicMock()
    target.config = mock_ldap_config
    return target
