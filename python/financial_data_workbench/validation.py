"""Configurable validation rules for financial CSV datasets."""

import re
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation

from .loader import CSVRecord, LoadedDataset
from .results import Severity, ValidationIssue, ValidationResult
from .schema import DataSchema

_INTEGER = re.compile(r"^[+-]?\d+$")


def _is_missing(value: str) -> bool:
    """Blank and whitespace-only cells count as missing; source text is kept."""
    return value.strip() == ""


def _parse_decimal(value: str) -> Decimal:
    result = Decimal(value.strip())
    if not result.is_finite():
        raise InvalidOperation("decimal must be finite")
    return result


def _parse_timestamp(value: str) -> datetime:
    """Parse the configured ISO timestamp representation.

    A date-only value such as ``2026-10-01`` is interpreted as midnight at
    the start of that date. This is a parsing convention only; it makes no
    claim about the observation's actual time zone.
    """
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def _parse_value(value: str, kind: type) -> object:
    stripped = value.strip()
    if kind is str:
        return value
    if kind is int:
        if not _INTEGER.fullmatch(stripped):
            raise ValueError("expected an integer")
        return int(stripped)
    if kind is Decimal:
        return _parse_decimal(value)
    if kind is bool:
        lowered = stripped.lower()
        if lowered not in {"true", "false"}:
            raise ValueError("expected true or false")
        return lowered == "true"
    if kind is datetime:
        return _parse_timestamp(value)
    if kind is date:
        return date.fromisoformat(stripped)
    raise TypeError(f"unsupported configured type: {kind!r}")


def _location(record: CSVRecord, column: str | None = None) -> dict:
    return {
        "record_number": record.record_number,
        "line_number": record.line_number,
        "column": column,
    }


