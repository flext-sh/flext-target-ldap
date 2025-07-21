"""Tests for data transformation engine."""

from __future__ import annotations

from flext_target_ldap.transformation import (
    DataTransformationEngine,
    MigrationValidator,
    TransformationRule,
)


class TestDataTransformationEngine:
    """Test data transformation engine."""

    def test_initialization(self) -> None:
        config = {"oracle_migration_mode": True}
        engine = DataTransformationEngine(config)

        assert engine.config == config
        assert len(engine.rules) > 0
        assert engine.stats["total_processed"] == 0

    def test_transform_oracle_dn_structure(self) -> None:
        config = {"enable_transformation": True}
        engine = DataTransformationEngine(config)

        entry = {
            "dn": "cn=testuser,ou=people,dc=ctbc",
            "objectClass": ["orclUser", "person"],
            "cn": "testuser",
        }

        result = engine.transform_entry(entry)

        assert result.success is True
        assert (
            result.transformed_entry["dn"] == "cn=testuser,ou=people,dc=network,dc=ctbc"
        )
        assert "oracle_dn_structure_transform" in result.applied_rules

    def test_transform_oracle_objectclasses(self) -> None:
        config = {"enable_transformation": True}
        engine = DataTransformationEngine(config)

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["orclUser", "top"],
            "cn": "testuser",
        }

        result = engine.transform_entry(entry)

        assert result.success is True
        transformed_ocs = result.transformed_entry["objectClass"]
        assert "orclUser" not in transformed_ocs
        assert "inetOrgPerson" in transformed_ocs
        assert "person" in transformed_ocs
        assert "oracle_objectclass_conversion" in result.applied_rules

    def test_transform_oracle_attributes(self) -> None:
        config = {"enable_transformation": True}
        engine = DataTransformationEngine(config)

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["orclUser"],
            "orclSamAccountName": "testuser",
            "orclCommonName": "Test User",
        }

        result = engine.transform_entry(entry)

        assert result.success is True
        transformed_entry = result.transformed_entry
        assert "orclSamAccountName" not in transformed_entry
        assert transformed_entry.get("uid") == "testuser"
        assert "orclCommonName" not in transformed_entry
        assert transformed_entry.get("cn") == "Test User"
        assert "oracle_attribute_mapping" in result.applied_rules

    def test_remove_empty_attributes(self) -> None:
        config = {"enable_transformation": True}
        engine = DataTransformationEngine(config)

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["person"],
            "cn": "testuser",
            "description": "",
            "mail": None,
            "telephoneNumber": [],
        }

        result = engine.transform_entry(entry)

        assert result.success is True
        transformed_entry = result.transformed_entry
        assert "description" not in transformed_entry
        assert "mail" not in transformed_entry
        assert "telephoneNumber" not in transformed_entry
        assert "cn" in transformed_entry  # Required attribute preserved
        assert "clean_empty_attributes" in result.applied_rules

    def test_dry_run_transformation(self) -> None:
        config = {"enable_transformation": True, "dry_run_mode": True}
        engine = DataTransformationEngine(config)

        entry = {
            "dn": "cn=testuser,ou=people,dc=ctbc",
            "objectClass": ["orclUser"],
            "cn": "testuser",
        }

        result = engine.transform_entry(entry)

        assert result.success is True
        assert len(result.applied_rules) > 0
        # Original entry should not be modified in dry run
        assert result.metadata.get("transformation_timestamp") is not None

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
            assert result.is_success

        stats = engine.get_statistics()
        assert stats["transformations_applied"] >= 0
        assert stats["rules_executed"] >= 0


