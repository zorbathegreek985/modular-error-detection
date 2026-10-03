# R13 — Research Artifact Audit

> Historical audit snapshot. Its proposed radix-spectrum capability was implemented in R14; R16 records the later full-table reproduction command and documentation consolidation.

## 1. Current project purpose

The mathematical project studies whether a plain integer residue changes under a single-digit substitution or an unequal adjacent transposition of a fixed-width decimal string. It combines elementary derivations, a finite exhaustive decimal sweep, analytical profiles and validators, reports, and plots. The broader research notes extend the formulas to radix \(q\), then examine what arithmetic information is lost when finite-alphabet error counts are observed without their reduced divisors.

The separate `financial_data_workbench` package is a configurable CSV validation library. It is not part of the checksum model and should remain a separate product concern. In this checkout it contains only the loader, schema, result, and validation modules; no reporting or CLI modules are present. These modules and their test are untracked local work, not part of the stated `HEAD` commit.

**Repository state observed:** directory `E:\modular-error-detection`, branch `main`, `HEAD` `e971497488dfea70699330dc7bd14643c9a996fa`. The working tree was already dirty before this audit: `python/modular_error_detection/__init__.py` was modified, and the financial modules, profile module, research notes, and related tests were untracked. The research conclusions below describe the inspected working-tree snapshot where noted; they must not be mistaken for content already published at `HEAD`.

## 2. Mathematical results inventory

The following are established within the stated model:

- **Proof:** for a fixed-width radix-\(q\) string, a substitution at place \(q^k\) changes the integer value by \(\Delta_s=(b-a)q^k\). Swapping higher-place digit \(a\) and lower-place digit \(b\) changes it by \(\Delta_t=(a-b)(q-1)q^k\). Detection is exactly a nonzero residue change modulo \(m\).
- **Proof:** gcd cancellation gives the necessary-and-sufficient undetection tests using \(h_s=m/\gcd(m,q^k)\) and \(h_t=m/\gcd(m,(q-1)q^k)\).
- **Proof:** \(W_q(h)=2\sum_{j=1}^{\lfloor(q-1)/h\rfloor}(q-hj)\) counts ordered unequal digit pairs with difference divisible by \(h\); it is zero above \(q-1\) and strictly decreasing on its positive range.
- **Proof:** multiplying the per-position pair counts by the free digit choices gives the finite-length event counts and exact rates. Prime valuations give finite stabilization and the stable reduced divisors.
- **Proof:** in decimal, modulus 11 detects every event of the two defined types at every finite length; moduli 3 and 9 detect no unequal adjacent transposition. These conclusions are limited to the stated event models.
- **Proof in R12:** equal observable spectra are exactly equality of both thresholded reduced-divisor trajectories. The zero joint class is infinite; each nonzero joint class is finite. The hidden stabilization index \(K\) is recovered from a nonzero complete spectrum but not from an all-zero one. These are elementary consequences of the same finite-alphabet threshold and valuation formulas, not a novelty claim.

**Computational observations:** the saved decimal sweep covers moduli 2–30 and lengths 1–4. R11 describes a bounded radix enumeration through modulus 1000; R12 describes an expanded enumeration through modulus 5000 for 13 radices. These finite results do not establish statements outside their ranges. Literature overlap is not settled: in particular, the full Gumm (1985) and Damm (2000) sources remain unresolved in the research record.

## 3. Implementation-to-mathematics mapping

