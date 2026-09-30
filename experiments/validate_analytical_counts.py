"""Validate sweep results against exact analytical event counts."""

import csv
import math
import re
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "reports" / "modulus_sweep.csv"
AGGREGATE_PATH = ROOT / "reports" / "modulus_sweep.md"
OUTPUT_PATH = ROOT / "reports" / "modulus_characterization.md"

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


def _validate_modulus(modulus: int) -> None:
    if isinstance(modulus, bool) or not isinstance(modulus, int):
        raise TypeError("modulus must be an integer (not bool)")
    if modulus <= 1:
        raise ValueError("modulus must be greater than 1")


def _validate_length(length: int) -> None:
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("length must be an integer (not bool)")
    if length < 1:
        raise ValueError("length must be at least 1")


def pair_weight(divisor: int) -> int:
    """Count ordered unequal digit pairs whose difference is divisible by h."""
    if isinstance(divisor, bool) or not isinstance(divisor, int):
        raise TypeError("divisor must be an integer (not bool)")
    if divisor <= 0:
        raise ValueError("divisor must be positive")
    limit = 9 // divisor
    return 2 * sum(10 - divisor * j for j in range(1, limit + 1))


def display_rate(detected: int, total: int) -> str:
    """Format a rate to two percentage decimals using exact half-even rounding."""
    if total == 0:
        if detected != 0:
            raise ValueError("detected events cannot be nonzero when total is zero")
        return "N/A"
    if total < 0 or detected < 0 or detected > total:
        raise ValueError("event counts must satisfy 0 <= detected <= total")
    hundredths, remainder = divmod(detected * 10_000, total)
    doubled = 2 * remainder
    if doubled > total or (doubled == total and hundredths % 2):
        hundredths += 1
    return f"{hundredths // 100}.{hundredths % 100:02d}%"


