# Modular Error Detection — Research Summary

## 1. Research Objective

This repository contains a reproducible computational-mathematics investigation of modular residue error detection for fixed-width digit strings. It derives exact conditions for modeled single substitutions and unequal adjacent transpositions, validates them computationally, generalizes the analysis to arbitrary radix within the stated model, and studies observable spectrum equivalence and identifiability limits.

The project concerns a plain residue of the represented string value. It is not a check-digit generator, financial validation method, cryptographic integrity system, or general theory of all error-detecting codes.

## 2. Mathematical Model

Fix an integer radix $q\ge2$, modulus $m\ge2$, and fixed string width $n\ge1$. Each digit $x_k$ lies in $\{0,1,\ldots,q-1\}$, with $k=0$ the least significant position. The represented value and checksum residue are

$$
N_q(x)=\sum_{k=0}^{n-1}x_kq^k,\qquad C_{m,q}(x)=N_q(x)\bmod m.
$$

The width is retained, including leading-zero positions. The decimal study is the case $q=10$. An alteration is detected exactly when the residue before and after it differs modulo $m$.

## 3. Error Models

The model includes only these two single-event classes:

- **Single substitution:** change one digit at position $k$ from $a$ to a different digit $b$. With $d=b-a$, the altered-minus-original value is $\Delta_s=dq^k$.
- **Unequal adjacent transposition:** exchange adjacent unequal digits. Let $a$ be the lower-place digit and $b$ the higher-place digit at positions $k$ and $k+1$. The altered-minus-original value is $\Delta_t=(a-b)(q-1)q^k$.

Equal adjacent digits are excluded because exchanging them does not change the string. Insertions, deletions, non-adjacent swaps, and multiple simultaneous changes are outside this model.

## 4. Exact Detection Conditions

The substitution is undetected exactly when

$$
m\mid d q^k.
$$

The adjacent transposition is undetected exactly when

$$
m\mid (a-b)(q-1)q^k.
$$

For any integer coefficient $c$, cancellation by the greatest common divisor gives $m\mid c u$ if and only if $m/\gcd(m,c)\mid u$. Thus the substitution's reduced divisor is $m/\gcd(m,q^k)$; the transposition's is $m/\gcd(m,(q-1)q^k)$. In each case, the event is undetected precisely when its nonzero digit difference is divisible by the corresponding reduced divisor. These are direct consequences of the residue model.

For decimal strings, the derived changes are $(b-a)10^k$ and, up to the selected digit/sign convention, $9(a-b)10^k$. In particular, modulus 11 detects every modeled substitution and unequal adjacent transposition at every finite width: the possible nonzero digit differences are not divisible by 11, and 10 and 9 are units modulo 11. This is a proof for the stated event classes, not a claim about arbitrary alterations.

## 5. Finite-Alphabet Counting

For radix $q$, let $W_q(h)$ count ordered unequal digit pairs $(a,b)$ from $\{0,\ldots,q-1\}$ whose difference is divisible by $h$. For $1\le h\le q-1$,

$$
W_q(h)=2\sum_{j=1}^{\lfloor(q-1)/h\rfloor}(q-hj),
$$

and $W_q(h)=0$ for $h>q-1$. For a positive difference $hj$, there are $q-hj$ possible smaller digits and two orientations. The zero tail occurs because no nonzero difference between alphabet digits can be a multiple of a divisor greater than the maximum difference.

For decimal digits this becomes $W(h)=2\sum_{j=1}^{\lfloor9/h\rfloor}(10-hj)$ for $1\le h\le9$, and $W(h)=0$ for $h>9$. This count is an observable of the finite digit alphabet: values above its threshold all map to zero. A compact expression for the count does not by itself establish novelty.

## 6. Position-Dependent Spectra

The number of undetected ordered digit pairs at position $k$ is given by the substitution and transposition spectra

$$
S_{m,q}(k)=W_q\!\left(\frac{m}{\gcd(m,q^k)}\right),\qquad
T_{m,q}(k)=W_q\!\left(\frac{m}{\gcd(m,(q-1)q^k)}\right).
$$

Position matters because the place value $q^k$ changes the effective divisibility condition. The reduced divisor retains arithmetic information before counting. The observable spectrum retains only the count after applying $W_q$; when a reduced divisor exceeds $q-1$, its count is zero and the exact divisor is not recoverable from that position's count alone.

## 7. Radix Generalization

R11 develops the same fixed-width analysis for each integer radix $q\ge2$. It defines the finite-alphabet count $W_q$, derives the two spectra above, and describes their stabilization using prime valuations of the modulus and radix. The spectra stabilize once the powers of primes shared with $q$ have been canceled from the reduced divisors; the endpoint used for a bounded comparison is the maximum stabilization position in that modulus range.

R11 also derives finite-length event totals and undetected counts. For length $n$, the total substitution events are $E_s=n(q-1)q^n$, and the total unequal adjacent-transposition events are $E_t=(n-1)(q-1)q^{n-1}$ for $n\ge2$ (zero at $n=1$). The undetected totals are

