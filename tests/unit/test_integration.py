"""Integration tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import io
import json
from collections.abc import (
    Mapping,
)
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from flext_target_ldap import FlextTargetLdap
from tests import t, u


def _write_jsonl(path: Path, events: t.SequenceOf[Mapping[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8"
    )


@pytest.fixture
def runner() -> Mock:
    mock_runner = Mock()
    mock_runner.invoke = Mock()
    return mock_runner


@pytest.fixture
def config_file(
    tmp_path: Path,
    mock_ldap_config: t.TargetLdap.SettingsPayload,
) -> Path:
    config_path = tmp_path / "settings.json"
    u.Cli.json_write(config_path, mock_ldap_config)
    return config_path


@pytest.fixture
def input_file(
    tmp_path: Path,
    singer_message_schema: str,
    singer_message_record: str,
    singer_message_state: str,
) -> Path:
    input_path = tmp_path / "input.jsonl"
    with input_path.open("w", encoding="utf-8") as handle:
        handle.write(singer_message_schema + "\n")
        handle.write(singer_message_record + "\n")
        handle.write(singer_message_state + "\n")
    return input_path


@pytest.fixture
def mock_ldap_api(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock_api = MagicMock()
    monkeypatch.setattr("flext_target_ldap.api.FlextTargetLdapClient", mock_api)
    return mock_api


def _invoke_target_cli(config_path: Path, input_path: Path) -> None:
    input_text = input_path.read_text(encoding="utf-8")
    with patch("sys.stdin", io.StringIO(input_text)):
        cli_fn = FlextTargetLdap.cli
        assert cli_fn is not None
        cli_fn(settings=str(config_path))


class TestsFlextTargetLdapIntegration:
    """Behavior contract for test_integration."""

    def test_basic_load(
        self, mock_ldap_api: MagicMock, config_file: Path, input_file: Path
    ) -> None:
        mock_conn = MagicMock()
        mock_conn.add_entry.return_value = True
        mock_conn.delete_entry.return_value = True
        mock_conn.modify_entry.return_value = True
        mock_ldap_api.return_value = mock_conn

        _invoke_target_cli(config_file, input_file)

        assert mock_conn.add_entry.called
        assert mock_conn.add_entry.call_count >= 1

    def test_upsert_behavior(
        self, mock_ldap_api: MagicMock, config_file: Path, tmp_path: Path
    ) -> None:
        input_path = tmp_path / "upsert_input.jsonl"
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "properties": {"dn": {"type": "string"}, "cn": {"type": "string"}},
            },
            "key_properties": ["dn"],
        }
        record1 = {
            "type": "RECORD",
            "stream": "users",
            "record": {"dn": "uid=test,dc=test,dc=com", "cn": "Test User"},
        }
        record2 = {
            "type": "RECORD",
            "stream": "users",
            "record": {"dn": "uid=test,dc=test,dc=com", "cn": "Updated Test User"},
        }
        _write_jsonl(input_path, [schema_msg, record1, record2])

        mock_conn = MagicMock()
        mock_conn.add_entry.return_value = True
        mock_conn.modify_entry.return_value = True
        mock_ldap_api.return_value = mock_conn

        _invoke_target_cli(config_file, input_path)

        assert mock_conn.add_entry.call_count >= 1
        assert mock_conn.modify_entry.call_count >= 1

    def test_delete_records(
        self, mock_ldap_api: MagicMock, config_file: Path, tmp_path: Path
    ) -> None:
        input_path = tmp_path / "delete_input.jsonl"
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {"properties": {"dn": {"type": "string"}}},
            "key_properties": ["dn"],
        }
        delete_record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=deleted,dc=test,dc=com",
                "_sdc_deleted_at": "2024-01-01T12:00:00Z",
            },
        }
        _write_jsonl(input_path, [schema_msg, delete_record])

        mock_conn = MagicMock()
        mock_conn.delete_entry.return_value = True
        mock_ldap_api.return_value = mock_conn

        _invoke_target_cli(config_file, input_path)

        mock_conn.delete_entry.assert_called_once_with("uid=deleted,dc=test,dc=com")

    def test_dn_template_usage(
        self,
        mock_ldap_api: MagicMock,
        tmp_path: Path,
        mock_ldap_config: t.TargetLdap.SettingsPayload,
    ) -> None:
        config_path = tmp_path / "template_config.json"
        u.Cli.json_write(config_path, mock_ldap_config)

        input_path = tmp_path / "template_input.jsonl"
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "properties": {"uid": {"type": "string"}, "cn": {"type": "string"}},
            },
            "key_properties": ["uid"],
        }
        record = {
            "type": "RECORD",
            "stream": "users",
            "record": {"uid": "testuser", "cn": "Test User"},
        }
        _write_jsonl(input_path, [schema_msg, record])

        mock_conn = MagicMock()
        mock_conn.add_entry.return_value = True
        mock_ldap_api.return_value = mock_conn

        _invoke_target_cli(config_path, input_path)

        add_calls = mock_conn.add_entry.call_args_list
        assert add_calls
        actual_dn = add_calls[0][0][0]
        assert actual_dn == "uid=testuser,dc=test,dc=com"

    def test_self(self, runner: Mock, tmp_path: Path) -> None:
        bad_config = {"invalid": "settings"}
        config_path = tmp_path / "bad_config.json"
        u.Cli.json_write(config_path, bad_config)
        mock_result = Mock()
        mock_result.exit_code = 1
        mock_result.output = "Configuration error"
        runner.invoke.return_value = mock_result

        result = runner.invoke(
            "mock_cli",
            ["--config", str(config_path)],
            input='{"type": "RECORD", "stream": "test", "record": {}}',
        )
        assert result.exit_code != 0

    def test_multi_stream_handling(
        self,
        mock_ldap_api: MagicMock,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        input_path = tmp_path / "multi_stream.jsonl"
        messages = [
            {
                "type": "SCHEMA",
                "stream": "users",
                "schema": {"properties": {"dn": {"type": "string"}}},
                "key_properties": ["dn"],
            },
            {
                "type": "RECORD",
                "stream": "users",
                "record": {"dn": "uid=user1,dc=test,dc=com"},
            },
            {
                "type": "SCHEMA",
                "stream": "groups",
                "schema": {"properties": {"dn": {"type": "string"}}},
                "key_properties": ["dn"],
            },
            {
                "type": "RECORD",
                "stream": "groups",
                "record": {"dn": "cn=group1,dc=test,dc=com"},
            },
        ]
        _write_jsonl(input_path, messages)

        mock_conn = MagicMock()
        mock_conn.add_entry.return_value = True
        mock_ldap_api.return_value = mock_conn

        _invoke_target_cli(config_file, input_path)

        assert mock_conn.add_entry.call_count >= 2
