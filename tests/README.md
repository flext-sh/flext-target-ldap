# 🧪 TARGET LDAP - Test Suite

> **Module**: Comprehensive test suite for TARGET LDAP with Singer SDK compliance and LDAP integration testing | **Audience**: QA Engineers, LDAP Administrators, Target Testing Specialists | **Status**: Production Ready

## 📋 **Overview**

Enterprise-grade test suite for the TARGET LDAP implementation, providing comprehensive testing coverage including unit tests, integration tests with real LDAP directories, performance testing, and Singer SDK compliance validation. This test suite demonstrates best practices for testing Singer targets and LDAP data loading operations.

---

## 🧭 **Navigation Context**

**🏠 Root**: [PyAuto Home](../../README.md) → **📂 Component**: [TARGET LDAP](../README.md) → **📂 Current**: Test Suite

---

## 🎯 **Module Purpose**

This test module provides comprehensive validation for the TARGET LDAP implementation, ensuring reliability, performance, and correctness of all LDAP data loading operations, Singer SDK compliance, and enterprise LDAP directory integration workflows.

### **Key Testing Areas**

- **Unit Testing** - Core target logic and LDAP transformation validation
- **Integration Testing** - End-to-end data loading with real LDAP directories
- **Performance Testing** - LDAP operation throughput and performance
- **Singer SDK Testing** - Target compliance and specification validation
- **LDAP Authentication Testing** - LDAP bind and authentication validation
- **Error Handling Testing** - LDAP error recovery and resilience validation

---

## 📁 **Test Structure**

```
tests/
├── unit/
│   ├── test_target_core.py              # Core target functionality tests
│   ├── test_sinks_validation.py         # Sink implementation tests
│   ├── test_transformation.py           # LDAP transformation tests
│   ├── test_client_ldap.py              # LDAP client tests
│   └── test_config_validation.py        # Configuration validation tests
├── integration/
│   ├── test_ldap_integration.py         # LDAP directory integration tests
│   ├── test_singer_compliance.py        # Singer SDK compliance tests
│   ├── test_data_loading.py             # End-to-end data loading tests
│   ├── test_batch_processing.py         # Batch processing integration tests
│   └── test_real_time_loading.py        # Real-time data loading tests
├── e2e/
│   ├── __init__.py                      # E2E test package initialization
│   ├── conftest.py                      # E2E specific fixtures
│   ├── test_target_e2e.py               # Complete end-to-end workflow tests
│   └── ldif/                            # LDIF test data
│       ├── 01-base.ldif                 # Base LDIF test data
│       ├── source/                      # Source LDIF data
│       │   └── 01-base.ldif             # Source base data
│       └── target/                      # Target LDIF data
├── performance/
│   ├── test_throughput_performance.py   # LDAP operation throughput testing
│   ├── test_concurrent_loading.py       # Concurrent LDAP loading scenarios
│   ├── test_memory_optimization.py      # Memory usage optimization tests
│   └── test_scalability_limits.py       # LDAP scalability testing
├── singer/
│   ├── test_target_compliance.py        # Singer target specification compliance
│   ├── test_schema_validation.py        # Schema handling validation
│   ├── test_state_management.py         # State management testing
│   └── test_message_processing.py       # Singer message processing tests
├── fixtures/
│   ├── ldap_fixtures.py                 # LDAP test data fixtures
│   ├── singer_fixtures.py               # Singer message test fixtures
│   └── authentication_fixtures.py       # LDAP authentication test fixtures
├── conftest.py                           # Pytest configuration and fixtures
├── test_client.py                        # LDAP client tests
├── test_integration.py                   # Integration tests
├── test_sinks.py                         # Sink implementation tests
├── test_target.py                        # Core target tests
└── test_transformation.py                # LDAP transformation tests
```

---

## 🔧 **Test Categories**

### **1. Unit Tests (unit/)**

#### **Core Target Testing (test_target_core.py)**

