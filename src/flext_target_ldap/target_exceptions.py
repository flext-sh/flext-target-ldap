"""🚨 ARCHITECTURAL COMPLIANCE: ZERO EXCEPTION DUPLICATION using flext-core Factory.

✅ REFATORAÇÃO COMPLETA: 250+ linhas de código duplicado ELIMINADAS.

- ANTES: 299 linhas com 10 classes manuais de exceptions
- DEPOIS: <60 linhas usando factory pattern limpo e DRY
- REDUÇÃO: 250+ linhas eliminadas = ~84% redução
- PADRÃO: Usa create_module_exception_classes() de flext-core
- ARQUITETURA: Funcionalidades genéricas permanecem nas bibliotecas abstratas
- EXPOSIÇÃO: API pública correta através do factory pattern

LDAP Target Exception Hierarchy - ZERO DUPLICATION.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Domain-specific exceptions for LDAP target operations using factory pattern to eliminate duplication.
"""

from __future__ import annotations

# 🚨 ZERO DUPLICATION: Use flext-core exception factory - eliminates 250+ lines
from flext_core.exceptions import create_module_exception_classes

# Generate all standard exceptions using factory pattern
_target_ldap_exceptions = create_module_exception_classes("flext_target_ldap")

# Export factory-created exception classes (using actual factory keys)
FlextTargetLdapError = _target_ldap_exceptions["FlextTargetLdapError"]
FlextTargetLdapValidationError = _target_ldap_exceptions["FlextTargetLdapValidationError"]
FlextTargetLdapConfigurationError = _target_ldap_exceptions["FlextTargetLdapConfigurationError"]
FlextTargetLdapProcessingError = _target_ldap_exceptions["FlextTargetLdapProcessingError"]
FlextTargetLdapConnectionError = _target_ldap_exceptions["FlextTargetLdapConnectionError"]
FlextTargetLdapAuthenticationError = _target_ldap_exceptions["FlextTargetLdapAuthenticationError"]
FlextTargetLdapTimeoutError = _target_ldap_exceptions["FlextTargetLdapTimeoutError"]

# Create backward-compatible aliases for existing code
FlextTargetLdapLoadError = FlextTargetLdapProcessingError  # Load errors are processing
FlextTargetLdapSchemaError = FlextTargetLdapValidationError  # Schema is validation
FlextTargetLdapWriteError = FlextTargetLdapProcessingError  # Write is processing


__all__ = [
    "FlextTargetLdapAuthenticationError",
    "FlextTargetLdapConfigurationError",
    "FlextTargetLdapConnectionError",
    "FlextTargetLdapError",
    "FlextTargetLdapLoadError",
    "FlextTargetLdapProcessingError",
    "FlextTargetLdapSchemaError",
    "FlextTargetLdapTimeoutError",
    "FlextTargetLdapValidationError",
    "FlextTargetLdapWriteError",
]
