"""CSV loading that preserves cell text and source record order."""

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .schema import DataSchema


class CSVInputError(ValueError):
    """Raised when CSV structure cannot be safely interpreted."""


@dataclass(frozen=True)
class CSVRecord:
    """A data record with a 1-based data record number and ending line.

    ``record_number`` excludes the header. ``line_number`` is the physical
    CSV line on which this record ends; for a quoted multiline field this is
    the final physical line of that logical data record.
    """

    record_number: int
    line_number: int
    values: Mapping[str, str]


@dataclass(frozen=True)
class LoadedDataset:
    """CSV header and records in their original order."""

    headers: tuple[str, ...]
    records: tuple[CSVRecord, ...]


def load_csv_text(text: str, schema: DataSchema) -> LoadedDataset:
    """Parse CSV text without normalizing, coercing, or reordering cell data."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(schema, DataSchema):
        raise TypeError("schema must be a DataSchema")

    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    try:
        raw_headers = next(reader)
    except StopIteration as error:
        raise CSVInputError("CSV is empty; a header row is required") from error
    except csv.Error as error:
        raise CSVInputError(f"Malformed CSV header: {error}") from error

    headers_list = list(raw_headers)
    if headers_list and headers_list[0].startswith("\ufeff"):
        headers_list[0] = headers_list[0].lstrip("\ufeff")
    headers = tuple(headers_list)
    if not headers or any(not header.strip() for header in headers):
        raise CSVInputError("CSV header contains an empty column name")
    duplicates = sorted({header for header in headers if headers.count(header) > 1})
    if duplicates:
        raise CSVInputError("CSV header contains duplicate columns: " + ", ".join(duplicates))

    missing = [name for name in schema.required_columns if name not in headers]
    if missing:
        raise CSVInputError("CSV is missing required columns: " + ", ".join(missing))

    records: list[CSVRecord] = []
    try:
        for record_number, row in enumerate(reader, start=1):
            line_number = reader.line_num
            if len(row) != len(headers):
                raise CSVInputError(
                    f"Malformed CSV record {record_number} ending at line "
                    f"{line_number}: expected {len(headers)} fields, found {len(row)}"
                )
            records.append(
                CSVRecord(
                    record_number=record_number,
                    line_number=line_number,
                    values=MappingProxyType(dict(zip(headers, row))),
                )
            )
    except csv.Error as error:
        raise CSVInputError(
            f"Malformed CSV near physical line {reader.line_num}: {error}"
        ) from error
    return LoadedDataset(headers=headers, records=tuple(records))


def load_csv(path: str | Path, schema: DataSchema) -> LoadedDataset:
    """Read UTF-8 CSV from ``path`` and preserve its cell values as strings."""
    try:
        with Path(path).open(encoding="utf-8-sig", newline="") as file:
            text = file.read()
    except (OSError, UnicodeError) as error:
        raise CSVInputError(f"Could not read CSV file {path}: {error}") from error
    return load_csv_text(text, schema)
