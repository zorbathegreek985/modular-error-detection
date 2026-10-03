# R10 — Count-Spectrum Equivalence: Theorem Discovery

> Historical research-development note. The proposed next step at the end of this document records the investigation's position at R10; the subsequent R11/R12 work developed the radix and identifiability analysis, and R12 later recommended closing this inverse-problem line absent stronger evidence. This note preserves that chronology and does not alter the results below.

> Historical research-development note. The proposed next step at the end of this document records the investigation's position at R10; the subsequent R11/R12 work developed the radix and identifiability analysis, and R12 later recommended closing this inverse-problem line absent stronger evidence. This note preserves that chronology and does not alter the results below.

> Historical research-development note. The proposed next step at the end of this document records the investigation's position at R10; the subsequent R11/R12 work developed the radix and identifiability analysis, and R12 later recommended closing this inverse-problem line absent stronger evidence. This note preserves that chronology and does not alter the results below.

## 1. Research question

For which distinct project moduli (m,n>1), if any, are the substitution and unequal-adjacent-transposition count spectra identical at every positional exponent? The observable is deliberately the count (W(h)), not the reduced divisor (h) itself.

This note asks whether equality of those observables yields a substantive classification or mostly records information lost when (W(h)=0) for all (h>9). The result below is a mathematical characterization of the observation map and its prime-factor inputs. It is not a novelty claim.

## 2. Exact definitions

For a fixed-width decimal string (x), with digit (x_k) in place (10^k), let

\[
N(x)=\sum_k x_k10^k,\qquad C_m(x)=N(x)\bmod m,
\]

where the project modulus satisfies (m>1). A single substitution at position (k\ge0) with nonzero digit difference (d) changes the value by (d10^k). Define

\[
h_s(m,k)=\frac{m}{\gcd(m,10^k)},\qquad S_m(k)=W(h_s(m,k)).
\]

An unequal adjacent transposition whose lower-place digit is at position (k\ge0) changes the value by (9d10^k), up to sign. Define

\[
h_t(m,k)=\frac{m}{\gcd(m,9\cdot10^k)},\qquad T_m(k)=W(h_t(m,k)).
\]

Two moduli (m,n>1) are **count-spectrum equivalent** if

\[
S_m(k)=S_n(k)\quad\text{and}\quad T_m(k)=T_n(k)
\qquad\text{for every integer }k\ge0.
\]

Here (k=0) is included. Every substitution position (k) occurs in some finite string, namely one of length at least (k+1). Every transposition position (k) is a valid adjacent pair in some finite string, namely one of length at least (k+2). Thus the all-(k) definition is exactly the union of the project’s finite-length position domains; it is not restricted to the historical length range 1–4. If only a fixed maximum length (L) is considered, the positions are instead (0\le k<L) for substitutions and (0\le k<L-1) for transpositions.

## 3. Behavior of (W(h))

For a positive integer (h), an unequal ordered decimal pair with absolute difference (hj\le9) has (10-hj) choices in each orientation. Therefore

\[
W(h)=2\sum_{j=1}^{\lfloor9/h\rfloor}(10-hj)
=20q-hq(q+1),\qquad q=\left\lfloor\frac9h\right\rfloor,
\]

when (1\le h\le9). If (h>9), no nonzero decimal digit difference is divisible by (h), so (W(h)=0).

| (h) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | (>9) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| (W(h)) | 90 | 40 | 24 | 16 | 10 | 8 | 6 | 4 | 2 | 0 |

The positive values are strictly decreasing on (h=1,\ldots,9), as the complete table shows. Consequently (W) is injective on ({1,\ldots,9}); the only collisions are among distinct inputs greater than 9, all of which map to zero. In particular,

\[
W(r)=W(s)\iff (r=s\le9)\text{ or }(r>9\text{ and }s>9)
\]

for positive integers (r,s).

## 4. Prime-factor derivation

Write

\[
m=2^a3^b5^c u,\qquad a,b,c\ge0,\qquad \gcd(u,30)=1.
\]

Since (10^k=2^k5^k) and (u) has no factors 2 or 5,

\[
\gcd(m,10^k)=2^{\min(a,k)}5^{\min(c,k)}.
\]

Hence

