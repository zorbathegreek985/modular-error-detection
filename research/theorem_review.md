# R4 Theorem Review: Independent Verification

## 1. Purpose

This document independently checks the mathematics in [the formal model](formal_model.md) and consolidates the results into a compact theorem structure. Scope is limited to the project's plain decimal residue and its two defined error classes.

The literature status remains: **not established as novel; insufficiently located in the searched literature.** Accessible reviewed material did not establish the exact factorized characterization for this plain-residue model. Do not upgrade this classification.

## 2. Mathematical objects and assumptions

Let `D={0,...,9}`, `n>=1`, and `x in D^n`. The string is fixed-width, so leading zeros retain their positions. With `x_k` the digit at place `10^k`, define `N_n(x)=sum_{k=0}^{n-1} x_k*10^k` and `C_m(x)=N_n(x) mod m`, for integer `m>1`. An event is detected exactly when the transformed string has a different residue; it is undetected exactly when `m` divides the value difference.

A substitution changes exactly one digit to a different digit. A transposition swaps one adjacent unequal pair; equal pairs are excluded because the string would not change. Every source string, position, and replacement/pair choice is an event. No probability distribution is assumed.

For a substitution, let `a` be the original digit and `b` the replacement. For a transposition, let `a` be the higher-place digit at `k+1` and `b` the lower-place digit at `k`. Set `d=b-a` in both cases. Then `d` belongs to `D*={-9,...,-1,1,...,9}` and every value in `D*` is realizable. The sign affects the displayed delta, but not divisibility. Substitution positions have `0<=k<n`; transposition lower-place indices have `0<=k<n-1`.

## 3. Independent derivation

### A. Substitution delta

Only place `k` changes, so `N_n(y)-N_n(x)=b*10^k-a*10^k=(b-a)*10^k=d*10^k`. Thus `Delta_s=d*10^k`.

### B. Adjacent transposition delta

Before the swap, the pair contributes `a*10^(k+1)+b*10^k`; afterward it contributes `b*10^(k+1)+a*10^k`. Subtraction gives

```text
Delta_t = (b-a)*10^(k+1) + (a-b)*10^k
        = (b-a)*(10-1)*10^k
        = 9*d*10^k.
```

This confirms the sign and indexing in the formal model. Defining `d=a-b` would negate both deltas without changing detection.

### C. General error delta

Both classes have `Delta=c*d*10^k`: `c=1` for substitution and `c=9` for an unequal adjacent swap. For a transposition, `k` is the lower-place index and is defined only when an adjacent pair exists.

## 4. Lemma: gcd divisibility

**Lemma.** For positive integer `m`, nonzero integer `q`, and any integer `d`, with `g=gcd(m,q)>0`,

```text
m | q*d  iff  m/g | d.
```

**Proof.** Write `m=g*m'`, `q=g*q'`; then `gcd(m',q')=1`. Hence `m|q*d` iff `m'|q'*d`, which by Euclid's lemma is equivalent to `m'|d`. Since `m'=m/g`, the result follows. Negative `q` or `d` cause no problem; divisibility is over integers and gcd is positive. The lemma also holds for `d=0`, though project events have `d!=0`. The checksum application assumes `m>1`. Its specializations `q=10^k` and `q=9*10^k` are nonzero for each integer `k>=0`.

Therefore the position-specific undetection conditions are exactly

```text
substitution:  r_s(k) | d,  r_s(k)=m/gcd(m,10^k)
transposition: r_t(k) | d,  r_t(k)=m/gcd(m,9*10^k).
```

## 5. Substitution theorem

**Theorem 1 (universal substitution detection at a position).** Fix `m>1` and `k>=0`. Every nonzero decimal substitution at that position, over every source string containing the position, is detected iff no `d in D*` is divisible by `r_s(k)`. Equivalently, it is detected universally iff `r_s(k)>9`.

**Proof.** By the lemma, an event is undetected iff `r_s(k)|d`. If `r_s(k)>9`, no nonzero `d` with `|d|<=9` is divisible by it. Conversely, if `r_s(k)<=9`, the allowed digit pair `(a,b)=(0,r_s(k))` has `d=r_s(k)`, producing an undetected event. Both directions hold; primality is irrelevant.

For fixed length `n`, all substitutions at every position and for every source string are detected iff `min_{0<=k<n} r_s(k)>9`. Since `gcd(m,10^k)` is nondecreasing by divisibility, `r_s(k)` is nonincreasing, so this is exactly `m/gcd(m,10^(n-1))>9`.

