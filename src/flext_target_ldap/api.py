"""Canonical target-ldap facade.

Owns the public ``FlextTargetLdap`` surface. Legacy runtime logic lives here so
``gen-init`` can keep ``api.py`` as the single canonical owner of the facade.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextContainer, FlextLogger
from flext_target_ldap import (
    FlextTargetLdapBaseSink,
    FlextTargetLdapClient,
    FlextTargetLdapGroupsSink,
    FlextTargetLdapOrchestrator,
    FlextTargetLdapOrganizationalUnitsSink,
    FlextTargetLdapSettings,
    FlextTargetLdapSink,
    FlextTargetLdapTarget,
    FlextTargetLdapUsersSink,
    c,
    p,
    t,
    u,
)


class FlextTargetLdap(FlextTargetLdapTarget):
    """LDAP target facade for Singer using flext-core patterns."""

    class _DefaultCliHelper:
        """Default CLI helper for printing output."""

        _logger = FlextLogger(__name__)

        def print(self, msg: str) -> None:
            """Print a message."""
            self._logger.info(msg)

    class _QuietCliHelper(_DefaultCliHelper):
        """Quiet CLI helper for state messages."""

        @override
        def print(self, msg: str) -> None:
            """Print a message at debug level."""
            self._logger.debug(msg)

    name = "target-ldap"
    config_class = FlextTargetLdapSettings
    config: t.ContainerValueMapping
    _logger: ClassVar[FlextLogger] = FlextLogger(__name__)

    @override
    def __init__(
        self,
        *,
        config: t.ContainerValueMapping | None = None,
        validate_config: bool = True,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(config=config or {}, validate_config=validate_config)
        self._orchestrator: FlextTargetLdapOrchestrator | None = None
        self._container: p.Container | None = None

    @property
    def orchestrator(self) -> FlextTargetLdapOrchestrator:
        """Get or create orchestrator."""
        if self._orchestrator is None:
            normalized_config: t.MutableScalarMapping = {}
            for key, value in self.config.items():
                match value:
                    case bool() | int() | str():
                        normalized_config[key] = value
                    case _:
                        normalized_config[key] = (
                            t.TargetLdap.STRING_ADAPTER.validate_python(value)
                        )
            settings = FlextTargetLdapSettings.model_validate(normalized_config)
            self._orchestrator = FlextTargetLdapOrchestrator(settings)
        return self._orchestrator

    @property
    def singer_catalog(self) -> t.ContainerValueMapping:
        """Return the Singer catalog for this target."""
        return u.TargetLdap.build_singer_catalog()

    def get_sink(self, stream_name: str) -> FlextTargetLdapSink:
        """Return an instantiated sink for the given stream name."""
        sink_class = self.get_sink_class(stream_name)
        return sink_class(
            target=self,
            stream_name=stream_name,
            schema={},
            key_properties=[],
        )

    def get_sink_class(self, stream_name: str) -> type[FlextTargetLdapSink]:
        """Return the appropriate sink class for the stream."""
        sink_mapping = {
            "users": FlextTargetLdapUsersSink,
            "groups": FlextTargetLdapGroupsSink,
            "organizational_units": FlextTargetLdapOrganizationalUnitsSink,
        }
        sink_class = sink_mapping.get(stream_name)
        if sink_class is None:
            self._logger.warning(
                "No specific sink found for stream '%s', using base sink",
                stream_name,
            )
            return FlextTargetLdapBaseSink
        self._logger.info(f"Using {sink_class.__name__} for stream '{stream_name}'")
        return sink_class

    def setup(self) -> None:
        """Set up the LDAP target."""
        _ = self.orchestrator
        self._logger.info("Orchestrator initialized successfully")
        self._container = FlextContainer.get_global()
        self._logger.info("DI container initialized successfully")
        host = u.TargetLdap.TypeConversion.to_str(
            self.config.get("host", "localhost"),
            default="localhost",
        )
        self._logger.info("LDAP target setup completed for host: %s", host)

    def teardown(self) -> None:
        """Teardown the LDAP target."""
        if self._orchestrator:
            self._orchestrator = None
            self._logger.info("Orchestrator cleaned up")
        if self._container is not None:
            self._container = None
            self._logger.info("DI container cleaned up")
        self._logger.info("LDAP target teardown completed")

    def validate_config(self) -> None:
        """Validate the target configuration."""
        host = self.config.get("host")
        if not host:
            msg = "LDAP host is required"
            raise ValueError(msg)
        base_dn = self.config.get("base_dn")
        if not base_dn:
            msg = "LDAP base DN is required"
            raise ValueError(msg)
        port_obj = self.config.get("port", c.Ldap.ConnectionDefaults.PORT)
        try:
            port = t.TargetLdap.INTEGER_ADAPTER.validate_python(port_obj)
        except Exception:
            port = c.Ldap.ConnectionDefaults.PORT
        if port <= 0 or port > c.MAX_PORT_NUMBER:
            msg = f"LDAP port must be between 1 and {c.MAX_PORT_NUMBER}"
            raise ValueError(msg)
        use_ssl = self.config.get("use_ssl", False)
        use_tls = self.config.get("use_tls", False)
        if use_ssl and use_tls:
            msg = "Cannot use both SSL and TLS simultaneously"
            raise ValueError(msg)
        self._logger.info("LDAP target configuration validated successfully")

    @staticmethod
    def _create_cli_helper(*, quiet: bool = False) -> FlextTargetLdap._DefaultCliHelper:
        """Create a CLI helper instance."""
        if quiet:
            return FlextTargetLdap._QuietCliHelper()
        return FlextTargetLdap._DefaultCliHelper()

    @staticmethod
    def _load_config_from_file(config_path: str) -> t.ContainerValueMapping:
        """Load configuration from JSON file."""
        try:
            content = Path(config_path).read_text(encoding="utf-8")
            return t.TargetLdap.CONTAINER_VALUE_MAP_ADAPTER.validate_json(content)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            msg = f"Failed to load configuration from {config_path}: {exc}"
            raise RuntimeError(msg) from exc

    @staticmethod
    def _get_ldap_api(
        config: t.ContainerValueMapping,
    ) -> FlextTargetLdapClient | None:
        """Get LDAP target client backed by flext-ldap."""
        try:
            return FlextTargetLdapClient(config=config)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            FlextTargetLdap._logger.warning(
                "Failed to initialize LDAP target client",
                error=exc,
                error_type=type(exc).__name__,
            )
            return None

    @staticmethod
    def _construct_dn(
        stream: str,
        record: t.ContainerValueMapping,
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
        record: t.ContainerValueMapping,
        stream: str,
        cfg: t.ContainerValueMapping,
        api: FlextTargetLdapClient | None,
        seen_dns: set[str],
    ) -> None:
        """Process a RECORD message."""
        if api is None:
            return
        dn_value = record.get("dn")
        dn_text = (
            "" if dn_value is None else u.TargetLdap.TypeConversion.to_str(dn_value)
        )
        if not dn_text.strip():
            base_dn = u.TargetLdap.TypeConversion.to_str(
                cfg.get("base_dn", "dc=test,dc=com"),
                default="dc=test,dc=com",
            )
            dn = FlextTargetLdap._construct_dn(stream, record, base_dn)
        else:
            dn = dn_text
        if record.get("_sdc_deleted_at"):
            api.delete_entry(dn)
            return
        try:
            if dn in seen_dns:
                api.modify_entry(dn, record)
            else:
                api.add_entry(dn, record)
                seen_dns.add(dn)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            FlextTargetLdap._logger.warning(
                f"Failed to add entry {dn}, attempting modify: {exc}"
            )
            api.modify_entry(dn, record)

    @staticmethod
    def run_cli(config: str | None = None) -> None:
        """Process Singer JSONL; echo STATE lines to stdout."""
        try:
            cfg: t.ContainerValueMapping = (
                FlextTargetLdap._load_config_from_file(config) if config else {}
            )
            current_stream: str | None = None
            api = FlextTargetLdap._get_ldap_api(cfg)
            seen_dns: set[str] = set()
            for line in sys.stdin:
                try:
                    raw = t.TargetLdap.SINGER_MESSAGE_ADAPTER.validate_json(line)
                    msg_type = raw.get("type")
                    if msg_type == "STATE":
                        cli_helper = FlextTargetLdap._create_cli_helper(quiet=True)
                        cli_helper.print(line.strip())
                        continue
                    if msg_type == "SCHEMA":
                        raw_stream = raw.get("stream")
                        current_stream = (
                            str(raw_stream) if raw_stream is not None else None
                        )
                        continue
                    if msg_type != "RECORD" or api is None:
                        continue
                    record_data = raw.get("record", {})
                    raw_stream = raw.get("stream")
                    stream = (
                        str(raw_stream)
                        if raw_stream is not None
                        else (current_stream or "users")
                    )
                    if not isinstance(record_data, Mapping):
                        continue
                    normalized_record: t.MutableContainerValueMapping = {}
                    for key, value in record_data.items():
                        match value:
                            case bool() | int() | float() | str():
                                normalized_record[str(key)] = value
                            case Path():
                                normalized_record[str(key)] = str(value)
                            case _:
                                normalized_record[str(key)] = str(value)
                    FlextTargetLdap._process_record_message(
                        normalized_record,
                        stream,
                        cfg,
                        api,
                        seen_dns,
                    )
                except c.Meltano.SINGER_SAFE_EXCEPTIONS:
                    FlextTargetLdap._logger.exception("Malformed input line failed")
                    raise
        except c.Meltano.SINGER_SAFE_EXCEPTIONS:
            FlextTargetLdap._logger.exception("Unexpected error in CLI execution")
            raise

    cli: ClassVar[Callable[..., None]] = run_cli


target_ldap = FlextTargetLdap
