from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from financial_data_workbench import (
    CSVInputError,
    DataSchema,
    NumericConstraint,
    OHLCColumns,
    Severity,
    load_csv,
    load_csv_text,
    validate_dataset,
)


HEADER = "timestamp,Open,High,Low,Close,Volume,note"
VALID_ROW = "2025-01-02T09:00:00,10.00,12.00,9.00,11.00,100, sample "


def ohlcv_schema(**overrides):
    settings = {
        "required_columns": ("timestamp", "Open", "High", "Low", "Close", "Volume", "note"),
        "column_types": {
            "timestamp": datetime,
            "Open": Decimal,
            "High": Decimal,
            "Low": Decimal,
            "Close": Decimal,
            "Volume": int,
        },
        "timestamp_column": "timestamp",
        "ohlc_columns": OHLCColumns(),
    }
    settings.update(overrides)
    return DataSchema(**settings)


def codes(result):
    return [issue.code for issue in result.issues]


def test_clean_dataset_has_no_issues_and_preserves_record_order():
    text = HEADER + "\n" + VALID_ROW + "\n2025-01-02T10:00:00,11,13,10,12,120,next"
    dataset = load_csv_text(text, ohlcv_schema())

    result = validate_dataset(dataset, ohlcv_schema())

    assert result.records_checked == 2
    assert result.issues == ()
    assert [record.record_number for record in dataset.records] == [1, 2]
    assert dataset.records[0].values["note"] == " sample "


def test_load_csv_reads_utf8_file_without_normalizing_cells(tmp_path):
    path = tmp_path / "financial.csv"
    path.write_text(HEADER + "\n" + VALID_ROW, encoding="utf-8")

    dataset = load_csv(path, ohlcv_schema())

    assert dataset.records[0].values["note"] == " sample "


def test_loader_rejects_missing_required_columns():
    with pytest.raises(CSVInputError, match="missing required columns: Close"):
        load_csv_text("timestamp,Open,High,Low,Volume,note\n", ohlcv_schema())


def test_missing_and_whitespace_only_values_are_reported_but_retained():
    dataset = load_csv_text(
        HEADER + "\n2025-01-02T09:00:00,10,12,9,11,100,   ", ohlcv_schema()
    )

    result = validate_dataset(dataset, ohlcv_schema())

    missing = [issue for issue in result.issues if issue.code == "MISSING_VALUE"]
    assert len(missing) == 1
    assert missing[0].column == "note"
    assert missing[0].record_number == 1
    assert dataset.records[0].values["note"] == "   "


def test_empty_cell_is_missing_and_remains_an_empty_source_string():
    dataset = load_csv_text(
        HEADER + "\n2025-01-02T09:00:00,10,12,9,11,100,", ohlcv_schema()
    )

    result = validate_dataset(dataset, ohlcv_schema())

    assert [issue.code for issue in result.issues] == ["MISSING_VALUE"]
    assert dataset.records[0].values["note"] == ""


def test_invalid_configured_types_are_reported():
    dataset = load_csv_text(
        HEADER + "\n2025-01-02T09:00:00,not-a-number,12,9,11,1.5,note",
        ohlcv_schema(),
    )
    result = validate_dataset(dataset, ohlcv_schema())

    invalid = [issue for issue in result.issues if issue.code == "INVALID_TYPE"]
    assert {issue.column for issue in invalid} == {"Open", "Volume"}


def test_invalid_timestamps_are_reported_with_data_record_and_physical_line():
    dataset = load_csv_text(
        HEADER + '\n"not a timestamp",10,12,9,11,1,"two lines\ncontinued"',
        ohlcv_schema(),
    )
    result = validate_dataset(dataset, ohlcv_schema())

    issue = next(item for item in result.issues if item.code == "INVALID_TIMESTAMP")
    assert issue.record_number == 1
    assert issue.line_number == 3
    assert issue.column == "timestamp"


def test_duplicate_rows_and_timestamps_are_distinguished():
    row = "2025-01-02T09:00:00,10,12,9,11,100,a"
    repeated_timestamp = "2025-01-02T09:00:00,10,12,9,11,100,b"
    dataset = load_csv_text(HEADER + "\n" + row + "\n" + row + "\n" + repeated_timestamp,
                            ohlcv_schema())

    result = validate_dataset(dataset, ohlcv_schema())

    assert codes(result).count("DUPLICATE_ROW") == 1
    assert codes(result).count("DUPLICATE_TIMESTAMP") == 2


