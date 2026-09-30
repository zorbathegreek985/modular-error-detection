# Mathematical Foundations

## Decimal strings and residues

A fixed-width decimal string with digits `x_(n-1)...x_1 x_0` represents the integer

`N = sum(x_k * 10^k, k = 0,...,n-1)`.

The string's residue modulo an integer `m > 1` is the remainder class `[N]` in `Z/mZ`. Two values are congruent modulo `m`, written `N' ≡ N (mod m)`, exactly when `m` divides their difference. A residue check detects an alteration when the original and altered values are not congruent.

The project keeps fixed-width strings as strings during error generation, so leading zeroes are preserved. Integer conversion is used for the residue; leading zeroes do not change the represented integer or its residue. Width still matters to the number of positions and events being counted.

## Error-induced residue changes

### Single-digit substitution

Suppose a digit `a` at place `10^k` is replaced by a different digit `b`. All other places cancel in the difference:

`Delta_s = N' - N = (b - a) * 10^k`.

It is undetected modulo `m` if and only if `m | (b-a) * 10^k`. Equivalently,

`m / gcd(m, 10^k) | (b-a)`.

Here `b-a` is nonzero and lies from -9 through 9. Whether a substitution is detectable therefore depends on both the place and the common factors of the modulus and that place's power of ten.

### Unequal adjacent transposition

Let `a` occupy the higher place `10^(k+1)` and `b` the lower place `10^k`, with `a != b`. Swapping them gives

`Delta_t = b*10^(k+1) + a*10^k - a*10^(k+1) - b*10^k`

`        = 9 * (b-a) * 10^k`.

The swap is undetected exactly when `m | 9*(b-a)*10^k`, or equivalently when

`m / gcd(m, 9*10^k) | (b-a)`.

Equal adjacent digits are excluded by the project definition: exchanging them leaves the string unchanged and does not produce a distinct altered string.

## Consequences for modulus 11

Modulo 11, `10 ≡ -1`, so every power of 10 is invertible. For a substitution, the nonzero difference `b-a` has magnitude at most 9, so it is not divisible by 11. Thus `(b-a)*10^k` is nonzero modulo 11.

For a transposition, `9` and every allowed nonzero `b-a` are also nonzero modulo 11, and `10^k` is invertible. Their product is nonzero modulo 11. Therefore modulus 11 detects every single-digit substitution and every unequal adjacent transposition for every finite string length under these definitions.

This is a mathematical proof for the stated error models. The sweep is a separate finite computation over moduli 2–30 and lengths 1–4; its modulus-11 rows agree with the proof but do not establish the all-length claim by themselves.

## Additional consequences and boundaries

For an adjacent transposition, `Delta_t` is always divisible by 9. Moduli 3 and 9 therefore miss every such event, at any length. This algebraic statement applies to the plain integer-residue method used here.

These conclusions do not extend automatically to multiple substitutions, insertions, deletions, non-adjacent permutations, or check-character algorithms with position-dependent transformations. A checksum defines a particular map from strings to check values; its guarantees are only as broad as the map and error model being analyzed.

## Sources

- The project-specific equations are derived from positional decimal notation and divisibility in `Z/mZ`; see also the generated [Phase 3 characterization](../reports/modulus_characterization.md).
- R. W. Hamming, [“Error Detecting and Error Correcting Codes”](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x), *Bell System Technical Journal*, 1950, for the broader code-theoretic setting.