```python
"""Unit tests for TARGET LDAP core functionality."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime

from target_ldap.target import TargetLDAP
from target_ldap.config import TargetConfig
from target_ldap.sinks import LDAPSink
from target_ldap.exceptions import (
    TargetConfigurationError,
    LDAPConnectionError,
    DataValidationError
)

class TestTargetLDAP:
    """Test LDAP target core functionality."""

    @pytest.fixture
    def target_config(self):
        """Target configuration fixture."""
        return TargetConfig(
            ldap_host="ldap://test-ldap.example.com",
            ldap_port=389,
            bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=example,dc=com",
            bind_password="REDACTED_LDAP_BIND_PASSWORD_password",
            base_dn="dc=example,dc=com",
            batch_size=100,
            timeout=30
        )

    @pytest.fixture
    def mock_ldap_client(self):
        """Mock LDAP client fixture."""
        return Mock()

    @pytest.fixture
    def target_instance(self, target_config, mock_ldap_client):
        """Target instance with mocked dependencies."""
        with patch('target_ldap.target.LDAPClient', return_value=mock_ldap_client):
            return TargetLDAP(config=target_config)

    def test_target_initialization_success(self, target_config):
        """Test successful target initialization."""
        # Act
        target = TargetLDAP(config=target_config)

        # Assert
        assert target.config == target_config
        assert target.name == "target-ldap"
        assert target.config.batch_size == 100

    def test_target_initialization_invalid_config(self):
        """Test target initialization with invalid configuration."""
        # Arrange
        invalid_config = TargetConfig(
            ldap_host="",  # Invalid empty host
            bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=example,dc=com",
            bind_password="password"
        )

        # Act & Assert
        with pytest.raises(TargetConfigurationError):
            TargetLDAP(config=invalid_config)

    def test_get_sink_for_stream(self, target_instance):
        """Test sink creation for specific stream."""
        # Arrange
        stream_name = "users"
        schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "cn": {"type": "string"},
                "mail": {"type": "string"}
            }
        }

        # Act
        sink = target_instance.get_sink(stream_name, schema)

        # Assert
        assert isinstance(sink, LDAPSink)
        assert sink.stream_name == stream_name
        assert sink.schema == schema

    def test_stream_discovery(self, target_instance, mock_ldap_client):
        """Test LDAP stream discovery functionality."""
        # Arrange
        mock_ldap_client.search.return_value = [
            {"dn": "ou=users,dc=example,dc=com", "objectClass": ["organizationalUnit"]},
            {"dn": "ou=groups,dc=example,dc=com", "objectClass": ["organizationalUnit"]}
        ]

        # Act
        streams = target_instance.discover_streams()

        # Assert
        assert len(streams) == 2
        assert streams[0]["name"] == "users"
        assert streams[1]["name"] == "groups"
        mock_ldap_client.search.assert_called_once()
```

#### **LDAP Transformation Testing (test_transformation.py)**