\[
h_s(m,k)=2^{a-\min(a,k)}3^b5^{c-\min(c,k)}u.
\]

For the transposition coefficient, (9\cdot10^k=3^2 2^k5^k). The gcd exponents are therefore

\[
\gcd(m,9\cdot10^k)=2^{\min(a,k)}3^{\min(b,2)}5^{\min(c,k)},
\]

and

\[
h_t(m,k)=2^{a-\min(a,k)}3^{b-\min(b,2)}5^{c-\min(c,k)}u.
\]

Set

\[
A=3^b u,\qquad B=3^{b-\min(b,2)}u=3^{\max(b-2,0)}u,
\]

and

\[
v_{a,c}(k)=2^{\max(a-k,0)}5^{\max(c-k,0)},\qquad K_m=\max(a,c).
\]

Then (h_s(m,k)=A v_{a,c}(k)), (h_t(m,k)=B v_{a,c}(k)), and (v_{a,c}(k)=1) for every (k\ge K_m). Also (A\ge B).

## 5. Substitution spectrum

The substitution spectrum is

\[
S_m(k)=W\!\left(A v_{a,c}(k)\right).
\]

Its reduced divisor is nonincreasing in (k), reaches (A) by (k=K_m), and remains there. Its count spectrum is consequently constant from (k=K_m) onward. The final count is (W(A)), which is positive exactly when (A\le9).

## 6. Transposition spectrum

The unequal-adjacent-transposition spectrum is

\[
T_m(k)=W\!\left(B v_{a,c}(k)\right).
\]

Its reduced divisor is nonincreasing in (k), reaches (B) by (k=K_m), and remains there. Its count spectrum is constant from (k=K_m) onward. The final count is (W(B)), positive exactly when (B\le9). Each (k\ge0) represents an actual pair position for sufficiently large finite width; the absence of a transposition event at length 1 does not remove (k=0) or any other position from this all-width definition.

## 7. Equivalence analysis

