import csv

import pytest

from experiments.analyze_per_length import (
    AGGREGATE_HEADER,
    CSV_FIELDS,
    ERROR_TYPES,
    LENGTHS,
    MODULI,
    load_aggregate_report,
    load_per_length_csv,
    reconcile_aggregates,
    render_report,
)


def make_rows(detection_fraction=0.5):
    rows = []
    for modulus in MODULI:
        for length in LENGTHS:
            for error_type in ERROR_TYPES:
                original_strings = 10**length
                if error_type == "substitution":
                    total = 9 * length * original_strings
                elif length == 1:
                    total = 0
                else:
                    total = 90 * (length - 1) * 10 ** (length - 2)
                detected = int(total * detection_fraction)
                undetected = total - detected
                rows.append({
                    "modulus": modulus,
                    "length": length,
                    "error_type": error_type,
                    "original_strings": original_strings,
                    "total_events": total,
                    "detected_events": detected,
                    "undetected_events": undetected,
                    "detection_rate": detected / total if total else None,
                    "undetected_rate": undetected / total if total else None,
                })
    return rows


def write_csv(path, rows, fields=None):
    fields = fields or list(CSV_FIELDS)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                **row,
                "detection_rate": (
                    "" if row.get("detection_rate") is None
                    else row["detection_rate"]
                ),
                "undetected_rate": (
                    "" if row.get("undetected_rate") is None
                    else row["undetected_rate"]
                ),
            })


def aggregate_text(rows, count_override=None, rate_override=None):
    lines = [
        "# Existing sweep report",
        "",
        "## Aggregate results by modulus",
        "",
        AGGREGATE_HEADER,
        "|---:|---|---:|---:|---:|---:|",
    ]
    for modulus in MODULI:
        for error_type in ERROR_TYPES:
            matching = [
                row for row in rows
                if row["modulus"] == modulus and row["error_type"] == error_type
            ]
            total = sum(row["total_events"] for row in matching)
            detected = sum(row["detected_events"] for row in matching)
            undetected = sum(row["undetected_events"] for row in matching)
            if count_override == (modulus, error_type):
                detected += 1
                undetected -= 1
            if rate_override == (modulus, error_type):
                rate = "99.99%"
            else:
                rate = f"{detected / total:.2%}" if total else "N/A"
            lines.append(
                f"| {modulus} | {error_type} | {total} | {detected} | "
                f"{undetected} | {rate} |"
            )
    return "\n".join(lines) + "\n"


def write_aggregate(path, rows, **kwargs):
    path.write_text(aggregate_text(rows, **kwargs), encoding="utf-8")


def test_load_valid_csv_preserves_per_length_counts(tmp_path):
    path = tmp_path / "sweep.csv"
    expected = make_rows()
    write_csv(path, expected)

    actual = load_per_length_csv(path)

    assert len(actual) == 232
    row = next(
        row for row in actual
        if (row["modulus"], row["length"], row["error_type"])
        == (11, 3, "substitution")
    )
    assert row["total_events"] == 27000
    assert row["detected_events"] == 13500
    assert row["undetected_events"] == 13500
    assert row["detection_rate"] == 0.5


def test_rejects_missing_required_column(tmp_path):
    path = tmp_path / "sweep.csv"
    write_csv(path, [], fields=sorted(CSV_FIELDS - {"undetected_rate"}))

    with pytest.raises(ValueError, match="missing required columns"):
        load_per_length_csv(path)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda row: row.update(modulus="not-a-number"), "Invalid value"),
        (lambda row: row.update(undetected_events=0), "Inconsistent event counts"),
        (lambda row: row.update(detection_rate="0.25"), "Incorrect detection_rate"),
        (lambda row: row.update(total_events=91, undetected_events=46), "Unexpected total event count"),
    ],
)
def test_rejects_malformed_or_inconsistent_csv(tmp_path, change, message):
    path = tmp_path / "sweep.csv"
    rows = make_rows()
    change(rows[0])
    write_csv(path, rows)

    with pytest.raises(ValueError, match=message):
        load_per_length_csv(path)


def test_rejects_missing_per_length_row(tmp_path):
    path = tmp_path / "sweep.csv"
    rows = make_rows()
    write_csv(path, rows[:-1])

    with pytest.raises(ValueError, match="dimensions are incomplete"):
        load_per_length_csv(path)


def test_zero_event_transposition_is_rendered_as_na(tmp_path):
    path = tmp_path / "sweep.csv"
    rows = make_rows()
    write_csv(path, rows)
    loaded = load_per_length_csv(path)

    row = next(
        row for row in loaded
        if row["length"] == 1 and row["error_type"] == "transposition"
    )
    assert row["total_events"] == 0
    assert row["detection_rate"] is None
    report = render_report(loaded)
    length_one = report.split("### String length 1", 2)[2].split("### String length 2", 1)[0]
    assert "| 2 | 1 | transposition | 0 | 0 | 0 | N/A |" in length_one
    assert "| 2 | 1 | transposition | 0 | 0 | 0 | 0.00% |" not in report


def test_aggregate_counts_reconcile_exactly(tmp_path):
    rows = make_rows()
    csv_path = tmp_path / "sweep.csv"
    report_path = tmp_path / "aggregate.md"
    write_csv(csv_path, rows)
    write_aggregate(report_path, rows)

    parsed_rows = load_per_length_csv(csv_path)
    aggregate = load_aggregate_report(report_path)
    reconcile_aggregates(parsed_rows, aggregate)
    assert len(aggregate) == 58


def test_reconciliation_respects_two_decimal_rate_rounding(tmp_path):
    rows = make_rows(detection_fraction=1 / 3)
    csv_path = tmp_path / "sweep.csv"
    report_path = tmp_path / "aggregate.md"
    write_csv(csv_path, rows)
    write_aggregate(report_path, rows)

    reconcile_aggregates(
        load_per_length_csv(csv_path), load_aggregate_report(report_path)
    )


@pytest.mark.parametrize("override", ["counts", "rate"])
def test_reconciliation_rejects_aggregate_mismatch(tmp_path, override):
    rows = make_rows()
    report_path = tmp_path / "aggregate.md"
    options = (
        {"count_override": (2, "substitution")}
        if override == "counts"
        else {"rate_override": (2, "substitution")}
    )
    write_aggregate(report_path, rows, **options)
    aggregate = load_aggregate_report(report_path)

    with pytest.raises(
        ValueError,
        match="Aggregate (counts do not|detection rate does not) reconcile",
    ):
        reconcile_aggregates(rows, aggregate)


def test_aggregate_parser_rejects_malformed_table_row(tmp_path):
    path = tmp_path / "aggregate.md"
    content = aggregate_text(make_rows()).replace(
        "| 2 | substitution |", "| two | substitution |", 1
    )
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed aggregate table row"):
        load_aggregate_report(path)


def test_aggregate_parser_requires_two_decimal_rate_precision(tmp_path):
    path = tmp_path / "aggregate.md"
    content = aggregate_text(make_rows()).replace("50.00%", "50.0%", 1)
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed aggregate table row"):
        load_aggregate_report(path)
