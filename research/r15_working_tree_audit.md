# R15 — Working-Tree and Research Artifact Audit

> Historical audit snapshot preceding R16. Its documentation and full-table reproducibility recommendations are recorded as follow-up items here, not as the current uncompleted status.

## 1. Baseline and Change Separation

**Observed repository state:** `E:\modular-error-detection`, branch `main`, `HEAD` `e971497488dfea70699330dc7bd14643c9a996fa`, upstream `origin/main`. The branch status has no ahead/behind count. There are no staged changes.

At the start of this audit the tracked diff contained `README.md` and `python/modular_error_detection/__init__.py`. The latter was already modified before R14. The R14 changes were identified by comparing with the recorded pre-R14 status: `README.md` was then unchanged, while `python/modular_error_detection/radix_spectra.py` and `tests/test_radix_spectra.py` did not yet exist. Thus those are the three R14 paths; the initializer change and all other paths below are pre-existing work and were not modified by R14.

Pre-existing untracked files at the audit baseline:

- `python/financial_data_workbench/__init__.py`, `loader.py`, `results.py`, `schema.py`, and `validation.py`
- `python/modular_error_detection/profiles.py`
- Research notes: `deep_prior_art_comparison.md`, `detection_profile_engine.md`, `formal_model.md`, `literature_matrix.md`, `novelty_boundary.md`, `novelty_boundary_r8.md`, `prior_art_claim_matrix.md`, `r9_research_decision.md`, `r10_count_spectrum_theorem.md`, `r11_radix_generalization.md`, `r12_identifiability.md`, `r13_research_artifact_audit.md`, `research_direction.md`, and `theorem_review.md`
- `tests/test_detection_profiles.py` and `tests/test_financial_validation.py`

The full baseline was `## main...origin/main`, ` M README.md`, ` M python/modular_error_detection/__init__.py`, plus the untracked paths above and the two R14 additions. The tracked diff summary was 37 changed lines in `README.md` and 29 in the pre-existing initializer; the initializer's diff is not an R14 change. The worktree is intentionally not clean and must not be cleaned by reverting these paths.

## 2. R14 Source Review

`python/modular_error_detection/radix_spectra.py` is a focused, dependency-free module. Its public functions expose the radix pair weight, substitution and transposition spectra, the stabilization position, and bounded spectrum grouping. The two frozen, slotted result dataclasses contain only immutable scalar values and tuples. A class's representative is its first member; because moduli are visited in ascending order, that is the smallest member. Group order and membership are deterministic.

The inputs enforce integer radix $q\ge2$, modulus $m\ge2$, and nonnegative maximum position. Boolean values are rejected as integers. The modulus interval must be nonempty and ordered, and at least one spectrum type must be selected. Both selection flags must be actual booleans. These checks match the existing package style.

`max_position` is inclusive: the returned spectra cover positions $0,1,\ldots,K$. The flattened key concatenates the selected substitution sequence and then the selected transposition sequence. The result records which components were selected, so single-spectrum keys are interpretable. The API does not infer that a caller's endpoint is sufficient; its docstring and README correctly tell callers to use a shared endpoint at least as large as the largest stabilization position when comparing complete spectra.

The README imports the functions from the actual submodule, calculates the maximum endpoint for its stated modulus range, and passes the positional arguments in the implemented order. No CLI, dataframe, or generated output is claimed. The example's endpoint approach is consistent with the returned inclusive prefixes.

There was no pre-existing radix-generalized spectrum helper to reuse. `profiles.py` is specifically decimal: it hardcodes powers of 10, decimal coefficients 1 and 9, and 90 digit pairs. R14 leaves that API untouched and implements the general-radix equations in a separate module. This is a second implementation of the same *mathematical abstraction*, but not an incompatible definition: it follows R11 and is checked through a different computation in the new tests. The separation is appropriate; a shared implementation would require changing the decimal API or adding an abstraction not otherwise present.

