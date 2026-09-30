"""Create a per-length analysis from the existing sweep reports."""

import csv
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "reports" / "modulus_sweep.csv"
AGGREGATE_PATH = ROOT / "reports" / "modulus_sweep.md"
OUTPUT_PATH = ROOT / "reports" / "modulus_sweep_by_length.md"

MODULI = range(2, 31)
LENGTHS = range(1, 5)
ERROR_TYPES = ("substitution", "transposition")
CSV_FIELDS = {
    "modulus",
    "length",
    "error_type",
    "original_strings",
    "total_events",
    "detected_events",
    "undetected_events",
    "detection_rate",
    "undetected_rate",
}
AGGREGATE_HEADER = (
    "| Modulus | Error type | Events | Detected | Undetected | Detection rate |"
)
AGGREGATE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(substitution|transposition)\s*\|\s*"
    r"(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*"
    r"(N/A|\d+\.\d{2}%)\s*\|$"
)


def _expected_csv_keys() -> set[tuple[int, int, str]]:
    return {
        (modulus, length, error_type)
        for modulus in MODULI
        for length in LENGTHS
        for error_type in ERROR_TYPES
    }


def load_per_length_csv(path: Path) -> list[dict]:
    """Read and validate all per-length rows from the sweep CSV."""
    rows = []
    seen = set()
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, restkey="_extra", restval=None)
        if reader.fieldnames is None:
            raise ValueError("Sweep CSV is empty or has no header")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Sweep CSV contains duplicate column names")
        missing = CSV_FIELDS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                "Sweep CSV is missing required columns: "
                + ", ".join(sorted(missing))
            )

        for line_number, raw in enumerate(reader, start=2):
            if raw.get("_extra") is not None or any(
                raw.get(field) is None for field in CSV_FIELDS
            ):
                raise ValueError(f"Malformed CSV row at line {line_number}")
            try:
                row = {
                    "modulus": int(raw["modulus"]),
                    "length": int(raw["length"]),
                    "error_type": raw["error_type"],
                    "original_strings": int(raw["original_strings"]),
                    "total_events": int(raw["total_events"]),
                    "detected_events": int(raw["detected_events"]),
                    "undetected_events": int(raw["undetected_events"]),
                    "detection_rate": (
                        None if raw["detection_rate"] == ""
                        else float(raw["detection_rate"])
                    ),
                    "undetected_rate": (
                        None if raw["undetected_rate"] == ""
                        else float(raw["undetected_rate"])
                    ),
                }
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid value in sweep CSV at line {line_number}"
                ) from error

            modulus = row["modulus"]
            length = row["length"]
            error_type = row["error_type"]
            total = row["total_events"]
            detected = row["detected_events"]
            undetected = row["undetected_events"]
            key = (modulus, length, error_type)
            if key in seen:
                raise ValueError(f"Duplicate sweep row for {key}")
            seen.add(key)

            if modulus not in MODULI or length not in LENGTHS:
                raise ValueError(f"Out-of-scope modulus or length at line {line_number}")
            if error_type not in ERROR_TYPES:
                raise ValueError(f"Unknown error type at line {line_number}: {error_type}")
            if row["original_strings"] != 10**length:
                raise ValueError(f"Unexpected original string count for {key}")
            if min(total, detected, undetected) < 0 or detected + undetected != total:
                raise ValueError(f"Inconsistent event counts for {key}")

            if error_type == "substitution":
                expected_total = 9 * length * row["original_strings"]
            elif length == 1:
                expected_total = 0
            else:
                expected_total = 90 * (length - 1) * 10 ** (length - 2)
            if total != expected_total:
                raise ValueError(
                    f"Unexpected total event count for {key}: "
                    f"expected {expected_total}, got {total}"
                )

            expected_detection = detected / total if total else None
            expected_undetected = undetected / total if total else None
            for name, expected in (
                ("detection_rate", expected_detection),
                ("undetected_rate", expected_undetected),
            ):
                actual = row[name]
                if expected is None:
                    if actual is not None:
                        raise ValueError(f"Zero-event rate must be blank for {key}: {name}")
                elif actual is None or not math.isfinite(actual) or not math.isclose(
                    actual, expected, rel_tol=1e-12, abs_tol=1e-15
                ):
                    raise ValueError(f"Incorrect {name} for {key}")
            rows.append(row)

    expected_keys = _expected_csv_keys()
    if seen != expected_keys:
        missing = sorted(expected_keys - seen)
        extra = sorted(seen - expected_keys)
        raise ValueError(
            f"Sweep CSV dimensions are incomplete or unexpected; "
            f"missing={missing[:3]}, extra={extra[:3]}"
        )
    return rows


