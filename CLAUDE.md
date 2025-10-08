# FLEXT TARGET LDAP - COMPREHENSIVE QUALITY REFACTORING

**Enterprise-Grade LDAP Data Loading Target with Singer Protocol Integration**  
**Version**: 2.1.0 | **Authority**: PROJECT | **Updated**: 2025-01-08  
**Environment**: `../.venv/bin/python` (No PYTHONPATH required)  
**Parent**: [FLEXT Workspace CLAUDE.md](../CLAUDE.md)
**Based on**: flext-core 0.9.9 with 75%+ test coverage (PROVEN FOUNDATION)

**Hierarchy**: This document provides project-specific standards based on workspace-level patterns defined in [../CLAUDE.md](../CLAUDE.md). For architectural principles, quality gates, and MCP server usage, reference the main workspace standards.

## 📋 DOCUMENT STRUCTURE & REFERENCES

**Quick Links**:
- **[~/.claude/commands/flext.md](~/.claude/commands/flext.md)**: Optimization command for module refactoring (USE with `/flext` command)
- **[../CLAUDE.md](../CLAUDE.md)**: FLEXT ecosystem standards and domain library rules

**CRITICAL INTEGRATION DEPENDENCIES**:
- **flext-meltano**: MANDATORY for ALL Singer operations (ZERO TOLERANCE for direct singer-sdk without flext-meltano)
- **flext-ldap**: MANDATORY for ALL LDAP operations (ZERO TOLERANCE for direct ldap3 imports)
- **flext-core**: Foundation patterns (FlextResult, FlextService, FlextContainer)

## 🔗 MCP SERVER INTEGRATION (MANDATORY)

| MCP Server              | Purpose                                                   | Status          |
| ----------------------- | --------------------------------------------------------- | --------------- |
| **serena-flext**        | Semantic code analysis, symbol manipulation, refactoring  | **MANDATORY**   |
| **sequential-thinking** | LDAP data loading and Singer protocol architecture        | **RECOMMENDED** |
| **context7**            | Third-party library documentation (Singer SDK, LDAP)      | **RECOMMENDED** |
| **github**              | Repository operations and Singer ecosystem PRs            | **ACTIVE**      |

**Usage**: `claude mcp list` for available servers, leverage for Singer-specific development patterns and LDAP loading analysis.

---

## 🎯 MISSION STATEMENT (NON-NEGOTIABLE) - LDAP TARGET DOMAIN

**OBJECTIVE**: Achieve 100% professional quality compliance across flext-target-ldap with zero regressions, following Singer protocol standards, LDAP enterprise patterns, Python 3.13+ standards, Pydantic best practices, and flext-core foundation patterns.

**CRITICAL REQUIREMENTS**:

- ✅ **95%+ pytest pass rate** with **75%+ coverage** (flext-core proven achievable at 79%)
- ✅ **Zero errors** in ruff, mypy (strict mode), and pyright across ALL source code
- ✅ **Unified classes per module** - single responsibility, no aliases, no wrappers, no helpers
- ✅ **Direct flext-core integration** - eliminate complexity, reduce configuration overhead
- ✅ **MANDATORY flext-cli usage** - ALL CLI projects use flext-cli for CLI AND output, NO direct Click/Rich
- ✅ **ZERO fallback tolerance** - no try/except fallbacks, no workarounds, always correct solutions
- ✅ **SOLID compliance** - proper abstraction, dependency injection, clean architecture
- ✅ **Professional English** - all docstrings, comments, variable names, function names
- ✅ **Incremental refactoring** - never rewrite entire modules, always step-by-step improvements
- ✅ **Real functional tests** - minimal mocks, test actual functionality with real LDAP environments
- ✅ **Production-ready code** - no workarounds, fallbacks, try-pass blocks, or incomplete implementations
- ✅ **Singer protocol compliance** - 100% Singer SDK specification adherence
- ✅ **LDAP enterprise patterns** - connection pooling, authentication, schema validation

**CURRENT ECOSYSTEM STATUS** (Evidence-based):

- 🔴 **Ruff Issues**: TBD - needs assessment
- 🟡 **MyPy Issues**: TBD - needs assessment
- 🟡 **Pyright Issues**: TBD - needs assessment
- 🔴 **Pytest Status**: TBD - needs assessment
- 🟢 **flext-core Foundation**: 79% coverage, fully functional API
- 🔵 **LDAP Domain**: Enterprise authentication, directory operations, connection pooling

---

## 🚨 ABSOLUTE PROHIBITIONS (ZERO TOLERANCE) - LDAP TARGET CONTEXT

### ❌ FORBIDDEN PRACTICES

1. **CODE QUALITY VIOLATIONS**:
   - object use of `# type: ignore` without specific error codes
   - object use of `object` types instead of proper type annotations
   - Silencing errors with ignore hints instead of fixing root causes
   - Creating wrappers, aliases, or compatibility facades
   - Using sed, awk, or automated scripts for complex refactoring

2. **ARCHITECTURE VIOLATIONS**:
   - Multiple classes per module (use single unified class per module)
   - Helper functions or constants outside of unified classes
   - Local reimplementation of flext-core functionality
   - Creating new modules instead of refactoring existing ones
   - Changing lint, type checker, or test framework behavior

3. **LDAP-SPECIFIC VIOLATIONS** (ABSOLUTE ZERO TOLERANCE):
   - **FORBIDDEN**: Hardcoded LDAP credentials in source code
   - **FORBIDDEN**: Connection leaks without proper cleanup
   - **FORBIDDEN**: Insecure authentication over plain connections
   - **FORBIDDEN**: DN injection vulnerabilities in template processing
   - **FORBIDDEN**: Ignoring LDAP schema constraints and validation
   - **FORBIDDEN**: Direct Python-ldap usage without flext-ldap integration
   - **FORBIDDEN**: Connection pooling bypasses for performance

4. **SINGER PROTOCOL VIOLATIONS** (ABSOLUTE ZERO TOLERANCE):
   - **FORBIDDEN**: Non-compliant Singer message formats
   - **FORBIDDEN**: State management bypasses or shortcuts
   - **FORBIDDEN**: Stream schema validation bypasses
   - **FORBIDDEN**: Batch processing without proper error handling
   - **FORBIDDEN**: Singer SDK pattern deviations

5. **CLI PROJECT VIOLATIONS** (ABSOLUTE ZERO TOLERANCE):
   - **MANDATORY**: ALL CLI projects MUST use `flext-cli` exclusively for CLI functionality AND data output
   - **FORBIDDEN**: Direct `import click` in any project code
   - **FORBIDDEN**: Direct `import rich` in any project code for output/formatting
   - **FORBIDDEN**: Local CLI implementations bypassing flext-cli
   - **FORBIDDEN**: object CLI functionality not going through flext-cli layer
   - **REQUIRED**: If flext-cli lacks functionality, IMPROVE flext-cli first - NEVER work around
   - **PRINCIPLE**: Fix the foundation, don't work around it
   - **OUTPUT RULE**: ALL data output, formatting, tables, progress bars MUST use flext-cli wrappers

6. **FALLBACK/WORKAROUND VIOLATIONS** (ABSOLUTE PROHIBITION):
   - **FORBIDDEN**: `try/except` blocks as fallback mechanisms
   - **FORBIDDEN**: Palliative solutions that mask root problems
   - **FORBIDDEN**: Temporary workarounds that become permanent
   - **FORBIDDEN**: "Good enough" solutions instead of correct solutions
   - **REQUIRED**: Always implement the correct solution, never approximate

7. **TESTING VIOLATIONS**:
   - Using excessive mocks instead of real functional tests
   - Accepting test failures and continuing development
   - Creating fake or placeholder test implementations
   - Testing code that doesn't actually execute real functionality

8. **DEVELOPMENT VIOLATIONS**:
   - Rewriting entire modules instead of incremental improvements
   - Skipping quality gates (ruff, mypy, pyright, pytest)
   - Modifying behavior of linting tools instead of fixing code
   - Rolling back git versions instead of fixing forward

---

## 🏗️ ARCHITECTURAL FOUNDATION (MANDATORY PATTERNS) - LDAP TARGET DOMAIN

### Core Integration Strategy

**PRIMARY FOUNDATION**: `flext-core` contains ALL base patterns - use exclusively, never reimplement locally

