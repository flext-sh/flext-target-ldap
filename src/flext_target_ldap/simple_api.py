"""Simple API for FLEXT target-ldap setup and configuration using flext-core patterns.

MIGRATED TO FLEXT-CORE:
Provides enterprise-ready setup utilities with ServiceResult pattern support.
"""

from __future__ import annotations

from typing import Any

from flext_target_ldap.client import ServiceResult
from flext_target_ldap.config import TargetLDAPConfig


def setup_ldap_target(config: TargetLDAPConfig | None = None) -> ServiceResult[TargetLDAPConfig]:
    """Setup LDAP target with configuration.

    Args:
        config: Optional configuration. If None, creates defaults.

    Returns:
        ServiceResult with TargetLDAPConfig or error message.

    """
    try:
        if config is None:
            # Create with intelligent defaults
            config = create_development_ldap_target_config()

        # Validate configuration
        config.model_validate(config.model_dump())

        return ServiceResult.ok(config)

    except Exception as e:
        return ServiceResult.fail(f"Failed to setup LDAP target: {e}")


def create_development_ldap_target_config(**overrides: Any) -> TargetLDAPConfig:
    """Create development LDAP target configuration with defaults.

    Args:
        **overrides: Configuration overrides

    Returns:
        TargetLDAPConfig for development use.

    """
    defaults: dict[str, Any] = {
        "host": "localhost",
        "port": 389,
        "bind_dn": "cn=admin,dc=example,dc=com",
        "password": "admin",
        "base_dn": "dc=example,dc=com",
        "use_ssl": False,
        "timeout": 30,
        "validate_records": True,
        "user_rdn_attribute": "uid",
        "group_rdn_attribute": "cn",
        "dry_run_mode": True,
        "batch_size": 50,
        "max_errors": 50,
        "enable_validation": True,
        "validation_strict_mode": False,
    }

    # Override with provided values
    defaults.update(overrides)

    return TargetLDAPConfig(**defaults)


def create_production_ldap_target_config(**overrides: Any) -> TargetLDAPConfig:
    """Create production LDAP target configuration with security defaults.

    Args:
        **overrides: Configuration overrides

    Returns:
        TargetLDAPConfig for production use.

    """
    defaults: dict[str, Any] = {
        "host": "ldap.company.com",
        "port": 636,
        "use_ssl": True,
        "timeout": 60,
        "validate_records": True,
        "user_rdn_attribute": "uid",
        "group_rdn_attribute": "cn",
        "dry_run_mode": False,
        "batch_size": 100,
        "max_errors": 10,
        "enable_validation": True,
        "validation_strict_mode": True,
        "parallel_processing": False,
        "ignore_transformation_errors": False,
    }

    # Override with provided values
    defaults.update(overrides)

    return TargetLDAPConfig(**defaults)


def create_migration_ldap_target_config(
    oracle_mode: bool = True,
    **overrides: Any,
) -> TargetLDAPConfig:
    """Create LDAP target configuration optimized for Oracle migrations.

    Args:
        oracle_mode: Enable Oracle-specific migration optimizations
        **overrides: Configuration overrides

    Returns:
        TargetLDAPConfig optimized for migrations.

    """
    defaults: dict[str, Any] = {
        "use_ssl": True,
        "timeout": 120,
        "validate_records": True,
        "oracle_migration_mode": oracle_mode,
        "preserve_original_attributes": True,
        "enable_transformation": True,
        "enable_validation": True,
        "validation_strict_mode": False,
        "dry_run_mode": False,
        "batch_size": 200,
        "parallel_processing": True,
        "max_errors": 100,
        "ignore_transformation_errors": True,
    }

    # Override with provided values
    defaults.update(overrides)

    return TargetLDAPConfig(**defaults)


def validate_ldap_target_config(config: TargetLDAPConfig) -> ServiceResult[bool]:
    """Validate LDAP target configuration.

    Args:
        config: Configuration to validate

    Returns:
        ServiceResult with validation success or error message.

    """
    try:
        # Validate using Pydantic model validation
        config.model_validate(config.model_dump())

        # Additional business rule validations
        if not config.host:
            return ServiceResult.fail("Host is required")

        if not config.base_dn:
            return ServiceResult.fail("Base DN is required")

        if config.port <= 0 or config.port > 65535:
            return ServiceResult.fail("Port must be between 1 and 65535")

        if config.timeout <= 0:
            return ServiceResult.fail("Timeout must be positive")

        if config.batch_size <= 0:
            return ServiceResult.fail("Batch size must be positive")

        return ServiceResult.ok(True)

    except Exception as e:
        return ServiceResult.fail(f"Configuration validation failed: {e}")


def create_test_connection_config(**overrides: Any) -> TargetLDAPConfig:
    """Create configuration for testing LDAP connections.

    Args:
        **overrides: Configuration overrides

    Returns:
        TargetLDAPConfig optimized for connection testing.

    """
    defaults: dict[str, Any] = {
        "host": "localhost",
        "port": 389,
        "bind_dn": "cn=admin,dc=test,dc=com",
        "password": "test",
        "base_dn": "dc=test,dc=com",
        "use_ssl": False,
        "timeout": 10,
        "validate_records": False,
        "dry_run_mode": True,
        "batch_size": 1,
        "max_errors": 1,
        "enable_validation": False,
    }

    # Override with provided values
    defaults.update(overrides)

    return TargetLDAPConfig(**defaults)


# Export convenience functions
__all__ = [
    "ServiceResult",
    "create_development_ldap_target_config",
    "create_migration_ldap_target_config",
    "create_production_ldap_target_config",
    "create_test_connection_config",
    "setup_ldap_target",
    "validate_ldap_target_config",
]
