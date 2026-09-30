import csv
from fractions import Fraction

import pytest

from experiments.validate_analytical_counts import (
    AGGREGATE_PATH,
    CSV_PATH,
    analytical_counts,
    display_rate,
    load_aggregate_markdown,
    load_sweep_csv,
    pair_weight,
    render_report,
    validate_against_reports,
)


def test_pair_weights_for_hand_calculated_divisors():
    assert pair_weight(1) == 90
    assert pair_weight(2) == 40
    assert pair_weight(3) == 24
    assert pair_weight(9) == 2
    assert pair_weight(10) == 0


def test_two_digit_substitution_counts_modulo_two():
    result = analytical_counts(2, 2, "substitution")

    assert result["total_events"] == 1800
    assert result["undetected_events"] == 1300
    assert result["detected_events"] == 500
    assert result["detection_rate"] == Fraction(5, 18)


@pytest.mark.parametrize(
    ("modulus", "undetected", "detected", "rate"),
    [
        (3, 24, 66, Fraction(11, 15)),
        (9, 2, 88, Fraction(44, 45)),
    ],
)
def test_length_one_substitution_rates(modulus, undetected, detected, rate):
    result = analytical_counts(modulus, 1, "substitution")

    assert result["total_events"] == 90
    assert result["undetected_events"] == undetected
    assert result["detected_events"] == detected
    assert result["detection_rate"] == rate


@pytest.mark.parametrize("modulus", [3, 9])
def test_moduli_three_and_nine_miss_all_unequal_transpositions(modulus):
    result = analytical_counts(modulus, 4, "transposition")

    assert result["total_events"] == 27000
    assert result["undetected_events"] == 27000
    assert result["detected_events"] == 0
    assert result["detection_rate"] == 0


def test_length_one_transposition_has_no_rate():
    result = analytical_counts(11, 1, "transposition")

    assert result == {
        "total_events": 0,
        "detected_events": 0,
        "undetected_events": 0,
        "detection_rate": None,
    }
    assert display_rate(0, 0) == "N/A"


def test_modulus_eleven_detects_both_error_types_for_arbitrary_tested_lengths():
    for length in range(1, 21):
        for error_type in ("substitution", "transposition"):
            result = analytical_counts(11, length, error_type)
            assert result["undetected_events"] == 0
            if result["total_events"]:
                assert result["detected_events"] == result["total_events"]
                assert result["detection_rate"] == 1


@pytest.mark.parametrize("modulus", [0, 1, -2, 2.5, True])
def test_invalid_modulus_rejected(modulus):
    with pytest.raises((TypeError, ValueError)):
        analytical_counts(modulus, 1, "substitution")


@pytest.mark.parametrize("length", [0, -1, 1.5, True])
def test_invalid_length_rejected(length):
    with pytest.raises((TypeError, ValueError)):
        analytical_counts(11, length, "substitution")


def test_unknown_error_type_rejected():
    with pytest.raises(ValueError, match="unknown error type"):
        analytical_counts(11, 2, "insertion")


@pytest.mark.parametrize(("detected", "total", "expected"), [(1, 32, "3.12%"), (3, 32, "9.38%")])
def test_percentage_format_uses_half_even_at_boundaries(detected, total, expected):
    assert display_rate(detected, total) == expected


def test_analytical_counts_match_all_existing_reports():
    rows, aggregate = validate_against_reports(CSV_PATH, AGGREGATE_PATH)

    assert len(rows) == 232
    assert len(aggregate) == 58


def copy_csv_with_mutation(tmp_path, mutate):
    with CSV_PATH.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames
        rows = list(reader)
    mutate(rows, fields)
    path = tmp_path / "sweep.csv"
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_missing_csv_row_is_rejected(tmp_path):
    path = copy_csv_with_mutation(tmp_path, lambda rows, _: rows.pop())

    with pytest.raises(ValueError, match="dimensions do not match"):
        load_sweep_csv(path)


def test_duplicate_csv_key_is_rejected(tmp_path):
    path = copy_csv_with_mutation(tmp_path, lambda rows, _: rows.append(rows[0].copy()))

    with pytest.raises(ValueError, match="Duplicate sweep CSV row"):
        load_sweep_csv(path)


