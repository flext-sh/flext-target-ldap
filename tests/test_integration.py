"""Integration tests for target-ldap."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from flext_target_ldap.target import TargetLDAP

if TYPE_CHECKING:
    from pathlib import Path
    from unittest.mock import Mock


class TestTargetLDAPIntegration:
    """Integration tests for target-ldap."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    @pytest.fixture
    def config_file(self, tmp_path: Path, mock_ldap_config: dict[str, object]) -> Path:
        config_path = tmp_path / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(mock_ldap_config, f)
        return config_path

    @pytest.fixture
    def input_file(
        self,
        tmp_path: Path,
        singer_message_schema: str,
        singer_message_record: str,
        singer_message_state: str,
    ) -> Path:
        input_path = tmp_path / "input.jsonl"
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(singer_message_schema + "\n")
            f.write(singer_message_record + "\n")
            f.write(singer_message_state + "\n")
        return input_path

    @patch("flext_target_ldap.client.get_ldap_api")
    def test_basic_load(
        self,
        mock_ldap_api: Mock,
        runner: CliRunner,
        config_file: Path,
        input_file: Path,
    ) -> None:
        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True
        mock_conn_instance.search.return_value = True
        mock_conn_instance.entries = []  # No existing entries
        mock_conn_instance.add.return_value = True
        # Mock LDAP API is already configured

        # Run target
        with open(input_file, encoding="utf-8") as f:
            result = runner.invoke(
                TargetLDAP.cli,
                ["--config", str(config_file)],
                input=f.read(),
                catch_exceptions=False,
            )

        if result.exit_code != 0:
            msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(msg)

        # Verify add was called
        assert mock_conn_instance.add.called

        # Check output contains state message
        if "STATE" not in result.output:
            msg: str = f"Expected {'STATE'} in {result.output}"
            raise AssertionError(msg)

    @patch("flext_target_ldap.client.get_ldap_api")
    def test_upsert_behavior(
        self,
        mock_ldap_api: Mock,
        runner: CliRunner,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        # Create input with duplicate records
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

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(schema_msg) + "\n")
            f.write(json.dumps(record1) + "\n")
            f.write(json.dumps(record2) + "\n")

        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True

        # First call: entry doesn't exist
        # Second call: entry exists
        mock_conn_instance.search.side_effect = [True, True]
        mock_conn_instance.entries = []
        mock_conn_instance.add.return_value = True
        mock_conn_instance.modify.return_value = True

        def search_side_effect(*args: Any, **kwargs: Any) -> bool:
            # First search: no entry
            # Second search: entry exists
            if mock_conn_instance.search.call_count <= 1:
                mock_conn_instance.entries = []
            else:
                mock_conn_instance.entries = [MagicMock()]
            return True

        mock_conn_instance.search.side_effect = search_side_effect
        # Mock LDAP API is already configured

        # Run target
        with open(input_path, encoding="utf-8") as f:
            result = runner.invoke(
                TargetLDAP.cli,
                ["--config", str(config_file)],
                input=f.read(),
                catch_exceptions=False,
            )

        if result.exit_code != 0:
            msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(msg)

        # Should have one add and one modify
        if mock_conn_instance.add.call_count < 1:
            msg: str = f"Expected {mock_conn_instance.add.call_count} >= {1}"
            raise AssertionError(msg)
        assert mock_conn_instance.modify.call_count >= 1

    @patch("flext_target_ldap.client.get_ldap_api")
    def test_delete_records(
        self,
        mock_ldap_api: Mock,
        runner: CliRunner,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        # Create input with deletion record
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

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(schema_msg) + "\n")
            f.write(json.dumps(delete_record) + "\n")

        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True
        mock_conn_instance.search.return_value = True
        mock_conn_instance.entries = [MagicMock()]  # Entry exists
        mock_conn_instance.delete.return_value = True
        # Mock LDAP API is already configured

        # Run target
        with open(input_path, encoding="utf-8") as f:
            result = runner.invoke(
                TargetLDAP.cli,
                ["--config", str(config_file)],
                input=f.read(),
                catch_exceptions=False,
            )

        if result.exit_code != 0:
            msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(msg)

        # Verify delete was called
        mock_conn_instance.delete.assert_called_once_with("uid=deleted,dc=test,dc=com")

    @patch("flext_target_ldap.client.get_ldap_api")
    def test_dn_template_usage(
        self,
        mock_ldap_api: Mock,
        runner: CliRunner,
        config_file: Path,
        tmp_path: Path,
        mock_ldap_config: dict[str, object],
    ) -> None:
        # Add DN template to config
        mock_ldap_config["dn_templates"] = {
            "users": "uid={uid},ou=people,dc=test,dc=com",
        }

        config_path = tmp_path / "template_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(mock_ldap_config, f)

        # Create input without DN
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

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(schema_msg) + "\n")
            f.write(json.dumps(record) + "\n")

        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True
        mock_conn_instance.search.return_value = True
        mock_conn_instance.entries = []
        mock_conn_instance.add.return_value = True
        # Mock LDAP API is already configured

        # Run target
        with open(input_path, encoding="utf-8") as f:
            result = runner.invoke(
                TargetLDAP.cli,
                ["--config", str(config_path)],
                input=f.read(),
                catch_exceptions=False,
            )

        if result.exit_code != 0:
            msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(msg)

        # Verify DN was constructed from template
        add_calls = mock_conn_instance.add.call_args_list
        assert len(add_calls) > 0
        if add_calls[0][0][0] != "uid=testuser,ou=people,dc=test,dc=com":
            msg: str = f"Expected {'uid=testuser,ou=people,dc=test,dc=com'}, got {add_calls[0][0][0]}"
            raise AssertionError(msg)

    def test_error_handling(self, runner: CliRunner, tmp_path: Path) -> None:
        # Invalid config
        bad_config = {"invalid": "config"}
        config_path = tmp_path / "bad_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(bad_config, f)

        result = runner.invoke(
            TargetLDAP.cli,
            ["--config", str(config_path)],
            input='{"type": "RECORD", "stream": "test", "record": {}}',
        )

        assert result.exit_code != 0

    @patch("flext_target_ldap.client.get_ldap_api")
    def test_multi_stream_handling(
        self,
        mock_ldap_api: Mock,
        runner: CliRunner,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        # Create input with multiple streams
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

        with open(input_path, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(msg) + "\n" for msg in messages)

        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True
        mock_conn_instance.search.return_value = True
        mock_conn_instance.entries = []
        mock_conn_instance.add.return_value = True
        # Mock LDAP API is already configured

        # Run target
        with open(input_path, encoding="utf-8") as f:
            result = runner.invoke(
                TargetLDAP.cli,
                ["--config", str(config_file)],
                input=f.read(),
                catch_exceptions=False,
            )

        if result.exit_code != 0:
            msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(msg)

        # Verify both streams were processed
        if mock_conn_instance.add.call_count < 2:
            msg: str = f"Expected {mock_conn_instance.add.call_count} >= {2}"
            raise AssertionError(msg)