```python
"""Unit tests for LDAP data transformation functionality."""

import pytest
from datetime import datetime

from target_ldap.transformation import (
    LDAPTransformer,
    convert_to_ldap_attributes,
    format_dn,
    validate_ldap_entry
)
from target_ldap.exceptions import TransformationError

class TestLDAPTransformer:
    """Test LDAP data transformation functionality."""

    @pytest.fixture
    def transformer(self):
        """LDAP transformer instance."""
        return LDAPTransformer()

    def test_convert_to_ldap_attributes(self, transformer):
        """Test conversion of record data to LDAP attributes."""
        # Arrange
        record = {
            "uid": "john.doe",
            "cn": "John Doe",
            "sn": "Doe",
            "givenName": "John",
            "mail": "john.doe@example.com",
            "userPassword": "password123"
        }

        # Act
        ldap_attributes = transformer.convert_to_ldap_attributes(record)

        # Assert
        assert ldap_attributes["uid"] == ["john.doe"]
        assert ldap_attributes["cn"] == ["John Doe"]
        assert ldap_attributes["mail"] == ["john.doe@example.com"]
        assert "objectClass" in ldap_attributes

    def test_format_dn_generation(self, transformer):
        """Test Distinguished Name generation."""
        # Arrange
        record = {
            "uid": "john.doe",
            "cn": "John Doe"
        }
        base_dn = "ou=users,dc=example,dc=com"

        # Act
        dn = transformer.format_dn(record, base_dn)

        # Assert
        assert dn == "uid=john.doe,ou=users,dc=example,dc=com"

    def test_validate_ldap_entry_success(self, transformer):
        """Test LDAP entry validation success."""
        # Arrange
        ldap_entry = {
            "dn": "uid=john.doe,ou=users,dc=example,dc=com",
            "attributes": {
                "objectClass": ["inetOrgPerson", "organizationalPerson", "person"],
                "uid": ["john.doe"],
                "cn": ["John Doe"],
                "sn": ["Doe"]
            }
        }

        # Act & Assert
        # Should not raise exception
        transformer.validate_ldap_entry(ldap_entry)

    def test_validate_ldap_entry_failure(self, transformer):
        """Test LDAP entry validation failure."""
        # Arrange
        invalid_entry = {
            "dn": "",  # Invalid empty DN
            "attributes": {
                "uid": ["john.doe"]
            }
        }

        # Act & Assert
        with pytest.raises(TransformationError):
            transformer.validate_ldap_entry(invalid_entry)

    def test_multi_value_attribute_handling(self, transformer):
        """Test handling of multi-value LDAP attributes."""
        # Arrange
        record = {
            "uid": "john.doe",
            "cn": "John Doe",
            "objectClass": ["inetOrgPerson", "organizationalPerson"],
            "mail": ["john.doe@example.com", "john@example.com"]
        }

        # Act
        ldap_attributes = transformer.convert_to_ldap_attributes(record)

        # Assert
        assert isinstance(ldap_attributes["objectClass"], list)
        assert len(ldap_attributes["objectClass"]) >= 2
        assert isinstance(ldap_attributes["mail"], list)
        assert len(ldap_attributes["mail"]) == 2

    def test_special_character_handling(self, transformer):
        """Test handling of special characters in LDAP data."""
        # Arrange
        record = {
            "uid": "user.with+special=chars",
            "cn": "User With Special, Characters",
            "description": "User with special chars: +, =, <, >, #, \\"
        }

        # Act
        ldap_attributes = transformer.convert_to_ldap_attributes(record)
        dn = transformer.format_dn(record, "ou=users,dc=example,dc=com")

        # Assert
        assert ldap_attributes["uid"] == ["user.with+special=chars"]
        assert "uid=user.with+special=chars" in dn
        # Verify DN escaping is handled properly
        assert "," in ldap_attributes["cn"][0]
```

### **2. Integration Tests (integration/)**

#### **LDAP Integration Testing (test_ldap_integration.py)**

