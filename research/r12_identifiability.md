# R12 — Finite-Alphabet Identifiability

## 1. Research question

This note asks what arithmetic information about a positive modulus can be recovered when an observer sees only the complete substitution and unequal-adjacent-transposition count spectra at a fixed radix. The observer does not see the modulus, reduced divisors, or internal gcd values.

The investigation builds on the error spectra, finite-alphabet pair-count function, and stabilization formulas in [R11](r11_radix_generalization.md), and the earlier count-equivalence question in [R10](r10_count_spectrum_theorem.md). It is an inverse-problem analysis of that existing model, not a new checksum model. No novelty claim is made.

## 2. Observation model

Fix an integer radix \(q\ge2\), let \(Q=q-1\), and let \(m\ge2\) be the modulus. Digits are \(0,\ldots,Q\), including leading-zero positions. For \(h\ge1\), define the number of ordered unequal digit pairs whose difference is divisible by \(h\):

$$
W_q(h)=2\sum_{j=1}^{\lfloor Q/h\rfloor}(q-hj).
$$

Thus \(W_q(h)=0\) for \(h>Q\), and \(W_q\) is strictly decreasing, hence injective, on \(1\le h\le Q\). This injectivity follows by comparing the positive summands for successive \(h\); a proof is given in R11. Define the threshold map

$$
c_Q(h)=\begin{cases}h,&1\le h\le Q,\\\bot,&h>Q.\end{cases}
$$

Then \(W_q(h)=W_q(h')\) if and only if \(c_Q(h)=c_Q(h')\). The symbol \(\bot\) means only “some value above the observation threshold”; it is not a reduced divisor.

The reduced divisors and observed spectra are

$$
h_s(m,k)=\frac{m}{\gcd(m,q^k)},\qquad
h_t(m,k)=\frac{m}{\gcd(m,Qq^k)},
$$

$$
S_{m,q}(k)=W_q(h_s(m,k)),\qquad
T_{m,q}(k)=W_q(h_t(m,k)),\qquad
O_q(m)=\bigl((S_{m,q}(k),T_{m,q}(k))\bigr)_{k\ge0}.
$$

The spectra count undetected digit-pair events at each position. Equality of spectra means equality of these counts at every position; it does not mean equality of the hidden reduced divisors.

For the arithmetic analysis, write \(\alpha_p=v_p(q)\), \(\beta_p=v_p(Q)\), and \(\gamma_p=v_p(m)\). Define

$$
A=A_q(m)=\prod_{p\nmid q}p^{\gamma_p},\qquad
B=B_q(m)=\prod_{p\nmid q}p^{\gamma_p-\min(\gamma_p,\beta_p)},
$$

and

$$
R_k=R_{q,m}(k)=\prod_{p\mid q}p^{\max(\gamma_p-k\alpha_p,0)}.
$$

Because \(\gcd(q,Q)=1\), the prime factors in \(R_k\) are disjoint from those in \(A\) and \(B\). Direct valuation arithmetic gives the useful factorization

$$
h_s(m,k)=A R_k,\qquad h_t(m,k)=B R_k,\qquad B=\frac{A}{\gcd(A,Q)}.
$$

Here \(B\mid A\), \(R_k\) is nonincreasing, and \(R_k=1\) for every \(k\ge K(q,m)\), where

$$
K(q,m)=\max_{p\mid q}\left\lceil\frac{\gamma_p}{\alpha_p}\right\rceil.
$$

The maximum is zero when \(m\) has no prime factor in common with \(q\).

## 3. Definition of identifiability

For a parameter \(P(m)\), say that \(P\) is identifiable from the joint spectrum at fixed \(q\) if

$$
O_q(m)=O_q(n)\quad\Longrightarrow\quad P(m)=P(n)
$$

for all moduli \(m,n\ge2\). This is global identifiability. A parameter can fail global identifiability but be recoverable under an explicitly stated condition, such as observing a nonzero spectrum.