$$
U_s=q^{n-1}\sum_{k=0}^{n-1}S_{m,q}(k),\qquad
U_t=q^{n-2}\sum_{k=0}^{n-2}T_{m,q}(k)\quad(n\ge2).
$$

Detected totals equal total minus undetected; rates divide by total when the event count is nonzero. These are the project's generalized formulations within this model, not a claim that radix-generalized check analysis is new.

## 8. Spectrum Equivalence and Identifiability

The observable spectra do not always identify the underlying modulus. Distinct moduli can have identical substitution and transposition count spectra even when their reduced divisors differ. The reason is the finite-alphabet threshold: $W_q$ is injective on its positive range $1\le h\le q-1$, but every $h>q-1$ is observed as zero. At each position, reduced divisors can therefore be distinguished when their values are within the observable range, while distinct values in the zero tail are indistinguishable by that count.

R11 proves the thresholded-observation criterion under the stated model; R12 develops the identifiability analysis. All-zero spectra discard especially much reduced-divisor information. Nonzero spectrum entries can reveal in-range reduced divisors and thus provide more information, but they do not guarantee unique recovery of a modulus. R12 gives examples of equal nonzero joint spectra for distinct moduli. Its bounded enumeration demonstrates instances over the configured finite domain; the general criteria are argued mathematically in the research notes.

## 9. Implementation

The `modular_error_detection` package separates decimal analytical profiles from radix enumeration:

- `profiles.py` computes exact decimal position and length profiles, event counts, rates, and reduced divisors.
- `radix_spectra.py` computes $W_q$, position spectra, stabilization positions, and deterministic classes of moduli with matching selected spectra.
- `experiments/reproduce_r12_radix_spectra.py` uses the existing radix API to calculate the bounded R12 table and writes CSV to standard output.

The corresponding tests include `tests/test_detection_profiles.py`, `tests/test_radix_spectra.py`, and `tests/test_r12_reproduction.py`. The financial-data workbench in the repository is a separate package and is not part of this mathematical implementation.

## 10. Independent Validation

The project uses several validation routes with different scope:

1. Exact analytical formulas derive counts and rates from the model.
2. The profile and spectrum implementations encode those formulas for decimal and radix cases.
3. Direct digit-pair enumeration compares independently computed small cases against the radix spectra implementation. This is **moderate** in scope: it uses a separate calculation route, but covers only small radix/modulus ranges. It is not an independent proof of every theorem.
4. The exhaustive decimal sweep enumerates the configured finite set of strings and errors and reconciles per-length data with aggregate results.
5. The bounded radix experiment groups moduli by computed spectrum tuples and reproduces the R12 table.

Agreement among computations supports implementation checks within tested domains. General claims rely on their derivations and assumptions, not on finite agreement alone.

## 11. Exhaustive Decimal Validation

The exhaustive experiment uses radix 10, fixed-width strings of lengths 1–4, and moduli 2–30. It enumerates single substitutions and unequal adjacent transpositions, retaining leading-zero positions, and analyzes results by position and length before aggregation. The saved CSV has 232 per-length rows; the Markdown report has 58 modulus/error-type aggregate rows. Analytical event counts and rates were reconciled against these results in the existing validation artifacts.

At length one, the transposition event set is empty, so its rate is undefined rather than zero. Aggregate rates pool event counts across lengths rather than averaging per-length rates. These reports establish results for this finite sweep only; the all-finite-length modulus-11 statement comes from the separate mathematical argument.

## 12. Bounded Radix Experiments

The R12 computation covers radices $2,3,4,5,6,7,8,9,10,11,12,16,20$ and moduli 2 through 5000 inclusive. It groups moduli by substitution-only, transposition-only, and joint spectrum, and reports the size of the all-zero joint class. The checked-in reproduction script uses the maximum stabilization position over each modulus interval as its inclusive endpoint.

The recorded comparison reports that every one of the 13 computed rows matched the documented R12 table. The following are bounded computational observations, not universal theorems:

| Radix | Substitution classes | Transposition classes | Joint classes | Zero-joint class size |
|---:|---:|---:|---:|---:|
| 2 | 13 | 13 | 13 | 4,987 |
| 3 | 16 | 16 | 23 | 4,977 |
| 4 | 19 | 20 | 30 | 4,966 |
| 5 | 21 | 21 | 35 | 4,961 |
| 6 | 38 | 37 | 58 | 4,877 |
| 7 | 26 | 25 | 45 | 4,943 |
| 8 | 29 | 29 | 48 | 4,933 |
| 9 | 32 | 29 | 57 | 4,910 |
| 10 | 62 | 55 | 103 | 4,811 |
| 11 | 33 | 32 | 59 | 4,923 |
| 12 | 56 | 55 | 88 | 4,784 |
| 16 | 47 | 44 | 90 | 4,816 |
| 20 | 84 | 83 | 129 | 4,725 |

The complete run and row-by-row comparison are recorded in R16. This summary does not claim that the experiment proves behavior outside those radices and moduli.

