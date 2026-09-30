"""Deterministic result types shared by dataset validators and callers."""

from collections import Counter
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    """One validation finding.

    Record numbers are 1-based among data records and exclude the header.
    Physical line numbers refer to the final CSV line of a record, which may
    differ when a quoted field spans multiple lines.
    """

    code: str
    severity: Severity
    message: str
    record_number: int | None = None
    line_number: int | None = None
    column: str | None = None


@dataclass(frozen=True)
class ValidationSummary:
    records_checked: int
    total_issues: int
    issues_by_severity: dict[str, int]
    issues_by_code: dict[str, int]


@dataclass(frozen=True)
class ValidationResult:
    records_checked: int
    issues: tuple[ValidationIssue, ...]

    @property
    def summary(self) -> ValidationSummary:
        severity_counts = Counter(issue.severity.value for issue in self.issues)
        code_counts = Counter(issue.code for issue in self.issues)
        return ValidationSummary(
            records_checked=self.records_checked,
            total_issues=len(self.issues),
            issues_by_severity={
                severity.value: severity_counts[severity.value]
                for severity in Severity
            },
            issues_by_code={key: code_counts[key] for key in sorted(code_counts)},
        )
