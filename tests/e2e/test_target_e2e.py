"""End-to-end tests for target-ldap."""

from __future__ import annotations

import json
import subprocess
from typing import TYPE_CHECKING, Any

from .conftest import (
    count_entries,
    get_user_attributes,
    verify_group_loaded,
    verify_user_loaded,
)

if TYPE_CHECKING:
    from pathlib import Path

    from ldap3 import Connection


class TestTargetLDAPE2E:
    """E2E tests for target-ldap."""

    def test_load_users(
        self,
        target_config_file: Path,
        sample_user_records: list[dict[str, Any]],
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test loading user records."""
        # Create input file
        input_file = tmp_path / "users.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            for record in sample_user_records:
                f.write(json.dumps(record) + "\n")

        # Run target
        with open(input_file, encoding="utf-8") as f:
            process = subprocess.Popen(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            _stdout, stderr = process.communicate()

        assert process.returncode == 0, f"Target failed: {stderr}"

        # Verify users were loaded
        assert verify_user_loaded(target_connection, "john.doe")
        assert verify_user_loaded(target_connection, "jane.smith")

        # Verify user attributes
        john_attrs = get_user_attributes(target_connection, "john.doe")
        assert john_attrs["cn"] == ["John Doe"]
        assert john_attrs["sn"] == ["Doe"]
        assert john_attrs["givenName"] == ["John"]
        assert john_attrs["mail"] == ["john.doe@source.com"]
        assert john_attrs["employeeNumber"] == ["1001"]

        jane_attrs = get_user_attributes(target_connection, "jane.smith")
        assert jane_attrs["cn"] == ["Jane Smith"]
        assert jane_attrs["sn"] == ["Smith"]
        assert jane_attrs["givenName"] == ["Jane"]
        assert jane_attrs["mail"] == ["jane.smith@source.com"]
        assert jane_attrs["employeeNumber"] == ["1002"]

    def test_load_groups(
        self,
        target_config_file: Path,
        sample_group_records: list[dict[str, Any]],
        sample_user_records: list[dict[str, Any]],
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test loading group records."""
        # First load users (groups need users to exist)
        input_file = tmp_path / "users_and_groups.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            for record in sample_user_records + sample_group_records:
                f.write(json.dumps(record) + "\n")

        # Run target
        with open(input_file, encoding="utf-8") as f:
            process = subprocess.Popen(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            _stdout, stderr = process.communicate()

        assert process.returncode == 0, f"Target failed: {stderr}"

        # Verify groups were loaded
        assert verify_group_loaded(target_connection, "engineering")
        assert verify_group_loaded(target_connection, "sales")

        # Verify group membership
        target_connection.search(
            search_base="dc=target,dc=com",
            search_filter="(cn=engineering)",
            search_scope="SUBTREE",
            attributes=["member"],
        )
        assert len(target_connection.entries) == 1
        engineering_group = target_connection.entries[0]
        members = (
            engineering_group.member.values
            if hasattr(engineering_group, "member")
            else []
        )

        # The DN should be transformed according to the template
        expected_member_dn = "uid=john.doe,ou=migrated,dc=target,dc=com"
        assert expected_member_dn in members

    def test_upsert_functionality(
        self,
        target_config_file: Path,
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test upsert (insert and update) functionality."""
        # First load - create user
        initial_record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=test.user,ou=people,dc=source,dc=com",
                "uid": "test.user",
                "cn": "Test User",
                "sn": "User",
                "givenName": "Test",
                "mail": "test.user@source.com",
                "employeeNumber": "9999",
                "employeeType": "active",
            },
            "time_extracted": "2024-01-01T12:00:00Z",
        }

        input_file1 = tmp_path / "initial.jsonl"
        with open(input_file1, "w", encoding="utf-8") as f:
            f.write(json.dumps(initial_record) + "\n")

        with open(input_file1, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                check=True,
            )

        # Verify initial load
        assert verify_user_loaded(target_connection, "test.user")
        initial_attrs = get_user_attributes(target_connection, "test.user")
        assert initial_attrs["mail"] == ["test.user@source.com"]
        assert initial_attrs["employeeType"] == ["active"]

        # Second load - update user
        updated_record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=test.user,ou=people,dc=source,dc=com",
                "uid": "test.user",
                "cn": "Test User Updated",
                "sn": "User",
                "givenName": "Test",
                "mail": "test.user.updated@source.com",
                "employeeNumber": "9999",
                "employeeType": "inactive",
                "title": "Senior Developer",  # New attribute
            },
            "time_extracted": "2024-01-01T12:30:00Z",
        }

        input_file2 = tmp_path / "updated.jsonl"
        with open(input_file2, "w", encoding="utf-8") as f:
            f.write(json.dumps(updated_record) + "\n")

        with open(input_file2, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                check=True,
            )

        # Verify update
        updated_attrs = get_user_attributes(target_connection, "test.user")
        assert updated_attrs["cn"] == ["Test User Updated"]
        assert updated_attrs["mail"] == ["test.user.updated@source.com"]
        assert updated_attrs["employeeType"] == ["inactive"]
        assert updated_attrs.get("title") == ["Senior Developer"]

    def test_deletion_markers(
        self,
        target_config_file: Path,
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test handling of deletion markers."""
        # First load - create user
        create_record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=delete.me,ou=people,dc=source,dc=com",
                "uid": "delete.me",
                "cn": "Delete Me",
                "sn": "Me",
                "givenName": "Delete",
                "mail": "delete.me@source.com",
                "employeeNumber": "8888",
            },
            "time_extracted": "2024-01-01T12:00:00Z",
        }

        input_file1 = tmp_path / "create.jsonl"
        with open(input_file1, "w", encoding="utf-8") as f:
            f.write(json.dumps(create_record) + "\n")

        with open(input_file1, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                check=True,
            )

        # Verify creation
        assert verify_user_loaded(target_connection, "delete.me")

        # Second load - delete user
        delete_record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=delete.me,ou=people,dc=source,dc=com",
                "uid": "delete.me",
                "_sdc_deleted_at": "2024-01-01T13:00:00Z",
            },
            "time_extracted": "2024-01-01T13:00:00Z",
        }

        input_file2 = tmp_path / "delete.jsonl"
        with open(input_file2, "w", encoding="utf-8") as f:
            f.write(json.dumps(delete_record) + "\n")

        with open(input_file2, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                check=True,
            )

        # Verify deletion
        assert not verify_user_loaded(target_connection, "delete.me")

    def test_dn_template_transformation(
        self,
        target_config_file: Path,
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test DN template transformation."""
        # Create user with source DN
        record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "dn": "uid=transform.me,ou=people,dc=source,dc=com",
                "uid": "transform.me",
                "cn": "Transform Me",
                "sn": "Me",
                "givenName": "Transform",
                "mail": "transform.me@source.com",
            },
            "time_extracted": "2024-01-01T12:00:00Z",
        }

        input_file = tmp_path / "transform.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        with open(input_file, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                check=True,
            )

        # Verify the user exists with transformed DN
        target_connection.search(
            search_base="dc=target,dc=com",
            search_filter="(uid=transform.me)",
            search_scope="SUBTREE",
            attributes=["*"],
        )

        assert len(target_connection.entries) == 1
        entry = target_connection.entries[0]

        # The DN should follow the template: uid={uid},ou=migrated,{base_dn}
        expected_dn = "uid=transform.me,ou=migrated,dc=target,dc=com"
        assert entry.entry_dn == expected_dn

    def test_batch_loading(
        self,
        target_config_file: Path,
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test loading large batches of records."""
        # Generate many user records
        records = [
            {
                "type": "RECORD",
                "stream": "users",
                "record": {
                    "dn": f"uid=batch{i:03d},ou=people,dc=source,dc=com",
                    "uid": f"batch{i:03d}",
                    "cn": f"Batch User {i}",
                    "sn": f"User{i}",
                    "givenName": "Batch",
                    "mail": f"batch{i:03d}@source.com",
                    "employeeNumber": str(5000 + i),
                },
                "time_extracted": f"2024-01-01T12:{i:02d}:00Z",
            }
            for i in range(50)
        ]

        input_file = tmp_path / "batch.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record) + "\n")

        # Run target
        with open(input_file, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(target_config_file)],
                stdin=f,
                check=True,
            )

        # Verify all users were loaded
        loaded_count = count_entries(target_connection, "(uid=batch*)")
        assert loaded_count == 50

        # Verify specific users
        assert verify_user_loaded(target_connection, "batch000")
        assert verify_user_loaded(target_connection, "batch049")

    def test_error_handling(
        self,
        target_config: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test error handling scenarios."""
        # Test with invalid LDAP server
        bad_config = target_config.copy()
        bad_config["host"] = "nonexistent.host"

        bad_config_file = tmp_path / "bad-config.json"
        bad_config_file.write_text(json.dumps(bad_config))

        # Create valid record
        record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "uid": "test.user",
                "cn": "Test User",
            },
        }

        input_file = tmp_path / "test.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        # Should fail with connection error
        with open(input_file, encoding="utf-8") as f:
            result = subprocess.run(
                ["target-ldap", "--config", str(bad_config_file)],
                stdin=f,
                capture_output=True,
                text=True,
                check=False,
            )

        assert result.returncode != 0

    def test_validation_mode(
        self,
        target_config: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Test validation mode functionality."""
        # Enable validation
        target_config["validate_records"] = True

        config_file = tmp_path / "validate-config.json"
        config_file.write_text(json.dumps(target_config))

        # Test with invalid record (missing required fields)
        invalid_record = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "uid": "invalid.user",
                # Missing required fields like cn, sn
            },
        }

        input_file = tmp_path / "invalid.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(invalid_record) + "\n")

        # Should handle validation gracefully
        with open(input_file, encoding="utf-8") as f:
            result = subprocess.run(
                ["target-ldap", "--config", str(config_file)],
                stdin=f,
                capture_output=True,
                text=True,
                check=False,
            )

        # The result depends on validation implementation
        # At minimum, it should not crash
        assert "error" in result.stderr.lower() or result.returncode != 0

    def test_custom_object_classes(
        self,
        target_config: dict[str, Any],
        target_connection: Connection,
        tmp_path: Path,
    ) -> None:
        """Test custom object classes configuration."""
        # Add custom object classes for service accounts
        target_config["dn_templates"]["service_accounts"] = (
            "uid={uid},ou=services,{base_dn}"
        )
        target_config["default_object_classes"]["service_accounts"] = [
            "account",
            "simpleSecurityObject",
            "top",
        ]

        config_file = tmp_path / "custom-config.json"
        config_file.write_text(json.dumps(target_config))

        # Create service account record
        record = {
            "type": "RECORD",
            "stream": "service_accounts",
            "record": {
                "dn": "uid=svc-test,ou=services,dc=source,dc=com",
                "uid": "svc-test",
                "description": "Test Service Account",
                "userPassword": "{SSHA}x+wnyY9qS7TCSSdg1CtNyJr8FtNFh2RF",
            },
            "time_extracted": "2024-01-01T12:00:00Z",
        }

        input_file = tmp_path / "service.jsonl"
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        # Ensure target OU exists
        import contextlib

        with contextlib.suppress(Exception):
            target_connection.add(
                "ou=services,dc=target,dc=com",
                attributes={
                    "objectClass": ["organizationalUnit", "top"],
                    "ou": "services",
                    "description": "Service Accounts",
                },
            )

        with open(input_file, encoding="utf-8") as f:
            subprocess.run(
                ["target-ldap", "--config", str(config_file)],
                stdin=f,
                check=True,
            )

        # Verify service account was loaded with correct object classes
        target_connection.search(
            search_base="dc=target,dc=com",
            search_filter="(uid=svc-test)",
            search_scope="SUBTREE",
            attributes=["objectClass"],
        )

        assert len(target_connection.entries) == 1
        entry = target_connection.entries[0]
        object_classes = [oc.lower() for oc in entry.objectClass.values]

        assert "account" in object_classes
        assert "simplesecurityobject" in object_classes
        assert "top" in object_classes
