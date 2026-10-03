# Research Direction: Complete Profiles of Plain Modular Decimal Residues

> Historical research-planning document. The questions and candidate directions below record the project's development at that stage and should not be read as the current research conclusion. R12 records the later decision to close the inverse-problem line as interesting but elementary.

## 1. Current research position

The project defines a plain residue check on fixed-width decimal strings and two error classes: one-digit substitutions and unequal adjacent transpositions. Its formal model derives exact position-wise undetection conditions, universal detection criteria, prime-factor limits, and exact pair/event counts. The existing finite sweep enumerates moduli 2-30 and lengths 1-4; the analytical validator is reported to reconcile all 232 per-length rows and 58 aggregate rows.

The theorem review found the mathematics correct but elementary, and the literature matrix records substantial earlier work on decimal error-detecting codes and check digits. The exact relationship of the project's factorized characterization to prior publications remains **not established as novel; insufficiently located in the searched literature**. A “complete detection profile” is a coherent way to organize this project's exact results, but the name itself does not establish a new result or a paper-level contribution.

## 2. Definition of a detection profile

Fix an integer modulus `m>1` and string length `n>=1`. Define the applicable position set for substitutions as `K_s(n)={0,...,n-1}` and for adjacent transpositions as `K_t(n)={0,...,n-2}`; `K_t(1)` is empty. For error class `e`, position `k`, and nonzero decimal difference `d in D*={-9,...,-1,1,...,9}`, define an indicator

```text
delta_e(m,k,d) = 1 if the event is detected, and 0 otherwise.
```

With `c_s=1`, `c_t=9`, and `h_e(m,k)=m/gcd(m,c_e*10^k)`, the exact profile is

```text
delta_e(m,k,d) = 1 iff h_e(m,k) does not divide d.
```

A **position-resolved exact detection profile** for `(m,n)` is the collection, for each applicable error class and position, of:

1. the undetection set `{d in D*: h_e(m,k) divides d}` and the universal guarantee flag;
2. the exact total, undetected, and detected event counts at that position;
3. an optional detection rate under an explicitly declared measure.

This divides the profile into three kinds of quantities:

- **Qualitative guarantee:** all events of the specified class/position are detected iff `h_e(m,k)>9`. This is distribution-free.
- **Exact counts:** these count discrete events and require the event definitions but no probability model.
- **Rate/probability:** the natural project rate is the fraction of all modeled events detected when events in the specified finite set are sampled uniformly. It is a probability only under that uniform event measure. Under a different source-string or error distribution, a different probability results.

The full profile across all finite lengths can be represented as two sequences indexed by `k>=0`, one for each error class. A profile for fixed length `n` is just the valid prefix of each sequence. A zero-event transposition profile at `n=1` has no rate; it is not zero percent.

## 3. Natural parameters

The minimal inputs to evaluate a particular event's detection are `(m,e,k,d)`: modulus, error class, position, and digit difference. The length `n` determines whether position `k` exists and is needed for string-level event totals and length rates. The source string itself is unnecessary for detection or aggregate counts once the valid digit-pair choices are accounted for.

Several candidate parameters are derived rather than independent:

- `c_e` is determined by error class (`1` for substitution, `9` for adjacent transposition).
- `h_e(m,k)` is determined by `m`, `e`, and `k`; it is the sufficient arithmetic parameter for undetection at that position.
- The digit difference `d` is necessary for an individual event; it can be omitted for a universal guarantee or an event count after summing over `D*`.
- Prime factorization is a way to calculate and understand the `h` sequences, not an additional independent input.
- Leading-zero values do not change the residue formulas, but width is essential to define position and the number of source strings/events.

For exact rate reporting, the measure is also part of the specification. The project counts each eligible event equally, not each source string equally.

## 4. Modulus classification possibilities

There are two distinct notions of profile equality.

**Exact reduced-divisor equality.** Two moduli have the same exact `h_s(k)` and `h_t(k)` sequences iff their sequence pairs agree at every index. This completely determines undetection sets and counts. It is not a useful grouping of distinct moduli: `h_s(0)=m`, so equality of exact substitution sequences already forces the moduli to be equal.