def load_aggregate_report(path: Path) -> dict[tuple[int, str], dict]:
    """Parse the existing aggregate Markdown table strictly."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    section = "## Aggregate results by modulus"
    if lines.count(section) != 1:
        raise ValueError("Aggregate report must contain exactly one aggregate section")
    start = lines.index(section) + 1
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    section_lines = lines[start:end]
    if section_lines.count(AGGREGATE_HEADER) != 1:
        raise ValueError("Aggregate report table header is missing or ambiguous")
    header_index = section_lines.index(AGGREGATE_HEADER)
    if header_index + 1 >= len(section_lines) or not section_lines[
        header_index + 1
    ].startswith("|---"):
        raise ValueError("Aggregate report table separator is missing")

    result = {}
    for line_number, line in enumerate(section_lines[header_index + 2:], start=1):
        if not line.startswith("|"):
            continue
        match = AGGREGATE_ROW.fullmatch(line)
        if match is None:
            raise ValueError(f"Malformed aggregate table row: {line}")
        modulus = int(match[1])
        error_type = match[2]
        key = (modulus, error_type)
        if key in result:
            raise ValueError(f"Duplicate aggregate row for {key}")
        rate_text = match[6]
        total, detected, undetected = map(int, match.group(3, 4, 5))
        if detected + undetected != total:
            raise ValueError(f"Aggregate event counts do not balance for {key}")
        if total == 0:
            if rate_text != "N/A":
                raise ValueError(f"Zero-event aggregate rate must be N/A for {key}")
            rate = None
        else:
            if rate_text == "N/A":
                raise ValueError(f"Nonzero aggregate rate cannot be N/A for {key}")
            rate = float(rate_text[:-1]) / 100
        result[key] = {
            "total_events": total,
            "detected_events": detected,
            "undetected_events": undetected,
            "detection_rate": rate,
            "rate_text": rate_text,
        }

    expected_keys = {(modulus, kind) for modulus in MODULI for kind in ERROR_TYPES}
    if set(result) != expected_keys:
        raise ValueError(
            "Aggregate report must contain exactly 58 modulus/error-type rows"
        )
    return result


def reconcile_aggregates(rows: list[dict], aggregate: dict[tuple[int, str], dict]) -> None:
    """Require CSV sums to match the existing aggregate table."""
    totals = defaultdict(lambda: [0, 0, 0])
    for row in rows:
        values = totals[(row["modulus"], row["error_type"])]
        values[0] += row["total_events"]
        values[1] += row["detected_events"]
        values[2] += row["undetected_events"]

    for key, (total, detected, undetected) in totals.items():
        if key not in aggregate:
            raise ValueError(f"Aggregate report is missing row for {key}")
        expected = aggregate[key]
        actual_counts = (total, detected, undetected)
        report_counts = (
            expected["total_events"],
            expected["detected_events"],
            expected["undetected_events"],
        )
        if actual_counts != report_counts:
            raise ValueError(
                f"Aggregate counts do not reconcile for {key}: "
                f"CSV={actual_counts}, Markdown={report_counts}"
            )
        actual_rate_text = f"{detected / total:.2%}" if total else "N/A"
        report_rate_text = expected["rate_text"]
        if actual_rate_text != report_rate_text:
            raise ValueError(
                f"Aggregate detection rate does not reconcile for {key}: "
                f"CSV={actual_rate_text}, Markdown={report_rate_text}"
            )


def render_report(rows: list[dict]) -> str:
    """Format the validated CSV rows by error type and string length."""
    lines = [
        "# Per-Length Modular Error-Detection Analysis",
        "",
        "These results reuse `reports/modulus_sweep.csv`; the exhaustive sweep is not rerun.",
        "Events and detection retain the definitions in the sweep: one-position substitutions and unequal adjacent swaps, detected when the residue changes.",
        "Detection rate is detected events divided by total events. Rates are shown to two decimal places; zero-event rates are `N/A`.",
        "Counts pooled across lengths were reconciled against `reports/modulus_sweep.md` before this report was written.",
    ]
    for error_type in ERROR_TYPES:
        lines.extend(["", f"## {error_type.title()}"])
        for length in LENGTHS:
            matching = [
                row for row in rows
                if row["error_type"] == error_type and row["length"] == length
            ]
            lines.extend([
                "",
                f"### String length {length}",
                "",
                "| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |",
                "|---:|---:|---|---:|---:|---:|---:|",
            ])
            for row in sorted(matching, key=lambda item: item["modulus"]):
                rate = (
                    f"{row['detection_rate']:.2%}"
                    if row["detection_rate"] is not None
                    else "N/A"
                )
                lines.append(
                    f"| {row['modulus']} | {length} | {error_type} | "
                    f"{row['total_events']} | {row['detected_events']} | "
                    f"{row['undetected_events']} | {rate} |"
                )
    return "\n".join(lines) + "\n"


def analyze(
    csv_path: Path = CSV_PATH,
    aggregate_path: Path = AGGREGATE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> tuple[list[dict], dict[tuple[int, str], dict]]:
    """Validate inputs, reconcile aggregates, and write a new report."""
    rows = load_per_length_csv(csv_path)
    aggregate = load_aggregate_report(aggregate_path)
    reconcile_aggregates(rows, aggregate)
    Path(output_path).write_text(render_report(rows), encoding="utf-8")
    return rows, aggregate


def main() -> None:
    try:
        rows, aggregate = analyze()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Per-length analysis stopped: {error}") from error
    print(f"Generated: {OUTPUT_PATH}")
    print(f"Per-length result rows: {len(rows)}")
    print(f"Aggregate comparisons passed: {len(aggregate)}")


if __name__ == "__main__":
    main()
