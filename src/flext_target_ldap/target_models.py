"""Pydantic models for LDAP target (attribute mapping, entry, transformation, batch)."""

from __future__ import annotations

from .models import FlextTargetLdapModels

LdapAttributeMappingModel = FlextTargetLdapModels.TargetLdap.AttributeMapping
LdapEntryModel = FlextTargetLdapModels.TargetLdap.Entry
LdapTransformationResultModel = FlextTargetLdapModels.TargetLdap.TransformationResult
LdapBatchProcessingModel = FlextTargetLdapModels.TargetLdap.BatchProcessing
LdapOperationStatisticsModel = FlextTargetLdapModels.TargetLdap.OperationStatistics

TransformationRule = LdapAttributeMappingModel
TransformationResult = LdapTransformationResultModel
LDAPProcessingResult = LdapBatchProcessingModel

__all__ = [
    "LDAPProcessingResult",
    "LdapAttributeMappingModel",
    "LdapBatchProcessingModel",
    "LdapEntryModel",
    "LdapOperationStatisticsModel",
    "LdapTransformationResultModel",
    "TransformationResult",
    "TransformationRule",
]
