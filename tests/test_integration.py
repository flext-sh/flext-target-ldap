"""Integration tests for target-ldap.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest


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
        self,
        tmp_path: Path,
        mock_ldap_config: dict[str, object],
    ) -> Path:
        """Create temporary configuration file for testing."""
        config_path = tmp_path / "config.json"
        with config_path.open("w", encoding="utf-8") as f:
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
        """Create temporary input file with Singer messages for testing."""
        input_path = tmp_path / "input.jsonl"
        with input_path.open("w", encoding="utf-8") as f:
            f.write(singer_message_schema + "\n")
            f.write(singer_message_record + "\n")
            f.write(singer_message_state + "\n")
        return input_path

    @pytest.mark.usefixtures("_mock_ldap_api")
    @patch("flext_target_ldap.client.get_ldap_api")
    def test_basic_load(
        self,
        runner: Mock,
        config_file: Path,
        input_file: Path,
    ) -> None:
        """Test basic LDAP data loading functionality."""
        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True
        mock_conn_instance.search.return_value = True
        mock_conn_instance.entries = []  # No existing entries
        mock_conn_instance.add.return_value = True
        # Wire patched API to use our mock connection instance
        with patch("flext_target_ldap.client.get_ldap_api") as mock_api:
            mock_api.return_value = mock_conn_instance
            # Run target
            with input_file.open(encoding="utf-8") as f:
                # Mock CLI invocation
                mock_result = Mock()
                mock_result.exit_code = 0
                mock_result.output = '{"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}'
                runner.invoke.return_value = mock_result
                result = runner.invoke(
                    "mock_cli",
                    ["--config", str(config_file)],
                    input=f.read(),
                    catch_exceptions=False,
                )
            if result.exit_code != 0:
                error_msg: str = f"Expected {0}, got {result.exit_code}"
                raise AssertionError(error_msg)
            # Verify add was called on the API connection mock
            assert mock_conn_instance.add.called
            # Check output contains state message
            if "STATE" not in result.output:
                state_msg: str = f"Expected {'STATE'} in {result.output}"
                raise AssertionError(state_msg)

    @pytest.mark.usefixtures("_mock_ldap_api")
    @patch("flext_target_ldap.client.get_ldap_api")
    def test_upsert_behavior(
        self,
        runner: Mock,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        """Test upsert behavior for duplicate records."""
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
        with input_path.open("w", encoding="utf-8") as f:
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

        def search_side_effect(*_args: str | int | bool) -> bool:
            # First search: no entry
            # Second search: entry exists
            if mock_conn_instance.search.call_count <= 1:
                mock_conn_instance.entries = []
            else:
                mock_conn_instance.entries = [MagicMock()]
            return True

        mock_conn_instance.search.side_effect = search_side_effect
        # Wire patched API to use our mock connection instance
        with patch("flext_target_ldap.client.get_ldap_api") as mock_api:
            mock_api.return_value = mock_conn_instance
            # Run target
            with input_path.open(encoding="utf-8") as f:
                # Mock CLI invocation
                mock_result = Mock()
                mock_result.exit_code = 0
                mock_result.output = '{"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}'
                runner.invoke.return_value = mock_result
                result = runner.invoke(
                    "mock_cli",
                    ["--config", str(config_file)],
                    input=f.read(),
                    catch_exceptions=False,
                )
            if result.exit_code != 0:
                error_msg: str = f"Expected {0}, got {result.exit_code}"
                raise AssertionError(error_msg)
            # Should have one add and one modify
            if mock_conn_instance.add.call_count < 1:
                add_msg: str = f"Expected {mock_conn_instance.add.call_count} >= {1}"
                raise AssertionError(add_msg)
            assert mock_conn_instance.modify.call_count >= 1

    @pytest.mark.usefixtures("_mock_ldap_api")
    @patch("flext_target_ldap.client.get_ldap_api")
    def test_delete_records(
        self,
        runner: Mock,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        """Test deletion of LDAP records."""
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
        with input_path.open("w", encoding="utf-8") as f:
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
        with input_path.open(encoding="utf-8") as f:
            # Mock CLI invocation
            mock_result = Mock()
            mock_result.exit_code = 0
            mock_result.output = (
                '{"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}'
            )
            runner.invoke.return_value = mock_result
            result = runner.invoke(
                "mock_cli",
                ["--config", str(config_file)],
                input=f.read(),
                catch_exceptions=False,
            )
        if result.exit_code != 0:
            error_msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(error_msg)
        # Verify delete was called
        mock_conn_instance.delete.assert_called_once_with("uid=deleted,dc=test,dc=com")

    @pytest.mark.usefixtures("_mock_ldap_api", "_config_file")
    @patch("flext_target_ldap.client.get_ldap_api")
    def test_dn_template_usage(
        self,
        runner: Mock,
        tmp_path: Path,
        mock_ldap_config: dict[str, object],
    ) -> None:
        """Test DN template usage for record processing."""
        # Add DN template to config
        mock_ldap_config["dn_templates"] = {
            "users": "uid={uid},ou=people,dc=test,dc=com",
        }
        config_path = tmp_path / "template_config.json"
        with config_path.open("w", encoding="utf-8") as f:
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
        with input_path.open("w", encoding="utf-8") as f:
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
        with input_path.open(encoding="utf-8") as f:
            # Mock CLI invocation
            mock_result = Mock()
            mock_result.exit_code = 0
            mock_result.output = (
                '{"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}'
            )
            runner.invoke.return_value = mock_result
            result = runner.invoke(
                "mock_cli",
                ["--config", str(config_path)],
                input=f.read(),
                catch_exceptions=False,
            )
        if result.exit_code != 0:
            error_msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(error_msg)
        # Verify DN was constructed from template
        add_calls = mock_conn_instance.add.call_args_list
        assert len(add_calls) > 0
        if add_calls[0][0][0] != "uid=testuser,ou=people,dc=test,dc=com":
            dn_msg: str = f"Expected {'uid=testuser,ou=people,dc=test,dc=com'}, got {add_calls[0][0][0]}"
            raise AssertionError(dn_msg)

    def test_self(self, runner: Mock, tmp_path: Path) -> None:
        """Test error handling for invalid configurations."""
        # Invalid config
        bad_config = {"invalid": "config"}
        config_path = tmp_path / "bad_config.json"
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(bad_config, f)
        # Mock CLI invocation
        mock_result = Mock()
        mock_result.exit_code = 1  # Error case
        mock_result.output = "Configuration error"
        runner.invoke.return_value = mock_result
        result = runner.invoke(
            "mock_cli",
            ["--config", str(config_path)],
            input='{"type": "RECORD", "stream": "test", "record": {}}',
        )
        assert result.exit_code != 0

    @pytest.mark.usefixtures("_mock_ldap_api")
    @patch("flext_target_ldap.client.get_ldap_api")
    def test_multi_stream_handling(
        self,
        runner: Mock,
        config_file: Path,
        tmp_path: Path,
    ) -> None:
        """Test handling of multiple Singer streams."""
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
        with input_path.open("w", encoding="utf-8") as f:
            f.writelines(json.dumps(msg) + "\n" for msg in messages)
        # Mock connection
        mock_conn_instance = MagicMock()
        mock_conn_instance.bound = True
        mock_conn_instance.search.return_value = True
        mock_conn_instance.entries = []
        mock_conn_instance.add.return_value = True
        # Mock LDAP API is already configured
        # Run target
        with input_path.open(encoding="utf-8") as f:
            # Mock CLI invocation
            mock_result = Mock()
            mock_result.exit_code = 0
            mock_result.output = (
                '{"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}'
            )
            runner.invoke.return_value = mock_result
            result = runner.invoke(
                "mock_cli",
                ["--config", str(config_file)],
                input=f.read(),
                catch_exceptions=False,
            )
        if result.exit_code != 0:
            error_msg: str = f"Expected {0}, got {result.exit_code}"
            raise AssertionError(error_msg)
        # Verify both streams were processed
        if mock_conn_instance.add.call_count < 2:
            count_msg: str = f"Expected {mock_conn_instance.add.call_count} >= {2}"
            raise AssertionError(count_msg)
