"""Internal runtime adapters for the target-ldap service facade.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_meltano import u

from flext_target_ldap import c, m, p, t


class FlextTargetLdapServiceRuntime:
    """Service-runtime adapters used by the target-ldap facade."""

    class Target(m.Meltano.SingerTargetBase):
        """Minimal Singer target used by the service facade."""

        name = c.TargetLdap.TARGET_NAME

    class Sink(m.Meltano.SingerSinkBase):
        """Singer sink adapter that delegates to the LDAP runtime sink."""

        name = "target-ldap-sink"

        _runtime_sink: p.TargetLdap.Sink

        @classmethod
        def create(
            cls,
            *,
            runtime_sink: p.TargetLdap.Sink,
            target: m.Meltano.SingerTargetBase,
            stream_name: str,
            schema: t.TargetLdap.MutableSchemaPayload,
            key_properties: t.StrSequence,
        ) -> FlextTargetLdapServiceRuntime.Sink:
            """Create an adapter sink and attach the LDAP runtime sink.

            LDAP-specific: schema validated via TargetLdap adapter with
            DN-normalized entries and hierarchical directory structure handling.

            Args:
                runtime_sink: LDAP runtime sink handling record writes.
                target: Singer target owning the sink.
                stream_name: Name of the Singer stream.
                schema: Singer schema for the stream.
                key_properties: Singer key properties for the stream.

            Returns:
                The adapter sink bound to the runtime sink.

            """
            validated_schema = u.json_dict_adapter().validate_python(schema)
            bound_sink = cls(
                target=target,
                stream_name=stream_name,
                schema=validated_schema,
                key_properties=key_properties,
            )
            bound_sink._runtime_sink = runtime_sink
            return bound_sink

        @override
        def process_batch(self, context: t.JsonMapping) -> None:
            """Singer batch hook is handled record-by-record by the runtime sink."""
            _ = context

        @override
        def process_record(self, record: t.JsonMapping, context: t.JsonMapping) -> None:
            """Delegate Singer record handling to the LDAP runtime sink.

            Args:
                record: Singer record payload to process.
                context: Singer record context metadata.

            Raises:
                RuntimeError: If the LDAP runtime sink rejects the record.

            """
            result = self._runtime_sink.process_record(
                u.normalize_to_json_mapping(record),
                u.normalize_to_json_mapping(context),
            )
            if result.failure:
                msg = result.error or "LDAP runtime sink rejected the record"
                raise RuntimeError(msg)

    @staticmethod
    def normalize_flat_schema(
        schema: t.FlatContainerMapping,
    ) -> t.TargetLdap.MutableSchemaPayload:
        """Normalize a flat Singer schema to the LDAP runtime contract.

        Args:
            schema: Flat Singer schema mapping to normalize.

        Returns:
            The schema values normalized to the runtime payload types.

        """
        return {
            key: u.Cli.normalize_json_value(
                str(value) if isinstance(value, Path) else value,
            )
            for key, value in schema.items()
        }


__all__: list[str] = ["FlextTargetLdapServiceRuntime"]
