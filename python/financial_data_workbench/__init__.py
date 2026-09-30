"""Dependency-light validation tools for financial CSV datasets."""

from .loader import CSVInputError, CSVRecord, LoadedDataset, load_csv, load_csv_text
from .results import Severity, ValidationIssue, ValidationResult, ValidationSummary
from .schema import DataSchema, NumericConstraint, OHLCColumns
from .validation import validate_dataset

__all__ = [
    "CSVInputError",
    "CSVRecord",
    "DataSchema",
    "LoadedDataset",
    "NumericConstraint",
    "OHLCColumns",
    "Severity",
    "ValidationIssue",
    "ValidationResult",
    "ValidationSummary",
    "load_csv",
    "load_csv_text",
    "validate_dataset",
]
