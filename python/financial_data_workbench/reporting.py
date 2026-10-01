"""Deterministic renderers for financial validation findings.

Reports are snapshots of a ``ValidationResult``. They are not authenticated
audit logs and do not establish that financial data is correct.
"""

import html
import json
import re
from typing import Any

from .results import ValidationResult


def _report_data(
    result: ValidationResult, source_label: str | None
) -> dict[str, Any]:
    if not isinstance(result, ValidationResult):
        raise TypeError("result must be a ValidationResult")
    if source_label is not None and not isinstance(source_label, str):
        raise TypeError("source_label must be a string or None")

    summary = result.summary
    data: dict[str, Any] = {
        "records_checked": summary.records_checked,
        "total_issues": summary.total_issues,
        "issues_by_severity": dict(summary.issues_by_severity),
        "issues_by_code": dict(summary.issues_by_code),
        "issues": [
            {
                "code": issue.code,
                "severity": issue.severity.value,
                "message": issue.message,
                "record_number": issue.record_number,
                "line_number": issue.line_number,
                "column": issue.column,
            }
            for issue in result.issues
        ],
    }
    if source_label is not None:
        data["source_label"] = source_label
    return data


def build_report_data(
    result: ValidationResult, source_label: str | None = None
) -> dict[str, Any]:
    """Build a JSON-compatible snapshot without changing the result."""
    return _report_data(result, source_label)


def _markdown_cell(value: object) -> str:
    """Escape untrusted text for a Markdown table cell."""
    text = html.escape(str(value), quote=True)
    text = text.replace("\\", "\\\\").replace("|", r"\|")
    text = re.sub(r"([*_`~\[\]])", r"\\\1", text)
    return text.replace("\r\n", "<br>").replace("\r", "<br>").replace("\n", "<br>")


def render_markdown_report(
    result: ValidationResult, source_label: str | None = None
) -> str:
    """Render a readable Markdown snapshot of a validation result."""
    data = _report_data(result, source_label)
    lines = ["# Financial Data Validation Report", ""]
    if "source_label" in data:
        lines.extend([f"Source: {_markdown_cell(data['source_label'])}", ""])

    lines.extend(
        [
            "## Summary",
            "",
            f"- Records checked: {data['records_checked']}",
            f"- Total issues: {data['total_issues']}",
            "",
            "### Issues by severity",
            "",
            "| Severity | Count |",
            "|---|---:|",
        ]
    )
    for severity, count in data["issues_by_severity"].items():
        lines.append(f"| {_markdown_cell(severity)} | {count} |")

    lines.extend(["", "### Issues by code", "", "| Issue code | Count |", "|---|---:|"])
    if data["issues_by_code"]:
        for code, count in data["issues_by_code"].items():
            lines.append(f"| {_markdown_cell(code)} | {count} |")
    else:
        lines.append("| None | 0 |")

    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| Code | Severity | Message | Data record | Physical line | Column |",
            "|---|---|---|---:|---:|---|",
        ]
    )
    if data["issues"]:
        for issue in data["issues"]:
            fields = (
                issue["code"],
                issue["severity"],
                issue["message"],
                issue["record_number"],
                issue["line_number"],
                issue["column"],
            )
            lines.append(
                "| " + " | ".join(
                    _markdown_cell(value) if value is not None else "N/A"
                    for value in fields
                ) + " |"
            )
    else:
        lines.append("| None | N/A | No validation issues. | N/A | N/A | N/A |")

    lines.extend(
        [
            "",
            "This report is a snapshot of validation findings, not an authenticated audit log or proof of financial correctness.",
            "",
        ]
    )
    return "\n".join(lines)


def render_json_report(
    result: ValidationResult, source_label: str | None = None
) -> str:
    """Render deterministic, standard-library JSON with one final newline."""
    return json.dumps(
        _report_data(result, source_label),
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
    ) + "\n"