Define \(m\sim_q n\) exactly when \(O_q(m)=O_q(n)\). The equivalence class \([m]_q\) is the set of moduli producing the same complete observable pair spectrum. Identifying this class is weaker than identifying \(m\) itself.

## 4. Modulus identifiability

**Proposition.** The modulus \(m\) is not identifiable from \(O_q(m)\), and a spectrum does not in general determine the hidden reduced-divisor sequence.

**Counterexample (decimal radix).** At \(q=10\), moduli 11 and 13 have \(A=B=m>9\) and \(R_k=1\). Both joint spectra are identically \((0,0)\), although the moduli and reduced divisors differ. The same all-zero class also contains 121, so even the exponent of the prime 11 is not fixed in that class.

More generally, the all-zero class is infinite for every fixed radix: every prime \(r>Q\) that does not divide \(qQ\) has \(A=B=r>Q\), and therefore gives the zero spectrum. There are infinitely many such primes. Thus the observer cannot identify the modulus, even if the complete infinite spectrum is available.

This is partial identification: the observation determines a thresholded arithmetic trajectory and, in some regimes, exact stable factors and stabilization position. It does not uniquely identify every modulus in the resulting class.

## 5. Prime-factor identifiability

The factors \(A\), \(B\), and \(R_k\) describe what the spectra can expose. They also clarify the three requested prime categories.

| Prime category | Stable information | What can be recovered conditionally | What is not globally identifiable |
|---|---|---|---|
| \(p\mid q\) | The prime is absent from both \(A\) and \(B\); it appears only through the transient factor \(R_k\). | If a reduced product \(A R_k\) or \(B R_k\) is visible (at most \(Q\)), that product is exact. When the joint spectrum is nonzero, \(K\) is identifiable, which bounds each exponent by \(\gamma_p\le K\alpha_p\). | The individual \(q\)-prime exponents and even whether a specified such prime divides \(m\) are not generally determined. |
| \(p\mid q-1\) | Its full exponent is retained in \(A\), while \(B\) retains only \(\max(\gamma_p-\beta_p,0)\). | If the substitution tail is nonzero, \(A\) is exact and its factorization gives \(\gamma_p\). If only the transposition tail is nonzero, \(B\) reveals the excess above \(\beta_p\), but a zero excess means only \(\gamma_p\le\beta_p\). | When the visible stable products are censored, membership or the exponent within the canceled range can vary in one class. |
| \(\gcd(p,q(q-1))=1\) | The full exponent \(\gamma_p\) appears in both \(A\) and \(B\). | If either stable product is observed exactly, factorization of that product recovers \(\gamma_p\). | If both stable products are above threshold, only threshold information about their products remains; individual prime factors and exponents need not be determined. |

The precise stable-product rule is:

* If the substitution spectrum is nonzero, then \(A\le Q\) and its stable value gives \(A\) exactly. Every exponent with \(p\nmid q\), including primes dividing \(q-1\), is then recoverable by factoring \(A\).
* If the substitution spectrum is zero but the joint spectrum is nonzero, then \(A>Q\) and \(B\le Q\). The transposition tail gives \(B\) exactly. Exponents outside \(q(q-1)\) are recoverable; for \(p\mid q-1\), only the excess \(\max(\gamma_p-\beta_p,0)\) is read directly from \(B\).
* If the joint spectrum is zero, then \(B>Q\). The stable observations disclose this inequality, not the factorization of \(B\).

These statements concern exact factorization of an observed integer. A thresholded product inequality alone does not reveal which factor made the product exceed \(Q\). Earlier positions add the clipped products described in Sections 6–8, not uncensored prime valuations.

**Counterexamples (decimal radix).** The all-zero moduli 11 and 33 differ in whether 3 divides the modulus; 11 and 121 differ in \(v_{11}\); and 11 and 13 differ in their prime support outside \(10\cdot9\). For a nonzero-spectrum example, 21 and 63 have the same joint spectrum \((0,6)\) at every \(k\), although their exponents of 3 are 1 and 2. Here \(B=7\), while the exponent of 3 is at most \(\beta_3=2\) and is removed from \(B\).