## 3. Mathematical Consistency Audit

The canonical model is stated in [the formal model](formal_model.md) for decimal strings and generalized in [R11](r11_radix_generalization.md). R14 agrees with the generalized formulas:

- A digit replacement has change $\Delta_s=(b-a)q^k$, with the sign set by altered minus original. Only divisibility by $m$ affects detection.
- Swapping unequal high/low digits has change equal up to sign to $\Delta_t=(a-b)(q-1)q^k$. R14's direct test uses the high-place contribution at $k+1$ and low-place contribution at $k$, so its position convention is the same.
- `radix_pair_weight(q, h)` computes $W_q(h)=2\sum_{j=1}^{\lfloor(q-1)/h\rfloor}(q-hj)$. Its empty sum is zero for $h>q-1$, and at $h=1$ it returns $q(q-1)$, the ordered unequal-pair total.
- The reduced divisors are $m/\gcd(m,q^k)$ for substitutions and $m/\gcd(m,(q-1)q^k)$ for transpositions. Applying $W_q$ to these divisors gives the R11 spectra exactly.
- `radix_stabilization_position` computes $K(q,m)=\max_{p\mid q}\lceil v_p(m)/v_p(q)\rceil$, with zero when $m$ has no prime factor in common with $q$. This is the hidden reduced-divisor stabilization endpoint in R11/R12, not the possibly earlier stabilization of the clipped observed counts. At $K$, the radix-power factors have been canceled; evaluating through $K$, inclusive, is sufficient for the complete spectra.

Grouping compares observable count tuples, not reduced-divisor tuples. Therefore it preserves the distinction R12 makes between equality of spectra and equality of hidden divisors. R14 makes no all-moduli classification claim: an enumeration's classes are only for its chosen radix, modulus interval, selected coordinates, and position prefix. R12's table labels remain bounded to its 13 radices and $2\le m\le5000$.

No mathematical or position-convention discrepancy was found in R14.

## 4. Independent Validation Audit

`tests/test_radix_spectra.py::direct_pair_spectrum` enumerates all ordered pairs of distinct digits. For substitution it computes source and replacement contributions at $q^k$. For transposition it computes the original and swapped two-place contributions directly, then counts pairs whose difference is zero modulo $m$. It compares these counts with the production spectrum for $q=2,3,4,5$, $2\le m\le8$, and $k=0,1,2$. The test does not call the production $W_q$, gcd reduction, or spectrum functions to obtain expected values.

**Classification: MODERATE overall.** The validation route is genuinely independent of the closed pair-count and gcd formulas and exhausts every relevant digit pair in each selected test case. Its parameter grid is deliberately small, so it is strong for those cases but does not independently validate every radix, modulus, or endpoint in the bounded R11/R12 experiments. Fixed expected cases add useful checks: decimal (14,35), radix-11 (14,35), a non-equivalent decimal pair, and R11's radix-2 class count for (2\le m\le1000). The tests validate implementation behavior; the written derivations, not these tests, establish the general theorems.

## 5. Test Coverage Matrix

