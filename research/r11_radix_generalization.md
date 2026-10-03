# R11 — Radix-Generalized Error Spectra

## 1. Motivation

R10 found that decimal count-spectrum equivalence is caused by applying a finite-alphabet pair count (W(h)) to reduced divisors: divisors above the largest allowed digit difference all become unobservable as zero. This note asks what is general to every radix and what follows specifically from decimal factorization.

The investigation derives the radix-(q) event spectra, proves the behavior of their pair-count function, gives prime-valuation stabilization, and runs a bounded exploration over the requested radices. It does not claim novelty or publication readiness.

## 2. General radix model

Let (q\ge2) be an integer radix, with digit alphabet

\[
\mathcal D_q=\{0,1,\ldots,q-1\}.
\]

For a fixed-width string (x=x_{n-1}\cdots x_0\in\mathcal D_q^n), preserve leading zeros and define

\[
N_q(x)=\sum_{k=0}^{n-1}x_kq^k,\qquad C_{m,q}(x)=N_q(x)\bmod m,
\]

where (m\ge2). Detection means that the altered string has a different residue modulo (m).

Changing a digit (a) at position (k) to (b) changes the value by

\[
\Delta_s=(b-a)q^k=dq^k.
\]

Swapping unequal digits (a,b) at adjacent positions (k+1,k) changes the value by

\[
\Delta_t=(a-b)(q^{k+1}-q^k)=(a-b)(q-1)q^k,
\]

up to the sign convention for (a-b). Equal adjacent digits are excluded because their swap is not a distinct error event.

## 3. Derivation of (W_q(h))

For a positive integer (h), define (W_q(h)) as the number of ordered unequal pairs ((a,b)\in\mathcal D_q^2) satisfying (h\mid(a-b)). Each possible positive absolute difference is (hj\le q-1). For fixed difference (hj), the smaller digit has (q-hj) possible values; there are that many pairs in each orientation. Therefore

\[
W_q(h)=2\sum_{j=1}^{\lfloor(q-1)/h\rfloor}(q-hj),\qquad 1\le h\le q-1.
\]

If (h>q-1), there is no nonzero digit difference divisible by (h), hence (W_q(h)=0). Writing (r=\lfloor(q-1)/h\rfloor\), the sum can also be written

\[
W_q(h)=2rq-h r(r+1).
\]

For (q=10), this is exactly the project’s decimal (W(h)), including (W(10,h)=0) for (h>9). Also (W_q(1)=q(q-1)), the number of ordered unequal digit pairs.

**Theorem 1 (strict decrease on the nonzero range).** For every integer (q\ge2), (W_q(h)) is strictly decreasing for integer (1\le h\le q-1). In particular, it is injective there, has no nonzero collisions, and all collisions between distinct positive inputs occur in the zero tail (h>q-1).

**Proof.** Let (F_q(h)=W_q(h)/2), and put (r_h=\lfloor(q-1)/h\rfloor). For (h<q-1), (r_{h+1}\le r_h) and (r_{h+1}\ge1). For every (1\le j\le r_{h+1}), both summands exist and

\[
q-hj>q-(h+1)j.
\]

Any additional summands of (F_q(h)) for (r_{h+1}<j\le r_h) are positive. Thus (F_q(h)>F_q(h+1)). At (h=q-1), (W_q(h)=2) while (W_q(q)=0), so the strict decrease reaches the zero tail. This proves the claim for all (q), not just the enumerated radices. \(\square\)

The threshold is the maximum nonzero digit difference (q-1). The loss of information above that threshold is a general finite-alphabet effect, not a decimal-specific property.

## 4. Substitution spectrum

For (m\ge2), define

\[
h_s(m,q,k)=\frac{m}{\gcd(m,q^k)}.
\]

The substitution is undetected exactly when (m\mid d q^k). GCD cancellation gives

\[
m\mid d q^k\iff h_s(m,q,k)\mid d.
\]

There are (W_q(h_s)) ordered unequal digit pairs with such a difference. Thus the undetected pair count at position (k) is (S_{m,q}(k)=W_q(h_s(m,q,k))). The complete substitution count spectrum is therefore

\[
S_{m,q}(k)=W_q\!\left(\frac{m}{\gcd(m,q^k)}\right),\qquad k\ge0.
\]

