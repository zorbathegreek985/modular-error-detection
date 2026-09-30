import csv

import pytest

from modular_error_detection.visualizations import (
    aggregate_detection_rates,
    write_detection_plot,
)


FIELDS = [
    "modulus",
    "length",
    "error_type",
    "total_events",
    "detected_events",
    "detection_rate",
]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_aggregate_detection_rates_are_event_weighted(tmp_path):
    path = tmp_path / "sweep.csv"
    write_csv(
        path,
        [
            {"modulus": 11, "length": 1, "error_type": "substitution", "total_events": 90, "detected_events": 90, "detection_rate": "1.0"},
            {"modulus": 11, "length": 2, "error_type": "substitution", "total_events": 1800, "detected_events": 900, "detection_rate": "0.5"},
            {"modulus": 11, "length": 1, "error_type": "transposition", "total_events": 0, "detected_events": 0, "detection_rate": ""},
            {"modulus": 11, "length": 2, "error_type": "transposition", "total_events": 90, "detected_events": 90, "detection_rate": "1.0"},
        ],
    )

    assert aggregate_detection_rates(path, "substitution") == [(11, 990 / 1890)]
    assert aggregate_detection_rates(path, "transposition") == [(11, 1.0)]


def test_aggregate_rate_is_none_when_all_events_are_blank(tmp_path):
    path = tmp_path / "sweep.csv"
    write_csv(
        path,
        [{"modulus": 3, "length": 1, "error_type": "transposition", "total_events": 0, "detected_events": 0, "detection_rate": ""}],
    )

    assert aggregate_detection_rates(path, "transposition") == [(3, None)]


def test_plot_omits_none_rate_instead_of_plotting_zero(tmp_path):
    path = tmp_path / "sweep.csv"
    output = tmp_path / "plot.svg"
    write_csv(
        path,
        [{"modulus": 3, "length": 1, "error_type": "transposition", "total_events": 0, "detected_events": 0, "detection_rate": ""}],
    )

    write_detection_plot(path, output, "transposition")
    svg = output.read_text(encoding="utf-8")
    assert "N/A values omitted" in svg
    assert "<circle" not in svg


def test_unknown_error_type_rejected(tmp_path):
    with pytest.raises(ValueError, match="unknown error type"):
        aggregate_detection_rates(tmp_path / "missing.csv", "other")
