"""Profile-driven LDAP sink for every target-ldap Singer stream.

One sink class serves every stream: the stream's entry profile from
``config/target-ldap.yaml`` supplies its DN, object-class and attribute rules,
and the directory capability is injected as ``p.TargetLdap.Directory``. Nothing
here names a stream, a client, or a directory server.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from flext_target_ldap import c, p, r, t, u


class FlextTargetLdapSinks:
    """Stream sink and the sink factory bound by the target facade."""

    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    class Sink:
        """Writes one stream's records to the injected directory."""

        def __init__(
            self,
            *,
            directory: p.TargetLdap.Directory,
            settings: t.TargetLdap.SettingsPayload,
            stream_name: str,
            schema: t.TargetLdap.SchemaPayload,
            key_properties: Sequence[str],
        ) -> None:
            """Bind the sink to its directory, entry profile, and settings."""
            self.directory = directory
            self.profile = u.TargetLdap.entry_profile(stream_name)
            self.settings = settings
            self.stream_name = stream_name
            self.schema = schema
            self.key_properties = key_properties
            self._written_dns: set[str] = set()

        def build_dn(self, record: t.TargetLdap.RecordPayload) -> p.Result[str]:
            """Build the entry DN of a record.

            Args:
                record: Singer record payload.

            Returns:
                The DN, or a failure when the record has no identity.

            """
            return u.TargetLdap.record_dn(record, self.profile, self.settings)

        def build_attributes(
            self,
            record: t.TargetLdap.RecordPayload,
        ) -> p.Result[t.Ldap.OperationAttributes]:
            """Build the entry attributes of a record.

            Args:
                record: Singer record payload.

            Returns:
                The entry attributes, without object classes.

            """
            attributes: t.Ldap.OperationAttributes = u.TargetLdap.entry_attributes(
                record,
                self.profile,
                self.settings,
            )
            return r[t.Ldap.OperationAttributes].ok(attributes)

        def resolve_object_classes(
            self,
            record: t.TargetLdap.RecordPayload,
        ) -> Sequence[str]:
            """Resolve the object classes of a record's entry.

            Args:
                record: Singer record payload.

            Returns:
                The entry object classes.

            """
            return u.TargetLdap.object_classes(record, self.profile, self.settings)

        @staticmethod
        def validate_entry(
            dn: str,
            attributes: t.Ldap.OperationAttributes,
            object_classes: Sequence[str],
        ) -> p.Result[bool]:
            """Validate one LDAP entry before writing it.

            Args:
                dn: Distinguished name of the entry.
                attributes: Entry attributes.
                object_classes: Object classes for the entry.

            Returns:
                Success, or a failure naming the first empty part.

            """
            return u.TargetLdap.validate_entry(dn, attributes, object_classes)

        def process_record(
            self,
            record: t.TargetLdap.RecordPayload,
            context: t.TargetLdap.RecordPayload,
        ) -> p.Result[bool]:
            """Write one record: delete, add, or modify its entry.

            Args:
                record: Singer record payload.
                context: Singer record context metadata (unused by LDAP).

            Returns:
                The outcome of the directory operation.

            """
            _ = context
            dn_result = self.build_dn(record)
            if dn_result.failure:
                result = r[bool].from_failure(dn_result)
            else:
                result = self._process_record_with_dn(record, dn_result.value)
            return result

        def _process_record_with_dn(
            self,
            record: t.TargetLdap.RecordPayload,
            dn: str,
        ) -> p.Result[bool]:
            """Apply the delete-or-write behavior after resolving the record DN.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            if record.get(c.TargetLdap.KEY_DELETED_AT):
                return self._delete_entry(dn)
            attributes = u.TargetLdap.entry_attributes(
                record,
                self.profile,
                self.settings,
            )
            object_classes = self.resolve_object_classes(record)
            validation = self.validate_entry(dn, attributes, object_classes)
            if validation.failure:
                return validation
            if dn in self._written_dns:
                return self._modify_entry(dn, attributes)
            added = self.directory.add_entry(dn, attributes, object_classes)
            if added.success:
                self._written_dns.add(dn)
                FlextTargetLdapSinks.logger.debug(
                    "%s entry added: %s",
                    self.profile.label,
                    dn,
                )
                return r[bool].ok(value=True)
            if self.settings.get(c.TargetLdap.KEY_UPDATE_EXISTING_ENTRIES) is True:
                return self._modify_entry(dn, attributes)
            return r[bool].fail(
                f"Failed to add {self.profile.label} {dn}: {added.error}",
            )

        def _modify_entry(
            self,
            dn: str,
            attributes: t.Ldap.OperationAttributes,
        ) -> p.Result[bool]:
            """Replace the attributes of an existing entry.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            modified = self.directory.modify_entry(dn, attributes)
            if modified.failure:
                return r[bool].fail(
                    f"Failed to modify {self.profile.label} {dn}: {modified.error}",
                )
            self._written_dns.add(dn)
            FlextTargetLdapSinks.logger.debug(
                "%s entry modified: %s",
                self.profile.label,
                dn,
            )
            return r[bool].ok(value=True)

        def _delete_entry(self, dn: str) -> p.Result[bool]:
            """Delete the entry of a record marked deleted at the source.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            deleted = self.directory.delete_entry(dn)
            if deleted.failure:
                return r[bool].fail(
                    f"Failed to delete {self.profile.label} {dn}: {deleted.error}",
                )
            self._written_dns.discard(dn)
            FlextTargetLdapSinks.logger.debug(
                "%s entry deleted: %s",
                self.profile.label,
                dn,
            )
            return r[bool].ok(value=True)

    @staticmethod
    def runtime_sink(
        *,
        stream_name: str,
        schema: t.TargetLdap.SchemaPayload,
        target_config: t.TargetLdap.SettingsPayload,
        directory: p.TargetLdap.Directory,
    ) -> FlextTargetLdapSinks.Sink:
        """Build the stream sink over an injected directory.

        Args:
            stream_name: Singer stream the sink writes.
            schema: Singer schema of the stream.
            target_config: Flat target settings payload.
            directory: Directory capability the sink writes through.

        Returns:
            The stream sink driven by the stream's entry profile.

        """
        return FlextTargetLdapSinks.Sink(
            directory=directory,
            settings=target_config,
            stream_name=stream_name,
            schema=schema,
            key_properties=[],
        )

    @staticmethod
    def create_sink(
        *,
        stream_name: str,
        schema: t.JsonMapping,
        target_config: t.JsonMapping,
        directory_factory: p.TargetLdap.DirectoryFactory,
    ) -> p.Meltano.SingerDrainSink:
        """Build the Singer drain sink of one stream.

        The target facade binds ``directory_factory`` at its composition root;
        the base service supplies the remaining arguments.

        Args:
            stream_name: Singer stream the sink drains.
            schema: Singer schema of the stream.
            target_config: Flat target settings payload.
            directory_factory: Builds the directory capability from settings.

        Returns:
            The Singer drain sink delegating to the stream sink.

        """
        normalized_config = u.normalize_to_json_mapping(target_config)
        normalized_schema = u.TargetLdap.normalize_flat_schema(schema)
        runtime_sink = FlextTargetLdapSinks.runtime_sink(
            stream_name=stream_name,
            schema=normalized_schema,
            target_config=normalized_config,
            directory=directory_factory(normalized_config),
        )
        return u.TargetLdap.Sink.create(
            runtime_sink=runtime_sink,
            target=u.TargetLdap.Target(
                config=u.json_dict_adapter().validate_python(normalized_config),
                validate_config=False,
            ),
            stream_name=stream_name,
            schema=normalized_schema,
            key_properties=[],
        )


__all__: list[str] = ["FlextTargetLdapSinks"]