**Observable behavioral equality.** Define `phi(h)=h` for `1<=h<=9`, and `phi(h)=TOP` for `h>9`, where `TOP` means no nonzero decimal digit difference is divisible by `h`. Then two moduli have identical position-wise qualitative guarantees, undetection-difference sets, and `W(h)` counts for all positions and both error classes exactly when their `phi(h_s(k))` and `phi(h_t(k))` sequences agree. For `h<=9`, the multiples in `D*` identify `h` (and so does `W(h)`); for `h>9`, the undetection set and pair count are empty. This is a mathematically natural observational equivalence if a grouped atlas is desired. It is not the same as equality of exact reduced divisors, and it need not preserve numerical modulus, total string count, or applications that use `m` itself.

For a fixed maximum length, truncate the signatures to the valid position prefixes; this may merge more moduli than the all-position equivalence. Whether presenting these groups is useful is an output/design choice. No new or uniquely valuable classification has yet been demonstrated.

## 5. Prime-factor structure

Write `m=2^a*3^b*5^c*u`, with `gcd(u,30)=1`.

### A. Substitutions

```text
h_s(m,k) = 2^(a-min(a,k))*3^b*5^(c-min(c,k))*u.
```

The exponents of 2 and 5 decrease during a finite transient and are exhausted by `k>=max(a,c)`. The 3-power and `u` remain. The stabilized divisor is `3^b*u`.

### B. Adjacent transpositions

```text
h_t(m,k) = 2^(a-min(a,k))*3^(b-min(b,2))*5^(c-min(c,k))*u.
```

Here `9=3^2` cancels up to two powers of 3 immediately. Any remaining 3-power stays unchanged as `k` grows; powers of 2 and 5 cancel after a finite number of positions. The stabilized divisor is `3^max(b-2,0)*u`.

These stabilized values characterize the all-finite-length universal guarantees by comparison with 9, but do not alone give the complete profile: the transient `h` values are needed for short positions, exact missed differences, and rates. To produce every `h` from factorization, the actual value of `u` and all exponents are used. Prime categories alone (e.g. “prime” versus “composite”) do not determine behavior.

## 6. Position/length behavior

For substitutions, `gcd(m,10^k)` stabilizes at `2^a*5^c` once `k>=max(a,c)`. For transpositions, `gcd(m,9*10^k)` stabilizes at `2^a*3^min(b,2)*5^c` once

```text
k >= max(a,c).
```

The factor `3^min(b,2)` is present from `k=0`; increasing `k` only adds powers of 2 and 5 to the gcd. Each gcd sequence is nondecreasing by divisibility and reaches its maximum after finitely many terms. The corresponding reduced-divisor sequences are nonincreasing and eventually constant. There is a finite transient followed by a constant tail, not a periodic sequence. For fixed length, only the first `n` substitution positions and first `n-1` transposition positions are present.

## 7. Exact counting framework

For positive integer `h`, let `W(h)` be the number of ordered unequal digit pairs `(a,b)` with `h|(b-a)`. The exact formula is

```text
W(h)=2*sum_{j=1}^{floor(9/h)}(10-h*j), with W(h)=0 when h>9.
```

At substitution position `k` in length `n`,

```text
total_s(k,n)      = 90*10^(n-1)
undetected_s(k,n)  = W(h_s(m,k))*10^(n-1)
detected_s(k,n)    = (90-W(h_s(m,k)))*10^(n-1)
rate_s(k,n)        = 1-W(h_s(m,k))/90.
```

At transposition position `k` for `n>=2`,

```text
total_t(k,n)      = 90*10^(n-2)
undetected_t(k,n)  = W(h_t(m,k))*10^(n-2)
detected_t(k,n)    = (90-W(h_t(m,k)))*10^(n-2)
rate_t(k,n)        = 1-W(h_t(m,k))/90.
```

These counts follow because each position has 90 ordered unequal digit pairs and the unaffected positions are free decimal digits. Summing over positions gives

