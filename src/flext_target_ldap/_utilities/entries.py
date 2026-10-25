"""Stateless entry mapping for the target-ldap sinks and directory client.

Every rule here is driven by the stream entry profiles declared in
``config/target-ldap.yaml`` and by the flat target settings; nothing names a
stream, a client, or a directory server.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_target_ldap import FlextTargetLdapSettings, c, config, m, p, r, t


class FlextTargetLdapUtilitiesEntries:
    """Profile, DN, attribute, and directory-operation mapping utilities."""

    @staticmethod
    def to_str_values(value: t.JsonValue | t.StrSequence) -> list[str]:
        """Convert a value or sequence of values to a list of strings.

        Args:
            value: JSON scalar or sequence of scalars from a Singer record.

        Returns:
            The value's string form as a single-item list, or the string
            form of each item for sequences.

        """
        if isinstance(value, Sequence) and not isinstance(value, str | bytes):
            return [str(item) for item in value]
        return [str(value)]

    @staticmethod
    def entry_profile(stream_name: str) -> m.TargetLdap.EntryProfile:
        """Return the declared entry profile of a Singer stream.

        Args:
            stream_name: Singer stream name.

        Returns:
            The stream's declared profile, or the declared default profile
            when the stream declares none.

        """
        rules = m.TargetLdap.Rules.model_validate(config.TargetLdap.model_dump())
        if stream_name in rules.entry_profiles:
            return rules.entry_profiles[stream_name]
        return rules.default_entry_profile

    @staticmethod
    def record_dn(
        record: t.TargetLdap.RecordPayload,
        profile: m.TargetLdap.EntryProfile,
        settings: t.TargetLdap.SettingsPayload,
    ) -> p.Result[str]:
        """Resolve the DN of a record: its explicit ``dn`` or the profile RDN.

        Args:
            record: Singer record payload.
            profile: Entry profile of the record's stream.
            settings: Flat target settings supplying the base DN.

        Returns:
            The DN, or a failure when the record carries neither a ``dn``
            nor any profile identity field.

        """
        explicit_dn = record.get(c.TargetLdap.KEY_DN)
        if isinstance(explicit_dn, str) and explicit_dn:
            return r[str].ok(explicit_dn)
        base_dn = settings.get(c.TargetLdap.KEY_BASE_DN, c.TargetLdap.DEFAULT_BASE_DN)
        for field in profile.identity_fields:
            identity = record.get(field)
            if identity:
                return r[str].ok(f"{profile.rdn_attribute}={identity},{base_dn}")
        return r[str].fail(f"No {profile.identity_label} found in record")

    @staticmethod
    def object_class_list(value: t.JsonValue) -> list[str]:
        """Normalize a declared object-class value to a list of names.

        Args:
            value: A single object-class name or a list of names.

        Returns:
            The non-empty object-class names.

        Raises:
            TypeError: If the value is neither a string nor a list.

        """
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [str(object_class) for object_class in value if object_class]
        msg = f"Object classes must be a string or a list, got {type(value).__name__}"
        raise TypeError(msg)

    @staticmethod
    def object_classes(
        record: t.TargetLdap.RecordPayload,
        profile: m.TargetLdap.EntryProfile,
        settings: t.TargetLdap.SettingsPayload,
    ) -> list[str]:
        """Resolve the object classes of a record's entry.

        The record's declared classes win, then the profile's settings key,
        then the profile defaults; the profile's required classes are always
        present.

        Args:
            record: Singer record payload.
            profile: Entry profile of the record's stream.
            settings: Flat target settings.

        Returns:
            The object classes of the entry.

        """
        declared_keys = [
            key for key in c.TargetLdap.RECORD_OBJECT_CLASS_KEYS if key in record
        ]
        configured = settings.get(profile.object_classes_setting)
        if declared_keys:
            classes = FlextTargetLdapUtilitiesEntries.object_class_list(
                record[declared_keys[0]],
            )
        elif configured is not None:
            classes = FlextTargetLdapUtilitiesEntries.object_class_list(configured)
        else:
            classes = list(profile.default_object_classes)
        classes.extend(
            required
            for required in profile.required_object_classes
            if required not in classes
        )
        return classes

    @staticmethod
    def attribute_mapping(settings: t.TargetLdap.SettingsPayload) -> t.StrMapping:
        """Return the configured record-field to LDAP-attribute mapping.

        Args:
            settings: Flat target settings.

        Returns:
            The configured mapping; empty when the settings declare none.

        Raises:
            TypeError: If the configured mapping is not a mapping.

        """
        raw = settings.get(c.TargetLdap.KEY_ATTRIBUTE_MAPPING, {})
        if isinstance(raw, Mapping):
            return {key: str(value) for key, value in raw.items()}
        msg = (
            f"Expected Mapping for '{c.TargetLdap.KEY_ATTRIBUTE_MAPPING}', "
            f"got {type(raw).__name__}: {raw!r}"
        )
        raise TypeError(msg)

    @staticmethod
    def entry_attributes(
        record: t.TargetLdap.RecordPayload,
        profile: m.TargetLdap.EntryProfile,
        settings: t.TargetLdap.SettingsPayload,
    ) -> t.MutableStrSequenceMapping:
        """Map a record to the LDAP attributes of its entry.

        Args:
            record: Singer record payload.
            profile: Entry profile of the record's stream.
            settings: Flat target settings supplying ``attribute_mapping``.

        Returns:
            The entry attributes, without object classes.

        """
        to_values = FlextTargetLdapUtilitiesEntries.to_str_values
        attributes: t.MutableStrSequenceMapping = {}
        if profile.include_unmapped_fields:
            attributes.update({
                key: to_values(value)
                for key, value in record.items()
                if key not in c.TargetLdap.RECORD_CONTROL_KEYS and value is not None
            })
        mappings = (
            profile.field_mapping,
            FlextTargetLdapUtilitiesEntries.attribute_mapping(settings),
        )
        for mapping in mappings:
            attributes.update({
                attribute: to_values(record[field])
                for field, attribute in mapping.items()
                if record.get(field) is not None
            })
        return attributes

    @staticmethod
    def validate_entry(
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence,
    ) -> p.Result[bool]:
        """Validate one LDAP entry before writing it.

        Args:
            dn: Distinguished name of the entry.
            attributes: Entry attributes.
            object_classes: Object classes for the entry.

        Returns:
            Success, or a failure naming the first empty part of the entry.

        """
        if not dn:
            return r[bool].fail("DN cannot be empty")
        if not attributes:
            return r[bool].fail("Attributes cannot be empty")
        if not object_classes:
            return r[bool].fail("Object classes cannot be empty")
        return r[bool].ok(value=True)

    @staticmethod
    def ldif_entry(
        dn: str,
        attributes: t.Ldap.OperationAttributes,
        object_classes: t.StrSequence | None = None,
    ) -> m.Ldif.Entry:
        """Build the LDIF entry model of an add operation.

        Args:
            dn: Distinguished name of the entry.
            attributes: Entry attributes to stringify.
            object_classes: Optional object classes added as attributes.

        Returns:
            The LDIF entry ready for the flext-ldap API.

        """
        entry_attributes: t.MutableMappingKV[str, t.StrSequence] = {
            key: FlextTargetLdapUtilitiesEntries.to_str_values(value)
            for key, value in attributes.items()
        }
        if object_classes:
            entry_attributes[c.TargetLdap.KEY_OBJECT_CLASS_ATTRIBUTE] = list(
                object_classes,
            )
        return m.Ldif.Entry(
            dn=m.Ldif.DN(value=dn),
            attributes=m.Ldif.Attributes.model_validate({
                "attributes": entry_attributes,
                "attribute_metadata": {},
                "metadata": None,
            }),
            changetype=None,
            metadata=None,
            validation_metadata=None,
        )

    @staticmethod
    def modify_changes(
        changes: t.Ldap.OperationAttributes,
    ) -> t.MutableMappingKV[str, t.SequenceOf[tuple[int, t.StrSequence]]]:
        """Build modify operations replacing each changed attribute.

        Args:
            changes: Attribute values to write.

        Returns:
            The replace operations keyed by attribute name.

        """
        return {
            key: [
                (
                    c.Ldap.ModifyOperation.REPLACE,
                    FlextTargetLdapUtilitiesEntries.to_str_values(value),
                ),
            ]
            for key, value in changes.items()
        }

    @staticmethod
    def connection_config(
        settings: (
            FlextTargetLdapSettings
            | m.Ldap.ConnectionConfig
            | t.TargetLdap.SettingsPayload
        ),
    ) -> m.Ldap.ConnectionConfig:
        """Resolve any supported settings payload to the connection model.

        Args:
            settings: Typed settings, connection model, or flat payload.

        Returns:
            The resolved LDAP connection configuration.

        """
        if isinstance(settings, m.Ldap.ConnectionConfig):
            return settings
        if isinstance(settings, FlextTargetLdapSettings):
            return m.Ldap.ConnectionConfig.model_validate({
                "host": settings.TargetLdap.host,
                "port": settings.TargetLdap.port,
                "use_ssl": settings.TargetLdap.use_ssl,
                "use_tls": settings.TargetLdap.use_tls,
                "bind_dn": settings.TargetLdap.bind_dn,
                "bind_password": settings.TargetLdap.bind_password,
                "timeout": settings.TargetLdap.timeout,
                "auto_bind": settings.TargetLdap.auto_bind,
                "auto_range": settings.TargetLdap.auto_range,
            })
        connection_value = settings.get("connection")
        if isinstance(connection_value, Mapping):
            return m.Ldap.ConnectionConfig.model_validate(connection_value)
        return m.Ldap.ConnectionConfig.model_validate(settings)


__all__: list[str] = ["FlextTargetLdapUtilitiesEntries"]
