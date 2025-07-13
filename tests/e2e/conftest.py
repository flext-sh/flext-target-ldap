"""E2E test configuration and fixtures for target-ldap."""

from __future__ import annotations

import json
import logging
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import ldap3
import pytest
from ldap3 import ALL, Connection, Server

import docker

if TYPE_CHECKING:
    from collections.abc import Generator
    from unittest.mock import Mock

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def docker_client() -> docker.DockerClient:
        return docker.from_env()


@pytest.fixture(scope="session")
def e2e_dir() -> Path:
        return Path(__file__).parent


@pytest.fixture(scope="session")
def project_root() -> Path:
        return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def ldap_containers(
    docker_client:
        docker.DockerClient,
    project_root: Path,
) -> Generator[Any]:
        compose_file = project_root / "docker-compose.yml"

    # Start containers
    logger.info("Starting OpenLDAP containers...")
    subprocess.run(
        ["docker-compose", "-f", str(compose_file), "up", "-d"],
        check=True,
        cwd=str(project_root),
    )

    # Wait for both LDAP servers to be ready
    for name, port, bind_dn, password in [:
        ("source", 20389, "cn=REDACTED_LDAP_BIND_PASSWORD,dc=source,dc=com", "source_password"),
        ("target", 21389, "cn=REDACTED_LDAP_BIND_PASSWORD,dc=target,dc=com", "target_password"),
    ]:
            max_retries = 30
        for i in range(max_retries):
            try:
            server = Server("localhost", port=port, get_info=ALL)
                conn = Connection(
                    server,
                    user=bind_dn,
                    password=password,
                    auto_bind=True,
                )
                conn.unbind()
                logger.info("OpenLDAP %s is ready", name)
                break
            except Exception:
            if i == max_retries - 1:
            raise
                logger.info(
                    "Waiting for OpenLDAP %s... (%d/%d)",
                    name,
                    i + 1,
                    max_retries,
                )
                time.sleep(2)

    yield

    # Stop containers
    logger.info("Stopping OpenLDAP containers...")
    subprocess.run(
        ["docker-compose", "-f", str(compose_file), "down", "-v"],
        check=True,
        cwd=str(project_root),
    )


@pytest.fixture
def source_connection(ldap_containers:
            Mock) -> Generator[Connection]:
        server = Server("localhost", port=20389, get_info=ALL)
    conn = Connection(
        server,
        user="cn=REDACTED_LDAP_BIND_PASSWORD,dc=source,dc=com",
        password="source_password",
        auto_bind=True,
        raise_exceptions=True,
    )

    yield conn

    if conn.bound:
            conn.unbind()


@pytest.fixture
def target_connection(ldap_containers:
        Mock) -> Generator[Connection]:
        server = Server("localhost", port=21389, get_info=ALL)
    conn = Connection(
        server,
        user="cn=REDACTED_LDAP_BIND_PASSWORD,dc=target,dc=com",
        password="target_password",
        auto_bind=True,
        raise_exceptions=True,
    )

    yield conn

    if conn.bound:
            conn.unbind()


@pytest.fixture
def target_config(tmp_path:
        Path) -> dict[str, Any]:
        return {
        "host": "localhost",
        "port": 21389,
        "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=target,dc=com",
        "password": "target_password",
        "base_dn": "dc=target,dc=com",
        "use_ssl": False,
        "validate_records": True,
        "dn_templates": {
            "users": "uid={uid},ou=migrated,{base_dn}",
            "groups": "cn={cn},ou=groups,{base_dn}",
        },
        "default_object_classes": {
            "users": ["inetOrgPerson", "organizationalPerson", "person", "top"],
            "groups": ["groupOfNames", "top"],
        },
    }


@pytest.fixture
def target_config_file(target_config:
        dict[str, Any], tmp_path: Path) -> Path:
        config_file = tmp_path / "target-config.json"
    config_file.write_text(json.dumps(target_config))
    return config_file


@pytest.fixture
def sample_user_records() -> list[dict[str, Any]]:
        return [
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=john.doe,ou=people,dc=source,dc=com",
                "uid": "john.doe",
                "cn": "John Doe",
                "sn": "Doe",
                "givenName": "John",
                "mail": "john.doe@source.com",
                "employeeNumber": "1001",
                "employeeType": "active",
                "departmentNumber": "engineering",
                "userPassword": "{SSHA}x+wnyY9qS7TCSSdg1CtNyJr8FtNFh2RF",
            },
            "time_extracted": "2024-01-01T12:00:00Z",
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=jane.smith,ou=people,dc=source,dc=com",
                "uid": "jane.smith",
                "cn": "Jane Smith",
                "sn": "Smith",
                "givenName": "Jane",
                "mail": "jane.smith@source.com",
                "employeeNumber": "1002",
                "employeeType": "active",
                "departmentNumber": "sales",
                "userPassword": "{SSHA}y+wnyY9qS7TCSSdg1CtNyJr8FtNFh2RF",
            },
            "time_extracted": "2024-01-01T12:00:01Z",
        },
    ]


@pytest.fixture
def sample_group_records() -> list[dict[str, Any]]:
        return [
        {
            "type": "RECORD",
            "stream": "groups",
            "record": {
                "dn": "cn=engineering,ou=groups,dc=source,dc=com",
                "cn": "engineering",
                "description": "Engineering Team",
                "member": [
                    "uid=john.doe,ou=people,dc=source,dc=com",
                ],
            },
            "time_extracted": "2024-01-01T12:00:02Z",
        },
        {
            "type": "RECORD",
            "stream": "groups",
            "record": {
                "dn": "cn=sales,ou=groups,dc=source,dc=com",
                "cn": "sales",
                "description": "Sales Team",
                "member": [
                    "uid=jane.smith,ou=people,dc=source,dc=com",
                ],
            },
            "time_extracted": "2024-01-01T12:00:03Z",
        },
    ]


def verify_user_loaded(
    conn:
        Connection,
    uid: str,
    base_dn: str = "dc=target,dc=com",
) -> bool:
        conn.search(
        search_base=base_dn,
        search_filter=f"(uid={uid})",
        search_scope=ldap3.SUBTREE,
        attributes=["*"],
    )
    return len(conn.entries) > 0


def verify_group_loaded(
    conn:
        Connection,
    cn: str,
    base_dn: str = "dc=target,dc=com",
) -> bool:
        conn.search(
        search_base=base_dn,
        search_filter=f"(cn={cn})",
        search_scope=ldap3.SUBTREE,
        attributes=["*"],
    )
    return len(conn.entries) > 0


def get_user_attributes(
    conn:
        Connection,
    uid: str,
    base_dn: str = "dc=target,dc=com",
) -> dict[str, Any]:
        conn.search(
        search_base=base_dn,
        search_filter=f"(uid={uid})",
        search_scope=ldap3.SUBTREE,
        attributes=["*"],
    )
    if conn.entries:
            entry = conn.entries[0]
        return {str(attr.key): attr.values for attr in entry}
    return {}


def count_entries(
    conn:
            Connection,
    search_filter: str,
    base_dn: str = "dc=target,dc=com",
) -> int:
        conn.search(
        search_base=base_dn,
        search_filter=search_filter,
        search_scope=ldap3.SUBTREE,
        attributes=["dn"],
    )
    return len(conn.entries)
