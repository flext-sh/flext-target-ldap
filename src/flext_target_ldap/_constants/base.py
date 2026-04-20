"""FlextTargetLdapConstantsBase - Target LDAP foundational constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_target_ldap import t


class FlextTargetLdapConstantsBase:
    """Base constants for Target LDAP domain."""

    # Environment and connection
    ENV_PREFIX: Final[str] = "FLEXT_TARGET_LDAP_"

    # Default values for settings fields
    CREATE_MISSING_ENTRIES: Final[bool] = True
    UPDATE_EXISTING_ENTRIES: Final[bool] = True
    DELETE_REMOVED_ENTRIES: Final[bool] = False
    DEFAULT_OBJECT_CLASSES: Final[t.VariadicTuple[str]] = ("top",)
