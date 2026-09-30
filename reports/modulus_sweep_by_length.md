# Per-Length Modular Error-Detection Analysis

These results reuse `reports/modulus_sweep.csv`; the exhaustive sweep is not rerun.
Events and detection retain the definitions in the sweep: one-position substitutions and unequal adjacent swaps, detected when the residue changes.
Detection rate is detected events divided by total events. Rates are shown to two decimal places; zero-event rates are `N/A`.
Counts pooled across lengths were reconciled against `reports/modulus_sweep.md` before this report was written.

## Substitution

### String length 1

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 1 | substitution | 90 | 50 | 40 | 55.56% |
| 3 | 1 | substitution | 90 | 66 | 24 | 73.33% |
| 4 | 1 | substitution | 90 | 74 | 16 | 82.22% |
| 5 | 1 | substitution | 90 | 80 | 10 | 88.89% |
| 6 | 1 | substitution | 90 | 82 | 8 | 91.11% |
| 7 | 1 | substitution | 90 | 84 | 6 | 93.33% |
| 8 | 1 | substitution | 90 | 86 | 4 | 95.56% |
| 9 | 1 | substitution | 90 | 88 | 2 | 97.78% |
| 10 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 11 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 12 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 13 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 14 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 15 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 16 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 17 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 18 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 19 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 20 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 21 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 22 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 23 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 24 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 25 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 26 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 27 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 28 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 29 | 1 | substitution | 90 | 90 | 0 | 100.00% |
| 30 | 1 | substitution | 90 | 90 | 0 | 100.00% |

### String length 2

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 2 | substitution | 1800 | 500 | 1300 | 27.78% |
| 3 | 2 | substitution | 1800 | 1320 | 480 | 73.33% |
| 4 | 2 | substitution | 1800 | 1240 | 560 | 68.89% |
| 5 | 2 | substitution | 1800 | 800 | 1000 | 44.44% |
| 6 | 2 | substitution | 1800 | 1480 | 320 | 82.22% |
| 7 | 2 | substitution | 1800 | 1680 | 120 | 93.33% |
| 8 | 2 | substitution | 1800 | 1600 | 200 | 88.89% |
| 9 | 2 | substitution | 1800 | 1760 | 40 | 97.78% |
| 10 | 2 | substitution | 1800 | 900 | 900 | 50.00% |
| 11 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 12 | 2 | substitution | 1800 | 1720 | 80 | 95.56% |
| 13 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 14 | 2 | substitution | 1800 | 1740 | 60 | 96.67% |
| 15 | 2 | substitution | 1800 | 1560 | 240 | 86.67% |
| 16 | 2 | substitution | 1800 | 1760 | 40 | 97.78% |
| 17 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 18 | 2 | substitution | 1800 | 1780 | 20 | 98.89% |
| 19 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 20 | 2 | substitution | 1800 | 1400 | 400 | 77.78% |
| 21 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 22 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 23 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 24 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 25 | 2 | substitution | 1800 | 1700 | 100 | 94.44% |
| 26 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 27 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 28 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 29 | 2 | substitution | 1800 | 1800 | 0 | 100.00% |
| 30 | 2 | substitution | 1800 | 1560 | 240 | 86.67% |

### String length 3

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 3 | substitution | 27000 | 5000 | 22000 | 18.52% |
| 3 | 3 | substitution | 27000 | 19800 | 7200 | 73.33% |
| 4 | 3 | substitution | 27000 | 12400 | 14600 | 45.93% |
| 5 | 3 | substitution | 27000 | 8000 | 19000 | 29.63% |
| 6 | 3 | substitution | 27000 | 21400 | 5600 | 79.26% |
| 7 | 3 | substitution | 27000 | 25200 | 1800 | 93.33% |
| 8 | 3 | substitution | 27000 | 21000 | 6000 | 77.78% |
| 9 | 3 | substitution | 27000 | 26400 | 600 | 97.78% |
| 10 | 3 | substitution | 27000 | 9000 | 18000 | 33.33% |
| 11 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 12 | 3 | substitution | 27000 | 23800 | 3200 | 88.15% |
| 13 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 14 | 3 | substitution | 27000 | 25800 | 1200 | 95.56% |
| 15 | 3 | substitution | 27000 | 22200 | 4800 | 82.22% |
| 16 | 3 | substitution | 27000 | 25000 | 2000 | 92.59% |
| 17 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 18 | 3 | substitution | 27000 | 26600 | 400 | 98.52% |
| 19 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 20 | 3 | substitution | 27000 | 14000 | 13000 | 51.85% |
| 21 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 22 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 23 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 24 | 3 | substitution | 27000 | 26200 | 800 | 97.04% |
| 25 | 3 | substitution | 27000 | 17000 | 10000 | 62.96% |
| 26 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 27 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 28 | 3 | substitution | 27000 | 26400 | 600 | 97.78% |
| 29 | 3 | substitution | 27000 | 27000 | 0 | 100.00% |
| 30 | 3 | substitution | 27000 | 22200 | 4800 | 82.22% |