| Capability | Tested? | Independent? | Scope | Remaining gap |
|---|---|---|---|---|
| Integer residue and same-residue behavior | Yes: `test_checksum.py`; also used in profile enumeration checks. | Fixed expected residues; the checksum test is direct against integer arithmetic. | Nonnegative integer inputs and selected moduli/values. | No separate string-width behavior in the checksum API; string errors are tested in `test_errors.py`. |
| Substitution delta/event behavior | Yes: `test_errors.py`, analytical-count tests, and profile brute-force comparisons. | Direct source/replacement generation and altered-string residue comparison in selected cases. | Decimal model; all string positions in selected short strings. | No general-radix source-string generator or exhaustive arbitrary-radix string test. |
| Transposition delta/event behavior | Yes: `test_errors.py`, analytical-count tests, and profile brute-force comparisons. | Direct swap contributions/residues for selected decimal profiles; R14 direct digit-pair calculation for selected radices. | Unequal adjacent pairs; equal pairs excluded. | No general-radix full-string enumerator; the radix test checks pair spectra, not whole strings. |
| Decimal $W(h)$ | Yes: hand-expected values in `test_detection_profiles.py` and `test_analytical_counts.py`. | Fixed expected values; profile tests also compare integrated counts with direct enumeration. | Selected divisors and decimal alphabet. | No exhaustive independent comparison of the decimal helper for every positive $h$. |
| General $W_q(h)$ | Yes: R14 boundary tests and direct digit-pair cross-check. | Yes, by ordered-pair enumeration independent of the sum. | $q=2\ldots5$, small moduli and selected divisors. | Does not test all $q,h$; the universal theorem is in R11. |
| Reduced divisors | Yes: decimal factorization checks and R14 spectrum checks. | Decimal tests derive gcd components by factorization; R14's pair route bypasses reduced divisors. | Selected moduli and positions; R14 additionally checks small radix values. | No independent factorization cross-check over the entire R12 domain in the unit suite. |
| Stabilization | Yes: decimal factorization tests and R14 fixed examples. | Separate prime-valuation calculations in decimal tests; R14 compares known values. | Selected moduli, plus R14 examples for bases 2 and 10. | No exhaustive independent validation across all composite radices and modulus bounds in routine tests. |
| Exact `Fraction` rates | Yes: `test_detection_profiles.py` and analytical-count tests. | Exact count ratios are asserted; brute-force counts support selected cases. | Decimal per-position and finite-length profiles. | Radix spectrum counts are raw pair counts, not a rate API. |
| Finite-length event counts | Yes: fixed expected counts and direct source-string enumeration tests. | Direct enumeration for selected moduli and lengths. | Decimal strings, including leading zeros; selected lengths. | Not a complete rerun of all decimal strings for every configured sweep case in the ordinary unit tests. |
| Decimal exhaustive sweep | Saved CSV/report validated by `test_analytical_counts.py`; sweep command is documented. | Analytical validator uses a different calculation from the source-edit sweep; tests reconcile saved outputs. | Saved moduli 2–30, lengths 1–4; 232 per-length and 58 aggregate rows. | The test suite does not rerun the exhaustive sweep; artifact freshness is a separate manual/release check. |
| Radix spectra | Yes: `test_radix_spectra.py`. | Direct ordered-pair changes for small parameters. | Selected small cases and fixed R11/R12 examples. | The test suite does not reproduce the full 13-radix, $m\le5000$ table. |
| Spectrum grouping | Yes: equality/difference membership test and known examples. | Key equality is checked against returned classes; deterministic repeated run is checked. | Small bounded domains and selected equivalence pairs. | No exhaustive test of all documented full-domain class counts in the test suite. |
| Identifiability observations | No dedicated executable identifiability API/tests. | R12 includes formula-derived examples and the bounded table; R14 can reproduce table counts. | Mathematical claims are in R12; computations are bounded. | No test for the general identifiability propositions; no separate code API for identifiability. |
| README/API examples | No automated doctest. | The example follows the current function signatures; R14's bounded computations exercised the same API pattern. | One decimal radix example over moduli 2–5000. | README example is not executed by pytest and does not itself loop over all 13 R12 radices. |

The `test_financial_validation.py` cases cover only the separate workbench and do not validate the modular-residue research. There is no dedicated test that runs `run_modulus_sweep.py` end to end; the analytical tests check stored artifacts instead.

## 6. Reproducibility Audit

`pyproject.toml` specifies Python 3.12 or later, setuptools package discovery from `python/`, no runtime dependencies, and pytest as an optional development dependency. The README documents editable installation with `python -m pip install -e ".[dev]"`, `python -m pytest`, and the root-level sweep, plot, per-length analysis, and analytical validator commands. It also documents the radix API and how to choose a common complete-spectrum endpoint. The package can be imported as `modular_error_detection.radix_spectra` after installation; the existing decimal profile APIs remain in `profiles.py`.

