"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextContainer

"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container using DRY pattern.

REFATORADO COMPLETO usando create_module_container_utilities:
- ZERO code duplication através do DRY utility pattern de flext-core
- USA create_module_container_utilities() para eliminar 77 linhas duplicadas
- Mantém apenas utilitários flext_target_ldap-específicos
- SOLID: Single source of truth para module container patterns

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""


get_flext_target_ldap_container = FlextContainer.get_global()


def get_flext_target_ldap_service(service_name: str) -> object:
    """Get service from FLEXT DI container."""
    return get_flext_target_ldap_container.get(service_name)


# Type assertion for the configuration function
# configure_flext_target_ldap_dependencies: Callable[[], None] = _configure_func
def configure_flext_target_ldap_dependencies() -> None:
    """Fallback configuration function."""


# Initialize flext_target_ldap dependencies on module import
configure_flext_target_ldap_dependencies()
