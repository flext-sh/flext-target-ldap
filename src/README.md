# 🎯 TARGET LDAP - Source Implementation

> **Module**: Complete LDAP target source implementation with enterprise directory loading and transformation capabilities | **Audience**: Data Engineers, LDAP Administrators, Singer SDK Developers | **Status**: Production Ready

## 📋 **Overview**

Complete source implementation of the TARGET LDAP Singer target, providing comprehensive data loading to LDAP directory services with advanced transformation, validation, and enterprise directory management capabilities for seamless data pipeline integration.

---

## 🧭 **Navigation Context**

**🏠 Root**: [PyAuto Home](../../README.md) → **📂 Component**: [TARGET LDAP](../README.md) → **📂 Current**: Source Implementation

---

## 🎯 **Module Purpose**

This source module implements a production-ready Singer target for LDAP directory services, following Singer SDK specifications with comprehensive data transformation, directory operations, and enterprise LDAP integration patterns for complex directory environments.

### **Key Capabilities**

- **Enterprise LDAP Loading** - Comprehensive LDAP directory data loading
- **Directory Operations** - Advanced LDAP create, update, delete operations
- **Data Transformation** - Built-in transformation and validation for LDAP formats
- **Schema Mapping** - Automatic mapping between data formats and LDAP schema
- **Batch Processing** - Efficient batch operations for large data sets
- **Error Handling** - Comprehensive error recovery and validation

---

## 📁 **Module Structure**

```
src/target_ldap/
├── __init__.py              # Public API exports and Singer target registration
├── sinks.py                 # Core sink implementations for LDAP operations
├── target.py                # Main Singer target implementation
└── transformation.py        # Data transformation and LDAP mapping logic
```

---

## 🔧 **Core Components**

### **1. Core Sinks (sinks.py)**

Main sink implementations for LDAP directory operations:

```python
class LdapDirectorySink(Sink):
    """Core sink for LDAP directory operations.

    Handles data loading to LDAP directory with comprehensive
    transformation, validation, and error handling capabilities.
    """

    def __init__(
        self,
        target: TargetLDAP,
        stream_name: str,
        schema: dict,
        key_properties: List[str]
    ):
        super().__init__(target, stream_name, schema, key_properties)
        self.ldap_adapter = LdapAdapter(target.config)
        self.transformation_engine = LdapTransformationEngine(schema)
        self.batch_buffer = []
        self.last_flush_time = time.time()

    def process_record(self, record: dict, context: dict) -> None:
        """Process individual record for LDAP directory loading."""

        # Transform record to LDAP format
        ldap_entry = self.transformation_engine.transform_to_ldap(record)

        # Validate LDAP entry structure
        validation_result = self._validate_ldap_entry(ldap_entry)
        if not validation_result.is_valid:
            raise LdapValidationError(
                f"LDAP entry validation failed: {validation_result.errors}"
            )

        # Add to batch buffer
        self.batch_buffer.append(ldap_entry)

        # Check if batch should be flushed
        if self._should_flush():
            self.flush_batch()

    def flush_batch(self) -> None:
        """Flush batch to LDAP directory."""
        if not self.batch_buffer:
            return

        try:
            with self.ldap_adapter.get_connection() as conn:
                conn.bind()

                for ldap_entry in self.batch_buffer:
                    self._process_ldap_entry(conn, ldap_entry)

                # Clear buffer on success
                self.batch_buffer.clear()
                self.last_flush_time = time.time()

        except Exception as e:
            self._handle_batch_error(e)

    def _process_ldap_entry(self, connection: Connection, entry: LdapEntry) -> None:
        """Process individual LDAP entry."""

        operation = entry.operation_type
        dn = entry.distinguished_name
        attributes = entry.attributes

        if operation == "add":
            self._add_ldap_entry(connection, dn, attributes)
        elif operation == "modify":
            self._modify_ldap_entry(connection, dn, attributes)
        elif operation == "delete":
            self._delete_ldap_entry(connection, dn)
        else:
            raise LdapOperationError(f"Unsupported operation: {operation}")

    def _add_ldap_entry(self, connection: Connection, dn: str, attributes: dict) -> None:
        """Add new LDAP entry."""
        try:
            connection.add(dn, attributes=attributes)

            if not connection.result['result'] == 0:
                raise LdapOperationError(
                    f"LDAP add failed: {connection.result['description']}"
                )

        except Exception as e:
            self._handle_ldap_error("add", dn, e)

    def _modify_ldap_entry(self, connection: Connection, dn: str, attributes: dict) -> None:
        """Modify existing LDAP entry."""
        try:
            # Build modification list
            modifications = {}
            for attr_name, attr_value in attributes.items():
                modifications[attr_name] = [(MODIFY_REPLACE, attr_value)]

            connection.modify(dn, modifications)

            if not connection.result['result'] == 0:
                raise LdapOperationError(
                    f"LDAP modify failed: {connection.result['description']}"
                )

        except Exception as e:
            self._handle_ldap_error("modify", dn, e)

    def _delete_ldap_entry(self, connection: Connection, dn: str) -> None:
        """Delete LDAP entry."""
        try:
            connection.delete(dn)

            if not connection.result['result'] == 0:
                raise LdapOperationError(
                    f"LDAP delete failed: {connection.result['description']}"
                )

        except Exception as e:
            self._handle_ldap_error("delete", dn, e)

    def _should_flush(self) -> bool:
        """Determine if batch should be flushed."""
        return (
            len(self.batch_buffer) >= self.target.config.batch_size or
            time.time() - self.last_flush_time >= self.target.config.max_batch_age
        )

class LdapUserSink(LdapDirectorySink):
    """Specialized sink for LDAP user entries."""

    def _validate_ldap_entry(self, entry: LdapEntry) -> ValidationResult:
        """Validate LDAP user entry."""
        errors = []

        # Check required user attributes
        required_attrs = ["cn", "sn", "objectClass"]
        for attr in required_attrs:
            if attr not in entry.attributes:
                errors.append(f"Required attribute '{attr}' missing")

        # Validate objectClass for users
        object_classes = entry.attributes.get("objectClass", [])
        if "person" not in object_classes and "inetOrgPerson" not in object_classes:
            errors.append("User entry must have 'person' or 'inetOrgPerson' objectClass")

        # Validate email format if present
        if "mail" in entry.attributes:
            email = entry.attributes["mail"]
            if not self._is_valid_email(email):
                errors.append(f"Invalid email format: {email}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )

class LdapGroupSink(LdapDirectorySink):
    """Specialized sink for LDAP group entries."""

    def _validate_ldap_entry(self, entry: LdapEntry) -> ValidationResult:
        """Validate LDAP group entry."""
        errors = []

        # Check required group attributes
        required_attrs = ["cn", "objectClass"]
        for attr in required_attrs:
            if attr not in entry.attributes:
                errors.append(f"Required attribute '{attr}' missing")

        # Validate objectClass for groups
        object_classes = entry.attributes.get("objectClass", [])
        if "group" not in object_classes and "groupOfNames" not in object_classes:
            errors.append("Group entry must have 'group' or 'groupOfNames' objectClass")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
```