## 6. Substitution-only identifiability

The complete substitution observation is exactly the thresholded trajectory

$$
\bigl(c_Q(A R_k)\bigr)_{k\ge0}.
$$

Equivalently,

$$
S_{m,q}(k)=S_{n,q}(k)\ \text{for every }k
\quad\Longleftrightarrow\quad
c_Q(A_q(m)R_{q,m}(k))=c_Q(A_q(n)R_{q,n}(k))\ \text{for every }k.
$$

This is a necessary-and-sufficient characterization, not a recovery of uncensored divisors. If \(A\le Q\), the stable substitution count gives \(W_q(A)\), from which \(A\) is recovered uniquely. If \(A>Q\), every substitution count is zero and the spectrum reports only that inequality. At an earlier position, a nonzero count recovers the product \(A R_k\) exactly; a zero count says only that it exceeds \(Q\).

Thus the substitution spectrum can recover the complete part of \(m\) coprime to \(q\) when \(A\le Q\), but not when that product lies in the zero tail. It sees the \(q\)-primary part only through the products \(R_k\), and those products are censored above \(Q\). It does not generally separate their prime factors.

**Counterexamples.** At \(q=10\), \(m=14\) and \(m=70\) both have substitution sequence \((0,6,6,\ldots)\): their reduced substitution divisors start at 14 and 70, both above 9, and then become 7. Their 5-adic exponents differ. Moduli 11 and 13 have all-zero substitution spectra although their stable reduced divisors are distinct and both exceed 9. These show respectively loss of transient \(q\)-prime detail and loss of exact large coprime reduced divisors.

The substitution spectrum is nonzero somewhere exactly when \(A\le Q\). In that case its minimal observed stabilization index equals \(K\). The proof parallels the joint result in Section 8, using \(A R_k\) in place of \(B R_k\). If it is all zero, \(K\) is not recoverable from that spectrum.

## 7. Transposition-only identifiability

The complete transposition observation is exactly

$$
\bigl(c_Q(B R_k)\bigr)_{k\ge0}.
$$

If \(B\le Q\), the stable count gives \(B\) exactly. If \(B>Q\), the entire transposition spectrum is zero and only the inequality is observed. At each earlier position the observer gets the exact product \(B R_k\) when it is at most \(Q\), and otherwise only the fact that it exceeds \(Q\).

Compared with substitution, the fixed factor \(q-1\) removes \(\gcd(A,q-1)\) from the stable product, so \(B=A/\gcd(A,q-1)\le A\). This can bring a transposition reduced divisor below the finite-alphabet threshold even when the corresponding substitution divisor stays above it. It also means the transposition tail alone omits up to \(\beta_p\) powers of each prime \(p\mid q-1\); it cannot distinguish their exponents within that canceled range without other visible information.

**Counterexample showing added information.** At \(q=10\), moduli 11 and 21 have identical, all-zero substitution spectra because their stable substitution divisors 11 and 21 exceed 9. Their transposition divisors are 11 and 7, respectively, so their transposition spectra are constantly 0 and 6. The transposition observation therefore separates a pair that substitution alone does not.

**Counterexample showing the remaining loss.** Moduli 21 and 63 both have transposition reduced divisor 7 at every position and therefore identical transposition spectra, although their 3-adic exponents differ. Both exponents are fully canceled by the factor 9 in the transposition coefficient.

For the bounded enumeration in Section 11, at \(q=10\) the substitution-only partition of moduli 2–5000 had 62 distinct spectra, the transposition-only partition had 55, and the joint partition had 103. Joint observations refine both single-spectrum partitions. This is a finite count of equivalence classes in the stated modulus range, not an all-moduli theorem or a measure of practical information.

## 8. Joint-spectrum identifiability

**Theorem (exact equivalence criterion).** For fixed \(q\),