```python
# ✅ CORRECT - Direct usage of flext-core foundation (VERIFIED API)
from flext_core import (
    FlextResult,           # Railway pattern - has .data, .value, .unwrap()
    FlextModels,           # Pydantic models - Entity, Value, AggregateRoot classes
    FlextDomainService,    # Base service - Pydantic-based with Generic[T]
    FlextContainer,        # Dependency injection - use .get_global()
    FlextLogger,           # Structured logging - direct instantiation
    FlextConstants,        # System constants
    FlextExceptions        # Exception hierarchy
)

# ✅ MANDATORY - For ALL CLI projects use flext-cli exclusively
from flext_cli import (
    FlextCliApi,           # High-level CLI API for programmatic access
    FlextCliMain,          # Main CLI entry point and command registration
    FlextCliConfigs,        # Configuration management for CLI
    FlextCliConstants,     # CLI-specific constants
    # NEVER import click or rich directly - ALL CLI + OUTPUT through flext-cli
)

# ✅ MANDATORY - LDAP domain integration
from flext_ldap import (
    FlextLdapApi,          # High-level LDAP API with connection pooling
    FlextLdapConnection,   # Secure LDAP connection management
    FlextLdapConfig,       # LDAP configuration with enterprise patterns
    FlextLdapOperations,   # LDAP operations with error handling
)

# ✅ MANDATORY - Singer protocol integration
from flext_meltano import (
    FlextSingerTarget,     # Base Singer target implementation
    FlextSingerMessage,    # Singer message processing
    FlextSingerConfig,     # Singer configuration patterns
    FlextSingerStream,     # Stream processing with FlextResult patterns
)

# ❌ ABSOLUTELY FORBIDDEN - These imports are ZERO TOLERANCE violations
# import click           # FORBIDDEN - use flext-cli
# import rich            # FORBIDDEN - use flext-cli output wrappers
# import ldap            # FORBIDDEN - use flext-ldap
# import ldap3           # FORBIDDEN - use flext-ldap
# from singer_sdk import Target  # FORBIDDEN - use flext-meltano patterns

# ✅ CORRECT - Unified class per module pattern (LDAP TARGET DOMAIN)
class UnifiedFlextLdapTargetService(FlextDomainService):
    """Single unified LDAP target service class following flext-core patterns.

    This class consolidates all LDAP target operations:
    - Singer protocol implementation with stream processing
    - LDAP directory data loading with enterprise authentication
    - Connection pooling and performance optimization
    - Comprehensive error handling with FlextResult patterns
    - Enterprise observability and monitoring integration
    """

    def __init__(self, **data) -> None:
        """Initialize service with proper dependency injection."""
        super().__init__(**data)
        # Use direct class access - NO wrapper functions
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        self._ldap_api = FlextLdapApi()
        self._cli_api = FlextCliApi()

    def orchestrate_ldap_data_loading(
        self,
        singer_messages: list[dict],
        ldap_config: dict
    ) -> FlextResult[LdapLoadingResult]:
        """Orchestrate complete Singer-to-LDAP data loading pipeline."""
        return (
            self._validate_singer_messages(singer_messages)
            .flat_map(lambda msgs: self._establish_ldap_connection(ldap_config))
            .flat_map(lambda conn: self._process_schema_messages(msgs, conn))
            .flat_map(lambda schemas: self._transform_record_messages(msgs, schemas))
            .flat_map(lambda records: self._load_ldap_entries(records, conn))
            .flat_map(lambda results: self._update_singer_state(results))
            .map(lambda state: self._create_loading_result(state))
            .map_error(lambda e: f"LDAP data loading failed: {e}")
        )

    def validate_ldap_connectivity(self, config: dict) -> FlextResult[LdapConnectionValidation]:
        """Validate LDAP connection with comprehensive authentication testing."""
        return (
            self._validate_ldap_config(config)
            .flat_map(lambda cfg: self._test_ldap_connection(cfg))
            .flat_map(lambda conn: self._validate_ldap_permissions(conn))
            .flat_map(lambda perms: self._test_ldap_operations(conn))
            .map(lambda ops: self._create_connectivity_validation(ops))
            .map_error(lambda e: f"LDAP connectivity validation failed: {e}")
        )

    def optimize_ldap_performance(
        self,
        connection_config: dict,
        operation_metrics: dict
    ) -> FlextResult[LdapPerformanceOptimization]:
        """Optimize LDAP operations based on performance metrics."""
        return (
            self._analyze_ldap_performance_metrics(operation_metrics)
            .flat_map(lambda metrics: self._calculate_optimal_batch_size(metrics))
            .flat_map(lambda batch: self._configure_connection_pooling(connection_config, batch))
            .flat_map(lambda pool: self._implement_caching_strategy(pool))
            .map(lambda cache: self._create_performance_optimization(cache))
            .map_error(lambda e: f"LDAP performance optimization failed: {e}")
        )

# ✅ CORRECT - Module exports
__all__ = ["UnifiedFlextLdapTargetService"]
```

### Domain Modeling with VERIFIED flext-core Patterns (LDAP TARGET DOMAIN)

```python
# ✅ CORRECT - Using VERIFIED flext-core API patterns for LDAP domain
from flext_core import FlextModels, FlextResult

# LDAP domain models - inherit from verified FlextModels classes
class LdapConnectionConfig(FlextModels.Entity):
    """LDAP connection configuration with business rules validation."""

    host: str
    port: int
    bind_dn: str
    bind_password: str
    base_dn: str
    use_ssl: bool = False

    def validate_business_rules(self) -> FlextResult[None]:
        """Required abstract method implementation for LDAP config."""
        if not self.host.strip():
            return FlextResult[None].fail("LDAP host cannot be empty")
        if self.port < 1 or self.port > 65535:
            return FlextResult[None].fail("LDAP port must be between 1 and 65535")
        if not self.bind_dn.strip():
            return FlextResult[None].fail("LDAP bind DN cannot be empty")
        return FlextResult[None].ok(None)

class LdapEntry(FlextModels.Value):
    """LDAP entry value object with validation."""

    dn: str
    attributes: dict[str, list[str]]
    object_classes: list[str]

    def validate_business_rules(self) -> FlextResult[None]:
        """Required abstract method implementation for LDAP entries."""
        if not self.dn.strip():
            return FlextResult[None].fail("LDAP DN cannot be empty")
        if not self.object_classes:
            return FlextResult[None].fail("LDAP entry must have object classes")
        return FlextResult[None].ok(None)

# Singer integration with LDAP domain
class SingerToLdapTransformer:
    """Transform Singer messages to LDAP entries."""

    def __init__(self) -> None:
        self._container = FlextContainer.get_global()

    def transform_record_to_ldap_entry(
        self,
        singer_record: dict,
        stream_config: dict
    ) -> FlextResult[LdapEntry]:
        """Transform Singer record to LDAP entry with validation."""
        try:
            # Extract DN using template
            dn_template = stream_config.get("dn_template", "")
            dn = self._build_dn_from_template(dn_template, singer_record)
            if not dn:
                return FlextResult[LdapEntry].fail("Failed to build DN from template")

            # Map attributes
            attribute_mapping = stream_config.get("attribute_mapping", {})
            ldap_attributes = self._map_singer_to_ldap_attributes(singer_record, attribute_mapping)

            # Get object classes
            object_classes = stream_config.get("object_classes", [])
            if not object_classes:
                return FlextResult[LdapEntry].fail("No object classes specified")

            # Create LDAP entry
            ldap_entry = LdapEntry(
                dn=dn,
                attributes=ldap_attributes,
                object_classes=object_classes
            )

            # Validate business rules
            validation_result = ldap_entry.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[LdapEntry].fail(f"LDAP entry validation failed: {validation_result.error}")

            return FlextResult[LdapEntry].ok(ldap_entry)

        except Exception as e:
            return FlextResult[LdapEntry].fail(f"Singer to LDAP transformation failed: {e}")
```

### CLI Development Patterns (MANDATORY FOR ALL CLI PROJECTS) - LDAP TARGET DOMAIN

