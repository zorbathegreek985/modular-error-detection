# Mathematical Characterization of Modular Error Detection

## Scope and conventions

This analysis covers moduli 2–30 and fixed-width decimal strings of lengths 1–4, using the existing sweep CSV. Leading zeros remain part of each string. Each substitution position/replacement and each unequal adjacent-pair position is a separate event; equal-digit swaps are excluded. An event is detected exactly when its residue changes modulo the selected modulus.

The formulas below apply to every finite length. The CSV validation concerns only the configured finite range above. Detection rates weight individual error events equally; without a model for how errors occur, they are not real-world error probabilities.

## Residue changes and undetected conditions

Let `d = b - a` be the nonzero replacement-minus-original digit difference, so `d` is in {-9,…,-1,1,…,9}. For a digit at place `10^k`, a substitution has residue change `Δs = d·10^k`. It is undetected modulo `m` if and only if `m` divides `d·10^k`, equivalently if `(m / gcd(m,10^k))` divides `d`.

For adjacent digits `a` (higher place) and `b` (lower place `10^k`), swapping them changes the value by `Δt = b·10^(k+1) + a·10^k - a·10^(k+1) - b·10^k = 9·d·10^k`. It is undetected if and only if `(m / gcd(m,9·10^k))` divides `d`.

## Exact event counts

For a positive integer `h`, define `W(h) = 2·Σ(10-hj)` over `j = 1,…,floor(9/h)`. For each positive difference `hj`, there are `10-hj` ordered digit pairs, and the negative difference contributes the same number. Thus `W(h)` counts ordered unequal digit pairs whose difference is divisible by `h`; when `h > 9`, the sum is empty and `W(h)=0`.

For length `n`, each substitution position has 90 ordered unequal digit pairs and `10^(n-1)` assignments to the other digits. Therefore `T_s = 90·n·10^(n-1)` and `U_s = 10^(n-1)·Σ W(m/gcd(m,10^k))` for `k = 0,…,n-1`.

For `n ≥ 2`, each adjacent position has 90 ordered unequal digit pairs and `10^(n-2)` assignments to the other digits. Therefore `T_t = 90·(n-1)·10^(n-2)` and `U_t = 10^(n-2)·Σ W(m/gcd(m,9·10^k))` for `k = 0,…,n-2`. For `n = 1`, `T_t = U_t = 0`, and the detection rate is N/A.

For either error type, detected events are `T-U`; when `T > 0`, the detection rate is `(T-U)/T`.

## Consequences for selected moduli

- **Moduli 3 and 9, transpositions:** `9·d·10^k` is divisible by both moduli, so every unequal adjacent transposition is undetected for every finite string length.
- **Modulus 3, substitutions:** 10 is congruent to 1 modulo 3. Differences divisible by 3 contribute `W(3)=24` undetected pairs out of 90 per position, giving a 73.33% detection rate at every length.
- **Modulus 9, substitutions:** 10 is congruent to 1 modulo 9. Only differences ±9 are divisible by 9, giving `W(9)=2` undetected pairs out of 90 and a 97.78% detection rate at every length.
- **Modulus 11:** 10 is invertible modulo 11, and the nonzero digit difference `d` as well as 9 is not divisible by 11. Neither residue-change formula can therefore be zero modulo 11. This proves detection of every allowed event for every finite length.

## Validation against saved results

The analytical formulas were compared with all 232 per-length CSV rows. Total, detected, and undetected counts matched exactly; rates matched after rounding to the reports’ two-decimal percentage format.

Analytical per-length counts were then summed by modulus and error type and compared with all 58 rows in `reports/modulus_sweep.md`. Counts and displayed rates matched exactly. This is an independent analytical validation of the existing finite experiment, not a rerun of the exhaustive enumeration.

The mathematical divisibility results above apply to every finite string length under the stated error definitions. Other numerical findings in this project describe only moduli 2–30 and lengths 1–4. No novelty or general practical-performance claim is made.