def test_malformed_csv_value_is_rejected(tmp_path):
    def mutate(rows, _):
        rows[0]["detected_events"] = "not-an-integer"

    path = copy_csv_with_mutation(tmp_path, mutate)
    with pytest.raises(ValueError, match="Malformed integer field"):
        load_sweep_csv(path)


def test_missing_required_csv_column_is_rejected(tmp_path):
    def mutate(rows, fields):
        fields.remove("undetected_rate")
        for row in rows:
            row.pop("undetected_rate")

    path = copy_csv_with_mutation(tmp_path, mutate)

    with pytest.raises(ValueError, match="missing required columns: undetected_rate"):
        load_sweep_csv(path)


def test_inconsistent_csv_event_partition_is_rejected(tmp_path):
    def mutate(rows, _):
        rows[0]["detected_events"] = str(int(rows[0]["detected_events"]) + 1)

    path = copy_csv_with_mutation(tmp_path, mutate)

    with pytest.raises(ValueError, match="Analytical detected_events mismatch"):
        load_sweep_csv(path)


def test_inconsistent_csv_rate_is_rejected(tmp_path):
    def mutate(rows, _):
        rows[0]["detection_rate"] = "0.1"

    path = copy_csv_with_mutation(tmp_path, mutate)

    with pytest.raises(ValueError, match="Two-decimal detection_rate mismatch"):
        load_sweep_csv(path)


def test_aggregate_markdown_mismatch_is_rejected(tmp_path):
    content = AGGREGATE_PATH.read_text(encoding="utf-8")
    old = "| 2 | substitution | 388890 | 55550 | 333340 | 14.28% |"
    new = "| 2 | substitution | 388890 | 55551 | 333339 | 14.28% |"
    assert old in content
    path = tmp_path / "aggregate.md"
    path.write_text(content.replace(old, new, 1), encoding="utf-8")

    load_aggregate_markdown(path)
    with pytest.raises(ValueError, match="Aggregate counts do not reconcile"):
        validate_against_reports(CSV_PATH, path)


def test_duplicate_aggregate_row_is_rejected(tmp_path):
    content = AGGREGATE_PATH.read_text(encoding="utf-8")
    row = "| 2 | substitution | 388890 | 55550 | 333340 | 14.28% |"
    path = tmp_path / "aggregate.md"
    path.write_text(content.replace(row, row + "\n" + row, 1), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate aggregate Markdown row"):
        load_aggregate_markdown(path)


def test_malformed_aggregate_row_is_rejected(tmp_path):
    content = AGGREGATE_PATH.read_text(encoding="utf-8")
    old = "| 2 | substitution | 388890 | 55550 | 333340 | 14.28% |"
    malformed = "| 2 | substitution | not-a-count | 55550 | 333340 | 14.28% |"
    assert old in content
    path = tmp_path / "aggregate.md"
    path.write_text(content.replace(old, malformed, 1), encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed aggregate Markdown row"):
        load_aggregate_markdown(path)


def test_missing_aggregate_row_is_rejected(tmp_path):
    content = AGGREGATE_PATH.read_text(encoding="utf-8")
    row = "| 2 | substitution | 388890 | 55550 | 333340 | 14.28% |"
    assert row in content
    path = tmp_path / "aggregate.md"
    path.write_text(content.replace(row + "\n", "", 1), encoding="utf-8")

    with pytest.raises(ValueError, match="exactly 58 expected rows"):
        validate_against_reports(CSV_PATH, path)


def test_rendered_report_contains_formulas_results_and_zero_event_rate():
    rows = load_sweep_csv(CSV_PATH)
    report = render_report(rows)

    assert "Δs = d·10^k" in report
    assert "Δt =" in report
    assert "W(3)=24" in report
    assert "W(9)=2" in report
    assert "Modulus 11" in report
    assert "For `n = 1`, `T_t = U_t = 0`, and the detection rate is N/A." in report
    assert "all 232 per-length CSV rows" in report
    assert "all 58 rows" in report