| Mathematical object | Implementation in this checkout | Tests or documents | Audit assessment |
|---|---|---|---|
| Integer checksum and same residue | `python/modular_error_detection/checksum.py`: `checksum` and `same_residue` operate on nonnegative integers, not width-bearing strings. | `tests/test_checksum.py`; `research/formal_model.md` defines the string-level map. | Implemented. Unit tests cover fixed examples and invalid inputs. The string-to-integer correspondence is simple, but this API does not itself retain width. |
| Substitution and adjacent-swap deltas | Not exposed as delta functions. The error generator edits strings; `profiles.py` uses coefficients 1 and 9 in the reduced-divisor calculation. | Proofs in `formal_model.md` and `theorem_review.md`; profile brute-force comparison tests. | Formula is documented and proved; implementation represents it indirectly through coefficient selection. |
| Reduced divisor | `profiles.reduced_divisor(m, coefficient, position)` computes \(m/\gcd(m,coefficient\,10^k)\). | `tests/test_detection_profiles.py` checks factorized gcd values for selected moduli and positions. | Implemented for decimal coefficients; no radix parameter. Factorization checks are a distinct calculation, though the test helper shares the same primes and model assumptions. |
| Decimal \(W(h)\) | `profiles.ordered_unequal_digit_pair_count`; a second closed-sum implementation is `experiments/validate_analytical_counts.py:pair_weight`. | Fixed expected values in `tests/test_detection_profiles.py` and `tests/test_analytical_counts.py`; direct event-enumeration tests exercise the integrated count. | Implemented twice. Standalone pair-count tests use selected hand expectations; no test exhaustively compares this function against all 100 ordered digit pairs. |
| Radix \(W_q(h)\) and radix spectra | No Python implementation in `python/` or `experiments/`. The formulas are in `research/r11_radix_generalization.md`; bounded calculations are described in R11/R12. | Mathematical proofs and tables in R11/R12; no radix-specific unit tests. | Math documented, but not a maintained executable API or experiment. |
| Substitution and transposition spectra | Decimal position profiles in `profiles.py` calculate reduced divisors, undetected pair counts, and rates for requested positions/lengths. Infinite spectra and general-radix spectra are not package functions. | `tests/test_detection_profiles.py`; formulas in formal model and R10–R12. | Finite decimal profiles implemented; broader spectrum objects are mathematical/documentary only. |
| Stabilization | Decimal `stabilization_position` and `stabilized_reduced_divisor` in `profiles.py`. | Factorized expected values over a selected modulus set in `tests/test_detection_profiles.py`; proofs in formal model/R11. | Implemented and tested for selected decimal moduli. Radix-general stabilization is not implemented. |
| Finite-length counts and rates | `substitution_length_profile` and `transposition_length_profile`; rates are `Fraction`. The analytical validator also uses `Fraction`. | Fixed exact expected counts/rates plus brute-force profile comparison for selected moduli and lengths. | Implemented. Direct enumeration gives a meaningful independent check over its selected finite cases. |
| Decimal sweep and CSV/Markdown outputs | `experiments/run_modulus_sweep.py` enumerates strings, calls the error generators, and compares integer residues. | README instructions; saved CSV/Markdown; analytical validator. | Reproducible after installation, with deterministic finite input space. Running it overwrites the CSV and aggregate Markdown. |
| Spectrum equivalence and identifiability | No production or experiment module implements this calculation. R10–R12 give definitions, formulas, examples, and bounded enumeration descriptions. | R10–R12 prose/pseudocode; no tests. | Not implemented. The general results are proofs in research notes; the bounded tables are not generated by a checked-in command. |

## 4. Test and validation audit

The test suite has meaningful coverage for checksum input validation, event generation, decimal profile counts, exact `Fraction` rates, finite-length edge cases, report parsers, and financial validation behavior. Relevant mathematical tests include:

- Hand-selected expected values for decimal pair counts \(W(h)\), reduced divisors, all-length thresholds, and exact rates.
- `test_analytical_profiles_cross_check_against_direct_event_enumeration`, which enumerates short fixed-width strings through the existing error generators and compares direct altered-string residues with profile counts for five selected moduli and lengths 1–3. This is a useful finite cross-check, not a proof for every parameter.
- `test_analytical_counts_match_all_existing_reports`, which calls the analytical validator against the saved reports and asserts 232 and 58 rows.
- Parser-negative tests for malformed/missing/duplicate CSV and aggregate rows, inconsistent counts/rates, and report rounding.

The full test suite was **not run** for this audit. It was not needed to inspect the implementation or validate the saved decimal data through the read-only validator functions. No lint, formatter, or static type-check command is configured in `pyproject.toml`.

The configuration and analysis tools are not uniformly tested against independent or adversarial input dimensions. In particular, the radix formulas, R10–R12 equivalence classes, and identifiability statements have no executable test suite because they have no corresponding checked-in implementation.

## 5. Independent-validation audit