$$
m\sim_q n
\quad\Longleftrightarrow\quad
\begin{cases}
c_Q(A_q(m)R_{q,m}(k))=c_Q(A_q(n)R_{q,n}(k)),\\
c_Q(B_q(m)R_{q,m}(k))=c_Q(B_q(n)R_{q,n}(k))
\end{cases}
\quad\text{for every }k\ge0.
$$

**Proof.** The two observed counts at position \(k\) are \(W_q(A R_k)\) and \(W_q(B R_k)\). The equality property of \(W_q\) proved in Section 2 says that two such counts agree exactly when their thresholded arguments agree. Apply it to both coordinates at every position. This proves both implications. \(\square\)

This criterion is exact but intentionally exposes its limitation: it is a clipped-trajectory description, not a short list of all arithmetic pairs \((m,n)\). It is finite to check for any given pair. Let \(K_m=K(q,m)\) and \(K_n=K(q,n)\). Since both trajectories are constant from their respective stabilization indices, it suffices to compare \(k=0,\ldots,\max(K_m,K_n)\), inclusive.

**Proposition (stable joint information).** The joint spectrum is identically zero if and only if \(B>Q\). If it is not identically zero, its transposition tail identifies \(B\) exactly. The substitution tail identifies \(A\) exactly if and only if \(A\le Q\); otherwise it identifies only \(A>Q\).

**Proof.** Since \(B\mid A\), we have \(B\le A\), and \(R_k\ge1\). If \(B>Q\), both \(BR_k\) and \(AR_k\) exceed \(Q\) at every position, giving the zero pair. If \(B\le Q\), the stable transposition divisor is \(B\), whose count \(W_q(B)\) is positive; hence the joint spectrum is nonzero and the tail recovers \(B\) by injectivity. The substitution tail has the same reasoning with \(A\). \(\square\)

Therefore the transposition observation can rescue stable information when \(A>Q\ge B\), but it does not in that case recover the canceled \(q-1\)-part of \(A\) unless it is exposed by another observation. For example, at decimal radix modulus 21 has \(A=21>9\), \(B=7\), so only the transposition tail is nonzero.

## 9. Stabilization identifiability

Distinguish the stabilization of the hidden reduced divisors from the first stabilization of the observed counts. The hidden pair \((A R_k,B R_k)\) stabilizes at \(K\). Because values above \(Q\) are clipped to zero counts, an observed sequence can become constant earlier.

Define the minimal observed stabilization index

$$
\kappa(O)=\min\{j\ge0: O_q(m)_k\text{ is constant for all }k\ge j\}.
$$

**Theorem (stabilization is identifiable exactly in the nonzero case).** If \(O_q(m)\) is nonzero, then \(\kappa(O)=K(q,m)\). If \(O_q(m)\) is identically zero, its minimal observed stabilization index is 0 and does not identify \(K(q,m)\). Thus \(K\) is conditionally identifiable from a nonzero spectrum, but not globally identifiable from joint spectra.

**Proof.** A nonzero joint spectrum implies \(B\le Q\), so its stable transposition count \(W_q(B)\) is positive. At \(k\ge K\), \(R_k=1\), so both coordinates have stabilized. For every \(k<K\), the definition of \(K\) ensures \(R_k>1\), hence \(B R_k>B\). If \(B R_k>Q\), the transposition count at \(k\) is zero, different from its positive stable count. Otherwise, both arguments are in the injective range and strict decrease gives \(W_q(BR_k)<W_q(B)\). Therefore the transposition coordinate at every \(k<K\) differs from its stable value, and the joint observation cannot have stabilized earlier than \(K\). So \(\kappa=K\).

If the joint spectrum is zero, then \(\kappa=0\) regardless of the hidden \(K\). At radix 10, moduli 11 and 110 are both all-zero, while \(K(10,11)=0\) and \(K(10,110)=1\). This proves non-identifiability in the zero case. \(\square\)

