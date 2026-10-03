import json

import pytest

from financial_data_workbench import (
    Severity,
    ValidationIssue,
    ValidationResult,
    build_report_data,
    load_csv_text,
    render_json_report,
    render_markdown_report,
    validate_dataset,
)
from financial_data_workbench.schema import DataSchema


def test_empty_result_renders_zero_counts_and_no_issues():
    result = ValidationResult(records_checked=0, issues=())

    data = build_report_data(result)
    markdown = render_markdown_report(result)
    json_text = render_json_report(result)

    assert data["records_checked"] == 0
    assert data["total_issues"] == 0
    assert data["issues_by_severity"] == {"error": 0, "warning": 0}
    assert data["issues_by_code"] == {}
    assert data["issues"] == []
    assert "No validation issues." in markdown
    assert "Total issues: 0" in markdown
    assert json.loads(json_text) == data


def test_report_includes_summary_counts_and_complete_issue_details():
    issues = (
        ValidationIssue(
            code="INVALID_TYPE",
            severity=Severity.ERROR,
            message="Close must be a decimal.",
            record_number=2,
            line_number=3,
            column="Close",
        ),
        ValidationIssue(
            code="TIMESTAMP_GAP",
            severity=Severity.WARNING,
            message="Unexpected interval.",
            record_number=4,
            line_number=5,
            column="timestamp",
        ),
    )
    result = ValidationResult(records_checked=4, issues=issues)

    data = build_report_data(result)

    assert data["records_checked"] == 4
    assert data["total_issues"] == 2
    assert data["issues_by_severity"] == {"error": 1, "warning": 1}
    assert data["issues_by_code"] == {"INVALID_TYPE": 1, "TIMESTAMP_GAP": 1}
    assert data["issues"][0] == {
        "code": "INVALID_TYPE",
        "severity": "error",
        "message": "Close must be a decimal.",
        "record_number": 2,
        "line_number": 3,
        "column": "Close",
    }


def test_optional_source_label_is_included_only_when_supplied():
    result = ValidationResult(records_checked=0, issues=())

    assert "source_label" not in build_report_data(result)
    assert build_report_data(result, "sample.csv")["source_label"] == "sample.csv"
    assert "Source: sample.csv" in render_markdown_report(result, "sample.csv")
    assert json.loads(render_json_report(result, "sample.csv"))["source_label"] == "sample.csv"


def test_missing_issue_location_fields_are_json_null_and_markdown_placeholders():
    result = ValidationResult(
        records_checked=1,
        issues=(ValidationIssue("DATASET_WARNING", Severity.WARNING, "General finding"),),
    )

    data = json.loads(render_json_report(result))
    markdown = render_markdown_report(result)

    issue = data["issues"][0]
    assert issue["record_number"] is None
    assert issue["line_number"] is None
    assert issue["column"] is None
    assert "| DATASET\\_WARNING | warning | General finding | N/A | N/A | N/A |" in markdown


def test_markdown_escapes_table_and_inline_markup_without_changing_json_values():
    label = "feed|one\n*raw*"
    message = "bad|value\n_next_ <tag> & `code`"
    result = ValidationResult(
        records_checked=1,
        issues=(ValidationIssue("BAD|VALUE", Severity.ERROR, message, 1, 2, "column|name"),),
    )

    markdown = render_markdown_report(result, label)
    data = json.loads(render_json_report(result, label))

    assert "feed\\|one<br>\\*raw\\*" in markdown
    assert "bad\\|value<br>\\_next\\_ &lt;tag&gt; &amp; \\`code\\`" in markdown
    assert data["source_label"] == label
    assert data["issues"][0]["message"] == message
    assert data["issues"][0]["code"] == "BAD|VALUE"
    assert data["issues"][0]["column"] == "column|name"


def test_json_is_valid_compatible_with_mapping_proxies_and_enum_severity():
    schema = DataSchema(required_columns=("price",), column_types={"price": int})
    dataset = load_csv_text("price\nnot-an-integer\n", schema)
    result = validate_dataset(dataset, schema)

    parsed = json.loads(render_json_report(result))

    assert parsed["issues_by_severity"] == {"error": 1, "warning": 0}
    assert parsed["issues"][0]["severity"] == "error"
    assert isinstance(render_json_report(result), str)


def test_json_output_is_deterministic_and_ends_with_one_newline():
    result = ValidationResult(
        records_checked=1,
        issues=(ValidationIssue("X", Severity.ERROR, "message", 1, 2, "column"),),
    )

    first = render_json_report(result, "source.csv")
    second = render_json_report(result, "source.csv")

    assert first == second
    assert first.endswith("\n")
    assert not first.endswith("\n\n")


def test_rendering_does_not_mutate_result_or_loaded_dataset():
    schema = DataSchema(required_columns=("price",), column_types={"price": int})
    dataset = load_csv_text("price\nnot-an-integer\n", schema)
    values_before = tuple(dict(record.values) for record in dataset.records)
    result = validate_dataset(dataset, schema)
    issues_before = result.issues
    summary_before = dict(result.summary.issues_by_code)

    build_report_data(result, "source.csv")
    render_markdown_report(result, "source.csv")
    render_json_report(result, "source.csv")

    assert result.issues == issues_before
    assert dict(result.summary.issues_by_code) == summary_before
    assert tuple(dict(record.values) for record in dataset.records) == values_before


@pytest.mark.parametrize("renderer", [build_report_data, render_markdown_report, render_json_report])
def test_reporting_requires_a_validation_result(renderer):
    with pytest.raises(TypeError, match="ValidationResult"):
        renderer(object())