The defined enumerations are deterministic: they use integer arithmetic, ascending modulus iteration, insertion-ordered grouping, and no random data or network access. The stored decimal reports are computational outputs; the decimal and radix algebraic identities and R11/R12 identifiability statements are presented as proofs. The finite decimal sweep and radix class tables are observations over explicitly bounded domains, not proofs beyond those domains.

The README makes the per-length and analytical-report overwrite behavior explicit and accurately distinguishes those generated output targets from their read-only CSV/aggregate inputs. R14 does not provide a CLI or a command that writes the radix table, which is consistent with its API-only scope. The API can reproduce the R12 table when invoked for each listed radix with a shared endpoint, but the README snippet demonstrates one radix only; no checked-in one-command driver reproduces the entire 13-row table. This is a convenience/reproducibility gap, not a formula defect.

One status inconsistency remains in the documentation: `research/formal_model.md:289` lists generalizing the decimal results to an arbitrary base as an open question, while R11 has since supplied the general-radix derivation. The formal model can remain explicitly decimal-only, but that question should be marked as answered elsewhere or removed from the active-question list in a documentation-only pass. `research/research_direction.md` also includes older proposed directions and R6-era status; it should be read as a historical planning record, not the latest decision.

## 7. Research-Claim Audit

| Classification | Findings in the inspected repository |
|---|---|
| **A. Mathematically established** | R11 proves the stated radix-$q$ change formulas, pair-weight formula and threshold behavior, reduced-divisor spectra, and stabilization. R12 proves its stated exact observable-equivalence and identifiability results under its definitions. The decimal modulus-11 and moduli-3/9 claims are scoped to the two specified error models. |
| **B. Computationally demonstrated** | The decimal sweep covers its finite configured grid. R11/R12 class counts are finite enumerations; R14 supplies a reusable API and tests several fixed/small cases. The full R12 table was also recomputed through the API during the R14 implementation work, but that one-off run is not a checked-in test command. |
| **C. Literature-supported in the research record** | The literature notes compare the project with weighted checks and check-character systems and cite Verhoeff, Schulz, ISO/IEC 7064, and other works. ISO/IEC 7064 is discussed as a family of specified standardized systems, not as identical to this plain-residue model. The R15 audit did not independently retrieve external source texts; these classifications reflect the repository's documented source review. |
| **D. Unresolved** | The exact prior-art relationship for the spectrum-equivalence/identifiability framing remains unresolved. The checked-in records state that Gumm (1985) and Damm (2000) full texts were not successfully inspected. “Not located” in a bounded review is not absence of prior work. No negative priority claim is supported. |
| **E. Exploratory or historical** | R9–R11 contain chronological research decisions and candidate directions. R12 gives the latest explicit decision: “interesting but elementary” and close the inverse-problem line absent stronger evidence. Earlier `research_direction.md` questions should not be mistaken for current selected work. |

The search for claim language found no unsupported novelty or priority claim in the README, R11, or R12. Older notes use “new” in bounded/contextual descriptions, while also explicitly disclaiming novelty; for example, `novelty_boundary.md` says equivalence research is not unprecedented, and `deep_prior_art_comparison.md` describes close prior work. Those qualified statements should remain read in context. The source-access limitations and no-novelty boundary are clear in R11/R12; the audit does not extend the literature search or make fresh claims about Verhoeff, Gumm, Damm, Schulz, or ISO/IEC 7064.

## 8. Research Artifact Inventory

