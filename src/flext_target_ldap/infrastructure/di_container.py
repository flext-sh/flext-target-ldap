"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container using DRY pattern.

REFATORADO COMPLETO usando create_module_container_utilities:
- ZERO code duplication através do DRY utility pattern de flext-core
- USA create_module_container_utilities() para eliminar 77 linhas duplicadas
- Mantém apenas utilitários flext_target_ldap-específicos
- SOLID: Single source of truth para module container patterns

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import create_module_container_utilities

if TYPE_CHECKING:
    from collections.abc import Callable

# Create all module-specific utilities using DRY pattern
_utilities = create_module_container_utilities("flext_target_ldap")

# Extract utilities with proper names for backward compatibility
get_flext_target_ldap_container = _utilities["get_container"]
_configure_func = _utilities["configure_dependencies"]
get_flext_target_ldap_service = _utilities["get_service"]

# Type assertion for the configuration function
configure_flext_target_ldap_dependencies: Callable[[], None] = _configure_func  # type: ignore[assignment]

# Initialize flext_target_ldap dependencies on module import
if callable(configure_flext_target_ldap_dependencies):
    configure_flext_target_ldap_dependencies()
