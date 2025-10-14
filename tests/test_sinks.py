"""Tests for target-ldap sinks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from flext_core import FlextCore

from flext_target_ldap import (
    GroupsSink,
    LDAPBaseSink,
    OrganizationalUnitsSink,
    UsersSink,
)


class TestLDAPBaseSink:
    """Test base LDAP sink."""

    @pytest.fixture
    def sink(
        self,
        mock_target: MagicMock,
        mock_ldap_config: FlextCore.Types.Dict,
    ) -> LDAPBaseSink:
        """Create LDAP base sink fixture for testing."""
        # Use mock_ldap_config parameter to avoid unused argument warning
        _mock_ldap_config = mock_ldap_config  # Acknowledge the parameter
        schema = {
            "properties": {
                "dn": {"type": "string"},
                "cn": {"type": "string"},
            },
        }
        return LDAPBaseSink(
            target=mock_target,
            stream_name="test_stream",
            schema=schema,
            key_properties=["dn"],
        )

    def test_ldap_sink_initialization(self, sink: LDAPBaseSink) -> None:
        """Test LDAP base sink initialization with proper configuration."""
        if sink.stream_name != "test_stream":
            stream_msg: str = f"Expected {'test_stream'}, got {sink.stream_name}"
            raise AssertionError(stream_msg)
        assert sink.key_properties == ["dn"]
        if "dn" not in sink.schema["properties"]:
            schema_msg: str = f"Expected {'dn'} in {sink.schema['properties']}"
            raise AssertionError(schema_msg)

    def test_build_dn_not_implemented(self, sink: LDAPBaseSink) -> None:
        """Test that build_dn method raises error when not implemented in subclass."""
        record = {"cn": "test"}
        result = sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "must be implemented in subclass" not in result.error:
            error_msg: str = (
                f"Expected {'must be implemented in subclass'} in {result.error}"
            )
            raise AssertionError(error_msg)

    def test_build_attributes_not_implemented(self, sink: LDAPBaseSink) -> None:
        """Test that build_attributes method raises error when not implemented in subclass."""
        record = {"cn": "test"}
        result = sink.build_attributes(record)
        assert not result.success
        assert result.error is not None
        if "must be implemented in subclass" not in result.error:
            error_msg: str = (
                f"Expected {'must be implemented in subclass'} in {result.error}"
            )
            raise AssertionError(error_msg)

    def test_get_object_classes_default(self, sink: LDAPBaseSink) -> None:
        """Test that get_object_classes returns default 'top' class."""
        record: FlextCore.Types.Dict = {}
        classes = sink.get_object_classes(record)
        if classes != ["top"]:
            classes_msg: str = f"Expected {['top']}, got {classes}"
            raise AssertionError(classes_msg)

    def test_validate_entry_success(self, sink: LDAPBaseSink) -> None:
        """Test successful validation of LDAP entry with valid DN, attributes, and object classes."""
        # Mock the private _client attribute since client is a property
        mock_client = MagicMock()
        mock_client.validate_dn.return_value.success = True
        sink._client = mock_client

        result = sink.validate_entry(
            "cn=test,dc=example,dc=com",
            {"cn": ["test"]},
            ["person", "top"],
        )
        assert result.success

    def test_validate_entry_empty_dn(self, sink: LDAPBaseSink) -> None:
        """Test validation failure when DN is empty."""
        result = sink.validate_entry("", {"cn": ["test"]}, ["person"])
        assert not result.success
        assert result.error is not None
        if "DN cannot be empty" not in result.error:
            dn_error_msg: str = f"Expected {'DN cannot be empty'} in {result.error}"
            raise AssertionError(dn_error_msg)

    def test_validate_entry_empty_attributes(self, sink: LDAPBaseSink) -> None:
        """Test validation failure when attributes are empty."""
        result = sink.validate_entry("cn=test,dc=example,dc=com", {}, ["person"])
        assert not result.success
        assert result.error is not None
        if "Attributes cannot be empty" not in result.error:
            attr_error_msg: str = (
                f"Expected {'Attributes cannot be empty'} in {result.error}"
            )
            raise AssertionError(attr_error_msg)

    def test_validate_entry_empty_object_classes(self, sink: LDAPBaseSink) -> None:
        """Test validation failure when object classes are empty."""
        result = sink.validate_entry("cn=test,dc=example,dc=com", {"cn": ["test"]}, [])
        assert not result.success
        assert result.error is not None
        if "Object classes cannot be empty" not in result.error:
            obj_classes_error_msg: str = (
                f"Expected {'Object classes cannot be empty'} in {result.error}"
            )
            raise AssertionError(obj_classes_error_msg)


class TestUsersSink:
    """Test Users sink."""

    @pytest.fixture
    def users_sink(
        self,
        mock_target: MagicMock,
        _mock_ldap_config: FlextCore.Types.Dict,
    ) -> UsersSink:
        """Create users sink fixture for testing."""
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

    def test_users_build_dn_success(self, users_sink: UsersSink) -> None:
        """Test building DN for user with UID attribute."""
        record = {"uid": "testuser", "cn": "Test User"}
        result = users_sink.build_dn(record)
        assert result.success
        if result.data != "uid=testuser,dc=example,dc=com":
            dn_result_msg: str = (
                f"Expected {'uid=testuser,dc=example,dc=com'}, got {result.data}"
            )
            raise AssertionError(dn_result_msg)

    def test_users_build_dn_missing_uid(self, users_sink: UsersSink) -> None:
        """Test building DN failure when UID attribute is missing."""
        record = {"cn": "Test User"}
        result = users_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No value found for RDN attribute 'uid'" not in result.error:
            msg = (
                f"Expected {"No value found for RDN attribute 'uid'"} in {result.error}"
            )
            raise AssertionError(msg)

    def test_users_build_attributes_basic(self, users_sink: UsersSink) -> None:
        """Test building basic LDAP attributes for user record."""
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
            uid_msg: str = f"Expected {['testuser']}, got {result.data['uid']}"
            raise AssertionError(uid_msg)
        assert result.data["cn"] == ["Test User"]
        if result.data["mail"] != ["test@example.com"]:
            mail_msg: str = (
                f"Expected {['test@example.com']}, got {result.data['mail']}"
            )
            raise AssertionError(mail_msg)
        assert result.data["sn"] == ["User"]
        if result.data["givenName"] != ["Test"]:
            given_name_msg: str = f"Expected {['Test']}, got {result.data['givenName']}"
            raise AssertionError(given_name_msg)

    def test_users_build_attributes_multivalued(self, users_sink: UsersSink) -> None:
        """Test building LDAP attributes with multi-valued fields."""
        record = {
            "uid": "testuser",
            "emails": ["test1@example.com", "test2@example.com"],
            "phone_numbers": ["123-456-7890", "098-765-4321"],
        }
        result = users_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["uid"] != ["testuser"]:
            uid_msg2: str = f"Expected {['testuser']}, got {result.data['uid']}"
            raise AssertionError(uid_msg2)
        assert result.data["mail"] == ["test1@example.com", "test2@example.com"]
        if result.data["telephoneNumber"] != ["123-456-7890", "098-765-4321"]:
            phone_msg: str = f"Expected {['123-456-7890', '098-765-4321']}, got {result.data['telephoneNumber']}"
            raise AssertionError(phone_msg)

    def test_users_get_object_classes_default(self, users_sink: UsersSink) -> None:
        """Test getting default object classes for user entries."""
        record: FlextCore.Types.Dict = {}
        classes = users_sink.get_object_classes(record)
        if classes != ["inetOrgPerson", "organizationalPerson", "person", "top"]:
            user_classes_msg: str = f"Expected {['inetOrgPerson', 'organizationalPerson', 'person', 'top']}, got {classes}"
            raise AssertionError(user_classes_msg)

    @pytest.mark.usefixtures("_mock_ldap_config")
    def test_get_object_classes_configured(
        self,
        mock_target: MagicMock,
    ) -> None:
        """Test getting configured object classes for user entries."""
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
        record: FlextCore.Types.Dict = {}
        classes = users_sink.get_object_classes(record)
        if classes != ["customUser", "top"]:
            custom_user_classes_msg: str = (
                f"Expected {['customUser', 'top']}, got {classes}"
            )
            raise AssertionError(custom_user_classes_msg)


class TestGroupsSink:
    """Test Groups sink."""

    @pytest.fixture
    def groups_sink(
        self,
        mock_target: MagicMock,
        _mock_ldap_config: FlextCore.Types.Dict,
    ) -> GroupsSink:
        """Create groups sink fixture for testing."""
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

    def test_groups_build_dn_success(self, groups_sink: GroupsSink) -> None:
        """Test building DN for group with CN attribute."""
        record = {"cn": "testgroup", "description": "Test Group"}
        result = groups_sink.build_dn(record)
        assert result.success
        if result.data != "cn=testgroup,dc=example,dc=com":
            group_dn_msg: str = (
                f"Expected {'cn=testgroup,dc=example,dc=com'}, got {result.data}"
            )
            raise AssertionError(group_dn_msg)

    def test_groups_build_dn_missing_cn(self, groups_sink: GroupsSink) -> None:
        """Test building DN failure when CN attribute is missing."""
        record = {"description": "Test Group"}
        result = groups_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No value found for RDN attribute 'cn'" not in result.error:
            msg = (
                f"Expected {"No value found for RDN attribute 'cn'"} in {result.error}"
            )
            raise AssertionError(msg)

    def test_groups_build_attributes_basic(self, groups_sink: GroupsSink) -> None:
        """Test building basic LDAP attributes for group record."""
        record = {
            "cn": "testgroup",
            "description": "Test Group",
            "members": ["uid=user1,dc=example,dc=com", "uid=user2,dc=example,dc=com"],
        }
        result = groups_sink.build_attributes(record)
        assert result.success
        assert result.data is not None
        if result.data["cn"] != ["testgroup"]:
            group_cn_msg: str = f"Expected {['testgroup']}, got {result.data['cn']}"
            raise AssertionError(group_cn_msg)
        assert result.data["description"] == ["Test Group"]
        expected_members = [
            "uid=user1,dc=example,dc=com",
            "uid=user2,dc=example,dc=com",
        ]
        if result.data["member"] != expected_members:
            members_msg: str = (
                f"Expected {expected_members}, got {result.data['member']}"
            )
            raise AssertionError(members_msg)

    def test_groups_get_object_classes_default(self, groups_sink: GroupsSink) -> None:
        """Test getting default object classes for group entries."""
        record: FlextCore.Types.Dict = {}
        classes = groups_sink.get_object_classes(record)
        if classes != ["groupOfNames", "top"]:
            group_classes_msg: str = (
                f"Expected {['groupOfNames', 'top']}, got {classes}"
            )
            raise AssertionError(group_classes_msg)


class TestOrganizationalUnitsSink:
    """Test Organizational Units sink."""

    @pytest.fixture
    def ou_sink(
        self,
        mock_target: MagicMock,
        _mock_ldap_config: FlextCore.Types.Dict,
    ) -> OrganizationalUnitsSink:
        """Create organizational units sink fixture for testing."""
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

    def test_ou_build_dn_success(self, ou_sink: OrganizationalUnitsSink) -> None:
        """Test building DN for organizational unit with OU attribute."""
        record = {"ou": "testou", "description": "Test OU"}
        result = ou_sink.build_dn(record)
        assert result.success
        if result.data != "ou=testou,dc=example,dc=com":
            ou_dn_msg: str = (
                f"Expected {'ou=testou,dc=example,dc=com'}, got {result.data}"
            )
            raise AssertionError(ou_dn_msg)

    def test_ou_build_dn_missing_ou(self, ou_sink: OrganizationalUnitsSink) -> None:
        """Test building DN failure when OU attribute is missing."""
        record = {"description": "Test OU"}
        result = ou_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No OU name found in record" not in result.error:
            ou_error_msg: str = (
                f"Expected {'No OU name found in record'} in {result.error}"
            )
            raise AssertionError(ou_error_msg)

    def test_ou_build_attributes_basic(self, ou_sink: OrganizationalUnitsSink) -> None:
        """Test building basic LDAP attributes for organizational unit record."""
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
            ou_attr_msg: str = f"Expected {['testou']}, got {result.data['ou']}"
            raise AssertionError(ou_attr_msg)
        assert result.data["description"] == ["Test OU"]
        if result.data["telephoneNumber"] != ["123-456-7890"]:
            phone_attr_msg: str = (
                f"Expected {['123-456-7890']}, got {result.data['telephoneNumber']}"
            )
            raise AssertionError(phone_attr_msg)
        assert result.data["street"] == ["123 Test St"]
        if result.data["l"] != ["Test City"]:
            city_msg: str = f"Expected {['Test City']}, got {result.data['l']}"
            raise AssertionError(city_msg)
        assert result.data["st"] == ["Test State"]
        if result.data["postalCode"] != ["12345"]:
            postal_msg: str = f"Expected {['12345']}, got {result.data['postalCode']}"
            raise AssertionError(postal_msg)

    def test_ou_get_object_classes_default(
        self, ou_sink: OrganizationalUnitsSink
    ) -> None:
        """Test getting default object classes for organizational unit entries."""
        record: FlextCore.Types.Dict = {}
        classes = ou_sink.get_object_classes(record)
        if classes != ["organizationalUnit", "top"]:
            ou_classes_msg: str = (
                f"Expected {['organizationalUnit', 'top']}, got {classes}"
            )
            raise AssertionError(ou_classes_msg)


class TestLDAPGenericSink:
    """Test Generic sink."""

    @pytest.fixture
    def generic_sink(
        self,
        mock_target: MagicMock,
        _mock_ldap_config: FlextCore.Types.Dict,
    ) -> LDAPBaseSink:
        """Create generic LDAP sink fixture for testing."""
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
        return LDAPBaseSink(
            target=mock_target,
            stream_name="generic",
            schema=schema,
            key_properties=["id"],
        )

    def test_generic_build_dn_explicit(self, generic_sink: LDAPBaseSink) -> None:
        """Test building DN using explicit DN field in record."""
        record = {"dn": "cn=test,dc=example,dc=com"}
        result = generic_sink.build_dn(record)
        assert result.success
        if result.data != "cn=test,dc=example,dc=com":
            generic_dn_msg: str = (
                f"Expected {'cn=test,dc=example,dc=com'}, got {result.data}"
            )
            raise AssertionError(generic_dn_msg)

    def test_generic_build_dn_id_field(self, generic_sink: LDAPBaseSink) -> None:
        """Test building DN using ID field with CN attribute."""
        record = {"id": "testentry", "cn": "Test Entry"}
        result = generic_sink.build_dn(record)
        assert result.success
        if result.data != "cn=testentry,dc=example,dc=com":
            generic_id_msg: str = (
                f"Expected {'cn=testentry,dc=example,dc=com'}, got {result.data}"
            )
            raise AssertionError(generic_id_msg)

    def test_generic_build_dn_no_identifier(self, generic_sink: LDAPBaseSink) -> None:
        """Test building DN failure when no identifier is found."""
        record = {"description": "Test Entry"}
        result = generic_sink.build_dn(record)
        assert not result.success
        assert result.error is not None
        if "No ID or name found for generic entry" not in result.error:
            generic_error_msg = (
                f"Expected {'No ID or name found for generic entry'} in {result.error}"
            )
            raise AssertionError(generic_error_msg)

    def test_generic_build_attributes_basic(self, generic_sink: LDAPBaseSink) -> None:
        """Test building basic LDAP attributes for generic record."""
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
            generic_id_attr_msg: str = (
                f"Expected {['testentry']}, got {result.data['id']}"
            )
            raise AssertionError(generic_id_attr_msg)
        assert result.data["cn"] == ["Test Entry"]
        if result.data["description"] != ["A test entry"]:
            desc_msg: str = (
                f"Expected {['A test entry']}, got {result.data['description']}"
            )
            raise AssertionError(desc_msg)
        if "_sdc_table_version" in result.data:
            sdc_msg: str = f"Expected '_sdc_table_version' not in {result.data}"
            raise AssertionError(sdc_msg)
        assert "_sdc_received_at" not in result.data

    def test_generic_get_object_classes_from_record(
        self, generic_sink: LDAPBaseSink
    ) -> None:
        """Test getting object classes from record data."""
        record = {"object_classes": ["customClass", "top"]}
        classes = generic_sink.get_object_classes(record)
        if classes != ["customClass", "top"]:
            custom_classes_msg: str = (
                f"Expected {['customClass', 'top']}, got {classes}"
            )
            raise AssertionError(custom_classes_msg)

    def test_generic_get_object_classes_single_value(
        self, generic_sink: LDAPBaseSink
    ) -> None:
        """Test getting object classes from single value in record."""
        record = {"object_classes": "customClass"}
        classes = generic_sink.get_object_classes(record)
        if classes != ["customClass"]:
            single_class_msg: str = f"Expected {['customClass']}, got {classes}"
            raise AssertionError(single_class_msg)

    def test_generic_get_object_classes_default(
        self, generic_sink: LDAPBaseSink
    ) -> None:
        """Test getting default object classes for generic entries."""
        record: FlextCore.Types.Dict = {}
        classes = generic_sink.get_object_classes(record)
        if classes != ["top"]:
            default_classes_msg: str = f"Expected {['top']}, got {classes}"
            raise AssertionError(default_classes_msg)

    @pytest.mark.usefixtures("_mock_ldap_config")
    def test_get_object_classes_configured(
        self,
        mock_target: MagicMock,
    ) -> None:
        """Test getting configured object classes for generic entries."""
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
        generic_sink = LDAPBaseSink(
            target=mock_target,
            stream_name="generic",
            schema=schema,
            key_properties=["id"],
        )
        record: FlextCore.Types.Dict = {}
        classes = generic_sink.get_object_classes(record)
        if classes != ["customGeneric", "top"]:
            configured_classes_msg: str = (
                f"Expected {['customGeneric', 'top']}, got {classes}"
            )
            raise AssertionError(configured_classes_msg)
