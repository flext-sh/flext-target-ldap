"""Internal runtime adapters for the target-ldap service facade."""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_meltano import m, u
from flext_target_ldap import FlextTargetLdap, p, t
from flext_target_ldap._models.sinks import FlextTargetLdapSink


class FlextTargetLdapServiceRuntime:
    """Service-runtime adapters used by the target-ldap facade."""

    class Target(m.Meltano.SingerTargetBase):
        """Minimal Singer target used by the service facade."""

        name = "target-ldap"

    class Sink(m.Meltano.SingerSinkBase):
        """Singer sink adapter that delegates to the LDAP runtime sink."""

        name = "target-ldap-sink"

        _runtime_sink: FlextTargetLdapSink

        @classmethod
        def create(
            cls,
            *,
            runtime_sink: FlextTargetLdapSink,
            target: m.Meltano.SingerTargetBase,
            stream_name: str,
            schema: t.TargetLdap.MutableSchemaPayload,
            key_properties: t.StrSequence,
        ) -> FlextTargetLdapServiceRuntime.Sink:
            """Create an adapter sink and attach the LDAP runtime sink."""
            schema_dict = t.json_dict_adapter().validate_python(schema)
            service_sink = cls(
                target=target,
                stream_name=stream_name,
                schema=schema_dict,
                key_properties=key_properties,
            )
            service_sink._runtime_sink = runtime_sink
            return service_sink

        @override
        def process_batch(
            self,
            context: t.JsonMapping,
        ) -> None:
            """Singer batch hook is handled record-by-record by the runtime sink."""
            _ = context

        @override
        def process_record(
            self,
            record: t.JsonMapping,
            context: t.JsonMapping,
        ) -> None:
            """Delegate Singer record handling to the LDAP runtime sink."""
            result = self._runtime_sink.process_record(
                u.normalize_to_json_mapping(record),
                u.normalize_to_json_mapping(context),
            )
            if result.failure:
                msg = result.error or "LDAP runtime sink rejected the record"
                raise RuntimeError(msg)

    @classmethod
    def create_sink(
        cls,
        *,
        stream_name: str,
        schema: t.FlatContainerMapping,
        target_config: t.JsonMapping,
    ) -> p.Meltano.SingerDrainSink:
        """Create the service-level Singer sink adapter."""
        normalized_target_config = u.normalize_to_json_mapping(
            target_config,
        )
        runtime_target = FlextTargetLdap(
            settings=normalized_target_config,
            validate_config=False,
        )
        normalized_schema = cls.normalize_flat_schema(schema)
        sink_class: type[FlextTargetLdapSink] = runtime_target.get_sink_class(
            stream_name,
        )
        runtime_sink = sink_class(
            target=runtime_target,
            stream_name=stream_name,
            schema=normalized_schema,
            key_properties=[],
        )
        return cls.Sink.create(
            runtime_sink=runtime_sink,
            target=cls.Target(
                config=t.json_dict_adapter().validate_python(normalized_target_config),
                validate_config=False,
            ),
            stream_name=stream_name,
            schema=normalized_schema,
            key_properties=[],
        )

    @staticmethod
    def normalize_flat_schema(
        schema: t.FlatContainerMapping,
    ) -> t.TargetLdap.MutableSchemaPayload:
        """Normalize a flat Singer schema to the LDAP runtime contract."""
        return {
            key: u.Cli.normalize_json_value(
                str(value) if isinstance(value, Path) else value,
            )
            for key, value in schema.items()
        }


__all__: list[str] = ["FlextTargetLdapServiceRuntime"]
