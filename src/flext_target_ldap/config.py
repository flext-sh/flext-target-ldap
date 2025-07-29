"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
Uses flext-core patterns for declarative configuration.
Zero tolerance for code duplication.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

# Import from flext-core for foundational patterns
from flext_core import (
    FlextResult,
    FlextValueObject as FlextDomainBaseModel,
)

# Import real LDAP connection config from flext-ldap (no fallbacks)
from pydantic import Field
from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from flext_ldap import FlextLdapConnectionConfig

# No TYPE_CHECKING imports needed - FlextLdapConnectionConfig already imported

# Compatibility warning for Singer adapters migration
warnings.warn(
    "🔄 ARCHITECTURE EVOLUTION: Singer adapters moved from flext-core to flext-meltano.\n"
    "💡 FUTURE PLAN: Use flext_meltano.config.SingerTargetConfig\n"
    "⚡ CURRENT: Temporary compatibility using BaseSettings",
    DeprecationWarning,
    stacklevel=2,
)


class TargetLDAPConfig(BaseSettings):
    """LDAP target configuration using consolidated patterns."""

    # Use real LDAP connection config from flext-ldap - no duplications
    connection: FlextLdapConnectionConfig = Field(
        ..., description="LDAP connection configuration",
    )

    # Target-specific settings (not duplicated)
    base_dn: str = Field(
        ..., description="Base DN for LDAP operations",
    )  # Keep for compatibility
    search_filter: str = Field("(objectClass=*)", description="Default search filter")
    search_scope: str = Field(
        "SUBTREE",
        description="Search scope: BASE, LEVEL, or SUBTREE",
    )

    # Connection timeouts
    connect_timeout: int = Field(10, description="Connection timeout in seconds")
    receive_timeout: int = Field(30, description="Receive timeout in seconds")

    # Batch processing settings
    batch_size: int = Field(1000, description="Batch size for bulk operations")
    max_records: int | None = Field(
        None,
        description="Maximum records to process (None for unlimited)",
    )

    # Target-specific settings
    create_missing_entries: bool = Field(
        True,
        description="Create entries that don't exist",
    )
    update_existing_entries: bool = Field(True, description="Update existing entries")
    delete_removed_entries: bool = Field(
        False,
        description="Delete entries not in source",
    )

    # Mapping and transformation
    attribute_mapping: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping from Singer field names to LDAP attributes",
    )
    object_classes: list[str] = Field(
        default_factory=lambda: ["top"],
        description="Default object classes for new entries",
    )

    class Config:
        """Pydantic configuration."""

        env_prefix = "TARGET_LDAP_"
        case_sensitive = False


class LDAPConnectionSettings(FlextDomainBaseModel):
    """LDAP connection settings model."""

    host: str = Field(..., description="LDAP server host")
    port: int = Field(389, description="LDAP server port")
    use_ssl: bool = Field(False, description="Use SSL connection")
    use_tls: bool = Field(False, description="Use TLS connection")
    bind_dn: str | None = Field(None, description="Bind DN")
    bind_password: str | None = Field(None, description="Bind password")
    base_dn: str = Field(..., description="Base DN")
    connect_timeout: int = Field(10, description="Connection timeout")
    receive_timeout: int = Field(30, description="Receive timeout")


class LDAPOperationSettings(FlextDomainBaseModel):
    """LDAP operation settings model."""

    batch_size: int = Field(1000, description="Batch size")
    max_records: int | None = Field(None, description="Maximum records")
    create_missing_entries: bool = Field(True, description="Create missing entries")
    update_existing_entries: bool = Field(True, description="Update existing entries")
    delete_removed_entries: bool = Field(False, description="Delete removed entries")


# Function removed - not used anywhere and caused mypy errors due to complex field typing


def validate_ldap_config(config: dict[str, Any]) -> FlextResult[TargetLDAPConfig]:
    """Validate LDAP configuration."""
    try:
        validated_config = TargetLDAPConfig(**config)
        return FlextResult.ok(validated_config)
    except (RuntimeError, ValueError, TypeError) as e:
        return FlextResult.fail(f"Configuration validation failed: {e}")
