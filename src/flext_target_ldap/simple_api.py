"""Simple API for flext-target-ldap using flext-core patterns.

REFACTORED:
Provides convenient functions for common LDAP operations.
Uses flext-core patterns for consistent error handling.
"""

from __future__ import annotations

from typing import Any

# Import from flext-core for foundational patterns
from flext_core import (
    FlextResult,
)


def create_ldap_target(config: dict[str, Any]) -> FlextResult[Any]:
    """Create LDAP target with configuration."""
    try:
        from flext_target_ldap.target import TargetLDAP

        target = TargetLDAP(config)
        return FlextResult.ok(target)
    except Exception as e:
        return FlextResult.fail(f"Failed to create LDAP target: {e}")


def load_users_to_ldap(
    users: list[dict[str, Any]],
    config: dict[str, Any],
) -> FlextResult[int]:
    """Load user records to LDAP."""
    target_result = create_ldap_target(config)
    if not target_result.is_success:
        return FlextResult.fail(f"Target creation failed: {target_result.error}")

    try:
        target = target_result.data
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])

        # Process records
        for user in users:
            sink.process_record(user)

        result = sink.get_processing_result()
        return FlextResult.ok(result.success_count)

    except Exception as e:
        return FlextResult.fail(f"Failed to load users: {e}")


def load_groups_to_ldap(
    groups: list[dict[str, Any]],
    config: dict[str, Any],
) -> FlextResult[int]:
    """Load group records to LDAP."""
    target_result = create_ldap_target(config)
    if not target_result.is_success:
        return FlextResult.fail(f"Target creation failed: {target_result.error}")

    try:
        target = target_result.data
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])

        # Process records
        for group in groups:
            sink.process_record(group)

        result = sink.get_processing_result()
        return FlextResult.ok(result.success_count)

    except Exception as e:
        return FlextResult.fail(f"Failed to load groups: {e}")


def test_ldap_connection(config: dict[str, Any]) -> FlextResult[bool]:
    """Test LDAP connection with given configuration."""
    try:
        from flext_target_ldap.client import LDAPClient, LDAPConnectionConfig

        connection_config = LDAPConnectionConfig(
            host=config["host"],
            port=config.get("port", 389),
            use_ssl=config.get("use_ssl", False),
            use_tls=config.get("use_tls", False),
            bind_dn=config.get("bind_dn"),
            bind_password=config.get("bind_password"),
            base_dn=config["base_dn"],
            connect_timeout=config.get("connect_timeout", 10),
            receive_timeout=config.get("receive_timeout", 30),
        )

        client = LDAPClient(connection_config)
        connect_result = client.connect()

        if connect_result.is_success:
            client.disconnect()
            return FlextResult.ok(True)
        return FlextResult.fail(f"Connection test failed: {connect_result.error}")

    except Exception as e:
        return FlextResult.fail(f"Connection test error: {e}")


# Convenience function aliases
create_target = create_ldap_target
test_connection = test_ldap_connection