| Validation path | Independence assessment | Classification |
|---|---|---|
| Historical sweep versus analytical validator | The sweep enumerates source strings and generated edits, then compares integer residues. The validator uses gcd-reduced divisors, a closed digit-pair sum, and free-position factors; it does not call the sweep's error generators. This is a genuinely different computational route, though both implement the same declared model. | **STRONG** for the saved finite decimal grid. |
| Profile formulas versus direct string enumeration tests | The expected profile is formula-based; the test separately enumerates source strings and calls the existing generators, then computes altered integer residues. The generator is shared with the historical sweep, so this does not independently test generator semantics from scratch. | **STRONG** for selected moduli/lengths; not exhaustive over the sweep grid. |
| Pair-count helper versus fixed expected values | Tests assert hand-selected decimal values, but do not independently enumerate every ordered pair for all divisors. | **MODERATE** as a spot check; integrated direct enumeration adds support. |
| Reduced-divisor tests | Tests derive expected gcds from a separate decimal prime-factor decomposition and compare against the generic gcd helper. Both paths use the same mathematical assumptions. | **MODERATE** for selected moduli and positions. |
| Stabilization and universal-detection tests | Selected values are checked against factorized expressions. The arbitrary-length modulus-11 unit test calls the analytical formula, so its length loop is not an independent proof. | **MODERATE** for implementation spot checks; **WEAK** as evidence for all-length claims. The proofs are the evidence for those claims. |
| R11/R12 bounded radix tables | The notes specify direct ordered digit-pair counts and gcd reduction, rather than using the closed \(W_q\) sum. During this audit I independently reran the R12 range in memory with a common per-radix stabilization endpoint; the class counts and zero-class sizes matched its table. No executable script or test is retained in the repository. | **STRONG** numerical cross-check in this audit; **MODERATE** reproducibility as a repository artifact. |
| Stored CSV against aggregate Markdown | Read-only calls to `validate_against_reports` confirmed 232 per-length rows and 58 aggregate rows reconcile. `analyze_per_length` independently confirmed the same row totals and that all 29 zero-event rows have blank rates. | **STRONG** for consistency of the saved artifacts with their analytical validators; not a replacement for the derivation or a fresh sweep. |

No test is itself a mathematical proof. The strongest support is the combination of written derivations, two different decimal computation paths, and exact reconciliation against the saved finite results.

## 6. Exhaustive-experiment audit

`experiments/run_modulus_sweep.py` uses `MODULI = range(2, 31)` and `LENGTHS = range(1, 5)`. For each length it enumerates all \(10^n\) fixed-width decimal strings with `itertools.product`, including leading zeros. For each source:

- A substitution event is one position and one different replacement digit. There are 9 choices per position; the generator yields each once.
- A transposition event is one adjacent position whose digits are unequal. Equal pairs are skipped; each eligible position yields one swap.
- Each event is counted against the residue of the original string. An event is detected exactly when `int(altered) % modulus` differs from the original residue. Integer conversion preserves numeric value; string generation and alteration preserve width.
- The total denominator is the number of generated events, not the number of strings. Substitution totals are \(9n10^n\). Transposition totals are \(90(n-1)10^{n-2}\) for \(n\ge2\); at length 1 the total is zero and rates are blank.
- Aggregate Markdown counts sum events over lengths first and divide summed detections by summed events. This is event-weighted, not an average of per-length rates.

The saved data has 232 per-length rows (29 moduli × four lengths × two error types) and 58 aggregate rows. Summed across lengths for one modulus, the event denominators are 388,890 substitutions and 28,890 transpositions. The experiment is deterministic and has no random seed or external dataset.

## 7. Radix-experiment audit

R11 states that it enumerated \(q\in\{2,3,4,5,6,7,8,9,10,11,12,16,20\}\), \(2\le m\le1000\), using direct ordered digit-pair counting for \(W_q\), gcd-reduced divisors, and stabilized position tuples. R12 extends the stated range to \(m\le5000\), includes substitution-only, transposition-only, and joint class counts, and supplies pseudocode. The mathematics covers all integer radices \(q\ge2\); the computations cover only the listed radices and finite modulus bounds.

The methodology is consistent with the decimal experiment's event convention: ordered unequal digit pairs, direct coefficient divisibility, and no equal swaps. However, these radix enumerations do not enumerate every length-\(n\) string or compare altered residues. They enumerate the analytical position spectra directly, so they verify the pair-count/trajectory calculations, not the source-string generator or finite-length rate formulas. The R11/R12 tables are not generated by a repository script and have no automated regression tests. The R12 pseudocode is sufficient to guide a reimplementation but is not an executable command.