| Group | Document | Status and continuing role |
|---|---|---|
| **FOUNDATION** | [`formal_model.md`](formal_model.md) | Useful decimal specification and proof record. It is not the general-radix specification. Its open-question bullet at line 289 is stale after R11 and should be annotated in a future documentation pass. |
| **FOUNDATION** | [`literature_matrix.md`](literature_matrix.md) | Useful claim/source summary. Retain as the navigable synthesis, with unresolved source access visible. |
| **FOUNDATION** | [`theorem_review.md`](theorem_review.md) | Useful historical independent review, not the canonical proof source. Findings should be treated as a review snapshot. |
| **IMPLEMENTATION / ANALYSIS** | [`detection_profile_engine.md`](detection_profile_engine.md) | Useful implementation note for the decimal profile API. Keep its decimal scope distinct from the radix module. |
| **IMPLEMENTATION / ANALYSIS** | [`r10_count_spectrum_theorem.md`](r10_count_spectrum_theorem.md) | Useful historical derivation/examples for decimal count-spectrum equivalence; later generalized by R11/R12. Retain as chronology. |
| **IMPLEMENTATION / ANALYSIS** | [`r11_radix_generalization.md`](r11_radix_generalization.md) | Current mathematical authority for general-radix spectra and Wq; includes bounded R11 table. Retain. |
| **IMPLEMENTATION / ANALYSIS** | [`r12_identifiability.md`](r12_identifiability.md) | Latest explicit mathematical conclusion and bounded R12 table. Retain as the current closure of that line. |
| **IMPLEMENTATION / ANALYSIS** | [`r13_research_artifact_audit.md`](r13_research_artifact_audit.md) | Historical audit and consolidation recommendation. Useful provenance, not a specification. |
| **IMPLEMENTATION / ANALYSIS** | R14 source/tests/README section | The implementation is in `python/modular_error_detection/radix_spectra.py` and `tests/test_radix_spectra.py`; there is no separate R14 research note. The code is executable evidence, not a substitute for R11/R12 proofs. |
| **PRIOR-ART BOUNDARY** | [`prior_art_claim_matrix.md`](prior_art_claim_matrix.md) | Useful claim-to-source comparison; retain, recognizing source limitations stated in it. |
| **PRIOR-ART BOUNDARY** | [`deep_prior_art_comparison.md`](deep_prior_art_comparison.md) | Detailed source notes that complement the matrix. Some overlap is intentional; use it as evidence detail rather than a competing decision. |
| **PRIOR-ART BOUNDARY** | [`novelty_boundary.md`](novelty_boundary.md) | Historical R7 boundary; useful record, potentially overlapping later matrices. Retain as history. |
| **PRIOR-ART BOUNDARY** | [`novelty_boundary_r8.md`](novelty_boundary_r8.md) | Later boundary refinement; useful historical state, partially superseded by R9/R12. Retain as chronology. |
| **PRIOR-ART BOUNDARY** | [`research_direction.md`](research_direction.md) | Broad earlier planning document; potentially redundant and partly superseded by the R12 decision. Retain but label/link as historical before presenting it as active direction. |
| **PRIOR-ART BOUNDARY** | [`r9_research_decision.md`](r9_research_decision.md) | Historical decision record superseded as current status by R12's explicit closure. Retain as chronology. |

No document should be deleted or merged as part of this audit. A future navigation pass could point from older decision documents to R12, clarify the formal-model scope, and designate one current literature summary while retaining detailed source records.

## 9. README Audit

The README identifies the decimal error models, fixed-width/leading-zero convention, finite sweep scope, installation/test commands, report outputs, and non-cryptographic limitation. Its new research-positioning sentence is conservative and explicitly disclaims novelty. It now links the formal model, R11, R12, and R13. The radix example matches the implemented module and calls `radix_stabilization_position` for every modulus before using the maximum as the inclusive endpoint.

The README does not claim that R14 enumerates digit strings or writes the R11/R12 tables. It says it groups analytical count spectra, which is accurate. No inaccurate API names or constructor arguments were found. Attribution is available in research references, but this checkout has no root `LICENSE`, `COPYING`, or `NOTICE`; distribution terms therefore remain unspecified. This is not an R14-created issue and is separate from mathematical correctness.

