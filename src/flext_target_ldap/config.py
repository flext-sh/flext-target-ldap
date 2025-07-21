"""Configuration for target-ldap using flext-core patterns.

REFACTORED:
            Uses flext-core SingerTargetConfig for declarative configuration.
Zero tolerance for code duplication.
"""

from __future__ import annotations

from typing import Any

from flext_core.config.adapters.singer import SingerTargetConfig
from pydantic import Field


class TargetLDAPConfig(SingerTargetConfig):
    """LDAP target configuration using flext-core patterns."""

    # Core LDAP connection settings
    host: str = Field(..., description="LDAP server hostname or IP address")
    port: int = Field(389, description="LDAP server port (389 for LDAP, 636 for LDAPS)")
    bind_dn: str | None = Field(
        None,
        description="Distinguished name for binding to LDAP",
    )
    password: str | None = Field(
        None,
        description="Password for LDAP authentication",
        json_schema_extra={"secret": True},
    )
    base_dn: str = Field(..., description="Base DN for LDAP operations")
    use_ssl: bool = Field(False, description="Use SSL/TLS for LDAP connection")
    timeout: int = Field(30, description="Connection timeout in seconds")

    # Processing settings
    validate_records: bool = Field(True, description="Validate records before loading")
    user_rdn_attribute: str = Field("uid", description="RDN attribute for user entries")
    group_rdn_attribute: str = Field(
        "cn",
        description="RDN attribute for group entries",
    )
    default_object_classes: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Default object classes for each stream",
    )
    dn_templates: dict[str, str] = Field(
        default_factory=dict,
        description="DN templates for each stream",
    )

    # Data transformation settings
    enable_transformation: bool = Field(
        False,
        description="Enable data transformation engine",
    )
    transformation_rules: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Custom transformation rules",
    )
    classification_patterns: dict[str, str] = Field(
        default_factory=dict,
        description="Custom patterns for data classification",
    )
    oracle_migration_mode: bool = Field(
        False,
        description="Enable Oracle-to-LDAP migration optimizations",
    )
    preserve_original_attributes: bool = Field(
        False,
        description="Preserve original Oracle attributes during transformation",
    )

    # Validation settings
    enable_validation: bool = Field(
        True,
        description="Enable entry validation before loading",
    )
    validation_strict_mode: bool = Field(
        False,
        description="Fail on validation errors (vs. warnings)",
    )
    migration_batch_id: str | None = Field(
        None,
        description="Identifier for migration batch tracking",
    )
    dry_run_mode: bool = Field(
        False,
        description="Validate and transform without actually loading data",
    )

    # Performance settings
    batch_size: int = Field(
        100,
        description="Number of entries to process in each batch",
        ge=1,
    )
    parallel_processing: bool = Field(
        False,
        description="Enable parallel processing for large datasets",
    )
    max_errors: int = Field(
        10,
        description="Maximum number of errors before stopping processing",
        ge=0,
    )
    ignore_transformation_errors: bool = Field(
        True,
        description="Continue processing on transformation errors",
    )

    @classmethod
    def config_jsonschema(cls) -> dict[str, Any]:
        """Return configuration schema in Singer SDK format.

        This method is required by Singer SDK to provide the configuration schema.
        """
        from flext_core.config.adapters.singer import singer_config_adapter

        return singer_config_adapter(cls, is_target=True)
