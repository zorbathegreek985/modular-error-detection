# Modular Error-Detection Sweep

## Experiment design

- Moduli: 2 through 30, inclusive.
- Decimal string lengths: 1 through 4, inclusive.
- Every fixed-width decimal string is enumerated,
  including strings with leading zeros.
- Substitution: change exactly one digit to a
  different decimal digit.
- Transposition: swap unequal adjacent digits;
  identical adjacent pairs are skipped.
- An event is detected when the altered string
  has a different residue modulo the modulus.
- Detection rate = detected events / total events.
- Undetected rate = undetected events / total events.
- Rates are blank when there are no applicable events.

## Methodology and interpretation

Each substitution event is one original string, one digit position, and one different replacement digit. Each transposition event is one original string and one position containing unequal adjacent digits; equal pairs are excluded because swapping them does not alter the string. Events are counted individually, even when they share an original string. An event is detected when the altered string's residue differs from the original's residue modulo the selected modulus.

For each row, detection rate is `detected_events / total_events` and undetected rate is `undetected_events / total_events`. If a row has no events, both rates are blank. In particular, length-1 strings have no adjacent pair and therefore no transposition events; their per-length CSV rates are blank. The aggregate table pools counts over lengths 1–4, so each aggregate transposition row has events from lengths 2–4.

Aggregate rates are event-weighted: the table divides the sum of detected events across lengths by the sum of all events across lengths. It does not take an unweighted mean of the four per-length rates. The CSV has 232 per-length rows (29 moduli × 4 lengths × 2 error types); this table has 58 aggregate rows (29 moduli × 2 error types).

The 100% modulus-11 rows agree with a general proof: for a substitution, the value change has form `(b-a)10^k`; for an unequal adjacent transposition it has form `9(b-a)10^k`, where `b-a` is nonzero and between -9 and 9. Modulo 11, 10 is invertible and neither 9 nor `b-a` is divisible by 11, so neither change is zero modulo 11. Thus modulus 11 detects every event of both types for any finite decimal-string length under these definitions. This is a mathematical result, while the table is only the finite sweep over lengths 1–4.

For unequal adjacent transpositions, the change is divisible by 9. Since 9 is zero modulo both 3 and 9, neither modulus detects these events. The table agrees: both moduli have zero detected transpositions in this sweep.

## Scope and limitations

The numerical results apply to the tested lengths and error models. Neither the sweep nor the proof covers arbitrary alteration types. A checksum may miss other changes and does not provide cryptographic security. The modulus-11 statement above is limited to the two defined event types, though it applies to every finite string length.

## Aggregate results by modulus

| Modulus | Error type | Events | Detected | Undetected | Detection rate |
|---:|---|---:|---:|---:|---:|
| 2 | substitution | 388890 | 55550 | 333340 | 14.28% |
| 2 | transposition | 28890 | 5550 | 23340 | 19.21% |
| 3 | substitution | 388890 | 285186 | 103704 | 73.33% |
| 3 | transposition | 28890 | 0 | 28890 | 0.00% |
| 4 | substitution | 388890 | 137714 | 251176 | 35.41% |
| 4 | transposition | 28890 | 13714 | 15176 | 47.47% |
| 5 | substitution | 388890 | 88880 | 300010 | 22.85% |
| 5 | transposition | 28890 | 8880 | 20010 | 30.74% |
| 6 | substitution | 388890 | 302962 | 85928 | 77.90% |
| 6 | transposition | 28890 | 5550 | 23340 | 19.21% |
| 7 | substitution | 388890 | 362964 | 25926 | 93.33% |
| 7 | transposition | 28890 | 26964 | 1926 | 93.33% |
| 8 | substitution | 388890 | 232686 | 156204 | 59.83% |
| 8 | transposition | 28890 | 22686 | 6204 | 78.53% |
| 9 | substitution | 388890 | 380248 | 8642 | 97.78% |
| 9 | transposition | 28890 | 0 | 28890 | 0.00% |
| 10 | substitution | 388890 | 99990 | 288900 | 25.71% |
| 10 | transposition | 28890 | 9990 | 18900 | 34.58% |
| 11 | substitution | 388890 | 388890 | 0 | 100.00% |
| 11 | transposition | 28890 | 28890 | 0 | 100.00% |
| 12 | substitution | 388890 | 329610 | 59280 | 84.76% |
| 12 | transposition | 28890 | 13714 | 15176 | 47.47% |
| 13 | substitution | 388890 | 388890 | 0 | 100.00% |
| 13 | transposition | 28890 | 28890 | 0 | 100.00% |
| 14 | substitution | 388890 | 369630 | 19260 | 95.05% |
| 14 | transposition | 28890 | 27630 | 1260 | 95.64% |
| 15 | substitution | 388890 | 311850 | 77040 | 80.19% |
| 15 | transposition | 28890 | 8880 | 20010 | 30.74% |
| 16 | substitution | 388890 | 326850 | 62040 | 84.05% |
| 16 | transposition | 28890 | 26850 | 2040 | 92.94% |
| 17 | substitution | 388890 | 388890 | 0 | 100.00% |
| 17 | transposition | 28890 | 28890 | 0 | 100.00% |
| 18 | substitution | 388890 | 382470 | 6420 | 98.35% |
| 18 | transposition | 28890 | 5550 | 23340 | 19.21% |
| 19 | substitution | 388890 | 388890 | 0 | 100.00% |
| 19 | transposition | 28890 | 28890 | 0 | 100.00% |
| 20 | substitution | 388890 | 155490 | 233400 | 39.98% |
| 20 | transposition | 28890 | 15490 | 13400 | 53.62% |
| 21 | substitution | 388890 | 388890 | 0 | 100.00% |
| 21 | transposition | 28890 | 26964 | 1926 | 93.33% |
| 22 | substitution | 388890 | 388890 | 0 | 100.00% |
| 22 | transposition | 28890 | 28890 | 0 | 100.00% |
| 23 | substitution | 388890 | 388890 | 0 | 100.00% |
| 23 | transposition | 28890 | 28890 | 0 | 100.00% |
| 24 | substitution | 388890 | 356090 | 32800 | 91.57% |
| 24 | transposition | 28890 | 22686 | 6204 | 78.53% |
| 25 | substitution | 388890 | 188790 | 200100 | 48.55% |
| 25 | transposition | 28890 | 18790 | 10100 | 65.04% |
| 26 | substitution | 388890 | 388890 | 0 | 100.00% |
| 26 | transposition | 28890 | 28890 | 0 | 100.00% |
| 27 | substitution | 388890 | 388890 | 0 | 100.00% |
| 27 | transposition | 28890 | 21186 | 7704 | 73.33% |
| 28 | substitution | 388890 | 376290 | 12600 | 96.76% |
| 28 | transposition | 28890 | 28290 | 600 | 97.92% |
| 29 | substitution | 388890 | 388890 | 0 | 100.00% |
| 29 | transposition | 28890 | 28890 | 0 | 100.00% |
| 30 | substitution | 388890 | 311850 | 77040 | 80.19% |
| 30 | transposition | 28890 | 9990 | 18900 | 34.58% |
