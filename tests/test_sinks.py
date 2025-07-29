"""Tests for target-ldap sinks."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from flext_target_ldap.sinks import (
    GenericSink,
    GroupsSink,
    LDAPSink,
    OrganizationalUnitsSink,
    UsersSink,
)


class TestLDAPSink:
    """Test base LDAP sink."""

    @pytest.fixture
    def sink(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> LDAPSink:
        schema = {
            "properties": {
                "dn": {"type": "string"},
                "cn": {"type": "string"},
            },
        }
        return LDAPSink(
            target=mock_target,
            stream_name="test_stream",
            schema=schema,
            key_properties=["dn"],
        )

    def test_sink_initialization(self, sink: LDAPSink) -> None:
        if sink.stream_name != "test_stream":
            raise AssertionError(f"Expected {"test_stream"}, got {sink.stream_name}")
        assert sink.key_properties == ["dn"]
        if "dn" not in sink.schema["properties"]:
            raise AssertionError(f"Expected {"dn"} in {sink.schema["properties"]}")

    def test_build_dn_not_implemented(self, sink: LDAPSink) -> None:
        record = {"cn": "test"}
        result = sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "must be implemented in subclass" not in result.error:
            raise AssertionError(f"Expected {"must be implemented in subclass"} in {result.error}")

    def test_build_attributes_not_implemented(self, sink: LDAPSink) -> None:
        record = {"cn": "test"}
        result = sink.build_attributes(record)
        assert not result.success
        assert result.error is not None
        if "must be implemented in subclass" not in result.error:
            raise AssertionError(f"Expected {"must be implemented in subclass"} in {result.error}")

    def test_get_object_classes_default(self, sink: LDAPSink) -> None:
        record: dict[str, Any] = {}
        classes = sink.get_object_classes(record)
        if classes != ["top"]:
            raise AssertionError(f"Expected {["top"]}, got {classes}")

    def test_validate_entry_success(self, sink: LDAPSink) -> None:
        # Mock the private _client attribute since client is a property
        mock_client = MagicMock()
        mock_client.validate_dn.return_value.is_success = True
        sink._client = mock_client

        result = sink.validate_entry(
            "cn=test,dc=example,dc=com",
            {"cn": ["test"]},
            ["person", "top"],
        )
        assert result.success

    def test_validate_entry_empty_dn(self, sink: LDAPSink) -> None:
        result = sink.validate_entry("", {"cn": ["test"]}, ["person"])
        assert not result.success
        assert result.error is not None
        if "DN cannot be empty" not in result.error:
            raise AssertionError(f"Expected {"DN cannot be empty"} in {result.error}")

    def test_validate_entry_empty_attributes(self, sink: LDAPSink) -> None:
        result = sink.validate_entry("cn=test,dc=example,dc=com", {}, ["person"])
        assert not result.success
        assert result.error is not None
        if "Attributes cannot be empty" not in result.error:
            raise AssertionError(f"Expected {"Attributes cannot be empty"} in {result.error}")

    def test_validate_entry_empty_object_classes(self, sink: LDAPSink) -> None:
        result = sink.validate_entry("cn=test,dc=example,dc=com", {"cn": ["test"]}, [])
        assert not result.success
        assert result.error is not None
        if "Object classes cannot be empty" not in result.error:
            raise AssertionError(f"Expected {"Object classes cannot be empty"} in {result.error}")


class TestUsersSink:
    """Test Users sink."""

    @pytest.fixture
    def users_sink(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> UsersSink:
        mock_target.config.update(
            {
                "base_dn": "dc=example,dc=com",
                "user_rdn_attribute": "uid",
            },
        )
        schema = {
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

    def test_build_dn_with_uid(self, users_sink: UsersSink) -> None:
        record = {"uid": "testuser", "cn": "Test User"}
        result = users_sink.build_dn(record)
        assert result.success
        if result.data != "uid=testuser,dc=example,dc=com":
            raise AssertionError(f"Expected {"uid=testuser,dc=example,dc=com"}, got {result.data}")

    def test_build_dn_missing_uid(self, users_sink: UsersSink) -> None:
        record = {"cn": "Test User"}
        result = users_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No value found for RDN attribute 'uid'" not in result.error:
            raise AssertionError(f"Expected {"No value found for RDN attribute 'uid'"} in {result.error}")

    def test_build_attributes_basic(self, users_sink: UsersSink) -> None:
        record = {
            "uid": "testuser",
            "cn": "Test User",
            "mail": "test@example.com",
            "sn": "User",
            "givenName": "Test",
        }
        result = users_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["uid"] != ["testuser"]:
            raise AssertionError(f"Expected {["testuser"]}, got {result.data["uid"]}")
        assert result.data["cn"] == ["Test User"]
        if result.data["mail"] != ["test@example.com"]:
            raise AssertionError(f"Expected {["test@example.com"]}, got {result.data["mail"]}")
        assert result.data["sn"] == ["User"]
        if result.data["givenName"] != ["Test"]:
            raise AssertionError(f"Expected {["Test"]}, got {result.data["givenName"]}")

    def test_build_attributes_multi_valued(self, users_sink: UsersSink) -> None:
        record = {
            "uid": "testuser",
            "emails": ["test1@example.com", "test2@example.com"],
            "phone_numbers": ["123-456-7890", "098-765-4321"],
        }
        result = users_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["uid"] != ["testuser"]:
            raise AssertionError(f"Expected {["testuser"]}, got {result.data["uid"]}")
        assert result.data["mail"] == ["test1@example.com", "test2@example.com"]
        if result.data["telephoneNumber"] != ["123-456-7890", "098-765-4321"]:
            raise AssertionError(f"Expected {["123-456-7890", "098-765-4321"]}, got {result.data["telephoneNumber"]}")

    def test_get_object_classes_default(self, users_sink: UsersSink) -> None:
        record: dict[str, Any] = {}
        classes = users_sink.get_object_classes(record)
        if classes != ["inetOrgPerson", "organizationalPerson", "person", "top"]:
            raise AssertionError(f"Expected {["inetOrgPerson", "organizationalPerson", "person", "top"]}, got {classes}")

    def test_get_object_classes_configured(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> None:
        # Create target with custom config
        mock_target.config.update(
            {
                "base_dn": "dc=example,dc=com",
                "user_rdn_attribute": "uid",
                "users_object_classes": ["customUser", "top"],
            },
        )
        schema = {
            "properties": {
                "uid": {"type": "string"},
                "cn": {"type": "string"},
            },
        }
        users_sink = UsersSink(
            target=mock_target,
            stream_name="users",
            schema=schema,
            key_properties=["uid"],
        )
        record: dict[str, Any] = {}
        classes = users_sink.get_object_classes(record)
        if classes != ["customUser", "top"]:
            raise AssertionError(f"Expected {["customUser", "top"]}, got {classes}")


class TestGroupsSink:
    """Test Groups sink."""

    @pytest.fixture
    def groups_sink(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> GroupsSink:
        mock_target.config.update(
            {
                "base_dn": "dc=example,dc=com",
                "group_rdn_attribute": "cn",
            },
        )
        schema = {
            "properties": {
                "cn": {"type": "string"},
                "member": {"type": "array"},
            },
        }
        return GroupsSink(
            target=mock_target,
            stream_name="groups",
            schema=schema,
            key_properties=["cn"],
        )

    def test_build_dn_with_cn(self, groups_sink: GroupsSink) -> None:
        record = {"cn": "testgroup", "description": "Test Group"}
        result = groups_sink.build_dn(record)
        assert result.success
        if result.data != "cn=testgroup,dc=example,dc=com":
            raise AssertionError(f"Expected {"cn=testgroup,dc=example,dc=com"}, got {result.data}")

    def test_build_dn_missing_cn(self, groups_sink: GroupsSink) -> None:
        record = {"description": "Test Group"}
        result = groups_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No value found for RDN attribute 'cn'" not in result.error:
            raise AssertionError(f"Expected {"No value found for RDN attribute 'cn'"} in {result.error}")

    def test_build_attributes_basic(self, groups_sink: GroupsSink) -> None:
        record = {
            "cn": "testgroup",
            "description": "Test Group",
            "members": ["uid=user1,dc=example,dc=com", "uid=user2,dc=example,dc=com"],
        }
        result = groups_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["cn"] != ["testgroup"]:
            raise AssertionError(f"Expected {["testgroup"]}, got {result.data["cn"]}")
        assert result.data["description"] == ["Test Group"]
        expected_members = [
            "uid=user1,dc=example,dc=com",
            "uid=user2,dc=example,dc=com",
        ]
        if result.data["member"] != expected_members:
            raise AssertionError(f"Expected {expected_members}, got {result.data['member']}")

    def test_get_object_classes_default(self, groups_sink: GroupsSink) -> None:
        record: dict[str, Any] = {}
        classes = groups_sink.get_object_classes(record)
        if classes != ["groupOfNames", "top"]:
            raise AssertionError(f"Expected {["groupOfNames", "top"]}, got {classes}")


class TestOrganizationalUnitsSink:
    """Test Organizational Units sink."""

    @pytest.fixture
    def ou_sink(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> OrganizationalUnitsSink:
        mock_target.config.update(
            {
                "base_dn": "dc=example,dc=com",
            },
        )
        schema = {
            "properties": {
                "ou": {"type": "string"},
                "description": {"type": "string"},
            },
        }
        return OrganizationalUnitsSink(
            target=mock_target,
            stream_name="organizational_units",
            schema=schema,
            key_properties=["ou"],
        )

    def test_build_dn_with_ou(self, ou_sink: OrganizationalUnitsSink) -> None:
        record = {"ou": "testou", "description": "Test OU"}
        result = ou_sink.build_dn(record)
        assert result.success
        if result.data != "ou=testou,dc=example,dc=com":
            raise AssertionError(f"Expected {"ou=testou,dc=example,dc=com"}, got {result.data}")

    def test_build_dn_missing_ou(self, ou_sink: OrganizationalUnitsSink) -> None:
        record = {"description": "Test OU"}
        result = ou_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No OU name found in record" not in result.error:
            raise AssertionError(f"Expected {"No OU name found in record"} in {result.error}")

    def test_build_attributes_basic(self, ou_sink: OrganizationalUnitsSink) -> None:
        record = {
            "ou": "testou",
            "description": "Test OU",
            "telephoneNumber": "123-456-7890",
            "street": "123 Test St",
            "l": "Test City",
            "st": "Test State",
            "postalCode": "12345",
        }
        result = ou_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["ou"] != ["testou"]:
            raise AssertionError(f"Expected {["testou"]}, got {result.data["ou"]}")
        assert result.data["description"] == ["Test OU"]
        if result.data["telephoneNumber"] != ["123-456-7890"]:
            raise AssertionError(f"Expected {["123-456-7890"]}, got {result.data["telephoneNumber"]}")
        assert result.data["street"] == ["123 Test St"]
        if result.data["l"] != ["Test City"]:
            raise AssertionError(f"Expected {["Test City"]}, got {result.data["l"]}")
        assert result.data["st"] == ["Test State"]
        if result.data["postalCode"] != ["12345"]:
            raise AssertionError(f"Expected {["12345"]}, got {result.data["postalCode"]}")

    def test_get_object_classes_default(self, ou_sink: OrganizationalUnitsSink) -> None:
        record: dict[str, Any] = {}
        classes = ou_sink.get_object_classes(record)
        if classes != ["organizationalUnit", "top"]:
            raise AssertionError(f"Expected {["organizationalUnit", "top"]}, got {classes}")


class TestGenericSink:
    """Test Generic sink."""

    @pytest.fixture
    def generic_sink(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> GenericSink:
        mock_target.config.update(
            {
                "base_dn": "dc=example,dc=com",
            },
        )
        schema = {
            "properties": {
                "dn": {"type": "string"},
                "cn": {"type": "string"},
            },
        }
        return GenericSink(
            target=mock_target,
            stream_name="generic",
            schema=schema,
            key_properties=["id"],
        )

    def test_build_dn_with_dn_field(self, generic_sink: GenericSink) -> None:
        record = {"dn": "cn=test,dc=example,dc=com"}
        result = generic_sink.build_dn(record)
        assert result.success
        if result.data != "cn=test,dc=example,dc=com":
            raise AssertionError(f"Expected {"cn=test,dc=example,dc=com"}, got {result.data}")

    def test_build_dn_with_id(self, generic_sink: GenericSink) -> None:
        record = {"id": "testentry", "cn": "Test Entry"}
        result = generic_sink.build_dn(record)
        assert result.success
        if result.data != "cn=testentry,dc=example,dc=com":
            raise AssertionError(f"Expected {"cn=testentry,dc=example,dc=com"}, got {result.data}")

    def test_build_dn_missing_identifier(self, generic_sink: GenericSink) -> None:
        record = {"description": "Test Entry"}
        result = generic_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No ID or name found for generic entry" not in result.error:
            raise AssertionError(f"Expected {"No ID or name found for generic entry"} in {result.error}")

    def test_build_attributes_basic(self, generic_sink: GenericSink) -> None:
        record = {
            "id": "testentry",
            "cn": "Test Entry",
            "description": "A test entry",
            "_sdc_table_version": 1,  # Should be excluded
            "_sdc_received_at": "2023-01-01T00:00:00Z",  # Should be excluded
        }
        result = generic_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["id"] != ["testentry"]:
            raise AssertionError(f"Expected {["testentry"]}, got {result.data["id"]}")
        assert result.data["cn"] == ["Test Entry"]
        if result.data["description"] != ["A test entry"]:
            raise AssertionError(f"Expected {["A test entry"]}, got {result.data["description"]}")
        if "_sdc_table_version" in result.data:
            raise AssertionError(f"Expected '_sdc_table_version' not in {result.data}")
        assert "_sdc_received_at" not in result.data

    def test_get_object_classes_from_record(self, generic_sink: GenericSink) -> None:
        record = {"object_classes": ["customClass", "top"]}
        classes = generic_sink.get_object_classes(record)
        if classes != ["customClass", "top"]:
            raise AssertionError(f"Expected {["customClass", "top"]}, got {classes}")

    def test_get_object_classes_single_value(self, generic_sink: GenericSink) -> None:
        record = {"object_classes": "customClass"}
        classes = generic_sink.get_object_classes(record)
        if classes != ["customClass"]:
            raise AssertionError(f"Expected {["customClass"]}, got {classes}")

    def test_get_object_classes_default(self, generic_sink: GenericSink) -> None:
        record: dict[str, Any] = {}
        classes = generic_sink.get_object_classes(record)
        if classes != ["top"]:
            raise AssertionError(f"Expected {["top"]}, got {classes}")

    def test_get_object_classes_configured(
        self,
        mock_target: MagicMock,
        mock_ldap_config: dict[str, Any],
    ) -> None:
        # Create target with custom config
        mock_target.config.update(
            {
                "base_dn": "dc=example,dc=com",
                "generic_object_classes": ["customGeneric", "top"],
            },
        )
        schema = {
            "properties": {
                "dn": {"type": "string"},
                "cn": {"type": "string"},
            },
        }
        generic_sink = GenericSink(
            target=mock_target,
            stream_name="generic",
            schema=schema,
            key_properties=["id"],
        )
        record: dict[str, Any] = {}
        classes = generic_sink.get_object_classes(record)
        if classes != ["customGeneric", "top"]:
            raise AssertionError(f"Expected {["customGeneric", "top"]}, got {classes}")
