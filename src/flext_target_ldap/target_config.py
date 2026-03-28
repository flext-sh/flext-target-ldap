"""Backward-compatible re-export of config functions from _utilities.config."""

from __future__ import annotations

from flext_target_ldap._utilities.config import (
    create_default_ldap_target_config,
    validate_ldap_target_config,
)

__all__ = [
    "create_default_ldap_target_config",
    "validate_ldap_target_config",
]
