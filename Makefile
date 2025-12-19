# flext-target-ldap - LDAP Singer Target
PROJECT_NAME := flext-target-ldap
COV_DIR := flext_target_ldap
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: target-run test-unit test-integration build shell

target-run: ## Run target with config
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run target-ldap --config config.json

.DEFAULT_GOAL := help
