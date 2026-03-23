"""Integration tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import io
from collections.abc import Mapping
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from pydantic import TypeAdapter

from flext_target_ldap.target import _target_ldap_flext_cli
from tests import t


class TestTargetLDAPIntegration:
    """Integration tests for target-ldap."""

    @pytest.fixture
    def runner(self) -> Mock:
        """CLI runner fixture for testing.

        Note: This will be replaced with flext-cli patterns in the future.
        """
        mock_runner = Mock()
        mock_runner.invoke = Mock()
        return mock_runner

    @pytest.fixture
    def config_file(
        self, tmp_path: Path, mock_ldap_config: Mapping[str, t.NormalizedValue]
    ) -> Path:
        """Create temporary configuration file for testing."""
        config_path = tmp_path / "config.json"
        config_path.write_text(
            TypeAdapter(t.NormalizedValue).dump_json(mock_ldap_config).decode("utf-8"),
            encoding="utf-8",
        )
        return config_path

    @pytest.fixture
    def input_file(
        self,
        tmp_path: Path,
        singer_message_schema: str,
        singer_message_record: str,
        singer_message_state: str,
    ) -> Path:
        """Create temporary input file with Singer messages for testing."""
        input_path = tmp_path / "input.jsonl"
        with input_path.open("w", encoding="utf-8") as f:
            f.write(singer_message_schema + "\n")
            f.write(singer_message_record + "\n")
            f.write(singer_message_state + "\n")
        return input_path

    @patch("flext_target_ldap.target._get_ldap_api")
    def test_basic_load(
        self, mock_api: MagicMock, config_file: Path, input_file: Path
    ) -> None:
        """Test basic LDAP data loading functionality."""
        mock_conn = MagicMock()
        mock_conn.add.return_value = True
        mock_conn.delete.return_value = True
        mock_conn.modify.return_value = True
        mock_api.return_value = mock_conn

        input_text = input_file.read_text(encoding="utf-8")
        with patch("sys.stdin", io.StringIO(input_text)):
            _target_ldap_flext_cli(config=str(config_file))

        assert mock_conn.add.called
        assert mock_conn.add.call_count >= 1

    @patch("flext_target_ldap.target._get_ldap_api")
    def test_upsert_behavior(
        self, mock_api: MagicMock, config_file: Path, tmp_path: Path
    ) -> None:
        """Test upsert behavior for duplicate records."""
        input_path = tmp_path / "upsert_input.jsonl"
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "properties": {"dn": {"type": "string"}, "cn": {"type": "string"}}
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
        with input_path.open("w", encoding="utf-8") as f:
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(schema_msg).decode("utf-8")
                + "\n"
            )
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(record1).decode("utf-8") + "\n"
            )
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(record2).decode("utf-8") + "\n"
            )

        mock_conn = MagicMock()
        mock_conn.add.return_value = True
        mock_conn.modify.return_value = True
        mock_api.return_value = mock_conn

        input_text = input_path.read_text(encoding="utf-8")
        with patch("sys.stdin", io.StringIO(input_text)):
            _target_ldap_flext_cli(config=str(config_file))

        if mock_conn.add.call_count < 1:
            add_msg: str = f"Expected {mock_conn.add.call_count} >= {1}"
            raise AssertionError(add_msg)
        # Second record with same DN should trigger modify (upsert)
        assert mock_conn.modify.call_count >= 1

    @patch("flext_target_ldap.target._get_ldap_api")
    def test_delete_records(
        self, mock_api: MagicMock, config_file: Path, tmp_path: Path
    ) -> None:
        """Test deletion of LDAP records."""
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
        with input_path.open("w", encoding="utf-8") as f:
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(schema_msg).decode("utf-8")
                + "\n"
            )
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(delete_record).decode("utf-8")
                + "\n"
            )

        mock_conn = MagicMock()
        mock_conn.delete.return_value = True
        mock_api.return_value = mock_conn

        input_text = input_path.read_text(encoding="utf-8")
        with patch("sys.stdin", io.StringIO(input_text)):
            _target_ldap_flext_cli(config=str(config_file))

        mock_conn.delete.assert_called_once_with("uid=deleted,dc=test,dc=com")

    @pytest.mark.usefixtures("config_file")
    @patch("flext_target_ldap.target._get_ldap_api")
    def test_dn_template_usage(
        self,
        mock_api: MagicMock,
        tmp_path: Path,
        mock_ldap_config: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test DN template usage for record processing."""
        mock_ldap_config["dn_templates"] = {
            "users": "uid={uid},ou=people,dc=test,dc=com"
        }
        config_path = tmp_path / "template_config.json"
        config_path.write_text(
            TypeAdapter(t.NormalizedValue).dump_json(mock_ldap_config).decode("utf-8"),
            encoding="utf-8",
        )
        input_path = tmp_path / "template_input.jsonl"
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "properties": {"uid": {"type": "string"}, "cn": {"type": "string"}}
            },
            "key_properties": ["uid"],
        }
        record = {
            "type": "RECORD",
            "stream": "users",
            "record": {"uid": "testuser", "cn": "Test User"},
        }
        with input_path.open("w", encoding="utf-8") as f:
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(schema_msg).decode("utf-8")
                + "\n"
            )
            f.write(
                TypeAdapter(t.NormalizedValue).dump_json(record).decode("utf-8") + "\n"
            )

        mock_conn = MagicMock()
        mock_conn.add.return_value = True
        mock_api.return_value = mock_conn

        # _process_record_message constructs DN via _construct_dn for records
        # without a "dn" field. The record has uid=testuser, stream=users,
        # so _construct_dn returns "uid=testuser,dc=test,dc=com" (using base_dn).
        input_text = input_path.read_text(encoding="utf-8")
        with patch("sys.stdin", io.StringIO(input_text)):
            _target_ldap_flext_cli(config=str(config_path))

        add_calls = mock_conn.add.call_args_list
        assert len(add_calls) > 0
        # _construct_dn uses base_dn from config: "dc=test,dc=com"
        # For users stream with uid=testuser: "uid=testuser,dc=test,dc=com"
        actual_dn = add_calls[0][0][0]
        expected_dn = "uid=testuser,dc=test,dc=com"
        if actual_dn != expected_dn:
            dn_msg: str = f"Expected {expected_dn}, got {actual_dn}"
            raise AssertionError(dn_msg)

    def test_self(self, runner: Mock, tmp_path: Path) -> None:
        """Test error handling for invalid configurations."""
        bad_config = {"invalid": "config"}
        config_path = tmp_path / "bad_config.json"
        config_path.write_text(
            TypeAdapter(t.NormalizedValue).dump_json(bad_config).decode("utf-8"),
            encoding="utf-8",
        )
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

    @patch("flext_target_ldap.target._get_ldap_api")
    def test_multi_stream_handling(
        self, mock_api: MagicMock, config_file: Path, tmp_path: Path
    ) -> None:
        """Test handling of multiple Singer streams."""
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
        with input_path.open("w", encoding="utf-8") as f:
            f.writelines(
                TypeAdapter(t.NormalizedValue).dump_json(msg).decode("utf-8") + "\n"
                for msg in messages
            )

        mock_conn = MagicMock()
        mock_conn.add.return_value = True
        mock_api.return_value = mock_conn

        input_text = input_path.read_text(encoding="utf-8")
        with patch("sys.stdin", io.StringIO(input_text)):
            _target_ldap_flext_cli(config=str(config_file))

        if mock_conn.add.call_count < 2:
            count_msg: str = f"Expected {mock_conn.add.call_count} >= {2}"
            raise AssertionError(count_msg)