For all finite lengths, the quantifiers are every `n>=1`, every `0<=k<n`, every source string, and every different replacement. The exact condition is derived in Section 8.

## 6. Adjacent transposition theorem

**Theorem 2 (universal unequal-swap detection at a pair).** Fix `m>1` and lower-place index `k>=0`. Every unequal adjacent transposition at that pair, over every source string containing it, is detected iff no `d in D*` is divisible by `r_t(k)`. Equivalently, this holds iff `r_t(k)>9`.

**Proof.** The lemma says the swap is undetected exactly when `r_t(k)|d`. If `r_t(k)>9`, no allowed difference is divisible by it. If `r_t(k)<=9`, choosing higher/lower digits `(a,b)=(0,r_t(k))` produces an allowed unequal pair and an undetected swap. This proves necessity and sufficiency.

For fixed length `n>=2`, all unequal swaps at all adjacent positions and all source strings are detected iff `min_{0<=k<n-1} r_t(k)>9`. The sequence is nonincreasing, so the condition is exactly `m/gcd(m,9*10^(n-2))>9`.

At `n=1`, the transposition event set is empty. Universal detection over an empty set is vacuously true, but a detection rate is undefined because the denominator is zero; the project correctly represents it as N/A/blank.

## 7. Universal detection criteria

The fixed-position theorems plus monotonicity give the fixed-length criteria. The all-length criteria are the eventual reduced-modulus limits proved next.

| Error class | One position `k` | Every position at fixed length `n` | All positions at every finite applicable length |
|---|---|---|---|
| Substitution | `m/gcd(m,10^k)>9` | `m/gcd(m,10^(n-1))>9` | `3^b*u>9` |
| Unequal adjacent transposition | `m/gcd(m,9*10^k)>9` | for `n>=2`: `m/gcd(m,9*10^(n-2))>9` | `3^max(b-2,0)*u>9` |

The final column assumes `m=2^a*3^b*5^c*u`, `a,b,c>=0`, `gcd(u,30)=1`.

## 8. Prime-factor characterization

Write `m=2^a*3^b*5^c*u`, where `gcd(u,30)=1`.

### A. Substitutions

Since `10^k=2^k*5^k`,

```text
r_s(k)=2^(a-min(a,k))*3^b*5^(c-min(c,k))*u.
```

As `k` increases, powers of 2 and 5 cancel until exhausted; the 3-power and `u` remain. For all `k>=max(a,c)`, `r_s(k)=3^b*u`, which is attained and is the minimum. Therefore every substitution at every position for every finite length is detected iff `3^b*u>9`. This is equivalent to `m/(2^a*5^c)>9`, the formal model's expression. If the eventual value is at most 9, it is attained at finite `k`, and choosing `d=r_s(k)` gives an undetected event. If it exceeds 9, every preceding reduced modulus is at least that value.

### B. Unequal adjacent transpositions

Since `9=3^2`,

```text
r_t(k)=2^(a-min(a,k))*3^(b-min(b,2))*5^(c-min(c,k))*u.
```

The factor `3^min(b,2)` is present from `k=0` and does not change with position, because `10^k` has no factor of 3. Powers of 2 and 5 eventually cancel, and the reduced-divisor sequence stabilizes at `k>=max(a,c)`. The attained eventual minimum is `3^max(b-2,0)*u`. Thus every unequal adjacent swap at every position for every finite length `n>=2` is detected iff `3^max(b-2,0)*u>9`.

This is a clean exact condition; the gcd criterion remains useful for individual positions and fixed lengths. The conclusion is specific to decimal positional value and the stated events; it is not a vague claim about prime moduli being “better.”

## 9. Modulus 11 corollary

For `m=11`, `a=b=c=0`, `u=11`; both all-length criteria reduce to `11>9`. Hence every defined single-digit substitution and every defined unequal adjacent transposition is detected for every finite fixed-width length under this residue model. This does not imply detection of insertions, deletions, multiple changes, non-adjacent swaps, arbitrary alterations, or errors under other algorithms. It does not show 11 is optimal under other objectives.

## 10. Modulus 3 and modulus 9 analysis

Because 10 is coprime to both 3 and 9, the substitution reduced moduli remain 3 and 9 at every position.