## 13. Reproducibility

The reproduction script is deterministic, calls the existing `radix_spectra` implementation, computes its statistics for the stated bounded domain, and prints CSV to standard output. It does not require network access, randomness, or stored result files. The project package must be installed as described in the README so the script can import it.

The R12 output is an executable reproduction of a finite table. It is separate from the analytical proofs and does not extend their scope. Ordinary tests exercise small domains; the full R12 computation is an explicit command rather than part of the routine test suite.

## 14. Literature Boundary

There is substantial prior work on error-detecting codes, check-digit systems, weighted modular checks, decimal error detection, single-error and adjacent-transposition detection, and equivalence or classification of check systems. The repository's literature records discuss Hamming, Verhoeff, Gumm, Damm, Schulz, ISO/IEC 7064, and Luhn within the limits of the sources they report reviewing.

Verhoeff is a close prior analogue for decimal weighted checks and error-rate/classification work. The exact relationships between this project's formulation and Gumm or Damm remain unresolved because their full primary texts were not verified in the documented review. The repository does not claim that its exact formulas are absent from the literature; the reviewed literature matrix and access notes describe the evidence limits.

The repository does not establish a novelty claim. Its contribution should currently be understood as a systematic, reproducible computational-mathematics investigation and implementation of the stated model.

## 15. Research Limitations

- The model uses fixed-width strings and only single substitutions and unequal adjacent transpositions.
- The finite-alphabet count can conceal distinct reduced divisors above its threshold.
- The decimal sweep and R12 radix experiment cover bounded computational domains.
- Independent direct digit-pair validation is moderate and limited to small parameter ranges; it is not a separate exhaustive proof of every theorem.
- Exact comparison with some prior group-based systems, particularly Gumm and Damm, remains unresolved in the reviewed records.
- No novelty or publication-priority claim is established.
- The financial-data workbench is separate and is not part of the mathematical contribution.

## 16. Current Research Position

The mathematical model is established, and its main formulas are implemented. The core formulas have multiple forms of validation, including direct small-domain digit-pair checks and reconciliation with the exhaustive decimal results. The radix generalization is implemented. Observable-spectrum equivalence and identifiability limits have been characterized within the stated model. The bounded R12 computational experiment has a checked-in reproduction path and is reported to match every documented row.

The literature boundary has been investigated, but it does not support a novelty claim. The project is best positioned as a reproducible computational-mathematics research artifact rather than a claimed new theorem.

## 17. Repository Research Map

The summary is the researcher-facing entry point. The detailed records remain available for proof, implementation, evidence, and chronology:

**Foundation**

- [Formal model](formal_model.md)
- [Literature matrix](literature_matrix.md)
- [Theorem review](theorem_review.md)

**Research development and history**

- [Research direction](research_direction.md)
- [R9 research decision](r9_research_decision.md)
- [R10 count-spectrum theorem](r10_count_spectrum_theorem.md)
- [R11 radix generalization](r11_radix_generalization.md)
- [R12 identifiability](r12_identifiability.md)

**Prior-art boundary**

- [Prior-art claim matrix](prior_art_claim_matrix.md)
- [Deep prior-art comparison](deep_prior_art_comparison.md)
- [R7 novelty boundary](novelty_boundary.md)
- [R8 novelty boundary](novelty_boundary_r8.md)

**Audits and consolidation**

- [R13 artifact audit](r13_research_artifact_audit.md)
- [R15 working-tree audit](r15_working_tree_audit.md)
- [R16 consolidation record](r16_consolidation_record.md)
- [R17 consistency audit](r17_final_consistency_audit.md)
- [R18 final consolidation record](r18_final_consolidation_record.md)
- [Research summary](research_summary.md)

**Implementation and verification**

- [`modular_error_detection` package](../python/modular_error_detection)
- [Detection-profile tests](../tests/test_detection_profiles.py)
- [Radix-spectrum tests](../tests/test_radix_spectra.py)
- [R12 reproduction test](../tests/test_r12_reproduction.py)
- [R12 reproduction script](../experiments/reproduce_r12_radix_spectra.py)

R9–R17 are research-development and audit records, not all current recommendations. This summary is the concise entry point; the earlier files preserve the chronology and supporting detail.

## 18. Reproduction Commands

From the repository root, install the project and development test dependency in the active Python environment:

```powershell
python -m pip install -e ".[dev]"
```

Run the ordinary tests with the repository virtual environment and its workspace-local pytest temporary directory:

```powershell
& ".\.venv\Scripts\python.exe" -m pytest -p no:cacheprovider --basetemp ".r16-pytest-tmp"
```

Reproduce the complete bounded R12 experiment with the same installed environment:

```powershell
& ".\.venv\Scripts\python.exe" experiments/reproduce_r12_radix_spectra.py
```

The first command installs the local package in editable mode with the `dev` extra from `pyproject.toml`. The test command runs pytest. The reproduction command prints its deterministic CSV table to standard output; it does not regenerate the historical decimal reports or plots.
