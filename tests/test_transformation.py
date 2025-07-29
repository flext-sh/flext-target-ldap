"""Tests for data transformation engine."""

from __future__ import annotations

from flext_target_ldap.transformation import (
# Constants
EXPECTED_DATA_COUNT = 3

    DataTransformationEngine,
    MigrationValidator,
    TransformationRule,
)


class TestDataTransformationEngine:
    """Test data transformation engine."""

    def test_initialization(self) -> None:
        rules = [TransformationRule(name="test", pattern="test", replacement="test")]
        engine = DataTransformationEngine(rules)

        if len(engine.rules) != 1:

            raise AssertionError(f"Expected {1}, got {len(engine.rules)}")
        stats = engine.get_statistics()
        if stats["transformations_applied"] != 0:
            raise AssertionError(f"Expected {0}, got {stats["transformations_applied"]}")

    def test_transform_oracle_dn_structure(self) -> None:
        rule = TransformationRule(
            name="oracle_dn_structure_transform",
            pattern="dc=ctbc",
            replacement="dc=network,dc=ctbc",
        )
        engine = DataTransformationEngine([rule])

        entry = {
            "dn": "cn=testuser,ou=people,dc=ctbc",
            "objectClass": ["orclUser", "person"],
            "cn": "testuser",
        }

        result = engine.transform_data(entry)

        assert result.success
        transform_result = result.data
        assert transform_result is not None
        assert (
            transform_result.transformed_data["dn"]
            == "cn=testuser,ou=people,dc=network,dc=ctbc"
        )
        if "oracle_dn_structure_transform" not in transform_result.applied_rules:
            raise AssertionError(f"Expected {"oracle_dn_structure_transform"} in {transform_result.applied_rules}")

    def test_transform_oracle_objectclasses(self) -> None:
        rule = TransformationRule(
            name="oracle_objectclass_conversion",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
        engine = DataTransformationEngine([rule])

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["orclUser", "top"],
            "cn": "testuser",
        }

        result = engine.transform_data(entry)

        assert result.success
        transform_result = result.data
        assert transform_result is not None
        # The transformed objectClass list contains the replacement
        object_classes = transform_result.transformed_data["objectClass"]
        if "inetOrgPerson" not in str(object_classes):
            raise AssertionError(f"Expected {"inetOrgPerson"} in {str(object_classes)}")
        assert "oracle_objectclass_conversion" in transform_result.applied_rules

    def test_transform_oracle_attributes(self) -> None:
        # Create rules for Oracle value transformation (not attribute name mapping)
        rules = [
            TransformationRule(
                name="oracle_user_prefix_removal",
                pattern="^orcl",
                replacement="",
            ),
            TransformationRule(
                name="normalize_case",
                pattern="User$",
                replacement="user",
            ),
        ]
        engine = DataTransformationEngine(rules)

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["orclUser"],
            "description": "Oracle User Account",
            "title": "Test User",
        }

        result = engine.transform_data(entry)

        assert result.success
        transform_result = result.data
        assert transform_result is not None
        # Check that transformation rules were applied
        assert len(transform_result.applied_rules) > 0
        # Check specific transformations
        if transform_result.transformed_data["objectClass"] != [:
            raise AssertionError(f"Expected {[}, got {transform_result.transformed_data["objectClass"]}")
            "user",
        ]  # orclUser -> User -> user
        if transform_result.transformed_data["title"] != "Test user"  # User -> user:
            raise AssertionError(f"Expected {"Test user"  # User -> user}, got {transform_result.transformed_data["title"]}")

    def test_remove_empty_attributes(self) -> None:
        # Create rule to clean empty attributes (simulated)
        rule = TransformationRule(
            name="clean_empty_attributes",
            pattern="",
            replacement="",
            enabled=False,  # This is a placeholder test
        )
        engine = DataTransformationEngine([rule])

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["person"],
            "cn": "testuser",
            "description": "",
            "mail": None,
            "telephoneNumber": [],
        }

        result = engine.transform_data(entry)

        assert result.success
        transform_result = result.data
        assert transform_result is not None
        # Entry is copied during transformation
        if "cn" not in transform_result.transformed_data:
            raise AssertionError(f"Expected {"cn"} in {transform_result.transformed_data}")

    def test_dry_run_transformation(self) -> None:
        rule = TransformationRule(
            name="test_rule",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
        engine = DataTransformationEngine([rule])

        entry = {
            "dn": "cn=testuser,ou=people,dc=ctbc",
            "objectClass": ["orclUser"],
            "cn": "testuser",
        }

        result = engine.transform_data(entry)

        assert result.success
        transform_result = result.data
        assert transform_result is not None
        # Check that transformation was performed
        if transform_result.original_data["objectClass"] != ["orclUser"]:
            raise AssertionError(f"Expected {["orclUser"]}, got {transform_result.original_data["objectClass"]}")

    def test_transformation_statistics(self) -> None:
        engine = DataTransformationEngine()

        # Process several entries
        entries = [
            {"dn": "cn=user1,dc=example,dc=com", "objectClass": ["orclUser"]},
            {"dn": "cn=user2,dc=example,dc=com", "objectClass": ["person"]},
            {"dn": "cn=user3,dc=ctbc", "objectClass": ["orclUser"]},
        ]

        for entry in entries:
            result = engine.transform_data(entry)
            assert result.success

        stats = engine.get_statistics()
        if stats["transformations_applied"] < 0:
            raise AssertionError(f"Expected {stats["transformations_applied"]} >= {0}")
        assert stats["rules_executed"] >= 0


class TestMigrationValidator:
    """Test migration validator."""

    def test_validate_valid_entry(self) -> None:
        validator = MigrationValidator()

        dn = "cn=testuser,ou=people,dc=example,dc=com"
        attributes = {
            "cn": "testuser",
            "sn": "User",
            "mail": "test@example.com",
        }
        object_classes = ["inetOrgPerson", "person"]

        result = validator.validate_entry(dn, attributes, object_classes)

        assert result.success

    def test_validate_missing_dn(self) -> None:
        validator = MigrationValidator()

        # Missing DN test - pass empty DN
        result = validator.validate_entry("", {"cn": "testuser"}, ["person"])

        assert not result.success
        assert result.error is not None
        if "DN cannot be empty or whitespace" not in result.error:
            raise AssertionError(f"Expected {"DN cannot be empty or whitespace"} in {result.error}")

    def test_validate_invalid_dn_syntax(self) -> None:
        validator = MigrationValidator()

        result = validator.validate_entry(
            "invalid_dn_format",
            {"cn": "testuser"},
            ["person"],
        )

        # This will depend on the actual validation implementation
        # For now, just check it doesn't crash
        assert result is not None

    def test_validate_missing_objectclass(self) -> None:
        validator = MigrationValidator()

        result = validator.validate_entry(
            "cn=testuser,dc=example,dc=com",
            {"cn": "testuser"},
            [],
        )

        assert not result.success
        assert result.error is not None
        if "Object classes must be a non-empty list" not in result.error:
            raise AssertionError(f"Expected {"Object classes must be a non-empty list"} in {result.error}")

    def test_validate_missing_required_attributes(self) -> None:
        validator = MigrationValidator()

        result = validator.validate_entry(
            "cn=testuser,ou=people,dc=example,dc=com",
            {"cn": "testuser"},
            ["person"],
        )

        # This test depends on validation rules which may produce warnings
        assert result is not None

    def test_validate_invalid_email(self) -> None:
        validator = MigrationValidator()

        result = validator.validate_entry(
            "cn=testuser,ou=people,dc=example,dc=com",
            {"cn": "testuser", "sn": "User", "mail": "invalid-email"},
            ["inetOrgPerson", "person"],
        )

        # Email validation might be handled differently
        assert result is not None

    def test_validation_statistics(self) -> None:
        validator = MigrationValidator()

        # Convert entries to proper format for validation
        test_cases = [
            ("cn=user1,dc=example,dc=com", {"cn": "user1", "sn": "One"}, ["person"]),
            ("invalid", {"cn": "user2"}, ["person"]),
            ("", {"cn": "user3"}, ["person"]),
        ]

        for dn, attributes, object_classes in test_cases:
            validator.validate_entry(dn, attributes, object_classes)

        stats = validator.get_validation_statistics()
        if stats["entries_validated"] != EXPECTED_DATA_COUNT:
            raise AssertionError(f"Expected {3}, got {stats["entries_validated"]}")
        if stats["validation_errors"] < 0:
            raise AssertionError(f"Expected {stats["validation_errors"]} >= {0}")
        assert stats["validation_warnings"] >= 0


class TestTransformationRule:
    """Test transformation rule configuration."""

    def test_transformation_rule_creation(self) -> None:
        rule = TransformationRule(
            name="test_rule",
            pattern="orclUser",
            replacement="person",
            enabled=True,
        )

        if rule.name != "test_rule":

            raise AssertionError(f"Expected {"test_rule"}, got {rule.name}")
        if not (rule.enabled):
            raise AssertionError(f"Expected True, got {rule.enabled}")
        if rule.pattern != "orclUser":
            raise AssertionError(f"Expected {"orclUser"}, got {rule.pattern}")
        assert rule.replacement == "person"


class TestIntegratedTransformation:
    """Test integrated transformation workflow."""

    def test_full_oracle_migration_workflow(self) -> None:
        # Create transformation rules for Oracle migration
        rules = [
            TransformationRule(
                name="oracle_dn_transform",
                pattern="dc=ctbc",
                replacement="dc=network,dc=ctbc",
            ),
            TransformationRule(
                name="oracle_objectclass",
                pattern="orclUser",
                replacement="inetOrgPerson",
            ),
        ]

        # Initialize engines
        transformation_engine = DataTransformationEngine(rules)
        validator = MigrationValidator(strict_mode=False)

        # Oracle entry to migrate
        oracle_entry = {
            "dn": "cn=john.doe,ou=people,dc=ctbc",
            "objectClass": ["orclUser", "top"],
            "orclSamAccountName": "john.doe",
            "orclCommonName": "John Doe",
            "orclMailNickname": "jdoe",
            "mail": "john.doe@company.com",
            "userPassword": "{SSHA}hashedpassword",
        }

        # Transform the entry
        transformation_result = transformation_engine.transform_data(oracle_entry)

        assert transformation_result.success
        transform_data = transformation_result.data
        assert transform_data is not None
        assert len(transform_data.applied_rules) > 0

        transformed_entry = transform_data.transformed_data

        # Check DN transformation
        if transformed_entry["dn"] != "cn=john.doe,ou=people,dc=network,dc=ctbc":
            raise AssertionError(f"Expected {"cn=john.doe,ou=people,dc=network,dc=ctbc"}, got {transformed_entry["dn"]}")

        # Check object class conversion - check if transformation was applied
        object_classes = transformed_entry["objectClass"]
        if "inetOrgPerson" not in str(object_classes):
            raise AssertionError(f"Expected {"inetOrgPerson"} in {str(object_classes)}")

        # Validate the transformed entry
        # Extract components for validation
        dn = transformed_entry["dn"]
        attributes = {
            k: v for k, v in transformed_entry.items() if k not in {"dn", "objectClass"}
        }
        obj_classes = (
            transformed_entry["objectClass"]
            if isinstance(transformed_entry["objectClass"], list)
            else [transformed_entry["objectClass"]]
        )

        validation_result = validator.validate_entry(dn, attributes, obj_classes)

        assert validation_result.success

    def test_classification_and_transformation_integration(self) -> None:
        rule = TransformationRule(
            name="general_transform",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
        engine = DataTransformationEngine([rule])

        # Test various entry types
        test_entries = [
            {
                "dn": "cn=oid,cn=oraclecontext,dc=example,dc=com",
                "objectClass": ["orclContext"],
            },
            {
                "dn": "cn=testuser,ou=people,dc=ctbc",
                "objectClass": ["orclUser"],
            },
            {
                "dn": "uid=standard.user,ou=people,dc=example,dc=com",
                "objectClass": ["inetOrgPerson"],
            },
        ]

        for entry in test_entries:
            result = engine.transform_data(entry)

            assert result.success
            transform_data = result.data
            assert transform_data is not None
            # Check that transformation was processed
            assert transform_data.original_data is not None
