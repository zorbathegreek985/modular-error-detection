# Formal Model for Modular Error Detection in Decimal Strings

## 1. Scope and purpose

This document formalizes the residue comparison studied by this project. The objects are fixed-width decimal strings and two transformations: one-digit substitution and unequal adjacent transposition. The model asks whether a transformation changes the integer residue modulo a specified integer.

This is not a cryptographic authentication scheme, fraud-detection system, error-correcting code, or general-purpose check-digit standard. It has no appended check digit and does not identify or repair an error. It does not assign probabilities to errors without an explicit probability measure. Nothing here is a claim about real-world error frequencies or novelty.

## 2. Basic definitions

Let the decimal digit alphabet be

\[
\mathcal D=\{0,1,\ldots,9\}.
\]

For an integer length \(n\geq 1\), a fixed-width decimal string is an element

\[
x=x_{n-1}x_{n-2}\cdots x_1x_0\in\mathcal D^n,
\]

where \(x_k\) is the digit in place \(10^k\). The width is part of the object: strings with leading zeros remain distinct strings even if their integer values coincide with those of shorter strings. All transformations below preserve width.

The positional value map is

\[
N_n(x)=\sum_{k=0}^{n-1}x_k10^k\in\mathbb Z_{\geq0}.
\]

For an integer modulus \(m>1\), define the residue (or checksum) function

\[
C_m(x)=N_n(x)\bmod m\in\{0,1,\ldots,m-1\}.
\]

An **error transformation** is a specified map on strings in \(\mathcal D^n\). An **error event** includes a source string and the particular transformation applied to it. Two event descriptions are counted as distinct when their source or transformation choice differs, even if they happen to produce the same altered string.

For source \(x\) and transformed string \(y\) of the same width, the event is **detected modulo \(m\)** when \(C_m(y)\ne C_m(x)\), equivalently when \(m\nmid N_n(y)-N_n(x)\). It is **undetected** when the residues are equal, equivalently when \(m\mid N_n(y)-N_n(x)\). The model does not designate a set of valid strings; it compares the source and altered residues.

## 3. Error event sets

### A. Single-digit substitutions

For fixed \(n\), define a substitution event as a tuple \((x,k,b)\) with \(x\in\mathcal D^n\), \(0\leq k<n\), and \(b\in\mathcal D\setminus\{x_k\}\). The source digit is \(a=x_k\); the altered string \(y\) has \(y_k=b\) and \(y_i=x_i\) for all \(i\ne k\). Thus every source string, position, and different replacement digit is a separate event.

### B. Unequal adjacent transpositions

For fixed \(n\), define an adjacent-transposition event as a tuple \((x,k)\) with \(x\in\mathcal D^n\), \(0\leq k<n-1\), and \(x_k\ne x_{k+1}\). The altered string exchanges those two digits and leaves every other position unchanged. Equal adjacent digits are excluded because their exchange leaves the string unchanged. For \(n=1\), the event set is empty.

Insertions, deletions, non-adjacent transpositions, multiple simultaneous changes, and arbitrary adversarial modifications are outside this model.

## 4. Fundamental divisibility lemma

**Lemma 1 (cancellation by a gcd).** Let \(m>1\), let \(q\ne0\) be an integer, and let \(d\in\mathbb Z\). Then

\[
m\mid qd\quad\Longleftrightarrow\quad \frac{m}{\gcd(m,q)}\mid d,
\]

where \(\gcd(m,q)\) is positive.

**Proof.** Let \(g=\gcd(m,q)\), \(m'=m/g\), and \(q'=q/g\). Then \(\gcd(m',q')=1\) and

\[
m\mid qd\quad\Longleftrightarrow\quad gm'\mid gq'd\quad\Longleftrightarrow\quad m'\mid q'd.
\]