def display_decimal_rate(rate: Decimal) -> str:
    """Format a validated decimal rate like the reports' percentage fields."""
    percentage = (rate * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    return f"{percentage:.2f}%"


def analytical_counts(modulus: int, length: int, error_type: str) -> dict:
    """Return exact total, undetected, detected, and rate values for a row."""
    _validate_modulus(modulus)
    _validate_length(length)
    if error_type not in ERROR_TYPES:
        raise ValueError(f"unknown error type: {error_type}")

    if error_type == "substitution":
        total = 90 * length * 10 ** (length - 1)
        undetected = 10 ** (length - 1) * sum(
            pair_weight(modulus // math.gcd(modulus, 10**k))
            for k in range(length)
        )
    elif length == 1:
        total = undetected = 0
    else:
        total = 90 * (length - 1) * 10 ** (length - 2)
        undetected = 10 ** (length - 2) * sum(
            pair_weight(modulus // math.gcd(modulus, 9 * 10**k))
            for k in range(length - 1)
        )

    detected = total - undetected
    rate = Fraction(detected, total) if total else None
    return {
        "total_events": total,
        "detected_events": detected,
        "undetected_events": undetected,
        "detection_rate": rate,
    }


def _expected_csv_keys() -> set[tuple[int, int, str]]:
    return {
        (modulus, length, error_type)
        for modulus in MODULI
        for length in LENGTHS
        for error_type in ERROR_TYPES
    }


def _read_rate(value: str, key: tuple[int, int, str], column: str) -> Decimal | None:
    if value == "":
        return None
    try:
        rate = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"Malformed {column} for {key}: {value!r}") from error
    if not rate.is_finite() or rate < 0 or rate > 1:
        raise ValueError(f"Out-of-range {column} for {key}: {value!r}")
    return rate


def load_sweep_csv(path: Path) -> list[dict]:
    """Read and validate the complete per-length CSV without enumerating strings."""
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
                raise ValueError(f"Malformed sweep CSV row at line {line_number}")
            try:
                row = {
                    "modulus": int(raw["modulus"]),
                    "length": int(raw["length"]),
                    "error_type": raw["error_type"],
                    "original_strings": int(raw["original_strings"]),
                    "total_events": int(raw["total_events"]),
                    "detected_events": int(raw["detected_events"]),
                    "undetected_events": int(raw["undetected_events"]),
                }
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Malformed integer field in sweep CSV at line {line_number}"
                ) from error

            modulus, length, error_type = (
                row["modulus"], row["length"], row["error_type"]
            )
            key = (modulus, length, error_type)
            if key in seen:
                raise ValueError(f"Duplicate sweep CSV row for {key}")
            seen.add(key)
            if modulus not in MODULI or length not in LENGTHS:
                raise ValueError(f"Unexpected modulus or length at line {line_number}")
            if error_type not in ERROR_TYPES:
                raise ValueError(f"Unexpected error type at line {line_number}: {error_type}")
            if row["original_strings"] != 10**length:
                raise ValueError(f"Unexpected original-string count for {key}")

            expected = analytical_counts(modulus, length, error_type)
            for field in (
                "total_events", "detected_events", "undetected_events"
            ):
                if row[field] != expected[field]:
                    raise ValueError(
                        f"Analytical {field} mismatch for {key}: "
                        f"CSV={row[field]}, expected={expected[field]}"
                    )

            expected_rate = expected["detection_rate"]
            for field in ("detection_rate", "undetected_rate"):
                actual_rate = _read_rate(raw[field], key, field)
                numerator = (
                    expected["detected_events"]
                    if field == "detection_rate"
                    else expected["undetected_events"]
                )
                if expected["total_events"] == 0:
                    if actual_rate is not None:
                        raise ValueError(f"Zero-event {field} must be blank for {key}")
                    continue
                if actual_rate is None:
                    raise ValueError(f"Missing {field} for {key}")
                if display_rate(
                    int(numerator), int(expected["total_events"])
                ) != display_decimal_rate(actual_rate):
                    raise ValueError(f"Two-decimal {field} mismatch for {key}")
            row["detection_rate"] = expected_rate
            rows.append(row)

    expected_keys = _expected_csv_keys()
    if seen != expected_keys:
        missing = sorted(expected_keys - seen)
        extra = sorted(seen - expected_keys)
        raise ValueError(
            f"Sweep CSV dimensions do not match 232 expected rows; "
            f"missing={missing[:3]}, extra={extra[:3]}"
        )
    return rows


def load_aggregate_markdown(path: Path) -> dict[tuple[int, str], dict]:
    """Parse the existing 58-row aggregate table and validate its rates."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    heading = "## Aggregate results by modulus"
    if lines.count(heading) != 1:
        raise ValueError("Aggregate Markdown must contain one aggregate section")
    start = lines.index(heading) + 1
    end = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    section = lines[start:end]
    if section.count(AGGREGATE_HEADER) != 1:
        raise ValueError("Aggregate Markdown table header is missing or duplicated")
    header_index = section.index(AGGREGATE_HEADER)
    if header_index + 1 >= len(section) or not section[header_index + 1].startswith("|---"):
        raise ValueError("Aggregate Markdown table separator is missing")

    result = {}
    for line in section[header_index + 2:]:
        if not line.startswith("|"):
            continue
        match = AGGREGATE_ROW.fullmatch(line)
        if match is None:
            raise ValueError(f"Malformed aggregate Markdown row: {line}")
        modulus, error_type = int(match[1]), match[2]
        key = (modulus, error_type)
        if key in result:
            raise ValueError(f"Duplicate aggregate Markdown row for {key}")
        total, detected, undetected = map(int, match.group(3, 4, 5))
        rate_text = match[6]
        if min(total, detected, undetected) < 0 or detected + undetected != total:
            raise ValueError(f"Inconsistent aggregate event counts for {key}")
        expected_rate = display_rate(detected, total)
        if rate_text != expected_rate:
            raise ValueError(
                f"Aggregate rate mismatch for {key}: "
                f"Markdown={rate_text}, count-derived={expected_rate}"
            )
        result[key] = {
            "total_events": total,
            "detected_events": detected,
            "undetected_events": undetected,
            "rate_text": rate_text,
        }

    expected_keys = {(modulus, kind) for modulus in MODULI for kind in ERROR_TYPES}
    if set(result) != expected_keys:
        raise ValueError("Aggregate Markdown must contain exactly 58 expected rows")
    return result


def validate_against_reports(csv_path: Path, markdown_path: Path) -> tuple[list[dict], dict]:
    """Validate all CSV rows and reconcile their sums with aggregate Markdown."""
    rows = load_sweep_csv(csv_path)
    aggregates = load_aggregate_markdown(markdown_path)
    sums = defaultdict(lambda: [0, 0, 0])
    for row in rows:
        values = sums[(row["modulus"], row["error_type"])]
        values[0] += row["total_events"]
        values[1] += row["detected_events"]
        values[2] += row["undetected_events"]

    for key, (total, detected, undetected) in sums.items():
        if key not in aggregates:
            raise ValueError(f"Aggregate Markdown is missing row for {key}")
        aggregate = aggregates[key]
        counts = (total, detected, undetected)
        aggregate_counts = (
            aggregate["total_events"],
            aggregate["detected_events"],
            aggregate["undetected_events"],
        )
        if counts != aggregate_counts:
            raise ValueError(
                f"Aggregate counts do not reconcile for {key}: "
                f"CSV={counts}, Markdown={aggregate_counts}"
            )
        rate_text = display_rate(detected, total)
        if rate_text != aggregate["rate_text"]:
            raise ValueError(
                f"Aggregate detection rate does not reconcile for {key}: "
                f"CSV={rate_text}, Markdown={aggregate['rate_text']}"
            )
    return rows, aggregates


def render_report(rows: list[dict]) -> str:
    """Render the mathematical characterization and validation summary."""
    lines = [
        "# Mathematical Characterization of Modular Error Detection",
        "",
        "## Scope and conventions",
        "",
        "This analysis covers moduli 2–30 and fixed-width decimal strings of lengths 1–4, using the existing sweep CSV. Leading zeros remain part of each string. Each substitution position/replacement and each unequal adjacent-pair position is a separate event; equal-digit swaps are excluded. An event is detected exactly when its residue changes modulo the selected modulus.",
        "",
        "The formulas below apply to every finite length. The CSV validation concerns only the configured finite range above. Detection rates weight individual error events equally; without a model for how errors occur, they are not real-world error probabilities.",
        "",
        "## Residue changes and undetected conditions",
        "",
        "Let `d = b - a` be the nonzero replacement-minus-original digit difference, so `d` is in {-9,…,-1,1,…,9}. For a digit at place `10^k`, a substitution has residue change `Δs = d·10^k`. It is undetected modulo `m` if and only if `m` divides `d·10^k`, equivalently if `(m / gcd(m,10^k))` divides `d`.",
        "",
        "For adjacent digits `a` (higher place) and `b` (lower place `10^k`), swapping them changes the value by `Δt = b·10^(k+1) + a·10^k - a·10^(k+1) - b·10^k = 9·d·10^k`. It is undetected if and only if `(m / gcd(m,9·10^k))` divides `d`.",
        "",
        "## Exact event counts",
        "",
        "For a positive integer `h`, define `W(h) = 2·Σ(10-hj)` over `j = 1,…,floor(9/h)`. For each positive difference `hj`, there are `10-hj` ordered digit pairs, and the negative difference contributes the same number. Thus `W(h)` counts ordered unequal digit pairs whose difference is divisible by `h`; when `h > 9`, the sum is empty and `W(h)=0`.",
        "",
        "For length `n`, each substitution position has 90 ordered unequal digit pairs and `10^(n-1)` assignments to the other digits. Therefore `T_s = 90·n·10^(n-1)` and `U_s = 10^(n-1)·Σ W(m/gcd(m,10^k))` for `k = 0,…,n-1`.",
        "",
        "For `n ≥ 2`, each adjacent position has 90 ordered unequal digit pairs and `10^(n-2)` assignments to the other digits. Therefore `T_t = 90·(n-1)·10^(n-2)` and `U_t = 10^(n-2)·Σ W(m/gcd(m,9·10^k))` for `k = 0,…,n-2`. For `n = 1`, `T_t = U_t = 0`, and the detection rate is N/A.",
        "",
        "For either error type, detected events are `T-U`; when `T > 0`, the detection rate is `(T-U)/T`.",
        "",
        "## Consequences for selected moduli",
        "",
        "- **Moduli 3 and 9, transpositions:** `9·d·10^k` is divisible by both moduli, so every unequal adjacent transposition is undetected for every finite string length.",
        "- **Modulus 3, substitutions:** 10 is congruent to 1 modulo 3. Differences divisible by 3 contribute `W(3)=24` undetected pairs out of 90 per position, giving a 73.33% detection rate at every length.",
        "- **Modulus 9, substitutions:** 10 is congruent to 1 modulo 9. Only differences ±9 are divisible by 9, giving `W(9)=2` undetected pairs out of 90 and a 97.78% detection rate at every length.",
        "- **Modulus 11:** 10 is invertible modulo 11, and the nonzero digit difference `d` as well as 9 is not divisible by 11. Neither residue-change formula can therefore be zero modulo 11. This proves detection of every allowed event for every finite length.",
        "",
        "## Validation against saved results",
        "",
        f"The analytical formulas were compared with all {len(rows)} per-length CSV rows. Total, detected, and undetected counts matched exactly; rates matched after rounding to the reports’ two-decimal percentage format.",
        "",
        "Analytical per-length counts were then summed by modulus and error type and compared with all 58 rows in `reports/modulus_sweep.md`. Counts and displayed rates matched exactly. This is an independent analytical validation of the existing finite experiment, not a rerun of the exhaustive enumeration.",
        "",
        "The mathematical divisibility results above apply to every finite string length under the stated error definitions. Other numerical findings in this project describe only moduli 2–30 and lengths 1–4. No novelty or general practical-performance claim is made.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    try:
        rows, aggregates = validate_against_reports(CSV_PATH, AGGREGATE_PATH)
        report = render_report(rows)
        OUTPUT_PATH.write_text(report, encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(f"Analytical validation stopped: {error}") from error
    print(f"Analytical validation passed: {len(rows)} per-length rows; {len(aggregates)} aggregate rows.")
    print(f"Generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
