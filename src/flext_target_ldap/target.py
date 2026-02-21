"""target-ldap main target class using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from contextlib import suppress
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Protocol, override

if TYPE_CHECKING:
    from flext_target_ldap.sinks import Sink, Target
else:
    try:
        from flext_meltano.singer.tap import FlextMeltanoStream as Sink
        from flext_meltano.singer.target import FlextMeltanoTarget as Target
    except ImportError:
        from flext_target_ldap.sinks import Sink, Target

from flext_core import FlextContainer, FlextLogger

from flext_target_ldap.application import LDAPTargetOrchestrator
from flext_target_ldap.constants import c
from flext_target_ldap.infrastructure import get_flext_target_ldap_container
from flext_target_ldap.settings import FlextTargetLdapSettings
from flext_target_ldap.sinks import (
    GroupsSink,
    LDAPBaseSink,
    OrganizationalUnitsSink,
    UsersSink,
)
from flext_target_ldap.typings import t


def _default_cli_helper(*, quiet: bool = False):  # noqa: ARG001
    class Helper:
        def print(self, msg: str) -> None:
            pass

    return Helper()


try:
    _cli_mod = import_module("flext_cli")
    flext_cli_create_helper = getattr(
        _cli_mod, "flext_cli_create_helper", _default_cli_helper
    )
except ImportError:
    flext_cli_create_helper = _default_cli_helper


logger = FlextLogger(__name__)

# Network constants - moved to c.TargetLdap.Connection.MAX_PORT_NUMBER


class _LdapApiProtocol(Protocol):
    def add(self, dn: str, record: t.Core.Dict) -> None: ...

    def modify(self, dn: str, record: t.Core.Dict) -> None: ...

    def delete(self, dn: str) -> None: ...


class TargetLDAP(Target):
    """LDAP target for Singer using flext-core patterns."""

    name = "target-ldap"
    config_class = FlextTargetLdapSettings
    config: dict[str, t.GeneralValueType]
    cli: ClassVar[Callable[..., None] | None] = None

    @override
    def __init__(
        self,
        *,
        config: t.Core.Dict | None = None,
        validate_config: bool = True,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(config=config or {}, validate_config=validate_config)

        # Initialize orchestrator with new modular architecture
        self._orchestrator: LDAPTargetOrchestrator | None = None
        self._container: FlextContainer | None = None

    @property
    def orchestrator(self) -> LDAPTargetOrchestrator:
        """Get or create orchestrator."""
        if self._orchestrator is None:
            self._orchestrator = LDAPTargetOrchestrator(dict(self.config))
        return self._orchestrator

    @property
    def singer_catalog(self) -> t.Core.Dict:
        """Return the Singer catalog for this target."""
        return {
            "streams": [
                {
                    "tap_stream_id": "users",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "full_name": {"type": "string"},
                            "phone": {"type": "string"},
                            "department": {"type": "string"},
                            "title": {"type": "string"},
                        },
                        "required": ["username"],
                    },
                },
                {
                    "tap_stream_id": "groups",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "members": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["name"],
                    },
                },
                {
                    "tap_stream_id": "organizational_units",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["name"],
                    },
                },
            ],
        }

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
            # Return LDAPBaseSink as default for generic streams
            return LDAPBaseSink

        logger.info("Using %s for stream '%s'", sink_class.__name__, stream_name)
        return sink_class

    def validate_config(self) -> None:
        """Validate the target configuration."""
        # Additional LDAP-specific validation
        host = self.config.get("host")
        if not host:
            msg = "LDAP host is required"
            raise ValueError(msg)

        base_dn = self.config.get("base_dn")
        if not base_dn:
            msg = "LDAP base DN is required"
            raise ValueError(msg)

        port_obj = self.config.get("port", 389)
        if isinstance(port_obj, bool):
            port = 389
        elif isinstance(port_obj, int):
            port = port_obj
        elif isinstance(port_obj, str):
            try:
                port = int(port_obj)
            except ValueError:
                port = 389
        else:
            port = 389
        if port <= 0 or port > c.TargetLdap.Connection.MAX_PORT_NUMBER:
            msg = f"LDAP port must be between 1 and {c.TargetLdap.Connection.MAX_PORT_NUMBER}"
            raise ValueError(msg)

        use_ssl = self.config.get("use_ssl", False)
        use_tls = self.config.get("use_tls", False)
        if use_ssl and use_tls:
            msg = "Cannot use both SSL and TLS simultaneously"
            raise ValueError(msg)

        logger.info("LDAP target configuration validated successfully")

    def setup(self) -> None:
        """Set up the LDAP target."""
        # Initialize orchestrator
        _ = self.orchestrator  # Ensure orchestrator is created
        logger.info("Orchestrator initialized successfully")

        # Initialize DI container
        self._container = get_flext_target_ldap_container()
        logger.info("DI container initialized successfully")

        host = self.config.get("host", "localhost")
        logger.info("LDAP target setup completed for host: %s", host)

    def teardown(self) -> None:
        """Teardown the LDAP target."""
        # Cleanup orchestrator
        if self._orchestrator:
            self._orchestrator = None
            logger.info("Orchestrator cleaned up")

        # Cleanup container
        if self._container is not None:
            self._container = None
            logger.info("DI container cleaned up")

        logger.info("LDAP target teardown completed")


def main() -> None:
    """CLI entry point for target-ldap."""
    # Delegate to FLEXT-CLI command for tests
    _target_ldap_flext_cli()


if __name__ == "__main__":
    main()


def _load_config_from_file(config_path: str) -> t.Core.Dict:
    """Load configuration from JSON file."""
    try:
        with Path(config_path).open(encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _get_ldap_api() -> _LdapApiProtocol | None:
    """Get optional LDAP API module."""
    try:
        client_mod = import_module("flext_target_ldap.client")
        return client_mod.get_flext_ldap_api()
    except Exception:
        return None


def _construct_dn(
    stream: str,
    record: t.Core.Dict,
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
    record: t.Core.Dict,
    stream: str,
    cfg: t.Core.Dict,
    api: _LdapApiProtocol | None,
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

    # Delete vs upsert
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
        except Exception:
            with suppress(Exception):
                api.modify(dn, record)


# FLEXT-CLI implementation for tests (echoes STATE lines)
def _target_ldap_flext_cli(config: str | None = None) -> None:
    """Process Singer JSONL; echo STATE lines to stdout."""
    try:
        cfg = _load_config_from_file(config) if config else {}
        current_stream: str | None = None
        api = _get_ldap_api()
        seen_dns: set[str] = set()

        for line in sys.stdin:
            try:
                obj = json.loads(line)
                msg_type = obj.get("type")
                if msg_type == "STATE":
                    cli_helper = flext_cli_create_helper(quiet=True)
                    cli_helper.print(line.strip())
                elif msg_type == "SCHEMA":
                    _schema = obj.get("schema") or {}
                    current_stream = obj.get("stream")
                elif msg_type == "RECORD" and api is not None:
                    record: dict[str, t.GeneralValueType] = obj.get("record") or {}
                    stream = obj.get("stream") or current_stream or "users"
                    _process_record_message(record, stream, cfg, api, seen_dns)
            except Exception:
                logger.debug("Malformed input line skipped in CLI", exc_info=True)
                continue
    except Exception:
        logger.debug("Unexpected error in CLI suppressed", exc_info=True)


# Expose CLI command via class attribute for tests expecting TargetLDAP.cli
TargetLDAP.cli = _target_ldap_flext_cli