```text
T_s(m,n)=90*n*10^(n-1)
U_s(m,n)=10^(n-1)*sum_{k=0}^{n-1} W(h_s(m,k))
R_s(m,n)=1-U_s(m,n)/T_s(m,n)

T_t(m,n)=90*(n-1)*10^(n-2), n>=2
U_t(m,n)=10^(n-2)*sum_{k=0}^{n-2} W(h_t(m,k))
R_t(m,n)=1-U_t(m,n)/T_t(m,n).
```

For `n=1`, set transposition total and undetected counts to zero and leave the rate undefined. These length-level formulas weight every event equally. Since every position has equal total event count, the length rate is also the arithmetic mean of the position rates; rates pooled over different lengths must instead weight by the number of events at each length.

Thus `h` is sufficient for a position's complete detection signature and `W(h)` is sufficient for its event count/rate. The whole profile additionally needs valid positions and the free-position multipliers.

## 8. Role of exhaustive computation

The existing sweep covers moduli 2-30, lengths 1-4, every fixed-width decimal string, and every event in the two generators. The theorem and `W(h)` formulas determine the results analytically; enumeration does not add mathematical information beyond those formulas for the same domain.

The sweep does provide concrete tables/plots, makes the finite landscape easy to inspect, and checks that the implementation's event generation and residue comparisons agree with independent formulas. It can also help expose implementation errors or suggest patterns to prove. Once the formulas are known, however, a displayed pattern is not a new discovery merely because it appears in the table. Existing report text says 232 per-length rows and 58 aggregate rows reconcile with analytical counts. This phase did not rerun the sweep or validator.

## 9. Candidate computational research questions

| Candidate | Critical assessment |
|---|---|
| **RQ-A:** Can behavior for substitutions and adjacent unequal swaps be completely classified from modulus prime factors? | For the universal all-length guarantee, yes: the stabilized criteria give an exact answer. For complete finite-position profiles, the full factorization and finite transient are required, not only the two stabilized thresholds. The present derivation substantially answers this within the model; novelty is unestablished and the result is elementary. |
| **RQ-B:** Can exact profiles be generated analytically for arbitrary `m` and finite `n`, without enumerating strings? | Yes in principle: compute the finite `h` sequences and apply closed-form `W(h)` counts. This is a useful implementation/reproducibility objective, but its mathematical content largely follows from the existing derivation. Success requires exact position and length counts/rates matching the formulas, plus clear zero-event handling. |
| **RQ-C:** What behavioral equivalence classes of moduli result when profiles are compared across all positions or a bounded length range? | The signature `phi(h)` gives a precise candidate equivalence. It may compress an atlas, but its value depends on whether the induced classes reveal interpretable structure beyond grouping identical observables. Success requires proving the equivalence criterion and documenting the scope of preserved quantities. |
| **RQ-D:** Does an exhaustive computational atlas reveal structural behavior not apparent from isolated check-digit examples? | It can display a landscape and validate code, but analytical profiles already determine the modeled counts. A claim of new structure requires a specified observable and evidence that it is not a restatement of the formulas or established check-digit work. |
| **RQ-E:** How do plain residues compare with Luhn, Verhoeff, Damm, or ISO 7064? | Potentially useful as a secondary controlled comparison, but not well-posed until exact variants and event domains are matched. This would broaden the current mathematical scope and does not follow from the existing sweep. |

## 10. Check-digit comparison scope

Treat Luhn, Verhoeff, Damm, and ISO 7064 as **background/discussion only** for the current profile question. A future comparison could be a separate secondary experiment; it should not be central unless the research question changes and comparable implementations are specified.

A fair comparison must state: the decimal alphabet; whether inputs include or append a check character; length conventions; whether the check character may itself be corrupted; the exact valid-code/check-digit rule; which positions and edits are in the error domain; whether equal swaps are excluded; how leading zeros are treated; whether weights/transformations depend on position; and the event measure used for rates. A weighted sum or group/quasigroup check character is not the same object as `N(x) mod m`. Comparisons that ignore these choices would conflate different error models.

## 11. Possible paper positioning