## 5. Transposition spectrum

Define

\[
h_t(m,q,k)=\frac{m}{\gcd(m,(q-1)q^k)}.
\]

The swap change is a nonzero digit difference times `(q-1)q^k`, up to sign. It is undetected exactly when `h_t` divides that difference. The complete unequal-adjacent-transposition count spectrum is

\[
T_{m,q}(k)=W_q\!\left(\frac{m}{\gcd(m,(q-1)q^k)}\right),\qquad k\ge0.
\]

### Finite-length event counts

At one substitution position in a length-(n) string, the other (n-1) digits have (q^{n-1}) choices, and the changed digit pair has (W_q(h_s)) choices. Hence the undetected count at that position is (q^{n-1}S_{m,q}(k)). Summing over positions gives

\[
U_s(m,q,n)=q^{n-1}\sum_{k=0}^{n-1}S_{m,q}(k).
\]

There are (q^n) source strings, (n) positions, and (q-1) distinct replacement digits, so the total number of substitution events is

\[
E_s(q,n)=n(q-1)q^n.
\]

For each adjacent pair, the remaining (n-2) digits have (q^{n-2}) choices, while (W_q(h_t)) counts ordered unequal source pairs whose swap is undetected. Thus, for (n\ge2),

\[
U_t(m,q,n)=q^{n-2}\sum_{k=0}^{n-2}T_{m,q}(k),\qquad
E_t(q,n)=(n-1)(q-1)q^{n-1}.
\]

Detected counts are (E-U); rates are ((E-U)/E) when (E>0). At length 1 there are no transposition events, so its rate is undefined (N/A), not zero. Leading zeros are included as ordinary fixed-width digit positions throughout.

## 6. Prime-factor structure

For each prime (p), write

\[
\alpha_p=v_p(q),\quad \beta_p=v_p(q-1),\quad \gamma_p=v_p(m).
\]

Since (gcd(q,q-1)=1), at most one of (alpha_p,\beta_p) is positive. The valuation identities are

\[
v_p(\gcd(m,q^k))=\min(\gamma_p,k\alpha_p),
\]

and

\[
v_p(\gcd(m,(q-1)q^k))=\min(\gamma_p,\beta_p+k\alpha_p).
\]

Consequently,

\[
v_p(h_s)=\gamma_p-\min(\gamma_p,k\alpha_p),\qquad
v_p(h_t)=\gamma_p-\min(\gamma_p,\beta_p+k\alpha_p).
\]

For the transposition expression, this includes immediate cancellation by (q-1) at (k=0) for its prime factors; the exponent formula remains valid for all primes.

There is also a direct relation between the two reduced divisors at the same position:

\[
h_t(m,q,k)=\frac{h_s(m,q,k)}{\gcd(h_s(m,q,k),q-1)}.
\]

Indeed, after writing (g=\gcd(m,q^k)), the quotients (m/g=h_s) and (q^k/g) are coprime. The extra factor (q-1) therefore cancels precisely the part of (h_s) sharing factors with (q-1). This proves the transposition reduction differs from the substitution reduction only by the stated factor.

Only primes dividing (q) can be progressively removed as (k) increases. A prime dividing (q-1) contributes a (k)-independent cancellation to (h_t), while primes dividing neither (q) nor (q-1) remain in both reduced divisors. Define

\[
K(q,m)=\max_{p\mid q}\left\lceil\frac{v_p(m)}{v_p(q)}\right\rceil,
\]

with zero contributions when (v_p(m)=0). Both reduced divisors are constant for (k\ge K(q,m)), and so are both spectra. The stable values are

\[
h_s^*(m,q)=\prod_{p\nmid q}p^{\gamma_p},\qquad
h_t^*(m,q)=\prod_{p\nmid q}p^{\gamma_p-\min(\gamma_p,\beta_p)}.
\]

The reduced divisors decrease to these stable values. Hence `S_{m,q}(k)` is zero for every `k` exactly when `h_s^*(m,q)>q-1`, and `T_{m,q}(k)` is zero for every `k` exactly when `h_t^*(m,q)>q-1`. Since `h_t^*` divides `h_s^*`, the joint spectrum is all zero exactly when `h_t^*(m,q)>q-1`. These are necessary-and-sufficient conditions for the all-zero classes at a fixed radix.

