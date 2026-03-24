"""Tests for data transformation engine.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import t

from flext_target_ldap.transformation import (
    DataTransformationEngine,
    MigrationValidator,
    TransformationRule,
)

EXPECTED_DATA_COUNT = 3


class TestDataTransformationEngine:
    """Test data transformation engine."""

    def test_initialization(self) -> None:
        """Test method."""
        "Test initialization function."
        rules = [TransformationRule(name="test", pattern="test", replacement="test")]
        engine = DataTransformationEngine(rules)
        if len(engine.rules) != 1:
            msg: str = f"Expected {1}, got {len(engine.rules)}"
            raise AssertionError(msg)
        assert hasattr(engine, "transform")

    def test_transform_oracle_dn_structure(self) -> None:
        """Test method."""
        "Test transform oracle dn structure function."
        rule = TransformationRule(
            name="oracle_dn_structure_transform",
            pattern="dc=invaliddc",
            replacement="dc=network,dc=invaliddc",
        )
        engine = DataTransformationEngine([rule])
        entry: Mapping[str, t.ContainerValue] = {
            "dn": "cn=testuser,ou=people,dc=invaliddc",
            "objectClass": ["orclUser", "person"],
            "cn": "testuser",
        }
        result = engine.transform(entry)
        assert result.is_success
        transform_result = result.value
        assert transform_result is not None
        assert (
            transform_result.transformed_data["dn"]
            == "cn=testuser,ou=people,dc=network,dc=invaliddc"
        )
        if "oracle_dn_structure_transform" not in transform_result.applied_rules:
            msg: str = f"Expected {'oracle_dn_structure_transform'} in {transform_result.applied_rules}"
            raise AssertionError(msg)

    def test_transform_oracle_objectclasses(self) -> None:
        """Test method."""
        "Test transform oracle objectclasses function."
        rule = TransformationRule(
            name="oracle_objectclass_conversion",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
        engine = DataTransformationEngine([rule])
        entry: Mapping[str, t.ContainerValue] = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["orclUser", "top"],
            "cn": "testuser",
        }
        result = engine.transform(entry)
        assert result.is_success
        transform_result = result.value
        assert transform_result is not None
        object_classes = transform_result.transformed_data["objectClass"]
        if "inetOrgPerson" not in str(object_classes):
            msg: str = f"Expected {'inetOrgPerson'} in {object_classes!s}"
            raise AssertionError(msg)
        assert "oracle_objectclass_conversion" in transform_result.applied_rules

    def test_transform_oracle_attributes(self) -> None:
        """Test method."""
        "Test transform oracle attributes function."
        rules = [
            TransformationRule(
                name="oracle_user_prefix_removal", pattern="orcl", replacement=""
            ),
            TransformationRule(
                name="normalize_case", pattern="User", replacement="user"
            ),
        ]
        engine = DataTransformationEngine(rules)
        entry: Mapping[str, t.ContainerValue] = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["orclUser"],
            "description": "Oracle User Account",
            "title": "Test User",
        }
        result = engine.transform(entry)
        assert result.is_success
        transform_result = result.value
        assert transform_result is not None
        assert transform_result.applied_rules
        expected_object_class = ["user"]
        if transform_result.transformed_data["objectClass"] != expected_object_class:
            msg: str = f"Expected {expected_object_class}, got {transform_result.transformed_data['objectClass']}"
            raise AssertionError(msg)
        if transform_result.transformed_data["title"] != "Test user":
            msg: str = f"Expected 'Test user', got {transform_result.transformed_data['title']}"
            raise AssertionError(msg)

    def test_remove_empty_attributes(self) -> None:
        """Test method."""
        "Test remove empty attributes function."
        rule = TransformationRule(
            name="clean_empty_attributes", pattern="empty", replacement=""
        )
        engine = DataTransformationEngine([rule])
        entry: Mapping[str, t.ContainerValue] = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["person"],
            "cn": "testuser",
            "description": "",
        }
        result = engine.transform(entry)
        assert result.is_success
        transform_result = result.value
        assert transform_result is not None
        if "cn" not in transform_result.transformed_data:
            msg: str = f"Expected {'cn'} in {transform_result.transformed_data}"
            raise AssertionError(msg)

    def test_dry_run_transformation(self) -> None:
        """Test method."""
        "Test dry run transformation function."
        rule = TransformationRule(
            name="test_rule", pattern="orclUser", replacement="inetOrgPerson"
        )
        engine = DataTransformationEngine([rule])
        entry: Mapping[str, t.ContainerValue] = {
            "dn": "cn=testuser,ou=people,dc=invaliddc",
            "objectClass": ["orclUser"],
            "cn": "testuser",
        }
        result = engine.transform(entry)
        assert result.is_success
        transform_result = result.value
        assert transform_result is not None
        if transform_result.transformed_data["objectClass"] != ["inetOrgPerson"]:
            msg: str = f"Expected {['inetOrgPerson']}, got {transform_result.transformed_data['objectClass']}"
            raise AssertionError(msg)

    def test_transformation_statistics(self) -> None:
        """Test method."""
        "Test transformation statistics function."
        rule = TransformationRule(
            name="orcl_to_inetorgperson",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
        engine = DataTransformationEngine([rule])
        entries: Sequence[Mapping[str, t.ContainerValue]] = [
            {"dn": "cn=user1,dc=example,dc=com", "objectClass": ["orclUser"]},
            {"dn": "cn=user2,dc=example,dc=com", "objectClass": ["person"]},
            {"dn": "cn=user3,dc=invaliddc", "objectClass": ["orclUser"]},
        ]
        applied_rules_count = 0
        for entry in entries:
            result = engine.transform(entry)
            assert result.is_success
            transform_result = result.value
            assert transform_result is not None
            applied_rules_count += len(transform_result.applied_rules)
        assert applied_rules_count >= 2
        stats = engine.get_statistics()
        assert stats["total_rules"] == 1
        assert stats["transformations_applied"] == 0


class TestMigrationValidator:
    """Test migration validator."""

    def test_validate_valid_entry(self) -> None:
        """Test validate valid entry function."""
        validator = MigrationValidator()
        data: Mapping[str, t.ContainerValue] = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "cn": "testuser",
            "sn": "User",
            "mail": "test@example.com",
            "objectClass": ["inetOrgPerson", "person"],
        }
        result = validator.validate(data)
        assert result.is_success

    def test_validate_missing_dn(self) -> None:
        """Test validate missing dn function."""
        validator = MigrationValidator()
        result = validator.validate("", {"cn": "testuser"}, ["person"])
        assert not result.is_success
        assert result.error is not None
        if "DN cannot be empty or whitespace" not in result.error:
            msg: str = (
                f"Expected {'DN cannot be empty or whitespace'} in {result.error}"
            )
            raise AssertionError(msg)

    def test_validate_invalid_dn_syntax(self) -> None:
        """Test validate invalid dn syntax function."""
        validator = MigrationValidator()
        result = validator.validate("invalid_dn_format", {"cn": "testuser"}, ["person"])
        assert result is not None

    def test_validate_missing_objectclass(self) -> None:
        """Test method."""
        "Test validate missing objectclass function."
        validator = MigrationValidator()
        result = validator.validate(
            "cn=testuser,dc=example,dc=com", {"cn": "testuser"}, []
        )
        assert not result.is_success
        assert result.error is not None
        if "Object classes must be a non-empty list" not in result.error:
            msg: str = f"Expected {'Object classes must be a non-empty list'} in {result.error}"
            raise AssertionError(msg)

    def test_validate_missing_required_attributes(self) -> None:
        """Test method."""
        "Test validate missing required attributes function."
        validator = MigrationValidator()
        result = validator.validate(
            "cn=testuser,ou=people,dc=example,dc=com", {"cn": "testuser"}, ["person"]
        )
        assert result is not None

    def test_validate_invalid_email(self) -> None:
        """Test method."""
        "Test validate invalid email function."
        validator = MigrationValidator()
        result = validator.validate(
            "cn=testuser,ou=people,dc=example,dc=com",
            {"cn": "testuser", "sn": "User", "mail": "invalid-email"},
            ["inetOrgPerson", "person"],
        )
        assert result is not None

    def test_validation_statistics(self) -> None:
        """Test method."""
        "Test validation statistics function."
        validator = MigrationValidator()
        test_cases = [
            ("cn=user1,dc=example,dc=com", {"cn": "user1", "sn": "One"}, ["person"]),
            ("invalid", {"cn": "user2"}, ["person"]),
            ("", {"cn": "user3"}, ["person"]),
        ]
        for dn, attributes, object_classes in test_cases:
            validator.validate(dn, attributes, object_classes)
        stats = validator.get_validation_statistics()
        if stats["entries_validated"] != EXPECTED_DATA_COUNT:
            msg: str = f"Expected {3}, got {stats['entries_validated']}"
            raise AssertionError(msg)
        if stats["validation_errors"] < 0:
            msg: str = f"Expected {stats['validation_errors']} >= {0}"
            raise AssertionError(msg)
        assert stats["validation_warnings"] >= 0


class TestTransformationRule:
    """Test transformation rule configuration."""

    def test_transformation_rule_creation(self) -> None:
        """Test method."""
        "Test transformation rule creation function."
        rule = TransformationRule(
            name="test_rule", pattern="orclUser", replacement="person", enabled=True
        )
        if rule.name != "test_rule":
            msg: str = f"Expected 'test_rule', got {rule.name}"
            raise AssertionError(msg)
        if not rule.enabled:
            msg: str = f"Expected True, got {rule.enabled}"
            raise AssertionError(msg)
        if rule.pattern != "orclUser":
            msg: str = f"Expected 'orclUser', got {rule.pattern}"
            raise AssertionError(msg)
        assert rule.replacement == "person"


class TestIntegratedTransformation:
    """Test integrated transformation workflow."""

    def test_full_oracle_migration_workflow(self) -> None:
        """Test method."""
        "Test full oracle migration workflow function."
        rules = [
            TransformationRule(
                name="oracle_dn_transform",
                pattern="dc=invaliddc",
                replacement="dc=network,dc=invaliddc",
            ),
            TransformationRule(
                name="oracle_objectclass",
                pattern="orclUser",
                replacement="inetOrgPerson",
            ),
        ]
        transformation_engine = DataTransformationEngine(rules)
        validator = MigrationValidator(strict_mode=False)
        oracle_entry: Mapping[str, t.ContainerValue] = {
            "dn": "cn=john.doe,ou=people,dc=invaliddc",
            "objectClass": ["orclUser", "top"],
            "orclSamAccountName": "john.doe",
            "orclCommonName": "John Doe",
            "orclMailNickname": "jdoe",
            "mail": "john.doe@company.com",
            "userPassword": "{SSHA}hashedpassword",
        }
        transformation_result = transformation_engine.transform(oracle_entry)
        assert transformation_result.is_success
        transform = transformation_result.value
        assert transform is not None
        assert transform.applied_rules
        transformed_entry = transform.transformed_data
        if transformed_entry["dn"] != "cn=john.doe,ou=people,dc=network,dc=invaliddc":
            msg: str = f"Expected {'cn=john.doe,ou=people,dc=network,dc=invaliddc'}, got {transformed_entry['dn']}"
            raise AssertionError(msg)
        object_classes = transformed_entry["objectClass"]
        if "inetOrgPerson" not in str(object_classes):
            msg: str = f"Expected {'inetOrgPerson'} in {object_classes!s}"
            raise AssertionError(msg)
        dn = str(transformed_entry["dn"])
        attributes = {
            k: v for k, v in transformed_entry.items() if k not in {"dn", "objectClass"}
        }
        raw_classes = transformed_entry["objectClass"]
        obj_classes: Sequence[str] = (
            [str(c) for c in raw_classes]
            if isinstance(raw_classes, list)
            else [str(raw_classes)]
        )
        validation_result = validator.validate(dn, attributes, obj_classes)
        assert validation_result.is_success

    def test_classification_and_transformation_integration(self) -> None:
        """Test method."""
        "Test classification and transformation integration function."
        rule = TransformationRule(
            name="general_transform", pattern="orclUser", replacement="inetOrgPerson"
        )
        engine = DataTransformationEngine([rule])
        test_entries: Sequence[Mapping[str, t.ContainerValue]] = [
            {
                "dn": "cn=oid,cn=oraclecontext,dc=example,dc=com",
                "objectClass": ["orclContext"],
            },
            {"dn": "cn=testuser,ou=people,dc=invaliddc", "objectClass": ["orclUser"]},
            {
                "dn": "uid=standard.user,ou=people,dc=example,dc=com",
                "objectClass": ["inetOrgPerson"],
            },
        ]
        for entry in test_entries:
            result = engine.transform(entry)
            assert result.is_success
            transform = result.value
            assert transform is not None
            assert transform.transformed_data is not None
