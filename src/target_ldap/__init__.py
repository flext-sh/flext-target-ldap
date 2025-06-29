"""target-ldap: Singer target for LDAP data loading.

This module implements a Singer target for loading data into LDAP directories
using the Singer SDK framework. It provides sinks for various LDAP object types
with support for create, update, and delete operations.

Architecture: Hexagonal Architecture - Port
Pattern: ETL Pipeline - Load
Dependencies: singer-sdk, ldap3
"""

from target_ldap.__version__ import __version__
from target_ldap.target import TargetLDAP

__all__ = ["TargetLDAP", "__version__"]