```python
"""Integration tests for LDAP directory integration."""

import pytest
import asyncio
from unittest.mock import patch, Mock
import json

from target_ldap.target import TargetLDAP
from target_ldap.config import TargetConfig

@pytest.mark.integration
class TestLDAPIntegration:
    """Test LDAP directory integration scenarios."""

    @pytest.fixture
    def integration_config(self):
        """Integration test configuration."""
        return TargetConfig(
            ldap_host="ldap://test-ldap.example.com",
            ldap_port=389,
            bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=example,dc=com",
            bind_password="integration_test_password",
            base_dn="dc=example,dc=com",
            batch_size=50,
            timeout=60
        )

    @pytest.fixture
    async def target_with_auth(self, integration_config):
        """Target instance with authenticated LDAP client."""
        target = TargetLDAP(config=integration_config)

        # Mock successful authentication
        with patch.object(target.ldap_client, 'bind') as mock_bind:
            mock_bind.return_value = True
            await target.ldap_client.bind()

        return target

    @pytest.mark.asyncio
    async def test_end_to_end_user_loading(self, target_with_auth):
        """Test end-to-end user data loading to LDAP."""
        # Arrange
        user_records = [
            {
                "uid": "john.doe",
                "cn": "John Doe",
                "sn": "Doe",
                "givenName": "John",
                "mail": "john.doe@example.com",
                "userPassword": "password123",
                "created_at": "2025-06-19T10:00:00Z"
            },
            {
                "uid": "jane.smith",
                "cn": "Jane Smith",
                "sn": "Smith",
                "givenName": "Jane",
                "mail": "jane.smith@example.com",
                "userPassword": "password456",
                "created_at": "2025-06-19T10:05:00Z"
            }
        ]

        schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "cn": {"type": "string"},
                "sn": {"type": "string"},
                "givenName": {"type": "string"},
                "mail": {"type": "string"},
                "userPassword": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        }

        # Mock successful LDAP operations
        with patch.object(target_with_auth.ldap_client, 'add_batch') as mock_add:
            mock_add.return_value = {
                "status": "success",
                "entries_processed": len(user_records),
                "operation_id": "OP_12345"
            }

            # Act
            sink = target_with_auth.get_sink("users", schema)

            for record in user_records:
                sink.process_record(record)

            result = sink.flush_records()

            # Assert
            assert result["status"] == "success"
            assert result["entries_processed"] == 2
            mock_add.assert_called_once()

    @pytest.mark.asyncio
    async def test_batch_processing_performance(self, target_with_auth):
        """Test batch processing performance with large LDAP datasets."""
        # Arrange
        batch_size = 100
        user_records = [
            {
                "uid": f"user_{i:06d}",
                "cn": f"Test User {i}",
                "sn": f"User{i}",
                "givenName": f"Test{i}",
                "mail": f"user{i}@example.com",
                "userPassword": f"password{i}"
            }
            for i in range(batch_size)
        ]

        schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "cn": {"type": "string"},
                "sn": {"type": "string"},
                "givenName": {"type": "string"},
                "mail": {"type": "string"},
                "userPassword": {"type": "string"}
            }
        }

        # Mock LDAP client for performance testing
        with patch.object(target_with_auth.ldap_client, 'add_batch') as mock_add:
            mock_add.return_value = {
                "status": "success",
                "entries_processed": batch_size,
                "processing_time_ms": 250
            }

            # Act
            import time
            start_time = time.time()

            sink = target_with_auth.get_sink("users", schema)

            for record in user_records:
                sink.process_record(record)

            result = sink.flush_records()
            end_time = time.time()

            # Assert
            processing_time = end_time - start_time
            assert result["status"] == "success"
            assert result["entries_processed"] == batch_size
            assert processing_time < 5.0  # Should process 100 entries in under 5 seconds

            # Verify batch was sent to LDAP
            mock_add.assert_called_once()
            call_args = mock_add.call_args[0][0]
            assert len(call_args) == batch_size
```

### **3. End-to-End Tests (e2e/)**

#### **Complete Workflow Testing (test_target_e2e.py)**

