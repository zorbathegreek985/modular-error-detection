# R9 Primary-Source Resolution and Research-Gap Decision

> Historical research-decision document. It records the status and recommendation at R9; R12 is the later decision record for the count-spectrum identifiability line.

## Decision summary

The repository’s core mathematics is a plain weighted modular checksum specialization, with exact event counts derived from the chosen decimal event model. The algebra is sound and reproducible, but the reviewed evidence does not establish a differentiated research contribution. Gumm’s and Damm’s primary articles could not both be inspected in full. Their accessible records nevertheless make clear that closely related check-character guarantees and group-based constructions are established prior art.

**Recommendation:** keep the project primarily as research software and a reproducible educational study for now. Do not frame the present work as a research paper contribution. One limited mathematical question remains suitable for exploratory analysis: classify moduli by their count-only error spectra and determine whether that classification yields more than a finite restatement of the existing formulas. It is not yet a paper-level gap.

This decision uses the repository’s [formal model](formal_model.md), [profile-engine description](detection_profile_engine.md), [R8 comparison](deep_prior_art_comparison.md), and [R8 novelty boundary](novelty_boundary_r8.md). No code or experiment was run or changed for this phase.

## Gumm primary-source status

### Access

Gumm’s university publication page identifies the 1985 article and links an author-hosted four-page PDF. The PDF endpoint was reachable during this review, but the web document reader exposed zero text lines; page screenshots also did not return readable content. I therefore could not inspect the full 1985 article, its pages, equations, or theorem statements. The publisher full text was not available in the accessible view. The [author publication list](https://www.mathematik.uni-marburg.de/~gumm/Papers/publ.html) confirms the citation and provides the link to the paper. The DOI is [10.1109/TIT.1985.1056991](https://doi.org/10.1109/TIT.1985.1056991).

Gumm’s author-hosted 1986 follow-up, “Encoding of Numbers to Detect Typing Errors,” was text-indexed and exposes a construction and proof sketch. It describes a check digit appended to a number, using a dihedral-group operation on decimal digits and position-dependent permutations. Its Theorem 3.1 states a single-error and transposition guarantee under an anti-symmetry condition on the permutation; a decimal permutation is then verified for the dihedral operation. This follow-up is useful primary-source evidence about Gumm’s group construction, but it is a different paper and does not substitute for reading the 1985 article. [Author-hosted 1986 follow-up](https://www.mathematik.uni-marburg.de/~gumm/Papers/EncodingOfNumbers.pdf).

### What can and cannot be concluded

The accessible abstract for the 1985 paper says that Gumm presents a single-check-digit method for number systems, using dihedral groups and suitable transformations in the stated important case of base `2r` with odd `r`, and that it detects single-digit errors and adjacent transpositions. The abstract does **not** establish an arbitrary scalar weighted-sum model, the project’s gcd tests, its pair-count formula, stabilization formulas, profile data structure, or modulus classes. The author-hosted follow-up confirms a group-valued, appended-check construction, not the project’s plain integer-residue computation.

The comparison with the project’s identities is therefore:

- Project weighted-sum changes are `Δ_s=(b-a)w_k` and `Δ_t=(a-b)(w_i-w_j)` modulo `m` (the transposition sign depends on the position convention). These follow by subtracting scalar weighted sums.
- With `w_k=10^k`, the adjacent positional difference is `9·10^k`.
- Gumm’s accessible follow-up uses group operations and permutations with an appended check character. It has analogous error classes and guarantees, but its objects are not the project’s scalar weights and residues. It is not justified to call the formulas equivalent based on the abstract or follow-up alone.
- The primary 1985 article’s exact definitions, assumptions, theorem locations, and relationship to earlier weighted-sum work remain **unverified**. No page or theorem citation is attributed to it here.

Thus Gumm is strong prior art for the broader goal of one check digit detecting single errors and adjacent transpositions in number systems. The evidence currently available does not show that the 1985 paper already states the project’s scalar weighted modular formulas. It also cannot establish that it does not.

## Damm primary-source status

Springer’s publisher page confirms the 2000 article and exposes its abstract, but marks the article as subscription content. The full paper was not lawfully accessible in the available view. No third-party copy was used. [Springer article page and abstract](https://link.springer.com/article/10.1007/s000130050524), DOI [10.1007/s000130050524](https://doi.org/10.1007/s000130050524).

The publisher abstract establishes that Damm studies check-digit systems over groups; states an existence criterion in terms of anti-symmetric mappings for detecting all single errors and adjacent transpositions; discusses anti-(auto)morphisms and constructions of anti-symmetric mappings; gives an upper bound on their number; and treats sign structures and dihedral groups. This is an abstract-level account only. The exact definitions, proof details, theorem numbering, classification scope, and any equivalence relation used in the paper remain unverified.

Schulz’s accessible chapter supplies a secondary group-check framework and discusses structural equivalence of group permutations/check-character systems. That relation is not shown to equal the project’s proposed equality of observable profiles over integer moduli. The Damm abstract does not claim integer modular sums as a special case and does not establish the project’s `W(h)` or stabilization formulas. The primary article’s complete contents remain an explicit uncertainty.

## Established prior art and exact project relationship

The primary sources inspected in the preceding phases—especially Verhoeff’s treatment of weighted modular decimal checks—and the accessible Gumm and Damm abstracts establish that the project sits within a mature check-digit/error-detection field. Verhoeff explicitly analyzes weighted modular decimal systems, error conditions, rates, and computational search. Schulz studies group-based check systems and equivalence/classification questions. Gumm and Damm concern group constructions with check characters, not the same scalar-residue object.

For the project’s weighted sum `S(x)=Σw_i x_i mod m`, subtraction gives the substitution and transposition identities. Selecting `w_k=10^k` gives the project’s decimal residue checksum. GCD cancellation gives the necessary-and-sufficient miss conditions. These are direct specialization and elementary derivation, not a new error-detection mechanism.

The modulus-11 universal result is a proof for this project’s exact error model and decimal digits. It follows because nonzero digit differences have magnitude at most 9 and the relevant reduced factors are 11. It is consistent with established weighted-check criteria; it is not evidence for a new general guarantee. The finite sweep verifies the implementation over its configured range, not the all-length theorem.

## `W(h)` status

The project’s

\[
W(h)=2\sum_{j=1}^{\lfloor9/h\rfloor}(10-hj),\qquad 1\le h\le9,
\]

counts ordered unequal decimal digit pairs whose difference is divisible by `h`; `W(h)=0` for `h>9`. For a coefficient `q`, cancellation reduces `m | q(a-b)` to divisibility by `h=m/gcd(m,q)`, so the count is exactly `W(h)`.

The generic formula was not found explicitly in the sources inspected. Verhoeff gives scheme-specific weighted-check rates/counts, including a special case equivalent to `h=5`. The underlying count is implicit in counting digit pairs satisfying a weighted modular error condition. Therefore the precise conclusion is **generic formula not located; special cases and underlying counting idea have prior-art analogues**. This does not mean the formula is novel.

## Stabilization status

For `m=2^a3^b5^cu` with `gcd(u,30)=1`, the expressions

\[
h_s(m,k)=\frac{m}{\gcd(m,10^k)},\qquad
h_t(m,k)=\frac{m}{\gcd(m,9\cdot10^k)}
\]

stabilize for `k≥max(a,c)` at `3^b u` and `3^{b-min(b,2)}u`, respectively. These follow immediately by tracking the 2-, 3-, and 5-adic valuations of the coefficients. Equivalent statements were **not located in the literature reviewed**. Because the derivation is a short valuation calculation from the model, this absence does not establish a research gap.

## Profile and equivalence status

The project’s profile collects reduced divisors, `W(h)` values, event counts, and rates by position. Weighted-check literature already studies position-dependent error conditions and detection rates. The exact bundle was not located, but the bundle itself is a representation of known observables rather than a demonstrated theorem.

Equality of full reduced-divisor profiles is uninformative for classifying distinct moduli when the first substitution entry is `h_s(m,0)=m`: equal profiles then force the same modulus. A count-only or rate-only relation is nontrivial in principle, but it must specify the error types, position domain, denominator, event convention, and treatment of zero-event positions. Schulz’s structural equivalences and Verhoeff’s rate-preserving transformations are conceptual precedents; they are not automatically the same relation.

For the decimal event model, `W(h)` distinguishes `h=1,…,9` (each has a different positive count), while every `h>9` maps to zero. Thus a count spectrum loses the exact value of any reduced divisor above 9. Stabilization means that comparison over all positions reduces to a finite prefix plus the stable tail. These observations make an exact count-equivalence classification feasible, but also suggest it may be a compact consequence of the existing formulas rather than a deep new theory. No claim of a useful or publishable classification is made.

## Candidate research directions

| Candidate | Prior-art coverage | What remains | Assessment |
|---|---|---|---|
| **A. Exact spectra for arbitrary radix and modulus** | Weighted modular checks and generalized check-digit systems already treat broad positional weights; digit-pair counting is a direct finite difference-distribution problem. | A useful classification or theorem uniform in radix, alphabet, modulus, and event convention. | The basic formulas generalize by replacing 10 with radix `r` and counting allowed digit differences. Likely a restatement unless a nontrivial structure emerges. |
| **B. Exact probabilities for arbitrary weight sequences** | Weighted check-digit theory, including Verhoeff’s generalized positional weights, is established. | A restricted weight family with a new theorem, optimization criterion, or structural invariant. | Generalizing the formulas alone is not differentiated; it largely recreates established weighted-check analysis. |
| **C. Classification by identical observable spectra** | Verhoeff studies rate behavior and transformations; Schulz studies equivalence of group check systems. | Necessary and sufficient arithmetic conditions for distinct plain moduli to have identical count-only profiles under a precisely defined domain. | The only plausible narrow mathematical question among these options. It may still be a finite re-expression of `W(h)` and stabilization, and needs an initial result before it can justify a paper. |
| **D. Finite-length versus asymptotic stabilization** | The project already derives the exact eventual divisors; valuation arithmetic explains the finite transient. | A meaningful consequence beyond calculating the threshold `max(a,c)`. | The stated stabilization is already elementary. A paper would require a new consequence or a materially broader setting. |
| **E. Unified modular, weighted, and nonlinear framework** | Weighted sums, group check-character systems, and quasigroup schemes each have substantial existing theory. | A precise common theorem preserving the distinctions among their algebraic objects. | As phrased, too broad. Combining vocabularies or implementations would not itself provide a contribution. |

### Directions rejected as current paper pivots

- **Arbitrary radix/modulus alone:** the change formulas and pair counts follow from weighted-sum subtraction and finite difference multiplicities.
- **Arbitrary weight sequences alone:** this is the established weighted-check framework rather than a differentiator.
- **Stabilization alone:** the formulas are immediate valuation arithmetic; no nontrivial consequence is presently identified.
- **A broad “unified framework”:** it risks conflating scalar modular sums with noncommutative group or quasigroup check-character constructions.
- **More plots, larger sweeps, or a Python implementation of the formulas:** these improve software and reproducibility but do not supply a mathematical theorem or classification.

## Defensible next question and contribution threshold

The one question worth a bounded exploratory check is:

> **For which distinct moduli, if any, are the substitution and unequal-adjacent-transposition count spectra identical at every positional exponent under the project’s fixed decimal event conventions, when spectra record `W(h)` counts but omit the reduced divisor itself?**

Define

\[
Q_m(k)=\left(W\!\left(\frac{m}{\gcd(m,10^k)}\right),\;
W\!\left(\frac{m}{\gcd(m,9\cdot10^k)}\right)\right),\qquad k\ge0.
\]

Count-equivalence means `Q_m(k)=Q_{m'}(k)` for every `k≥0`. Since both components stabilize, a finite comparison suffices once a proved stabilization bound is reached. Since `W(h)=0` for all `h>9`, the observation map is many-to-one at large reduced divisors. A valid contribution would need to prove necessary and sufficient arithmetic conditions for this equivalence, establish whether distinct moduli actually occur, and show that the classification explains or predicts something not immediately given by evaluating the formulas.

### Minimum evidence required

**Mathematical:** prove the finite-prefix bound; characterize equality of the two `W` sequences; prove both directions of the classification; state all edge cases and denominator conventions. If the result reduces to a tautological finite algorithm without explanatory structure, stop treating it as a paper direction.

**Computational:** independently enumerate a declared bounded modulus range; compare every pair’s computed count spectra with the proposed theorem; include moduli around factors 2, 3, and 5 and around the `h=9/10` threshold; provide hand-checkable examples and deterministic code. Computation is verification and exploration, not proof of the all-moduli claim.

**Literature:** inspect the full Gumm (1985) and Damm (2000) primary texts through a lawful library or author route; search prior weighted-check classifications, rate-preserving transformations, and observable-spectrum terminology; follow relevant citations in Verhoeff and Schulz. Document searches and access limits. A bounded search still cannot prove absence.

Until these conditions are met, this question is exploratory and does **not** support a novelty claim or an assumption that the project should proceed toward a paper.

## Project disposition

Of the four proposed dispositions:

- **A. Continue toward a research paper:** not supported by current evidence.
- **B. Pivot to arbitrary radices or weights:** not recommended without a specific nontrivial theorem; the broad versions overlap established weighted-check theory.
- **C. Reframe as a computational/reproducibility study:** defensible if the purpose is explicitly educational or methodological and it is compared honestly with earlier computational analyses such as Verhoeff’s.
- **D. Remain primarily research software:** the best-supported current disposition. The repository provides tested, inspectable implementations, analytical cross-checks, reports, and a financial validation workbench. These are useful software artifacts without requiring a claim of mathematical novelty.

## Sources and access record

- Gumm, “A new class of check-digit methods for arbitrary number systems,” *IEEE Transactions on Information Theory* 31(1), 102–105 (1985), [author’s publication list and linked PDF](https://www.mathematik.uni-marburg.de/~gumm/Papers/publ.html), [DOI](https://doi.org/10.1109/TIT.1985.1056991). The four-page PDF endpoint was reached but could not be text-inspected with the available reader; the article’s full content remains unverified.
- Gumm, “Encoding of Numbers to Detect Typing Errors,” *International Journal of Applied Engineering Education* 2 (1986), 61–65, [author-hosted PDF](https://www.mathematik.uni-marburg.de/~gumm/Papers/EncodingOfNumbers.pdf). The author-hosted copy’s indexed text exposes its dihedral operation, permutation condition, check-digit theorem, and implementation discussion. It is a follow-up, not the 1985 article.
- Damm, “Check digit systems over groups and anti-symmetric mappings,” *Archiv der Mathematik* 75, 413–421 (2000), [Springer publisher page and abstract](https://link.springer.com/article/10.1007/s000130050524), [DOI](https://doi.org/10.1007/s000130050524). Full text was paywalled in the accessible publisher view.
- Schulz, “Check Character Systems and Anti-symmetric Mappings,” LNCS 2122 (2001), [author-hosted full text](https://page.mi.fu-berlin.de/rhschulz/digits.pdf), consulted for the group model and system-equivalence distinction.
- Verhoeff, *Error Detecting Decimal Codes*, Mathematical Centre Tract 29 (1969), [CWI repository scan](https://ir.cwi.nl/pub/32080/32080D.pdf), consulted in the relevant weighted modular sections as documented in [R8](deep_prior_art_comparison.md).

The review does not rely on unauthorized mirrors of either primary article. Secondary abstracts are used only for the claims they actually state.

## Remaining uncertainty

1. The exact contents and theorem statements of Gumm (1985) remain unverified despite reaching an author-hosted PDF.
2. Damm’s full definitions, proofs, and any equivalence notion in the 2000 article remain unverified; the publisher abstract and Schulz’s secondary discussion do not replace the article.
3. No complete literature search has established whether the generic `W(h)` formula, the stabilization formulas, or the count-only modulus classification appear elsewhere.
4. It is unknown whether count-equivalence yields distinct classes with a simple arithmetic characterization or only a tautological computation.
5. No claim is made that the existing project is novel or that no research paper could ever result from a future theorem.
