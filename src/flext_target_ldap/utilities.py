"""Singer target utilities for LDAP domain operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import (
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from datetime import datetime

from flext_ldap import FlextLdapUtilities
from flext_meltano import u
from flext_target_ldap import c, m, p, r, t


class FlextTargetLdapUtilities(u, FlextLdapUtilities):
    """Single unified utilities class for Singer target LDAP operations.

    Follows FLEXT unified class pattern with nested helper classes for
    domain-specific Singer target functionality with LDAP directory operations.

    Constants are accessed via constants module:
        c.Ldap.PORT (389)
        c.LDAPS_DEFAULT_PORT (636)
        c.DEFAULT_SIZE
    """

    class TargetLdap:
        """Singer protocol utilities for target operations."""

        @staticmethod
        def build_singer_catalog() -> t.TargetLdap.CatalogPayload:
            """Build the canonical Singer catalog for LDAP targets."""
            return t.Cli.JSON_MAPPING_ADAPTER.validate_python({
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
            })

        class TypeConversion:
            """Type coercion utilities for Singer settings values to typed Python values."""

            @staticmethod
            def build_connection_config(
                settings: t.TargetLdap.SettingsPayload,
            ) -> m.Ldap.ConnectionConfig:
                """Build LDAP ConnectionConfig from a flat settings mapping."""
                return m.Ldap.ConnectionConfig(
                    host=u.to_str(
                        settings.get(c.TargetLdap.KEY_HOST, c.TargetLdap.DEFAULT_HOST),
                        default=c.TargetLdap.DEFAULT_HOST,
                    ),
                    port=u.to_int(
                        settings.get(c.TargetLdap.KEY_PORT, c.Ldap.PORT),
                        default=c.Ldap.PORT,
                    ),
                    use_ssl=bool(
                        settings.get(c.TargetLdap.KEY_USE_SSL, c.Ldap.DEFAULT_USE_SSL)
                    ),
                    bind_dn=u.to_str(
                        settings.get(
                            c.TargetLdap.KEY_BIND_DN,
                            c.TargetLdap.DEFAULT_BIND_DN,
                        ),
                    ),
                    bind_password=u.to_str(
                        settings.get(
                            c.TargetLdap.KEY_PASSWORD,
                            c.TargetLdap.DEFAULT_BIND_PASSWORD,
                        ),
                    ),
                    timeout=u.to_int(
                        settings.get(c.TargetLdap.KEY_TIMEOUT, c.Ldap.TIMEOUT),
                        default=c.Ldap.TIMEOUT,
                    ),
                )

            @staticmethod
            def extract_attribute_mapping(
                settings: t.TargetLdap.SettingsPayload,
            ) -> t.StrMapping:
                """Extract attribute mapping from settings."""
                raw = settings.get(c.TargetLdap.KEY_ATTRIBUTE_MAPPING, {})
                if isinstance(raw, Mapping):
                    normalized_mapping: t.MutableMappingKV[str, str] = {}
                    for key, value in raw.items():
                        normalized_key = key
                        normalized_value = str(value)
                        normalized_mapping[normalized_key] = normalized_value
                    return normalized_mapping
                msg = f"Expected Mapping for 'attribute_mapping', got {type(raw).__name__}: {raw!r}"
                raise TypeError(msg)

            @staticmethod
            def extract_object_classes(
                settings: t.TargetLdap.SettingsPayload,
            ) -> t.StrSequence:
                """Extract object classes from settings."""
                raw = settings.get(c.TargetLdap.KEY_OBJECT_CLASSES)
                if isinstance(raw, list):
                    return [str(object_class) for object_class in raw if object_class]
                if isinstance(raw, str):
                    return [raw]
                return [c.TargetLdap.DEFAULT_OBJECT_CLASS]

        class LdapDataProcessing:
            """LDAP-specific data processing utilities."""

            @staticmethod
            def build_ldap_dn(
                record: t.TargetLdap.RecordPayload,
                dn_template: str,
                base_dn: str,
            ) -> p.Result[str]:
                """Build LDAP Distinguished Name from record data.

                Args:
                record: Record data
                dn_template: DN template with placeholders
                base_dn: Base DN for the directory

                Returns:
                r[str]: Built DN or error

                """
                if not record or not dn_template or (not base_dn):
                    return r[str].fail("Record, DN template, and base DN are required")
                try:
                    dn_rdn = dn_template
                    for key, value in record.items():
                        placeholder = f"{{{key}}}"
                        if placeholder in dn_rdn:
                            dn_rdn = dn_rdn.replace(placeholder, str(value))
                    if "{" in dn_rdn and "}" in dn_rdn:
                        return r[str].fail(f"Unresolved placeholders in DN: {dn_rdn}")
                    full_dn = f"{dn_rdn},{base_dn}"
                    if not FlextTargetLdapUtilities.TargetLdap.LdapDataProcessing.split(
                        full_dn
                    ):
                        return r[str].fail(f"Invalid DN format: {full_dn}")
                    return r[str].ok(full_dn)
                except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                    return r[str].fail(f"Error building DN: {e}")

            @staticmethod
            def convert_record_to_ldap_attributes(
                record: t.TargetLdap.RecordPayload,
                attribute_mapping: t.StrMapping | None = None,
            ) -> p.Result[Mapping[str, Sequence[bytes]]]:
                """Convert Singer record to LDAP attributes format.

                Args:
                record: Singer record data
                attribute_mapping: Optional mapping from record keys to LDAP attributes

                Returns:
                r[Mapping[str, Sequence[bytes]]]: LDAP attributes or error

                """
                if not record:
                    return r[Mapping[str, Sequence[bytes]]].fail(
                        "Record cannot be empty"
                    )
                try:
                    ldap_attrs: MutableMapping[str, Sequence[bytes]] = {}
                    mapping = attribute_mapping or {}
                    for key, value in record.items():
                        ldap_attr = mapping.get(key, key)
                        if isinstance(value, list):
                            ldap_values = [
                                str(item).encode(c.Ldif.Encoding.UTF8) for item in value
                            ]
                            if ldap_values:
                                ldap_attrs[ldap_attr] = ldap_values
                        else:
                            ldap_attrs[ldap_attr] = [
                                str(value).encode(c.Ldif.Encoding.UTF8)
                            ]
                    return r[Mapping[str, Sequence[bytes]]].ok(ldap_attrs)
                except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
                    return r[Mapping[str, Sequence[bytes]]].fail(
                        f"Error converting to LDAP attributes: {e}",
                    )

            @staticmethod
            def extract_object_classes(
                record: t.TargetLdap.RecordPayload,
                default_object_classes: t.StrSequence | None = None,
            ) -> t.StrSequence:
                """Extract object classes for LDAP entry.

                Args:
                record: Singer record data
                default_object_classes: Default object classes if not in record

                Returns:
                t.StrSequence: List of object classes

                """
                object_classes = record.get(
                    c.TargetLdap.KEY_OBJECT_CLASS_CAMEL,
                ) or record.get(c.TargetLdap.KEY_OBJECT_CLASS_LOWER)
                if object_classes:
                    if isinstance(object_classes, list):
                        return [str(oc) for oc in object_classes if oc]
                    return [str(object_classes)]
                if default_object_classes:
                    return default_object_classes
                return [c.TargetLdap.DEFAULT_OBJECT_CLASS]

            @staticmethod
            def sanitize_ldap_value(value: str) -> str:
                """Sanitize value for LDAP attribute insertion.

                Args:
                value: Value to sanitize

                Returns:
                str: Sanitized value

                """
                if not value:
                    return ""
                ldap_escapes = {
                    "\\": "\\5c",
                    "*": "\\2a",
                    "(": "\\28",
                    ")": "\\29",
                    "\x00": "\\00",
                }
                sanitized = value
                for char, escape in ldap_escapes.items():
                    sanitized = sanitized.replace(char, escape)
                return sanitized.strip()

            @staticmethod
            def split(dn: str) -> bool:
                """Validate LDAP Distinguished Name format.

                Args:
                dn: Distinguished Name to validate

                Returns:
                bool: True if valid, False otherwise

                """
                if not dn:
                    return False
                return bool(re.match(c.TargetLdap.LDAP_DN_PATTERN, dn.strip()))

        class ConfigValidation:
            """Configuration validation utilities."""

            @staticmethod
            def validate_ldap_connection_config(
                settings: Mapping[str, t.JsonPayload],
            ) -> p.Result[Mapping[str, t.JsonPayload]]:
                """Validate LDAP connection configuration.

                Args:
                settings: Configuration dictionary

                Returns:
                r[Mapping[str, t.JsonPayload]]: Validated settings or error

                """
                required_fields = [
                    c.TargetLdap.KEY_HOST,
                    c.TargetLdap.KEY_BIND_DN,
                    c.TargetLdap.KEY_BIND_PASSWORD,
                    c.TargetLdap.KEY_BASE_DN,
                ]
                missing_fields = [
                    field for field in required_fields if field not in settings
                ]
                if missing_fields:
                    return r[Mapping[str, t.JsonPayload]].fail(
                        f"Missing required LDAP connection fields: {', '.join(missing_fields)}",
                    )
                host = settings[c.TargetLdap.KEY_HOST]
                if not isinstance(host, str) or not host.strip():
                    return r[Mapping[str, t.JsonPayload]].fail(
                        "Host must be a non-empty string",
                    )
                bind_dn_raw = settings[c.TargetLdap.KEY_BIND_DN]
                bind_dn = u.to_str(bind_dn_raw)
                if not bind_dn:
                    return r[Mapping[str, t.JsonPayload]].fail(
                        "Bind DN must be a string",
                    )
                if not FlextTargetLdapUtilities.TargetLdap.LdapDataProcessing.split(
                    bind_dn
                ):
                    return r[Mapping[str, t.JsonPayload]].fail(
                        f"Invalid bind DN format: {bind_dn}",
                    )
                base_dn_raw = settings[c.TargetLdap.KEY_BASE_DN]
                base_dn = u.to_str(base_dn_raw)
                if not base_dn:
                    return r[Mapping[str, t.JsonPayload]].fail(
                        "Base DN must be a string",
                    )
                if not FlextTargetLdapUtilities.TargetLdap.LdapDataProcessing.split(
                    base_dn
                ):
                    return r[Mapping[str, t.JsonPayload]].fail(
                        f"Invalid base DN format: {base_dn}",
                    )
                if c.TargetLdap.KEY_PORT in settings:
                    port_raw = settings[c.TargetLdap.KEY_PORT]
                    match port_raw:
                        case bool() | Mapping() | list():
                            return r[Mapping[str, t.JsonPayload]].fail(
                                "Port must be a valid integer between 1 and 65535",
                            )
                        case int() as port_int:
                            pass
                        case str() | float():
                            try:
                                port_int = int(port_raw)
                            except (RuntimeError, TypeError, ValueError):
                                return r[Mapping[str, t.JsonPayload]].fail(
                                    "Port must be a valid integer between 1 and 65535",
                                )
                        case _:
                            return r[Mapping[str, t.JsonPayload]].fail(
                                "Port must be a valid integer between 1 and 65535",
                            )
                    if not (0 < port_int <= c.MAX_PORT):
                        return r[Mapping[str, t.JsonPayload]].fail(
                            "Port must be a valid integer between 1 and 65535",
                        )
                use_ssl = settings.get(c.TargetLdap.KEY_USE_SSL, c.Ldap.DEFAULT_USE_SSL)
                use_tls = settings.get(c.TargetLdap.KEY_USE_TLS, c.Ldap.DEFAULT_USE_TLS)
                if use_ssl and use_tls:
                    return r[Mapping[str, t.JsonPayload]].fail(
                        "Cannot use both SSL and TLS simultaneously",
                    )
                return r[Mapping[str, t.JsonPayload]].ok(settings)

            @staticmethod
            def validate_target_config(
                settings: Mapping[str, t.JsonPayload],
            ) -> p.Result[Mapping[str, t.JsonPayload]]:
                """Validate target configuration.

                Args:
                settings: Target configuration

                Returns:
                r[Mapping[str, t.JsonPayload]]: Validated settings or error

                """
                ldap_result = FlextTargetLdapUtilities.TargetLdap.ConfigValidation.validate_ldap_connection_config(
                    settings,
                )
                if ldap_result.failure:
                    return ldap_result
                operation_mode = settings.get(
                    c.TargetLdap.KEY_OPERATION_MODE,
                    c.TargetLdap.DEFAULT_OPERATION_MODE,
                )
                valid_modes = list(c.TargetLdap.OPERATION_MODES)
                if operation_mode not in valid_modes:
                    return r[Mapping[str, t.JsonPayload]].fail(
                        f"Invalid operation mode: {operation_mode}. Valid modes: {', '.join(valid_modes)}",
                    )
                if c.TargetLdap.KEY_DN_TEMPLATE in settings:
                    dn_template = settings[c.TargetLdap.KEY_DN_TEMPLATE]
                    if not isinstance(dn_template, str) or not dn_template.strip():
                        return r[Mapping[str, t.JsonPayload]].fail(
                            "DN template must be a non-empty string",
                        )
                batch_size = settings.get(c.TargetLdap.KEY_BATCH_SIZE, c.DEFAULT_SIZE)
                match batch_size:
                    case bool():
                        return r[Mapping[str, t.JsonPayload]].fail(
                            "Batch size must be a positive integer",
                        )
                    case int() if batch_size > 0:
                        pass
                    case _:
                        return r[Mapping[str, t.JsonPayload]].fail(
                            "Batch size must be a positive integer",
                        )
                return r[Mapping[str, t.JsonPayload]].ok(settings)

            @staticmethod
            def coerce_container_value(
                value: m.ConfigMap | t.JsonPayload,
            ) -> m.ConfigMap | t.JsonList | t.JsonValue | None:
                """Coerce a container value to a normalized form for LDAP operations.

                Recursively normalizes BaseModel, scalar, list, and Mapping values into
                types suitable for LDAP attribute storage.

                Args:
                    value: Value to coerce (ConfigMap, scalar, list, dict, or BaseModel)

                Returns:
                    Normalized value, ConfigMap, list of container values, or None if
                    the value cannot be coerced.

                """
                if isinstance(value, m.BaseModel):
                    return FlextTargetLdapUtilities.TargetLdap.ConfigValidation.coerce_container_value(
                        value.model_dump(),
                    )
                if isinstance(value, datetime):
                    return value.isoformat()
                if isinstance(value, (str, int, float, bool)):
                    return value
                if isinstance(value, list):
                    normalized_list: MutableSequence[t.JsonValue] = []
                    for item in value:
                        if isinstance(
                            item, (str, int, float, bool, datetime, list, dict)
                        ):
                            coerced_item = FlextTargetLdapUtilities.TargetLdap.ConfigValidation.coerce_container_value(
                                item,
                            )
                            if isinstance(
                                coerced_item, (str, int, float, bool, datetime)
                            ):
                                normalized_list.append(coerced_item)
                    return normalized_list
                if isinstance(value, Mapping):
                    normalized_dict: dict[str, str | int | float | bool] = {}
                    for key, item in value.items():
                        if isinstance(
                            item, (str, int, float, bool, datetime, list, dict)
                        ):
                            coerced_item = FlextTargetLdapUtilities.TargetLdap.ConfigValidation.coerce_container_value(
                                item,
                            )
                            if coerced_item is not None and isinstance(
                                coerced_item,
                                (str, int, float, bool),
                            ):
                                normalized_dict[key] = coerced_item
                    return m.ConfigMap.model_validate(normalized_dict)
                return None


u = FlextTargetLdapUtilities

__all__: list[str] = ["FlextTargetLdapUtilities", "u"]