### String length 4

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 4 | substitution | 360000 | 50000 | 310000 | 13.89% |
| 3 | 4 | substitution | 360000 | 264000 | 96000 | 73.33% |
| 4 | 4 | substitution | 360000 | 124000 | 236000 | 34.44% |
| 5 | 4 | substitution | 360000 | 80000 | 280000 | 22.22% |
| 6 | 4 | substitution | 360000 | 280000 | 80000 | 77.78% |
| 7 | 4 | substitution | 360000 | 336000 | 24000 | 93.33% |
| 8 | 4 | substitution | 360000 | 210000 | 150000 | 58.33% |
| 9 | 4 | substitution | 360000 | 352000 | 8000 | 97.78% |
| 10 | 4 | substitution | 360000 | 90000 | 270000 | 25.00% |
| 11 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 12 | 4 | substitution | 360000 | 304000 | 56000 | 84.44% |
| 13 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 14 | 4 | substitution | 360000 | 342000 | 18000 | 95.00% |
| 15 | 4 | substitution | 360000 | 288000 | 72000 | 80.00% |
| 16 | 4 | substitution | 360000 | 300000 | 60000 | 83.33% |
| 17 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 18 | 4 | substitution | 360000 | 354000 | 6000 | 98.33% |
| 19 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 20 | 4 | substitution | 360000 | 140000 | 220000 | 38.89% |
| 21 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 22 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 23 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 24 | 4 | substitution | 360000 | 328000 | 32000 | 91.11% |
| 25 | 4 | substitution | 360000 | 170000 | 190000 | 47.22% |
| 26 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 27 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 28 | 4 | substitution | 360000 | 348000 | 12000 | 96.67% |
| 29 | 4 | substitution | 360000 | 360000 | 0 | 100.00% |
| 30 | 4 | substitution | 360000 | 288000 | 72000 | 80.00% |

## Transposition

### String length 1

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 1 | transposition | 0 | 0 | 0 | N/A |
| 3 | 1 | transposition | 0 | 0 | 0 | N/A |
| 4 | 1 | transposition | 0 | 0 | 0 | N/A |
| 5 | 1 | transposition | 0 | 0 | 0 | N/A |
| 6 | 1 | transposition | 0 | 0 | 0 | N/A |
| 7 | 1 | transposition | 0 | 0 | 0 | N/A |
| 8 | 1 | transposition | 0 | 0 | 0 | N/A |
| 9 | 1 | transposition | 0 | 0 | 0 | N/A |
| 10 | 1 | transposition | 0 | 0 | 0 | N/A |
| 11 | 1 | transposition | 0 | 0 | 0 | N/A |
| 12 | 1 | transposition | 0 | 0 | 0 | N/A |
| 13 | 1 | transposition | 0 | 0 | 0 | N/A |
| 14 | 1 | transposition | 0 | 0 | 0 | N/A |
| 15 | 1 | transposition | 0 | 0 | 0 | N/A |
| 16 | 1 | transposition | 0 | 0 | 0 | N/A |
| 17 | 1 | transposition | 0 | 0 | 0 | N/A |
| 18 | 1 | transposition | 0 | 0 | 0 | N/A |
| 19 | 1 | transposition | 0 | 0 | 0 | N/A |
| 20 | 1 | transposition | 0 | 0 | 0 | N/A |
| 21 | 1 | transposition | 0 | 0 | 0 | N/A |
| 22 | 1 | transposition | 0 | 0 | 0 | N/A |
| 23 | 1 | transposition | 0 | 0 | 0 | N/A |
| 24 | 1 | transposition | 0 | 0 | 0 | N/A |
| 25 | 1 | transposition | 0 | 0 | 0 | N/A |
| 26 | 1 | transposition | 0 | 0 | 0 | N/A |
| 27 | 1 | transposition | 0 | 0 | 0 | N/A |
| 28 | 1 | transposition | 0 | 0 | 0 | N/A |
| 29 | 1 | transposition | 0 | 0 | 0 | N/A |
| 30 | 1 | transposition | 0 | 0 | 0 | N/A |