- **Modulus 3 substitutions:** undetected iff `3|d`, so exactly `d=+-3,+-6,+-9` are missed. `W(3)=24` of 90 ordered unequal pairs are missed; `66/90=11/15` are detected under equal event weighting.
- **Modulus 9 substitutions:** undetected iff `9|d`, so only `d=+-9` are missed. `W(9)=2` of 90 pairs are missed; `88/90=44/45` are detected under equal event weighting.
- **Transpositions modulo 3 or 9:** `Delta_t=9*d*10^k` is divisible by both moduli. Every unequal adjacent transposition is undetected, at every position and length.

Thus modulus 3 detects some substitutions but misses those whose digit difference is divisible by 3; modulus 9 misses only the 0/9 substitutions. Both fail completely for the defined adjacent swaps.

## 11. Exact `W(h)` counting result

**Proposition.** For positive integer `h`, let `W(h)` count ordered pairs `(a,b) in D x D` with `a!=b` and `h|(b-a)`. Then

```text
W(h)=2*sum_{j=1}^{floor(9/h)}(10-h*j).
```

**Proof.** Each nonzero difference divisible by `h` is `+h*j` or `-h*j`, where `1<=j<=floor(9/h)`. For positive difference `b-a=h*j`, the smaller digit ranges from 0 to `9-h*j`, giving `10-h*j` ordered pairs. Reversing each pair gives the same number for negative difference. These are disjoint, hence the factor 2. The sum is empty for `h>9`, so `W(h)=0`; `W(1)=90` counts every ordered unequal digit pair.

`W(h)` counts **ordered** source/replacement pairs for substitutions and ordered higher/lower source-digit pairs for transpositions. The sum indexes positive differences only; the factor 2 includes negative differences. It does not count unordered pairs or whole strings. At a given position set `h=m/gcd(m,c*10^k)`, with `c=1` or 9. The gcd lemma makes `h|d` exactly the undetection condition, so `W(h)` is exactly the undetected ordered digit-pair count at that position. Multiply by `10^(n-1)` for free digits at a substitution position or `10^(n-2)` for free digits at a transposition pair position. Sum over positions for whole-string event totals.

## 12. Edge-case verification

The reduced moduli below are computed from the gcd formulas for every requested `m` and `k=0,1,2,3`. A listed representative `d` is undetected exactly when the corresponding reduced modulus divides it. The requested set is `{-9,-5,-3,-2,-1,1,2,3,5,9}`. Differences 4 and 6 are absent from that sample but are valid decimal differences and test the necessity direction for reduced moduli 4 and 6.

| `m` | `r_s(0),r_s(1),r_s(2),r_s(3)` | `r_t(0),r_t(1),r_t(2),r_t(3)` | Listed-difference check |
|---:|---|---|---|
| 2 | 2, 1, 1, 1 | 2, 1, 1, 1 | `r=2` misses listed `+-2`; `r=1` misses all. |
| 3 | 3, 3, 3, 3 | 1, 1, 1, 1 | Substitution misses `+-3,+-9`; transposition misses all. |
| 5 | 5, 1, 1, 1 | 5, 1, 1, 1 | `r=5` misses `+-5`; `r=1` misses all. |
| 9 | 9, 9, 9, 9 | 1, 1, 1, 1 | Substitution misses `+-9`; transposition misses all. |
| 10 | 10, 1, 1, 1 | 10, 1, 1, 1 | `r=10` misses none of the sample; `r=1` misses all. |
| 11 | 11, 11, 11, 11 | 11, 11, 11, 11 | No listed difference is divisible by 11; all are detected. |
| 12 | 12, 6, 3, 3 | 4, 2, 1, 1 | Substitution `r=3` misses `+-3,+-9`; transposition `r=4` misses none listed, but valid `d=+-4` is missed; `r=2` misses `+-2`; `r=1` misses all. |
| 18 | 18, 9, 9, 9 | 2, 1, 1, 1 | Substitution `r=9` misses `+-9`; transposition `r=2` misses `+-2`, then `r=1` misses all. |
| 25 | 25, 5, 1, 1 | 25, 5, 1, 1 | `r=25` misses none listed; `r=5` misses `+-5`; `r=1` misses all. |
| 30 | 30, 3, 3, 3 | 10, 1, 1, 1 | Substitution `r=3` misses `+-3,+-9`; transposition `r=10` misses none listed; `r=1` misses all. |
| 31 | 31, 31, 31, 31 | 31, 31, 31, 31 | No listed difference is divisible by 31; all are detected. |

For `r=6`, which occurs outside this table, valid `d=+-6` confirms the `r<=9` failure direction despite not belonging to the requested sample set. No counterexample to the formulas was found. This is a finite arithmetic sanity check, not a sweep or evidence for the universal proof.

