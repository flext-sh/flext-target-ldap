"""Canonical target-ldap facade.

Owns the public ``FlextTargetLdap`` surface. Legacy runtime logic lives here so
``gen-init`` can keep ``api.py`` as the single canonical owner of the facade.
"""

from __future__ import annotations

import sys
from collections.abc import (
    Callable,
    Mapping,
)
from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextContainer
from flext_target_ldap import (
    FlextTargetLdapSettings,
    c,
    p,
    t,
    u,
)
from flext_target_ldap._models.sinks import (
    FlextTargetLdapBaseSink,
    FlextTargetLdapGroupsSink,
    FlextTargetLdapOrganizationalUnitsSink,
    FlextTargetLdapSink,
    FlextTargetLdapTarget,
    FlextTargetLdapUsersSink,
)
from flext_target_ldap._utilities.client import FlextTargetLdapClient
from flext_target_ldap.application.orchestrator import FlextTargetLdapOrchestrator


class FlextTargetLdap(FlextTargetLdapTarget):
    """LDAP target facade for Singer using flext-core patterns."""

    name = "target-ldap"
    config_class = FlextTargetLdapSettings
    settings: t.TargetLdap.SettingsPayload
    _container_type: ClassVar[p.ContainerType] = FlextContainer
    logger: ClassVar[p.Logger] = u.fetch_logger(__name__)

    @override
    def __init__(
        self,
        *,
        settings: t.TargetLdap.SettingsPayload | None = None,
        validate_config: bool = True,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(settings=settings or {}, validate_config=validate_config)
        self._orchestrator: FlextTargetLdapOrchestrator | None = None
        self._container: p.Container | None = None

    @property
    def orchestrator(self) -> FlextTargetLdapOrchestrator:
        """The or create orchestrator."""
        if self._orchestrator is None:
            settings = FlextTargetLdapSettings.model_validate(self.settings)
            self._orchestrator = FlextTargetLdapOrchestrator(settings)
        return self._orchestrator

    @property
    def singer_catalog(self) -> t.TargetLdap.CatalogPayload:
        """The Singer catalog for this target."""
        return u.TargetLdap.build_singer_catalog()

    def get_sink(self, stream_name: str) -> FlextTargetLdapSink:
        """An instantiated sink for the given stream name."""
        sink_class = self.get_sink_class(stream_name)
        return sink_class(
            target=self,
            stream_name=stream_name,
            schema={},
            key_properties=[],
        )

    def get_sink_class(self, stream_name: str) -> type[FlextTargetLdapSink]:
        """The appropriate sink class for the stream."""
        sink_mapping = {
            "users": FlextTargetLdapUsersSink,
            "groups": FlextTargetLdapGroupsSink,
            "organizational_units": FlextTargetLdapOrganizationalUnitsSink,
        }
        sink_class = sink_mapping.get(stream_name)
        if sink_class is None:
            self.logger.warning(
                "No specific sink found for stream '%s', using base sink",
                stream_name,
            )
            return FlextTargetLdapBaseSink
        self.logger.info(f"Using {sink_class.__name__} for stream '{stream_name}'")
        return sink_class

    def setup(self) -> None:
        """Set up the LDAP target."""
        _ = self.orchestrator
        self.logger.info("Orchestrator initialized successfully")
        self._container = self._container_type.shared()
        self.logger.info("DI container initialized successfully")
        validated_settings = FlextTargetLdapSettings.model_validate(self.settings)
        self.logger.info(
            "LDAP target setup completed for host: %s",
            validated_settings.connection.host,
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
        """Load configuration from JSON file."""
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
        """Construct DN from record based on stream type."""
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
        cfg: FlextTargetLdapSettings,
        api: FlextTargetLdapClient,
        seen_dns: set[str],
    ) -> None:
        """Process a RECORD message."""
        dn_value = record.get("dn")
        dn_text = "" if dn_value is None else str(dn_value)
        attributes: dict[str, list[str]] = {
            key: api.to_str_values(value)
            for key, value in record.items()
            if key not in {"dn", "_sdc_deleted_at"}
        }
        object_classes = attributes.pop("objectClass", None)
        if object_classes is None:
            object_classes = attributes.pop("objectclass", None)
        if not dn_text.strip():
            dn = FlextTargetLdap._construct_dn(stream, record, cfg.base_dn)
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
        """Process Singer JSONL; echo STATE lines to stdout."""
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
        validated_settings = FlextTargetLdapSettings.model_validate(cfg)
        current_stream: str | None = None
        api = FlextTargetLdapClient(validated_settings)
        seen_dns: set[str] = set()
        for line in sys.stdin:
            current_stream = FlextTargetLdap._process_input_line(
                line,
                current_stream,
                validated_settings,
                api,
                seen_dns,
            )

    @staticmethod
    def _process_input_line(
        line: str,
        current_stream: str | None,
        settings: FlextTargetLdapSettings,
        api: FlextTargetLdapClient,
        seen_dns: set[str],
    ) -> str | None:
        """Process one Singer input line and return the current stream."""
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
        """Parse one Singer input line."""
        try:
            return t.Cli.JSON_MAPPING_ADAPTER.validate_json(line)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS:
            FlextTargetLdap.logger.exception("Malformed input line failed")
            raise


target_ldap = FlextTargetLdap

__all__: list[str] = [
    "FlextTargetLdap",
    "target_ldap",
]
