# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Target LDAP is a Singer target implementation for LDAP directory services, part of the larger FLEXT ecosystem. This project enables loading data from Singer taps into LDAP directories with enterprise-grade reliability and performance.

## Architecture

This project follows Clean Architecture and Domain-Driven Design patterns using flext-core foundations:

### Core Components

- **Target Class**: `TargetLDAP` in `src/flext_target_ldap/target.py` - Main Singer target implementation with Click CLI
- **Application Layer**: `LDAPTargetOrchestrator` in `src/flext_target_ldap/application/orchestrator.py` - Business logic orchestration
- **Infrastructure Layer**: Dependency injection container in `src/flext_target_ldap/infrastructure/di_container.py` (uses flext-core DRY patterns)
- **Sinks Layer**: Stream-specific sinks in `src/flext_target_ldap/sinks.py` - UsersSink, GroupsSink, OrganizationalUnitsSink
- **Client Layer**: LDAP client in `src/flext_target_ldap/client.py` - Connection and operation management
- **Singer Layer**: Singer SDK integration in `src/flext_target_ldap/singer/` - catalog, stream, and target abstractions

### Key Dependencies

- **flext-core**: Foundational patterns, FlextResult, logging, dependency injection
- **flext-meltano**: Singer SDK integration (consolidated from singer-sdk)
- **flext-ldap**: LDAP connection and operations
- **flext-observability**: Monitoring and metrics

### Configuration

- Configuration class: `TargetLDAPConfig` in `src/flext_target_ldap/config.py`
- Uses Pydantic settings with type validation
- LDAP connection settings integrated with flext-ldap patterns

## Development Commands

### Essential Quality Gates (Run Before Committing)

```bash
make validate    # Complete validation: lint + type + security + test (MUST PASS)
make check       # Essential checks: lint + type only
make test        # Run tests with 90% coverage requirement
make lint        # Ruff linting with ALL rules enabled
make type-check  # Strict MyPy type checking
make security    # Security scans: bandit + pip-audit
```

### Development Setup

```bash
make setup       # Complete development setup (install + pre-commit hooks)
make install     # Install dependencies with Poetry
make install-dev # Install with dev dependencies
```

### Testing Commands

```bash
make test                 # All tests with coverage (90% minimum)
make test-unit           # Unit tests only (pytest -m "not integration")
make test-integration    # Integration tests only (pytest -m integration)
make test-singer         # Singer protocol tests (pytest -m singer)
make test-fast           # Run tests without coverage
make coverage-html       # Generate HTML coverage report
```

### Singer Target Operations

```bash
make test-target         # Test basic target functionality (--about, --version)
make validate-target-config # Validate target configuration JSON
make dry-run             # Run target in dry-run mode
make load                # Run target data loading with config/state files
```

### LDAP-Specific Operations

```bash
make ldap-connect        # Test LDAP connection
make ldap-write-test     # Test LDAP write operations
make ldap-schema         # Validate LDAP schema
```

### Code Quality

```bash
make format      # Format code with ruff
make fix         # Auto-fix all issues (format + lint)
```

### Environment Setup

```bash
# Start LDAP test servers
docker-compose up -d

# Access LDAP REDACTED_LDAP_BIND_PASSWORD interface at http://localhost:20080 (phpLDAPREDACTED_LDAP_BIND_PASSWORD)

# LDAP test servers:
# Source: localhost:20389 (dc=source,dc=com)
# Target: localhost:21389 (dc=target,dc=com)
```

## Testing Strategy

### Test Structure

- **Unit Tests**: Business logic and component testing
- **Integration Tests**: LDAP server integration with Docker
- **Singer Tests**: Singer protocol compliance testing

### Test Requirements

- Minimum 90% test coverage enforced (configurable in pyproject.toml)
- All tests must pass before commits
- Integration tests use Docker containers for LDAP servers
- Tests use pytest with asyncio mode enabled

### Running Specific Tests

```bash
pytest tests/ -v                      # All tests with verbose output
pytest tests/ -m unit                 # Unit tests only
pytest tests/ -m integration          # Integration tests only
pytest tests/ -m singer               # Singer protocol tests only
pytest tests/ -m "not slow"           # Exclude slow tests
pytest tests/ --lf                    # Last failed tests only
pytest tests/ -x                      # Stop on first failure
```

