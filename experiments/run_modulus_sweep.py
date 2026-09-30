"""Exhaustively evaluate modular checksum error detection."""

import csv
from itertools import product
from pathlib import Path

from modular_error_detection.errors import (
    adjacent_transpositions,
    single_digit_substitutions,
)

MODULI = range(2, 31)
LENGTHS = range(1, 5)

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
CSV_PATH = REPORTS_DIR / "modulus_sweep.csv"
MD_PATH = REPORTS_DIR / "modulus_sweep.md"

CSV_FIELDS = [
    "modulus",
    "length",
    "error_type",
    "original_strings",
    "total_events",
    "detected_events",
    "undetected_events",
    "detection_rate",
    "undetected_rate",
]


def decimal_strings(length: int):
    """Yield every fixed-width decimal string of the given length."""
    if length < 1:
        raise ValueError("length must be at least 1")

    for digits in product("0123456789", repeat=length):
        yield "".join(digits)


def count_events(length: int, modulus: int, error_type: str) -> dict:
    """Count detected and undetected error events."""
    if error_type not in {"substitution", "transposition"}:
        raise ValueError("unknown error type")

    total = 0
    detected = 0
    original_count = 0

    for original in decimal_strings(length):
        original_count += 1
        original_residue = int(original) % modulus

        if error_type == "substitution":
            altered_strings = single_digit_substitutions(original)
        else:
            altered_strings = adjacent_transpositions(original)

        for altered in altered_strings:
            total += 1

            if int(altered) % modulus != original_residue:
                detected += 1

    undetected = total - detected

    return {
        "modulus": modulus,
        "length": length,
        "error_type": error_type,
        "original_strings": original_count,
        "total_events": total,
        "detected_events": detected,
        "undetected_events": undetected,
        "detection_rate": detected / total if total else "",
        "undetected_rate": undetected / total if total else "",
    }


def run_sweep() -> list[dict]:
    """Run all combinations of modulus, length, and error type."""
    rows = []

    for modulus in MODULI:
        for length in LENGTHS:
            for error_type in ("substitution", "transposition"):
                rows.append(
                    count_events(length, modulus, error_type)
                )

    return rows


def write_csv(rows: list[dict]) -> None:
    """Write results to CSV."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=CSV_FIELDS
        )
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict]) -> None:
    """Write the experiment summary to Markdown."""
    lines = [
        "# Modular Error-Detection Sweep",
        "",
        "## Experiment design",
        "",
        "- Moduli: 2 through 30, inclusive.",
        "- Decimal string lengths: 1 through 4, inclusive.",
        "- Every fixed-width decimal string is enumerated,",
        "  including strings with leading zeros.",
        "- Substitution: change exactly one digit to a",
        "  different decimal digit.",
        "- Transposition: swap unequal adjacent digits;",
        "  identical adjacent pairs are skipped.",
        "- An event is detected when the altered string",
        "  has a different residue modulo the modulus.",
        "- Detection rate = detected events / total events.",
        "- Undetected rate = undetected events / total events.",
        "- Rates are blank when there are no applicable events.",
        "",
        "## Scope and limitations",
        "",
        "These results apply only to the tested string lengths",
        "and error models. They do not establish universal",
        "error-detection guarantees or novelty.",
        "",
        "## Aggregate results by modulus",
        "",
        "| Modulus | Error type | Events | Detected | "
        "Undetected | Detection rate |",
        "|---:|---|---:|---:|---:|---:|",
    ]

    for modulus in MODULI:
        for error_type in ("substitution", "transposition"):
            matching = [
                row
                for row in rows
                if row["modulus"] == modulus
                and row["error_type"] == error_type
            ]

            total = sum(
                row["total_events"] for row in matching
            )
            detected = sum(
                row["detected_events"] for row in matching
            )
            undetected = total - detected

            if total:
                rate = f"{detected / total:.2%}"
            else:
                rate = "N/A"

            lines.append(
                f"| {modulus} | {error_type} | {total} | "
                f"{detected} | {undetected} | {rate} |"
            )

    MD_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    """Run the sweep and write both reports."""
    rows = run_sweep()
    write_csv(rows)
    write_markdown(rows)

    print(f"Generated: {CSV_PATH}")
    print(f"Generated: {MD_PATH}")
    print(f"Result rows: {len(rows)}")


if __name__ == "__main__":
    main()