# Logging Migration Report for flext-target-ldap

## Summary

Total files with logging imports: 8

## Files to Migrate

- `src/flext_target_ldap/client.py:9` - `import logging`
- `src/flext_target_ldap/sinks.py:10` - `import logging`
- `src/flext_target_ldap/target.py:8` - `import logging`
- `src/flext_target_ldap/transformation.py:10` - `import logging`
- `src/target_ldap/client.py:9` - `import logging`
- `src/target_ldap/sinks.py:10` - `import logging`
- `src/target_ldap/target.py:8` - `import logging`
- `src/target_ldap/transformation.py:10` - `import logging`

## Migration Steps

1. Replace logging imports:

   ```python
   # Old
   import logging
   logger = logging.getLogger(__name__)

   # New
   from flext_observability.logging import get_logger
   logger = get_logger(__name__)
   ```

2. Add setup_logging to your main entry point:

   ```python
   from flext_observability import setup_logging

   setup_logging(
       service_name="flext-target-ldap",
       log_level="INFO",
       json_logs=True
   )
   ```

3. Update logging calls to use structured format:

   ```python
   # Old
   logger.info("Processing %s items", count)

   # New
   logger.info("Processing items", count=count)
   ```

See `examples/logging_migration.py` for a complete example.