```python
# ✅ CORRECT - ALL CLI projects MUST use flext-cli exclusively
from flext_cli import FlextCliApi, FlextCliMain, FlextCliConfigs
# ❌ FORBIDDEN - NEVER import click directly
# import click  # THIS IS ABSOLUTELY FORBIDDEN

class LdapTargetCliService:
    """CLI service using flext-cli foundation - NO Click imports allowed.

    LDAP TARGET SPECIALIZATION:
    - flext-cli automatically loads .env from execution root
    - flext-core provides configuration infrastructure
    - Project ONLY describes LDAP-specific configuration schema
    """

    def __init__(self) -> None:
        """Initialize LDAP target CLI service with automatic configuration loading."""
        # ✅ AUTOMATIC: Configuration loaded transparently by flext-cli/flext-core
        self._cli_api = FlextCliApi()
        self._config = FlextCliConfigs()  # Automatically includes .env + defaults + CLI params
        self._ldap_api = FlextLdapApi()

    def define_ldap_target_configuration_schema(self) -> FlextResult[dict]:
        """Define LDAP target configuration schema extending universal patterns."""
        # ✅ CORRECT: LDAP-specific schema extending universal patterns
        ldap_target_config_schema = {
            # LDAP connection configuration (LDAP target specific)
            "ldap": {
                "host": {
                    "default": "localhost",              # Level 3: DEFAULT CONSTANTS
                    "env_var": "LDAP_HOST",              # Levels 1&2: ENV VARS → CONFIG FILE
                    "cli_param": "--ldap-host",          # Level 4: CLI PARAMETERS
                    "config_formats": {                  # Multi-format support
                        "env": "LDAP_HOST",
                        "toml": "ldap.host",
                        "yaml": "ldap.host",
                        "json": "ldap.host"
                    },
                    "type": str,
                    "required": True,
                    "description": "LDAP server hostname"
                },
                "port": {
                    "default": 389,                      # Level 3: DEFAULT CONSTANTS
                    "env_var": "LDAP_PORT",              # Levels 1&2: ENV VARS → CONFIG FILE
                    "cli_param": "--ldap-port",          # Level 4: CLI PARAMETERS
                    "config_formats": {
                        "env": "LDAP_PORT",
                        "toml": "ldap.port",
                        "yaml": "ldap.port",
                        "json": "ldap.port"
                    },
                    "type": int,
                    "required": False,
                    "description": "LDAP server port"
                },
                "credentials": {
                    "bind_dn": {
                        "default": None,                 # Level 3: No default for security
                        "env_var": "LDAP_BIND_DN",       # Levels 1&2: ENV VARS → CONFIG FILE
                        "cli_param": "--bind-dn",        # Level 4: CLI PARAMETERS
                        "config_formats": {
                            "env": "LDAP_BIND_DN",
                            "toml": "ldap.credentials.bind_dn",
                            "yaml": "ldap.credentials.bind_dn",
                            "json": "ldap.credentials.bind_dn"
                        },
                        "type": str,
                        "required": True,
                        "description": "LDAP bind DN for authentication"
                    },
                    "bind_password": {
                        "default": None,                 # Level 3: No default for security
                        "env_var": "LDAP_BIND_PASSWORD", # Levels 1&2: ENV VARS → CONFIG FILE
                        "cli_param": "--bind-password",  # Level 4: CLI PARAMETERS (discouraged)
                        "config_formats": {
                            "env": "LDAP_BIND_PASSWORD",
                            "toml": "ldap.credentials.bind_password",
                            "yaml": "ldap.credentials.bind_password",
                            "json": "ldap.credentials.bind_password"
                        },
                        "type": str,
                        "required": True,
                        "sensitive": True,               # Mark as sensitive data
                        "description": "LDAP bind password"
                    }
                },
                "base_dn": {
                    "default": "dc=example,dc=com",      # Level 3: DEFAULT CONSTANTS
                    "env_var": "LDAP_BASE_DN",           # Levels 1&2: ENV VARS → CONFIG FILE
                    "cli_param": "--base-dn",            # Level 4: CLI PARAMETERS
                    "config_formats": {
                        "env": "LDAP_BASE_DN",
                        "toml": "ldap.base_dn",
                        "yaml": "ldap.base_dn",
                        "json": "ldap.base_dn"
                    },
                    "type": str,
                    "required": True,
                    "description": "LDAP base DN for operations"
                },
                "use_ssl": {
                    "default": False,                    # Level 3: DEFAULT CONSTANTS
                    "env_var": "LDAP_USE_SSL",           # Levels 1&2: ENV VARS → CONFIG FILE
                    "cli_param": "--use-ssl",            # Level 4: CLI PARAMETERS
                    "config_formats": {
                        "env": "LDAP_USE_SSL",
                        "toml": "ldap.use_ssl",
                        "yaml": "ldap.use_ssl",
                        "json": "ldap.use_ssl"
                    },
                    "type": bool,
                    "required": False,
                    "description": "Enable SSL/TLS for LDAP connection"
                }
            },
            # Singer target configuration (Singer protocol specific)
            "singer": {
                "batch_size": {
                    "default": 100,                      # Level 3: DEFAULT CONSTANTS
                    "env_var": "SINGER_BATCH_SIZE",      # Levels 1&2: ENV VARS → CONFIG FILE
                    "cli_param": "--batch-size",         # Level 4: CLI PARAMETERS
                    "config_formats": {
                        "env": "SINGER_BATCH_SIZE",
                        "toml": "singer.batch_size",
                        "yaml": "singer.batch_size",
                        "json": "singer.batch_size"
                    },
                    "type": int,
                    "required": False,
                    "description": "Singer batch size for processing"
                },
                "max_connections": {
                    "default": 5,                        # Level 3: DEFAULT CONSTANTS
                    "env_var": "SINGER_MAX_CONNECTIONS", # Levels 1&2: ENV VARS → CONFIG FILE
                    "cli_param": "--max-connections",    # Level 4: CLI PARAMETERS
                    "config_formats": {
                        "env": "SINGER_MAX_CONNECTIONS",
                        "toml": "singer.max_connections",
                        "yaml": "singer.max_connections",
                        "json": "singer.max_connections"
                    },
                    "type": int,
                    "required": False,
                    "description": "Maximum LDAP connections for parallel processing"
                }
            }
        }

        # Register LDAP target schema with flext-cli
        schema_result = self._config.register_universal_schema(ldap_target_config_schema)
        if schema_result.is_failure:
            return FlextResult[dict].fail(f"LDAP target schema registration failed: {schema_result.error}")

        return FlextResult[dict].ok(ldap_target_config_schema)

    def create_ldap_target_cli_interface(self) -> FlextResult[FlextCliMain]:
        """Create LDAP target CLI interface using flext-cli patterns."""
        # Initialize main CLI handler
        main_cli = FlextCliMain(
            name="target-ldap",
            description="FLEXT Target LDAP - Enterprise LDAP data loading with Singer protocol"
        )

        # Register LDAP target command groups
        ldap_result = main_cli.register_command_group("ldap", self._create_ldap_commands)
        if ldap_result.is_failure:
            return FlextResult[FlextCliMain].fail(f"LDAP commands registration failed: {ldap_result.error}")

        singer_result = main_cli.register_command_group("singer", self._create_singer_commands)
        if singer_result.is_failure:
            return FlextResult[FlextCliMain].fail(f"Singer commands registration failed: {singer_result.error}")

        return FlextResult[FlextCliMain].ok(main_cli)

    def _create_ldap_commands(self) -> FlextResult[dict]:
        """Create LDAP-specific commands using flext-cli patterns."""
        commands = {
            "test-connection": self._cli_api.create_command(
                name="test-connection",
                description="Test LDAP server connectivity",
                handler=self._handle_ldap_test_connection,
                arguments=["--host", "--port", "--bind-dn"],
                output_format="table"
            ),
            "validate-schema": self._cli_api.create_command(
                name="validate-schema",
                description="Validate LDAP schema compatibility",
                handler=self._handle_ldap_validate_schema,
                output_format="json"
            )
        }
        return FlextResult[dict].ok(commands)

    def _handle_ldap_test_connection(self, args: dict) -> FlextResult[str]:
        """Handle LDAP connection testing - proper error handling, no fallbacks."""
        # Get LDAP configuration
        ldap_config_result = self._get_ldap_configuration_from_args(args)
        if ldap_config_result.is_failure:
            return FlextResult[str].fail(f"LDAP config error: {ldap_config_result.error}")

        ldap_config = ldap_config_result.unwrap()

        # Test connection through flext-ldap API
        connection_result = self._ldap_api.test_connection(ldap_config)
        if connection_result.is_failure:
            return FlextResult[str].fail(f"LDAP connection failed: {connection_result.error}")

        connection_info = connection_result.unwrap()
        return FlextResult[str].ok(f"LDAP connection successful: {connection_info}")

# ✅ CORRECT - CLI entry point using flext-cli for LDAP target
def main() -> None:
    """Main CLI entry point for LDAP target - uses flext-cli, never Click directly."""
    cli_service = LdapTargetCliService()
    cli_result = cli_service.create_ldap_target_cli_interface()

    if cli_result.is_failure:
        # Use flext-cli for error output
        cli_api = FlextCliApi()
        error_output = cli_api.format_error_message(
            message=f"LDAP target CLI initialization failed: {cli_result.error}",
            error_type="initialization",
            suggestions=[
                "Check flext-cli installation",
                "Verify LDAP configuration",
                "Ensure flext-ldap dependencies"
            ]
        )
        cli_api.display_error(error_output.unwrap() if error_output.is_success else cli_result.error)
        exit(1)

    cli = cli_result.unwrap()
    cli.run()

# ✅ CORRECT - Module exports for LDAP target CLI
__all__ = ["LdapTargetCliService", "main"]
```

