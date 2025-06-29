"""target-ldap main target class.

This module implements the main target class for LDAP data loading.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar

from singer_sdk import Target
from singer_sdk import typing as th

from target_ldap.sinks import (
    GenericSink,
    GroupsSink,
    OrganizationalUnitsSink,
    UsersSink,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from singer_sdk.sinks import Sink


logger = logging.getLogger(__name__)


class TargetLDAP(Target):
    """Singer target for LDAP data loading."""

    name = "target-ldap"

    config_jsonschema: ClassVar[dict[str, Any]] = th.PropertiesList(
        th.Property(
            "host",
            th.StringType,
            required=True,
            description="LDAP server hostname or IP address",
        ),
        th.Property(
            "port",
            th.IntegerType,
            default=389,
            description="LDAP server port (389 for LDAP, 636 for LDAPS)",
        ),
        th.Property(
            "bind_dn",
            th.StringType,
            description="Distinguished name for binding to LDAP",
        ),
        th.Property(
            "password",
            th.StringType,
            secret=True,
            description="Password for LDAP authentication",
        ),
        th.Property(
            "base_dn",
            th.StringType,
            required=True,
            description="Base DN for LDAP operations",
        ),
        th.Property(
            "use_ssl",
            th.BooleanType,
            default=False,
            description="Use SSL/TLS for LDAP connection",
        ),
        th.Property(
            "timeout",
            th.IntegerType,
            default=30,
            description="Connection timeout in seconds",
        ),
        th.Property(
            "validate_records",
            th.BooleanType,
            default=True,
            description="Validate records before loading",
        ),
        th.Property(
            "user_rdn_attribute",
            th.StringType,
            default="uid",
            description="RDN attribute for user entries",
        ),
        th.Property(
            "group_rdn_attribute",
            th.StringType,
            default="cn",
            description="RDN attribute for group entries",
        ),
        th.Property(
            "default_object_classes",
            th.ObjectType(),
            description="Default object classes for each stream",
        ),
        th.Property(
            "dn_templates",
            th.ObjectType(),
            description="DN templates for each stream",
        ),
        th.Property(
            "stream_maps",
            th.ObjectType(),
            description="Configuration for stream maps",
        ),
        th.Property(
            "stream_map_settings",
            th.ObjectType(),
            description="Settings for stream maps",
        ),
        # Data Transformation Configuration
        th.Property(
            "enable_transformation",
            th.BooleanType,
            default=False,
            description="Enable data transformation engine",
        ),
        th.Property(
            "transformation_rules",
            th.ArrayType(th.ObjectType()),
            description="Custom transformation rules",
        ),
        th.Property(
            "classification_patterns",
            th.ObjectType(),
            description="Custom patterns for data classification",
        ),
        th.Property(
            "oracle_migration_mode",
            th.BooleanType,
            default=False,
            description="Enable Oracle-to-LDAP migration optimizations",
        ),
        th.Property(
            "preserve_original_attributes",
            th.BooleanType,
            default=False,
            description="Preserve original Oracle attributes during transformation",
        ),
        # Migration and Validation Configuration
        th.Property(
            "enable_validation",
            th.BooleanType,
            default=True,
            description="Enable entry validation before loading",
        ),
        th.Property(
            "validation_strict_mode",
            th.BooleanType,
            default=False,
            description="Fail on validation errors (vs. warnings)",
        ),
        th.Property(
            "migration_batch_id",
            th.StringType,
            description="Identifier for migration batch tracking",
        ),
        th.Property(
            "dry_run_mode",
            th.BooleanType,
            default=False,
            description="Validate and transform without actually loading data",
        ),
        # Performance and Batch Processing
        th.Property(
            "batch_size",
            th.IntegerType,
            default=100,
            description="Number of entries to process in each batch",
        ),
        th.Property(
            "parallel_processing",
            th.BooleanType,
            default=False,
            description="Enable parallel processing for large datasets",
        ),
        th.Property(
            "max_errors",
            th.IntegerType,
            default=10,
            description="Maximum number of errors before stopping processing",
        ),
        th.Property(
            "ignore_transformation_errors",
            th.BooleanType,
            default=True,
            description="Continue processing on transformation errors",
        ),
    ).to_dict()

    def get_sink(
        self,
        stream_name: str,
        *,
        record: dict[str, Any] | None = None,  # noqa: ARG002
        schema: dict[str, Any] | None = None,
        key_properties: Sequence[str] | None = None,
    ) -> Sink:
        """Get sink for a stream.

        Args:
        ----
            stream_name: Name of the stream
            record: Sample record (optional)
            schema: Stream schema
            key_properties: Primary key properties

        Returns:
        -------
            Appropriate sink instance

        """
        # Map stream names to sink classes
        sink_mapping = {
            "users": UsersSink,
            "groups": GroupsSink,
            "organizational_units": OrganizationalUnitsSink,
        }

        sink_class = sink_mapping.get(stream_name, GenericSink)

        # Apply DN template if configured
        dn_templates = self.config.get("dn_templates", {})
        config_dict = dict(self.config)
        if stream_name in dn_templates:
            config_dict[f"{stream_name}_dn_template"] = dn_templates[stream_name]

        # Apply default object classes if configured
        default_object_classes = self.config.get("default_object_classes", {})
        if stream_name in default_object_classes:
            config_dict[f"{stream_name}_object_classes"] = default_object_classes[
                stream_name
            ]

        # Update the target config
        self._config = config_dict

        return sink_class(
            target=self,
            stream_name=stream_name,
            schema=schema or {},
            key_properties=list(key_properties) if key_properties else None,
        )


if __name__ == "__main__":
    TargetLDAP.cli()
