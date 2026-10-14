"""Canonical target-ldap facade.

Owns the public ``FlextTargetLdap`` surface. Legacy runtime logic lives here so
``gen-init`` can keep ``api.py`` as the single canonical owner of the facade.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextContainer
from flext_target_ldap import FlextTargetLdapSettings, c, p, t, u
from flext_target_ldap._models import FlextTargetLdapModelsSinks
from flext_target_ldap._utilities import (
    FlextTargetLdapClient,
    FlextTargetLdapServiceRuntime,
)
from flext_target_ldap.application import FlextTargetLdapOrchestrator


class FlextTargetLdap(
    FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapTarget,
):
    """LDAP target facade for Singer using flext-core patterns."""

    name = "target-ldap"
    config_class = FlextTargetLdapSettings
    _container_type: ClassVar[p.ContainerType] = FlextContainer
    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    @override
    def __init__(
        self,
        *,
        settings: t.TargetLdap.SettingsPayload | None = None,
        validate_config: bool = True,
        **kwargs: t.Scalar,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(
            settings=settings or {},
            validate_config=validate_config,
            **kwargs,
        )
        self._orchestrator: FlextTargetLdapOrchestrator | None = None
        self._container: p.Container | None = None

    @property
    def orchestrator(self) -> FlextTargetLdapOrchestrator:
        """The orchestrator for this target, created on first access."""
        if self._orchestrator is None:
            settings = FlextTargetLdapSettings.model_validate(self.settings)
            self._orchestrator = FlextTargetLdapOrchestrator(settings)
        return self._orchestrator

    @property
    def singer_catalog(self) -> t.TargetLdap.CatalogPayload:
        """The Singer catalog for this target."""
        return u.TargetLdap.build_singer_catalog()

    def resolve_sink(
        self,
        stream_name: str,
    ) -> FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapBaseSink:
        """Return an instantiated sink for the given stream name.

        Args:
            stream_name: Name of the Singer stream to resolve.

        Returns:
            A sink instance bound to this target for the stream.

        """
        sink_class = self.resolve_sink_class(stream_name)
        return sink_class(
            target=self,
            stream_name=stream_name,
            schema={},
            key_properties=[],
        )

    def resolve_sink_class(
        self,
        stream_name: str,
    ) -> type[FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapBaseSink]:
        """Return the appropriate sink class for the stream.

        Args:
            stream_name: Name of the Singer stream to map.

        Returns:
            The sink class handling the stream; the base sink when the
            stream has no dedicated mapping.

        """
        sink_mapping = {
            "users": (
                FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapUsersSink
            ),
            "groups": (
                FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapGroupsSink
            ),
            "organizational_units": (
                FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapOrganizationalUnitsSink
            ),
        }
        sink_class = sink_mapping.get(stream_name)
        if sink_class is None:
            self.logger.warning(
                "No specific sink found for stream '%s', using base sink",
                stream_name,
            )
            return (
                FlextTargetLdapModelsSinks.FlextTargetLdapModels.FlextTargetLdapBaseSink
            )
        self.logger.info(
            "Using %s for stream '%s'",
            sink_class.__name__,
            stream_name,
        )
        return sink_class

    def create_sink(
        self,
        stream_name: str,
        schema: t.JsonMapping,
    ) -> p.Meltano.SingerDrainSink:
        """Create the service-level Singer sink for one stream.

        The facade owns the sink creation (ADR-006); the runtime helper only
        builds the LDAP runtime sink and adapter from the resolved target.

        Args:
            stream_name: Name of the Singer stream the sink drains.
            schema: Flattened Singer schema for the stream.

        Returns:
            The service-level Singer sink for the stream.

        """
        normalized_target_config = u.normalize_to_json_mapping(self.settings)
        normalized_schema = FlextTargetLdapServiceRuntime.normalize_flat_schema(
            schema,
        )
        sink_class = self.resolve_sink_class(stream_name)
        runtime_sink = sink_class(
            target=self,
            stream_name=stream_name,
            schema=normalized_schema,
            key_properties=[],
        )
        return FlextTargetLdapServiceRuntime.Sink.create(
            runtime_sink=runtime_sink,
            target=FlextTargetLdapServiceRuntime.Target(
                config=u.json_dict_adapter().validate_python(normalized_target_config),
                validate_config=False,
            ),
            stream_name=stream_name,
            schema=normalized_schema,
            key_properties=[],
        )

    def setup(self) -> None:
        """Set up the LDAP target."""
        _ = self.orchestrator
        self.logger.info("Orchestrator initialized successfully")
        self._container = self._container_type.shared()
        self.logger.info("DI container initialized successfully")
        validated_settings = FlextTargetLdapSettings.model_validate(self.settings)
        self.logger.info(
            "LDAP target setup completed for host: %s",
            validated_settings.TargetLdap.host,
        )

    def teardown(self) -> None:
        """Teardown the LDAP target."""
        if self._orchestrator:
            self._orchestrator = None
            self.logger.info("Orchestrator cleaned up")
        if self._container is not None:
            self._container = None
            self.logger.info("DI container cleaned up")
        self.logger.info("LDAP target teardown completed")

    def validate_config(self) -> None:
        """Validate the target configuration."""
        _ = FlextTargetLdapSettings.model_validate(self.settings)
        self.logger.info("LDAP target configuration validated successfully")

    @staticmethod
    def _load_config_from_file(config_path: str) -> t.TargetLdap.SettingsPayload:
        """Load configuration from JSON file.

        Args:
            config_path: Path to the JSON configuration file.

        Returns:
            The parsed settings payload from the file.

        Raises:
            RuntimeError: If the configuration file cannot be read or
                parsed as a JSON mapping.

        """
        read = u.Cli.files_read_text(Path(config_path))
        if read.failure:
            msg = f"Failed to load configuration from {config_path}: {read.error}"
            raise RuntimeError(msg)
        try:
            return t.Cli.JSON_MAPPING_ADAPTER.validate_json(read.value)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            msg = f"Failed to load configuration from {config_path}: {exc}"
            raise RuntimeError(msg) from exc

    @staticmethod
    def _construct_dn(
        stream: str,
        record: t.TargetLdap.RecordPayload,
        base_dn: str,
    ) -> str:
        """Construct DN from record based on stream type.

        Args:
            stream: Singer stream name selecting the RDN convention.
            record: Singer record supplying the RDN value.
            base_dn: Base DN appended after the RDN.

        Returns:
            The DN constructed for the record.

        """
        if stream == "users":
            uid = record.get("uid") or record.get("username") or "user"
            return f"uid={uid},{base_dn}"
        if stream == "groups":
            cn = record.get("cn") or record.get("name") or "group"
            return f"cn={cn},{base_dn}"
        name = record.get("name") or "entry"
        return f"cn={name},{base_dn}"

    @staticmethod
    def _process_record_message(
        record: t.TargetLdap.RecordPayload,
        stream: str,
        cfg: t.TargetLdap.SettingsPayload,
        api: FlextTargetLdapClient,
        seen_dns: set[str],
    ) -> None:
        """Process a RECORD message.

        Args:
            record: Singer record payload to write to LDAP.
            stream: Singer stream name used to derive the DN.
            cfg: Flat target settings payload.
            api: LDAP client used to add, modify, or delete entries.
            seen_dns: DNs already written in this run; a repeat switches
                the operation from add to modify.

        """
        dn_value = record.get("dn")
        dn_text = "" if dn_value is None else str(dn_value)
        attributes: t.MutableStrSequenceMapping = {
            key: api.to_str_values(value)
            for key, value in record.items()
            if key not in {"dn", "_sdc_deleted_at"}
        }
        object_classes = attributes.pop("objectClass", None)
        if object_classes is None:
            object_classes = attributes.pop("objectclass", None)
        if not dn_text.strip():
            base_dn_value = cfg.get(c.TargetLdap.KEY_BASE_DN)
            base_dn = (
                base_dn_value
                if isinstance(base_dn_value, str)
                else c.TargetLdap.DEFAULT_BASE_DN
            )
            dn = FlextTargetLdap._construct_dn(stream, record, base_dn)
        else:
            dn = dn_text
        if record.get("_sdc_deleted_at"):
            api.delete_entry(dn)
            return
        try:
            if dn in seen_dns:
                api.modify_entry(dn, attributes)
            else:
                api.add_entry(dn, attributes, object_classes)
                seen_dns.add(dn)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            FlextTargetLdap.logger.warning(
                f"Failed to add entry {dn}, attempting modify: {exc}",
            )
            api.modify_entry(dn, attributes)

    @staticmethod
    def run_cli(settings: str | None = None) -> None:
        """Process Singer JSONL from stdin; echo STATE lines to stdout.

        Args:
            settings: Optional path to a JSON configuration file.

        Raises:
            SINGER_SAFE_EXCEPTIONS: Re-raised after logging when CLI
                processing fails.

        """
        try:
            FlextTargetLdap._run_cli(settings)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS:
            FlextTargetLdap.logger.exception("Unexpected error in CLI execution")
            raise

    cli: ClassVar[Callable[..., None]] = run_cli

    @staticmethod
    def _run_cli(settings: str | None) -> None:
        """Run target CLI processing without owning the exception boundary."""
        cfg: t.TargetLdap.SettingsPayload = (
            FlextTargetLdap._load_config_from_file(settings) if settings else {}
        )
        # NOTE (multi-agent): the Singer config payload is the flat public
        # contract; the client resolves its connection section internally.
        api = FlextTargetLdapClient(cfg)
        current_stream: str | None = None
        seen_dns: set[str] = set()
        for line in sys.stdin:
            current_stream = FlextTargetLdap._process_input_line(
                line,
                current_stream,
                cfg,
                api,
                seen_dns,
            )

    @staticmethod
    def _process_input_line(
        line: str,
        current_stream: str | None,
        settings: t.TargetLdap.SettingsPayload,
        api: FlextTargetLdapClient,
        seen_dns: set[str],
    ) -> str | None:
        """Process one Singer input line and return the current stream.

        Args:
            line: Raw Singer JSONL line from stdin.
            current_stream: Stream name carried over from previous lines.
            settings: Flat target settings payload.
            api: LDAP client used to write RECORD messages.
            seen_dns: DNs already written in this run.

        Returns:
            The stream name to carry forward, or ``None`` when the line
            carries no stream information.

        """
        raw = FlextTargetLdap._parse_input_line(line)
        msg_type = raw.get("type")
        if msg_type == "STATE":
            FlextTargetLdap.logger.debug(line.strip())
            return current_stream
        if msg_type == "SCHEMA":
            raw_stream = raw.get("stream")
            return str(raw_stream) if raw_stream is not None else None
        if msg_type != "RECORD":
            return current_stream
        record_data = raw.get("record", {})
        raw_stream = raw.get("stream")
        stream = (
            str(raw_stream) if raw_stream is not None else (current_stream or "users")
        )
        if not isinstance(record_data, Mapping):
            return current_stream
        normalized_record: t.TargetLdap.MutableRecordPayload = {}
        for key, value in record_data.items():
            normalized_record[key] = value
        FlextTargetLdap._process_record_message(
            normalized_record,
            stream,
            settings,
            api,
            seen_dns,
        )
        return current_stream

    @staticmethod
    def _parse_input_line(line: str) -> t.JsonMapping:
        """Parse one Singer input line.

        Args:
            line: Raw Singer JSONL line from stdin.

        Returns:
            The parsed JSON mapping for the line.

        Raises:
            SINGER_SAFE_EXCEPTIONS: Re-raised after logging when the line
                is not valid JSON.

        """
        try:
            return t.Cli.JSON_MAPPING_ADAPTER.validate_json(line)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS:
            FlextTargetLdap.logger.exception("Malformed input line failed")
            raise


__all__: list[str] = ["FlextTargetLdap"]
