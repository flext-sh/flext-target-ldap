"""target-ldap: Singer target for LDAP data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.

This module implements a Singer target for loading data into LDAP directories
using the Singer SDK framework. It provides sinks for various LDAP object types
with support for create, update, and delete operations.

Architecture: Hexagonal Architecture - Port
Pattern: ETL Pipeline - Load
Dependencies: singer-sdk, ldap3
"""

from flext_target_ldap.__version__ import __version__
from flext_target_ldap.target import TargetLDAP

__all__ = ["TargetLDAP", "__version__"]
