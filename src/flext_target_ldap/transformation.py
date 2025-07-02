"""Data transformation engine for target-ldap.

This module implements sophisticated data transformation capabilities
for Oracle-to-LDAP migration scenarios, ported from client-a-oud-mig
for the brutal simplification project.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, ClassVar

from flext_ldap.utils.simple_dn_utils import simple_parse_dn


# Simple TransformationAppliedEvent definition until ldap-core-shared is fixed
@dataclass
class TransformationAppliedEvent:
    """Simple event for data transformation operations."""

    transformation_type: str
    source_entry_dn: str
    target_entry_dn: str
    success: bool
    transformation_rules_applied: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


logger = logging.getLogger(__name__)


@dataclass
class ClassificationResult:
    """Result of data classification operation."""

    entry_type: str
    confidence: float = 0.0
    reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source_indicators: list[str] = field(default_factory=list)


@dataclass
class TransformationRule:
    """Configuration for a single transformation rule."""

    name: str
    condition: str  # Python expression to evaluate
    action: str  # Type of transformation
    parameters: dict[str, Any] = field(default_factory=dict)
    priority: int = 100
    enabled: bool = True
    description: str = ""


@dataclass
class TransformationResult:
    """Result of transformation operation."""

    success: bool
    original_entry: dict[str, Any]
    transformed_entry: dict[str, Any]
    applied_rules: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class OidDataClassifier:
    """Classifier for Oracle Internet Directory (OID) data entries.

    Ported from client-a-oud-mig to provide intelligent classification
    of different entry types during migration.
    """

    INTERNAL_OID_PATTERNS: ClassVar[list[str]] = [
        r"cn=oid.*",
        r"cn=opmn.*",
        r"cn=catalog.*",
        r"cn=products.*",
        r"cn=oraclecontext.*",
        r"cn=subscriber.*",
        r"cn=orclreplicationcontext.*",
        r"cn=orclservercontext.*",
        r"cn=subschemasubentry.*",
    ]

    ORACLE_SCHEMA_PATTERNS: ClassVar[list[str]] = [
        r"cn=subschemasubentry.*",
        r"cn=schema.*",
        r"cn=configuration.*",
    ]

    ORACLE_ACL_PATTERNS: ClassVar[list[str]] = [
        r"cn=acl.*",
        r"cn=policycontext.*",
        r"cn=.*,cn=acl.*",
    ]

    BUSINESS_DATA_PATTERNS: ClassVar[list[str]] = [
        r"cn=.*,ou=people.*",
        r"cn=.*,ou=users.*",
        r"cn=.*,ou=groups.*",
        r"uid=.*,ou=.*",
        r"mail=.*",
    ]

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize classifier with configuration."""
        self.config = config or {}
        self.custom_patterns = self.config.get("custom_classification_patterns", {})

    def classify_entry(
        self,
        dn: str,
        attributes: dict[str, Any],
    ) -> ClassificationResult:
        """Classify an LDAP entry based on DN and attributes.

        Args:
        ----
            dn: Distinguished name of the entry
            attributes: Entry attributes

        Returns:
        -------
            Classification result with type and confidence

        """
        dn_lower = dn.lower()
        object_classes = [oc.lower() for oc in attributes.get("objectClass", [])]

        # Check for internal OID data
        if self._matches_patterns(dn_lower, self.INTERNAL_OID_PATTERNS):
            return ClassificationResult(
                entry_type="internal_oid",
                confidence=0.95,
                reasons=["DN matches internal OID patterns"],
                source_indicators=["oracle_internal"],
                metadata={"skip_migration": True},
            )

        # Check for Oracle schema objects
        if self._matches_patterns(dn_lower, self.ORACLE_SCHEMA_PATTERNS):
            return ClassificationResult(
                entry_type="oracle_schema",
                confidence=0.90,
                reasons=["DN matches Oracle schema patterns"],
                source_indicators=["oracle_schema"],
                metadata={"requires_transformation": True},
            )

        # Check for Oracle ACL objects
        if self._matches_patterns(dn_lower, self.ORACLE_ACL_PATTERNS):
            return ClassificationResult(
                entry_type="oracle_acl",
                confidence=0.85,
                reasons=["DN matches Oracle ACL patterns"],
                source_indicators=["oracle_acl"],
                metadata={"requires_acl_conversion": True},
            )

        # Check for Oracle-specific object classes
        oracle_ocs = [oc for oc in object_classes if oc.startswith("orcl")]
        if oracle_ocs:
            return ClassificationResult(
                entry_type="oracle_user" if "orcluser" in oracle_ocs else "oracle_data",
                confidence=0.80,
                reasons=[f"Contains Oracle object classes: {oracle_ocs}"],
                source_indicators=["oracle_objectclass"],
                metadata={
                    "oracle_classes": oracle_ocs,
                    "requires_transformation": True,
                },
            )

        # Check for business data
        if self._matches_patterns(dn_lower, self.BUSINESS_DATA_PATTERNS):
            return ClassificationResult(
                entry_type="business_data",
                confidence=0.75,
                reasons=["DN matches business data patterns"],
                source_indicators=["business_pattern"],
                metadata={"migrate_priority": "high"},
            )

        # Check for standard LDAP object classes
        if "person" in object_classes or "inetorgperson" in object_classes:
            return ClassificationResult(
                entry_type="user",
                confidence=0.70,
                reasons=["Contains person object classes"],
                source_indicators=["standard_person"],
            )

        if "groupofnames" in object_classes or "groupofuniquenames" in object_classes:
            return ClassificationResult(
                entry_type="group",
                confidence=0.70,
                reasons=["Contains group object classes"],
                source_indicators=["standard_group"],
            )

        if "organizationalunit" in object_classes:
            return ClassificationResult(
                entry_type="organizational_unit",
                confidence=0.70,
                reasons=["Contains OU object class"],
                source_indicators=["standard_ou"],
            )

        # Default classification
        return ClassificationResult(
            entry_type="unknown",
            confidence=0.10,
            reasons=["No specific patterns matched"],
            source_indicators=["fallback"],
        )

    def _matches_patterns(self, dn: str, patterns: list[str]) -> bool:
        """Check if DN matches any of the given patterns."""
        return any(re.match(pattern, dn, re.IGNORECASE) for pattern in patterns)