## Singer Protocol Integration

### CLI Usage

```bash
# Basic usage (reads JSONL from stdin)
target-ldap --config config.json < input.jsonl

# Target information
target-ldap --about
target-ldap --version
```

### Stream Processing

The target supports three main stream types:

- **users**: Maps to LDAP user entries (uid-based DNs)
- **groups**: Maps to LDAP group entries (cn-based DNs)
- **organizational_units**: Maps to LDAP OU entries

### Configuration

Configuration expects standard Singer format with LDAP-specific settings:

- `host`: LDAP server hostname (required)
- `base_dn`: Base DN for operations (required)
- `port`: LDAP server port (default: 389)
- `use_ssl`, `use_tls`: Security options (mutually exclusive)

## Code Patterns

### FlextResult Pattern

All operations return `FlextResult[T]` for consistent error handling:

```python
from flext_core import FlextResult

def orchestrate_data_loading(records: list[dict]) -> FlextResult[dict]:
    try:
        # Processing logic
        return FlextResult[None].ok({"processed": len(records)})
    except Exception as e:
        return FlextResult[None].fail(f"Loading failed: {e}")
```

### Dependency Injection

Uses flext-core DI container patterns (DRY implementation):

```python
from flext_target_ldap.infrastructure import get_flext_target_ldap_container

# Container uses flext-core patterns to eliminate code duplication
container = get_flext_target_ldap_container()
```

### Singer Sink Architecture

Stream-specific sinks inherit from base classes:

```python
from flext_target_ldap.sinks import LDAPBaseSink

class UsersSink(LDAPBaseSink):
    # Stream: "users"
    # DN pattern: uid={username},{base_dn}

class GroupsSink(LDAPBaseSink):
    # Stream: "groups"
    # DN pattern: cn={name},{base_dn}
```

## Quality Standards

### Zero Tolerance Enforcement

- **Strict Type Checking**: MyPy strict mode with comprehensive type annotations
- **90% Test Coverage**: Enforced minimum coverage with pytest-cov
- **Comprehensive Linting**: Ruff with extensive rule set
- **Security Scanning**: Bandit + pip-audit for vulnerability detection
- **Pre-commit Hooks**: Automated quality gates on commits

### Code Quality Tools Configuration

- **Ruff**: Python 3.13, extends `../.ruff-shared.toml`
- **MyPy**: Strict mode with Pydantic plugin, covers `src/` and `tests/`
- **Pytest**: Asyncio mode, strict markers, 8.0+ minimum version
- **Coverage**: Branch coverage, 90% minimum threshold

## Important File Locations

### Core Implementation Files

- `src/flext_target_ldap/target.py` - Main TargetLDAP class with Click CLI
- `src/flext_target_ldap/sinks.py` - Stream-specific sink implementations
- `src/flext_target_ldap/application/orchestrator.py` - Business logic orchestration
- `src/flext_target_ldap/client.py` - LDAP client and connection management
- `src/flext_target_ldap/config.py` - Pydantic configuration classes

### Test Organization

- `tests/conftest.py` - Pytest configuration and shared fixtures
- `tests/test_*.py` - Main test files (unit, integration, target functionality)

### Docker Environment

- `docker-compose.yml` - LDAP test servers (source:20389, target:21389) and phpLDAPREDACTED_LDAP_BIND_PASSWORD:20080
- Uses `osixia/openldap:1.5.0` and `osixia/phpldapREDACTED_LDAP_BIND_PASSWORD:0.9.0` images

## Troubleshooting

### Common Development Issues

**LDAP Connection Testing:**

```bash
make ldap-connect       # Test basic LDAP connectivity
docker-compose logs openldap-target  # Check target server logs
docker-compose logs openldap-source  # Check source server logs
```

**Test Failures:**

```bash
make test-fast          # Quick test run without coverage
pytest tests/ -x -vvs   # Stop on first failure with detailed output
pytest tests/ --lf      # Re-run only last failed tests
```

**Type Checking Issues:**

```bash
make type-check         # Run MyPy with strict configuration
poetry run mypy src/ --show-error-codes  # Show specific error codes
```

**Build and Dependency Issues:**

```bash
make clean              # Clean build artifacts and caches
make reset              # Deep clean including virtual environment
make diagnose           # Show environment diagnostics
make doctor             # Run health check + diagnostics
```