The injectivity property of (W) gives an exact criterion. For two moduli, write their parameters as (A,B,v(k)) and (A',B',v'(k)). They are count-spectrum equivalent if and only if, for every (k\ge0), each of the following two conditions holds independently:

\[
\begin{aligned}
&Av(k)=A'v'(k)\le9\quad\text{or}\quad Av(k)>9\text{ and }A'v'(k)>9,\\
&Bv(k)=B'v'(k)\le9\quad\text{or}\quad Bv(k)>9\text{ and }B'v'(k)>9.
\end{aligned}
\]

This is a necessary-and-sufficient characterization of the information the spectra retain: a reduced divisor at most 9 is observed exactly, while every value above 9 is observed only as zero. It is not a closed-form list of all arithmetic equivalence classes; deriving such a list would require classifying these thresholded trajectories.

The stable transposition count reveals (B) exactly when (B\le9); when (B>9) it reveals only that the stable value exceeds 9. The stable substitution count similarly reveals (A) only when (A\le9). Thus the pair of tails can expose some of the (3^bu) and (3^{\max(b-2,0)}u) factors, but cannot recover arbitrarily large values. The factors (2^a) and (5^c) occur only in the transient multiplier (v_{a,c}(k)); they are observable only at positions where the relevant product is at most 9. Joint equivalence is the intersection of the two individual equivalences, so adding the second spectrum can only split classes or leave them unchanged.

Distinct equivalent moduli do exist, including equivalences with nonzero spectra and different reduced-divisor trajectories. For example:

\[
h_s(14,k)=h_t(14,k)=\begin{cases}14,&k=0,\\7,&k\ge1,\end{cases}
\qquad
h_s(35,k)=h_t(35,k)=\begin{cases}35,&k=0,\\7,&k\ge1.\end{cases}
\]

Both moduli therefore have (S(k)=T(k)=0) at (k=0), and (S(k)=T(k)=W(7)=6) for every (k\ge1). The reduced divisors differ at (k=0), but both lie in the zero tail of (W).

More generally, for any fixed (K\ge1), all moduli

\[
m=7\cdot2^a5^c,\qquad \max(a,c)=K,
\]

have the same pair of spectra: both counts are zero for (k<K), and both equal 6 for (k\ge K). At each (k<K), at least one residual factor in (v_{a,c}(k)) is at least 2, so (7v_{a,c}(k)\ge14>9). For (k\ge K), (v=1) and (W(7)=6). The family includes distinct moduli such as 14, 35, and 70 when (K=1).

Thus equivalence is neither impossible for distinct moduli nor limited to the joint all-zero spectrum. The observed nonzero equivalences still arise from loss of information above the threshold 9, together with later agreement of the visible reduced divisors.

## 8. Zero-spectrum classification

Because (v_{a,c}(k)\ge1) and its minimum 1 is attained for (k\ge K_m):

**Proposition 1.** The substitution spectrum is identically zero if and only if

\[
A=3^b u>9.
\]

**Proposition 2.** The transposition spectrum is identically zero if and only if

\[
B=3^{\max(b-2,0)}u>9.
\]

**Corollary.** Both spectra are identically zero if and only if

\[
3^{\max(b-2,0)}u>9.
\]

Indeed (A\ge B), so the joint condition is exactly the transposition condition. All moduli satisfying it belong to one all-zero equivalence class. This is an infinite family; the powers (2^a) and (5^c) do not affect whether the stable factors exceed 9. The individual conditions differ: for (m=21), (A=21>9) but (B=7\le9), so substitutions are all zero while the transposition spectrum is eventually 6.

## 9. Stabilization and finite-prefix bound

The reduced divisors stabilize at (K_m=\max(a,c)), and the spectra stabilize no later than that same position because applying (W) to a constant reduced divisor leaves it constant. The first stable position is not necessarily the first position at which the *count* stabilizes: if all early reduced divisors exceed 9, their counts can all be zero before the reduced divisor reaches its eventual value.

**Proposition 3 (finite-prefix test).** For moduli (m,n>1), let

\[
K=\max(K_m,K_n).
\]

They are count-spectrum equivalent for every (k\ge0) if and only if both spectra agree at every (k=0,1,\ldots,K). For (k\ge K), both moduli are already at their respective stable reduced divisors, so their two count values are constant; equality at (K) establishes equality on the whole tail.

This is a justified finite bound from the factorizations, not a claim that it is globally minimal for every pair. For a range (m,n\le M), one common bound is (K\le\lfloor\log_2 M\rfloor), since (a\le\lfloor\log_2 M\rfloor) and (c\le\lfloor\log_5 M\rfloor\le\lfloor\log_2 M\rfloor). The enumeration below uses the sharper actual maximum (K=12) for (M=5000).

## 10. Computational exploration

I independently enumerated moduli (2\le m\le5000). For each modulus, the reduced divisors were calculated with integer gcds. (W(h)) was independently counted by looping over the 100 ordered decimal digit pairs and counting unequal pairs for which (h\mid(b-a)); this does not use the closed-sum implementation. The two resulting sequences were compared as tuples for (k=0,\ldots,12). This prefix is sufficient for the entire infinite spectrum on this range: (v_2(m)\le12), (v_5(m)\le5), so all reduced divisors have stabilized by (k=12).

**Computational observation (bounded range only):**

- 4,999 moduli produced 103 distinct joint spectrum classes.
- The substitution-only and transposition-only partitions had 62 and 55 classes, respectively; using both produced 103 joint classes in this range.
- There was one all-zero class containing 4,811 moduli.
- There were 45 other non-singleton classes with nonzero spectra; the largest had 9 members.
- The remaining 57 classes among the nonzero spectra were singletons.
- No enumeration result is used as a proof for moduli outside this range.

Examples of nonzero-spectrum classes found:

| Moduli in one class | Substitution spectrum for (k=0,1,\ldots) | Transposition spectrum for (k=0,1,\ldots) |
|---|---|---|
| 14, 35, 70 | (0,6,6,\ldots) | (0,6,6,\ldots) |
| 28, 140, 175, 350, 700 | (0,0,6,6,\ldots) | (0,0,6,6,\ldots) |
| 84, 252, 420, 525, 1050, 1260, 1575, 2100, 3150 | (0,0,0,0,\ldots) | (0,0,6,6,\ldots) |

These are observations from the specified bounded computation. The parameterized family in Section 7 has a separate proof.

## 11. Theorem / proposition statements

1. **Lemma 1:** (W(h)) has the values in Section 3; it is injective on (1\le h\le9), and zero for all (h>9).
2. **Proposition 1:** (S_m(k)\equiv0) for all (k\ge0) iff (3^bu>9).
3. **Proposition 2:** (T_m(k)\equiv0) for all (k\ge0) iff (3^{\max(b-2,0)}u>9).
4. **Proposition 3:** Equality of the two spectra for all (k\ge0) is equivalent to equality through (k=K=\max(K_m,K_n)), inclusive.
5. **Proposition 4 (observation criterion):** Two moduli are equivalent iff at every (k), each corresponding pair of reduced divisors is either equal and at most 9, or both are greater than 9.
6. **Proposition 5 (infinite nonzero family):** For fixed (K\ge1), the moduli (7\cdot2^a5^c) with (max(a,c)=K) are all pairwise count-spectrum equivalent, with common spectra zero for (k<K) and 6 thereafter.

## 12. Proofs

**Lemma 1.** For a positive difference (d=hj\le9), the smaller digit has (10-d) possible values. There are the same number of ordered pairs in the reverse orientation. Summing gives (W(h)=2\sum_{j=1}^{\lfloor9/h\rfloor}(10-hj)), and the arithmetic-sum identity gives (20q-hq(q+1)). Substitution of (h=1,\ldots,9) gives the complete table; those entries are distinct and positive. For (h>9), there are no admissible nonzero differences. This proves the lemma for every positive integer (h), not by bounded enumeration.

**Proposition 1.** Write (h_s=A v_{a,c}(k)). Since (v_{a,c}(k)\ge1), if (A>9), every (h_s(m,k)>9) and every count is zero. If (A\le9), then for (k\ge K_m), (v=1), so (S_m(k)=W(A)>0). Both directions follow.

**Proposition 2.** The same argument with (h_t=Bv_{a,c}(k)) gives zero for every position exactly when (B>9); if (B\le9), the stable count is the positive value (W(B)).

**Proposition 3.** Each modulus has (v_{a,c}(k)=1) at and after its (K_m). Thus for the pair, both spectra are constant at and after (K=\max(K_m,K_n)). Agreement on (0\le k\le K) implies agreement at (K), hence on the entire constant tail. The converse is immediate because equality for all (k) includes that prefix.

**Proposition 4.** Apply Lemma 1 to each coordinate: (W(r)=W(s)) precisely when the two positive inputs are the same value at most 9 or are both in the zero tail above 9. Requiring this for both substitution and transposition coordinates at every position is exactly the definition of joint spectrum equivalence.

**Proposition 5.** For (m=7\cdot2^a5^c), (A=B=7). If (k<K=\max(a,c)), at least one of ((a-k)_+,(c-k)_+) is positive, so (v_{a,c}(k)\ge2), and both reduced divisors are at least 14; both counts are zero. If (k\ge K), (v=1), so both counts equal (W(7)=6). The result depends only on (K), not on the individual pair ((a,c)), proving pairwise equivalence for all moduli in this fixed-(K) family.

## 13. Counterexamples, if any

The conjecture that distinct equivalent moduli might be impossible is disproved by 14 and 35. They have different reduced divisors at (k=0) (14 versus 35), but both divisors exceed 9, so the observed counts agree. Their reduced divisors are both 7 from (k=1) onward. The family in Proposition 5 gives infinitely many such distinct pairs with nonzero stable spectra.

The conjecture that every nontrivial equivalence must have all-zero spectra is also disproved by the same example: its spectra are ((0,6,6,\ldots)) for both error types. The separate all-zero family is characterized exactly in Section 8.

## 14. Relationship to existing project results

The reduced-divisor formulas and stabilization are from the project’s established analysis. The present result applies the exact shape of (W) to those formulas. It separates three objects:

1. **Reduced-divisor profile:** (h_s(m,k),h_t(m,k)).
2. **Count spectrum:** (S_m(k),T_m(k)), which applies (W) and loses distinctions above 9.
3. **Finite-string event counts and rates:** position sums with common length-dependent factors.

For length (n\ge1), the undetected substitution total and all-event total are

\[
U_s(m,n)=10^{n-1}\sum_{k=0}^{n-1}S_m(k),\qquad
E_s(n)=90n10^{n-1}.
\]

For (n\ge2), the unequal-transposition totals are

\[
U_t(m,n)=10^{n-2}\sum_{k=0}^{n-2}T_m(k),\qquad
E_t(n)=90(n-1)10^{n-2}.
\]

Detected totals are (E-U), and rates divide by (E). Therefore count-spectrum equivalence implies equal finite-length event counts and rates for every length: the sums use the same spectrum entries and the multipliers/denominators are common to all moduli. The converse for a single fixed length is false because aggregating positions can hide differences. For example, at length 4, moduli 81 and 84 both have substitution miss-count sums 0 and transposition miss-count sums 6, but their transposition spectra are respectively ((2,2,2)) and ((0,0,6)). Their length-4 aggregate counts and rates agree even though their position-resolved spectra differ. Equality of aggregate counts at every length would imply equality of the prefix sums and therefore recover each position count by successive differences, but the usual finite experiment covers only a bounded set of lengths.

## 15. Research-contribution assessment

**Classification: B. Interesting but likely elementary / insufficiently differentiated.**

The question does not collapse to the single all-zero family: infinitely many nonzero-spectrum equivalences exist, and the bounded search finds many classes. The exact reason, however, is transparent from the observation map: (W) preserves each reduced divisor through 9 and clips every larger value to zero. The finite-prefix result follows from the already-known stabilization. The threshold criterion is a concise theorem, but by itself is a direct consequence of the existing formulas, not a non-obvious classification of arithmetic classes.

The fixed-(K) family is a proved structural example, not evidence of novelty. A research-paper direction would require a complete arithmetic classification of all nonzero count-spectrum classes and a meaningful consequence that is not just the thresholded-trajectory criterion. The current bounded enumeration and theorem do not meet that threshold. No novelty or publishability claim is made.

## 16. If the question collapses: next candidate question

The question does **not** collapse completely, so no broad replacement question is proposed. One narrowly motivated follow-up is:

> For a fixed decimal length limit (L), classify the equivalence classes of moduli under equality of the position-resolved nonzero count spectra for (0\le k<L), and compare those classes with equivalence under the aggregate finite-length count vectors for lengths (1,\ldots,L).

This asks how much information is lost first by the (W(h)) zero tail and then by summing positions. The example with moduli 81 and 84 shows that a single-length aggregate can lose position information. A finite-(L) classification may be useful for explaining experiment tables, but it is likely an elementary finite partition unless it yields a compact arithmetic theorem. It should be explored only if that distinction has a clear use; otherwise retain the project’s existing software/reproducibility focus.

## 17. Limitations and unresolved literature questions

- The enumeration is limited to moduli 2–5000. It is a pattern-discovery and implementation check, not a proof for arbitrary moduli.
- The all-zero and fixed-(K) family propositions are proved directly from the formulas; they do not classify every equivalence class.
- A complete closed-form classification of nonzero classes has not been derived here. Proposition 4 is exact but states the thresholded-trajectory criterion rather than enumerating all arithmetic parameter families.
- This phase does not resolve the full texts of Gumm (1985) or Damm (2000), or establish whether equivalent classification results appear in earlier literature.
- No claim is made that count-spectrum equivalence is new. Its overlap with weighted-check rate/profile classifications requires further primary-source review before any stronger research framing.
- The project’s event models remain single substitutions and unequal adjacent transpositions on fixed-width decimal strings. The results do not apply automatically to other error types, alphabets, or check constructions.

## 18. Exact recommended next step

Do not expand the experiment or claim novelty. If pursuing this direction, first derive a complete arithmetic classification of the thresholded trajectories

\[
\left(W\!\left(3^bu\,2^{(a-k)_+}5^{(c-k)_+}\right),\;
W\!\left(3^{\max(b-2,0)}u\,2^{(a-k)_+}5^{(c-k)_+}\right)\right)_{k\ge0}
\]

by the factorization parameters, prove necessary and sufficient conditions for two parameter tuples to yield the same sequence, and compare that classification to the count-only and finite-length aggregate relations. Use independent enumeration on bounded ranges to check the theorem, then review full lawful primary sources for prior classifications. If the result reduces to the clipping criterion in Proposition 4 with no further explanatory structure or use, close the theorem-discovery branch and keep the repository framed as research software and a reproducible educational study.