## 8. Research-claim boundary

| Claim | Status | Safe wording | Wording not supported |
|---|---|---|---|
| The delta and gcd criteria are correct. | Proved under the formal model's definitions. | “The proof shows … for the defined fixed-width digit events.” | “A new checksum theorem” or “a universal error-detection theorem.” |
| Modulus 11 catches both defined decimal event types. | Proved for every finite length; the sweep agrees over lengths 1–4. | “Under these two error models, modulus 11 detects every event.” | “Modulus 11 catches every possible data alteration.” |
| Moduli 3 and 9 miss all defined unequal adjacent swaps. | Divisibility proof for all finite lengths; bounded rows agree. | “The swap delta is divisible by 9 in this model.” | “All algorithms using mod 3 or mod 9 miss swaps.” |
| The decimal sweep's values match formulas. | Verified against the saved 232/58 artifacts by independent analytical code paths. | “The stored results reconcile over moduli 2–30 and lengths 1–4.” | “The finite computation proves the theorem.” |
| Radix spectra and R12 identifiability results hold generally. | Proofs in R11/R12; not implemented as package functions. | “The note proves the stated result for integer radix \(q\ge2\).” | “The repository implements a general-radix analyzer.” |
| These results are novel or first. | **NOT SUPPORTED.** | “The reviewed literature does not settle exact overlap.” | “No prior work exists,” “first,” or publication-readiness claims. |
| Gumm or Damm lacks an equivalent result. | **UNRESOLVED**; full texts remain uninspected in the notes. | “The relationship remains unresolved from the accessible material reviewed.” | Any negative claim about their complete results. |

The literature record is explicitly bounded: Verhoeff is CLOSE prior context; Gumm is CLOSE but unresolved at full text; Damm is RELATED but unresolved; Schulz is RELATED; an exact match for R12's observable-equivalence criterion was not located in the reviewed materials. “Not located” is not evidence of absence. Classification vocabularies differ among documents (A–F in `literature_matrix.md`, claim-specific labels in R11/R12); future summaries should make the claim being classified explicit.

## 9. Authoritative mathematical model

`research/formal_model.md` is the cleanest existing authority for the decimal model and should remain so. `research/r11_radix_generalization.md` is the extension for integer radix \(q\ge2\). Their common core is:

For \(x=x_{n-1}\cdots x_0\in\{0,\ldots,q-1\}^n\), retaining fixed width and leading zeros,

$$
N_q(x)=\sum_{k=0}^{n-1}x_kq^k,\qquad C_{m,q}(x)=N_q(x)\bmod m,\quad m\ge2.
$$

Detection means the altered string has a different residue. With \(d=b-a\) for a substitution and \(a,b\) the higher/lower digits for a swap,

$$
\Delta_s=dq^k,\qquad \Delta_t=(a-b)(q-1)q^k
$$

up to the chosen sign convention; only divisibility matters. The reduced divisors and ordered-pair count are

$$
h_s=\frac{m}{\gcd(m,q^k)},\qquad
h_t=\frac{m}{\gcd(m,(q-1)q^k)},
$$

$$
W_q(h)=2\sum_{j=1}^{\lfloor(q-1)/h\rfloor}(q-hj),\qquad W_q(h)=0\text{ for }h>q-1.
$$

Equal adjacent digits are excluded, leading zeros are preserved, and rates are event-weighted counts rather than probabilities without an explicit event distribution. No mathematical definition needs changing. The decimal-only Python profile API should be labeled as such rather than presented as the radix implementation.

## 10. Documentation architecture

The existing notes contain substantial duplicate derivation and chronological research decisions. The smallest authoritative arrangement is:

1. Keep `formal_model.md` as the mathematical specification and proof authority for decimal strings.
2. Keep `literature_matrix.md` as the claim-by-claim literature boundary; use `deep_prior_art_comparison.md` as its detailed source record, not a competing conclusion.
3. Keep `theorem_review.md` as an independent mathematical/code review record, not a second formal specification.
4. Treat R9–R12 as chronological decision and exploratory records. R12 supersedes the earlier open question about whether to pursue the identifiability line; label or link them as historical notes rather than leaving them to look like concurrent plans.
5. Keep `detection_profile_engine.md` as the decimal API implementation note. It must not imply that radix spectra or identifiability are implemented.
6. Use the R13 audit itself to identify the one methodological document gap. Do not create separate `mathematical_specification.md`, `validation_protocol.md`, and `literature_boundary.md` documents that would duplicate the existing authorities.