def validate_dataset(dataset: LoadedDataset, schema: DataSchema) -> ValidationResult:
    """Return findings without changing or removing any input record.

    Rules run in a stable order: cell presence/types/constraints, duplicate
    rows, then timestamp and OHLC checks. Cadence is an elapsed interval check
    between adjacent valid timestamps; it does not apply a trading calendar.
    """
    if not isinstance(dataset, LoadedDataset):
        raise TypeError("dataset must be a LoadedDataset")
    if not isinstance(schema, DataSchema):
        raise TypeError("schema must be a DataSchema")

    issues: list[ValidationIssue] = []

    def add(code: str, message: str, record: CSVRecord, column: str | None = None,
            severity: Severity = Severity.ERROR) -> None:
        issues.append(ValidationIssue(code=code, severity=severity, message=message,
                                      **_location(record, column)))

    for record in dataset.records:
        for column in schema.required_columns:
            raw = record.values[column]
            if _is_missing(raw):
                add("MISSING_VALUE", f"Required value for {column!r} is blank.", record, column)
                continue
            kind = schema.column_types.get(column)
            if kind is not None and column != schema.timestamp_column:
                try:
                    _parse_value(raw, kind)
                except (ValueError, TypeError, InvalidOperation, OverflowError) as error:
                    add("INVALID_TYPE", f"Value in {column!r} does not match {kind.__name__}: {error}.", record, column)

            constraint = schema.numeric_constraints.get(column)
            if constraint is not None:
                try:
                    number = _parse_decimal(raw)
                except (InvalidOperation, ValueError):
                    add("INVALID_NUMERIC", f"Value in {column!r} is not a finite decimal number.", record, column)
                else:
                    if constraint.minimum is not None and (
                        number < constraint.minimum
                        or (number == constraint.minimum and not constraint.minimum_inclusive)
                    ):
                        add("BELOW_MINIMUM", f"Value in {column!r} is below its configured minimum.", record, column)
                    if constraint.maximum is not None and (
                        number > constraint.maximum
                        or (number == constraint.maximum and not constraint.maximum_inclusive)
                    ):
                        add("ABOVE_MAXIMUM", f"Value in {column!r} exceeds its configured maximum.", record, column)

    seen_rows: dict[tuple[str, ...], CSVRecord] = {}
    for record in dataset.records:
        key = tuple(record.values[column] for column in dataset.headers)
        if key in seen_rows:
            add("DUPLICATE_ROW", f"Record duplicates record {seen_rows[key].record_number}.", record)
        else:
            seen_rows[key] = record

    timestamp_values: list[tuple[CSVRecord, datetime | None]] = []
    timestamp_column = schema.timestamp_column
    if timestamp_column is not None:
        seen_timestamps: dict[datetime, CSVRecord] = {}
        for record in dataset.records:
            raw = record.values[timestamp_column]
            if _is_missing(raw):
                timestamp_values.append((record, None))
                continue
            try:
                timestamp = _parse_timestamp(raw)
            except ValueError as error:
                add("INVALID_TIMESTAMP", f"Invalid ISO-8601 timestamp: {error}.", record, timestamp_column)
                timestamp_values.append((record, None))
                continue
            timestamp_values.append((record, timestamp))
            previous_same = seen_timestamps.get(timestamp)
            if previous_same is not None:
                add("DUPLICATE_TIMESTAMP", f"Timestamp duplicates record {previous_same.record_number}.", record, timestamp_column)
            else:
                seen_timestamps[timestamp] = record

        previous_valid: datetime | None = None
        for index, (record, current) in enumerate(timestamp_values):
            if current is not None:
                if previous_valid is not None:
                    try:
                        order_delta = current - previous_valid
                    except TypeError:
                        add("INCOMPATIBLE_TIMESTAMP_ZONES",
                            "Valid timestamps mix timezone-aware and timezone-naive values.",
                            record, timestamp_column)
                    else:
                        if order_delta < timedelta(0):
                            add("UNSORTED_TIMESTAMP",
                                "Timestamp is earlier than the preceding valid timestamp.",
                                record, timestamp_column)
                previous_valid = current

            # Cadence is only evaluated across adjacent source records. Invalid
            # or missing timestamps therefore break cadence comparisons.
            if index == 0 or current is None:
                continue
            _, previous = timestamp_values[index - 1]
            if previous is None:
                continue
            try:
                cadence_delta = current - previous
            except TypeError:
                continue
            if cadence_delta <= timedelta(0):
                continue
            if (schema.expected_cadence is not None
                    and cadence_delta != schema.expected_cadence):
                code = ("TIMESTAMP_GAP" if cadence_delta > schema.expected_cadence
                        else "TIMESTAMP_CADENCE_MISMATCH")
                add(code,
                    f"Adjacent timestamp interval {cadence_delta} differs from expected cadence {schema.expected_cadence}.",
                    record, timestamp_column, Severity.WARNING)

    if schema.ohlc_columns is not None:
        columns = schema.ohlc_columns
        for record in dataset.records:
            parsed: dict[str, Decimal] = {}
            for column in columns.price_columns:
                raw = record.values[column]
                if _is_missing(raw):
                    continue
                try:
                    parsed[column] = _parse_decimal(raw)
                except (InvalidOperation, ValueError):
                    add("INVALID_OHLC_NUMBER", f"OHLC value in {column!r} is not a finite decimal.", record, column)
            if len(parsed) != len(columns.price_columns):
                continue
            open_value = parsed[columns.open]
            high_value = parsed[columns.high]
            low_value = parsed[columns.low]
            close_value = parsed[columns.close]
            for label, value in (("open", open_value), ("close", close_value), ("low", low_value)):
                if high_value < value:
                    add("OHLC_HIGH_BELOW_COMPONENT",
                        f"High must be greater than or equal to {label}.", record, columns.high)
            for label, value in (("open", open_value), ("close", close_value), ("high", high_value)):
                if low_value > value:
                    add("OHLC_LOW_ABOVE_COMPONENT",
                        f"Low must be less than or equal to {label}.", record, columns.low)

    return ValidationResult(records_checked=len(dataset.records), issues=tuple(issues))
