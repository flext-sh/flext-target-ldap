"""target-ldap main target class using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping
from contextlib import suppress
from importlib import import_module
from pathlib import Path
from typing import ClassVar, override

from flext_core import FlextLogger
from pydantic import ConfigDict, TypeAdapter, ValidationError

from flext_target_ldap import (
    FlextTargetLdapSettings,
    GroupsSink,
    LDAPBaseSink,
    LDAPTargetOrchestrator,
    OrganizationalUnitsSink,
    Sink,
    Target,
    UsersSink,
    build_singer_catalog,
    c,
    get_flext_target_ldap_container,
    p,
    t,
)

_SINGER_MSG_ADAPTER: TypeAdapter[Mapping[str, t.NormalizedValue]] = TypeAdapter(
    Mapping[str, t.NormalizedValue],
    config=ConfigDict(strict=False),
)


class _DefaultCliHelper:
    """Default CLI helper for printing output."""

    _logger = FlextLogger(__name__)

    def print(self, msg: str) -> None:
        """Print a message."""
        self._logger.info(msg)


def _default_cli_helper(*, quiet: bool = False) -> _DefaultCliHelper:
    """Create a default CLI helper."""
    if quiet:

        class _QuietHelper(_DefaultCliHelper):
            @override
            def print(self, msg: str) -> None:
                self._logger.debug(msg)

        return _QuietHelper()
    return _DefaultCliHelper()


flext_cli_create_helper = _default_cli_helper
logger = FlextLogger(__name__)


_LdapApi = p.TargetLdap.LdapApi


class TargetLDAP(Target):
    """LDAP target for Singer using flext-core patterns."""

    name = "target-ldap"
    config_class = FlextTargetLdapSettings
    config: Mapping[str, t.ContainerValue]
    cli: ClassVar[Callable[..., None] | None] = None

    @override
    def __init__(
        self,
        *,
        config: Mapping[str, t.ContainerValue] | None = None,
        validate_config: bool = True,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(config=config or {}, validate_config=validate_config)
        self._orchestrator: LDAPTargetOrchestrator | None = None
        self._container: p.Container | None = None

    @property
    def orchestrator(self) -> LDAPTargetOrchestrator:
        """Get or create orchestrator."""
        if self._orchestrator is None:
            normalized_config: Mapping[str, str | int | bool] = {}
            for key, value in self.config.items():
                match value:
                    case bool() | int() | str():
                        normalized_config[key] = value
                    case _:
                        normalized_config[key] = str(value)
            self._orchestrator = LDAPTargetOrchestrator(normalized_config)
        return self._orchestrator

    @property
    def singer_catalog(self) -> Mapping[str, t.ContainerValue]:
        """Return the Singer catalog for this target."""
        return build_singer_catalog()

    def get_sink_class(self, stream_name: str) -> type[Sink]:
        """Return the appropriate sink class for the stream."""
        sink_mapping = {
            "users": UsersSink,
            "groups": GroupsSink,
            "organizational_units": OrganizationalUnitsSink,
        }
        sink_class = sink_mapping.get(stream_name)
        if not sink_class:
            logger.warning(
                "No specific sink found for stream '%s', using base sink",
                stream_name,
            )
            return LDAPBaseSink
        logger.info(f"Using {sink_class.__name__} for stream '{stream_name}'")
        return sink_class

    def setup(self) -> None:
        """Set up the LDAP target."""
        _ = self.orchestrator
        logger.info("Orchestrator initialized successfully")
        self._container = get_flext_target_ldap_container()
        logger.info("DI container initialized successfully")
        host = str(self.config.get("host", "localhost"))
        logger.info("LDAP target setup completed for host: %s", host)

    def teardown(self) -> None:
        """Teardown the LDAP target."""
        if self._orchestrator:
            self._orchestrator = None
            logger.info("Orchestrator cleaned up")
        if self._container is not None:
            self._container = None
            logger.info("DI container cleaned up")
        logger.info("LDAP target teardown completed")

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
        port_obj = self.config.get("port", c.TargetLdap.Connection.DEFAULT_PORT)
        try:
            port = int(str(port_obj))
        except (TypeError, ValueError):
            port = c.TargetLdap.Connection.DEFAULT_PORT
        if port <= 0 or port > c.TargetLdap.Connection.MAX_PORT_NUMBER:
            msg = f"LDAP port must be between 1 and {c.TargetLdap.Connection.MAX_PORT_NUMBER}"
            raise ValueError(msg)
        use_ssl = self.config.get("use_ssl", False)
        use_tls = self.config.get("use_tls", False)
        if use_ssl and use_tls:
            msg = "Cannot use both SSL and TLS simultaneously"
            raise ValueError(msg)
        logger.info("LDAP target configuration validated successfully")


def main() -> None:
    """CLI entry point for target-ldap."""
    _target_ldap_flext_cli()


if __name__ == "__main__":
    main()


def _load_config_from_file(config_path: str) -> Mapping[str, t.ContainerValue]:
    """Load configuration from JSON file."""
    config_adapter: TypeAdapter[Mapping[str, t.ContainerValue]] = TypeAdapter(
        Mapping[str, t.ContainerValue],
    )
    try:
        content = Path(config_path).read_text(encoding="utf-8")
        return config_adapter.validate_json(content)
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
        ValidationError,
    ):
        return {}


def _get_ldap_api() -> _LdapApi | None:
    """Get optional LDAP API module."""
    try:
        client_mod = import_module("flext_target_ldap.client")
        return client_mod.get_flext_ldap_api()
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "Failed to load optional LDAP API module",
            error=exc,
            error_type=type(exc).__name__,
        )
        return None


def _construct_dn(
    stream: str,
    record: Mapping[str, t.ContainerValue],
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


def _process_record_message(
    record: Mapping[str, t.ContainerValue],
    stream: str,
    cfg: Mapping[str, t.ContainerValue],
    api: _LdapApi | None,
    seen_dns: set[str],
) -> None:
    """Process a RECORD message."""
    if api is None:
        return
    dn_value = record.get("dn")
    if dn_value is None or not str(dn_value).strip():
        base_dn = str(cfg.get("base_dn", "dc=test,dc=com"))
        dn = _construct_dn(stream, record, base_dn)
    else:
        dn = str(dn_value)
    if record.get("_sdc_deleted_at"):
        with suppress(Exception):
            api.delete(dn)
    else:
        try:
            if dn in seen_dns:
                api.modify(dn, record)
            else:
                api.add(dn, record)
                seen_dns.add(dn)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ):
            with suppress(Exception):
                api.modify(dn, record)


def _target_ldap_flext_cli(config: str | None = None) -> None:
    """Process Singer JSONL; echo STATE lines to stdout."""
    try:
        cfg = _load_config_from_file(config) if config else {}
        current_stream: str | None = None
        api = _get_ldap_api()
        seen_dns: set[str] = set()
        for line in sys.stdin:
            try:
                raw = _SINGER_MSG_ADAPTER.validate_json(line)
                msg_type = raw.get("type")
                if msg_type == "STATE":
                    cli_helper = flext_cli_create_helper(quiet=True)
                    cli_helper.print(line.strip())
                elif msg_type == "SCHEMA":
                    _schema: Mapping[str, t.ContainerValue] = {}
                    current_stream = raw.get("stream")
                elif msg_type == "RECORD" and api is not None:
                    record_data = raw.get("record", {})
                    stream = raw.get("stream") or current_stream or "users"
                    normalized_record: Mapping[str, t.ContainerValue] = {}
                    for key, value in record_data.items():
                        match value:
                            case bool() | int() | float() | str() | dict() | list():
                                normalized_record[str(key)] = value
                            case Path():
                                normalized_record[str(key)] = str(value)
                            case _:
                                normalized_record[str(key)] = str(value)
                    _process_record_message(
                        normalized_record,
                        stream,
                        cfg,
                        api,
                        seen_dns,
                    )
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ):
                logger.debug("Malformed input line skipped in CLI", exc_info=True)
                continue
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
    ):
        logger.debug("Unexpected error in CLI suppressed", exc_info=True)


TargetLDAP.cli = _target_ldap_flext_cli
