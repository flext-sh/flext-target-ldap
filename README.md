# 📥 Target LDAP - Enterprise Directory Data Loading & Synchronization

> **Function**: Production-grade Singer target for LDAP/Active Directory data loading with schema validation | **Audience**: Directory Engineers, Identity Management Teams | **Status**: Production Ready

[![Singer](https://img.shields.io/badge/singer-target-blue.svg)](https://www.singer.io/)
[![LDAP](https://img.shields.io/badge/ldap-v3-green.svg)](https://ldap.com/)
[![Meltano](https://img.shields.io/badge/meltano-compatible-green.svg)](https://meltano.com/)
[![Python](https://img.shields.io/badge/python-3.9%2B-orange.svg)](https://www.python.org/)

## 📋 **Overview**

Enterprise Singer target for loading identity data into LDAP directories with automatic schema validation, DN generation, and multi-valued attribute handling

---

## 🧭 **Navigation Context**

**🏠 Root**: [PyAuto Home](../README.md) → **📂 Current**: Target LDAP

---

## 🎯 **Core Purpose**

This Singer target provides enterprise-grade data loading capabilities for LDAP directories including Active Directory, OpenLDAP, and Oracle Directory Server. It handles complex identity synchronization scenarios with automatic DN generation, schema validation, and comprehensive error handling.

### **Key Capabilities**

- **Intelligent DN Generation**: Template-based DN construction
- **Schema Validation**: Pre-flight checks against LDAP schema
- **Multi-valued Attributes**: Proper handling of groups, emails, etc.
- **Upsert Operations**: Create or update based on existence
- **Soft Deletes**: Mark entries as deleted with metadata

### **Production Features**

- **Transaction Safety**: Atomic operations with rollback
- **Connection Pooling**: Efficient connection management
- **Error Recovery**: Automatic retry with exponential backoff
- **Audit Trail**: Complete operation logging

---

## 🚀 **Quick Start**

### **Installation**

```bash
# Install via pip (recommended for production)
pip install target-ldap

# Install via Meltano
meltano add loader target-ldap

# Install from source
git clone https://github.com/datacosmos-br/target-ldap
cd target-ldap
poetry install
```

### **Basic Configuration**

```json
{
  "host": "ldap.company.com",
  "port": 389,
  "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=company,dc=com",
  "password": "secure_password",
  "base_dn": "dc=company,dc=com",
  "use_ssl": false,
  "timeout": 30,
  "validate_records": true,
  "user_rdn_attribute": "uid",
  "group_rdn_attribute": "cn"
}
```

### **Running the Target**

```bash
# Basic usage with tap
tap-csv --config tap_config.json | \
  target-ldap --config target_config.json

# From file
cat users.jsonl | target-ldap --config config.json

# With state management
tap-ldap --config tap_config.json --state state.json | \
  target-ldap --config target_config.json | \
  tail -1 > state.json
```

---

## 🏗️ **Architecture**

### **Data Processing Pipeline**

```
┌─────────────────────────────────────────┐
│         Singer Tap (Any)                │
│        (Data Source)                    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Singer Protocol                  │
│      (JSON Lines Input)                 │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Target LDAP                     │
│    (Directory Synchronizer)             │
├─────────────────────────────────────────┤
│ • DN Generator                          │
│ • Schema Validator                      │
│ • Attribute Mapper                      │
│ • Operation Executor                    │
│ • Error Handler                         │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Stream-Specific Sinks              │
├─────────────────────────────────────────┤
│ • UserSink                              │
│ • GroupSink                             │
│ • OrganizationalUnitSink                │
│ • GenericLDAPSink                       │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         LDAP Directory                  │
│    (Active Directory, OpenLDAP)         │
└─────────────────────────────────────────┘
```

### **Component Structure**

```
target-ldap/
├── src/target_ldap/
│   ├── __init__.py          # Package initialization
│   ├── target.py            # Main target class
│   ├── client.py            # LDAP client wrapper
│   ├── sinks/               # Specialized sinks
│   │   ├── base.py          # Base LDAP sink
│   │   ├── user.py          # User operations
│   │   ├── group.py         # Group operations
│   │   └── ou.py            # OU operations
│   ├── transformation.py    # Data transformation
│   ├── validation.py        # Schema validation
│   └── utils/               # Utilities
│       ├── dn.py           # DN manipulation
│       └── attributes.py    # Attribute handling
├── tests/                   # Test suite
├── examples/                # Usage examples
└── meltano.yml             # Meltano config
```

---

## 🔧 **Core Features**

### **1. DN Template System**

Flexible DN generation with templates:

```json
{
  "dn_templates": {
    "users": "uid={uid},ou=users,dc=company,dc=com",
    "groups": "cn={cn},ou=groups,dc=company,dc=com",
    "service_accounts": "uid={uid},ou=services,dc=company,dc=com",
    "computers": "cn={name},ou=computers,dc=company,dc=com"
  }
}
```

### **2. Object Class Management**

Automatic object class assignment:

```json
{
  "default_object_classes": {
    "users": ["inetOrgPerson", "organizationalPerson", "person", "top"],
    "groups": ["groupOfNames", "top"],
    "service_accounts": ["account", "simpleSecurityObject", "top"],
    "organizational_units": ["organizationalUnit", "top"]
  }
}
```

### **3. Attribute Mapping**

Transform incoming data to LDAP attributes:

```json
{
  "attribute_mappings": {
    "users": {
      "email": "mail",
      "phone": "telephoneNumber",
      "mobile": "mobile",
      "employee_id": "employeeNumber",
      "department": "departmentNumber",
      "manager_dn": "manager"
    }
  }
}
```

### **4. Multi-valued Attribute Handling**

Proper handling of array attributes:

```python
# Automatically handles multi-valued attributes
{
  "record": {
    "uid": "jdoe",
    "mail": ["john.doe@company.com", "jdoe@company.com"],
    "memberOf": [
      "cn=developers,ou=groups,dc=company,dc=com",
      "cn=employees,ou=groups,dc=company,dc=com"
    ]
  }
}
```

### **5. Operation Types**

#### **Upsert (Default)**

```json
{
  "type": "RECORD",
  "stream": "users",
  "record": {
    "uid": "jdoe",
    "cn": "John Doe",
    "mail": "john.doe@company.com"
  }
}
```

#### **Delete**

```json
{
  "type": "RECORD",
  "stream": "users",
  "record": {
    "dn": "uid=jdoe,ou=users,dc=company,dc=com",
    "_sdc_deleted_at": "2024-06-19T10:30:00Z"
  }
}
```

---

## 📊 **Advanced Features**

### **Schema Validation**

Pre-flight validation against LDAP schema:

```python
# Automatic schema validation
{
  "validate_schema": true,
  "schema_strict_mode": false,  # Allow extra attributes
  "validate_objectclasses": true,
  "validate_attributes": true
}
```

### **Referential Integrity**

Maintain relationships between entries:

```json
{
  "referential_integrity": {
    "validate_member_dns": true,
    "validate_manager_dns": true,
    "create_missing_groups": false,
    "update_group_membership": true
  }
}
```

### **Bulk Operations**

Efficient batch processing:

```json
{
  "batch_config": {
    "batch_size": 100,
    "parallel_operations": 5,
    "transaction_mode": "per_batch",
    "rollback_on_error": true
  }
}
```

### **Active Directory Extensions**

Special handling for AD attributes:

```json
{
  "active_directory": {
    "enable_ad_extensions": true,
    "user_account_control": true,
    "password_never_expires": false,
    "sam_account_name_from_uid": true,
    "user_principal_name_suffix": "@company.com"
  }
}
```

---

## 🔐 **Security**

### **Authentication Options**

```json
{
  "authentication": {
    "method": "simple", // simple, sasl
    "sasl_mechanism": "GSSAPI",
    "kerberos_keytab": "/path/to/keytab",
    "use_start_tls": true,
    "validate_certificates": true
  }
}
```

### **Connection Security**

- **LDAPS**: SSL/TLS encryption
- **StartTLS**: Upgrade plain connection
- **SASL**: Kerberos, EXTERNAL, DIGEST-MD5
- **Connection Pooling**: Secure connection reuse

### **Data Protection**

- **Password Hashing**: Automatic SSHA/SHA256
- **Attribute Encryption**: Sensitive field protection
- **Audit Logging**: All operations tracked
- **Access Control**: Bind DN permissions

---

## 🧪 **Testing**

### **Test Coverage**

- Unit Tests: 93%+ coverage
- Integration Tests: Mock LDAP server
- End-to-End Tests: Docker LDAP
- Security Tests: Auth and encryption

### **Running Tests**

```bash
# Unit tests
poetry run pytest tests/unit

# Integration tests
poetry run pytest tests/integration

# E2E tests with Docker
poetry run pytest tests/e2e

# All tests with coverage
poetry run pytest --cov=target_ldap
```

---

## 📚 **Usage Examples**

### **User Synchronization**

```python
# examples/user_sync.py
import json
from target_ldap import TargetLDAP

# Configure target
config = {
    "host": "ldap.company.com",
    "bind_dn": "cn=sync,dc=company,dc=com",
    "password": "sync_password",
    "base_dn": "dc=company,dc=com",
    "dn_templates": {
        "users": "uid={uid},ou=users,dc=company,dc=com"
    }
}

# Create target
target = TargetLDAP(config=config)

# Process user records
users = [
    {"uid": "jdoe", "cn": "John Doe", "mail": "jdoe@company.com"},
    {"uid": "jsmith", "cn": "Jane Smith", "mail": "jsmith@company.com"}
]

for user in users:
    target.process_record(user, "users")
```

### **Group Management**

```python
# examples/group_management.py
# Sync groups with members
groups = [
    {
        "cn": "developers",
        "description": "Development Team",
        "member": [
            "uid=jdoe,ou=users,dc=company,dc=com",
            "uid=jsmith,ou=users,dc=company,dc=com"
        ]
    }
]

for group in groups:
    target.process_record(group, "groups")
```

### **Active Directory Integration**

```python
# examples/active_directory.py
config = {
    "host": "dc.company.com",
    "port": 636,
    "use_ssl": True,
    "bind_dn": "CN=Sync User,OU=Service Accounts,DC=company,DC=com",
    "password": "secure_password",
    "base_dn": "DC=company,DC=com",
    "active_directory": {
        "enable_ad_extensions": True,
        "user_principal_name_suffix": "@company.com"
    }
}

# AD-specific attributes
ad_user = {
    "uid": "jdoe",
    "cn": "John Doe",
    "sAMAccountName": "jdoe",
    "userPrincipalName": "jdoe@company.com",
    "userAccountControl": 512  # Normal account
}
```

### **Meltano Pipeline**

```yaml
# meltano.yml
project_id: identity_sync
environments:
  - name: prod
    config:
      plugins:
        loaders:
          - name: target-ldap
            variant: datacosmos
            pip_url: target-ldap
            config:
              host: ${LDAP_HOST}
              port: ${LDAP_PORT}
              bind_dn: ${LDAP_BIND_DN}
              password: ${LDAP_PASSWORD}
              base_dn: ${LDAP_BASE_DN}
              use_ssl: true
```

---

## 🔗 **Integration Ecosystem**

### **Compatible Sources**

| Tap            | Purpose          | Status    |
| -------------- | ---------------- | --------- |
| `tap-csv`      | CSV user imports | ✅ Tested |
| `tap-postgres` | Database sync    | ✅ Tested |
| `tap-ldap`     | LDAP to LDAP     | ✅ Tested |
| `tap-rest-api` | HR system sync   | ✅ Tested |

### **PyAuto Integration**

| Component                                | Integration     | Purpose              |
| ---------------------------------------- | --------------- | -------------------- |
| [tap-ldap](../tap-ldap/)                 | Source tap      | Directory extraction |
| [ldap-core-shared](../ldap-core-shared/) | Shared models   | LDAP domain models   |
| [flext-ldap](../flext-ldap/)             | Migration tools | Directory migration  |

### **Directory Targets**

| Directory        | Protocol   | Features             |
| ---------------- | ---------- | -------------------- |
| Active Directory | LDAP/LDAPS | Full AD extensions   |
| OpenLDAP         | LDAP/LDAPS | Standard compliance  |
| Oracle Directory | LDAP/LDAPS | Enterprise features  |
| FreeIPA          | LDAP/LDAPS | Kerberos integration |

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **DN Already Exists**

   - **Symptom**: Entry already exists error
   - **Solution**: Ensure upsert mode is enabled

2. **Schema Violations**

   - **Symptom**: Object class violation
   - **Solution**: Check required attributes for object class

3. **Connection Timeouts**
   - **Symptom**: LDAP server timeout
   - **Solution**: Increase timeout, check network

### **Debug Mode**

```bash
# Enable debug logging
export TARGET_LDAP_LOG_LEVEL=DEBUG

# LDAP protocol tracing
export LDAP_TRACE_LEVEL=2

# Dry run mode
target-ldap --config config.json --dry-run
```

---

## 🛠️ **CLI Reference**

```bash
# Basic loading
target-ldap --config config.json

# Specific streams
target-ldap --config config.json --streams users,groups

# Validation only
target-ldap --config config.json --validate-only

# Test connection
target-ldap --config config.json --test

# Version info
target-ldap --version
```

---

## 📖 **Configuration Reference**

### **Required Settings**

| Setting    | Type   | Description          | Example                    |
| ---------- | ------ | -------------------- | -------------------------- |
| `host`     | string | LDAP server hostname | ldap.company.com           |
| `bind_dn`  | string | Bind DN for auth     | cn=REDACTED_LDAP_BIND_PASSWORD,dc=company,dc=com |
| `password` | string | Bind password        | secure_password            |
| `base_dn`  | string | Base DN              | dc=company,dc=com          |

### **Optional Settings**

| Setting               | Type    | Description        | Default |
| --------------------- | ------- | ------------------ | ------- |
| `port`                | integer | LDAP port          | 389     |
| `use_ssl`             | boolean | Use LDAPS          | false   |
| `timeout`             | integer | Connection timeout | 30      |
| `validate_records`    | boolean | Schema validation  | true    |
| `user_rdn_attribute`  | string  | User RDN attr      | uid     |
| `group_rdn_attribute` | string  | Group RDN attr     | cn      |

---

## 🔗 **Cross-References**

### **Prerequisites**

- [Singer Specification](https://hub.meltano.com/singer/spec) - Singer protocol specification
- [LDAP Protocol](https://ldap.com/ldapv3-wire-protocol-reference/) - LDAP v3 reference
- [RFC 4511](https://datatracker.ietf.org/doc/html/rfc4511) - LDAP protocol specification

### **Next Steps**

- [Directory Sync Guide](../docs/guides/directory-sync.md) - Complete sync setup
- [Identity Pipeline](../docs/guides/identity-pipeline.md) - Identity management
- [Production Deployment](../docs/deployment/ldap-deployment.md) - Production setup

### **Related Topics**

- [Singer Best Practices](../docs/patterns/singer.md) - Target patterns
- [Identity Management](../docs/patterns/identity.md) - Identity patterns
- [Directory Security](../docs/patterns/ldap-security.md) - Security best practices

---

**📂 Component**: Target LDAP | **🏠 Root**: [PyAuto Home](../README.md) | **Framework**: Singer SDK 0.39.0+ | **Updated**: 2025-06-19
