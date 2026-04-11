"""Internal runtime adapters for the target-ldap service facade."""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_meltano import (
    Sink as FlextMeltanoSingerSinkBase,
    Target as FlextMeltanoSingerTargetBase,
)
from flext_target_ldap import FlextTargetLdap, FlextTargetLdapSink, p, t, u


class FlextTargetLdapServiceRuntime:
    """Service-runtime adapters used by the target-ldap facade."""

    class Target(FlextMeltanoSingerTargetBase):
        """Minimal Singer target used by the service facade."""

        name = "target-ldap"

    class Sink(FlextMeltanoSingerSinkBase):
        """Singer sink adapter that delegates to the LDAP runtime sink."""

        name = "target-ldap-sink"

        _runtime_sink: FlextTargetLdapSink

        @classmethod
        def create(
            cls,
            *,
            runtime_sink: FlextTargetLdapSink,
            target: FlextMeltanoSingerTargetBase,
            stream_name: str,
            schema: t.MutableMappingKV[str, t.ContainerValue],
            key_properties: t.StrSequence,
        ) -> FlextTargetLdapServiceRuntime.Sink:
            """Create an adapter sink and attach the LDAP runtime sink."""
            service_sink = cls(
                target=target,
                stream_name=stream_name,
                schema=schema,
                key_properties=key_properties,
            )
            service_sink._runtime_sink = runtime_sink
            return service_sink

        @override
        def process_batch(
            self,
            context: t.ContainerMapping,
        ) -> None:
            """Singer batch hook is handled record-by-record by the runtime sink."""
            _ = context

        @override
        def process_record(
            self,
            record: t.ContainerMapping,
            context: t.ContainerMapping,
        ) -> None:
            """Delegate Singer record handling to the LDAP runtime sink."""
            result = self._runtime_sink.process_record(
                FlextTargetLdapServiceRuntime.normalize_singer_mapping(record),
                FlextTargetLdapServiceRuntime.normalize_singer_mapping(context),
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
        target_config: t.ContainerMapping,
    ) -> p.Meltano.SingerDrainSink:
        """Create the service-level Singer sink adapter."""
        normalized_target_config = cls.normalize_singer_mapping(target_config)
        runtime_target = FlextTargetLdap(
            settings=normalized_target_config,
            validate_config=False,
        )
        normalized_schema = cls.normalize_flat_schema(schema)
        sink_class: type[FlextTargetLdapSink] = runtime_target.get_sink_class(
            stream_name
        )
        runtime_sink = sink_class(
            target=runtime_target,
            stream_name=stream_name,
            schema=normalized_schema,
            key_properties=[],
        )
        return cls.Sink.create(
            runtime_sink=runtime_sink,
            target=cls.Target(settings=normalized_target_config, validate_config=False),
            stream_name=stream_name,
            schema=dict(normalized_schema),
            key_properties=[],
        )

    @classmethod
    def normalize_singer_mapping(
        cls,
        source: t.ContainerMapping,
    ) -> t.MutableMappingKV[str, t.ContainerValue]:
        """Normalize a Singer payload mapping to the LDAP runtime contract."""
        normalized: t.MutableMappingKV[str, t.ContainerValue] = {}
        for key, value in source.items():
            normalized_value = cls.normalize_singer_value(value)
            if normalized_value is not None:
                normalized[str(key)] = normalized_value
        return normalized

    @classmethod
    def normalize_singer_value(
        cls,
        value: t.NormalizedValue,
    ) -> t.ContainerValue | None:
        """Normalize a Singer payload value to the LDAP runtime contract."""
        if value is None:
            return None
        if isinstance(value, Path):
            return str(value)
        if u.scalar(value):
            return value
        if u.mapping(value):
            return cls.normalize_singer_mapping(value)
        normalized_sequence: t.MutableSequenceOf[t.ContainerValue] = []
        for item in value:
            normalized_item = cls.normalize_singer_value(item)
            if normalized_item is not None:
                normalized_sequence.append(normalized_item)
        return normalized_sequence

    @staticmethod
    def normalize_flat_schema(
        schema: t.FlatContainerMapping,
    ) -> t.MutableMappingKV[str, t.ContainerValue]:
        """Normalize a flat Singer schema to the LDAP runtime contract."""
        return {
            key: (str(value) if isinstance(value, Path) else value)
            for key, value in schema.items()
        }


__all__ = ["FlextTargetLdapServiceRuntime"]
