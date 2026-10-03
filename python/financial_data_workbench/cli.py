"""Command-line interface for validating financial CSV files."""

import argparse
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
import os
from pathlib import Path
import sys
from typing import Sequence

from .loader import CSVInputError, load_csv
from .reporting import render_json_report, render_markdown_report
from .results import ValidationResult
from .schema import DataSchema, NumericConstraint, OHLCColumns
from .validation import validate_dataset


def _schema_for_profile(name: str) -> DataSchema:
    """Build a documented built-in schema profile for the CLI."""
    if name != "ohlcv":
        raise ValueError("unsupported schema profile")
    return DataSchema(
        required_columns=("timestamp", "Open", "High", "Low", "Close", "Volume"),
        column_types={
            "timestamp": datetime,
            "Open": Decimal,
            "High": Decimal,
            "Low": Decimal,
            "Close": Decimal,
            "Volume": int,
        },
        timestamp_column="timestamp",
        numeric_constraints={"Volume": NumericConstraint(minimum=0)},
        ohlc_columns=OHLCColumns(),
    )


def _same_file(input_path: Path, output_path: Path) -> bool:
    """Return whether paths identify the same file, including aliases."""
    try:
        return os.path.samefile(input_path, output_path)
    except (FileNotFoundError, OSError):
        return input_path.resolve() == output_path.resolve()


def _report_safe_result(result: ValidationResult) -> ValidationResult:
    """Avoid including an invalid timestamp's source text in report messages."""
    issues = tuple(
        replace(issue, message="Invalid ISO-8601 timestamp.")
        if issue.code == "INVALID_TIMESTAMP"
        else issue
        for issue in result.issues
    )
    return ValidationResult(records_checked=result.records_checked, issues=issues)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="financial-data-workbench",
        description="Validate a financial CSV and render a findings report.",
    )
    parser.add_argument("input", help="CSV file to validate")
    parser.add_argument("--schema", choices=("ohlcv",), default="ohlcv")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", help="report file path; omit to write the report to stdout")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI; return 0 for clean data, 1 for findings, or 2 for errors."""
    args = _parser().parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output is not None else None

    if (output_path is not None and input_path.exists()
            and _same_file(input_path, output_path)):
        print("Error: report output must not be the input file.", file=sys.stderr)
        return 2

    try:
        schema = _schema_for_profile(args.schema)
        dataset = load_csv(input_path, schema)
        result = validate_dataset(dataset, schema)
    except (CSVInputError, OSError, ValueError, TypeError):
        # Avoid echoing parser details or source values on the command line.
        print("Error: input could not be loaded or validated.", file=sys.stderr)
        return 2

    renderer = render_json_report if args.format == "json" else render_markdown_report
    report = renderer(_report_safe_result(result), source_label=input_path.name)
    if output_path is None:
        try:
            sys.stdout.write(report)
        except (OSError, UnicodeError):
            print("Error: report could not be written.", file=sys.stderr)
            return 2
    else:
        try:
            output_path.write_text(report, encoding="utf-8", newline="")
        except (OSError, UnicodeError, ValueError):
            print("Error: report could not be written.", file=sys.stderr)
            return 2

    summary = result.summary
    print(
        f"Checked {summary.records_checked} records; "
        f"{summary.total_issues} issue(s) "
        f"({summary.issues_by_severity['error']} error(s), "
        f"{summary.issues_by_severity['warning']} warning(s)).",
        file=sys.stderr if output_path is None else sys.stdout,
    )
    return 1 if summary.total_issues else 0