Since \(m'\) and \(q'\) are coprime, Euclid's lemma gives \(m'\mid q'd\) iff \(m'\mid d\). Substituting \(m'=m/\gcd(m,q)\) proves both directions. \(\square\)

For either error class, let \(c=1\) for substitution and \(c=9\) for adjacent transposition. Applying Lemma 1 with \(q=c10^k\) gives

\[
m\mid cd10^k\quad\Longleftrightarrow\quad h_{m,c}(k):=\frac{m}{\gcd(m,c10^k)}\mid d.
\]

## 5. Position-wise necessary and sufficient conditions

**Theorem 1 (substitution at a fixed position).** Fix \(m>1\), \(n\geq1\), and a position \(k\) with \(0\leq k<n\). If the source digit is \(a\), the replacement digit is \(b\ne a\), and \(d=b-a\), then the substitution is undetected modulo \(m\) if and only if

\[
m\mid d10^k,
\]

equivalently, if and only if \(m/\gcd(m,10^k)\mid d\).

**Proof.** Only the \(k\)-th digit changes, so

\[
N_n(y)-N_n(x)=b10^k-a10^k=(b-a)10^k=d10^k.
\]

By definition, the event is undetected exactly when this difference is divisible by \(m\). Lemma 1 gives the equivalent gcd condition. \(\square\)

**Theorem 2 (unequal adjacent transposition at a fixed pair).** Fix \(m>1\), \(n\geq2\), and an adjacent pair of positions \(k+1,k\), where \(0\leq k<n-1\). Let the source digits be \(x_{k+1}=a\), \(x_k=b\), with \(a\ne b\), and define \(d=b-a\). After swapping them, the event is undetected modulo \(m\) if and only if

\[
m\mid 9d10^k,
\]

equivalently, if and only if \(m/\gcd(m,9\cdot10^k)\mid d\).

**Proof.** After the swap, the higher-place digit is \(b\) and the lower-place digit is \(a\). Therefore

\[
\begin{aligned}
N_n(y)-N_n(x)
&=b10^{k+1}+a10^k-a10^{k+1}-b10^k\\
&=(b-a)(10^{k+1}-10^k)\\
&=9d10^k.
\end{aligned}
\]

The event is undetected exactly when the difference is divisible by \(m\). Lemma 1 gives the stated necessary-and-sufficient condition. \(\square\)

The sign convention is fixed by \(d=b-a\) in both theorems. Reversing the convention would negate the difference but would not change divisibility.

## 6. Universal detection conditions for substitutions

For a fixed position \(k\), write

\[
r_k^{(s)}=\frac{m}{\gcd(m,10^k)}.
\]

Every nonzero difference of two decimal digits is one of \(-9,\ldots,-1,1,\ldots,9\), and every such difference is realizable by a digit pair.

**Theorem 3 (all substitutions at a fixed position).** Fix \(m>1\) and \(k\geq0\). Every possible nonzero single-digit substitution at position \(k\) is detected modulo \(m\) if and only if

\[
r_k^{(s)}>9.
\]

**Proof.** By Theorem 1 and Lemma 1, an event with difference \(d\) is undetected exactly when \(r_k^{(s)}\mid d\). If \(r_k^{(s)}>9\), no nonzero \(d\) with \(|d|\leq9\) can be divisible by it. Conversely, if \(r_k^{(s)}\leq9\), choose the digit pair \((a,b)=(0,r_k^{(s)})\), which is allowed and has difference \(d=r_k^{(s)}\). This event is undetected. Thus the condition is necessary as well as sufficient. \(\square\)

**Corollary 3.1 (fixed length).** For fixed \(m>1\) and length \(n\geq1\), every substitution event at every position is detected if and only if

\[
\frac{m}{\gcd(m,10^{n-1})}>9.
\]

Indeed, \(r_k^{(s)}\) is nonincreasing as \(k\) increases, so its minimum over \(0\leq k<n\) is at \(k=n-1\). This statement quantifies over every source string and every different replacement at all positions of this fixed width.

**Corollary 3.2 (all finite lengths).** For fixed \(m>1\), every substitution event at every position for every finite length is detected if and only if

\[
\frac{m}{2^{v_2(m)}5^{v_5(m)}}>9,
\]

where \(v_p(m)\) is the exponent of prime \(p\) in \(m\), with exponent zero if \(p\nmid m\).

**Proof.** Factor \(m=2^a3^b5^c u\), where \(a,b,c\geq0\) and \(\gcd(u,30)=1\). Then

\[
r_k^{(s)}=2^{a-\min(a,k)}3^b5^{c-\min(c,k)}u.
\]

These values are nonincreasing in \(k\) and eventually equal \(3^bu=m/(2^a5^c)\). Theorem 3 holds for every finite position iff this eventual minimum exceeds 9. If it is at most 9, that value is attained at some finite \(k\), and Theorem 3 supplies an undetected allowed substitution there. \(\square\)

## 7. Universal detection conditions for unequal adjacent transpositions

For a fixed pair whose lower-place index is \(k\), define

\[
r_k^{(t)}=\frac{m}{\gcd(m,9\cdot10^k)}.
\]

Every nonzero difference \(d\in\{-9,\ldots,-1,1,\ldots,9\}\) is realizable by an unequal adjacent digit pair.

**Theorem 4 (all unequal swaps at a fixed pair).** Fix \(m>1\), \(n\geq2\), and \(0\leq k<n-1\). Every unequal adjacent transposition at this pair of positions, over every source string, is detected modulo \(m\) if and only if

\[
r_k^{(t)}>9.
\]

**Proof.** Theorem 2 and Lemma 1 say an event is undetected exactly when \(r_k^{(t)}\mid d\). If \(r_k^{(t)}>9\), no allowed nonzero difference is divisible by it. If \(r_k^{(t)}\leq9\), the unequal pair \((a,b)=(0,r_k^{(t)})\) realizes \(d=r_k^{(t)}\), giving an undetected event. \(\square\)

**Corollary 4.1 (fixed length).** For fixed \(m>1\) and \(n\geq2\), every unequal adjacent transposition at every pair is detected if and only if

\[
\frac{m}{\gcd(m,9\cdot10^{n-2})}>9.
\]

The sequence \(r_k^{(t)}\) is nonincreasing, so the last pair, with lower-place index \(n-2\), gives the minimum. When \(n=1\), the transposition event set is empty; universal detection is vacuously true, but its detection rate is undefined (N/A), not 100%.

**Corollary 4.2 (all finite lengths).** For fixed \(m>1\), every unequal adjacent transposition at every position for every finite length \(n\geq2\) is detected if and only if

\[
\frac{m}{2^{v_2(m)}5^{v_5(m)}3^{\min(v_3(m),2)}}>9.
\]

**Proof.** Write \(m=2^a3^b5^cu\), \(\gcd(u,30)=1\). Since \(9\cdot10^k=3^2\cdot2^k\cdot5^k\),

\[
r_k^{(t)}=
2^{a-\min(a,k)}3^{b-\min(b,2)}5^{c-\min(c,k)}u.
\]

This sequence is nonincreasing in \(k\) and eventually equals \(3^{\max(b-2,0)}u\), the left side of the criterion. Apply Theorem 4 as in Corollary 3.2. \(\square\)

## 8. Prime-factor structure

For \(m=2^a3^b5^cu\), \(\gcd(u,30)=1\), the all-length criteria are therefore:

| Error class | Eventual reduced modulus | Universal detection at every position for all finite lengths iff |
|---|---:|---:|
| Substitution | \(3^b u\) | \(3^b u>9\) |
| Unequal adjacent transposition | \(3^{\max(b-2,0)}u\) | \(3^{\max(b-2,0)}u>9\) |

The fixed-position factors \(r_k\) also include any not-yet-cancelled powers of 2 and 5. Increasing \(k\) adds powers of 2 and 5 through \(10^k\), so those factors progressively cancel from the reduced modulus. A factor 3 does not cancel in the substitution formula because 10 is coprime to 3. In the transposition formula, the factor 9 cancels up to two powers of 3 immediately; any excess power of 3 remains. Prime factors in \(u\), being coprime to 2, 3, and 5, remain in every reduced modulus.

The relevant quantity is the reduced modulus at each position, not whether \(m\) is prime or composite. A composite modulus can satisfy either criterion, while a modulus with only factors from 2, 3, and 5 can fail one or both. The criteria are specific to base 10 and the stated error transformations.

## 9. Modulus 11 as a corollary

For \(m=11\), the factorization has \(a=b=c=0\), \(u=11\). Both eventual reduced moduli in Section 8 equal 11, which exceeds 9. Thus every substitution and every unequal adjacent transposition is detected for every finite string length under the project's definitions.

Equivalently, at each position, neither \(d10^k\) nor \(9d10^k\) is divisible by 11: 10 and 9 are units modulo 11, and no allowed nonzero \(d\) is divisible by 11. This corollary does not assert detection of insertions, deletions, multiple changes, non-adjacent swaps, or arbitrary alterations.

## 10. Exact event counts

For positive integer \(h\), let \(W(h)\) count ordered pairs \((a,b)\in\mathcal D^2\) with \(a\ne b\) and \(h\mid(b-a)\). The absolute difference must be a positive multiple \(hj\), with \(1\leq j\leq\lfloor9/h\rfloor\). For a fixed positive difference \(hj\), there are \(10-hj\) pairs with \(b-a=hj\): the smaller digit can be any of \(0,\ldots,9-hj\). Reversing each pair gives the same number with negative difference, accounting for the factor 2. Hence

\[
W(h)=2\sum_{j=1}^{\lfloor9/h\rfloor}(10-hj).
\]

If \(h>9\), no nonzero difference of decimal digits is a multiple of \(h\), so the sum is empty and \(W(h)=0\). In particular, \(W(1)=90\), the number of all ordered unequal digit pairs.

For substitution position \(k\), the lemma gives \(h=r_k^{(s)}\). There are \(W(h)\) undetected ordered pairs at that digit position; the other \(n-1\) digits have \(10^{n-1}\) choices. Thus

\[
U_s(m,n)=10^{n-1}\sum_{k=0}^{n-1}W\!\left(\frac{m}{\gcd(m,10^k)}\right),
\qquad T_s(n)=90n10^{n-1}.
\]

For transposition pair position \(k\), \(h=r_k^{(t)}\), and the remaining \(n-2\) digits have \(10^{n-2}\) choices. For \(n\geq2\),

\[
U_t(m,n)=10^{n-2}\sum_{k=0}^{n-2}W\!\left(\frac{m}{\gcd(m,9\cdot10^k)}\right),
\qquad T_t(n)=90(n-1)10^{n-2}.
\]

For \(n=1\), define \(U_t=T_t=0\); there are no transposition events. In either class, detected count is \(T-U\). When \(T>0\), the event-enumeration detection rate is \((T-U)/T\). These are counts and finite rates, not probabilities absent an explicitly chosen distribution.

## 11. Relationship to existing computational results

The current exhaustive sweep covers moduli 2–30 and lengths 1–4. At each setting it enumerates every source string and every event in the two definitions above, preserving leading zeros and excluding equal adjacent swaps. The saved CSV records 232 per-length rows; the aggregate report contains 58 modulus/error-type rows.

Agreement between exact enumeration and the derived formulas checks that the computed finite totals, detected counts, undetected counts, and displayed rates agree with the mathematical characterization over this configured domain. It does not prove the characterization for all moduli or lengths, replace the proof, establish novelty, or imply a real-world error probability. Formula comparison is not fully independent if the validator and expected counts share code or assumptions; hand-derived examples and an independently implemented derivation reduce, but do not eliminate, that concern.

The modulus-11 and moduli-3/9 statements are mathematical consequences of the divisibility conditions. Their agreement with the finite sweep is a consistency check, not the source of those proofs.

## 12. Edge cases and quantifier check

The universal labels below concern **every event at every position over every source string of a given fixed length**. “All lengths” means every finite length in which the error class has positions. “Partial” means some events are detected and some are not; “complete failure” means every event in the specified class is undetected.

| Modulus | Substitution prediction across lengths | Adjacent-transposition prediction across lengths | Explanation |
|---:|---|---|---|
| 2 | Partial | Partial | At positions \(k\geq1\), powers of 10 make the reduced modulus 1, so all events there are undetected; at \(k=0\), differences not divisible by 2 are detected. |
| 3 | Partial | Complete failure | Substitution reduced modulus remains 3, so differences divisible by 3 are missed while differences not divisible by 3 are detected. For transpositions, 3 divides 9, so every reduced modulus is 1. |
| 5 | Partial | Partial | At sufficiently large positions the reduced modulus is 1; lower positions include both detectable and undetectable differences. |
| 9 | Partial | Complete failure | Substitution reduced modulus is 9. For transpositions, 9 divides the change factor, so the reduced modulus is 1 at every position. |
| 10 | Partial | Partial | Substitution is universal only at \(k=0\); at \(k\geq1\), every event is undetected. Transposition is universal at \(k=0\), but reduced modulus is 1 from \(k\geq1\). |
| 11 | Universal | Universal | Both all-length reduced moduli are 11. |
| 12 | Partial | Partial | All-length reduced moduli are 3 for substitutions and 1 for transpositions; each is at most 9, but at the lowest position each is greater than 1. |
| 18 | Partial | Partial | The all-length reduced moduli are 9 and 1, respectively. At low positions there are also detectable differences. |
| 25 | Partial | Partial | The factors of 5 cancel as position grows; low positions can detect all or some events, later positions become partial or wholly undetected. |
| \(m>30\) | Depends on factorization | Depends on factorization | Size alone does not determine the outcome. For example, 31 satisfies both criteria; 32 satisfies neither all-length criterion. |

For fixed length, apply the endpoint criteria, not only the all-length column: substitutions use \(r_{n-1}^{(s)}\), and for \(n\geq2\) transpositions use \(r_{n-2}^{(t)}\). At \(k=0\), the substitution reduced modulus is \(m\); the transposition reduced modulus is \(m/\gcd(m,9)\). At large \(k\), the factorization limits in Section 8 apply. At length 1, substitutions have one position; transpositions have no events and therefore no defined rate. Leading zeros do not alter the positional proof. The maximum difference \(|d|=9\) is included in the allowed set and explains why the strict threshold is greater than 9, not greater than or equal to 9.

## 13. Guarantee, rate, and probability

- **Guarantee:** every event in a precisely stated event set is detected. A universal guarantee requires quantifiers over all source strings, allowed transformations, and positions specified by the claim.
- **Detection rate:** detected-event count divided by total-event count in a finite enumeration, when the denominator is positive. The project's rates weight each enumerated event equally.
- **Probability:** a probability measure over source strings and transformations, followed by the measure of the detected or undetected event set. Uniform selection from the finite event set makes the empirical event rate a probability under that particular model; other distributions yield different probabilities.

When there are zero events, a rate is undefined and is represented as N/A or blank, not zero.

## 14. Limitations

This model is limited to base-10 digits, fixed-width strings, the residue \(N(x)\bmod m\), and single substitutions or unequal adjacent transpositions. It has no appended check digit, error-location or correction procedure, authentication, cryptographic security, or adversarial security proof. It has no real-world error distribution or arbitrary data-corruption model. The all-length result for modulus 11 does not imply that 11 is universally optimal under other objectives, alphabets, check constructions, or error models. No novelty claim is made.

## 15. Open theoretical questions

The following questions were open in this decimal-only document. The first has since been resolved within the established model; its answer is linked below. The remaining questions are outside the results developed here:

- How do the divisibility and universal-detection conditions generalize from decimal base 10 to an arbitrary base \(B\) and digit alphabet? **Resolved within the established fixed-width radix model:** see the derivations in [R11](r11_radix_generalization.md). This is no longer an open question for that model.
- How do position-dependent weighted checksums change the substitution and transposition conditions?
- What are the exact conditions for non-adjacent transpositions?
- What conditions characterize multiple simultaneous substitutions or compound errors?
- Can the framework give complete error-detection profiles for arbitrary moduli and specified error sets?
- How does this plain residue comparison relate formally to established check-digit constructions and their conventions?
- What additional structure, such as position-dependent weights or a noncommutative operation, is required for a check-digit scheme to detect error classes missed by plain residues?
- Which statements are already established in the coding/check-digit literature, and what remains after a systematic literature review?

## 16. Research claim status

| Claim | Status | Evidence required | Current evidence |
|---|---|---|---|
| The substitution residue change is \(d10^k\). | Mathematically established | Algebra from positional-value definition. | Derived in Theorem 1. |
| The adjacent-swap residue change is \(9d10^k\) under the stated position convention. | Mathematically established | Algebra from the two exchanged positions. | Derived in Theorem 2. |
| Divisibility reduces to \(m/\gcd(m,q)\mid d\). | Mathematically established | GCD cancellation proof. | Lemma 1. |
| The fixed-position all-event tests are exactly reduced modulus \(>9\). | Mathematically established | Both directions and realizability of every difference 1–9. | Theorems 3 and 4. |
| The all-length factorization criteria in Section 8 are necessary and sufficient. | Mathematically established within this formal model | Verify factorization, eventual minima, and event quantifiers. | Corollaries 3.2 and 4.2 derive them. Not a novelty claim. |
| Modulus 11 detects all events of both defined classes at every finite length. | Mathematically established | Follows from the all-length criteria or direct units argument. | Section 9. Does not cover arbitrary alterations. |
| Moduli 3 and 9 miss every unequal adjacent transposition. | Mathematically established | Divisibility by 9 for every transposition. | Theorem 2 and Section 12. |
| Exact event-count formulas using \(W(h)\). | Mathematically established within this model | Pair count by difference and independent check of free positions. | Section 10; also implemented in existing analytical code. |
| Existing finite sweep values agree with exact formulas. | Computationally validated | Reconcile each row and aggregate without altering source artifacts. | Existing validator and characterization report state that 232 rows and 58 aggregates reconcile; this document did not rerun the sweep. |
| Agreement establishes the all-modulus/all-length theorem. | Not established by computation | A proof with explicit quantifiers. | Finite enumeration cannot establish this; proofs are stated above. |
| The characterization is novel. | Not yet established | Systematic literature review and comparison of exact definitions/results. | No novelty assessment is made. |
| Enumerated event rates equal real-world error probabilities. | Not yet established | A justified probability model and data. | Only uniform finite-event rates are defined here. |

## 17. References

The following references were already identified in the project's research documents. They provide background and comparison context; the elementary divisibility results above are proved here and do not depend on these references.

- R. W. Hamming, “Error Detecting and Error Correcting Codes,” *Bell System Technical Journal*, 29(2), 147–160 (1950). DOI: [10.1002/j.1538-7305.1950.tb00463.x](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x).
- J. Verhoeff, *Error Detecting Decimal Codes*, Mathematical Centre Tract 29 (1969). Bibliographic record: [CWI repository](https://ir.cwi.nl/pub/13045). The existing research notes identify this as background on decimal check-digit codes; no specific result from the monograph is assumed in the proofs above.
- ISO/IEC 7064:2003, *Information technology — Security techniques — Check character systems*. [ISO record](https://www.iso.org/standard/31531.html). It describes guarantees for the standard's specified check-character systems, not for every plain modular residue scheme.
- H. M. Damm, “Check digit systems over groups and anti-symmetric mappings,” *Archiv der Mathematik* (2000), DOI: [10.1007/s000130050524](https://doi.org/10.1007/s000130050524). The existing comparison notes distinguish the paper's general group-based results from claims about a specific decimal quasigroup construction; that distinction is retained here.
- H. Michael Damm, *Total anti-symmetrische Quasigruppen*, dissertation, Philipps-Universität Marburg (2004). [Repository PDF](https://archiv.ub.uni-marburg.de/diss/z2004/0516/pdf/dhmd.pdf). The existing notes say the bibliographic record was identified but full text was inaccessible; no specific dissertation theorem is relied on here.

## Potential implementation/model discrepancies

No mathematical discrepancy between the stated transformations and the inspected checksum/error-generation conventions was identified. This document does not change or revalidate implementation behavior. In the audited checkout, the financial validation package and its test are untracked work in progress; no reporting or CLI implementation, console-script packaging, or root `LICENSE` was present. They are outside this mathematical model and should not be described as tracked/published capabilities based on this checkout.