## 13. Comparison with existing implementation

Inspection of the implementation, analytical code, tests, and characterization report found matching semantics:

- `checksum.py` computes integer `value % modulus`. The sweep converts a string to an integer only for residue computation; this preserves the numeric value and residue, while string-based generation preserves width and leading zeros.
- `single_digit_substitutions` iterates every position and every different ASCII decimal digit, preserving width. This matches one event per source-position-replacement choice.
- `adjacent_transpositions` emits a swap for each unequal adjacent pair, skips equal pairs, preserves width, and produces no event for length 1.
- `analytical_counts` uses `m/gcd(m,10^k)` or `m/gcd(m,9*10^k)`, applies the ordered-pair `pair_weight(h)`, and multiplies by the free-position counts. Rates use exact fractions; zero-event rate is absent/`None` and rendered N/A.
- The characterization report gives the same deltas, `W(h)`, total and undetected count formulas, and the 3/9/11 consequences. It states reconciliation of 232 per-length rows and 58 aggregate rows; this review did not rerun validation.

The formal model matches the inspected implementation's event semantics. No mismatch was identified.

## 14. Comparison with literature findings

The [literature matrix](literature_matrix.md) records prior decimal error-detecting work, including Verhoeff's decimal-code monograph, Gumm's generalized check-digit method, substitution/transposition code theory, Damm's group-based results, and ISO check-character systems. These are relevant but do not automatically share the plain `N(x) mod m` construction.

The exact plain-residue factorization characterization remains **not established as novel; insufficiently located in the searched literature**. Do not upgrade this to a novelty claim. The Verhoeff monograph's contents indicate prior computational search in decimal error-detecting codes, so a broad “first computational study” statement is unsupported.

## 15. Established vs project-derived claims

### Established mathematics

Positional representation, gcd cancellation, Euclid's lemma, prime factorization, and finite digit-pair counting are established elementary mathematics. The delta equations and position-specific divisibility conditions follow from the stated definitions.

### Project-derived results

The project formulates the reduced-modulus tests, derives their exact decimal universal thresholds, fixed-length endpoint conditions, all-finite-length factorization criteria, and `W(h)` event counts under its event definitions. “Project-derived” refers to the derivation here, not priority.

### Computationally validated results

The existing characterization report and validator state that formulas reconcile 232 per-length rows and 58 aggregate rows, including counts and displayed rates. This is evidence over moduli 2-30 and lengths 1-4 only. No sweep or validator was run in this phase. Finite agreement is not proof of all-length claims.

### Literature-established results

Decimal check-digit/error-detecting codes, substitution/transposition error models, group-based methods, and standardized check-character systems predate this project. The reviewed evidence establishes this broad prior art but neither establishes nor rules out publication of the exact plain-residue factorization formula.

### Not established

Novelty, priority, superiority, real-world error probabilities, and guarantees outside the defined event classes are not established. Whether a comparable plain-residue sweep has already been published remains uncertain.

## 16. Potential implementation/model discrepancies

No mathematical or event-semantics discrepancy was found in the inspected checksum, generators, analytical count implementation, tests, or characterization report. Integer conversion is consistent with the positional-value map; the original strings are retained for edits. This was read-only inspection; no validator or report was regenerated.

## 17. Research significance assessment

The statements are mathematically correct under the stated assumptions. Their core proof is short and largely an elementary consequence of gcd arithmetic and the bounded decimal difference set. On its own, the factorization theorem is likely too elementary to support a research paper as a new theorem, especially while its exact prior-art relationship is unresolved.

Combined with exhaustive computation, the work gives a reproducible account of event counts and rates over a selected finite modulus/length grid and checks that account against closed-form counts. This is useful and auditable, but this review cannot establish that the combination is novel or sufficient for publication. A stronger contribution would need a substantial open problem or a justified application, alongside fuller prior-art review; this review does not select a new theorem.

## 18. Remaining mathematical questions

- What exact characterization holds in arbitrary base `B` with a specified alphabet and error set?
- How do arbitrary positional weights change the substitution and adjacent-swap conditions?
- What conditions govern non-adjacent swaps or multiple simultaneous substitutions?
- What probability models, if any, are justified for an application?

These are possible next questions, not claims that no prior work exists.

## 19. Recommended next research action

**Exactly one action:** conduct a citation-chained, full-text prior-art review of linear positional checksum codes over arbitrary bases, comparing each source's exact code definition and theorem statements with `N(x) mod m` before deciding whether to pursue a broader theorem or an application.