- **Pure mathematical paper:** the exact criteria are clean and general within the model, but the arguments are short elementary arithmetic. Without a deeper classification theorem, new structure, or nontrivial extension, this framing is weak.
- **Computational mathematics paper:** exact formulas plus a finite exhaustive profile can provide analytical-computational cross-validation. Its strength is transparent, reproducible counts; limitation is that formulas already determine the finite results.
- **Experimental computer science paper:** executable sweep, tests, reports, and plotted profiles support reproducibility. The finite scope and deterministic toy error model limit claims about actual error processes.
- **Software/reproducibility paper:** reusable validators and exact report reconciliation are demonstrable engineering outputs. A paper would need evidence of broader utility, quality, or adoption beyond one repository's study.
- **Applied data-integrity paper:** would require a target data domain, an empirically justified error distribution, and comparison against suitable deployed methods. The current model and evidence do not provide these.

At present no paper type is supported as publication-ready by the existing evidence. If the work is developed, the most defensible framing is an analytical/computational reproducibility study, with explicit modest scope; that framing still requires a literature review sufficient to establish its contribution.

## 12. Candidate contributions

| Candidate contribution | Mathematical content | Computational content | Literature overlap | Evidence currently available | Additional work required | Risk of being too elementary | Potential research value |
|---|---|---|---|---|---|---|---|
| Unified formalization | Defines strings, events, detection, quantifiers | Makes formulas and counts comparable | Decimal error codes and check-digit theory are established | `formal_model.md`, code/report conventions | Compare definitions with primary sources and tighten notation | High | Useful reproducibility foundation |
| Exact factorization characterization | Reduced gcd sequences and all-length guarantee thresholds | Can predict finite positions too | Prior decimal/check-digit theory is substantial; exact overlap unresolved | Proof in formal model and theorem review | Deeper full-text prior-art review; prove any genuinely broader synthesis | High | Compact exact characterization if its relation to literature is clarified |
| Complete modulus profiles | Per-position signatures and event statistics | Profile table for arbitrary moduli/lengths | Close to general check-digit analysis; exact plain-residue coverage uncertain | Closed forms from `h` and `W` | Define minimal outputs and demonstrate interpretive use | Medium-high | Makes guarantees and rates auditable together |
| Exact event-count formulas | Pair count `W(h)` and free-position factors | Avoids enumerating all strings | Error statistics/counting are well-established themes | Hand derivation and validator | Compare counts independently and cover arbitrary parameters | High | Efficient exact oracle for software validation |
| Exhaustive computational atlas | No new theorem by itself | Finite tables/plots over modulus/length grid | Verhoeff documents a prior search program; other prior enumeration unknown | Existing 2-30, 1-4 outputs | Reproducible generation and explain what patterns add beyond formulas | Medium-high | Accessible map and regression artifact |
| Reproducible validation framework | Mathematical validation logic | Tests and reconciliation of source artifacts | Software validation is not the same as a checksum theorem | Existing analytical validator and reported reconciliations | Independent implementation review and documentation | Low-medium | Strongest current engineering/reproducibility artifact |
| Comparison with established schemes | Requires separate scheme-specific mathematics | Controlled parallel event enumeration | Directly overlaps extensive algorithm literature | Background documents only; no implementations in this phase | Select variants, define common error domain, verify sources and code | Medium | Could contextualize results, but easily becomes incomparable or too broad |

## 13. Claims to avoid

The project should not frame itself as:

- “modulus 11 is best” or “modulus 11 solves error detection”;
- a new checksum algorithm;
- financial fraud detection;
- cryptographic security or authentication;
- AI-based error detection or machine learning for checksum optimization.

Those claims are unsupported by the model, outputs, or literature review. The modulus-11 guarantee applies only to the specified substitutions and unequal adjacent swaps in this plain-residue model.

## 14. Candidate research questions

### Candidate 1

**Question:** What is a complete exact position-resolved detection profile for plain modular decimal residues at arbitrary modulus `m` and length `n`?