### String length 2

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 2 | transposition | 90 | 50 | 40 | 55.56% |
| 3 | 2 | transposition | 90 | 0 | 90 | 0.00% |
| 4 | 2 | transposition | 90 | 74 | 16 | 82.22% |
| 5 | 2 | transposition | 90 | 80 | 10 | 88.89% |
| 6 | 2 | transposition | 90 | 50 | 40 | 55.56% |
| 7 | 2 | transposition | 90 | 84 | 6 | 93.33% |
| 8 | 2 | transposition | 90 | 86 | 4 | 95.56% |
| 9 | 2 | transposition | 90 | 0 | 90 | 0.00% |
| 10 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 11 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 12 | 2 | transposition | 90 | 74 | 16 | 82.22% |
| 13 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 14 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 15 | 2 | transposition | 90 | 80 | 10 | 88.89% |
| 16 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 17 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 18 | 2 | transposition | 90 | 50 | 40 | 55.56% |
| 19 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 20 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 21 | 2 | transposition | 90 | 84 | 6 | 93.33% |
| 22 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 23 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 24 | 2 | transposition | 90 | 86 | 4 | 95.56% |
| 25 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 26 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 27 | 2 | transposition | 90 | 66 | 24 | 73.33% |
| 28 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 29 | 2 | transposition | 90 | 90 | 0 | 100.00% |
| 30 | 2 | transposition | 90 | 90 | 0 | 100.00% |

### String length 3

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 3 | transposition | 1800 | 500 | 1300 | 27.78% |
| 3 | 3 | transposition | 1800 | 0 | 1800 | 0.00% |
| 4 | 3 | transposition | 1800 | 1240 | 560 | 68.89% |
| 5 | 3 | transposition | 1800 | 800 | 1000 | 44.44% |
| 6 | 3 | transposition | 1800 | 500 | 1300 | 27.78% |
| 7 | 3 | transposition | 1800 | 1680 | 120 | 93.33% |
| 8 | 3 | transposition | 1800 | 1600 | 200 | 88.89% |
| 9 | 3 | transposition | 1800 | 0 | 1800 | 0.00% |
| 10 | 3 | transposition | 1800 | 900 | 900 | 50.00% |
| 11 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 12 | 3 | transposition | 1800 | 1240 | 560 | 68.89% |
| 13 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 14 | 3 | transposition | 1800 | 1740 | 60 | 96.67% |
| 15 | 3 | transposition | 1800 | 800 | 1000 | 44.44% |
| 16 | 3 | transposition | 1800 | 1760 | 40 | 97.78% |
| 17 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 18 | 3 | transposition | 1800 | 500 | 1300 | 27.78% |
| 19 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 20 | 3 | transposition | 1800 | 1400 | 400 | 77.78% |
| 21 | 3 | transposition | 1800 | 1680 | 120 | 93.33% |
| 22 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 23 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 24 | 3 | transposition | 1800 | 1600 | 200 | 88.89% |
| 25 | 3 | transposition | 1800 | 1700 | 100 | 94.44% |
| 26 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 27 | 3 | transposition | 1800 | 1320 | 480 | 73.33% |
| 28 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 29 | 3 | transposition | 1800 | 1800 | 0 | 100.00% |
| 30 | 3 | transposition | 1800 | 900 | 900 | 50.00% |

### String length 4

| Modulus | Length | Error type | Total events | Detected events | Undetected events | Detection rate |
|---:|---:|---|---:|---:|---:|---:|
| 2 | 4 | transposition | 27000 | 5000 | 22000 | 18.52% |
| 3 | 4 | transposition | 27000 | 0 | 27000 | 0.00% |
| 4 | 4 | transposition | 27000 | 12400 | 14600 | 45.93% |
| 5 | 4 | transposition | 27000 | 8000 | 19000 | 29.63% |
| 6 | 4 | transposition | 27000 | 5000 | 22000 | 18.52% |
| 7 | 4 | transposition | 27000 | 25200 | 1800 | 93.33% |
| 8 | 4 | transposition | 27000 | 21000 | 6000 | 77.78% |
| 9 | 4 | transposition | 27000 | 0 | 27000 | 0.00% |
| 10 | 4 | transposition | 27000 | 9000 | 18000 | 33.33% |
| 11 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 12 | 4 | transposition | 27000 | 12400 | 14600 | 45.93% |
| 13 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 14 | 4 | transposition | 27000 | 25800 | 1200 | 95.56% |
| 15 | 4 | transposition | 27000 | 8000 | 19000 | 29.63% |
| 16 | 4 | transposition | 27000 | 25000 | 2000 | 92.59% |
| 17 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 18 | 4 | transposition | 27000 | 5000 | 22000 | 18.52% |
| 19 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 20 | 4 | transposition | 27000 | 14000 | 13000 | 51.85% |
| 21 | 4 | transposition | 27000 | 25200 | 1800 | 93.33% |
| 22 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 23 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 24 | 4 | transposition | 27000 | 21000 | 6000 | 77.78% |
| 25 | 4 | transposition | 27000 | 17000 | 10000 | 62.96% |
| 26 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 27 | 4 | transposition | 27000 | 19800 | 7200 | 73.33% |
| 28 | 4 | transposition | 27000 | 26400 | 600 | 97.78% |
| 29 | 4 | transposition | 27000 | 27000 | 0 | 100.00% |
| 30 | 4 | transposition | 27000 | 9000 | 18000 | 33.33% |
