"""DI Container utilities for flext-target-ldap using flext-core patterns.

This module provides dependency injection container utilities following
flext-core foundation patterns, eliminating code duplication and ensuring
consistent dependency management across the LDAP target implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextCore

get_flext_target_ldap_container = FlextCore.Container.get_global()


def get_flext_target_ldap_service(service_name: str) -> object:
    """Get service from FLEXT DI container."""
    return get_flext_target_ldap_container.get(service_name)


# Type assertion for the configuration function
# configure_flext_target_ldap_dependencies: Callable[[], None] = _configure_func
def configure_flext_target_ldap_dependencies() -> None:
    """Fallback configuration function."""


# Initialize flext_target_ldap dependencies on module import
configure_flext_target_ldap_dependencies()
