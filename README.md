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