Recommended README/documentation follow-up is limited: link or describe the full 13-radix reproduction if a one-command rerun is desired, and clarify that the README's general research scope links to separate decimal and radix specifications. No README correction specific to R14 is required by this review.

## 10. Financial Workbench Separation

The financial package is a separate `financial_data_workbench` namespace and its untracked files are not imported by the modular checksum package or its experiment scripts. The README and formal mathematical model describe the checksum research without presenting financial validation as a mathematical contribution. R13 explicitly describes the workbench as separate local work. No conceptual boundary issue was found in the inspected README/research framing. This audit did not review the financial implementation's correctness.

## 11. Public-Research Readiness

| Dimension | Status | Basis |
|---|---|---|
| Mathematical specification | **READY** | Decimal and general-radix models are separately documented; R11/R12 provide proofs and state their assumptions. |
| Implementation | **READY** | Decimal profiles and the bounded radix spectrum API implement the stated formulas; R14 passes input, deterministic grouping, and example checks. |
| Independent validation | **PARTIALLY READY** | Direct digit-pair checks independently validate small radix cases, but the routine suite does not independently cross-check the entire q=2..20, m≤5000 grid. |
| Reproducibility | **PARTIALLY READY** | Decimal commands are documented; the radix API can reproduce bounded tables, but there is no checked-in command that emits the entire R12 table and README demonstrates only q=10. |
| Literature boundary | **PARTIALLY READY** | The records are cautious and explicit about unresolved Gumm/Damm access; they are not a fresh or exhaustive literature review. |
| Documentation | **PARTIALLY READY** | Useful authorities exist, but the formal model retains a stale arbitrary-base open question and older planning documents are not uniformly marked superseded/historical. |
| Test coverage | **PARTIALLY READY** | Strong coverage of the decimal package and focused R14 tests; generalized-radix testing is narrow and no README doctest/full R12 table regression is present. |
| Research-claim discipline | **READY** | Current README and R11/R12 avoid novelty claims, separate proofs from bounded observations, and disclose unresolved prior art. |

These are readiness labels by dimension, not an aggregate score or ranking.

## 12. Minimum Remaining Work

No R14 correctness fix is required. Before presenting the repository as a stable, internally consistent research artifact, the minimum evidence-supported follow-up is a documentation-only pass that:

1. Marks the arbitrary-radix question in `formal_model.md:289` as addressed by R11 while retaining the formal model's decimal-only scope.
2. Makes R12's closure the clearly current research decision and points older planning/decision notes to it, without deleting historical records.
3. States a reproducible command or small script/example for rerunning the complete 13-radix R12 table if full-table reproducibility is a release criterion. The existing API already supports this; no new math or public abstraction is needed.

Optional distribution work includes choosing and adding a root license. It is not a correctness blocker and was not part of R14. No financial changes, theorem extensions, or novelty search are warranted by this audit.

## 13. Final Assessment

R14 is mathematically consistent with the model in R11/R12 and with the separate decimal-only API in `profiles.py`. Its `W_q`, reduced-divisor spectra, position convention, inclusive endpoint, and class-key behavior agree with the established definitions. The direct-pair tests provide a genuinely separate validation route, classified **MODERATE** for the implementation overall because the tested radix/modulus domain is intentionally small.

No concrete correctness or documentation error introduced specifically by R14 was found. No R14 correction is required. The remaining issues are documentation status drift, bounded test coverage, and lack of a checked-in one-command reproduction of the entire R12 table. The existing research documents consistently bound class-count observations and state that literature overlap remains unresolved; this audit did not independently access external publications.

## 14. Exact Next Step

The next step is a narrowly scoped documentation consolidation: update the stale open-question status in `research/formal_model.md`, identify R12 as the current closure in older planning notes, and add a concise full-table reproduction recipe using the existing radix API if repeatability of all 13 R12 rows is required. Preserve all historical notes and the current mathematical scope. Do not expand the mathematics or make a novelty claim.