For decimal radix (q=10=2\cdot5), (q-1=9=3^2): powers of 2 and 5 are progressively canceled, while up to two powers of 3 are canceled immediately in the transposition divisor. The general statements are not decimal-specific; the prime factors and valuations change with (q).

## 7. Threshold and information-loss phenomenon

The arithmetic trajectory ((h_s,h_t)) is transformed into the observable pair spectrum by (W_q). By Theorem 1, at a fixed radix (q), a reduced divisor (h\le q-1) is recoverable exactly from its count; any (h>q-1) is observed only as zero. Thus two different reduced divisors at the same position are observationally indistinguishable exactly when both exceed (q-1).

For fixed (q), define two modulus spectra to be equal when both (S_{m,q}(k)) and (T_{m,q}(k)) agree for all (k\ge0). The exact criterion is: at every position, each corresponding pair of reduced divisors must either be the same value at most (q-1), or both be greater than (q-1). This follows from injectivity on the positive range and the zero tail. It is a finite comparison: for moduli (m,n), it suffices to check (k=0,\ldots,\max(K(q,m),K(q,n))), inclusive.

The zero-tail phenomenon is necessary for different reduced divisors to yield equal counts at a position. However, a joint spectrum can be nonzero while distinct moduli remain equivalent. In radix 11, moduli 14 and 35 both have (S(k)=0) for all (k), since (h_s=14) and (35), respectively, remain above the threshold 10. For both moduli, (h_t(k)=7) for every (k), because (gcd(14,10\cdot11^k)=2) and (gcd(35,10\cdot11^k)=5). Thus both transposition spectra are constantly (W_{11}(7)=8). Their joint spectra agree and are nonzero. This example follows directly from the formulas and also appears in the bounded enumeration.

Across different radices, raw pair counts have different alphabet-dependent denominators and are not by themselves a canonical measure of equal detection performance. Any cross-radix equivalence should first specify whether it compares raw counts, normalized rates, or another observable.

## 8. Computational exploration

I enumerated (q\in\{2,3,4,5,6,7,8,9,10,11,12,16,20\}) and (2\le m\le1000). For each ((q,m)), reduced divisors were calculated by integer gcd. (W_q(h)) was independently counted by testing all ordered digit pairs ((a,b)) directly for (a\ne b) and (h\mid(a-b)). Spectra were grouped within each fixed radix as tuples for (k=0,\ldots,9). This covers the whole sequence: for all listed (q) and (m\le1000), the valuation bound (K(q,m)\le9).

| Radix (q) | Distinct joint spectrum classes | All-zero moduli | Nonzero non-singleton classes | Largest nonzero class |
|---:|---:|---:|---:|---:|
| 2 | 10 | 990 | 0 | 1 |
| 3 | 19 | 981 | 0 | 1 |
| 4 | 23 | 974 | 3 | 2 |
| 5 | 28 | 969 | 3 | 2 |
| 6 | 44 | 921 | 20 | 5 |
| 7 | 34 | 956 | 8 | 3 |
| 8 | 40 | 949 | 7 | 3 |
| 9 | 45 | 932 | 12 | 6 |
| 10 | 77 | 884 | 24 | 6 |
| 11 | 45 | 939 | 12 | 3 |
| 12 | 66 | 870 | 28 | 8 |
| 16 | 72 | 870 | 21 | 10 |
| 20 | 94 | 841 | 32 | 6 |

**Computational observations, limited to this range:** each radix had one joint all-zero class; nonzero equivalence classes also occurred for several radices. Across the 13 tested radices, no distinct (h_1,h_2\in\{1,\ldots,q-1\}) had equal (W_q) values; Theorem 1 proves this for every radix. For (q=11), one nonzero class includes 14, 35, and 70, with substitution spectrum constantly zero and transposition spectrum constantly 8. These finite groupings do not establish an all-moduli classification.

If the ((q,m)) systems are pooled across radices by literal equality of raw count tuples, the bounded computation gives 468 keys among 12,987 systems, with one 12,076-member all-zero key and 51 other non-singleton keys that mix radices. This pooled relation is reported only to make the grouping convention explicit; it should not be interpreted as equal detection rates across different alphabet sizes.

