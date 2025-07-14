"""target-ldap main target class using flext-core patterns.

REFACTORED:
        Uses flext-core configuration patterns and flext-observability logging.
Zero tolerance for code duplication.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from typing import Any

from singer_sdk import Target

from flext_target_ldap.config import TargetLDAPConfig
from flext_target_ldap.sinks import GenericSink
from flext_target_ldap.sinks import GroupsSink
from flext_target_ldap.sinks import OrganizationalUnitsSink
from flext_target_ldap.sinks import UsersSink

if TYPE_CHECKING:
    from collections.abc import Sequence

    from singer_sdk.sinks import Sink


logger = logging.getLogger(__name__)


class TargetLDAP(Target):
    """Singer target for LDAP data loading using flext-core patterns."""

    name = "target-ldap"

    # Use flext-core configuration class
    config_class = TargetLDAPConfig

    config_jsonschema = TargetLDAPConfig.config_jsonschema()

    def get_sink(
        self,
        stream_name: str,
        *,
        record: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
        key_properties: Sequence[str] | None = None,
    ) -> Sink:
        """Get appropriate sink for the given stream.

        Args:
            stream_name: Name of the data stream to process.
            record: Optional record for context.
            schema: Optional schema for validation.
            key_properties: Optional key properties for the stream.

        Returns:
            Sink instance for processing the stream data.

        """
        # Map stream names to sink classes
        sink_mapping = {
            "users": UsersSink,
            "groups": GroupsSink,
            "organizational_units": OrganizationalUnitsSink,
        }

        sink_class = sink_mapping.get(stream_name, GenericSink)

        # Apply DN template if configured:
        dn_templates = self.config.get("dn_templates", {})
        config_dict = dict(self.config)
        if stream_name in dn_templates:
            config_dict[f"{stream_name}_dn_template"] = dn_templates[stream_name]

        # Apply default object classes if configured:
        default_object_classes = self.config.get("default_object_classes", {})
        if stream_name in default_object_classes:
            config_dict[f"{stream_name}_object_classes"] = default_object_classes[
                stream_name
            ]

        # Update the target config
        self._config = config_dict

        # Provide a proper default schema if none provided
        default_schema = {
            "type": "object",
            "properties": {
                "dn": {"type": "string", "description": "Distinguished Name"},
                "objectClass": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Object classes",
                },
                "cn": {"type": "string", "description": "Common Name"},
            },
        }

        return sink_class(
            target=self,
            stream_name=stream_name,
            schema=schema or default_schema,
            key_properties=list(key_properties) if key_properties else ["dn"],
        )


def main() -> None:
    """Main CLI entry point."""
    TargetLDAP.cli()


if __name__ == "__main__":
    main()