---

## 📊 QUALITY ASSESSMENT PROTOCOL - LDAP TARGET DOMAIN

### Phase 1: Comprehensive Issue Identification

**MANDATORY FIRST STEP**: Get precise counts of all quality issues:

```bash
# Count exact number of issues across all tools (LDAP target specific)
echo "=== FLEXT TARGET LDAP QUALITY ASSESSMENT ==="
echo "============================================="

echo "=== RUFF ISSUES ==="
ruff check . --output-format=github | wc -l

echo "=== MYPY ISSUES ==="
mypy src/flext_target_ldap/ --show-error-codes --no-error-summary 2>&1 | grep -E "error:|note:" | wc -l

echo "=== PYRIGHT ISSUES ==="
pyright src/flext_target_ldap/ --level error 2>&1 | grep -E "error|warning" | wc -l

echo "=== PYTEST RESULTS ==="
pytest tests/ --tb=no -q 2>&1 | grep -E "failed|passed|error" | tail -1

echo "=== CURRENT COVERAGE ==="
pytest tests/ --cov=src/flext_target_ldap --cov-report=term-missing --tb=no 2>&1 | grep "TOTAL"

echo "=== LDAP INTEGRATION TESTS ==="
pytest tests/integration/test_ldap_operations.py --tb=no -q 2>&1 | grep -E "failed|passed|error" | tail -1

echo "=== SINGER PROTOCOL COMPLIANCE ==="
pytest tests/singer/ --tb=no -q 2>&1 | grep -E "failed|passed|error" | tail -1
```

### Phase 2: Systematic Resolution Workflow

**PRIORITY ORDER** (High impact first - LDAP target focused):

1. **Fix import and syntax errors** (prevents other tools from running)
2. **Resolve LDAP connection and authentication issues** (core functionality)
3. **Fix Singer protocol compliance issues** (specification adherence)
4. **Address type safety issues** (mypy strict mode + pyright)
5. **Address code quality violations** (ruff with all rules enabled)
6. **Achieve test coverage** (75%+ with real LDAP functional tests)
7. **Optimize and consolidate** (remove duplication, improve LDAP performance)

### Phase 3: Continuous Validation

**AFTER EVERY CHANGE** (mandatory validation cycle):

```bash
# LDAP target validation cycle (must pass before proceeding)
ruff check src/flext_target_ldap/ --fix-only      # Auto-fix what can be auto-fixed
ruff check src/flext_target_ldap/                 # Verify zero remaining issues
mypy src/flext_target_ldap/ --strict --no-error-summary  # Verify zero type errors
pytest tests/ --tb=short -x                       # Stop on first test failure

# LDAP-specific validation
make test-ldap-integration                         # LDAP server integration tests
make test-singer-compliance                        # Singer protocol compliance
```

---

## 🛠️ INCREMENTAL REFACTORING METHODOLOGY - LDAP TARGET DOMAIN

### Strategy: Progressive Enhancement (NOT Rewriting)

**APPROACH**: Each refactoring cycle improves one specific aspect while maintaining all existing LDAP functionality.

#### Cycle 1: LDAP Foundation Consolidation

```python
# BEFORE - Multiple scattered LDAP implementations
class LdapConnectionManager:
    def connect(self): pass

class LdapOperations:
    def add_entry(self): pass

class SingerProcessor:
    def process_messages(self): pass

# Scattered helper functions
def build_dn_from_template(): pass

# AFTER - Single unified class (incremental improvement)
class UnifiedFlextLdapTargetService(FlextDomainService):
    """Consolidated LDAP target service following single responsibility principle."""

    def orchestrate_ldap_data_loading(
        self,
        singer_messages: list[dict],
        ldap_config: dict
    ) -> FlextResult[LdapLoadingResult]:
        """Former multiple services now unified with proper error handling."""
        # Implementation using flext-core patterns with LDAP specialization

    def validate_ldap_connectivity(self, config: dict) -> FlextResult[LdapConnectionValidation]:
        """Former LdapConnectionManager functionality with proper error handling."""
        # Implementation using flext-ldap integration

    def _build_dn_from_template(self, template: str, data: dict) -> str:
        """Former helper function now as private method."""
        # Implementation as part of unified class
```

#### Cycle 2: Singer Protocol Integration Enhancement

```python
# BEFORE - Weak Singer integration
def process_singer_message(message: object) -> object:
    return message

# AFTER - Strong Singer protocol compliance (incremental improvement)
def process_singer_schema_message(self, message: dict) -> FlextResult[LdapSchemaProcessing]:
    """Process Singer SCHEMA messages with full type safety and error handling."""
    if not isinstance(message, dict):
        return FlextResult[LdapSchemaProcessing].fail("Invalid message type")

    if message.get("type") != "SCHEMA":
        return FlextResult[LdapSchemaProcessing].fail("Expected SCHEMA message")

    try:
        schema_validation = self._validate_singer_schema(message)
        if schema_validation.is_failure:
            return FlextResult[LdapSchemaProcessing].fail(f"Schema validation failed: {schema_validation.error}")

        ldap_mapping = self._map_schema_to_ldap_objectclasses(schema_validation.unwrap())
        if ldap_mapping.is_failure:
            return FlextResult[LdapSchemaProcessing].fail(f"LDAP mapping failed: {ldap_mapping.error}")

        return FlextResult[LdapSchemaProcessing].ok(ldap_mapping.unwrap())

    except Exception as e:
        return FlextResult[LdapSchemaProcessing].fail(f"Singer schema processing failed: {e}")
```

#### Cycle 3: Test Coverage Achievement with Real LDAP Integration

```python
# NEW - Comprehensive functional tests with real LDAP servers
class TestUnifiedLdapTargetServiceComplete:
    """Complete test coverage for unified LDAP target service."""

    @pytest.fixture(scope="session")
    def ldap_test_environment(self):
        """Real LDAP test environment with Docker containers."""
        with LdapTestEnvironment() as env:
            env.start_ldap_server()
            env.setup_test_schemas()
            env.load_test_data()
            yield env.get_connection_config()

    @pytest.mark.parametrize("singer_message_type,expected_result", [
        ({"type": "SCHEMA", "stream": "users", "schema": USER_SCHEMA}, "success"),
        ({"type": "RECORD", "stream": "users", "record": {"uid": "testuser"}}, "success"),
        ({"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}, "success"),
        ({}, "failure"),  # Invalid message
        ({"type": "INVALID"}, "failure"),  # Invalid type
    ])
    def test_singer_message_processing_scenarios(
        self,
        ldap_test_environment,
        singer_message_type,
        expected_result
    ):
        """Test all Singer message processing scenarios comprehensively."""
        service = UnifiedFlextLdapTargetService()
        result = service.process_singer_message(singer_message_type, ldap_test_environment)

        if expected_result == "success":
            assert result.is_success
        else:
            assert result.is_failure

    def test_ldap_error_handling_comprehensive(self, ldap_test_environment):
        """Test all LDAP error handling paths."""
        service = UnifiedFlextLdapTargetService()

        # Test all LDAP failure modes
        error_cases = [
            {"host": "invalid-host", "port": 389},     # Connection failure
            {"host": "localhost", "bind_dn": "invalid"}, # Authentication failure
            {"valid_config": True, "invalid_dn": "malformed"}, # DN format error
        ]

        for case in error_cases:
            result = service.validate_ldap_connectivity(case)
            assert result.is_failure, f"Should fail for case: {case}"
            assert result.error, "Error message should be present"

    def test_integration_with_flext_core_and_ldap(self, ldap_test_environment):
        """Test integration with flext-core and flext-ldap components."""
        service = UnifiedFlextLdapTargetService()

        # Test flext-core container integration
        container_result = service._container.get("ldap_service")

        # Test flext-ldap integration
        ldap_api_result = service._ldap_api.test_connection(ldap_test_environment)
        assert ldap_api_result.is_success or ldap_api_result.is_failure  # Either is valid

        # Test flext-cli integration for CLI commands
        cli_result = service._cli_api.format_output({"test": "data"}, "table")
        assert cli_result.is_success or cli_result.is_failure  # Either is valid
```

