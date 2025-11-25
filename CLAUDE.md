# FLEXT-Target-LDAP Project Guidelines

**Reference**: See [../CLAUDE.md](../CLAUDE.md) for FLEXT ecosystem standards and general rules.

---

## Project Overview

**FLEXT-Target-LDAP** is the Singer target for LDAP directory loading in the FLEXT ecosystem.

**Version**: 2.1.0  
**Status**: Production-ready  
**Python**: 3.13+

**CRITICAL INTEGRATION DEPENDENCIES**:
- **flext-meltano**: MANDATORY for ALL Singer operations (ZERO TOLERANCE for direct singer-sdk without flext-meltano)
- **flext-ldap**: MANDATORY for ALL LDAP operations (ZERO TOLERANCE for direct ldap3 imports)
- **flext-core**: Foundation patterns (FlextResult, FlextService, FlextContainer)

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests
```

---

## Key Patterns

### Singer Target Implementation

```python
from flext_core import FlextResult
from flext_target_ldap import FlextTargetLdap

target = FlextTargetLdap()

# Process records
result = target.write_record(record)
if result.is_success:
    print("Record written to LDAP")
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:
- ❌ Direct singer-sdk imports (use flext-meltano)
- ❌ Direct ldap3 imports (use flext-ldap)
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types

**MANDATORY**:
- ✅ Use `FlextResult[T]` for all operations
- ✅ Use flext-meltano for Singer operations
- ✅ Use flext-ldap for LDAP operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations

---

**Additional Resources**: [../CLAUDE.md](../CLAUDE.md) (workspace), [README.md](README.md) (overview)
