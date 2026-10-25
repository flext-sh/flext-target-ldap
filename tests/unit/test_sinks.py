"""Observable behavior of the profile-driven target-ldap stream sink.

Expectations derive from the stream entry profiles the sink reads
(``u.TargetLdap.entry_profile``), never from copied config values.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_target_ldap.services import FlextTargetLdapClient, FlextTargetLdapSinks
from tests import c, p, t, tm, u


class TestsFlextTargetLdapSinks:
    """Behavior contract for the stream sink."""

    @staticmethod
    def build_sink(
        stream_name: str,
        payload: t.TargetLdap.SettingsPayload,
        updates: t.TargetLdap.SettingsPayload,
    ) -> p.TargetLdap.Sink:
        """Build the stream sink over a client bound to the merged settings.

        Returns:
            The stream sink.

        """
        settings: t.TargetLdap.SettingsPayload = {
            **payload,
            "base_dn": c.TargetLdap.Tests.SAMPLE_BASE_DN,
            **updates,
        }
        return FlextTargetLdapSinks.runtime_sink(
            stream_name=stream_name,
            schema={"properties": {"dn": {"type": "string"}}},
            target_config=settings,
            directory=FlextTargetLdapClient(settings=settings),
        )

    class TestsEntryValidation:
        """Behavior contract for entry validation and sink identity."""

        @staticmethod
        def test_sink_binds_stream_and_schema(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test the sink carries its stream and schema."""
            sink = TestsFlextTargetLdapSinks.build_sink(
                "test_stream",
                ldap_settings_payload,
                {},
            )
            tm.that(sink.stream_name, eq="test_stream")
            properties = sink.schema.get("properties")
            tm.that(properties, is_=dict)
            tm.that(properties, has="dn")

        @staticmethod
        def test_validate_entry_success(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test validate entry success."""
            sink = TestsFlextTargetLdapSinks.build_sink(
                "test_stream",
                ldap_settings_payload,
                {},
            )
            result = sink.validate_entry(
                f"cn=test,{c.TargetLdap.Tests.SAMPLE_BASE_DN}",
                {"cn": ["test"]},
                ["person", "top"],
            )
            tm.ok(result)

        @staticmethod
        @pytest.mark.parametrize(
            ("dn", "attributes", "object_classes", "expected_message"),
            [
                ("", {"cn": ["test"]}, ["person"], "DN cannot be empty"),
                (
                    "cn=test,dc=example,dc=com",
                    {},
                    ["person"],
                    "Attributes cannot be empty",
                ),
                (
                    "cn=test,dc=example,dc=com",
                    {"cn": ["test"]},
                    [],
                    "Object classes cannot be empty",
                ),
            ],
        )
        def test_validate_entry_failure_cases(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
            dn: str,
            attributes: t.Ldap.OperationAttributes,
            object_classes: list[str],
            expected_message: str,
        ) -> None:
            """Test validate entry failure cases."""
            sink = TestsFlextTargetLdapSinks.build_sink(
                "test_stream",
                ldap_settings_payload,
                {},
            )
            result = sink.validate_entry(dn, attributes, object_classes)
            tm.that(tm.fail(result), has=expected_message)

    class TestsDeclaredStreams:
        """Behavior contract for streams with a declared entry profile."""

        @staticmethod
        @pytest.mark.parametrize(
            "stream_name",
            ["users", "groups", "organizational_units"],
        )
        def test_build_dn_uses_profile_rdn(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
            stream_name: str,
        ) -> None:
            """Test the DN uses the profile RDN and first identity field."""
            profile = u.TargetLdap.entry_profile(stream_name)
            base_dn = c.TargetLdap.Tests.SAMPLE_BASE_DN
            sink = TestsFlextTargetLdapSinks.build_sink(
                stream_name,
                ldap_settings_payload,
                {},
            )
            record: t.TargetLdap.RecordPayload = {
                profile.identity_fields[0]: "entry1",
            }
            tm.ok(
                sink.build_dn(record),
                eq=f"{profile.rdn_attribute}=entry1,{base_dn}",
            )

        @staticmethod
        @pytest.mark.parametrize(
            "stream_name",
            ["users", "groups", "organizational_units"],
        )
        def test_build_dn_without_identity_fails(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
            stream_name: str,
        ) -> None:
            """Test a record without any identity field has no DN."""
            profile = u.TargetLdap.entry_profile(stream_name)
            sink = TestsFlextTargetLdapSinks.build_sink(
                stream_name,
                ldap_settings_payload,
                {},
            )
            result = sink.build_dn({"unmapped_field": "value"})
            tm.that(tm.fail(result), has=f"No {profile.identity_label} found")

        @staticmethod
        def test_explicit_dn_wins(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test an explicit record ``dn`` is used as is."""
            sink = TestsFlextTargetLdapSinks.build_sink(
                "users",
                ldap_settings_payload,
                {},
            )
            explicit_dn = f"uid=explicit,{c.TargetLdap.Tests.SAMPLE_BASE_DN}"
            tm.ok(
                sink.build_dn({"dn": explicit_dn, "username": "x"}),
                eq=explicit_dn,
            )

        @staticmethod
        @pytest.mark.parametrize(
            "stream_name",
            ["users", "groups", "organizational_units"],
        )
        def test_build_attributes_follows_field_mapping(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
            stream_name: str,
        ) -> None:
            """Test mapped record fields become their declared attributes."""
            profile = u.TargetLdap.entry_profile(stream_name)
            sink = TestsFlextTargetLdapSinks.build_sink(
                stream_name,
                ldap_settings_payload,
                {},
            )
            record: t.TargetLdap.RecordPayload = {
                field: f"value-{field}" for field in profile.field_mapping
            }
            attributes = tm.ok(sink.build_attributes(record))
            for field, attribute in profile.field_mapping.items():
                tm.that(attributes[attribute], eq=[f"value-{field}"])

        @staticmethod
        def test_build_attributes_keeps_multiple_values(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test list values stay multi-valued attributes."""
            profile = u.TargetLdap.entry_profile("users")
            field = next(iter(profile.field_mapping))
            sink = TestsFlextTargetLdapSinks.build_sink(
                "users",
                ldap_settings_payload,
                {},
            )
            attributes = tm.ok(sink.build_attributes({field: ["one", "two"]}))
            tm.that(attributes[profile.field_mapping[field]], eq=["one", "two"])

        @staticmethod
        @pytest.mark.parametrize(
            "stream_name",
            ["users", "groups", "organizational_units"],
        )
        def test_object_classes_include_required(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
            stream_name: str,
        ) -> None:
            """Test every entry carries the profile's required classes."""
            profile = u.TargetLdap.entry_profile(stream_name)
            sink = TestsFlextTargetLdapSinks.build_sink(
                stream_name,
                ldap_settings_payload,
                {},
            )
            classes = sink.resolve_object_classes({})
            for required in profile.required_object_classes:
                tm.that(classes, has=required)

        @staticmethod
        def test_object_classes_follow_configured_setting(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test the profile's settings key adds configured classes."""
            profile = u.TargetLdap.entry_profile("users")
            sink = TestsFlextTargetLdapSinks.build_sink(
                "users",
                ldap_settings_payload,
                {profile.object_classes_setting: ["customUser", "top"]},
            )
            classes = sink.resolve_object_classes({})
            tm.that(classes, has="customUser")
            for required in profile.required_object_classes:
                tm.that(classes, has=required)

    class TestsUndeclaredStream:
        """Behavior contract for streams that use the default profile."""

        @staticmethod
        def test_build_dn_from_identity_field(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test the default profile derives the DN from its identity."""
            profile = u.TargetLdap.entry_profile("generic")
            base_dn = c.TargetLdap.Tests.SAMPLE_BASE_DN
            sink = TestsFlextTargetLdapSinks.build_sink(
                "generic",
                ldap_settings_payload,
                {},
            )
            tm.ok(
                sink.build_dn({profile.identity_fields[0]: "testentry"}),
                eq=f"{profile.rdn_attribute}=testentry,{base_dn}",
            )

        @staticmethod
        def test_build_dn_without_identity_fails(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test a record without identity has no DN."""
            profile = u.TargetLdap.entry_profile("generic")
            sink = TestsFlextTargetLdapSinks.build_sink(
                "generic",
                ldap_settings_payload,
                {},
            )
            result = sink.build_dn({"description": "Test Entry"})
            tm.that(tm.fail(result), has=f"No {profile.identity_label} found")

        @staticmethod
        def test_build_attributes_writes_every_field(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test the default profile writes every non-control field."""
            sink = TestsFlextTargetLdapSinks.build_sink(
                "generic",
                ldap_settings_payload,
                {},
            )
            attributes = tm.ok(
                sink.build_attributes({
                    "dn": f"cn=testentry,{c.TargetLdap.Tests.SAMPLE_BASE_DN}",
                    "cn": "Test Entry",
                    "description": "A test entry",
                }),
            )
            tm.that(attributes["cn"], eq=["Test Entry"])
            tm.that(attributes["description"], eq=["A test entry"])
            tm.that(attributes, lacks="dn")

        @staticmethod
        @pytest.mark.parametrize(
            ("declared", "expected"),
            [
                (["customClass", "top"], ["customClass", "top"]),
                ("customClass", ["customClass"]),
            ],
        )
        def test_object_classes_from_record(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
            declared: t.JsonValue,
            expected: list[str],
        ) -> None:
            """Test record-declared object classes win."""
            sink = TestsFlextTargetLdapSinks.build_sink(
                "generic",
                ldap_settings_payload,
                {},
            )
            classes = sink.resolve_object_classes({"object_classes": declared})
            tm.that(classes, eq=expected)

        @staticmethod
        def test_object_classes_default(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test the default profile's classes apply when none are set."""
            profile = u.TargetLdap.entry_profile("generic")
            sink = TestsFlextTargetLdapSinks.build_sink(
                "generic",
                ldap_settings_payload,
                {},
            )
            tm.that(
                sink.resolve_object_classes({}),
                eq=list(profile.default_object_classes),
            )

        @staticmethod
        def test_object_classes_configured(
            ldap_settings_payload: t.TargetLdap.SettingsPayload,
        ) -> None:
            """Test the default profile's settings key sets the classes."""
            profile = u.TargetLdap.entry_profile("generic")
            sink = TestsFlextTargetLdapSinks.build_sink(
                "generic",
                ldap_settings_payload,
                {profile.object_classes_setting: ["customGeneric", "top"]},
            )
            tm.that(sink.resolve_object_classes({}), eq=["customGeneric", "top"])