`README.md` currently links the Phase 4 educational documents but not the research record. A small research section linking the formal model, literature boundary, and final audit would make the project easier to navigate without duplicating their contents.

## 11. Repository quality audit

- **Packaging:** `pyproject.toml` uses setuptools, source under `python/`, package discovery from that directory, Python `>=3.12`, no runtime dependencies, and pytest as an optional development dependency. Version metadata is `0.1.0`. There is no console-script mapping in this checkout. No CLI module is present.
- **Tests and tools:** pytest is the only configured quality tool. No lint, formatting, type-check, or CI configuration was found in the inspected project inventory.
- **Outputs:** the six expected CSV/Markdown/SVG research artifacts are present. The README accurately identifies sweep, plot, per-length, and analytical-validation commands. The sweep overwrites its CSV and aggregate Markdown; the plot command writes the two SVG targets; the per-length and analytical scripts write their output Markdown paths.
- **Documentation mismatch:** README lines 62 and 70 say the analysis/validator do not overwrite or modify existing reports, while `analyze_per_length.py:291` and `validate_analytical_counts.py:368` call `write_text` on their report output paths. The source CSV and aggregate inputs are read-only, but an existing generated output at the target path is overwritten. Clarify that distinction before describing these commands as non-overwriting.
- **Research navigation/status:** the R9–R12 notes are present but not linked from README. `formal_model.md` still lists arbitrary-base derivation as an open theoretical question, although R11 supplies that derivation. `research_direction.md` retains earlier open research questions and an R6-era status note; R12's B decision should be made visibly later/authoritative.
- **License:** no root `LICENSE`, `COPYING`, or `NOTICE` file exists in this checkout. This is a distribution/attribution decision, not a mathematical defect; select and add a license if redistribution is intended.
- **Financial workbench boundary:** code is in a separate package, but local worktree files are untracked and absent from the public README. No reporting/CLI is present. Keep its status separate from claims about the published mathematical package.
- **Financial workbench issues found by inspection:** `NumericConstraint` accepts equal minimum/maximum bounds when either endpoint is exclusive (`schema.py:49` checks only `minimum > maximum`), which defines an empty allowed interval. A direct construction check confirmed both forms are accepted. Reject equal bounds if either endpoint is exclusive. `ValidationSummary` is a frozen dataclass but exposes mutable `dict` fields (`results.py:31–35`). The timestamp parser helper is duplicated in the main timestamp loop (`validation.py:26–33, 134`). Existing financial tests do not cover duplicate CSV headers, BOM handling, malformed quoting, or blank physical rows. These are outside the math core and no change was made.
- **Files/state:** research records, the profile engine, and financial code/tests listed as untracked are not part of `HEAD`. The only pre-existing tracked modification observed was `python/modular_error_detection/__init__.py`. No obvious secret-like strings were found by a targeted repository text scan. All relative Markdown links checked in the project resolved; external URLs were not live-checked.

## 12. Reproducibility audit

A researcher with Python 3.12+ can install the editable package and pytest using the README command `python -m pip install -e ".[dev]"`, then run `python -m pytest`. The documented root-level commands are:

- `python experiments/run_modulus_sweep.py` — deterministically enumerates the decimal sample space and overwrites the sweep CSV/Markdown.
- `python experiments/render_modulus_plots.py` — reads the existing CSV and writes the two SVG files; it does not rerun the sweep.
- `python experiments/analyze_per_length.py` — validates/reconciles the existing CSV and aggregate report, then writes the per-length Markdown target.
- `python experiments/validate_analytical_counts.py` — validates the saved CSV and aggregate table against analytical formulas, then writes the characterization Markdown target.

The CSV and reports make inputs and finite outputs inspectable; no random process, external dataset, or network access is involved. The CSV validator plus aggregate reconciler is executable and was called read-only during this audit: 232 rows and 58 aggregate rows passed. The per-length loader/reconciler also passed on the saved artifacts, including 29 length-one zero-event rows with blank rates.

