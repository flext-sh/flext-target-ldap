"""Tests for target-ldap sinks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from tests import m

if TYPE_CHECKING:
    from tests import t


def _update_target_settings(
    target: m.TargetLdap.Target,
    updates: t.TargetLdap.SettingsPayload,
) -> None:
    """Merge one settings update into the target's settings payload."""
    target.settings = {**target.settings, **updates}


@pytest.fixture
def ldap_base_sink(ldap_target: m.TargetLdap.Target) -> m.TargetLdap.BaseSink:
    """Provide ``ldap_base_sink``.

    Returns:
        The resulting ``m.TargetLdap.BaseSink``.
    """
    ldap_target.settings = {**ldap_target.settings, "base_dn": "dc=example,dc=com"}
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"dn": {"type": "string"}, "cn": {"type": "string"}},
    }
    return m.TargetLdap.BaseSink(
        target=ldap_target,
        stream_name="test_stream",
        schema=schema,
        key_properties=["dn"],
    )


@pytest.fixture
def users_sink(ldap_target: m.TargetLdap.Target) -> m.TargetLdap.UsersSink:
    """Provide ``users_sink``.

    Returns:
        The resulting ``m.TargetLdap.UsersSink``.
    """
    ldap_target.settings = {
        **ldap_target.settings,
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
    return m.TargetLdap.UsersSink(
        target=ldap_target,
        stream_name="users",
        schema=schema,
        key_properties=["uid"],
    )


@pytest.fixture
def groups_sink(ldap_target: m.TargetLdap.Target) -> m.TargetLdap.GroupsSink:
    """Provide ``groups_sink``.

    Returns:
        The resulting ``m.TargetLdap.GroupsSink``.
    """
    ldap_target.settings = {
        **ldap_target.settings,
        "base_dn": "dc=example,dc=com",
        "group_rdn_attribute": "cn",
    }
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"cn": {"type": "string"}, "member": {"type": "array"}},
    }
    return m.TargetLdap.GroupsSink(
        target=ldap_target,
        stream_name="groups",
        schema=schema,
        key_properties=["cn"],
    )


@pytest.fixture
def ou_sink(ldap_target: m.TargetLdap.Target) -> m.TargetLdap.OrganizationalUnitsSink:
    """Provide ``ou_sink``.

    Returns:
        The resulting ``m.TargetLdap.OrganizationalUnitsSink``.
    """
    ldap_target.settings = {**ldap_target.settings, "base_dn": "dc=example,dc=com"}
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"ou": {"type": "string"}, "description": {"type": "string"}},
    }
    return m.TargetLdap.OrganizationalUnitsSink(
        target=ldap_target,
        stream_name="organizational_units",
        schema=schema,
        key_properties=["ou"],
    )


@pytest.fixture
def generic_sink(ldap_target: m.TargetLdap.Target) -> m.TargetLdap.BaseSink:
    """Provide ``generic_sink``.

    Returns:
        The resulting ``m.TargetLdap.BaseSink``.
    """
    ldap_target.settings = {**ldap_target.settings, "base_dn": "dc=example,dc=com"}
    schema: t.TargetLdap.SchemaPayload = {
        "properties": {"dn": {"type": "string"}, "cn": {"type": "string"}},
    }
    return m.TargetLdap.BaseSink(
        target=ldap_target,
        stream_name="generic",
        schema=schema,
        key_properties=["id"],
    )