The computation also checked strict decrease of the finite (W_q) tables for the listed radices. The proof in Section 3, not the enumeration, establishes the general theorem.

## 9. Theorem candidates

| Candidate | Outcome | Status |
|---|---|---|
| A. (W_q(h)) is strictly decreasing on (1\le h\le q-1). | True. | Theorem 1, proved for every integer radix. |
| B. All collisions of (W_q) arise from its zero tail. | True. | Follows from Theorem 1 and (W_q(h)=0) for (h>q-1). |
| C. The spectrum is determined by a finite valuation trajectory stabilizing at (K(q,m)=\max_{p\mid q}\lceil v_p(m)/v_p(q)\rceil). | True. | Direct valuation derivation in Section 6; (W_q) cannot delay stabilization. It may become constant earlier because of the zero tail. |
| D. Transposition differs from substitution through the extra factor (q-1). | True for this error model. | The two coefficients are (q^k) and ((q-1)q^k); their gcd valuations are stated in Section 6. |
| E. A complete arithmetic characterization of observable-spectrum equality exists. | True in a finite necessary-and-sufficient form; no compact classification of all classes is established here. | Apply Theorem 1 positionwise and check through the joint stabilization bound. This criterion is explicit but closely restates the observation map. |

## 10. Proofs and counterexamples

The proof of the pair-count formula and strict decrease is in Section 3. The residue-change identities and gcd cancellation prove the spectra in Sections 4–5. The prime-by-prime valuation calculation in Section 6 proves the stabilization statement. These are mathematical derivations, not computational observations.

The radix-11 pair (m=14,n=35) is a counterexample to the claim that identical joint spectra imply identical reduced-divisor trajectories. Their substitution reduced divisors are 14 and 35 at every (k), so both substitution counts are zero. Their transposition reduced divisors are both 7 at every (k), so both transposition counts are 8. The example has a proof from the formulas and is also present in the bounded enumeration.

No counterexample to strict decrease or injectivity of (W_q) on the nonzero range exists: Theorem 1 rules them out for all (q\ge2).

## 11. Prior-art comparison

The labels below describe the evidence actually reviewed, not conclusions about all literature.

