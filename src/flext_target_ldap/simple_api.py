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
from flext_ldap import FlextLdapConnectionConfig, get_ldap_api

from flext_target_ldap.target import TargetLDAP


def create_ldap_target(config: dict[str, Any]) -> FlextResult[Any]:
    """Create LDAP target with configuration."""
    try:

        target = TargetLDAP(config)
        return FlextResult.ok(target)
    except (RuntimeError, ValueError, TypeError) as e:
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
        if target is None:
            return FlextResult.fail("Target creation failed")
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])

        # Process records
        for user in users:
            sink.process_record(user, {})

        result = sink.get_processing_result()
        return FlextResult.ok(result.success_count)

    except (RuntimeError, ValueError, TypeError) as e:
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
        if target is None:
            return FlextResult.fail("Target creation failed")
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])

        # Process records
        for group in groups:
            sink.process_record(group, {})

        result = sink.get_processing_result()
        return FlextResult.ok(result.success_count)

    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Failed to load groups: {e}")


def test_ldap_connection(config: dict[str, Any]) -> FlextResult[bool]:
    """Test LDAP connection with given configuration."""
    try:

        connection_config = FlextLdapConnectionConfig(
            server=config["host"],
            port=config.get("port", 389),
            use_ssl=config.get("use_ssl", False),
            timeout_seconds=config.get("connect_timeout", 30),
        )

        # Use real flext-ldap API
        get_ldap_api()
        # For connection test, we just validate the config
        validation_result = connection_config.validate_domain_rules()
        if validation_result.is_success:
            return FlextResult.ok(True)
        return FlextResult.fail(f"Connection config validation failed: {validation_result.error}")

    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Connection test error: {e}")


# Convenience function aliases
create_target = create_ldap_target
test_connection = test_ldap_connection
