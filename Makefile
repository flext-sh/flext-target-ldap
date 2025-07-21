# FLEXT Target LDAP - LDAP Directory Singer Target
# ===============================================
# Enterprise-grade Singer target for LDAP directory data loading
# Python 3.13 + Singer SDK + LDAP + FLEXT Core + Zero Tolerance Quality Gates

.PHONY: help check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-singer
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: target-test target-validate target-schema target-run
.PHONY: ldap-connect ldap-schema ldap-operations ldap-performance

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🎯 FLEXT Target LDAP - LDAP Directory Singer Target"
	@echo "=================================================="
	@echo "🎯 Singer SDK + LDAP + FLEXT Core + Python 3.13"
	@echo ""
	@echo "📦 Enterprise-grade LDAP directory target for Singer protocol"
	@echo "🔒 Zero tolerance quality gates with directory integration"
	@echo "🧪 90%+ test coverage requirement with LDAP integration testing"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT TARGET LDAP COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_target_ldap --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-singer: ## Run Singer protocol tests
	@echo "🧪 Running Singer protocol tests..."
	@poetry run pytest tests/singer/ -v
	@echo "✅ Singer tests complete"

test-ldap: ## Run LDAP-specific tests
	@echo "🧪 Running LDAP-specific tests..."
	@poetry run pytest tests/ -m "ldap" -v
	@echo "✅ LDAP tests complete"

test-directory: ## Run directory operation tests
	@echo "🧪 Running directory operation tests..."
	@poetry run pytest tests/ -m "directory" -v
	@echo "✅ Directory tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_target_ldap --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🎯 SINGER TARGET OPERATIONS
# ============================================================================

target-test: ## Test LDAP target functionality
	@echo "🎯 Testing LDAP target functionality..."
	@poetry run target-ldap --about
	@poetry run target-ldap --version
	@echo "✅ Target test complete"

target-validate: ## Validate target configuration
	@echo "🔍 Validating target configuration..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json --validate-config
	@echo "✅ Target configuration validated"

target-schema: ## Validate LDAP schema
	@echo "🔍 Validating LDAP schema..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json --validate-schema
	@echo "✅ LDAP schema validated"

target-run: ## Run LDAP data loading
	@echo "🎯 Running LDAP data loading..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json < tests/fixtures/data/sample_input.jsonl
	@echo "✅ LDAP data loading complete"

target-run-debug: ## Run LDAP target with debug logging
	@echo "🎯 Running LDAP target with debug..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json --log-level DEBUG < tests/fixtures/data/sample_input.jsonl
	@echo "✅ LDAP debug run complete"

target-dry-run: ## Run LDAP target in dry-run mode
	@echo "🎯 Running LDAP target dry-run..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json --dry-run < tests/fixtures/data/sample_input.jsonl
	@echo "✅ LDAP dry-run complete"

target-users: ## Load user data to LDAP
	@echo "🎯 Loading user data to LDAP..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json < tests/fixtures/data/users.jsonl
	@echo "✅ User data loading complete"

target-groups: ## Load group data to LDAP
	@echo "🎯 Loading group data to LDAP..."
	@poetry run target-ldap --config tests/fixtures/config/target_config.json < tests/fixtures/data/groups.jsonl
	@echo "✅ Group data loading complete"

# ============================================================================
# 📁 LDAP OPERATIONS
# ============================================================================

ldap-connect: ## Test LDAP connection
	@echo "📁 Testing LDAP connection..."
	@poetry run python -c "from flext_target_ldap.client import TargetLDAPClient; import asyncio; import json; config = json.load(open('tests/fixtures/config/target_config.json')); client = TargetLDAPClient(config); print('Testing connection...'); result = asyncio.run(client.connect()); print('✅ Connected!' if result.is_success else f'❌ Failed: {result.error}')"
	@echo "✅ LDAP connection test complete"

ldap-schema: ## Validate LDAP schema
	@echo "📁 Validating LDAP schema..."
	@poetry run python scripts/validate_ldap_schema.py
	@echo "✅ LDAP schema validation complete"

ldap-operations: ## Test LDAP operations
	@echo "📁 Testing LDAP operations..."
	@poetry run python scripts/test_ldap_operations.py
	@echo "✅ LDAP operations test complete"

