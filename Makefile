# FLEXT-TARGET-LDAP Makefile
# Migrated to use base.mk - 2026-01-03

PROJECT_NAME := flext-target-ldap
# Include shared base.mk for standard targets
ifneq ("$(wildcard ../base.mk)", "")
include ../base.mk
else
include base.mk
endif

# =============================================================================
# SINGER TARGET CONFIGURATION
# =============================================================================

TARGET_CONFIG ?= config.json
TARGET_STATE ?= state.json

# =============================================================================
# SINGER TARGET OPERATIONS
# =============================================================================

.PHONY: load validate-target-config test-target dry-run test-singer

load: ## Run target data loading
	$(POETRY) run target-ldap --config $(TARGET_CONFIG) --state $(TARGET_STATE)

validate-target-config: ## Validate target configuration
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "import json; json.load(open('$(TARGET_CONFIG)'))"

test-target: ## Test target functionality
	$(POETRY) run target-ldap --about
	$(POETRY) run target-ldap --version

dry-run: ## Run target in dry-run mode
	$(POETRY) run target-ldap --config $(TARGET_CONFIG) --dry-run

# =============================================================================
# LDAP-SPECIFIC TARGETS
# =============================================================================

.PHONY: ldap-connect ldap-schema ldap-write-test

ldap-connect: ## Test LDAP connection
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_target_ldap.client import test_connection; test_connection()"

ldap-schema: ## Validate LDAP schema
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_target_ldap.schema import validate_schema; validate_schema()"

ldap-write-test: ## Test LDAP write operations
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_target_ldap.operations import test_write; test_write()"

# =============================================================================
# PROJECT-SPECIFIC TEST TARGETS
# =============================================================================

test-singer: ## Run Singer protocol tests
	$(POETRY) run pytest $(TESTS_DIR) -m singer -v