---

## 🔧 TOOL-SPECIFIC RESOLUTION STRATEGIES - LDAP TARGET DOMAIN

### Ruff Issues Resolution (LDAP Target Specific)

```bash
# LDAP target specific ruff analysis
ruff check src/flext_target_ldap/ --select F    # Pyflakes errors (critical)
ruff check src/flext_target_ldap/ --select E9   # Syntax errors (critical)
ruff check src/flext_target_ldap/ --select F821 # Undefined name (critical)

# LDAP-specific import issues
ruff check src/flext_target_ldap/ --select I    # Import sorting
ruff check src/flext_target_ldap/ --select F401 # Unused imports

# Auto-fix LDAP target code
ruff check src/flext_target_ldap/ --fix-only --select I,F401,E,W
```

**LDAP TARGET RESOLUTION PATTERNS**:

```python
# ✅ CORRECT - Fix LDAP magic values
# BEFORE
if timeout > 30:  # Magic number for LDAP timeout

# AFTER
class LdapTargetConstants:
    DEFAULT_CONNECTION_TIMEOUT = 30
    DEFAULT_BIND_TIMEOUT = 15
    DEFAULT_BATCH_SIZE = 100
    MAX_RETRY_ATTEMPTS = 3

if timeout > LdapTargetConstants.DEFAULT_CONNECTION_TIMEOUT:

# ✅ CORRECT - Fix complex LDAP functions
# BEFORE
def process_singer_to_ldap(data):
    # 50+ lines of mixed LDAP and Singer logic

# AFTER
class LdapSingerProcessor:
    def process(self, singer_data: SingerMessage) -> FlextResult[LdapProcessingResult]:
        """Main processing method with clear separation."""
        return (
            self._validate_singer_message(singer_data)
            .flat_map(self._transform_to_ldap_format)
            .flat_map(self._validate_ldap_constraints)
            .flat_map(self._execute_ldap_operations)
            .map(self._create_processing_result)
        )

    def _validate_singer_message(self, message: SingerMessage) -> FlextResult[SingerMessage]:
        """Focused Singer message validation logic."""

    def _transform_to_ldap_format(self, message: SingerMessage) -> FlextResult[LdapEntry]:
        """Focused LDAP transformation logic."""

    def _execute_ldap_operations(self, entry: LdapEntry) -> FlextResult[LdapOperationResult]:
        """Focused LDAP operation execution logic."""
```

### MyPy Issues Resolution (LDAP Target Specific)

```python
# ✅ CORRECT - Proper LDAP-specific generic typing
from typing import Generic, TypeVar, Protocol
from flext_ldap import FlextLdapConnection

T = TypeVar('T')
LdapEntryType = TypeVar('LdapEntryType', bound='LdapEntry')

class LdapTargetProcessor(Generic[LdapEntryType]):
    """Generic LDAP target processor with proper type constraints."""

    def process_ldap_entry(self, entry: LdapEntryType) -> FlextResult[LdapEntryType]:
        """Process LDAP entry maintaining type safety."""
        return FlextResult[LdapEntryType].ok(entry)

# ✅ CORRECT - LDAP Protocol usage instead of object
class LdapProcessable(Protocol):
    """Protocol defining LDAP processable interface."""

    def get_dn(self) -> str: ...
    def get_attributes(self) -> dict[str, list[str]]: ...
    def get_object_classes(self) -> list[str]: ...

def process_ldap_entry(entry: LdapProcessable) -> FlextResult[dict]:
    """Process any entry implementing LdapProcessable protocol."""
    try:
        dn = entry.get_dn()
        attributes = entry.get_attributes()
        object_classes = entry.get_object_classes()

        return FlextResult[dict].ok({
            "dn": dn,
            "attributes": attributes,
            "object_classes": object_classes
        })
    except Exception as e:
        return FlextResult[dict].fail(f"LDAP entry processing failed: {e}")
```

---

## 🔬 CLI TESTING AND DEBUGGING METHODOLOGY - LDAP TARGET DOMAIN

### Critical Principle: LDAP Configuration Hierarchy and .env Detection

**LDAP TARGET SPECIALIZATION**: Configuration follows strict priority hierarchy with ENVIRONMENT VARIABLES taking precedence over .env files. The .env file is automatically detected from CURRENT execution directory. All LDAP testing and debugging MUST use FLEXT ecosystem exclusively.

**CORRECT PRIORITY ORDER**:

```
1. ENVIRONMENT VARIABLES  (export LDAP_HOST=prod-ldap-server - HIGHEST PRIORITY)
2. .env FILE             (LDAP_HOST=localhost from execution directory)
3. DEFAULT CONSTANTS     (LDAP_HOST="localhost" in code)
4. CLI PARAMETERS        (--ldap-host override-server for specific overrides)
```

#### 🔧 LDAP TARGET CLI TESTING PATTERN

```bash
# ✅ CORRECT - LDAP target CLI testing pattern
# Configuration file automatically detected from current directory

# LDAP Target CLI testing commands:
# Phase 1: CLI Debug Mode Testing (MANDATORY FLEXT-CLI)
python -m target_ldap --debug test-connection \
  --ldap-host localhost \
  --ldap-port 389 \
  --bind-dn "cn=admin,dc=test,dc=com" \
  --config-file ldap-test.env

# Phase 2: CLI Trace Mode Testing (FLEXT-CLI + FLEXT-CORE LOGGING)
export LOG_LEVEL=DEBUG
export LDAP_TRACE_ENABLED=true
python -m target_ldap test-connection \
  --ldap-host localhost \
  --ldap-port 389 \
  --config-format toml

# Phase 3: CLI LDAP Schema Validation (LDAP-SPECIFIC)
python -m target_ldap validate-ldap-schema --debug --config-format yaml

# Phase 4: CLI Singer Protocol Testing (SINGER-SPECIFIC)
python -m target_ldap test-singer-compliance --debug --trace

# Phase 5: CLI LDAP Integration Testing (FULL INTEGRATION)
python -m target_ldap test-ldap-integration \
  --ldap-host localhost \
  --ldap-port 389 \
  --debug --trace --config-file production.toml
```

### 🚫 ABSOLUTELY FORBIDDEN - External LDAP Testing Patterns

**ZERO TOLERANCE VIOLATIONS** - These patterns are absolutely forbidden:

```bash
# ❌ FORBIDDEN - External LDAP testing tools
# ldapsearch -h localhost -p 389 -D "cn=admin,dc=test,dc=com" -w "password"  # FORBIDDEN
# ldapadd -h localhost -p 389 -D "cn=admin,dc=test,dc=com" -w "password"     # FORBIDDEN
# ldapmodify -h localhost -p 389 -D "cn=admin,dc=test,dc=com"                # FORBIDDEN

# ❌ FORBIDDEN - Custom LDAP testing scripts bypassing FLEXT
# python custom_test_ldap_connection.py     # FORBIDDEN
# python manual_ldap_operations.py          # FORBIDDEN
# python direct_ldap_integration.py         # FORBIDDEN

# ❌ FORBIDDEN - Manual .env loading for LDAP
# export $(cat .env | xargs)     # FORBIDDEN - flext-cli does this automatically
# source .env                    # FORBIDDEN - flext-cli handles .env loading

# ❌ FORBIDDEN - Non-FLEXT LDAP diagnostic tools
# netcat -zv localhost 389       # FORBIDDEN - use CLI test commands
# telnet localhost 389           # FORBIDDEN - use CLI test commands
# nmap -p 389 localhost          # FORBIDDEN - use CLI diagnostic commands
```

### ✅ CORRECT - FLEXT CLI Testing and Debugging for LDAP Target

