"""FlextTargetLdapConstantsBase - Target LDAP foundational constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextTargetLdapConstantsBase:
    """Base constants for Target LDAP domain."""

    # Environment and connection
    ENV_PREFIX: Final[str] = "FLEXT_TARGET_LDAP_"
    CONNECT_TIMEOUT: Final[int] = 10
    MAX_PORT_NUMBER: Final[int] = 65535
    LDAPS_DEFAULT_PORT: Final[int] = 636

    # Default values for settings fields
    CREATE_MISSING_ENTRIES: Final[bool] = True
    UPDATE_EXISTING_ENTRIES: Final[bool] = True
    DELETE_REMOVED_ENTRIES: Final[bool] = False
    DEFAULT_OBJECT_CLASSES: Final[tuple[str, ...]] = ("top",)
