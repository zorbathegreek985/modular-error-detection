import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from financial_data_workbench.cli import main


HEADER = "timestamp,Open,High,Low,Close,Volume\n"
VALID_ROW = "2025-01-02T09:00:00,10.00,12.00,9.00,11.00,100\n"
INVALID_ROW = "2025-01-02T09:00:00,10.00,9.00,9.50,11.00,-5\n"


def test_valid_csv_markdown_stdout_and_success_exit(tmp_path, capsys):
    source = tmp_path / "market.csv"
    source.write_text(HEADER + VALID_ROW, encoding="utf-8")

    code = main([str(source)])

    captured = capsys.readouterr()
    assert code == 0
    assert "Financial Data Validation Report" in captured.out
    assert "Checked 1 records; 0 issue(s)" in captured.err


def test_invalid_csv_reports_json_and_data_issue_exit(tmp_path, capsys):
    source = tmp_path / "market.csv"
    source.write_text(HEADER + INVALID_ROW, encoding="utf-8")

    code = main([str(source), "--format", "json"])

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert code == 1
    assert report["total_issues"] > 0
    assert "issue(s)" in captured.err
    assert "-5" not in captured.out + captured.err


@pytest.mark.parametrize("format_name, expected", [("markdown", "# Financial Data"), ("json", '"records_checked": 1')])
def test_output_file_written_in_selected_format(tmp_path, format_name, expected):
    source = tmp_path / "input.csv"
    output = tmp_path / f"report.{format_name}"
    source.write_text(HEADER + VALID_ROW, encoding="utf-8")

    assert main([str(source), "--format", format_name, "--output", str(output)]) == 0
    assert expected in output.read_text(encoding="utf-8")


def test_missing_input_returns_execution_error_without_echoing_path(tmp_path, capsys):
    missing = tmp_path / "secret-market.csv"

    code = main([str(missing)])

    captured = capsys.readouterr()
    assert code == 2
    assert "could not be loaded" in captured.err
    assert "secret-market" not in captured.err


@pytest.mark.parametrize("arguments", [["missing.csv", "--schema", "other"], ["missing.csv", "--format", "xml"]])
def test_invalid_schema_or_format_is_rejected_by_argparse(arguments, capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(arguments)

    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_output_write_failure_returns_execution_error(tmp_path, capsys):
    source = tmp_path / "input.csv"
    source.write_text(HEADER + VALID_ROW, encoding="utf-8")
    output = tmp_path / "missing-parent" / "report.md"

    assert main([str(source), "--output", str(output)]) == 2
    assert "report could not be written" in capsys.readouterr().err


def test_input_output_collision_is_rejected_without_overwrite(tmp_path, capsys):
    source = tmp_path / "input.csv"
    original = HEADER + VALID_ROW
    source.write_text(original, encoding="utf-8")

    code = main([str(source), "--output", str(source)])

    assert code == 2
    assert source.read_text(encoding="utf-8") == original
    assert "must not be the input" in capsys.readouterr().err


def test_invalid_cell_values_are_not_exposed_in_terminal_summary(tmp_path, capsys):
    source = tmp_path / "input.csv"
    source.write_text(HEADER + "2025-01-02T09:00:00,secret,12,9,11,100\n", encoding="utf-8")

    code = main([str(source)])

    captured = capsys.readouterr()
    assert code == 1
    assert "secret" not in captured.out + captured.err
    assert "issue(s)" in captured.err


def test_invalid_timestamp_value_is_not_exposed_in_stdout_report(tmp_path, capsys):
    source = tmp_path / "input.csv"
    secret_timestamp = "private-timestamp-token"
    source.write_text(HEADER + f"{secret_timestamp},10,12,9,11,100\n", encoding="utf-8")

    code = main([str(source), "--format", "json"])

    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert code == 1
    assert report["issues"][0]["code"] == "INVALID_TIMESTAMP"
    assert secret_timestamp not in captured.out + captured.err


@pytest.mark.parametrize(
    ("field", "sentinel", "expected_code"),
    [
        ("timestamp", "TS_SENTINEL_79f1", "INVALID_TIMESTAMP"),
        ("Open", "OHLC_SENTINEL_28c4", "INVALID_OHLC_NUMBER"),
        ("Volume", "VOLUME_SENTINEL_63a8", "INVALID_NUMERIC"),
    ],
)
@pytest.mark.parametrize("format_name", ["markdown", "json"])
@pytest.mark.parametrize("write_to_file", [False, True])
def test_source_values_never_leak_into_cli_reports_or_terminal(
    tmp_path, capsys, field, sentinel, expected_code, format_name, write_to_file
):
    source = tmp_path / "input.csv"
    values = {
        "timestamp": "2025-01-02T09:00:00",
        "Open": "10.00",
        "High": "12.00",
        "Low": "9.00",
        "Close": "11.00",
        "Volume": "100",
    }
    values[field] = sentinel
    source.write_text(HEADER + ",".join(values[column] for column in (
        "timestamp", "Open", "High", "Low", "Close", "Volume"
    )) + "\n", encoding="utf-8")
    output = tmp_path / f"report.{format_name}" if write_to_file else None
    arguments = [str(source), "--format", format_name]
    if output is not None:
        arguments.extend(["--output", str(output)])

    code = main(arguments)

    captured = capsys.readouterr()
    report_text = output.read_text(encoding="utf-8") if output is not None else captured.out
    assert code == 1
    assert sentinel not in report_text
    assert sentinel not in captured.out + captured.err
    if format_name == "json":
        report = json.loads(report_text)
        assert any(issue["code"] == expected_code for issue in report["issues"])
        assert report["total_issues"] > 0
    else:
        assert expected_code.replace("_", r"\_") in report_text
        assert "| Code | Severity | Message |" in report_text
    assert "issue(s)" in captured.out + captured.err


def test_module_entry_point_executes_cli(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text(HEADER + VALID_ROW, encoding="utf-8")
    environment = os.environ.copy()
    project_root = str(Path(__file__).resolve().parents[1])
    package_root = os.path.join(project_root, "python")
    environment["PYTHONPATH"] = package_root + os.pathsep + environment.get("PYTHONPATH", "")

    completed = subprocess.run(
        [sys.executable, "-m", "financial_data_workbench", str(source)],
        cwd=project_root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert "Financial Data Validation Report" in completed.stdout
