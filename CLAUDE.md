# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Target LDAP is a Singer target implementation for LDAP directory services, part of the larger FLEXT ecosystem. This project enables loading data from Singer taps into LDAP directories with enterprise-grade reliability and performance.

## Architecture

This project follows Clean Architecture and Domain-Driven Design patterns using flext-core foundations:

### Core Components

- **Target Class**: `TargetLDAP` in `src/flext_target_ldap/target.py` - Main Singer target implementation
- **Application Layer**: `LDAPTargetOrchestrator` in `src/flext_target_ldap/application/orchestrator.py` - Business logic orchestration
- **Infrastructure Layer**: Dependency injection container in `src/flext_target_ldap/infrastructure/di_container.py`
- **Connection Layer**: LDAP connection management in `src/flext_target_ldap/connection/`
- **Singer Layer**: Singer SDK integration in `src/flext_target_ldap/singer/`

### Key Dependencies

- **flext-core**: Foundational patterns, FlextResult, logging, dependency injection
- **flext-meltano**: Singer SDK integration (consolidated from singer-sdk)
- **flext-ldap**: LDAP connection and operations
- **flext-observability**: Monitoring and metrics

### Configuration

- Configuration class: `TargetLDAPConfig` in `src/flext_target_ldap/config.py`
- Uses Pydantic settings with type validation
- LDAP connection settings integrated with flext-ldap patterns

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: LDAP Integration Library Dependency

**Status**: ALTO - Integration com flext-ldap precisa optimization
**Problema**:

- Connection layer pode duplicate flext-ldap functionality
- LDAP operations patterns podem not be fully aligned
- Directory modification strategies podem be incomplete

**TODO**:

- [ ] Optimize integration com flext-ldap para eliminate duplication
- [ ] Align LDAP operations patterns com library
- [ ] Implement comprehensive directory modification strategies
- [ ] Document LDAP integration best practices

### 🚨 GAP 2: Clean Architecture Implementation Complexity

**Status**: ALTO - Application orchestrator pode indicate over-engineering
**Problema**:

- LDAPTargetOrchestrator suggests complex orchestration layer
- DI container para LDAP target pode be overkill
- Architecture layers podem be too granular para Singer target

**TODO**:

- [ ] Review orchestration complexity vs benefits
- [ ] Simplify architecture se appropriate
- [ ] Optimize DI container usage
- [ ] Document architecture decisions

### 🚨 GAP 3: LDAP Data Loading Patterns

**Status**: ALTO - LDAP directory loading patterns podem be suboptimal
**Problema**:

- Bulk LDAP operations strategies não documented
- LDAP schema validation patterns podem be missing
- Error handling para LDAP failures pode be incomplete

**TODO**:

- [ ] Implement LDAP bulk operations onde appropriate
- [ ] Add LDAP schema validation
- [ ] Enhance error handling para LDAP-specific failures
- [ ] Document LDAP loading patterns

## Development Commands

### Essential Quality Gates (Run Before Committing)

```bash
make validate    # Complete validation: lint + type + security + test (MUST PASS)
make check       # Essential checks: lint + type + test
make test        # Run tests with 90% coverage requirement
make lint        # Ruff linting with ALL rules enabled
make type-check  # Strict MyPy type checking
make security    # Security scans: bandit + pip-audit + secrets
```

### Development Setup

```bash
make setup       # Complete development setup
make install     # Install dependencies with Poetry
make dev-install # Development environment + pre-commit hooks
```

### Testing Commands

```bash
make test                 # All tests with coverage (90% minimum)
make test-unit           # Unit tests only
make test-integration    # Integration tests only
make test-singer         # Singer protocol tests
make coverage            # Generate detailed coverage report
make coverage-html       # Open HTML coverage report
```

### Singer Target Operations

```bash
make target-test         # Test basic target functionality
make target-validate     # Validate target configuration
make target-schema       # Validate LDAP schema compatibility
make target-run          # Run with sample data
make target-run-debug    # Run with debug logging
make target-dry-run      # Run in dry-run mode
```

### LDAP-Specific Operations

```bash
make ldap-connection     # Test LDAP connection
make ldap-write-test     # Test LDAP write operations
make ldap-schema-check   # Check LDAP schema compatibility
make ldap-operations     # Test LDAP operations
make ldap-performance    # Run performance benchmarks
make ldap-diagnostics    # Run LDAP diagnostics
```

