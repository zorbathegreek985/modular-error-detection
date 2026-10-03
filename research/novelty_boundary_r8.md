# R8 Novelty Boundary

> Historical literature-boundary snapshot from R8. R9 and R12 record later source-access and research-position decisions; retain this note as chronology, not as the latest status.

## Purpose and evidentiary limits

This note records what the reviewed sources support and what remains uncertain. “Not located” means that no matching statement was found in the sources and portions inspected; it does not mean that no such publication exists. The source-access details and claim-by-claim comparison are in [deep_prior_art_comparison.md](deep_prior_art_comparison.md).

## Claim-by-claim boundary

| Claim | Status after R8 review | Basis and limit |
|---|---|---|
| Modular checksum error detection is determined by a residue change. | **Established framework.** | The project is a weighted modular check with positional weights. Verhoeff explicitly studies weighted modular decimal checks. |
| A substitution changes the weighted sum by `(b-a)w_k`; an exchange in positions `i,j` changes it by `(a-b)(w_i-w_j)`, up to sign. | **Established identity; project specialization.** | Direct subtraction gives the identities. With `w_k=10^k`, the project’s formulas follow. They are elementary consequences of the weighted-sum model. |
| The project’s adjacent-swap coefficient is `9·10^k`. | **Direct specialization.** | `10^(k+1)-10^k=9·10^k`. This is not a separate checksum mechanism. |
| The gcd reductions give necessary and sufficient miss conditions. | **Elementary derivation.** | `m | qd` iff `m/gcd(m,q) | d`. No new number-theoretic method is involved. |
| `W(h)=2Σ(10-hj)` counts ordered unequal decimal pairs with difference divisible by `h`. | **Exact count derived; generic formula not located.** | The sum enumerates positive differences `hj≤9`, with `10-hj` pairs in each orientation. Verhoeff has related scheme-specific counts, including the `h=5` case; the general closed form was not found in inspected material. This is not a novelty claim. |
| The reduced divisors stabilize according to the 2-, 3-, and 5-adic factors stated in the project. | **Elementary valuation derivation; matching prior statement not located.** | The formulas follow by cancellation in `gcd(m,10^k)` and `gcd(m,9·10^k)`. The bounded literature review did not find them stated equivalently. |
| Modulus 11 detects every defined substitution and unequal adjacent transposition. | **Proven for the project model; a specialization of established weighted-check guarantees.** | The reduced coefficients exceed the largest decimal digit difference, or equivalently the nonzero adjacent weights differ modulo 11. Verhoeff discusses weighted modulus-11 conditions. The proof is general in string length, but not a new general detection principle. |
| The profile engine and finite sweep validate/illustrate these results. | **Reproducible implementation of the stated model.** | The engine is a computational organization and cross-check. The configured finite sweep does not prove claims beyond its finite parameters; the algebraic derivations do. Prior computational check-code search is documented by Verhoeff. |
| A position-resolved profile is a distinct mathematical object. | **Exact package not located; not established as a contribution.** | Verhoeff gives position-weight conditions, rates, and search results; Schulz classifies group-based check systems. The project’s tuple of reduced divisors/counts/rates is a convenient representation of familiar observables. |
| Moduli are equivalent when their observable profiles match. | **Definition is project-specific; equivalence as a research topic is established.** | Schulz studies equivalence of group permutations/check-character systems; Verhoeff studies rate-preserving transformations. The project’s comparison object differs, but defining equality of observables alone is not a result. Including `h(m,1,0)=m` makes full reduced-divisor profile equality force equal moduli. |
| Gumm or Damm already state the project’s scalar formulas. | **Unverified.** | Their primary full texts were not successfully inspected. Their accessible abstract/secondary-source evidence concerns group or dihedral check-character constructions, not a verified scalar weighted-sum theorem. No conclusion of absence or equivalence is justified. |

## Assessment of the combined work