```python
# ✅ CORRECT - LDAP target testing through FLEXT ecosystem exclusively
from flext_core import FlextResult, get_logger
from flext_cli import FlextCliApi, FlextCliConfigs
from flext_ldap import FlextLdapApi, FlextLdapConnection
from flext_meltano import FlextSingerTarget

class LdapTargetCliTestingService:
    """LDAP target CLI testing service using FLEXT ecosystem - .env automatically loaded."""

    def __init__(self) -> None:
        """Initialize LDAP target CLI testing with automatic .env configuration loading."""
        # ✅ AUTOMATIC: .env loaded transparently by FLEXT ecosystem
        self._logger = get_logger("ldap_target_testing")
        self._cli_api = FlextCliApi()
        self._config = FlextCliConfigs()  # Automatically loads .env + defaults + CLI params
        self._ldap_api = FlextLdapApi()

    def debug_ldap_target_configuration(self) -> FlextResult[dict]:
        """Debug LDAP target configuration using FLEXT patterns - .env as source of truth."""
        self._logger.debug("Starting LDAP target configuration debugging")

        # ✅ CORRECT: Access configuration through FLEXT API (includes .env automatically)
        config_result = self._config.get_all_configuration()
        if config_result.is_failure:
            return FlextResult[dict].fail(f"Configuration access failed: {config_result.error}")

        config_data = config_result.unwrap()

        # Debug output through FLEXT CLI API
        debug_display_result = self._cli_api.display_debug_information(
            title="LDAP Target Configuration Debug (ENV → .env → DEFAULT → CLI)",
            data=config_data,
            format_type="tree"  # flext-cli handles formatted output
        )

        if debug_display_result.is_failure:
            return FlextResult[dict].fail(f"Debug display failed: {debug_display_result.error}")

        return FlextResult[dict].ok(config_data)

    def test_ldap_connectivity_debug(self) -> FlextResult[dict]:
        """Test LDAP connectivity with debug logging - FLEXT-LDAP exclusively."""
        self._logger.debug("Starting LDAP connectivity testing")

        # ✅ CORRECT: Get LDAP configuration from .env through FLEXT config
        ldap_config_result = self._config.get_ldap_configuration()
        if ldap_config_result.is_failure:
            return FlextResult[dict].fail(f"LDAP config access failed: {ldap_config_result.error}")

        ldap_config = ldap_config_result.unwrap()

        # ✅ CORRECT: Test connection through FLEXT-LDAP API (NO external tools)
        connection_result = self._ldap_api.test_connection_with_debug(
            host=ldap_config["host"],
            port=ldap_config["port"],
            bind_dn=ldap_config["bind_dn"],
            bind_password=ldap_config["bind_password"],
            debug_mode=True
        )

        if connection_result.is_failure:
            # Display debug information through FLEXT CLI
            self._cli_api.display_error_with_debug(
                error_message=f"LDAP connection failed: {connection_result.error}",
                debug_data=ldap_config,
                suggestions=[
                    "Check .env file LDAP configuration",
                    "Verify LDAP server is running",
                    "Validate network connectivity",
                    "Check LDAP credentials and permissions"
                ]
            )
            return FlextResult[dict].fail(connection_result.error)

        # Display success with debug information
        connection_info = connection_result.unwrap()
        self._cli_api.display_success_with_debug(
            success_message="LDAP connection successful",
            debug_data=connection_info,
            format_type="table"
        )

        return FlextResult[dict].ok(connection_info)

    def test_singer_protocol_compliance_debug(self, test_messages: list[dict]) -> FlextResult[dict]:
        """Test Singer protocol compliance with debug traces - FLEXT-MELTANO exclusively."""
        self._logger.debug("Starting Singer protocol compliance testing")

        # ✅ CORRECT: Process Singer messages through FLEXT-MELTANO API with debug mode
        compliance_result = self._process_singer_messages_with_debug(
            messages=test_messages,
            debug_mode=True,
            trace_mode=True,
            validation_level="strict"
        )

        if compliance_result.is_failure:
            # Display debug information through FLEXT CLI
            self._cli_api.display_error_with_debug(
                error_message=f"Singer protocol compliance failed: {compliance_result.error}",
                debug_data={"test_messages": test_messages},
                suggestions=[
                    "Check Singer message format and structure",
                    "Verify stream schema definitions",
                    "Validate Singer protocol specification compliance",
                    "Check LDAP target configuration for Singer integration"
                ]
            )
            return FlextResult[dict].fail(compliance_result.error)

        # Display compliance results with debug information
        compliance_info = compliance_result.unwrap()
        self._cli_api.display_success_with_debug(
            success_message=f"Singer protocol compliance successful: {len(compliance_info['processed_messages'])} messages processed",
            debug_data=compliance_info,
            format_type="summary"
        )

        return FlextResult[dict].ok(compliance_info)

    def validate_ldap_target_environment_debug(self) -> FlextResult[dict]:
        """Validate complete LDAP target environment using FLEXT ecosystem - .env as truth source."""
        validation_results = {}

        # Phase 1: Configuration validation (.env + defaults + CLI)
        config_result = self.debug_ldap_target_configuration()
        if config_result.is_success:
            validation_results["configuration"] = "✅ PASSED"
        else:
            validation_results["configuration"] = f"❌ FAILED: {config_result.error}"

        # Phase 2: LDAP connectivity validation (flext-ldap)
        ldap_result = self.test_ldap_connectivity_debug()
        if ldap_result.is_success:
            validation_results["ldap_connectivity"] = "✅ PASSED"
        else:
            validation_results["ldap_connectivity"] = f"❌ FAILED: {ldap_result.error}"

        # Phase 3: Singer protocol compliance validation (flext-meltano)
        singer_test_messages = self._generate_test_singer_messages()
        singer_result = self.test_singer_protocol_compliance_debug(singer_test_messages)
        if singer_result.is_success:
            validation_results["singer_compliance"] = "✅ PASSED"
        else:
            validation_results["singer_compliance"] = f"❌ FAILED: {singer_result.error}"

        # Phase 4: FLEXT ecosystem integration validation
        ecosystem_result = self._validate_flext_ecosystem_integration()
        if ecosystem_result.is_success:
            validation_results["flext_ecosystem"] = "✅ PASSED"
        else:
            validation_results["flext_ecosystem"] = f"❌ FAILED: {ecosystem_result.error}"

        # Display complete validation results through FLEXT CLI
        self._cli_api.display_validation_results(
            title="Complete LDAP Target Environment Validation (ENV → .env → DEFAULT → CLI)",
            results=validation_results,
            format_type="detailed_table"
        )

        return FlextResult[dict].ok(validation_results)
```

### 🎯 LDAP Target CLI Testing Best Practices (.env as Source of Truth)

#### 1. LDAP Target Configuration Testing Priority Order

```bash
# ✅ CORRECT - Test LDAP configuration hierarchy through CLI
python -m target_ldap debug-config --debug
# This shows: ENVIRONMENT VARIABLES → .env FILE → DEFAULT CONSTANTS → CLI PARAMETERS resolution

# ✅ CORRECT - Test environment variable precedence over .env for LDAP
export LDAP_HOST=prod-ldap-server
export LDAP_PORT=636
python -m target_ldap debug-config --debug
# This shows environment variable takes precedence over .env file

# ✅ CORRECT - Test CLI parameters for LDAP-specific overrides
python -m target_ldap debug-config --debug --ldap-host cli-override-host --ldap-port 9999
# This shows CLI parameter overrides for specific execution
```

#### 2. LDAP Target Environment Validation Through CLI

```bash
# ✅ CORRECT - Complete LDAP target environment validation
python -m target_ldap validate-environment --debug --trace

# ✅ CORRECT - Specific LDAP component testing
python -m target_ldap test-ldap-connection --debug      # Test LDAP through flext-ldap
python -m target_ldap test-singer-compliance --debug    # Test Singer through flext-meltano
python -m target_ldap debug-config --debug              # Test configuration loading
```

#### 3. LDAP Target Problem Diagnosis Through CLI Debug

```bash
# ✅ CORRECT - Progressive LDAP target diagnosis through FLEXT CLI commands
# Step 1: Verify configuration loading
python -m target_ldap debug-config --debug

# Step 2: Test LDAP connectivity
python -m target_ldap test-ldap-connection --debug --trace

# Step 3: Test Singer protocol compliance
python -m target_ldap test-singer-compliance --debug

# Step 4: Full LDAP target environment validation
python -m target_ldap validate-environment --debug --trace
```

---

## 📈 CONTINUOUS IMPROVEMENT CYCLE - LDAP TARGET DOMAIN

### Daily Quality Gates

**MANDATORY EXECUTION**: Every development session must end with full validation

