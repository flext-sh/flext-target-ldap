# internal.invalid.md - TARGET-LDAP PROJECT SPECIFICS

**Hierarquia**: **PROJECT-SPECIFIC**  
**Projeto**: Target LDAP - Enterprise Directory Data Loading  
**Status**: PRODUCTION READY - Active directory synchronization  
**Framework**: Singer Protocol + LDAP v3 + Directory Synchronization  
**Última Atualização**: 2025-06-26

**Referência Global**: `/home/marlonsc/CLAUDE.md` → Universal principles  
**Referência Workspace**: `../CLAUDE.md` → PyAuto workspace patterns  
**Referência Cross-Workspace**: `/home/marlonsc/internal.invalid.md` → Cross-workspace issues

---

## 🎯 PROJECT-SPECIFIC CONFIGURATION

### Virtual Environment Usage

```bash
# MANDATORY: Use workspace venv
source /home/marlonsc/pyauto/.venv/bin/activate
# NOT project-specific venv
```

### Agent Coordination

```bash
# Read workspace coordination first
cat /home/marlonsc/pyauto/.token | tail -5
# Use project .token only for project-specific coordination
```

### Project-Specific Environment Variables

```bash
# Target LDAP specific configurations
export TARGET_LDAP_HOST=ldap-target.company.com
export TARGET_LDAP_PORT=636
export TARGET_LDAP_BIND_DN="cn=REDACTED_LDAP_BIND_PASSWORD,dc=company,dc=com"
export TARGET_LDAP_PASSWORD=secure_REDACTED_LDAP_BIND_PASSWORD_password
export TARGET_LDAP_BASE_DN="dc=company,dc=com"
export TARGET_LDAP_USE_SSL=true
export TARGET_LDAP_LOG_LEVEL=DEBUG
export TARGET_LDAP_BATCH_SIZE=100
export TARGET_LDAP_TIMEOUT=30
export TARGET_LDAP_VALIDATION_MODE=strict
```

---

## 🏗️ TARGET LDAP ARCHITECTURE

### **Purpose & Role**

- **Singer Protocol Target**: Standardized data loading to LDAP directories
- **Directory Synchronization**: Real-time sync between directory systems
- **Identity Data Sink**: Final destination for identity analytics pipelines
- **Round-Trip Integration**: Complete data flow with tap-ldap for full sync
- **Schema Transformation**: Data mapping between different directory schemas

### **Core Singer Components**

```python
# Singer protocol target implementation
src/target_ldap/
├── target.py            # Main Singer target implementation
├── client.py            # LDAP connection and operations
├── sinks.py             # Stream sinks (users, groups, OUs)
├── transformation.py    # Data transformation and mapping
└── __init__.py          # Package exports
```

### **Production Data Sinks**

- **Users Sink**: Load user data to directory (inetOrgPerson, user objects)
- **Groups Sink**: Load group data and membership (groupOfNames, group objects)
- **Organizational Units**: Create and maintain OU hierarchy
- **Schema Sink**: Apply schema changes and attribute definitions
- **Custom Sinks**: Configurable LDAP object creation

---

## 🔧 PROJECT-SPECIFIC TECHNICAL DETAILS

### **Development Commands**

```bash
# MANDATORY: Always from workspace venv
source /home/marlonsc/pyauto/.venv/bin/activate

# Singer protocol development
make install-dev       # Install development dependencies
make test              # Run complete test suite
make test-unit         # Unit tests only
make test-integration  # Integration tests with mock LDAP
make test-e2e          # End-to-end tests with Docker LDAP
make lint              # Code quality checks
make format            # Code formatting

# Singer target operations
target-ldap --config config.json < users.jsonl
target-ldap --config config.json --test-connection
```

### **LDAP Target Testing**

```bash
# Test LDAP target connectivity
target-ldap --config config.json --test

# Test with debug logging
export TARGET_LDAP_LOG_LEVEL=DEBUG
target-ldap --config config.json < sample_data.jsonl

# Test schema validation
target-ldap --config config.json --validate-schema < users_schema.jsonl
```

### **Meltano Integration**

```bash
# Add to Meltano project
meltano add loader target-ldap

# Run via Meltano
meltano elt tap-postgres target-ldap --job_id=directory_sync
meltano elt tap-ldap target-ldap --job_id=ldap_round_trip

# Configuration validation
meltano invoke target-ldap --test
```

---

## 🚨 PROJECT-SPECIFIC KNOWN ISSUES

### **LDAP Target Challenges**

- **Write Performance**: LDAP write operations are typically slower than reads
- **Schema Constraints**: Target directory schema must accommodate source data
- **Referential Integrity**: Group memberships require users to exist first
- **Concurrent Writes**: Multiple writers may cause conflicts
- **Transaction Support**: Limited transaction support in LDAP operations

### **Singer Protocol Considerations**

```python
# LDAP-specific Singer target patterns
class LDAPTargetPatterns:
    """Production patterns for LDAP Singer target."""

    def handle_dependency_ordering(self):
        """Handle object creation order for referential integrity."""
        # Create objects in dependency order
        creation_order = [
            "organizational_units",  # Create OUs first
            "users",                # Create users second
            "groups",               # Create groups last (reference users)
        ]

        for object_type in creation_order:
            if object_type in self.pending_objects:
                self.create_objects(self.pending_objects[object_type])

    def handle_schema_mapping(self, singer_record: dict):
        """Map Singer record to LDAP attributes."""
        # Handle different directory schemas
        if self.target_schema == "active_directory":
            return self.map_to_ad_schema(singer_record)
        elif self.target_schema == "openldap":
            return self.map_to_openldap_schema(singer_record)
        else:
            return self.map_to_generic_schema(singer_record)
```