def test_unsorted_timestamps_are_reported():
    rows = [
        "2025-01-02T10:00:00,10,12,9,11,1,a",
        "2025-01-02T09:00:00,10,12,9,11,1,b",
    ]
    result = validate_dataset(load_csv_text(HEADER + "\n" + "\n".join(rows), ohlcv_schema()),
                             ohlcv_schema())

    issue = next(item for item in result.issues if item.code == "UNSORTED_TIMESTAMP")
    assert issue.record_number == 2


def test_gap_is_warning_when_expected_cadence_is_configured():
    schema = ohlcv_schema(expected_cadence=timedelta(hours=1))
    rows = [
        "2025-01-02T09:00:00,10,12,9,11,1,a",
        "2025-01-02T11:00:00,10,12,9,11,1,b",
    ]
    result = validate_dataset(load_csv_text(HEADER + "\n" + "\n".join(rows), schema), schema)

    gap = next(issue for issue in result.issues if issue.code == "TIMESTAMP_GAP")
    assert gap.severity is Severity.WARNING
    assert gap.record_number == 2


def test_no_gap_findings_without_cadence_configuration():
    rows = [
        "2025-01-02T09:00:00,10,12,9,11,1,a",
        "2025-01-02T15:00:00,10,12,9,11,1,b",
    ]
    result = validate_dataset(load_csv_text(HEADER + "\n" + "\n".join(rows), ohlcv_schema()),
                             ohlcv_schema())

    assert "TIMESTAMP_GAP" not in codes(result)
    assert "TIMESTAMP_CADENCE_MISMATCH" not in codes(result)


def test_valid_ohlc_relationships_use_decimal_values():
    dataset = load_csv_text(HEADER + "\n" + VALID_ROW, ohlcv_schema())

    result = validate_dataset(dataset, ohlcv_schema())

    assert not any(code.startswith("OHLC_") for code in codes(result))


def test_invalid_ohlc_relationships_are_reported_without_modifying_values():
    row = "2025-01-02T09:00:00,10.00,9.00,11.00,12.00,100,note"
    dataset = load_csv_text(HEADER + "\n" + row, ohlcv_schema())

    result = validate_dataset(dataset, ohlcv_schema())

    assert codes(result).count("OHLC_HIGH_BELOW_COMPONENT") == 3
    assert codes(result).count("OHLC_LOW_ABOVE_COMPONENT") == 2
    assert dataset.records[0].values["High"] == "9.00"


def test_numeric_constraints_are_configurable_and_decimal_exact():
    schema = ohlcv_schema(
        numeric_constraints={"Close": NumericConstraint(minimum="0.01", maximum="100.00")}
    )
    rows = [
        "2025-01-02T09:00:00,10,12,9,0.00,1,a",
        "2025-01-02T10:00:00,10,12,9,100.01,1,b",
    ]
    result = validate_dataset(load_csv_text(HEADER + "\n" + "\n".join(rows), schema), schema)

    assert codes(result).count("BELOW_MINIMUM") == 1
    assert codes(result).count("ABOVE_MAXIMUM") == 1


def test_whitespace_is_preserved_and_trimmed_only_for_validation():
    row = '2025-01-02T09:00:00," 10.00 ",12,9,11,100," value "'
    dataset = load_csv_text(HEADER + "\n" + row, ohlcv_schema())

    result = validate_dataset(dataset, ohlcv_schema())

    assert result.issues == ()
    assert dataset.records[0].values["Open"] == " 10.00 "
    assert dataset.records[0].values["note"] == " value "


def test_result_summary_and_issue_order_are_deterministic():
    row = "2025-01-02T09:00:00,10,12,9,11,100,a"
    schema = ohlcv_schema(expected_cadence=timedelta(hours=1))
    text = HEADER + "\n" + row + "\n" + row
    dataset = load_csv_text(text, schema)
    first = validate_dataset(dataset, schema)
    second = validate_dataset(dataset, schema)

    assert first == second
    assert first.summary == second.summary
    assert first.summary.records_checked == 2
    assert first.summary.total_issues == len(first.issues)
    assert first.summary.issues_by_code == {
        "DUPLICATE_ROW": 1,
        "DUPLICATE_TIMESTAMP": 1,
    }


def test_schema_rejects_float_for_financial_numeric_type():
    with pytest.raises(TypeError, match="unsupported type"):
        DataSchema(required_columns=("price",), column_types={"price": float})