### **2. Main Target Implementation (target.py)**

Singer SDK-compliant target implementation:

```python
class TargetLDAP(Target):
    """LDAP directory Singer target for data loading.

    Implements Singer SDK specification for LDAP directory
    data loading with comprehensive transformation and validation.
    """

    name = "target-ldap"
    config_jsonschema = th.PropertiesList(
        th.Property("ldap_server", th.StringType, required=True),
        th.Property("ldap_port", th.IntegerType, default=389),
        th.Property("bind_dn", th.StringType, required=True),
        th.Property("bind_password", th.StringType, required=True, secret=True),
        th.Property("base_dn", th.StringType, required=True),
        th.Property("use_ssl", th.BooleanType, default=False),
        th.Property("use_tls", th.BooleanType, default=False),
        th.Property("batch_size", th.IntegerType, default=100),
        th.Property("max_batch_age", th.IntegerType, default=300),
        th.Property("operation_mode", th.StringType, default="upsert"),
    ).to_dict()

    default_sink_class = LdapDirectorySink

    def get_sink_class(self, stream_name: str) -> Type[Sink]:
        """Get appropriate sink class for stream."""

        if stream_name.lower().startswith("user"):
            return LdapUserSink
        elif stream_name.lower().startswith("group"):
            return LdapGroupSink
        elif stream_name.lower().startswith("ou"):
            return LdapOUSink
        else:
            return LdapDirectorySink

    def get_sink(
        self,
        stream_name: str,
        record: dict,
        schema: dict,
        key_properties: List[str]
    ) -> Sink:
        """Create sink for specific stream."""
        sink_class = self.get_sink_class(stream_name)
        return sink_class(
            target=self,
            stream_name=stream_name,
            schema=schema,
            key_properties=key_properties
        )
```

### **3. Data Transformation (transformation.py)**

Comprehensive data transformation for LDAP format:

```python
class LdapTransformationEngine:
    """Data transformation engine for LDAP target.

    Handles transformation of input data to LDAP entry format
    with comprehensive mapping and validation capabilities.
    """

    def __init__(self, schema: dict):
        self.schema = schema
        self.attribute_mappings = self._build_attribute_mappings()
        self.object_class_mappings = self._build_object_class_mappings()

    def transform_to_ldap(self, record: dict) -> LdapEntry:
        """Transform input record to LDAP entry format."""

        # Determine operation type
        operation_type = self._determine_operation_type(record)

        # Build distinguished name
        dn = self._build_distinguished_name(record)

        # Transform attributes
        ldap_attributes = self._transform_attributes(record)

        # Add required object classes
        ldap_attributes["objectClass"] = self._determine_object_classes(record)

        return LdapEntry(
            distinguished_name=dn,
            attributes=ldap_attributes,
            operation_type=operation_type
        )

    def _build_distinguished_name(self, record: dict) -> str:
        """Build LDAP distinguished name from record."""

        # Determine RDN attribute (typically cn, uid, or ou)
        rdn_attr = self._determine_rdn_attribute(record)
        rdn_value = record.get(rdn_attr)

        if not rdn_value:
            raise TransformationError(f"RDN attribute '{rdn_attr}' not found in record")

        # Build DN with proper escaping
        rdn = f"{rdn_attr}={self._escape_dn_value(rdn_value)}"

        # Add base DN
        base_dn = self._determine_base_dn(record)

        return f"{rdn},{base_dn}"

    def _transform_attributes(self, record: dict) -> dict:
        """Transform record attributes to LDAP format."""

        ldap_attributes = {}

        for field_name, field_value in record.items():
            # Skip metadata fields
            if field_name.startswith("_"):
                continue

            # Map field name to LDAP attribute
            ldap_attr_name = self.attribute_mappings.get(field_name, field_name)

            # Transform field value
            ldap_attr_value = self._transform_attribute_value(
                field_value,
                ldap_attr_name
            )

            ldap_attributes[ldap_attr_name] = ldap_attr_value

        return ldap_attributes

    def _transform_attribute_value(self, value: Any, attr_name: str) -> Any:
        """Transform individual attribute value for LDAP."""

        if value is None:
            return []

        # Handle different attribute types
        if attr_name in ["memberOf", "member", "objectClass"]:
            # Multi-value attributes
            if isinstance(value, str):
                return [value]
            elif isinstance(value, list):
                return value
            else:
                return [str(value)]

        elif attr_name in ["userAccountControl", "primaryGroupID"]:
            # Integer attributes
            return int(value) if value else 0

        elif attr_name in ["accountExpires", "lastLogon", "pwdLastSet"]:
            # Windows timestamp attributes
            if isinstance(value, str):
                # Parse ISO datetime to Windows timestamp
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return int((dt - datetime(1601, 1, 1, tzinfo=timezone.utc)).total_seconds() * 10000000)
            return value

        else:
            # String attributes (default)
            return str(value) if value else ""

    def _determine_object_classes(self, record: dict) -> List[str]:
        """Determine appropriate LDAP object classes for record."""

        object_classes = []

        # Check for user indicators
        if any(field in record for field in ["mail", "sAMAccountName", "userPrincipalName"]):
            object_classes.extend(["top", "person", "organizationalPerson", "user"])

        # Check for group indicators
        elif any(field in record for field in ["groupType", "member"]):
            object_classes.extend(["top", "group"])

        # Check for OU indicators
        elif "ou" in record or "organizationalUnit" in record.get("objectClass", []):
            object_classes.extend(["top", "organizationalUnit"])

        # Default to generic object
        else:
            object_classes.extend(["top"])

        # Add custom object classes from mapping
        custom_classes = self.object_class_mappings.get(
            record.get("record_type", ""), []
        )
        object_classes.extend(custom_classes)

        return list(set(object_classes))  # Remove duplicates

    def _build_attribute_mappings(self) -> dict:
        """Build attribute name mappings from schema."""

        mappings = {
            # Common user attribute mappings
            "username": "sAMAccountName",
            "email": "mail",
            "first_name": "givenName",
            "last_name": "sn",
            "display_name": "displayName",
            "phone": "telephoneNumber",
            "mobile": "mobile",
            "department": "department",
            "title": "title",
            "manager": "manager",

            # Common group attribute mappings
            "group_name": "cn",
            "group_description": "description",
            "group_members": "member",

            # Common OU attribute mappings
            "ou_name": "ou",
            "ou_description": "description"
        }

        # Add custom mappings from schema
        schema_mappings = self.schema.get("ldap_mappings", {})
        mappings.update(schema_mappings)

        return mappings

    def _build_object_class_mappings(self) -> dict:
        """Build object class mappings from schema."""

        return {
            "user": ["top", "person", "organizationalPerson", "user"],
            "group": ["top", "group"],
            "contact": ["top", "person", "organizationalPerson", "contact"],
            "computer": ["top", "person", "organizationalPerson", "user", "computer"],
            "ou": ["top", "organizationalUnit"]
        }
```