- **Mathematical scope:** Undetection sets, universal flags, and exact event counts for the two defined error classes.
- **Computational scope:** Generate profile rows from gcd sequences and `W(h)`, without string enumeration.
- **Literature overlap:** Check-digit profiles and error counts are established topics; exact plain-residue formulation remains insufficiently located.
- **Successful answer:** A specification and formulas that determine every profile row and its rate under the uniform-event measure.
- **Evidence required:** Proof of formulas, exact comparisons over selected finite cases, and verified prior-art comparison.
- **Main risk:** It may be a convenient packaging of already elementary formulas rather than a research contribution.

### Candidate 2

**Question:** What is the coarsest modulus equivalence relation preserving all qualitative guarantees and exact event rates for the two error classes, at all positions and lengths?

- **Mathematical scope:** Equivalence via identical `phi(h_s(k))` and `phi(h_t(k))` sequences; characterize classes arithmetically.
- **Computational scope:** Produce representative classes and finite-range atlas summaries.
- **Literature overlap:** Related to code equivalence/classification, but direct comparison is needed.
- **Successful answer:** Necessary and sufficient conditions for profile equality, with a useful arithmetic class description.
- **Evidence required:** Proof that `phi` preserves and distinguishes the profile observables; literature search; examples showing whether classes aid interpretation.
- **Main risk:** The equivalence may be formally correct but trivial or have little explanatory value.

### Candidate 3

**Question:** How do position-dependent checksum weights alter exact substitution and adjacent-transposition profiles over decimal strings?

- **Mathematical scope:** Generalize deltas to `d*w_k` and `d*(w_(k+1)-w_k)`, then characterize divisibility by `m`.
- **Computational scope:** Compare selected weight families using exact event counts.
- **Literature overlap:** High; weighted check digits and established algorithms already address these error classes.
- **Successful answer:** A precisely delimited theorem that unifies a nontrivial family and agrees with carefully chosen checks.
- **Evidence required:** Primary-source review, exact definitions, proofs, and a reason the generalized theorem adds insight.
- **Main risk:** Re-deriving known weighted-code conditions without a meaningful synthesis.

### Candidate 4

**Question:** Does the finite sweep reveal implementation or reporting errors that exact profiles can detect, and how can the verification be made independent?

- **Mathematical scope:** Exact profile formulas serve as oracle for finite counts.
- **Computational scope:** Independent generation, reconciliation, and reproducible artifact checks.
- **Literature overlap:** Reproducible computational mathematics and software verification; specific prior art needs investigation.
- **Successful answer:** Demonstrate that independently produced counts reconcile, with clear failure detection and immutable source results.
- **Evidence required:** Independent implementation/design, documented runs and differences, and a bounded literature review.
- **Main risk:** A sound software-quality project may still not be a mathematical research paper.

## 15. Recommended working research question

**Working question:** *What is the minimal exact representation of the position-wise substitution and unequal-adjacent-transposition detection profiles of plain modular decimal residues for arbitrary modulus and finite length, and what modulus equivalence classes preserve those profiles?*

This focuses the project on the profile framing without assuming novelty. The existing `h` sequences and `W(h)` formulas already provide a candidate complete representation, and `phi(h)` gives an observational equivalence candidate. A successful answer must prove sufficiency and minimality for the declared observables, clarify whether the induced classes are interpretable, and compare the exact formulation with prior literature. It may conclude that the result is too elementary or not distinct from existing theory.

## 16. Provisional contribution statement

**Provisional statement:** “This study develops an exact, position-resolved account of single-substitution and unequal-adjacent-transposition detection for plain modular residues of fixed-width decimal strings. It expresses undetection through reduced gcd conditions, derives event counts from ordered digit-pair counts, and uses exhaustive finite computations to check the implementation and illustrate profiles over a stated modulus and length range. The relation of the exact formulation to prior literature, and its significance as a research contribution, remain under investigation.”

This describes work that could be supported by the current mathematics and outputs; it makes no novelty claim.

## 17. Recommended next research phase

**R6 status:** the proposed exact analytical detection-profile engine has now been implemented in `modular_error_detection.profiles`; see [the engine notes](detection_profile_engine.md). That implementation does not rerun or overwrite the historical experiment artifacts. The underlying literature relationship and research significance remain open; implementation alone does not establish novelty.