class TestsFlextTargetLdapSinks:
    """Behavior contract for test_sinks."""

    @staticmethod
    def test_ldap_sink_initialization(
        ldap_base_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test ldap sink initialization."""
        tm.that(ldap_base_sink.stream_name, eq="test_stream")
        tm.that(ldap_base_sink.key_properties, eq=["dn"])
        properties = ldap_base_sink.schema.get("properties")
        tm.that(properties, is_=dict)
        tm.that(properties, has="dn")

    @staticmethod
    @pytest.mark.parametrize(
        ("record", "expected_error"),
        [
            ({"description": "no id fields"}, "must be implemented in subclass"),
            ({"cn": "test"}, "must be implemented in subclass"),
        ],
    )
    def test_base_sink_validation_failures(
        ldap_base_sink: m.TargetLdap.BaseSink,
        record: t.TargetLdap.RecordPayload,
        expected_error: str,
    ) -> None:
        """Test base sink validation failures."""
        description = record.get("description")
        if isinstance(description, str) and "id fields" in description:
            result = ldap_base_sink.build_dn(record)
        else:
            result = ldap_base_sink.build_attributes(record)
        assert result.failure
        assert result.error is not None
        assert expected_error in result.error

    @staticmethod
    def test_resolve_object_classes_default(
        ldap_base_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test resolve object classes default."""
        record: t.TargetLdap.RecordPayload = {}
        classes = ldap_base_sink.resolve_object_classes(record)
        tm.that(classes, eq=["top"])

    @staticmethod
    def test_validate_entry_success(
        ldap_base_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test validate entry success."""
        result = ldap_base_sink.validate_entry(
            "cn=test,dc=example,dc=com",
            {"cn": ["test"]},
            ["person", "top"],
        )
        tm.ok(result)

    @staticmethod
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
        ldap_base_sink: m.TargetLdap.BaseSink,
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: list[str],
        expected_message: str,
    ) -> None:
        """Test validate entry failure cases."""
        result = ldap_base_sink.validate_entry(dn, attributes, object_classes)
        tm.fail(result)
        assert result.error is not None
        assert expected_message in result.error

    @staticmethod
    def test_users_build_dn_success(users_sink: m.TargetLdap.UsersSink) -> None:
        """Test users build dn success."""
        record = {"uid": "testuser", "cn": "Test User"}
        result = users_sink.build_dn(record)
        tm.ok(result)
        tm.that(result.value, eq="uid=testuser,dc=example,dc=com")

    @staticmethod
    def test_users_build_dn_missing_uid(
        users_sink: m.TargetLdap.UsersSink,
    ) -> None:
        """Test users build dn missing uid."""
        result = users_sink.build_dn({"cn": "Test User"})
        tm.fail(result)
        assert result.error is not None
        assert "No value found for RDN attribute 'uid'" in result.error

    @staticmethod
    def test_users_build_attributes_basic(
        users_sink: m.TargetLdap.UsersSink,
    ) -> None:
        """Test users build attributes basic."""
        result = users_sink.build_attributes({
            "uid": "testuser",
            "cn": "Test User",
            "mail": "test@example.com",
            "sn": "User",
            "givenName": "Test",
        })
        tm.ok(result)
        tm.that(result.value, none=False)
        tm.that(result.value["uid"], eq=["testuser"])
        tm.that(result.value["cn"], eq=["Test User"])
        tm.that(result.value["mail"], eq=["test@example.com"])
        tm.that(result.value["sn"], eq=["User"])
        tm.that(result.value["givenName"], eq=["Test"])

    @staticmethod
    def test_users_build_attributes_multivalued(
        users_sink: m.TargetLdap.UsersSink,
    ) -> None:
        """Test users build attributes multivalued."""
        result = users_sink.build_attributes({
            "uid": "testuser",
            "emails": ["test1@example.com", "test2@example.com"],
            "phone_numbers": ["123-456-7890", "098-765-4321"],
        })
        tm.ok(result)
        tm.that(result.value, none=False)
        tm.that(result.value["mail"], eq=["test1@example.com", "test2@example.com"])
        tm.that(result.value["telephoneNumber"], eq=["123-456-7890", "098-765-4321"])

    @staticmethod
    def test_users_get_object_classes_default(
        users_sink: m.TargetLdap.UsersSink,
    ) -> None:
        """Test users get object classes default."""
        classes = users_sink.resolve_object_classes({})
        tm.that(classes, eq=["inetOrgPerson", "organizationalPerson", "person", "top"])

    @staticmethod
    def test_users_get_object_classes_configured(
        ldap_target: m.TargetLdap.Target,
    ) -> None:
        """Test users get object classes configured."""
        _update_target_settings(
            ldap_target,
            {
                "base_dn": "dc=example,dc=com",
                "user_rdn_attribute": "uid",
                "users_object_classes": ["customUser", "top"],
            },
        )
        sink = m.TargetLdap.UsersSink(
            target=ldap_target,
            stream_name="users",
            schema={
                "properties": {"uid": {"type": "string"}, "cn": {"type": "string"}},
            },
            key_properties=["uid"],
        )
        tm.that(sink.resolve_object_classes({}), eq=["customUser", "top"])

    @staticmethod
    def test_groups_build_dn_success(
        groups_sink: m.TargetLdap.GroupsSink,
    ) -> None:
        """Test groups build dn success."""
        result = groups_sink.build_dn({"cn": "testgroup", "description": "Test Group"})
        tm.ok(result)
        tm.that(result.value, eq="cn=testgroup,dc=example,dc=com")

    @staticmethod
    def test_groups_build_dn_missing_cn(
        groups_sink: m.TargetLdap.GroupsSink,
    ) -> None:
        """Test groups build dn missing cn."""
        result = groups_sink.build_dn({"description": "Test Group"})
        tm.fail(result)
        assert result.error is not None
        assert "No value found for RDN attribute 'cn'" in result.error

    @staticmethod
    def test_groups_build_attributes_basic(
        groups_sink: m.TargetLdap.GroupsSink,
    ) -> None:
        """Test groups build attributes basic."""
        result = groups_sink.build_attributes({
            "cn": "testgroup",
            "description": "Test Group",
            "members": ["uid=user1,dc=example,dc=com", "uid=user2,dc=example,dc=com"],
        })
        tm.ok(result)
        tm.that(result.value, none=False)
        tm.that(result.value["cn"], eq=["testgroup"])
        tm.that(result.value["description"], eq=["Test Group"])
        tm.that(
            result.value["member"],
            eq=["uid=user1,dc=example,dc=com", "uid=user2,dc=example,dc=com"],
        )

    @staticmethod
    def test_groups_get_object_classes_default(
        groups_sink: m.TargetLdap.GroupsSink,
    ) -> None:
        """Test groups get object classes default."""
        tm.that(groups_sink.resolve_object_classes({}), eq=["groupOfNames", "top"])

    @staticmethod
    def test_ou_build_dn_success(
        ou_sink: m.TargetLdap.OrganizationalUnitsSink,
    ) -> None:
        """Test ou build dn success."""
        result = ou_sink.build_dn({"name": "testou", "description": "Test OU"})
        tm.ok(result)
        tm.that(result.value, has="testou")

    @staticmethod
    def test_ou_build_dn_missing_ou(
        ou_sink: m.TargetLdap.OrganizationalUnitsSink,
    ) -> None:
        """Test ou build dn missing ou."""
        result = ou_sink.build_dn({"description": "Test OU"})
        tm.fail(result)
        tm.that(result.error, none=False)

    @staticmethod
    def test_ou_build_attributes_basic(
        ou_sink: m.TargetLdap.OrganizationalUnitsSink,
    ) -> None:
        """Test ou build attributes basic."""
        result = ou_sink.build_attributes({"ou": "testou", "description": "Test OU"})
        tm.fail(result)

    @staticmethod
    def test_ou_get_object_classes_default(
        ou_sink: m.TargetLdap.OrganizationalUnitsSink,
    ) -> None:
        """Test ou get object classes default."""
        tm.that(ou_sink.resolve_object_classes({}), has="top")

    @staticmethod
    def test_generic_build_dn_explicit(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic build dn explicit."""
        result = generic_sink.build_dn({"dn": "cn=test,dc=example,dc=com"})
        tm.ok(result)
        tm.that(result.value, eq="cn=test,dc=example,dc=com")

    @staticmethod
    def test_generic_build_dn_id_field(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic build dn id field."""
        result = generic_sink.build_dn({"id": "testentry", "cn": "Test Entry"})
        tm.ok(result)
        tm.that(result.value, eq="cn=testentry,dc=example,dc=com")

    @staticmethod
    def test_generic_build_dn_no_identifier(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic build dn no identifier."""
        result = generic_sink.build_dn({"description": "Test Entry"})
        tm.fail(result)
        assert result.error is not None
        assert "No ID or name found for generic entry" in result.error

    @staticmethod
    def test_generic_build_attributes_basic(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic build attributes basic."""
        result = generic_sink.build_attributes({
            "id": "testentry",
            "cn": "Test Entry",
            "description": "A test entry",
        })
        tm.fail(result)
        assert result.error is not None
        assert "must be implemented in subclass" in result.error

    @staticmethod
    def test_generic_get_object_classes_from_record(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic get object classes from record."""
        tm.that(
            generic_sink.resolve_object_classes({
                "object_classes": ["customClass", "top"],
            }),
            eq=["customClass", "top"],
        )

    @staticmethod
    def test_generic_get_object_classes_single_value(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic get object classes single value."""
        tm.that(
            generic_sink.resolve_object_classes({"object_classes": "customClass"}),
            eq=["customClass"],
        )

    @staticmethod
    def test_generic_get_object_classes_default(
        generic_sink: m.TargetLdap.BaseSink,
    ) -> None:
        """Test generic get object classes default."""
        tm.that(generic_sink.resolve_object_classes({}), eq=["top"])

    @staticmethod
    def test_generic_get_object_classes_configured(
        ldap_target: m.TargetLdap.Target,
    ) -> None:
        """Test generic get object classes configured."""
        _update_target_settings(
            ldap_target,
            {
                "base_dn": "dc=example,dc=com",
                "generic_object_classes": ["customGeneric", "top"],
            },
        )
        sink = m.TargetLdap.BaseSink(
            target=ldap_target,
            stream_name="generic",
            schema={"properties": {"dn": {"type": "string"}, "cn": {"type": "string"}}},
            key_properties=["id"],
        )
        classes = sink.resolve_object_classes({})
        tm.that(classes, eq=["customGeneric", "top"])
