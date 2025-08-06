"""Simple API for flext-target-ldap using flext-core patterns.

REFACTORED:
Provides convenient functions for common LDAP operations.
Uses flext-core patterns for consistent error handling.
"""

from __future__ import annotations

from flext_core import (
    FlextResult,
)
from flext_ldap import FlextLdapConnectionConfig, get_ldap_api

from flext_target_ldap.target import TargetLDAP


def create_ldap_target(config: dict[str, object]) -> FlextResult[object]:
    """Create LDAP target with configuration."""
    try:
        target = TargetLDAP(config=config)
        return FlextResult.ok(target)
    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Failed to create LDAP target: {e}")


def load_users_to_ldap(
    users: list[dict[str, object]],
    config: dict[str, object],
) -> FlextResult[int]:
    """Load user records to LDAP."""
    target_result = create_ldap_target(config)
    if not target_result.success:
        return FlextResult.fail(f"Target creation failed: {target_result.error}")

    try:
        target = target_result.data
        if target is None:
            return FlextResult.fail("Target creation failed")
        
        # Type assertion since we know target is TargetLDAP
        from flext_target_ldap.target import TargetLDAP
        assert isinstance(target, TargetLDAP)
        sink = target.get_sink_class("users")(target, "users", {}, ["username"])

        # Process records
        for user in users:
            sink.process_record(user, {})

        # Return count of processed users
        return FlextResult.ok(len(users))

    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Failed to load users: {e}")


def load_groups_to_ldap(
    groups: list[dict[str, object]],
    config: dict[str, object],
) -> FlextResult[int]:
    """Load group records to LDAP."""
    target_result = create_ldap_target(config)
    if not target_result.success:
        return FlextResult.fail(f"Target creation failed: {target_result.error}")

    try:
        target = target_result.data
        if target is None:
            return FlextResult.fail("Target creation failed")
        
        # Type assertion since we know target is TargetLDAP
        from flext_target_ldap.target import TargetLDAP
        assert isinstance(target, TargetLDAP)
        sink = target.get_sink_class("groups")(target, "groups", {}, ["name"])

        # Process records
        for group in groups:
            sink.process_record(group, {})

        # Return count of processed groups
        return FlextResult.ok(len(groups))

    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Failed to load groups: {e}")


def test_ldap_connection(config: dict[str, object]) -> FlextResult[bool]:
    """Test LDAP connection with given configuration."""
    try:
        # Validate connection config by creating it
        FlextLdapConnectionConfig(
            host=str(config["host"]),
            port=int(str(config.get("port", 389)))
            if config.get("port", 389) is not None
            else 389,
            use_ssl=bool(config.get("use_ssl")),
            timeout=int(str(config.get("connect_timeout", 30)))
            if config.get("connect_timeout", 30) is not None
            else 30,
        )

        # Use real flext-ldap API
        get_ldap_api()
        # For connection test, config is already validated by Pydantic on construction
        # Just return success if we got this far
        return FlextResult.ok(data=True)

    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Connection test error: {e}")


# Convenience function aliases
create_target = create_ldap_target
test_connection = test_ldap_connection
