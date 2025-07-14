"""Tests for target-ldap sinks."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from flext_target_ldap.sinks import GenericSink
from flext_target_ldap.sinks import GroupsSink
from flext_target_ldap.sinks import LDAPSink
from flext_target_ldap.sinks import OrganizationalUnitsSink
from flext_target_ldap.sinks import UsersSink


class TestLDAPSink:
    """Test base LDAP sink."""

    @pytest.fixture
    def sink(self,
        mock_target:
        MagicMock,
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

    def test_sink_initialization(self, sink:
        LDAPSink) -> None:
        assert sink.stream_name == "test_stream"
        assert sink.key_properties == ["dn"]
        assert "dn" in sink.schema["properties"]

    def test_get_dn_from_record_explicit(self, sink:
        LDAPSink) -> None:
        record = {"dn": "cn=test,dc=example,dc=com"}
        assert sink.get_dn_from_record(record) == "cn=test,dc=example,dc=com"

    def test_get_dn_from_record_template(self,
        sink:
        LDAPSink,
        mock_target: MagicMock,
    ) -> None:
        mock_target.config["test_stream_dn_template"] = (
            "cn={cn},ou=test,dc=example,dc=com"
        )

        record = {"cn": "testgroup"}
        dn = sink.get_dn_from_record(record)
        assert dn == "cn=testgroup,ou=test,dc=example,dc=com"

    def test_get_dn_from_record_rdn(self, sink:
        LDAPSink) -> None:
        sink.get_rdn_attribute = lambda: "cn"  # type: ignore

        record = {"cn": "test"}
        dn = sink.get_dn_from_record(record)
        assert dn == "cn=test,dc=test,dc=com"

    def test_get_dn_from_record_error(self, sink:
        LDAPSink) -> None:
        record = {"uid": "test"}  # No DN, no matching RDN

        with pytest.raises(ValueError, match="Cannot determine DN"):
            sink.get_dn_from_record(record)

    def test_get_object_classes(self, sink:
        LDAPSink) -> None:
        # From record
        record = {"objectClass": ["person", "top"]}
        classes = sink.get_object_classes(record)
        assert classes == ["person", "top"]

        # Single value
        record = {"objectClass": "person"}
        classes = sink.get_object_classes(record)
        assert classes == ["person"]

        # Default
        sink.get_default_object_classes = lambda: ["defaultClass"]  # type: ignore
        record = {}
        classes = sink.get_object_classes(record)
        assert classes == ["defaultClass"]

    def test_prepare_attributes(self, sink:
        LDAPSink) -> None:
        record = {
            "dn": "cn=test,dc=example,dc=com",
            "cn": "test",
            "member": ["user1", "user2"],
            "description": ["Single item list"],
            "objectClass": ["group"],
            "_sdc_deleted_at": "2024-01-01",
        }

        attrs = sink.prepare_attributes(record)

        # Special fields removed
        assert "dn" not in attrs
        assert "objectClass" not in attrs
        assert "_sdc_deleted_at" not in attrs

        # Multi-valued preserved
        assert attrs["member"] == ["user1", "user2"]

        # Single-valued flattened
        assert attrs["description"] == "Single item list"

    @patch("target_ldap.sinks.LDAPClient")
    def test_process_record_upsert(self,
        mock_client_class:
        MagicMock,
        sink: LDAPSink,
        sample_user_record: dict[str, Any],
    ) -> None:
        mock_client = MagicMock()
        mock_client.upsert_entry.return_value = (True, "add")
        sink._client = mock_client

        sink.process_record(sample_user_record, {})

        mock_client.upsert_entry.assert_called_once()
        call_args = mock_client.upsert_entry.call_args
        assert call_args[0][0] == "uid=jdoe,ou=users,dc=test,dc=com"

    @patch("target_ldap.sinks.LDAPClient")
    def test_process_record_delete(self,
        mock_client_class:
        MagicMock,
        sink: LDAPSink,
    ) -> None:
        mock_client = MagicMock()
        mock_client.entry_exists.return_value = True
        mock_client.delete_entry.return_value = True
        sink._client = mock_client

        record = {
            "dn": "cn=test,dc=example,dc=com",
            "_sdc_deleted_at": "2024-01-01T12:00:00Z",
        }

        sink.process_record(record, {})

        mock_client.entry_exists.assert_called_once_with("cn=test,dc=example,dc=com")
        mock_client.delete_entry.assert_called_once_with("cn=test,dc=example,dc=com")


class TestUsersSink:
    """Test users sink."""

    @pytest.fixture
    def users_sink(self,
        mock_target:
        MagicMock,
    ) -> UsersSink:
        schema = {"properties": {"dn": {"type": "string"}}}
        return UsersSink(
            target=mock_target,
            stream_name="users",
            schema=schema,
            key_properties=["dn"],
        )

    def test_users_sink_properties(self, users_sink:
        UsersSink) -> None:
        assert users_sink.get_rdn_attribute() == "uid"
        assert "inetOrgPerson" in users_sink.get_default_object_classes()
        assert "person" in users_sink.get_default_object_classes()

    def test_custom_rdn_attribute(self,
        users_sink:
        UsersSink,
        mock_target: MagicMock,
    ) -> None:
        mock_target.config["user_rdn_attribute"] = "mail"
        assert users_sink.get_rdn_attribute() == "mail"


class TestGroupsSink:
    """Test groups sink."""

    @pytest.fixture
    def groups_sink(self,
        mock_target:
        MagicMock,
    ) -> GroupsSink:
        schema = {"properties": {"dn": {"type": "string"}}}
        return GroupsSink(
            target=mock_target,
            stream_name="groups",
            schema=schema,
            key_properties=["dn"],
        )

    def test_groups_sink_properties(self, groups_sink:
        GroupsSink) -> None:
        assert groups_sink.get_rdn_attribute() == "cn"
        assert "groupOfNames" in groups_sink.get_default_object_classes()

    def test_prepare_attributes_member_requirement(self,
        groups_sink:
        GroupsSink,
        mock_target: MagicMock,
    ) -> None:
        # No members - should add placeholder
        record = {"cn": "empty-group"}
        attrs = groups_sink.prepare_attributes(record)
        assert "member" in attrs
        assert attrs["member"][0].endswith("dc=test,dc=com")

        # Empty member list - should add placeholder
        record = {"cn": "empty-group", "member": []}
        attrs = groups_sink.prepare_attributes(record)
        assert len(attrs["member"]) > 0

        # Has members - should preserve
        record = {"cn": "group", "member": ["uid=user1,dc=test,dc=com"]}
        attrs = groups_sink.prepare_attributes(record)
        assert attrs["member"] == ["uid=user1,dc=test,dc=com"]


class TestOrganizationalUnitsSink:
    """Test organizational units sink."""

    @pytest.fixture
    def ou_sink(self,
        mock_target:
        MagicMock,
    ) -> OrganizationalUnitsSink:
        schema = {"properties": {"dn": {"type": "string"}}}
        return OrganizationalUnitsSink(
            target=mock_target,
            stream_name="organizational_units",
            schema=schema,
            key_properties=["dn"],
        )

    def test_ou_sink_properties(self, ou_sink:
        OrganizationalUnitsSink) -> None:
        assert ou_sink.get_rdn_attribute() == "ou"
        assert "organizationalUnit" in ou_sink.get_default_object_classes()


class TestGenericSink:
    """Test generic sink."""

    @pytest.fixture
    def generic_sink(self,
        mock_target:
        MagicMock,
    ) -> GenericSink:
        schema = {"properties": {"dn": {"type": "string"}}}
        return GenericSink(
            target=mock_target,
            stream_name="custom_stream",
            schema=schema,
            key_properties=["dn"],
        )

    def test_generic_sink_defaults(self, generic_sink:
        GenericSink) -> None:
        assert generic_sink.get_rdn_attribute() == "cn"
        assert generic_sink.get_default_object_classes() == ["top"]

    def test_generic_sink_custom_config(self,
        generic_sink:
        GenericSink,
        mock_target: MagicMock,
    ) -> None:
        mock_target.config["custom_stream_rdn_attribute"] = "uid"
        mock_target.config["custom_stream_object_classes"] = ["account", "top"]

        assert generic_sink.get_rdn_attribute() == "uid"
        assert generic_sink.get_default_object_classes() == ["account", "top"]