```bash
#!/bin/bash
# ldap_target_quality_gate_check.sh - Run this after every change session

set -e  # Exit on any error

echo "=== FLEXT TARGET LDAP QUALITY GATE VALIDATION ==="

echo "1. Ruff Check (Code Quality)..."
ruff check src/flext_target_ldap/ tests/ examples/ scripts/
echo "✅ Ruff passed"

echo "2. MyPy Check (Type Safety)..."
mypy src/flext_target_ldap/ --strict --no-error-summary
echo "✅ MyPy passed"

echo "3. Pyright Check (Advanced Type Safety)..."
pyright src/flext_target_ldap/ --level error
echo "✅ Pyright passed"

echo "4. Pytest Execution (Functional Tests)..."
pytest tests/ --cov=src/flext_target_ldap --cov-report=term-missing --cov-fail-under=75 -x
echo "✅ Pytest passed with 75%+ coverage"

echo "5. LDAP Integration Testing..."
pytest tests/integration/test_ldap_operations.py -v
echo "✅ LDAP integration tests passed"

echo "6. Singer Protocol Compliance..."
pytest tests/singer/ -v
echo "✅ Singer protocol compliance passed"

echo "7. Import Validation..."
python -c "import src.flext_target_ldap; print('✅ All imports work')"

echo "=== ALL LDAP TARGET QUALITY GATES PASSED ==="
```

### Success Metrics Tracking

**MEASURABLE TARGETS** (LDAP Target Specific):

```bash
# Track LDAP target progress with concrete numbers
echo "LDAP TARGET QUALITY METRICS TRACKING" > ldap_target_quality_metrics.log
echo "Date: $(date)" >> ldap_target_quality_metrics.log
echo "Ruff Issues: $(ruff check src/flext_target_ldap/ --output-format=github | wc -l)" >> ldap_target_quality_metrics.log
echo "MyPy Issues: $(mypy src/flext_target_ldap/ 2>&1 | grep -c error || echo 0)" >> ldap_target_quality_metrics.log
echo "Test Coverage: $(pytest --cov=src/flext_target_ldap --cov-report=term 2>/dev/null | grep TOTAL | awk '{print $4}')" >> ldap_target_quality_metrics.log
echo "Pytest Pass Rate: $(pytest --tb=no -q 2>&1 | grep -E '[0-9]+ passed' | awk '{print $1}')" >> ldap_target_quality_metrics.log
echo "LDAP Integration Tests: $(pytest tests/integration/test_ldap_operations.py --tb=no -q 2>&1 | grep -E '[0-9]+ passed' | awk '{print $1}')" >> ldap_target_quality_metrics.log
echo "Singer Compliance Tests: $(pytest tests/singer/ --tb=no -q 2>&1 | grep -E '[0-9]+ passed' | awk '{print $1}')" >> ldap_target_quality_metrics.log
```

**TARGET ACHIEVEMENTS** (Evidence-based, realistic goals):

- 🎯 **Ruff Issues**: From TBD to 0 (Systematic reduction by category)
- 🎯 **MyPy Issues**: Maintain 0 in src/ (Achieve and validate continuously)
- 🎯 **Pyright Issues**: From TBD to 0 (LDAP-specific type corrections)
- 🎯 **Test Coverage**: Achieve 75%+ (Match flext-core proven success at 79%)
- 🎯 **Pytest Pass Rate**: Achieve 100% pass rate for all test categories
- 🎯 **LDAP Integration**: 100% pass rate for real LDAP integration tests
- 🎯 **Singer Compliance**: 100% pass rate for Singer protocol compliance tests

---

## 🎖️ PROFESSIONAL EXCELLENCE STANDARDS - LDAP TARGET DOMAIN

### LDAP Target Documentation Standards

```python
class FlextLdapTargetService(FlextDomainService[FlextResult[LdapTargetResult]]):
    """Professional LDAP target service following SOLID principles and Singer protocol.

    This service handles Singer-to-LDAP data loading operations with comprehensive
    error handling, type safety, and integration with the flext-core foundation and
    flext-ldap infrastructure. It demonstrates proper separation of concerns,
    dependency injection patterns, and enterprise LDAP authentication.

    LDAP Domain Specialization:
    - Enterprise LDAP directory integration with connection pooling
    - Singer protocol implementation with stream-to-LDAP mapping
    - Comprehensive schema validation and constraint checking
    - Performance optimization with batch processing and caching

    Attributes:
        _container: Dependency injection container from flext-core
        _logger: Structured logger for operational observability
        _ldap_api: LDAP operations API from flext-ldap
        _singer_api: Singer protocol API from flext-meltano

    Example:
        >>> service = FlextLdapTargetService()
        >>> config = {"host": "ldap.company.com", "port": 389, "bind_dn": "cn=admin"}
        >>> messages = [{"type": "SCHEMA", "stream": "users"}, {"type": "RECORD", "stream": "users"}]
        >>> result = service.orchestrate_ldap_data_loading(messages, config)
        >>> assert result.is_success
        >>> data = result.unwrap()
    """

    def __init__(self) -> None:
        """Initialize LDAP target service with proper dependency injection."""
        super().__init__()
        self._container = get_flext_container()
        self._logger = get_logger(__name__)
        self._ldap_api = FlextLdapApi()
        self._singer_api = FlextSingerTarget()

    def orchestrate_ldap_data_loading(
        self,
        singer_messages: list[dict],
        ldap_config: dict
    ) -> FlextResult[LdapTargetResult]:
        """Orchestrate complete Singer-to-LDAP data loading pipeline with error handling.

        This method implements the railway pattern for error handling across the complete
        Singer protocol to LDAP directory loading pipeline. It ensures that failures are
        properly captured and propagated without raising exceptions, maintaining data
        integrity throughout the entire process.

        LDAP Pipeline Stages:
        1. Singer message validation and parsing
        2. LDAP connection establishment with authentication
        3. Schema message processing and LDAP object class mapping
        4. Record message transformation to LDAP entry format
        5. LDAP directory entry creation/modification operations
        6. Singer state management and checkpoint persistence

        Args:
            singer_messages: List of Singer protocol messages (SCHEMA, RECORD, STATE)
            ldap_config: LDAP connection and operation configuration

        Returns:
            FlextResult containing either successful LdapTargetResult or error message

        Example:
            >>> singer_messages = [
            ...     {"type": "SCHEMA", "stream": "users", "schema": {...}},
            ...     {"type": "RECORD", "stream": "users", "record": {"uid": "john", "cn": "John Doe"}},
            ...     {"type": "STATE", "value": {"bookmarks": {"users": {"version": 1}}}}
            ... ]
            >>> ldap_config = {"host": "ldap.company.com", "bind_dn": "cn=admin", "bind_password": "secret"}
            >>> result = service.orchestrate_ldap_data_loading(singer_messages, ldap_config)
            >>> if result.is_success:
            ...     loading_result = result.unwrap()
            ...     print(f"Loaded {loading_result.entries_processed} LDAP entries")
            ... else:
            ...     logger.error(f"LDAP loading failed: {result.error}")
        """
        return (
            self._validate_singer_messages(singer_messages)
            .flat_map(lambda msgs: self._establish_ldap_connection(ldap_config))
            .flat_map(lambda conn: self._process_schema_messages(msgs, conn))
            .flat_map(lambda schemas: self._transform_record_messages(msgs, schemas))
            .flat_map(lambda records: self._load_ldap_entries(records, conn))
            .flat_map(lambda results: self._update_singer_state(results))
            .map(lambda state: self._create_loading_result(state))
            .map_error(lambda e: f"LDAP data loading pipeline failed: {e}")
        )
```

### Error Handling Excellence (ZERO FALLBACK TOLERANCE) - LDAP TARGET DOMAIN