```python
"""End-to-end tests for complete TARGET LDAP workflow."""

import pytest
from unittest.mock import patch, Mock
import json
from datetime import datetime
import os

from target_ldap.target import TargetLDAP
from target_ldap.config import TargetConfig

@pytest.mark.e2e
class TestCompleteLDAPWorkflow:
    """Test complete LDAP target workflow."""

    @pytest.fixture
    def production_config(self):
        """Production-like configuration."""
        return TargetConfig(
            ldap_host="ldap://production-ldap.example.com",
            ldap_port=636,  # LDAPS
            bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=company,dc=com",
            bind_password="prod_REDACTED_LDAP_BIND_PASSWORD_password",
            base_dn="dc=company,dc=com",
            use_ssl=True,
            batch_size=1000,
            timeout=120,
            retry_attempts=3
        )

    def test_ldif_file_processing(self, production_config):
        """Test processing LDIF files for complete directory sync."""
        # Arrange
        ldif_file_path = os.path.join(os.path.dirname(__file__), "ldif", "01-base.ldif")

        # Mock LDAP target
        target = TargetLDAP(config=production_config)

        with patch.object(target.ldap_client, 'bind') as mock_bind, \
             patch.object(target.ldap_client, 'add_batch') as mock_add:

            mock_bind.return_value = True
            mock_add.return_value = {"status": "success", "entries_processed": 10}

            # Act
            # Process LDIF file through target
            result = target.process_ldif_file(ldif_file_path)

            # Assert
            assert result["status"] == "success"
            assert result["entries_processed"] > 0
            mock_bind.assert_called_once()
            mock_add.assert_called()

    @pytest.mark.asyncio
    async def test_complete_directory_migration(self, production_config):
        """Test complete directory migration workflow."""
        # Arrange
        directory_data = {
            "organizationalUnits": [
                {"dn": "ou=users,dc=company,dc=com", "objectClass": ["organizationalUnit"], "ou": "users"},
                {"dn": "ou=groups,dc=company,dc=com", "objectClass": ["organizationalUnit"], "ou": "groups"}
            ],
            "users": [
                {"uid": "REDACTED_LDAP_BIND_PASSWORD", "cn": "Administrator", "sn": "Admin", "mail": "REDACTED_LDAP_BIND_PASSWORD@company.com"},
                {"uid": "user1", "cn": "User One", "sn": "One", "mail": "user1@company.com"}
            ],
            "groups": [
                {"cn": "REDACTED_LDAP_BIND_PASSWORDistrators", "objectClass": ["groupOfNames"], "member": ["uid=REDACTED_LDAP_BIND_PASSWORD,ou=users,dc=company,dc=com"]},
                {"cn": "users", "objectClass": ["groupOfNames"], "member": ["uid=user1,ou=users,dc=company,dc=com"]}
            ]
        }

        # Mock successful LDAP operations
        target = TargetLDAP(config=production_config)

        with patch.object(target.ldap_client, 'bind') as mock_bind, \
             patch.object(target.ldap_client, 'add_batch') as mock_add:

            mock_bind.return_value = True
            mock_add.return_value = {"status": "success", "entries_processed": 2}

            # Act - Process each data type in proper order
            results = {}

            # First create organizational units
            for stream_name in ["organizationalUnits", "users", "groups"]:
                if stream_name in directory_data:
                    sink = target.get_sink(stream_name, self._get_schema_for_stream(stream_name))

                    for record in directory_data[stream_name]:
                        sink.process_record(record)

                    results[stream_name] = sink.flush_records()

            # Assert
            for stream_name, result in results.items():
                assert result["status"] == "success"
                assert result["entries_processed"] >= 2

    def _get_schema_for_stream(self, stream_name):
        """Get schema for LDAP stream type."""
        schemas = {
            "organizationalUnits": {
                "type": "object",
                "properties": {
                    "dn": {"type": "string"},
                    "objectClass": {"type": "array", "items": {"type": "string"}},
                    "ou": {"type": "string"}
                }
            },
            "users": {
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "cn": {"type": "string"},
                    "sn": {"type": "string"},
                    "mail": {"type": "string"}
                }
            },
            "groups": {
                "type": "object",
                "properties": {
                    "cn": {"type": "string"},
                    "objectClass": {"type": "array", "items": {"type": "string"}},
                    "member": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
        return schemas.get(stream_name, {})
```

---

## 🔧 **Test Configuration**

### **Pytest Configuration (conftest.py)**