class TestMigrationValidator:
    """Test migration validator."""

    def test_validate_valid_entry(self) -> None:
        validator = MigrationValidator()

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["inetOrgPerson", "person"],
            "cn": "testuser",
            "sn": "User",
            "mail": "test@example.com",
        }

        result = validator.validate_entry(entry)

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert "dn_syntax" in result["checks_performed"]
        assert "object_classes" in result["checks_performed"]

    def test_validate_missing_dn(self) -> None:
        validator = MigrationValidator()

        entry = {"objectClass": ["person"], "cn": "testuser"}

        result = validator.validate_entry(entry)

        assert result["valid"] is False
        assert "Missing DN" in result["errors"]

    def test_validate_invalid_dn_syntax(self) -> None:
        validator = MigrationValidator()

        entry = {"dn": "invalid_dn_format", "objectClass": ["person"], "cn": "testuser"}

        result = validator.validate_entry(entry)

        assert result["valid"] is False
        assert any("Invalid DN syntax" in error for error in result["errors"])

    def test_validate_missing_objectclass(self) -> None:
        validator = MigrationValidator()

        entry = {"dn": "cn=testuser,dc=example,dc=com", "cn": "testuser"}

        result = validator.validate_entry(entry)

        assert result["valid"] is False
        assert "Missing objectClass" in result["errors"]

    def test_validate_missing_required_attributes(self) -> None:
        validator = MigrationValidator()

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["person"],
            "cn": "testuser",
            # Missing required 'sn' attribute for person
        }

        result = validator.validate_entry(entry)

        assert result["valid"] is False
        assert any(
            "Missing required attribute 'sn'" in error for error in result["errors"]
        )

    def test_validate_invalid_email(self) -> None:
        validator = MigrationValidator()

        entry = {
            "dn": "cn=testuser,ou=people,dc=example,dc=com",
            "objectClass": ["inetOrgPerson", "person"],
            "cn": "testuser",
            "sn": "User",
            "mail": "invalid-email",
        }

        result = validator.validate_entry(entry)

        assert result["valid"] is True  # Email validation produces warnings, not errors
        assert any("Invalid email format" in warning for warning in result["warnings"])

    def test_validation_statistics(self) -> None:
        validator = MigrationValidator()

        # Process several entries
        entries = [
            {
                "dn": "cn=user1,dc=example,dc=com",
                "objectClass": ["person"],
                "cn": "user1",
                "sn": "One",
            },
            {"dn": "invalid", "objectClass": ["person"], "cn": "user2"},
            {"objectClass": ["person"], "cn": "user3"},
        ]

        for entry in entries:
            validator.validate_entry(entry)

        stats = validator.get_validation_statistics()
        assert stats["total_validated"] == 3
        assert stats["validation_passed"] >= 1
        assert stats["validation_failed"] >= 1
        assert stats["pass_rate"] >= 0


class TestTransformationRule:
    """Test transformation rule configuration."""

    def test_transformation_rule_creation(self) -> None:
        rule = TransformationRule(
            name="test_rule",
            condition="entry.get('objectClass') == ['orclUser']",
            action="convert_oracle_objectclasses",
            parameters={"mappings": {"orclUser": ["person"]}},
            priority=10,
            description="Test rule",
        )

        assert rule.name == "test_rule"
        assert rule.enabled is True
        assert rule.priority == 10
        assert rule.parameters["mappings"]["orclUser"] == ["person"]


class TestIntegratedTransformation:
    """Test integrated transformation workflow."""

    def test_full_oracle_migration_workflow(self) -> None:
        config = {
            "enable_transformation": True,
            "oracle_migration_mode": True,
            "enable_validation": True,
        }

        # Initialize engines
        transformation_engine = DataTransformationEngine(config)
        validator = MigrationValidator(config)

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
        transformation_result = transformation_engine.transform_entry(oracle_entry)

        assert transformation_result.success is True
        assert len(transformation_result.applied_rules) > 0

        transformed_entry = transformation_result.transformed_entry

        # Check DN transformation
        assert transformed_entry["dn"] == "cn=john.doe,ou=people,dc=network,dc=ctbc"

        # Check object class conversion
        assert "orclUser" not in transformed_entry["objectClass"]
        assert "inetOrgPerson" in transformed_entry["objectClass"]
        assert "person" in transformed_entry["objectClass"]

        # Check attribute mapping
        assert "orclSamAccountName" not in transformed_entry
        assert transformed_entry["uid"] == "john.doe"
        assert "orclCommonName" not in transformed_entry
        assert transformed_entry["cn"] == "John Doe"

        # Validate the transformed entry
        validation_result = validator.validate_entry(transformed_entry)

        assert validation_result["valid"] is True
        assert len(validation_result["errors"]) == 0

        # Should have minimal warnings for a well-formed entry
        assert len(validation_result["warnings"]) <= 1

    def test_classification_and_transformation_integration(self) -> None:
        config = {"enable_transformation": True}
        engine = DataTransformationEngine(config)

        # Test various entry types
        test_entries = [
            {
                "dn": "cn=oid,cn=oraclecontext,dc=example,dc=com",
                "objectClass": ["orclContext"],
                "expected_classification": "internal_oid",
            },
            {
                "dn": "cn=testuser,ou=people,dc=ctbc",
                "objectClass": ["orclUser"],
                "expected_classification": "oracle_user",
            },
            {
                "dn": "uid=standard.user,ou=people,dc=example,dc=com",
                "objectClass": ["inetOrgPerson"],
                "expected_classification": "business_data",
            },
        ]

        for entry_data in test_entries:
            entry = {
                k: v for k, v in entry_data.items() if k != "expected_classification"
            }

            result = engine.transform_entry(entry)

            assert result.success is True
            classification = result.metadata.get("classification")
            assert classification is not None
            assert classification.entry_type == entry_data["expected_classification"]
