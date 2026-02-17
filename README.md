# FLEXT-Target-LDAP

[![Singer SDK](https://img.shields.io/badge/singer--sdk-compliant-brightgreen.svg)](https://sdk.meltano.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Target-LDAP** is a Singer-compliant target for loading data into LDAP directories. It enables specialized loading workflows for Active Directory and OpenLDAP, ensuring data integrity and correct schema mapping.

Part of the [FLEXT](https://github.com/flext-sh/flext) ecosystem.

## 🚀 Key Features

- **LDAP Directory Loading**: Efficiently loads data into hierarchical LDAP structures.
- **Intelligent Mapping**: Configurable DN templates and attribute mappings for flexible schema alignment.
- **Operational Control**: Supports ADD, MODIFY, and DELETE operations with rollback capabilities.
- **Batch Processing**: Optimized for performance with configurable batch sizes and connection pooling.
- **Security First**: Full support for LDAPS (SSL/TLS) and secure authentication methods.

## 📦 Installation

Install via Poetry:

```bash
poetry add flext-target-ldap
```

## 🛠️ Usage

### Basic Execution

Pipe data from a tap into the target:

```bash
cat data.jsonl | target-ldap --config config.json
```

### Configuration

Define your LDAP connection and mapping rules:

```json
{
  "ldap_host": "ldap.example.com",
  "bind_dn": "cn=admin,dc=example,dc=com",
  "bind_password": "secure_password",
  "base_dn": "dc=example,dc=com",
  "batch_size": 100,
  "default_stream_maps": {
    "users": {
        "dn_template": "uid={uid},ou=people,dc=example,dc=com",
        "object_classes": ["inetOrgPerson", "person"],
        "attribute_mapping": {
            "user_id": "uid",
            "email": "mail",
            "full_name": "cn"
        }
    }
  }
}
```

## 🏗️ Architecture

Built on the Singer SDK, ensuring standard compliance:

- **Orchestrator**: Manages the data flow and applies business logic.
- **Connection Manager**: Handles resilient LDAP connections using `flext-ldap`.
- **Stream Maps**: Flexible engine for transforming flat records into hierarchical LDAP entries.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on setting up a local LDAP test environment.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