### **Production Error Handling**

```bash
# Common LDAP target issues
1. Object Already Exists: Handle duplicate entries gracefully
2. Schema Violations: Validate data before LDAP operations
3. Permission Denied: Verify bind DN has write permissions
4. Referential Integrity: Create dependencies before references
5. Connection Timeouts: Implement retry logic for write operations
```

---

## 🎯 PROJECT-SPECIFIC SUCCESS METRICS

### **Singer Protocol Compliance**

- **Data Loading**: 100% successful loading of valid Singer records
- **Schema Adherence**: Complete compliance with target LDAP schema
- **Error Handling**: Graceful handling of invalid or duplicate data
- **Performance**: >100 objects/second write throughput
- **Consistency**: Atomic operations maintaining directory integrity

### **Directory Synchronization Goals**

- **Write Success Rate**: 99%+ successful LDAP write operations
- **Data Integrity**: 100% referential integrity maintenance
- **Sync Latency**: <5 minutes from source change to target update
- **Conflict Resolution**: Automatic handling of concurrent write conflicts
- **Recovery**: Complete rollback capability for failed transactions

---

## 🔗 PROJECT-SPECIFIC INTEGRATIONS

### **Singer Ecosystem Integration**

- **Source Compatibility**: Works with all Singer-compliant taps
- **Meltano Plugin**: Official Meltano Hub target plugin
- **Schema Validation**: Automatic schema compatibility checking
- **State Management**: Incremental loading support

### **PyAuto Ecosystem Integration**

- **tap-ldap**: Perfect round-trip integration for directory sync
- **ldap-core-shared**: Shared LDAP models and schema definitions
- **flx-ldap**: Advanced LDAP transformation capabilities
- **client-a-oud-mig**: Target for Oracle Directory migration

### **Enterprise Directory Integration**

```python
# Production LDAP target configuration
class ProductionLDAPTarget:
    """Production LDAP target for enterprise directories."""

    # Active Directory target configuration
    AD_TARGET_CONFIG = {
        "host": "dc-target.company.com",
        "port": 636,
        "use_ssl": True,
        "bind_dn": "CN=svc-target-ldap,OU=Service Accounts,DC=company,DC=com",
        "base_dn": "DC=company,DC=com",
        "schema_type": "active_directory",
        "batch_size": 50,
        "timeout": 30,
        "validation_mode": "strict",
    }

    # OpenLDAP target configuration
    OPENLDAP_TARGET_CONFIG = {
        "host": "ldap-target.company.com",
        "port": 636,
        "use_ssl": True,
        "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=company,dc=com",
        "base_dn": "dc=company,dc=com",
        "schema_type": "openldap",
        "batch_size": 100,
        "timeout": 30,
        "validation_mode": "permissive",
    }
```

---

## 📊 PROJECT-SPECIFIC MONITORING

### **Singer Target Metrics**

```python
# Key metrics for Singer target monitoring
TARGET_LDAP_METRICS = {
    "write_throughput": "Objects written per second",
    "error_rate": "Percentage of failed write operations",
    "schema_validation_rate": "Percentage of records passing validation",
    "dependency_resolution_time": "Time to resolve object dependencies",
    "connection_success_rate": "LDAP connection reliability",
    "referential_integrity_score": "Percentage of valid references",
}
```

### **Directory Write Health Checks**

```bash
# Production monitoring commands
target-ldap --config config.json --test                    # Connection test
target-ldap --config config.json --validate-schema         # Schema validation
target-ldap --config config.json --dry-run < test_data.jsonl  # Dry run test
```

---

## 📋 PROJECT-SPECIFIC MAINTENANCE

### **Regular Maintenance Tasks**

- **Daily**: Monitor write throughput and error rates
- **Weekly**: Validate referential integrity and schema compliance
- **Monthly**: Update target directory service account passwords
- **Quarterly**: Review and optimize write performance patterns

### **Singer Protocol Updates**

```bash
# Keep Singer SDK updated
pip install --upgrade singer-sdk

# Validate Singer target compliance
singer-check-target --target target-ldap --config config.json
singer-check-schema --schema target_users.json
```

### **Emergency Procedures**

```bash
# LDAP target emergency troubleshooting
1. Test LDAP write access: ldapmodify -H $LDAP_URI -D "$BIND_DN" -w "$PASSWORD" -f test_modify.ldif
2. Check schema compatibility: target-ldap --config config.json --validate-schema
3. Verify referential integrity: python scripts/check_ldap_integrity.py
4. Clear failed operations: target-ldap --config config.json --clear-failed-operations
```

---

**PROJECT SUMMARY**: Singer protocol target para carregamento de dados de identidade em diretórios LDAP/Active Directory com validação de schema, integridade referencial e sincronização em tempo real.

**CRITICAL SUCCESS FACTOR**: Manter integridade total dos dados durante operações de escrita LDAP, garantindo consistência e performance para sincronização de diretórios empresariais.

---

_Última Atualização: 2025-06-26_  
_Próxima Revisão: Semanal durante sincronizações ativas_  
_Status: PRODUCTION READY - Sincronização ativa entre diretórios empresariais_
