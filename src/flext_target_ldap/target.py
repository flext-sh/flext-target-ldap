"""target-ldap main target class using flext-core patterns.

REFACTORED:
Uses flext-core configuration patterns for robust LDAP target implementation.
Zero tolerance for code duplication.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from flext_core import FlextContainer, get_logger

# CONSOLIDATED: Use centralized Singer SDK from flext-meltano
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano import Target

# Import from new modular architecture
from flext_target_ldap.application import LDAPTargetOrchestrator
from flext_target_ldap.config import TargetLDAPConfig
from flext_target_ldap.infrastructure import get_flext_target_ldap_container
from flext_target_ldap.sinks import (
    GroupsSink,
    OrganizationalUnitsSink,
    UsersSink,
)

if TYPE_CHECKING:
    from flext_meltano import Sink

logger = get_logger(__name__)


class TargetLDAP(Target):
    """LDAP target for Singer using flext-core patterns."""

    name = "target-ldap"
    config_class = TargetLDAPConfig

    def __init__(
        self,
        config: dict[str, object] | None = None,
        validate_config: bool = True,
    ) -> None:
        """Initialize LDAP target."""
        super().__init__(config=config, validate_config=validate_config)

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
    def singer_catalog(self) -> dict[str, object]:
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
                f"No specific sink found for stream '{stream_name}', using base sink",
            )
            # Return UsersSink as default - could create a GenericSink if needed
            return UsersSink

        logger.info(f"Using {sink_class.__name__} for stream '{stream_name}'")
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

        port = self.config.get("port", 389)
        if port <= 0 or port > 65535:
            msg = "LDAP port must be between 1 and 65535"
            raise ValueError(msg)

        use_ssl = self.config.get("use_ssl", False)
        use_tls = self.config.get("use_tls", False)
        if use_ssl and use_tls:
            msg = "Cannot use both SSL and TLS simultaneously"
            raise ValueError(msg)

        logger.info("LDAP target configuration validated successfully")

    def setup(self) -> None:
        """Setup the LDAP target."""
        # Initialize orchestrator
        _ = self.orchestrator  # Ensure orchestrator is created
        logger.info("Orchestrator initialized successfully")

        # Initialize DI container
        self._container = get_flext_target_ldap_container()
        logger.info("DI container initialized successfully")

        host = self.config.get("host", "localhost")
        logger.info(f"LDAP target setup completed for host: {host}")

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
    # from flext_meltano import target_test_runner  # Not available

    # Basic CLI support
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        return

    # Run the target
    target = TargetLDAP()
    # target_test_runner(target)  # Not available - use Singer SDK directly
    target.cli()


if __name__ == "__main__":
    main()