### Code Quality

```bash
make format      # Format code with ruff
make format-check # Check formatting without fixing
make fix         # Auto-fix all issues (format + lint)
```

### Environment Setup

```bash
# Start LDAP test servers
docker-compose up -d

# Access LDAP REDACTED_LDAP_BIND_PASSWORD interface
# http://localhost:20080 (phpLDAPREDACTED_LDAP_BIND_PASSWORD)

# LDAP test servers:
# Source: localhost:20389 (dc=source,dc=com)
# Target: localhost:21389 (dc=target,dc=com)
```

## Testing Strategy

### Test Structure

- **Unit Tests**: Business logic and component testing
- **Integration Tests**: LDAP server integration with Docker
- **Singer Tests**: Singer protocol compliance testing
- **Performance Tests**: LDAP operation benchmarks

### Test Requirements

- Minimum 90% test coverage enforced
- All tests must pass before commits
- Integration tests use Docker containers for LDAP servers
- Performance benchmarks for LDAP operations

### Running Specific Tests

```bash
pytest tests/unit/                    # Unit tests only
pytest tests/integration/             # Integration tests
pytest tests/singer/                  # Singer protocol tests
pytest tests/performance/             # Performance benchmarks
pytest -m "not slow"                  # Exclude slow tests
pytest --benchmark-only               # Benchmarks only
```

## Singer Protocol Integration

### CLI Usage

```bash
# Basic usage
target-ldap --config config.json < input.jsonl

# Configuration sample
target-ldap --config-sample > config_sample.json

# Target information
target-ldap --about
target-ldap --version
```

### Configuration

The target accepts standard Singer configuration format with LDAP-specific settings:

- LDAP connection parameters (host, port, credentials)
- Base DN configuration
- Schema mapping settings
- Batch processing options

## Code Patterns

### FlextResult Pattern

All operations return `FlextResult[T]` for consistent error handling:

```python
from flext_core import FlextResult

def load_data(records: list[dict]) -> FlextResult[dict]:
    try:
        # Processing logic
        return FlextResult.success({"processed": len(records)})
    except Exception as e:
        return FlextResult.failure(f"Load failed: {e}")
```

### Dependency Injection

Uses flext-core DI container for dependency management:

```python
from flext_target_ldap.infrastructure import get_flext_target_ldap_container

container = get_flext_target_ldap_container()
orchestrator = container.get(LDAPTargetOrchestrator)
```

### Configuration Pattern

Configuration follows Pydantic BaseSettings pattern:

```python
class TargetLDAPConfig(BaseSettings):
    # LDAP connection settings
    # Processing options
    # Schema configuration
```

## Quality Standards

### Zero Tolerance Enforcement

- **100% Type Coverage**: Strict MyPy with no untyped code
- **90% Test Coverage**: Enforced minimum coverage
- **All Lint Rules**: Ruff with ALL rules enabled
- **Security Scanning**: Bandit + pip-audit + secrets detection
- **Pre-commit Hooks**: Automated quality gates

### Code Quality Tools

- **Ruff**: Linting and formatting (ALL rules enabled)
- **MyPy**: Strict type checking
- **Bandit**: Security vulnerability scanning
- **Pytest**: Testing with coverage reporting
- **Pre-commit**: Automated quality enforcement

## Troubleshooting

### Common Issues

**LDAP Connection Issues:**

```bash
make ldap-connection    # Test LDAP connectivity
docker-compose logs openldap-target  # Check LDAP server logs
```

**Test Failures:**

```bash
make test-unit          # Run unit tests only
pytest -x tests/        # Stop on first failure
pytest --lf             # Run last failed tests
```

**Type Checking Issues:**

```bash
make type-check         # Full MyPy checking
mypy src/ --show-error-codes  # Show specific error codes
```

**Performance Issues:**

```bash
make ldap-performance   # Run performance benchmarks
make ldap-diagnostics   # LDAP-specific diagnostics
```

### Docker Environment

The project includes Docker Compose setup for LDAP testing:

- Source LDAP server: `localhost:20389`
- Target LDAP server: `localhost:21389`
- Admin interface: `localhost:20080`

Use `docker-compose up -d` to start the test environment.
