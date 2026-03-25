"""DI Container utilities for flext-target-ldap using flext-core patterns.

This module provides dependency injection container utilities following
flext-core foundation patterns, eliminating code duplication and ensuring
consistent dependency management across the LDAP target implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextContainer, p, r

from flext_target_ldap import t


def get_flext_target_ldap_container() -> p.Container:
    """Get the global FLEXT DI container."""
    return FlextContainer.get_global()


def get_flext_target_ldap_service(
    service_name: str,
) -> r[t.RegisterableService]:
    """Get service from FLEXT DI container."""
    container = get_flext_target_ldap_container()
    return container.get(service_name)


def configure_flext_target_ldap_dependencies() -> None:
    """Fallback configuration function."""


configure_flext_target_ldap_dependencies()
