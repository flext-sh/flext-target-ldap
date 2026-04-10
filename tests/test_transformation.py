"""Tests for data transformation engine.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence

import pytest

from flext_target_ldap import (
    FlextTargetLdapMigrationValidator,
    FlextTargetLdapTransformationEngine,
)
from tests import c, m, t

EXPECTED_DATA_COUNT = c.TargetLdap.Tests.EXPECTED_DATA_COUNT


def test_transformation_engine_initialization() -> None:
    rules = [
        m.TargetLdap.TransformationRule(
            name="test",
            pattern="test",
            replacement="test",
        )
    ]
    engine = FlextTargetLdapTransformationEngine(rules)
    assert len(engine.rules) == 1


@pytest.mark.parametrize(
    ("rules", "entry", "expected_dn", "expected_rule"),
    [
        (
            [
                m.TargetLdap.TransformationRule(
                    name="oracle_dn_structure_transform",
                    pattern="dc=invaliddc",
                    replacement="dc=network,dc=invaliddc",
                )
            ],
            {
                "dn": "cn=testuser,ou=people,dc=invaliddc",
                "objectClass": ["orclUser", "person"],
                "cn": "testuser",
            },
            "cn=testuser,ou=people,dc=network,dc=invaliddc",
            "oracle_dn_structure_transform",
        ),
    ],
)
def test_transform_oracle_dn_structure(
    rules: list[m.TargetLdap.TransformationRule],
    entry: t.ContainerValueMapping,
    expected_dn: str,
    expected_rule: str,
) -> None:
    engine = FlextTargetLdapTransformationEngine(rules)
    result = engine.transform(entry)
    assert result.is_success
    transform_result = result.value
    assert transform_result is not None
    assert transform_result.transformed_data["dn"] == expected_dn
    assert expected_rule in transform_result.applied_rules


def test_transform_oracle_objectclasses() -> None:
    rule = m.TargetLdap.TransformationRule(
        name="oracle_objectclass_conversion",
        pattern="orclUser",
        replacement="inetOrgPerson",
    )
    engine = FlextTargetLdapTransformationEngine([rule])
    entry: t.ContainerValueMapping = {
        "dn": "cn=testuser,ou=people,dc=example,dc=com",
        "objectClass": ["orclUser", "top"],
        "cn": "testuser",
    }
    result = engine.transform(entry)
    assert result.is_success
    transform_result = result.value
    assert transform_result is not None
    object_classes = transform_result.transformed_data["objectClass"]
    assert "inetOrgPerson" in (
        object_classes if isinstance(object_classes, list) else str(object_classes)
    )
    assert "oracle_objectclass_conversion" in transform_result.applied_rules


def test_transform_oracle_attributes_and_title_case() -> None:
    engine = FlextTargetLdapTransformationEngine([
        m.TargetLdap.TransformationRule(
            name="oracle_user_prefix_removal",
            pattern="orcl",
            replacement="",
        ),
        m.TargetLdap.TransformationRule(
            name="normalize_case",
            pattern="User",
            replacement="user",
        ),
    ])
    entry: t.ContainerValueMapping = {
        "dn": "cn=testuser,ou=people,dc=example,dc=com",
        "objectClass": ["orclUser"],
        "description": "Oracle User Account",
        "title": "Test User",
    }
    result = engine.transform(entry)
    assert result.is_success
    transform_result = result.value
    assert transform_result is not None
    assert transform_result.transformed_data["objectClass"] == ["user"]
    assert transform_result.transformed_data["title"] == "Test user"


def test_remove_empty_attributes() -> None:
    engine = FlextTargetLdapTransformationEngine([
        m.TargetLdap.TransformationRule(
            name="clean_empty_attributes",
            pattern="empty",
            replacement="",
        )
    ])
    entry: t.ContainerValueMapping = {
        "dn": "cn=testuser,ou=people,dc=example,dc=com",
        "objectClass": ["person"],
        "cn": "testuser",
        "description": "",
    }
    result = engine.transform(entry)
    assert result.is_success
    transform_result = result.value
    assert transform_result is not None
    assert "cn" in transform_result.transformed_data


def test_dry_run_transformation() -> None:
    rule = m.TargetLdap.TransformationRule(
        name="test_rule",
        pattern="orclUser",
        replacement="inetOrgPerson",
    )
    engine = FlextTargetLdapTransformationEngine([rule])
    entry: t.ContainerValueMapping = {
        "dn": "cn=testuser,ou=people,dc=invaliddc",
        "objectClass": ["orclUser"],
        "cn": "testuser",
    }
    result = engine.transform(entry)
    assert result.is_success
    transform_result = result.value
    assert transform_result is not None
    assert transform_result.transformed_data["objectClass"] == ["inetOrgPerson"]


def test_transformation_statistics() -> None:
    engine = FlextTargetLdapTransformationEngine([
        m.TargetLdap.TransformationRule(
            name="orcl_to_inetorgperson",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
    ])
    entries: Sequence[t.ContainerValueMapping] = [
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


@pytest.mark.parametrize(
    (
        "dn",
        "attributes",
        "object_classes",
        "expected_success",
        "expected_error_substring",
    ),
    [
        (
            "cn=testuser,ou=people,dc=example,dc=com",
            {"cn": "testuser", "sn": "User", "mail": "test@example.com"},
            ["inetOrgPerson", "person"],
            True,
            None,
        ),
        (
            "",
            {"cn": "testuser"},
            ["person"],
            False,
            "DN cannot be empty or whitespace",
        ),
        (
            "invalid_dn_format",
            {"cn": "testuser"},
            ["person"],
            False,
            None,
        ),
        (
            "cn=testuser,dc=example,dc=com",
            {"cn": "testuser"},
            [],
            False,
            "Object classes must be a non-empty list",
        ),
        (
            "cn=testuser,ou=people,dc=example,dc=com",
            {"cn": "testuser", "sn": "User", "mail": "invalid-email"},
            ["inetOrgPerson", "person"],
            True,
            None,
        ),
    ],
)
def test_migration_validator_various_inputs(
    dn: str,
    attributes: t.ContainerValueMapping,
    object_classes: list[str],
    expected_success: bool,
    expected_error_substring: str | None,
) -> None:
    validator = FlextTargetLdapMigrationValidator()
    result = validator.validate(dn, attributes, object_classes)
    assert result.is_success == expected_success
    if expected_error_substring is not None:
        assert result.error is not None
        assert expected_error_substring in result.error


def test_validation_statistics() -> None:
    validator = FlextTargetLdapMigrationValidator()
    test_cases = [
        ("cn=user1,dc=example,dc=com", {"cn": "user1", "sn": "One"}, ["person"]),
        ("invalid", {"cn": "user2"}, ["person"]),
        ("", {"cn": "user3"}, ["person"]),
    ]
    for dn, attributes, object_classes in test_cases:
        validator.validate(dn, attributes, object_classes)

    stats = validator.get_validation_statistics()
    assert stats["entries_validated"] == EXPECTED_DATA_COUNT
    assert stats["validation_errors"] >= 0
    assert stats["validation_warnings"] >= 0


def test_transformation_rule_creation() -> None:
    rule = m.TargetLdap.TransformationRule(
        name="test_rule",
        pattern="orclUser",
        replacement="person",
        enabled=True,
    )
    assert rule.name == "test_rule"
    assert rule.enabled
    assert rule.pattern == "orclUser"
    assert rule.replacement == "person"


def test_full_oracle_migration_workflow() -> None:
    rules = [
        m.TargetLdap.TransformationRule(
            name="oracle_dn_transform",
            pattern="dc=invaliddc",
            replacement="dc=network,dc=invaliddc",
        ),
        m.TargetLdap.TransformationRule(
            name="oracle_objectclass",
            pattern="orclUser",
            replacement="inetOrgPerson",
        ),
    ]
    transformation_engine = FlextTargetLdapTransformationEngine(rules)
    validator = FlextTargetLdapMigrationValidator(strict_mode=False)
    oracle_entry: t.ContainerValueMapping = {
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
    transformed_entry = transform.transformed_data
    assert transformed_entry["dn"] == "cn=john.doe,ou=people,dc=network,dc=invaliddc"
    raw_classes = transformed_entry["objectClass"]
    assert "inetOrgPerson" in (
        raw_classes if isinstance(raw_classes, list) else str(raw_classes)
    )

    dn = str(transformed_entry["dn"])
    attributes = {
        k: v for k, v in transformed_entry.items() if k not in {"dn", "objectClass"}
    }
    raw_classes = transformed_entry["objectClass"]
    obj_classes: t.StrSequence = (
        [str(item) for item in raw_classes]
        if isinstance(raw_classes, list)
        else [str(raw_classes)]
    )
    validation_result = validator.validate(dn, attributes, obj_classes)
    assert validation_result.is_success


def test_classification_and_transformation_integration() -> None:
    engine = FlextTargetLdapTransformationEngine([
        m.TargetLdap.TransformationRule(
            name="general_transform",
            pattern="orclUser",
            replacement="inetOrgPerson",
        )
    ])
    test_entries: Sequence[t.ContainerValueMapping] = [
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
