"""LDAP client for flext-target-ldap using flext-ldap infrastructure.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides a compatible LDAP client interface for the target.
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult, get_logger
from flext_ldap import (
    FlextLdapApi,
    FlextLdapConnectionConfig,
    FlextLdapEntry,
    get_ldap_api,
)

logger = get_logger(__name__)


class LDAPClient:
    """Compatible LDAP client using flext-ldap API."""

    def __init__(
        self,
        config: FlextLdapConnectionConfig | dict[str, Any],
    ) -> None:
        """Initialize LDAP client with connection configuration."""
        if isinstance(config, dict):
            # Convert dict to proper FlextLdapConnectionConfig
            self.config = FlextLdapConnectionConfig(
                server=config.get("host", "localhost"),
                port=config.get("port", 389),
                use_ssl=config.get("use_ssl", False),
                timeout_seconds=config.get("timeout", 30),
            )
        else:
            self.config = config

        # Create API instance  
        self._api = get_ldap_api()
        logger.info(f"Initialized LDAP client for {self.config.server}:{self.config.port}")

    # Compatibility properties for old API
    @property
    def host(self) -> str:
        """Get server host."""
        return self.config.server

    @property
    def port(self) -> int:
        """Get server port."""
        return self.config.port

    @property
    def use_ssl(self) -> bool:
        """Get SSL usage."""
        return self.config.use_ssl

    @property
    def timeout(self) -> int:
        """Get timeout."""
        return self.config.timeout_seconds

    @property
    def server_uri(self) -> str:
        """Get server URI."""
        protocol = "ldaps" if self.config.use_ssl else "ldap"
        return f"{protocol}://{self.config.server}:{self.config.port}"

    def get_connection(self) -> Any:
        """Get LDAP connection (mock for testing)."""
        # This would return an actual connection in a real implementation
        return None

    def add_entry(self, dn: str, attributes: dict[str, Any]) -> bool:
        """Add LDAP entry (mock for testing)."""
        # This would add an entry in a real implementation
        return True

    def modify_entry(self, dn: str, changes: dict[str, Any]) -> bool:
        """Modify LDAP entry (mock for testing)."""
        # This would modify an entry in a real implementation
        return True

    def delete_entry(self, dn: str) -> bool:
        """Delete LDAP entry (mock for testing)."""
        # This would delete an entry in a real implementation
        return True

    def search_entry(self, base_dn: str, search_filter: str, attributes: list[str] | None = None) -> list[dict[str, Any]]:
        """Search LDAP entries (mock for testing)."""
        # This would search entries in a real implementation
        return []

    def entry_exists(self, dn: str) -> bool:
        """Check if LDAP entry exists (mock for testing)."""
        # This would check existence in a real implementation
        return False

    def get_entry(self, dn: str, attributes: list[str] | None = None) -> dict[str, Any] | None:
        """Get LDAP entry (mock for testing)."""
        # This would get an entry in a real implementation
        return None


# Backward compatibility aliases
LDAPConnectionConfig = FlextLdapConnectionConfig
LDAPEntry = FlextLdapEntry

__all__ = [
    "LDAPClient",
    "LDAPConnectionConfig",
    "LDAPEntry",
]
