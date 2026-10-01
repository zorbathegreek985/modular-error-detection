"""Dependency-light validation tools for financial CSV datasets."""

from .loader import CSVInputError, CSVRecord, LoadedDataset, load_csv, load_csv_text
from .results import Severity, ValidationIssue, ValidationResult, ValidationSummary
from .reporting import build_report_data, render_json_report, render_markdown_report
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
    "build_report_data",
    "load_csv",
    "load_csv_text",
    "render_json_report",
    "render_markdown_report",
    "validate_dataset",
]