In particular, an observed nonzero count anywhere implies a nonzero stable transposition count: the reduced divisors only decrease, so once one is at most \(Q\), its stable value is also at most \(Q\). The theorem concerns the complete infinite spectrum; a finite prefix that ends before stabilization may not reveal \(\kappa\).

## 10. Equivalence classes

The exact classes are preimages of the clipped trajectories in Theorem 8. The following class-size statement gives additional structure.

**Proposition (zero class infinite; every nonzero class finite).** For fixed \(q\), the all-zero joint equivalence class is

$$
\{m\ge2:B_q(m)>Q\},
$$

and is infinite. Every nonzero joint-spectrum equivalence class is finite.

**Proof.** The zero-class equality is the stable joint criterion in Section 8. It is infinite because infinitely many primes \(r>Q\) do not divide \(qQ\); for each, \(A=B=r\), so its spectrum is zero. For a nonzero class, the observed tail determines \(B\le Q\), and Section 9 determines \(K\). For every member, write \(A/B=d\). From \(B=A/\gcd(A,Q)\), we have \(d=\gcd(A,Q)\mid Q\), giving only finitely many possibilities for \(A\). Once \(A\) is chosen, all prime exponents outside \(q\) are fixed. Also, for each \(p\mid q\), \(\gamma_p\le K\alpha_p\), so there are finitely many possible \(q\)-primary exponent vectors. Thus only finitely many moduli can belong to the class. \(\square\)

For any equivalent pair, the following are constant: both complete thresholded trajectories; the stable thresholded values \(c_Q(A)\) and \(c_Q(B)\); and whether the spectrum is zero. In a nonzero class, \(B\) and \(K\) are exact invariants. When \(A\le Q\), \(A\) is also an exact invariant. The raw modulus, individual prime factors in censored products, and \(K\) in the zero class are not invariants.

These criteria characterize equivalence without enumerating a canonical parameter list for every nonzero class. They are sufficient to compare any pair exactly, but they do not provide a more compact classification than the finite clipped trajectories.

## 11. Computational exploration

**Computational observation (bounded only).** I enumerated radices

$$
q\in\{2,3,4,5,6,7,8,9,10,11,12,16,20\}
$$

and moduli \(2\le m\le5000\). For each radix, \(W_q(h)\) was computed directly by testing all ordered digit pairs \((a,b)\), \(a\ne b\), and checking divisibility of \(a-b\) by \(h\). The reduced divisors used integer gcd. The stabilization index was calculated from prime valuations. For each radix I found the largest \(K(q,m)\) in the bounded modulus range and evaluated every modulus at the common positions \(k=0,\ldots,K_{\max}(q)\), inclusive. Since every sequence is stable by that endpoint, the fixed-length tuples represent the complete infinite spectra and can be compared without confusing different stabilization indices with different tuple lengths. Moduli were grouped separately by their \(S\) tuples, \(T\) tuples, and paired \(O\) tuples.

| Radix \(q\) | Substitution classes | Transposition classes | Joint classes | Moduli in zero joint class |
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

The computations found nonzero joint classes containing multiple moduli for each listed radix except 2. They found no class mixing zero and nonzero spectra, as also follows directly from equality of observations. Each radix had a joint all-zero class containing moduli with different \(K\). No nonzero joint class in this bounded range had different \(K\); the stabilization theorem in Section 9 proves that this holds without the bound. The bounded enumeration also found nonzero classes with differing prime exponents in each requested category; the hand-checkable decimal examples above illustrate such losses.

**Reproduction command.** From the repository root, run `python experiments/reproduce_r12_radix_spectra.py`. The command uses the existing radix-spectrum implementation for the 13 radices listed above and moduli \(2\le m\le5000\), computes a common inclusive stabilization endpoint for each radix, and prints the four class statistics and zero-joint-class size shown in the table. Its output should match every row above. These are bounded computational observations; the general results in this note are established by the proofs, not by the enumeration.