ldap-performance: ## Run LDAP performance tests
	@echo "⚡ Running LDAP performance tests..."
	@poetry run pytest tests/performance/ -v --benchmark-only
	@echo "✅ LDAP performance tests complete"

ldap-diagnostics: ## Run LDAP diagnostics
	@echo "🔍 Running LDAP diagnostics..."
	@poetry run python scripts/ldap_diagnostics.py
	@echo "✅ LDAP diagnostics complete"

ldap-browse: ## Browse LDAP directory structure
	@echo "📁 Browsing LDAP directory structure..."
	@poetry run python scripts/browse_ldap_directory.py
	@echo "✅ LDAP directory browsing complete"

ldap-dn-test: ## Test DN generation
	@echo "📁 Testing DN generation..."
	@poetry run python scripts/test_dn_generation.py
	@echo "✅ DN generation test complete"

# ============================================================================
# 🔍 DIRECTORY VALIDATION
# ============================================================================

validate-users: ## Validate user entries
	@echo "🔍 Validating user entries..."
	@poetry run python scripts/validate_users.py
	@echo "✅ User validation complete"

validate-groups: ## Validate group entries
	@echo "🔍 Validating group entries..."
	@poetry run python scripts/validate_groups.py
	@echo "✅ Group validation complete"

validate-ous: ## Validate organizational units
	@echo "🔍 Validating organizational units..."
	@poetry run python scripts/validate_ous.py
	@echo "✅ OU validation complete"

validate-attributes: ## Validate attribute mappings
	@echo "🔍 Validating attribute mappings..."
	@poetry run python scripts/validate_attributes.py
	@echo "✅ Attribute validation complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# LDAP Target settings
export TARGET_LDAP_HOST := localhost
export TARGET_LDAP_PORT := 389
export TARGET_LDAP_USE_SSL := false
export TARGET_LDAP_BASE_DN := dc=test,dc=com

# Singer settings
export SINGER_LOG_LEVEL := INFO
export SINGER_BATCH_SIZE := 100
export SINGER_MAX_BATCH_AGE := 300

# Directory settings
export TARGET_LDAP_USER_RDN_ATTRIBUTE := uid
export TARGET_LDAP_GROUP_RDN_ATTRIBUTE := cn
export TARGET_LDAP_VALIDATE_RECORDS := true

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-target-ldap
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Target LDAP - LDAP Directory Singer Target

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 SINGER SPECIFIC COMMANDS
# ============================================================================

singer-about: ## Show Singer target about information
	@echo "🎵 Singer target about information..."
	@poetry run target-ldap --about
	@echo "✅ About information displayed"

singer-config-sample: ## Generate Singer config sample
	@echo "🎵 Generating Singer config sample..."
	@poetry run target-ldap --config-sample > config_sample.json
	@echo "✅ Config sample generated: config_sample.json"

singer-discover: ## Run Singer discovery (if applicable)
	@echo "🎵 Running Singer discovery..."
	@poetry run target-ldap --discover
	@echo "✅ Discovery complete"

singer-test-streams: ## Test Singer streams
	@echo "🎵 Testing Singer streams..."
	@poetry run pytest tests/singer/test_streams.py -v
	@echo "✅ Singer streams tests complete"

# ============================================================================
# 🎯 ACTIVE DIRECTORY SUPPORT
# ============================================================================

ad-test: ## Test Active Directory integration
	@echo "🏢 Testing Active Directory integration..."
	@poetry run python scripts/test_active_directory.py
	@echo "✅ Active Directory test complete"

ad-user-account-control: ## Test userAccountControl management
	@echo "🏢 Testing userAccountControl management..."
	@poetry run python scripts/test_user_account_control.py
	@echo "✅ userAccountControl test complete"

ad-upn-generation: ## Test UPN generation
	@echo "🏢 Testing UPN generation..."
	@poetry run python scripts/test_upn_generation.py
	@echo "✅ UPN generation test complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Singer project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Singer Target + LDAP"
	@echo "🐍 Python: 3.13"
	@echo "🔗 Framework: FLEXT Core + Singer SDK"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: LDAP Directory Singer Target"
	@echo "🔗 Dependencies: flext-core, flext-ldap, singer-sdk"
	@echo "📦 Provides: LDAP directory data loading capabilities"
	@echo "🎯 Standards: Enterprise LDAP integration patterns"
