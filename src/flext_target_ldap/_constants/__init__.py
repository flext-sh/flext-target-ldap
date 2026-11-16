# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Ldap. Constants package.

Copyright (c) 2026 Marlon Santa Cruz. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_ldap._constants.base import FlextTargetLdapConstantsBase


__all__: tuple[str, ...] = ("FlextTargetLdapConstantsBase",)

install_lazy_exports(
    __name__,
    globals(),
    {"FlextTargetLdapConstantsBase": ".base"},
    public_exports=__all__,
    deferred_members={
        "FlextTargetLdapConstantsBase": (
            "ENV_PREFIX",
            "CREATE_MISSING_ENTRIES",
            "UPDATE_EXISTING_ENTRIES",
            "DELETE_REMOVED_ENTRIES",
            "DEFAULT_OBJECT_CLASSES",
            "DEFAULT_HOST",
            "DEFAULT_BIND_DN",
            "DEFAULT_BIND_PASSWORD",
            "KEY_HOST",
            "KEY_PORT",
            "KEY_BIND_DN",
            "KEY_BIND_CREDENTIAL",
            "KEY_BASE_DN",
            "KEY_ATTRIBUTE_MAPPING",
            "KEY_DN",
            "KEY_DELETED_AT",
            "KEY_UPDATE_EXISTING_ENTRIES",
            "KEY_OBJECT_CLASS_ATTRIBUTE",
            "RECORD_OBJECT_CLASS_KEYS",
            "RECORD_CONTROL_KEYS",
            "TARGET_NAME",
            "DEFAULT_BASE_DN",
        ),
    },
)