For instance, at \(q=10\), joint-equivalence class counts exceed both single-spectrum counts (103 versus 62 substitution classes and 55 transposition classes). The joint spectrum is a refinement of each single-spectrum relation by definition. The example 11 versus 21 shows a specific split produced by the transposition coordinate. The counts are finite computational observations, not a proof of class counts outside \(m\le5000\).

An equivalent dependency-free enumeration can be reproduced with this pseudocode:

```text
for q in {2,3,4,5,6,7,8,9,10,11,12,16,20}:
    Kmax = max K(q,m) for m in 2..5000
    for m in 2..5000:
        factor q and m; compute K(q,m)
        for k in 0..Kmax:
            hs = m / gcd(m, q^k)
            ht = m / gcd(m, (q-1) q^k)
            S[k] = count ordered a != b in 0..q-1 with hs | (a-b)
            T[k] = count ordered a != b in 0..q-1 with ht | (a-b)
        group (S, T), S, and T tuples within this q
```

The enumeration is an implementation check and source of examples. The general statements in Sections 8–10 are proved from the formulas and do not depend on this finite range.

## 12. Theorem / propositions

**Theorem 1 — Exact observable equivalence.** Two moduli have equal joint spectra if and only if their two thresholded reduced-divisor trajectories agree at every position. It suffices to compare through \(\max(K_m,K_n)\). This criterion is exact but retains a trajectory-comparison form.

**Proposition 2 — Stable-factor recovery.** A nonzero joint spectrum recovers \(B\) exactly; it also recovers \(A\) exactly precisely when \(A\le Q\). An all-zero joint spectrum is equivalent to \(B>Q\).

**Theorem 3 — Stabilization identifiability.** For nonzero joint spectra, the minimal observed stabilization index is the hidden reduced-divisor stabilization index \(K\). For zero spectra, \(K\) is not identifiable.

**Proposition 4 — Equivalence-class sizes.** The all-zero joint class is infinite; every nonzero joint class is finite.

The first criterion is a necessary-and-sufficient characterization, but it is a direct consequence of the existing \(W_q\) threshold and gcd trajectories. The latter results give useful conditional recovery statements, not a classification by a new arithmetic invariant.

## 13. Proofs and counterexamples

The proofs of Theorems 1 and 3 and Propositions 2 and 4 are included in Sections 8–10. Their common ingredients are: strict injectivity of \(W_q\) on \([1,Q]\), its zero tail above \(Q\), the factorization \(h_s=A R_k\), \(h_t=B R_k\), and eventual cancellation of the \(q\)-primary factor.

**Counterexample collection (all at \(q=10\)).**

| Claim tested | Moduli | Same observation | Arithmetic difference |
|---|---|---|---|
| Modulus identifiable | 11 and 13 | Both joint spectra are all zero. | Distinct prime moduli and distinct stable divisors. |
| \(K\) globally identifiable | 11 and 110 | Both joint spectra are all zero. | \(K=0\) versus \(K=1\). |
| Individual \(q\)-prime exponents identifiable | 14 and 70 | Both have \(S=(0,6,6,\ldots)\) and \(T=(0,6,6,\ldots)\). | \(v_5=0\) versus \(v_5=1\). |
| \(q-1\)-prime exponents always identifiable | 21 and 63 | Both have \((S,T)=((0,6),(0,6),\ldots)\). | \(v_3=1\) versus \(v_3=2\). |
| Large coprime divisor is recovered from a zero spectrum | 11 and 121 | Both joint spectra are all zero. | \(v_{11}=1\) versus \(v_{11}=2\). |
| Transposition adds information to substitution | 11 and 21 | Substitution spectra are both all zero. | Transposition spectra are constantly 0 and 6. |

These examples are verified directly by the formulas. The bounded enumeration also found them; the proofs of the general propositions do not rely on the enumeration.

## 14. Prior-art comparison