The current mathematics is best described as a systematic derivation and computational presentation of a particular weighted modular checksum, together with exact event counts for the project’s event definitions. The substitution and transposition identities are standard weighted-sum subtraction; the gcd and stabilization results are elementary arithmetic; and the modulus-11 result is a specialization of known weighted-check conditions. The exact `W(h)` presentation and profile packaging were not located in the inspected literature, but their absence has not been established, and neither is by itself evidence of a differentiated research contribution.

Accordingly, the present combination is **not shown to be materially differentiated from established theory**. It has educational and reproducibility value. A stronger research claim would require a nontrivial theorem, an explanatory classification, or a demonstrated use that is not a restatement of the reduced-divisor formulas, plus a targeted literature review. The full Gumm (1985) and Damm (2000) articles remain key unresolved primary sources.

## Three candidate research questions

### 1. Count/rate-only equivalence classes of moduli

- **Question:** For a declared domain of moduli, when do two moduli have identical substitution and unequal-adjacent-transposition detected/undetected counts at every positional exponent, ignoring the reduced divisor itself?
- **Prior-art basis:** Verhoeff studies weighted-check detection rates and rate-preserving transformations. Schulz studies equivalence of group-based check systems and computed classes. Those are close analogues, but not the same objects or necessarily the same relation.
- **Known:** At exponent `k`, the project’s miss counts are `W(h_s(m,k))` and `W(h_t(m,k))`, with `h_s=m/gcd(m,10^k)` and `h_t=m/gcd(m,9·10^k)`. These sequences stabilize after the 2- and 5-adic factors in the coefficients have canceled.
- **Unknown:** Whether distinct moduli can have identical count/rate sequences for both error types, what arithmetic conditions characterize such pairs, and whether the resulting classes simplify or explain behavior beyond direct profile comparison.
- **Why meaningful:** It separates behavioral performance from the internal divisor parameter and could reveal genuinely indistinguishable checksum behaviors.
- **Proof/computation needed:** First define the position domain (all `k≥0` or a fixed maximum length) and event denominator. Prove a finite comparison bound from stabilization; derive necessary and sufficient conditions for equality of the two `W` sequences; independently enumerate a bounded set of moduli and compare with the theorem.
- **Paper potential:** Conditional. It could support a focused mathematical note if the classification is nontrivial and useful. Do not imply such classes exist before proving it.

### 2. Generic closed forms for digit-difference distributions

- **Question:** Which exact pair-count formulas hold for arbitrary radix `B`, allowed digit set, coefficient `q`, and modulus `m`, and how do they relate to prior weighted-check error statistics?
- **Prior-art basis:** Verhoeff gives weighted decimal error conditions and scheme-specific counts; the project’s `W(h)` is the decimal specialization of counting unequal pairs whose difference is divisible by a reduced divisor.
- **Known:** For decimal digits, direct summation yields the project formula. For another finite digit set, counts can be obtained by enumerating its difference multiplicities.
- **Unknown:** Whether a compact general expression provides insight beyond this elementary difference-distribution method, and whether existing literature already gives it in equivalent form.
- **Why meaningful:** A general exact count could make error-rate comparisons possible across radices and digit alphabets without repeating event enumeration.
- **Proof/computation needed:** State digit and event conventions; derive pair-difference multiplicities; prove the count formula; compare exact predictions against exhaustive enumeration for small radices and coefficients; complete a source review before making a contribution claim.
- **Paper potential:** Unclear. It is likely routine unless the result yields a substantially simpler classification or useful theorem.

### 3. Weighted positional checksum profiles beyond powers of the radix