Reproducibility gaps are specific: the R11/R12 radix enumeration has no checked-in runnable script/test; README target-overwrite behavior is ambiguous; R12's pseudocode describes the computation but no command reproduces its table. The decimal methodology and expected outputs are otherwise stated clearly. External literature access limitations are recorded, but external citation URLs were not tested for current availability in this audit.

## 13. Source/test changes actually required

No mathematical defect was found in the decimal checksum, generators, profile formulas, event denominators, exact rates, or stored decimal reports. No change to those mathematical definitions or existing experiment outputs is required.

The following are justified follow-up changes, not changes made in this audit:

1. **Financial package correctness:** reject equal numeric bounds when either bound is exclusive. Add tests for both endpoints. This affects only the untracked financial package and should be handled under that package's scope.
2. **Radix reproducibility:** add one small deterministic research enumerator that reproduces the R11/R12 tables and tests the closed \(W_q\) expression against direct ordered-pair enumeration. This is a reproducibility improvement, not a new theorem.
3. **Documentation:** accurately disclose output-file overwrites; identify R9–R12 as chronological records with R12's conclusion controlling; update the stale arbitrary-base open question; link the research record from README.
4. **Financial quality backlog:** make summary mappings read-only if deep immutability is intended, reuse the timestamp helper, and add the missing loader regression cases. These are not blockers for the mathematical model, but the empty-interval issue is a confirmed configuration defect.

No source or test file was edited, and no tests were weakened or changed.

## 14. Recommended consolidation plan

Do not create all five proposed documentation files. Preserve existing authority and consolidate only the missing method record:

- `formal_model.md`: authoritative decimal specification and proofs.
- `literature_matrix.md` plus `deep_prior_art_comparison.md`: bounded literature status and detailed source notes.
- `theorem_review.md`: independent review record.
- `detection_profile_engine.md`: decimal implementation/API note.
- R9–R12: dated research decisions and exploratory work, with links making the current conclusion clear.
- One future `computational_methodology.md`: decimal commands and output paths, independent validation levels, and exact R11/R12 enumeration procedure/script. This avoids duplicating formulas and bibliographies.

The README should become the navigation point. A separate mathematical specification, validation protocol, literature boundary, and research conclusion are not necessary unless a future manuscript requires them.

## 15. Final research positioning

The proposed narrative is accurate with one qualification:

> A reproducible computational-mathematics investigation of modular residue error detection, with exact derivations, an exhaustive decimal experiment, a radix-general mathematical extension, and analysis of observable-spectrum equivalence and identifiability limits.

“Reproducible” is fully supported for the decimal sweep and its analytical reconciliation. For the R11/R12 radix tables, say “bounded exploratory enumeration described in the research notes” until a runnable artifact is checked in. The project should not be described as discovering a new modular error-detection theory. No publication-level novelty claim is supported.

## 16. Risks and unresolved issues

- The exact relationship of the project formulas and R12 equivalence criterion to prior work is unresolved; Gumm and Damm full texts remain uninspected.
- R11/R12 computation is not reproducible from a checked-in command, and no automated tests cover the generalized-radix results.
- The existing documentation has old exploratory questions that can be mistaken for active plans, plus ambiguous claims about generated-report overwrites.
- The current working tree does not match `HEAD`: local research, profile, and financial artifacts are untracked, and the package initializer is modified. A published-state audit must distinguish those artifacts from committed capabilities.
- No root license is present; distribution terms are unspecified.
- The separate, untracked financial package contains the empty-bound configuration defect described above. It should not be presented as finished until corrected and tested.
- No full test suite, build, or external-link availability check was run in this audit.

## 17. Exact next implementation step

After review of this audit, the smallest technical follow-up is a dependency-free `experiments/enumerate_radix_spectra.py` plus focused `tests/test_radix_spectra.py` that reproduce the R11/R12 tables with a common stabilization endpoint and compare direct digit-pair counts with the closed \(W_q\) formula. Keep the model fixed; add no theorem or new radix range. In that same approved documentation pass, clarify that analysis scripts overwrite their output targets and add README links to the authoritative research notes. Handle the financial empty-interval defect separately under the workbench scope.