---

## 🔄 **Operation Workflows**

### **Complete LDAP Loading Workflow**

```python
async def execute_ldap_data_loading(
    target: TargetLDAP,
    input_stream: TextIO,
    state: Optional[Dict] = None
) -> LoadResult:
    """Execute complete LDAP data loading workflow."""

    load_stats = LoadStats()

    try:
        # Initialize target
        await target.initialize()

        # Process input stream
        for line in input_stream:
            message = singer.parse_message(line)

            if isinstance(message, singer.RecordMessage):
                # Get appropriate sink for stream
                sink = target.get_sink(
                    message.stream,
                    message.record,
                    message.schema,
                    message.key_properties
                )

                # Process record through sink
                sink.process_record(message.record, {})
                load_stats.records_processed += 1

            elif isinstance(message, singer.SchemaMessage):
                # Update schema for stream
                target.update_schema(message.stream, message.schema)

            elif isinstance(message, singer.StateMessage):
                # Update state
                target.update_state(message.value)

        # Flush all pending batches
        for sink in target.get_active_sinks():
            sink.flush_batch()

        return LoadResult(
            records_loaded=load_stats.records_processed,
            batches_sent=load_stats.batches_sent,
            errors_encountered=load_stats.errors,
            final_state=target.get_state(),
            load_duration=load_stats.get_duration()
        )

    except Exception as e:
        await target.handle_load_error(e)
        raise
    finally:
        await target.cleanup()
```

---

## 🧪 **Testing Utilities**

### **Test Patterns**

```python
@pytest.mark.asyncio
async def test_ldap_user_transformation():
    """Test LDAP user transformation functionality."""
    schema = {
        "properties": {
            "username": {"type": "string"},
            "email": {"type": "string"},
            "first_name": {"type": "string"},
            "last_name": {"type": "string"}
        }
    }

    engine = LdapTransformationEngine(schema)

    input_record = {
        "username": "jdoe",
        "email": "john.doe@company.com",
        "first_name": "John",
        "last_name": "Doe"
    }

    ldap_entry = engine.transform_to_ldap(input_record)

    assert ldap_entry.attributes["sAMAccountName"] == "jdoe"
    assert ldap_entry.attributes["mail"] == "john.doe@company.com"
    assert ldap_entry.attributes["givenName"] == "John"
    assert ldap_entry.attributes["sn"] == "Doe"
    assert "person" in ldap_entry.attributes["objectClass"]

@pytest.mark.asyncio
async def test_ldap_connection():
    """Test LDAP connection functionality."""
    config = LdapConfig(
        ldap_server="test-ldap.company.com",
        ldap_port=389,
        bind_dn="cn=REDACTED_LDAP_BIND_PASSWORD,dc=company,dc=com",
        bind_password="test_password",
        base_dn="dc=company,dc=com"
    )

    adapter = LdapAdapter(config)

    with adapter.get_connection() as conn:
        assert conn.bind(), "LDAP connection should succeed"
```

---

## 🔗 **Cross-References**

### **Component Documentation**

- [Component Overview](../README.md) - Complete TARGET LDAP documentation
- [Examples](../examples/README.md) - Usage examples and configurations
- [Tests](../tests/README.md) - Testing strategies and utilities

### **Singer SDK References**

- [Singer SDK Documentation](https://sdk.meltano.com/en/latest/) - Singer SDK specification
- [Target Patterns](https://sdk.meltano.com/en/latest/targets.html) - Target implementation patterns
- [Data Transformation](https://sdk.meltano.com/en/latest/stream_maps.html) - Data transformation patterns

### **LDAP References**

- [LDAP Protocol Specification](https://tools.ietf.org/html/rfc4511) - LDAP protocol standards
- [LDAP Schema Reference](https://tools.ietf.org/html/rfc4512) - LDAP schema standards
- [Active Directory Schema](https://docs.microsoft.com/en-us/windows/win32/adschema/) - AD schema reference

---

**📂 Module**: Source Implementation | **🏠 Component**: [TARGET LDAP](../README.md) | **Framework**: Singer SDK 0.35.0+ | **Updated**: 2025-06-19