```python
# ✅ PROFESSIONAL - Proper LDAP error handling WITHOUT try/except fallbacks
def robust_ldap_operation(
    ldap_config: LdapConnectionConfig,
    ldap_entry: LdapEntry
) -> FlextResult[LdapOperationResult]:
    """Robust LDAP operation with proper error boundary handling - NO FALLBACKS.

    This demonstrates the correct approach for LDAP operations: validate inputs,
    handle LDAP-specific errors explicitly, and return meaningful error messages.
    NO try/except blocks used as fallback mechanisms.
    """

    # Step 1: Comprehensive LDAP configuration validation - fail fast and clearly
    if ldap_config.host is None:
        return FlextResult[LdapOperationResult].fail("LDAP host cannot be None")

    if not isinstance(ldap_config, LdapConnectionConfig):
        return FlextResult[LdapOperationResult].fail(f"Expected LdapConnectionConfig, got {type(ldap_config)}")

    # Step 2: LDAP business rule validation - explicit error checking
    config_validation_result = ldap_config.validate_business_rules()
    if config_validation_result.is_failure:
        return FlextResult[LdapOperationResult].fail(f"LDAP config validation failed: {config_validation_result.error}")

    # Step 3: LDAP connection establishment - check result, no exception catching
    connection_result = establish_ldap_connection(ldap_config)
    if connection_result.is_failure:
        return FlextResult[LdapOperationResult].fail(f"LDAP connection failed: {connection_result.error}")

    # Step 4: LDAP entry validation - explicit success/failure handling
    entry_validation_result = validate_ldap_entry(ldap_entry)
    if entry_validation_result.is_failure:
        return FlextResult[LdapOperationResult].fail(f"LDAP entry validation failed: {entry_validation_result.error}")

    # Step 5: LDAP operation execution - explicit error handling
    operation_result = execute_ldap_add_operation(connection_result.unwrap(), entry_validation_result.unwrap())
    if operation_result.is_failure:
        return FlextResult[LdapOperationResult].fail(f"LDAP add operation failed: {operation_result.error}")

    return FlextResult[LdapOperationResult].ok(operation_result.unwrap())

# ❌ FORBIDDEN - Try/except as fallback mechanism for LDAP operations
def bad_ldap_operation_with_fallbacks(ldap_config: dict, ldap_entry: dict) -> dict:
    """THIS IS ABSOLUTELY FORBIDDEN - demonstrates what NOT to do for LDAP operations."""
    try:
        # Some LDAP operation that might fail
        result = risky_ldap_operation(ldap_config, ldap_entry)
        return result
    except LDAPException:
        # FORBIDDEN: Silent fallback that masks real LDAP problems
        return {"status": "success", "entries": []}  # This hides the real LDAP issue!

    try:
        # FORBIDDEN: Multiple LDAP fallback attempts
        return alternative_ldap_operation(ldap_config, ldap_entry)
    except Exception:
        # FORBIDDEN: Final fallback that gives false success for LDAP
        return {"status": "partial_success", "entries": []}  # User thinks LDAP worked!

# ✅ CORRECT - Explicit LDAP error handling without fallbacks
def correct_ldap_operation(
    ldap_config: LdapConnectionConfig,
    ldap_entry: LdapEntry
) -> FlextResult[LdapOperationResult]:
    """Correct approach - explicit LDAP error handling, no hidden fallbacks."""

    # Attempt primary LDAP operation
    primary_result = execute_primary_ldap_operation(ldap_config, ldap_entry)
    if primary_result.is_failure:
        # Log the specific LDAP failure, don't hide it
        logger.error(f"Primary LDAP operation failed: {primary_result.error}")
        return FlextResult[LdapOperationResult].fail(f"LDAP operation failed: {primary_result.error}")

    # If LDAP operation succeeded, validate the result
    validation_result = validate_ldap_operation_result(primary_result.unwrap())
    if validation_result.is_failure:
        return FlextResult[LdapOperationResult].fail(f"LDAP result validation failed: {validation_result.error}")

    return FlextResult[LdapOperationResult].ok(validation_result.unwrap())

# ✅ CORRECT - LDAP service unavailability handling without fallbacks
def ldap_directory_operation(query: str, ldap_config: LdapConnectionConfig) -> FlextResult[LdapQueryResult]:
    """LDAP directory operation with proper error handling - no silent fallbacks."""

    # Get LDAP service from container
    container = FlextContainer.get_global()
    ldap_service_result = container.get("ldap_service")

    # If LDAP service unavailable, FAIL EXPLICITLY - don't hide the problem
    if ldap_service_result.is_failure:
        return FlextResult[LdapQueryResult].fail("LDAP service is unavailable - system configuration error")

    ldap_service = ldap_service_result.unwrap()

    # Execute LDAP query and handle results explicitly
    query_result = ldap_service.execute_ldap_query(query, ldap_config)
    if query_result.is_failure:
        # Return specific LDAP error, don't try alternative approaches silently
        return FlextResult[LdapQueryResult].fail(f"LDAP query execution failed: {query_result.error}")

    return FlextResult[LdapQueryResult].ok(query_result.unwrap())
```

---

## ⚡ EXECUTION CHECKLIST - LDAP TARGET DOMAIN

### Before Starting object Work

- [ ] Read all documentation: `CLAUDE.md`, `FLEXT_REFACTORING_PROMPT.md`, project `README.md`
- [ ] Verify virtual environment: `../.venv/bin/python` (VERIFIED WORKING)
- [ ] Run baseline quality assessment using exact commands provided
- [ ] Plan incremental improvements (never wholesale rewrites)
- [ ] Establish measurable success criteria from current baseline
- [ ] Set up LDAP test environment (Docker compose with OpenLDAP)
- [ ] Verify Singer protocol compliance test data

### During Each Development Cycle

- [ ] Make minimal, focused changes (single aspect per change)
- [ ] Validate after every modification using quality gates
- [ ] Test actual functionality (minimal mocks, real LDAP execution)
- [ ] Document changes with professional English
- [ ] Update tests to maintain coverage near 75%+
- [ ] Verify LDAP integration tests pass
- [ ] Confirm Singer protocol compliance

### After Each Development Session

- [ ] Full quality gate validation (ruff + mypy + pyright + pytest)
- [ ] LDAP integration testing with real LDAP server
- [ ] Singer protocol compliance validation
- [ ] Coverage measurement and improvement tracking
- [ ] Integration testing with flext-core dependencies
- [ ] Update documentation reflecting current reality
- [ ] Commit with descriptive messages explaining improvements

### Project Completion Criteria

- [ ] **Code Quality**: Zero ruff violations across all code
- [ ] **Type Safety**: Zero mypy/pyright errors in src/
- [ ] **Test Coverage**: 75%+ with real functional tests
- [ ] **LDAP Integration**: 100% pass rate for LDAP integration tests
- [ ] **Singer Compliance**: 100% pass rate for Singer protocol compliance
- [ ] **Documentation**: Professional English throughout
- [ ] **Architecture**: Clean SOLID principles implementation
- [ ] **Integration**: Seamless flext-core foundation usage
- [ ] **Maintainability**: Clear, readable, well-structured code

---

## 🏁 FINAL SUCCESS VALIDATION - LDAP TARGET DOMAIN

```bash
#!/bin/bash
# ldap_target_final_validation.sh - Complete LDAP target validation

echo "=== FLEXT TARGET LDAP FINAL VALIDATION ==="

# Quality Gates
ruff check src/flext_target_ldap/ --statistics
mypy src/flext_target_ldap/ --strict --show-error-codes
pyright src/flext_target_ldap/ --stats
pytest tests/ --cov=src/flext_target_ldap --cov-report=term-missing --cov-fail-under=75

# LDAP-Specific Validation
echo "Testing LDAP integration..."
pytest tests/integration/test_ldap_operations.py -v

echo "Testing Singer protocol compliance..."
pytest tests/singer/ -v

# Functional Validation
python -c "
import sys
sys.path.insert(0, 'src')

try:
    # Test flext-core integration
    from flext_core import FlextResult, get_flext_container, FlextModels
    print('✅ flext-core integration: SUCCESS')

    # Test flext-ldap integration
    from flext_ldap import FlextLdapApi, FlextLdapConnection
    print('✅ flext-ldap integration: SUCCESS')

    # Test flext-meltano integration
    from flext_meltano import FlextSingerTarget
    print('✅ flext-meltano integration: SUCCESS')

    # Test LDAP target functionality
    from flext_target_ldap import UnifiedFlextLdapTargetService
    print('✅ LDAP target import: SUCCESS')

    # Test CLI functionality
    from flext_target_ldap.cli import LdapTargetCliService
    print('✅ LDAP target CLI: SUCCESS')

    print('✅ All imports: SUCCESS')
    print('✅ FINAL VALIDATION: PASSED')

except Exception as e:
    print(f'❌ VALIDATION FAILED: {e}')
    sys.exit(1)
"

echo "=== LDAP TARGET READY FOR PRODUCTION ==="
```

---

**The path to excellence is clear: Follow these standards precisely for LDAP target domain, validate continuously with real LDAP integration testing, never compromise on Singer protocol compliance, and ALWAYS use FLEXT ecosystem for CLI testing and debugging with correct configuration priority (ENV → .env → DEFAULT → CLI) and automatic .env detection from current execution directory.**

**LDAP TARGET SPECIALIZATION**: Enterprise LDAP directory operations, Singer protocol compliance, connection pooling optimization, comprehensive authentication patterns, schema validation, and production-ready error handling deliver industry-leading LDAP data loading capabilities.