| Source or area | Classification | What the reviewed evidence supports | Limit |
|---|---|---|---|
| Verhoeff, *Error Detecting Decimal Codes* (1969) | **CLOSE ANALOGUE** | Full text was inspected for weighted modular decimal systems, digit-error conditions, rates, and computational search. This is direct prior context for (q=10) and its weighted-check analysis. | Decimal focus; no claim that the exact radix-general (W_q) theorem was found there. [CWI record and scan](https://ir.cwi.nl/pub/32080/32080D.pdf). |
| Gumm, “A new class of check-digit methods for arbitrary number systems” (1985) | **CLOSE ANALOGUE; UNRESOLVED DUE TO ACCESS** | The accessible abstract describes a group/dihedral check-digit method for number systems with single-error and adjacent-transposition guarantees. A text-indexed author-hosted 1986 follow-up gives more detail about the group construction, but is a different paper. | The author-hosted 1985 PDF was reachable but not text-inspectable with the available reader; do not infer its exact results from the abstract. [Author publication list](https://www.mathematik.uni-marburg.de/~gumm/Papers/publ.html); [1986 follow-up](https://www.mathematik.uni-marburg.de/~gumm/Papers/EncodingOfNumbers.pdf). |
| Damm, “Check digit systems over groups and anti-symmetric mappings” (2000) | **RELATED BUT DIFFERENT; UNRESOLVED DUE TO ACCESS** | Publisher abstract describes group systems and anti-symmetric mappings for universal single and adjacent-transposition detection. | Full paper remains inaccessible; it is not evidence for the scalar (W_q) formulas. [Springer abstract](https://link.springer.com/article/10.1007/s000130050524). |
| Schulz, “Check Character Systems and Anti-symmetric Mappings” (2001) | **RELATED BUT DIFFERENT** | Accessible chapter treats group check equations and equivalence of group-based check-character systems. | The objects are not the scalar modular residue spectra studied here. [Author-hosted chapter](https://page.mi.fu-berlin.de/rhschulz/digits.pdf). |
| ISO/IEC 7064 | **RELATED BUT DIFFERENT** | ISO’s official description covers numeric, alphabetic, and alphanumeric strings and pure/hybrid check-character systems, with error-detection requirements. | It is a standard for appended check characters; the abstract does not establish the exact (W_q) pair count or this no-check-character residue comparison. [Official ISO page](https://www.iso.org/standard/31531.html). |
| Weighted modular check-digit systems | **EXACT MATCH (for the weighted-sum error-change identities)** | For a linear weighted residue, coordinate changes are determined by weighted digit differences. Choosing weights (q^k) gives these radix formulas. Verhoeff supplies inspected decimal weighted-check prior art. | The project omits an appended check character and counts fixed-width source/error events; not every check-digit implementation has these same semantics. |
| General radix / number-system check-digit literature | **CLOSE ANALOGUE; SPECIFIC OVERLAP UNRESOLVED** | Gumm’s accessible abstract explicitly addresses arbitrary number systems, but via a group construction; later general-group schemes also exist. | The 1985 full text was not inspected, and a broad literature search is not complete. The exact relation to this scalar framework cannot be settled from accessible abstracts. |
| Exact generic formula (W_q(h)) and strict-decrease proof | **NOT LOCATED in the reviewed materials** | This note derives both directly from the finite digit set. | Not located is not evidence of novelty; no exhaustive literature search was performed. |

The formulas are elementary consequences of positional notation, gcd cancellation, and a finite digit-pair count. Prior work on weighted check systems is sufficiently close that radix generalization alone should not be presented as a differentiated result. Gumm and Damm remain important unresolved primary sources; their inaccessible full text is not treated as proof of either overlap or absence.

## 12. Research-contribution assessment

**Classification: C. Elementary restatement of known weighted-checksum theory.**

The radix formulas follow from replacing the decimal positional weight (10^k) by (q^k). The swap coefficient is the difference of adjacent weights, ((q-1)q^k). The pair-count formula is a direct count over a finite alphabet. Strict decrease follows from a termwise comparison. Prime stabilization is a valuation calculation. Together these form a useful exact framework, but the current results do not require a non-obvious theorem beyond the derived elementary statements.

This assessment is about the mathematical differentiation test, not the value of the code or the correctness of the analysis. The generalized results may be useful as educational documentation or software support. No claim of novelty or publication readiness is made.

## 13. Possible research pivots

1. **Finite-alphabet identifiability:** For fixed (q), classify the exact preimage sets of the map from modulus (m) to its joint observable spectrum, and determine which arithmetic factors are identifiable from nonzero positions versus hidden by the (h>q-1) tail. The basic threshold is already understood; a meaningful result would need a compact classification with explanatory consequences beyond applying the finite-prefix criterion.
2. **Constrained modulus design:** For fixed (q), maximum width (n), and modulus bound (m\le M), characterize moduli maximizing the minimum of substitution and unequal-adjacent-transposition detection rates. This has a concrete objective, but optimization of check-digit performance has prior literature; a source review and a nontrivial structural theorem would be necessary before treating it as a research gap.

Neither direction is selected as a paper topic. The first is closest to the observed information-loss structure; it should be pursued only if a complete arithmetic classification proves simpler or more explanatory than the finite observable criterion.

## 14. Limitations

- The computational exploration covers only the 13 listed radices and moduli through 1000.
- The spectra cover only single substitutions and unequal adjacent transpositions on fixed-width strings.
- The all-position sequence is not a probability distribution; rates require a specified event denominator, as in the finite-length formulas.
- For length 1, transposition has no events and its rate is undefined.
- Raw spectra from different radices are not directly comparable without defining a normalization.
- The literature review is bounded. The full Gumm (1985) and Damm (2000) articles remain uninspected; no absence or exact overlap claim is made for their inaccessible details.
- No source code, tests, existing reports, plots, or financial workbench files were changed, and no project test suite was run.

## 15. Recommended next action

Do not expand the implementation or present radix generalization alone as a research contribution. If there is continued mathematical interest, pursue the finite-alphabet identifiability question only as a bounded theorem exercise: derive a full parameter classification for the thresholded valuation trajectories, compare it with the finite-prefix criterion, and stop if it yields no simpler explanatory result. Before making any stronger literature claim, obtain lawful full-text access to Gumm (1985) and Damm (2000) and compare their exact constructions and theorems.