class DataTransformationEngine:
    """Advanced data transformation engine for Oracle-to-LDAP migration.

    Ported from client-a-oud-mig to provide enterprise-grade transformation
    capabilities for complex migration scenarios.
    """

    # Default transformation rules
    DEFAULT_RULES: ClassVar[list[dict[str, Any]]] = [
        {
            "name": "oracle_dn_structure_transform",
            "condition": (
                "classification.entry_type in ['oracle_user', 'oracle_data'] "
                "and 'dc=ctbc' in entry['dn']"
            ),
            "action": "transform_dn_structure",
            "parameters": {
                "source_pattern": r"(.*),dc=ctbc",
                "target_pattern": r"\1,dc=network,dc=ctbc",
            },
            "priority": 10,
            "description": "Transform Oracle DN structure to target format",
        },
        {
            "name": "oracle_objectclass_conversion",
            "condition": "any(oc.startswith('orcl') for oc in entry.get('objectClass', []))",
            "action": "convert_oracle_objectclasses",
            "parameters": {
                "mappings": {
                    "orclUser": ["inetOrgPerson", "person", "organizationalPerson"],
                    "orclGroup": ["groupOfNames"],
                    "orclContext": ["organizationalUnit"],
                },
            },
            "priority": 20,
            "description": "Convert Oracle object classes to standard LDAP equivalents",
        },
        {
            "name": "oracle_attribute_mapping",
            "condition": "classification.entry_type.startswith('oracle_')",
            "action": "map_oracle_attributes",
            "parameters": {
                "attribute_mappings": {
                    "orclSamAccountName": "uid",
                    "orclCommonName": "cn",
                    "orclMailNickname": "mailNickname",
                    "orclGUID": "entryUUID",
                },
            },
            "priority": 30,
            "description": "Map Oracle-specific attributes to standard equivalents",
        },
        {
            "name": "oracle_aci_to_acl_conversion",
            "condition": "classification.entry_type == 'oracle_acl'",
            "action": "convert_aci_to_acl",
            "parameters": {
                "preserve_original": False,
                "default_permissions": ["read", "search"],
            },
            "priority": 40,
            "description": "Convert Oracle ACI format to OUD ACL format",
        },
        {
            "name": "clean_empty_attributes",
            "condition": "True",  # Apply to all entries
            "action": "remove_empty_attributes",
            "parameters": {
                "preserve_required": True,
                "required_attributes": ["cn", "objectClass"],
            },
            "priority": 90,
            "description": "Remove empty or null attribute values",
        },
    ]

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize transformation engine."""
        self.config = config or {}
        self.classifier = OidDataClassifier(config)
        self.rules = self._load_transformation_rules()
        self.stats = {
            "total_processed": 0,
            "total_transformed": 0,
            "rules_applied": {},
            "errors": [],
            "warnings": [],
        }

    def _load_transformation_rules(self) -> list[TransformationRule]:
        """Load transformation rules from configuration."""
        rules: list[Any] = []

        # Load default rules
        for rule_config in self.DEFAULT_RULES:
            rule = TransformationRule(**rule_config)
            rules.append(rule)

        # Load custom rules from config
        custom_rules = self.config.get("transformation_rules", [])
        for rule_config in custom_rules:
            rule = TransformationRule(**rule_config)
            rules.append(rule)

        # Sort by priority
        rules.sort(key=lambda r: r.priority)

        return rules

    def transform_entry(self, entry: dict[str, Any]) -> TransformationResult:
        """Transform a single LDAP entry.

        Args:
        ----
            entry: Original entry data

        Returns:
        -------
            Transformation result with modified entry

        """
        self.stats["total_processed"] += 1

        # Start with original entry
        result = TransformationResult(
            success=True,
            original_entry=entry.copy(),
            transformed_entry=entry.copy(),
        )

        try:
            # Classify the entry first
            dn = entry.get("dn", "")
            attributes = {k: v for k, v in entry.items() if k != "dn"}

            classification = self.classifier.classify_entry(dn, attributes)
            result.metadata["classification"] = classification

            # Apply transformation rules
            for rule in self.rules:
                if not rule.enabled:
                    continue

                # Check if rule condition is met
                if self._evaluate_condition(rule.condition, entry, classification):
                    try:
                        # Apply the transformation
                        self._apply_transformation_rule(rule, result, classification)
                        result.applied_rules.append(rule.name)

                        # Update statistics
                        self.stats["rules_applied"][rule.name] = (
                            self.stats["rules_applied"].get(rule.name, 0) + 1
                        )

                    except Exception as e:
                        error_msg = f"Error applying rule {rule.name}: {e}"
                        result.errors.append(error_msg)
                        result.warnings.append(f"Skipped rule {rule.name} due to error")
                        logger.exception(error_msg)

            # Mark as transformed if any rules were applied
            if result.applied_rules:
                self.stats["total_transformed"] += 1
                result.metadata["transformation_timestamp"] = datetime.now(
                    UTC,
                ).isoformat()

                # Emit transformation event
                event = TransformationAppliedEvent(
                    dn=entry.get("dn", ""),
                    transformation_rules=result.applied_rules,
                    original_data=result.original_entry,
                    transformed_data=result.transformed_entry,
                )
                result.metadata["event"] = event

        except Exception as e:
            result.success = False
            result.errors.append(f"Transformation failed: {e}")
            self.stats["errors"].append(str(e))
            logger.exception("Failed to transform entry %s", entry.get("dn", "unknown"))

        return result

    def _evaluate_condition(
        self,
        condition: str,
        entry: dict[str, Any],
        classification: ClassificationResult,
    ) -> bool:
        """Evaluate a rule condition."""
        try:
            # Create evaluation context
            context = {
                "entry": entry,
                "classification": classification,
                "dn": entry.get("dn", ""),
                "attributes": {k: v for k, v in entry.items() if k != "dn"},
            }

            # Safely evaluate the condition with minimal builtins
            safe_builtins = {
                "any": any,
                "all": all,
                "len": len,
                "bool": bool,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
            }
            return bool(eval(condition, {"__builtins__": safe_builtins}, context))

        except Exception as e:
            logger.warning("Failed to evaluate condition '%s': %s", condition, e)
            return False

    def _apply_transformation_rule(
        self,
        rule: TransformationRule,
        result: TransformationResult,
        classification: ClassificationResult,
    ) -> None:
        """Apply a specific transformation rule."""
        action = rule.action
        params = rule.parameters
        entry = result.transformed_entry

        if action == "transform_dn_structure":
            self._transform_dn_structure(entry, params, result)

        elif action == "convert_oracle_objectclasses":
            self._convert_oracle_objectclasses(entry, params, result)

        elif action == "map_oracle_attributes":
            self._map_oracle_attributes(entry, params, result)

        elif action == "convert_aci_to_acl":
            self._convert_aci_to_acl(entry, params, result)

        elif action == "remove_empty_attributes":
            self._remove_empty_attributes(entry, params, result)

        else:
            result.warnings.append(f"Unknown transformation action: {action}")

    def _transform_dn_structure(
        self,
        entry: dict[str, Any],
        params: dict[str, Any],
        result: TransformationResult,
    ) -> None:
        """Transform DN structure using regex patterns."""
        dn = entry.get("dn", "")
        source_pattern = params.get("source_pattern", "")
        target_pattern = params.get("target_pattern", "")

        if not dn or not source_pattern:
            return

        new_dn = re.sub(source_pattern, target_pattern, dn, flags=re.IGNORECASE)
        if new_dn != dn:
            entry["dn"] = new_dn
            result.metadata["dn_transformed"] = {"from": dn, "to": new_dn}

    def _convert_oracle_objectclasses(
        self,
        entry: dict[str, Any],
        params: dict[str, Any],
        result: TransformationResult,
    ) -> None:
        """Convert Oracle object classes to standard LDAP equivalents."""
        mappings = params.get("mappings", {})
        object_classes = entry.get("objectClass", [])

        if not isinstance(object_classes, list):
            object_classes = [object_classes]

        new_object_classes: list[Any] = []
        conversions: dict[str, Any] = {}

        for oc in object_classes:
            if oc in mappings:
                # Convert Oracle object class
                standard_ocs = mappings[oc]
                if isinstance(standard_ocs, str):
                    standard_ocs = [standard_ocs]
                new_object_classes.extend(standard_ocs)
                conversions[oc] = standard_ocs
                # Keep existing object class
                new_object_classes.append(oc)

        if conversions:
            # Remove duplicates while preserving order
            entry["objectClass"] = list(dict.fromkeys(new_object_classes))
            result.metadata["objectclass_conversions"] = conversions

    def _map_oracle_attributes(
        self,
        entry: dict[str, Any],
        params: dict[str, Any],
        result: TransformationResult,
    ) -> None:
        """Map Oracle-specific attributes to standard equivalents."""
        mappings = params.get("attribute_mappings", {})
        conversions: dict[str, Any] = {}

        for oracle_attr, standard_attr in mappings.items():
            if oracle_attr in entry:
                value = entry.pop(oracle_attr)
                entry[standard_attr] = value
                conversions[oracle_attr] = standard_attr

        if conversions:
            result.metadata["attribute_mappings"] = conversions

    def _convert_aci_to_acl(
        self,
        entry: dict[str, Any],
        params: dict[str, Any],
        result: TransformationResult,
    ) -> None:
        """Convert Oracle ACI format to OUD ACL format."""
        # This is a simplified implementation - in real scenario would need
        # comprehensive ACI parsing and ACL generation
        aci_attrs = ["aci", "orclACI"]
        preserve_original = params.get("preserve_original", False)

        for aci_attr in aci_attrs:
            if aci_attr in entry:
                aci_values = entry[aci_attr]
                if not isinstance(aci_values, list):
                    aci_values = [aci_values]

                # Convert each ACI to ACL format (simplified)
                acl_values: list[Any] = []
                for aci in aci_values:
                    acl = self._convert_aci_string_to_acl(aci, params)
                    acl_values.append(acl)

                # Replace or add ACL attribute
                if not preserve_original:
                    entry.pop(aci_attr)

                entry["ds-privilege-name"] = acl_values
                result.metadata[f"{aci_attr}_converted"] = len(acl_values)

    def _convert_aci_string_to_acl(self, aci: str, params: dict[str, Any]) -> str:
        """Convert a single ACI string to ACL format."""
        # Simplified conversion - real implementation would need comprehensive parsing
        default_perms = params.get("default_permissions", ["read", "search"])

        # Extract basic information from ACI (this is very simplified)
        if "allow" in aci.lower():
            return f"({','.join(default_perms)})"
        return "(read,search)"

    def _remove_empty_attributes(
        self,
        entry: dict[str, Any],
        params: dict[str, Any],
        result: TransformationResult,
    ) -> None:
        """Remove empty or null attribute values."""
        preserve_required = params.get("preserve_required", True)
        required_attrs = set(params.get("required_attributes", ["cn", "objectClass"]))

        removed_attrs: list[Any] = []

        for attr_name in list(entry.keys()):
            if preserve_required and attr_name in required_attrs:
                continue

            value = entry[attr_name]

            # Check for empty values
            if value is None or value == "" or (isinstance(value, list) and not value):
                entry.pop(attr_name)
                removed_attrs.append(attr_name)

        if removed_attrs:
            result.metadata["removed_empty_attributes"] = removed_attrs

    def get_statistics(self) -> dict[str, Any]:
        """Get transformation statistics."""
        return {
            "total_processed": self.stats["total_processed"],
            "total_transformed": self.stats["total_transformed"],
            "transformation_rate": (
                self.stats["total_transformed"]
                / max(self.stats["total_processed"], 1)
                * 100
            ),
            "rules_applied": dict(self.stats["rules_applied"]),
            "error_count": len(self.stats["errors"]),
            "warning_count": len(self.stats["warnings"]),
            "last_updated": datetime.now(UTC).isoformat(),
        }

    def reset_statistics(self) -> None:
        """Reset transformation statistics."""
        self.stats = {
            "total_processed": 0,
            "total_transformed": 0,
            "rules_applied": {},
            "errors": [],
            "warnings": [],
        }


class MigrationValidator:
    """Validator for ensuring migration data quality and compliance.

    Provides validation capabilities for migration scenarios.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize migration validator."""
        self.config = config or {}
        self.validation_stats = {
            "total_validated": 0,
            "validation_passed": 0,
            "validation_failed": 0,
            "errors": [],
            "warnings": [],
        }

    def validate_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        """Validate a single entry for migration compliance."""
        self.validation_stats["total_validated"] += 1

        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks_performed": [],
        }

        # DN validation
        dn = entry.get("dn", "")
        if not dn:
            validation_result["errors"].append("Missing DN")
            validation_result["valid"] = False
        elif not self._validate_dn_syntax(dn):
            validation_result["errors"].append(f"Invalid DN syntax: {dn}")
            validation_result["valid"] = False
        validation_result["checks_performed"].append("dn_syntax")

        # Object class validation
        object_classes = entry.get("objectClass", [])
        if not object_classes:
            validation_result["errors"].append("Missing objectClass")
            validation_result["valid"] = False
        elif not self._validate_object_classes(object_classes):
            validation_result["warnings"].append("Unusual object class combination")
        validation_result["checks_performed"].append("object_classes")

        # Required attributes validation
        self._validate_required_attributes(entry, validation_result)
        validation_result["checks_performed"].append("required_attributes")

        # Data type validation
        self._validate_attribute_types(entry, validation_result)
        validation_result["checks_performed"].append("attribute_types")

        # Update statistics
        if validation_result["valid"]:
            self.validation_stats["validation_passed"] += 1
        else:
            self.validation_stats["validation_failed"] += 1
            self.validation_stats["errors"].extend(validation_result["errors"])

        self.validation_stats["warnings"].extend(validation_result["warnings"])

        return validation_result

    def _validate_dn_syntax(self, dn: str) -> bool:
        """Validate DN syntax."""
        try:
            # Use ldap-core-shared utilities
            components = simple_parse_dn(dn)
            return len(components) > 0
        except Exception:
            return False

    def _validate_object_classes(self, object_classes: list[str]) -> bool:
        """Validate object class combination."""
        if not isinstance(object_classes, list):
            object_classes = [object_classes]

        # Check for common valid combinations
        structural_classes = {
            "person",
            "inetOrgPerson",
            "groupOfNames",
            "organizationalUnit",
            "organization",
        }
        has_structural = any(oc.lower() in structural_classes for oc in object_classes)

        return has_structural or "top" in [oc.lower() for oc in object_classes]

    def _validate_required_attributes(
        self,
        entry: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        """Validate required attributes based on object classes."""
        object_classes = entry.get("objectClass", [])
        if not isinstance(object_classes, list):
            object_classes = [object_classes]

        # Define required attributes for common object classes
        required_attrs = {
            "person": ["cn", "sn"],
            "inetOrgPerson": ["cn", "sn"],
            "groupOfNames": ["cn", "member"],
            "organizationalUnit": ["ou"],
            "organization": ["o"],
        }

        for oc in object_classes:
            oc_lower = oc.lower()
            if oc_lower in required_attrs:
                for attr in required_attrs[oc_lower]:
                    if attr not in entry or not entry[attr]:
                        result["errors"].append(
                            f"Missing required attribute '{attr}' for object class '{oc}'",
                        )
                        result["valid"] = False

    def _validate_attribute_types(
        self,
        entry: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        """Validate attribute value types and formats."""
        # Email validation
        if "mail" in entry:
            mail_values = entry["mail"]
            if not isinstance(mail_values, list):
                mail_values = [mail_values]

            for mail in mail_values:
                if not re.match(r"^[^@]+@[^@]+\.[^@]+$", str(mail)):
                    result["warnings"].append(f"Invalid email format: {mail}")

        # DN reference validation
        dn_attributes = {"member", "memberOf", "manager"}
        for attr in dn_attributes:
            if attr in entry:
                dn_values = entry[attr]
                if not isinstance(dn_values, list):
                    dn_values = [dn_values]

                for dn_ref in dn_values:
                    if not self._validate_dn_syntax(str(dn_ref)):
                        result["warnings"].append(
                            f"Invalid DN reference in {attr}: {dn_ref}",
                        )

    def get_validation_statistics(self) -> dict[str, Any]:
        """Get validation statistics."""
        total = self.validation_stats["total_validated"]
        return {
            "total_validated": total,
            "validation_passed": self.validation_stats["validation_passed"],
            "validation_failed": self.validation_stats["validation_failed"],
            "pass_rate": (self.validation_stats["validation_passed"] / max(total, 1))
            * 100,
            "error_count": len(self.validation_stats["errors"]),
            "warning_count": len(self.validation_stats["warnings"]),
            "last_updated": datetime.now(UTC).isoformat(),
        }