def test_loader_rejects_malformed_row_width():
    with pytest.raises(CSVInputError, match="expected 7 fields, found 6"):
        load_csv_text(HEADER + "\n2025-01-02T09:00:00,10,12,9,11,100", ohlcv_schema())


def test_cadence_requires_timestamp_column_and_positive_interval():
    with pytest.raises(ValueError, match="requires a timestamp_column"):
        DataSchema(required_columns=("price",), expected_cadence=timedelta(minutes=1))
    with pytest.raises(ValueError, match="must be positive"):
        DataSchema(required_columns=("timestamp",), timestamp_column="timestamp",
                   expected_cadence=timedelta(0))


def test_invalid_timestamp_does_not_hide_later_out_of_order_valid_timestamp():
    schema = DataSchema(required_columns=("timestamp",), timestamp_column="timestamp")
    dataset = load_csv_text(
        'timestamp\n2026-10-01T10:00:00\nnot-a-time\n2026-10-01T09:00:00\n',
        schema,
    )

    result = validate_dataset(dataset, schema)

    assert [(issue.code, issue.record_number) for issue in result.issues] == [
        ("INVALID_TIMESTAMP", 2),
        ("UNSORTED_TIMESTAMP", 3),
    ]


def test_missing_timestamp_does_not_hide_later_out_of_order_valid_timestamp():
    schema = DataSchema(required_columns=("timestamp",), timestamp_column="timestamp")
    dataset = load_csv_text(
        'timestamp\n2026-10-01T10:00:00\n""\n2026-10-01T09:00:00\n',
        schema,
    )

    result = validate_dataset(dataset, schema)

    assert [(issue.code, issue.record_number) for issue in result.issues] == [
        ("MISSING_VALUE", 2),
        ("UNSORTED_TIMESTAMP", 3),
    ]


def test_invalid_timestamp_does_not_cause_false_order_issue_for_later_time():
    schema = DataSchema(required_columns=("timestamp",), timestamp_column="timestamp")
    dataset = load_csv_text(
        'timestamp\n2026-10-01T10:00:00\nnot-a-time\n2026-10-01T11:00:00\n',
        schema,
    )

    result = validate_dataset(dataset, schema)

    assert [(issue.code, issue.record_number) for issue in result.issues] == [
        ("INVALID_TIMESTAMP", 2)
    ]


@pytest.mark.parametrize("middle", ["not-a-time", '""'])
def test_cadence_does_not_infer_gap_across_invalid_or_missing_timestamp(middle):
    schema = DataSchema(
        required_columns=("timestamp",),
        timestamp_column="timestamp",
        expected_cadence=timedelta(hours=1),
    )
    dataset = load_csv_text(
        "timestamp\n2026-10-01T09:00:00\n"
        + middle
        + "\n2026-10-01T11:00:00\n",
        schema,
    )

    result = validate_dataset(dataset, schema)

    assert "TIMESTAMP_GAP" not in codes(result)


def test_date_only_timestamp_is_parsed_as_naive_midnight():
    schema = DataSchema(required_columns=("timestamp",), timestamp_column="timestamp")
    dataset = load_csv_text(
        "timestamp\n2026-10-01\n2026-10-01T00:00:00\n", schema
    )

    result = validate_dataset(dataset, schema)

    assert [(issue.code, issue.record_number) for issue in result.issues] == [
        ("DUPLICATE_TIMESTAMP", 2)
    ]


def test_schema_rejects_non_ohlc_configuration():
    with pytest.raises(TypeError, match="OHLCColumns instance"):
        DataSchema(required_columns=("Open",), ohlc_columns="Open")


@pytest.mark.parametrize(
    "kwargs, error, message",
    [
        ({"open": ""}, ValueError, "open column name"),
        ({"high": None}, ValueError, "high column name"),
        ({"low": 5}, ValueError, "low column name"),
        ({"close": " "}, ValueError, "close column name"),
        ({"volume": ""}, ValueError, "volume column name"),
        ({"volume": 5}, ValueError, "volume column name"),
    ],
)
def test_schema_rejects_invalid_ohlc_column_names(kwargs, error, message):
    with pytest.raises(error, match=message):
        OHLCColumns(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"minimum_inclusive": 1},
        {"minimum_inclusive": "false"},
        {"maximum_inclusive": 0},
        {"maximum_inclusive": None},
    ],
)
def test_numeric_constraint_requires_boolean_inclusivity_flags(kwargs):
    with pytest.raises(TypeError, match="must be a bool"):
        NumericConstraint(**kwargs)
