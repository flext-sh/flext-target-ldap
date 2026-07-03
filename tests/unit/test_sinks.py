"""Tests for target-ldap sinks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from flext_target_ldap._models.sinks import (
    FlextTargetLdapBaseSink as LDAPBaseSink,
    FlextTargetLdapGroupsSink as GroupsSink,
    FlextTargetLdapOrganizationalUnitsSink as OrganizationalUnitsSink,
    FlextTargetLdapUsersSink as UsersSink,
)
from tests.typings import t


@pytest.fixture
def ldap_base_sink(mock_target: MagicMock) -> LDAPBaseSink:
    mock_target.settings = {**mock_target.settings, "base_dn": "dc=example,dc=com"}
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"dn": {"type": "string"}, "cn": {"type": "string"}},
    }
    return LDAPBaseSink(
        target=mock_target,
        stream_name="test_stream",
        schema=schema,
        key_properties=["dn"],
    )


@pytest.fixture
def users_sink(mock_target: MagicMock) -> UsersSink:
    mock_target.settings = {
        **mock_target.settings,
        "base_dn": "dc=example,dc=com",
        "user_rdn_attribute": "uid",
    }
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {
            "uid": {"type": "string"},
            "cn": {"type": "string"},
            "mail": {"type": "string"},
        },
    }
    return UsersSink(
        target=mock_target,
        stream_name="users",
        schema=schema,
        key_properties=["uid"],
    )


@pytest.fixture
def groups_sink(mock_target: MagicMock) -> GroupsSink:
    mock_target.settings = {
        **mock_target.settings,
        "base_dn": "dc=example,dc=com",
        "group_rdn_attribute": "cn",
    }
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"cn": {"type": "string"}, "member": {"type": "array"}},
    }
    return GroupsSink(
        target=mock_target,
        stream_name="groups",
        schema=schema,
        key_properties=["cn"],
    )


@pytest.fixture
def ou_sink(mock_target: MagicMock) -> OrganizationalUnitsSink:
    mock_target.settings = {**mock_target.settings, "base_dn": "dc=example,dc=com"}
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"ou": {"type": "string"}, "description": {"type": "string"}},
    }
    return OrganizationalUnitsSink(
        target=mock_target,
        stream_name="organizational_units",
        schema=schema,
        key_properties=["ou"],
    )


@pytest.fixture
def generic_sink(mock_target: MagicMock) -> LDAPBaseSink:
    mock_target.settings = {**mock_target.settings, "base_dn": "dc=example,dc=com"}
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"dn": {"type": "string"}, "cn": {"type": "string"}},
    }
    return LDAPBaseSink(
        target=mock_target,
        stream_name="generic",
        schema=schema,
        key_properties=["id"],
    )


class TestsFlextTargetLdapSinks:
    """Behavior contract for test_sinks."""

    def test_ldap_sink_initialization(self, ldap_base_sink: LDAPBaseSink) -> None:
        assert ldap_base_sink.stream_name == "test_stream"
        assert ldap_base_sink.key_properties == ["dn"]
        properties = ldap_base_sink.schema.get("properties")
        assert isinstance(properties, dict)
        assert "dn" in properties

    @pytest.mark.parametrize(
        ("record", "expected_error"),
        [
            ({"description": "no id fields"}, "must be implemented in subclass"),
            ({"cn": "test"}, "must be implemented in subclass"),
        ],
    )
    def test_base_sink_validation_failures(
        self,
        ldap_base_sink: LDAPBaseSink,
        record: t.TargetLdap.RecordPayload,
        expected_error: str,
    ) -> None:
        description = record.get("description")
        if isinstance(description, str) and "id fields" in description:
            result = ldap_base_sink.build_dn(record)
        else:
            result = ldap_base_sink.build_attributes(record)
        assert not result.success
        assert result.error is not None and expected_error in result.error

    def test_resolve_object_classes_default(self, ldap_base_sink: LDAPBaseSink) -> None:
        record: t.TargetLdap.RecordPayload = {}
        classes = ldap_base_sink.resolve_object_classes(record)
        assert classes == ["top"]

    def test_validate_entry_success(self, ldap_base_sink: LDAPBaseSink) -> None:
        mock_client = MagicMock()
        mock_client.validate_dn.return_value.success = True
        ldap_base_sink.client = mock_client
        result = ldap_base_sink.validate_entry(
            "cn=test,dc=example,dc=com", {"cn": ["test"]}, ["person", "top"]
        )
        assert result.success

    @pytest.mark.parametrize(
        ("dn", "attributes", "object_classes", "expected_message"),
        [
            ("", {"cn": ["test"]}, ["person"], "DN cannot be empty"),
            ("cn=test,dc=example,dc=com", {}, ["person"], "Attributes cannot be empty"),
            (
                "cn=test,dc=example,dc=com",
                {"cn": ["test"]},
                [],
                "Object classes cannot be empty",
            ),
        ],
    )
    def test_validate_entry_failure_cases(
        self,
        ldap_base_sink: LDAPBaseSink,
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: list[str],
        expected_message: str,
    ) -> None:
        result = ldap_base_sink.validate_entry(dn, attributes, object_classes)
        assert not result.success
        assert result.error is not None and expected_message in result.error

    def test_users_build_dn_success(self, users_sink: UsersSink) -> None:
        record = {"uid": "testuser", "cn": "Test User"}
        result = users_sink.build_dn(record)
        assert result.success
        assert result.value == "uid=testuser,dc=example,dc=com"

    def test_users_build_dn_missing_uid(self, users_sink: UsersSink) -> None:
        result = users_sink.build_dn({"cn": "Test User"})
        assert not result.success
        assert (
            result.error is not None
            and "No value found for RDN attribute 'uid'" in result.error
        )

    def test_users_build_attributes_basic(self, users_sink: UsersSink) -> None:
        result = users_sink.build_attributes({
            "uid": "testuser",
            "cn": "Test User",
            "mail": "test@example.com",
            "sn": "User",
            "givenName": "Test",
        })
        assert result.success
        assert result.value is not None
        assert result.value["uid"] == ["testuser"]
        assert result.value["cn"] == ["Test User"]
        assert result.value["mail"] == ["test@example.com"]
        assert result.value["sn"] == ["User"]
        assert result.value["givenName"] == ["Test"]

    def test_users_build_attributes_multivalued(self, users_sink: UsersSink) -> None:
        result = users_sink.build_attributes({
            "uid": "testuser",
            "emails": ["test1@example.com", "test2@example.com"],
            "phone_numbers": ["123-456-7890", "098-765-4321"],
        })
        assert result.success
        assert result.value is not None
        assert result.value["mail"] == ["test1@example.com", "test2@example.com"]
        assert result.value["telephoneNumber"] == ["123-456-7890", "098-765-4321"]

    def test_users_get_object_classes_default(self, users_sink: UsersSink) -> None:
        classes = users_sink.resolve_object_classes({})
        assert classes == ["inetOrgPerson", "organizationalPerson", "person", "top"]

    def test_users_get_object_classes_configured(self, mock_target: MagicMock) -> None:
        mock_target.settings = {
            **mock_target.settings,
            "base_dn": "dc=example,dc=com",
            "user_rdn_attribute": "uid",
            "users_object_classes": ["customUser", "top"],
        }
        sink = UsersSink(
            target=mock_target,
            stream_name="users",
            schema={
                "properties": {"uid": {"type": "string"}, "cn": {"type": "string"}}
            },
            key_properties=["uid"],
        )
        assert sink.resolve_object_classes({}) == ["customUser", "top"]

    def test_groups_build_dn_success(self, groups_sink: GroupsSink) -> None:
        result = groups_sink.build_dn({"cn": "testgroup", "description": "Test Group"})
        assert result.success
        assert result.value == "cn=testgroup,dc=example,dc=com"

    def test_groups_build_dn_missing_cn(self, groups_sink: GroupsSink) -> None:
        result = groups_sink.build_dn({"description": "Test Group"})
        assert not result.success
        assert (
            result.error is not None
            and "No value found for RDN attribute 'cn'" in result.error
        )

    def test_groups_build_attributes_basic(self, groups_sink: GroupsSink) -> None:
        result = groups_sink.build_attributes({
            "cn": "testgroup",
            "description": "Test Group",
            "members": ["uid=user1,dc=example,dc=com", "uid=user2,dc=example,dc=com"],
        })
        assert result.success
        assert result.value is not None
        assert result.value["cn"] == ["testgroup"]
        assert result.value["description"] == ["Test Group"]
        assert result.value["member"] == [
            "uid=user1,dc=example,dc=com",
            "uid=user2,dc=example,dc=com",
        ]

    def test_groups_get_object_classes_default(self, groups_sink: GroupsSink) -> None:
        assert groups_sink.resolve_object_classes({}) == ["groupOfNames", "top"]

    def test_ou_build_dn_success(self, ou_sink: OrganizationalUnitsSink) -> None:
        result = ou_sink.build_dn({"name": "testou", "description": "Test OU"})
        assert result.success
        assert "testou" in result.value

    def test_ou_build_dn_missing_ou(self, ou_sink: OrganizationalUnitsSink) -> None:
        result = ou_sink.build_dn({"description": "Test OU"})
        assert not result.success
        assert result.error is not None

    def test_ou_build_attributes_basic(self, ou_sink: OrganizationalUnitsSink) -> None:
        result = ou_sink.build_attributes({"ou": "testou", "description": "Test OU"})
        assert not result.success

    def test_ou_get_object_classes_default(
        self, ou_sink: OrganizationalUnitsSink
    ) -> None:
        assert "top" in ou_sink.resolve_object_classes({})

    def test_generic_build_dn_explicit(self, generic_sink: LDAPBaseSink) -> None:
        result = generic_sink.build_dn({"dn": "cn=test,dc=example,dc=com"})
        assert result.success
        assert result.value == "cn=test,dc=example,dc=com"

    def test_generic_build_dn_id_field(self, generic_sink: LDAPBaseSink) -> None:
        result = generic_sink.build_dn({"id": "testentry", "cn": "Test Entry"})
        assert result.success
        assert result.value == "cn=testentry,dc=example,dc=com"

    def test_generic_build_dn_no_identifier(self, generic_sink: LDAPBaseSink) -> None:
        result = generic_sink.build_dn({"description": "Test Entry"})
        assert not result.success
        assert (
            result.error is not None
            and "No ID or name found for generic entry" in result.error
        )

    def test_generic_build_attributes_basic(self, generic_sink: LDAPBaseSink) -> None:
        result = generic_sink.build_attributes({
            "id": "testentry",
            "cn": "Test Entry",
            "description": "A test entry",
        })
        assert not result.success
        assert (
            result.error is not None
            and "must be implemented in subclass" in result.error
        )

    def test_generic_get_object_classes_from_record(
        self, generic_sink: LDAPBaseSink
    ) -> None:
        assert generic_sink.resolve_object_classes({
            "object_classes": ["customClass", "top"]
        }) == ["customClass", "top"]

    def test_generic_get_object_classes_single_value(
        self, generic_sink: LDAPBaseSink
    ) -> None:
        assert generic_sink.resolve_object_classes({
            "object_classes": "customClass"
        }) == ["customClass"]

    def test_generic_get_object_classes_default(
        self, generic_sink: LDAPBaseSink
    ) -> None:
        assert generic_sink.resolve_object_classes({}) == ["top"]

    def test_generic_get_object_classes_configured(
        self, mock_target: MagicMock
    ) -> None:
        mock_target.settings = {
            **mock_target.settings,
            "base_dn": "dc=example,dc=com",
            "generic_object_classes": ["customGeneric", "top"],
        }
        sink = LDAPBaseSink(
            target=mock_target,
            stream_name="generic",
            schema={"properties": {"dn": {"type": "string"}, "cn": {"type": "string"}}},
            key_properties=["id"],
        )
        classes = sink.resolve_object_classes({})
        assert classes == ["customGeneric", "top"]