- **Question:** For a specified family of weight sequences, can exact all-position single-substitution and adjacent-transposition profiles be classified arithmetically?
- **Prior-art basis:** Verhoeff explicitly treats generalized positional weights, weighted modular decimal checks, rate behavior, and computational search. Consequently, arbitrary weight sequences alone do not distinguish the project.
- **Known:** For weights `w_k`, the miss tests are `m | (b-a)w_k` and `m | (a-b)(w_k-w_{k+1})`.
- **Unknown:** Whether a tightly restricted family has a useful new classification, invariant, or optimization result beyond applying those tests.
- **Why meaningful:** A proved classification could explain design trade-offs for a defined family of linear checks.
- **Proof/computation needed:** Choose a mathematically motivated family and objective; establish exact divisibility criteria and classification; compare against known generalized-weight results; verify by finite exhaustive checks.
- **Paper potential:** Not established. A broad pivot to arbitrary weight sequences would largely recreate existing linear check-digit theory.

## Selected next direction

**Investigate count/rate-only equivalence classes of moduli for the two existing error models.** This direction stays within the project’s definitions, differs from the current equality of reduced-divisor profiles, and can be made precise using the exact `W` counts and stabilization results. It also has a direct comparison point in Verhoeff’s rate-preserving transformations and Schulz’s system-equivalence work.

The next work should begin with a formal definition of the observable (counts, rates, or both) and its position domain. For the strongest arithmetic formulation, define for `k≥0`

\[
P_m(k)=\bigl(W(m/\gcd(m,10^k)),\ W(m/\gcd(m,9\cdot10^k))\bigr),
\]

and call two moduli count-equivalent when these ordered pairs agree for every `k≥0`. Prove that checking a finite prefix suffices using stabilization, then determine whether distinct moduli can be equivalent and characterize them if so. If only rates are compared, denominators and zero-event conventions must be specified separately. This is a proposed question, not a claim that nontrivial classes exist or that the question is novel.

## Claims to avoid

Do not claim that the project:

- introduces weighted modular checksum theory or the first analysis of decimal substitutions/transpositions;
- provides a new modulus-11 guarantee or a new general universal-detection principle;
- is the first exhaustive or computational study of checksum behavior;
- introduces a novel `W(h)` theorem, stabilization theorem, detection profile, or equivalence theory;
- proves Gumm or Damm do or do not contain a particular formula, until their complete primary articles are lawfully accessed and inspected.

## Cautious contribution wording

The following wording is defensible as a description, not a novelty claim:

> This project gives an explicit derivation and tested implementation of exact substitution and unequal-adjacent-transposition counts for the plain decimal residue checksum under stated event-counting conventions. It relates those counts to reduced divisors and documents the finite sweep as a reproducible illustration of the formulas.

Any stronger statement about a contribution to the literature should wait for a nontrivial result and further primary-source review.

## Evidence required before a novelty claim

1. Lawfully obtain and inspect the complete Gumm (1985) and Damm (2000) articles, recording the exact definitions and theorem statements relevant to weighted checks, error counts, and equivalence.
2. Trace and inspect the pertinent predecessors cited by Verhoeff and the group-check literature; search by mathematical formulation as well as terminology.
3. Search specifically for the generic digit-difference count, equivalent error spectra, valuation/stabilization statements, and plain-modulus count/rate classification.
4. State search sources, queries, dates, inclusion criteria, and inaccessible records. A documented bounded search still cannot establish universal absence.
5. Prove that the selected result is not just an immediate specialization or restatement, and identify a use or insight that makes it mathematically meaningful.

## Source-access summary

- **Inspected in full for relevant sections:** Verhoeff’s 1969 monograph and Schulz’s 2001 chapter.
- **Partially accessed:** Gumm’s author-hosted 1985 PDF was located but could not be text-inspected; only abstract/indexed material and an author-hosted follow-up were usable. Hamming’s publisher record and a short open extract, the official ISO preview, ISBN Agency FAQ, Luhn patent, and Abdel-Ghaffar publisher abstract support only limited claims.
- **Not inspected in full:** Damm’s 2000 article; his dissertation PDF endpoint was inaccessible. Schulz’s chapter supplies secondary description of related group-theoretic results but does not replace the primary text.

See [deep_prior_art_comparison.md](deep_prior_art_comparison.md) for the comparison table, bibliographic links, citation-chain limits, and the detailed `W(h)`, stabilization, profile, and equivalence assessments.