```python
"""Pytest configuration and shared fixtures for TARGET LDAP tests."""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch
import json

from target_ldap.config import TargetConfig
from target_ldap.target import TargetLDAP

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_config():
    """Test configuration fixture."""
    return TargetConfig(
        ldap_host=os.getenv("TEST_LDAP_HOST", "ldap://test-ldap.example.com"),
        ldap_port=int(os.getenv("TEST_LDAP_PORT", "389")),
        bind_dn=os.getenv("TEST_BIND_DN", "cn=REDACTED_LDAP_BIND_PASSWORD,dc=example,dc=com"),
        bind_password=os.getenv("TEST_BIND_PASSWORD", "REDACTED_LDAP_BIND_PASSWORD_password"),
        base_dn=os.getenv("TEST_BASE_DN", "dc=example,dc=com"),
        batch_size=100,
        timeout=30
    )

@pytest.fixture
def mock_ldap_client():
    """Mock LDAP client."""
    client = Mock()
    client.bind.return_value = True
    client.add_batch.return_value = {
        "status": "success",
        "entries_processed": 0
    }
    client.search.return_value = []
    return client

@pytest.fixture
def target_instance(test_config, mock_ldap_client):
    """Target instance with mocked LDAP client."""
    with patch('target_ldap.target.LDAPClient', return_value=mock_ldap_client):
        return TargetLDAP(config=test_config)

@pytest.fixture
def sample_user_records():
    """Sample user records for testing."""
    return [
        {
            "uid": "john.doe",
            "cn": "John Doe",
            "sn": "Doe",
            "givenName": "John",
            "mail": "john.doe@example.com",
            "userPassword": "password123",
            "created_at": "2025-06-19T10:00:00Z"
        },
        {
            "uid": "jane.smith",
            "cn": "Jane Smith",
            "sn": "Smith",
            "givenName": "Jane",
            "mail": "jane.smith@example.com",
            "userPassword": "password456",
            "created_at": "2025-06-19T10:05:00Z"
        }
    ]

@pytest.fixture
def user_schema():
    """User stream schema fixture."""
    return {
        "type": "object",
        "properties": {
            "uid": {"type": "string"},
            "cn": {"type": "string"},
            "sn": {"type": "string"},
            "givenName": {"type": "string"},
            "mail": {"type": "string"},
            "userPassword": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"}
        },
        "required": ["uid", "cn", "sn"]
    }

@pytest.fixture
def singer_messages():
    """Sample Singer messages for testing."""
    return [
        {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "cn": {"type": "string"},
                    "mail": {"type": "string"}
                }
            }
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "uid": "john.doe",
                "cn": "John Doe",
                "mail": "john.doe@example.com"
            }
        },
        {
            "type": "STATE",
            "value": {"bookmarks": {"users": {"timestamp": "2025-06-19T10:00:00Z"}}}
        }
    ]
```

---

## 🔗 **Cross-References**

### **Component Documentation**

- [Component Overview](../README.md) - Complete TARGET LDAP documentation
- [Source Implementation](../src/README.md) - Source code structure and patterns
- [Configuration Guide](../docker-compose.yml) - Docker configuration examples

### **Testing Documentation**

- [Singer SDK Testing](https://sdk.meltano.com/en/latest/testing.html) - Singer SDK testing guidelines
- [PyTest Documentation](https://docs.pytest.org/) - Python testing framework
- [LDAP Testing Best Practices](https://ldapwiki.com/wiki/LDAP%20Testing) - LDAP testing patterns

### **LDAP References**

- [LDAP Protocol Documentation](https://ldapwiki.com/wiki/LDAP%20Protocol) - LDAP protocol reference
- [Python LDAP Documentation](https://python-ldap.readthedocs.io/) - Python LDAP library
- [LDIF Format Specification](https://tools.ietf.org/html/rfc2849) - LDIF format reference

---

**📂 Module**: Test Suite | **🏠 Component**: [TARGET LDAP](../README.md) | **Framework**: PyTest 7.0+ | **Updated**: 2025-06-19
