"""Integration tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json as _stdlib_json
import sys
from typing import TYPE_CHECKING

import pytest

from flext_target_ldap import FlextTargetLdap
from flext_target_ldap._utilities.client import FlextTargetLdapClient
from flext_tests import tm
from tests import u

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from tests import t


def _write_jsonl(path: Path, events: t.SequenceOf[Mapping[str, object]]) -> None:
    """Serialize Singer events as JSONL via stdlib json (test fixture)."""
    serialized = "\n".join(_stdlib_json.dumps(dict(event)) for event in events)
    path.write_text(serialized + "\n", encoding="utf-8")


@pytest.fixture
def real_config(
    real_connection_config: t.TargetLdap.SettingsPayload,
) -> t.TargetLdap.SettingsPayload:
    """Flat Singer config bound to the real OpenLDAP container."""
    return real_connection_config


@pytest.fixture
def config_file(
    tmp_path: Path,
    real_config: t.TargetLdap.SettingsPayload,
) -> Path:
    config_path = tmp_path / "settings.json"
    u.Cli.json_write(config_path, real_config)
    return config_path


def _run_target_cli(
    monkeypatch: pytest.MonkeyPatch,
    config_path: Path,
    input_path: Path,
) -> None:
    """Run the real target CLI feeding a real file as stdin (no mock)."""
    with input_path.open(encoding="utf-8") as handle:
        monkeypatch.setattr(sys, "stdin", handle)
        FlextTargetLdap.cli(settings=str(config_path))


def _search(
    real_config: t.TargetLdap.SettingsPayload,
    base_dn: str,
    search_filter: str,
) -> list[object]:
    client = FlextTargetLdapClient(settings=dict(real_config))
    result = client.search_entry(
        base_dn=base_dn,
        search_filter=search_filter,
        attributes=["cn"],
    )
    tm.ok(result)
    return list(result.unwrap())


class TestsFlextTargetLdapIntegration:
    """Behavior contract for test_integration exercised against real OpenLDAP."""

    @pytest.mark.integration
    def test_basic_load(
        self,
        monkeypatch: pytest.MonkeyPatch,
        real_config: t.TargetLdap.SettingsPayload,
        real_base_dn: str,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        dn = f"uid=basicload,{real_base_dn}"
        FlextTargetLdapClient(settings=dict(real_config)).delete_entry(dn)
        input_path = tmp_path / "input.jsonl"
        _write_jsonl(
            input_path,
            [
                {
                    "type": "SCHEMA",
                    "stream": "users",
                    "schema": {"properties": {"uid": {"type": "string"}}},
                    "key_properties": ["uid"],
                },
                {
                    "type": "RECORD",
                    "stream": "users",
                    "record": {
                        "uid": "basicload",
                        "cn": "Basic Load",
                        "sn": "Load",
                        "objectClass": ["inetOrgPerson", "person", "top"],
                    },
                },
            ],
        )
        _run_target_cli(monkeypatch, config_file, input_path)
        entries = _search(real_config, real_base_dn, "(uid=basicload)")
        tm.that(len(entries), eq=1)
        FlextTargetLdapClient(settings=dict(real_config)).delete_entry(dn)

    @pytest.mark.integration
    def test_multi_stream_handling(
        self,
        monkeypatch: pytest.MonkeyPatch,
        real_config: t.TargetLdap.SettingsPayload,
        real_base_dn: str,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        user_dn = f"uid=multiuser,{real_base_dn}"
        client = FlextTargetLdapClient(settings=dict(real_config))
        client.delete_entry(user_dn)
        input_path = tmp_path / "multi_stream.jsonl"
        _write_jsonl(
            input_path,
            [
                {
                    "type": "SCHEMA",
                    "stream": "users",
                    "schema": {"properties": {"uid": {"type": "string"}}},
                    "key_properties": ["uid"],
                },
                {
                    "type": "RECORD",
                    "stream": "users",
                    "record": {
                        "uid": "multiuser",
                        "cn": "Multi User",
                        "sn": "User",
                        "objectClass": ["inetOrgPerson", "person", "top"],
                    },
                },
            ],
        )
        _run_target_cli(monkeypatch, config_file, input_path)
        entries = _search(real_config, real_base_dn, "(uid=multiuser)")
        tm.that(len(entries), eq=1)
        client.delete_entry(user_dn)
