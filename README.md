# Modular Error Detection

This project studies how modular residues detect common errors in fixed-width decimal strings. It includes Python checksum utilities, unit tests, and an exhaustive sweep with CSV and Markdown reports.

## Research question and error models

For a selected modulus, which single-digit substitutions and unequal adjacent transpositions change a string's residue?

- **Single-digit substitution:** choose one position and replace its digit with any of the other nine decimal digits. Each position and replacement is a separate event.
- **Unequal adjacent transposition:** choose an adjacent pair with different digits and swap them. Each unequal pair position is a separate event. Equal adjacent digits are excluded because swapping them leaves the string unchanged.

An event is detected exactly when the altered string has a different residue modulo the selected modulus.

## Sweep and results

The exhaustive sweep uses moduli **2–30** and fixed string lengths **1–4**. It enumerates every decimal string of each width, including leading zeros. Error generation preserves the width and leading zeros; converting a string to an integer for its residue does not change that residue.

The CSV contains **232 per-length result rows**: 29 moduli × 4 lengths × 2 error types. The Markdown report contains **58 aggregate rows**: 29 moduli × 2 error types, with counts and detection rates pooled across lengths. Its rates are event-weighted (total detected events divided by total events), not averages of the four per-length rates. Length-1 strings have no adjacent positions, so their transposition event count is zero and their per-length rates are blank in the CSV. The Markdown combines lengths, so each aggregate transposition row includes the events from lengths 2–4.

For every finite decimal-string length under these definitions, modulus 11 detects all single-digit substitutions and all unequal adjacent transpositions. This follows mathematically: a substitution changes the value by `(b-a)10^k`, and a transposition by `9(b-a)10^k` for some nonzero digit difference `b-a`; modulo 11, 10 is a unit and neither the nonzero digit difference nor 9 is divisible by 11. This proof is stronger than the finite sweep, whose modulus-11 rows cover lengths 1–4 and agree with it.

Modulo 3 and modulo 9 cannot detect unequal adjacent transpositions: their value change is a multiple of 9. The sweep’s transposition rows for both moduli consequently show zero detected events.

These findings cover only the error models and range above. Other alterations can preserve a residue, so checksum detection does not guarantee detection of every possible change. A modular checksum is not a cryptographic security mechanism.

## Development

Python 3.12 or later is required. From the repository root, install the project and development dependency:

```powershell
python -m pip install -e ".[dev]"
```

Run the test suite:

```powershell
python -m pytest
```

Execute the sweep:

```powershell
python experiments/run_modulus_sweep.py
```

The sweep writes `reports/modulus_sweep.csv` and `reports/modulus_sweep.md`, replacing those generated report files.

Render separate SVG plots from the existing CSV without rerunning the sweep:

```powershell
python experiments/render_modulus_plots.py
```

The plots are saved as `reports/substitution_detection_rate.svg` and `reports/transposition_detection_rate.svg`. Their rates aggregate event counts across lengths rather than averaging per-length rates.

Analyze the existing sweep results by string length:

```powershell
python experiments/analyze_per_length.py
```

The analysis validates the per-length CSV data against the existing aggregate report before saving `reports/modulus_sweep_by_length.md`. It reuses the existing sweep results and does not rerun the exhaustive experiment or overwrite the existing reports.

Validate the sweep counts against exact analytical formulas:

```powershell
python experiments/validate_analytical_counts.py
```

The validator reads the existing per-length CSV and aggregate Markdown, checks all event counts and displayed rates, and saves the mathematical characterization to `reports/modulus_characterization.md`. It does not rerun the exhaustive sweep or modify the existing reports.

## Phase 4 research notes

The research documents provide theoretical foundations, factual comparisons with established check-character and integrity methods, an educational timeline, and a record of study limitations and possible follow-up work:

- [Phase 4 research plan](docs/research_plan.md)
- [Mathematical foundations](docs/mathematical_foundations.md)
- [Checksum algorithm comparison](docs/checksum_algorithms_comparison.md)
- [Error detection and error correction](docs/error_detection_vs_error_correction.md)
- [Checksum history](docs/checksum_history.md)
- [Limitations and future work](docs/limitations_and_future_work.md)

## Financial validation reports

The financial workbench can render an existing `ValidationResult` as Markdown or deterministic JSON. Reports include summary counts and findings without copying financial cell values. The optional source label is caller-supplied; reports do not calculate file hashes or add timestamps. A report is a snapshot of validation findings, not an authenticated audit log or proof of financial correctness.

```python
from financial_data_workbench import (
    DataSchema,
    load_csv,
    render_json_report,
    render_markdown_report,
    validate_dataset,
)

schema = DataSchema(
    required_columns=("timestamp", "Close"),
    timestamp_column="timestamp",
)
dataset = load_csv("prices.csv", schema)
result = validate_dataset(dataset, schema)

markdown = render_markdown_report(result, source_label="prices.csv")
json_report = render_json_report(result, source_label="prices.csv")
```

### Command-line CSV validation

The workbench also provides a small command-line interface using the built-in
`ohlcv` profile. Install the project, then run it from the repository root:

```powershell
python -m pip install -e .
financial-data-workbench prices.csv --schema ohlcv --format markdown --output validation-report.md
```

The installed `financial-data-workbench` command and
`python -m financial_data_workbench` use the same CLI; either form may be used.
The latter is also available after installation.

The profile expects the case-sensitive columns `timestamp`, `Open`, `High`,
`Low`, `Close`, and `Volume`. Timestamps use the validator's ISO parsing;
date-only values are interpreted as midnight without implying a time zone.
The four OHLC columns are parsed as decimal values and checked using the
existing high/low relationships. `Volume` is an integer constrained to be
nonnegative. No price bounds, cadence, or exchange-calendar rules are assumed.
The report is written as Markdown by default; pass `--format json` for JSON,
or omit `--output` to write the report to standard output. The CLI prints a
summary without raw cell values.

Exit codes are `0` when validation finds no issues, `1` when validation
completes with data-quality issues, and `2` for command or execution errors.
An output path that identifies the input file is rejected to prevent replacing
the source CSV. `--schema ohlcv` is a CLI profile, not a schema registry entry
or an existing project-wide schema identifier.
