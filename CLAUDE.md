# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

flext-target-ldap is a production-grade Singer target for loading identity data into LDAP directories (Active Directory, OpenLDAP, Oracle Directory Server). It's built on the Singer SDK with flext-core patterns for enterprise-grade directory synchronization.

## Development Commands

### Setup and Installation

```bash
# Install dependencies (uses Poetry)
make install-dev

# Complete development setup
make dev-setup
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test types
poetry run pytest tests/unit        # Unit tests only
poetry run pytest tests/integration # Integration tests
poetry run pytest tests/e2e         # End-to-end with Docker LDAP
poetry run pytest -m ldap          # LDAP-specific tests
poetry run pytest -m singer        # Singer protocol tests
```

### Code Quality

```bash
# Run all quality checks
make check

# Individual checks
make lint           # Ruff linting
make type-check     # MyPy type checking
make format         # Code formatting
make security       # Bandit security analysis
make pre-commit     # Pre-commit hooks
```

### Development Workflow

```bash
# Quick development test cycle
make dev-test

# Run target in development mode
make dev

# Build package
make build
```

### LDAP Testing Environment

```bash
# Start Docker LDAP servers for testing
docker-compose up openldap-source openldap-target

# Run target against test LDAP
target-ldap --config examples/config.json --test
```

## Architecture

### Core Components

- **TargetLDAP** (`src/flext_target_ldap/target.py`) - Main Singer target implementation
- **LDAPClient** (`src/flext_target_ldap/client.py`) - LDAP connection and operations wrapper using ldap3
- **Sinks** (`src/flext_target_ldap/sinks.py`) - Stream-specific data processors:
  - `UsersSink` - User object processing
  - `GroupsSink` - Group object and membership processing
  - `OrganizationalUnitsSink` - OU structure management
  - `GenericSink` - Fallback for custom objects
- **Config** (`src/flext_target_ldap/config.py`) - Pydantic configuration using flext-core patterns
- **Transformation** (`src/flext_target_ldap/transformation.py`) - Data mapping and validation engine

### Key Design Patterns

- **Singer Protocol Compliance** - Processes SCHEMA, RECORD, and STATE messages
- **Stream-based Processing** - Different sinks handle different data types (users, groups, OUs)
- **DN Template System** - Configurable Distinguished Name generation
- **Schema Validation** - Pre-flight validation against LDAP schema
- **Upsert Operations** - Create or update entries based on existence
- **Multi-valued Attributes** - Proper handling of arrays (groups, emails, etc.)

### Integration Points

- **flext-core** - Configuration patterns and domain models
- **flext-observability** - Structured logging and metrics
- **singer-sdk** - Singer protocol implementation
- **ldap3** - Python LDAP client library

## Configuration

### Required Settings

- `host` - LDAP server hostname
- `bind_dn` - Authentication DN
- `password` - Authentication password
- `base_dn` - Base DN for operations

### Optional Settings

- `port` - Server port (389/636)
- `use_ssl` - Enable LDAPS
- `timeout` - Connection timeout
- `validate_records` - Schema validation
- `dn_templates` - Custom DN generation templates
- `default_object_classes` - Object class mappings

## Testing Strategy

### Test Structure

- **Unit Tests** (`tests/test_*.py`) - Component testing with mocks
- **Integration Tests** (`tests/integration/`) - Mock LDAP server testing
- **E2E Tests** (`tests/e2e/`) - Docker LDAP container testing
- **Test Data** (`tests/e2e/ldif/`) - LDIF files for LDAP seeding

### Test Requirements

- 90%+ code coverage enforced
- LDAP connection mocking for unit tests
- Docker containers for realistic integration testing
- Singer protocol compliance validation

## Common Development Tasks

### Adding New Sink Types

1. Create new sink class inheriting from `LDAPSink`
2. Implement `process_record()` method
3. Add to sink mapping in `TargetLDAP.get_sink()`
4. Add corresponding tests

### Extending LDAP Operations

1. Add methods to `LDAPClient` class
2. Handle ldap3 exceptions appropriately
3. Add comprehensive logging
4. Write unit tests with mock connections

### Configuration Changes

1. Update `TargetLDAPConfig` class with new Pydantic fields
2. Add validation if needed
3. Update documentation and examples
4. Test configuration loading

## Troubleshooting

### Debug Mode

```bash
# Enable verbose logging
export TARGET_LDAP_LOG_LEVEL=DEBUG

# LDAP protocol tracing
export LDAP_TRACE_LEVEL=2

# Dry run testing
target-ldap --config config.json --dry-run
```

### Common Issues

- **Connection errors** - Check host, port, SSL settings
- **Authentication failures** - Verify bind_dn and password
- **Schema violations** - Enable validation and check object classes
- **DN conflicts** - Review DN templates and RDN attributes

## Dependencies

### Core Dependencies

- `singer-sdk` - Singer protocol implementation
- `ldap3` - LDAP client library
- `python-ldap` - Additional LDAP support
- `flext-core` - FLEXT framework patterns
- `flext-observability` - Logging and monitoring

### Development Dependencies

- `pytest` - Testing framework with asyncio support
- `ruff` - Fast Python linter and formatter
- `mypy` - Static type checking
- `pre-commit` - Git hook management

## Integration Notes

This target works with any Singer-compliant tap and integrates into the broader FLEXT ecosystem for directory synchronization and identity management pipelines.