This is a targeted comparison against the repository's existing literature notes, especially [R9](r9_research_decision.md), [R10](r10_count_spectrum_theorem.md), [R11](r11_radix_generalization.md), the [prior-art claim matrix](prior_art_claim_matrix.md), and the [deep prior-art comparison](deep_prior_art_comparison.md). It is not a new or exhaustive literature review. No reviewed source is classified as an **EXACT** match for this observation-equivalence result.

| Area or source | Assessment in the reviewed repository material | Relevance and limit |
|---|---|---|
| Weighted modular checks and error spectra | **CLOSE** | Verhoeff's 1969 monograph was reviewed for decimal weighted-check analysis, error conditions, rates, and computational search. That is close context, but the reviewed notes do not establish this exact inverse map as a stated result. |
| Gumm (1985) | **CLOSE; UNRESOLVED** | Existing notes report an accessible abstract for arbitrary-number-system check digits with single-error and adjacent-transposition guarantees. The full article was not inspected, and its group check-digit construction is not shown to be this scalar residue spectrum. |
| Damm (2000) | **RELATED; UNRESOLVED** | Existing notes report an abstract about group check-digit systems and anti-symmetric mappings. The full text and any exact relationship to scalar count-spectrum equivalence remain unverified. |
| Schulz (2001) | **RELATED** | Existing notes describe group-based check-character system equivalences. No identity between that relation and equality of these scalar observable spectra was established. |
| Exact clipped-trajectory criterion in Theorem 1 | **NOT LOCATED** in the reviewed materials | It follows immediately from the project's \(W_q\) injectivity/zero-tail property and reduced-divisor formulas. “Not located” is bounded-search evidence, not evidence of novelty or absence. |

The exact inverse-identifiability result may have analogues under established classifications of weighted checks or error spectra. Because Gumm (1985) and Damm (2000) remain incompletely inspected and no broad search was performed, that question is **UNRESOLVED**. No priority, novelty, or publication claim is warranted.

## 15. Research decision

**Decision: B. Interesting but elementary.**

The exact equivalence test, stable-factor recovery conditions, conditional identifiability of \(K\), and finite/non-finite class dichotomy are useful consequences of the observation map. Their proofs use the same elementary structure already established in R10–R11: a finite-alphabet count that is injective up to \(Q\), a zero tail above \(Q\), and prime-valuation cancellation in powers of \(q\). The necessary-and-sufficient class test remains a clipped restatement of those formulas; the conditional \(K\) and class-size results do not provide enough differentiation to justify an open-ended research program.

The evidence supports closing this inverse-problem line as a mathematical research direction. The results are suitable as a carefully scoped research note about what this model's observations conceal and reveal. This is a scope decision, not a claim that an equivalent result is absent from prior literature.

## 16. If viable: R13 theorem program

Not applicable. Decision B does not meet the R12 condition for proposing R13. No replacement research direction is proposed.

## 17. Limitations

- The arithmetic conclusions apply to the specified radix-\(q\) digit alphabet, modulus \(m\ge2\), and substitution/unequal-adjacent-transposition count spectra. They do not characterize other error models or check-digit systems.
- Exact observation means the full infinite position sequence. A finite observed prefix can fail to reveal stabilization or stable factors.
- The clipped-trajectory equivalence criterion is exact but is not a short parameterization of every nonzero class.
- Factorization recovery statements assume the observer can factor an exactly observed stable integer; computational factoring cost is outside this mathematical identifiability model.
- Enumeration is restricted to 13 listed radices and moduli 2–5000. It does not prove all-moduli statements.
- The literature comparison is limited to existing repository research notes. Gumm (1985) and Damm (2000) remain incompletely inspected; no novelty claim follows from material not located.

## 18. Recommended next action

Do not expand this line into R13. Retain this note as a bounded mathematical characterization and close the inverse-problem investigation unless a later, well-sourced prior-art comparison or a demonstrably non-elementary question changes the assessment. Keep the computational counts labeled as finite observations and the general identifiability statements labeled as proofs.
