# R17 — Final Consistency and Working-Tree Audit

## 1. Baseline

The audit began in `E:\modular-error-detection` on branch `main`, at `e971497488dfea70699330dc7bd14643c9a996fa`, tracking `origin/main`. The branch had no reported ahead/behind divergence. No staged changes were present.

Git required a per-command `safe.directory` override because the repository owner differs from the sandbox user. The command used was `git -c safe.directory=E:/modular-error-detection ...`; no Git configuration was changed.

The initial status was already dirty:

```text
## main...origin/main
 M README.md
 M python/modular_error_detection/__init__.py
?? experiments/reproduce_r12_radix_spectra.py
?? python/financial_data_workbench/__init__.py
?? python/financial_data_workbench/loader.py
?? python/financial_data_workbench/results.py
?? python/financial_data_workbench/schema.py
?? python/financial_data_workbench/validation.py
?? python/modular_error_detection/profiles.py
?? python/modular_error_detection/radix_spectra.py
?? research/deep_prior_art_comparison.md
?? research/detection_profile_engine.md
?? research/formal_model.md
?? research/literature_matrix.md
?? research/novelty_boundary.md
?? research/novelty_boundary_r8.md
?? research/prior_art_claim_matrix.md
?? research/r10_count_spectrum_theorem.md
?? research/r11_radix_generalization.md
?? research/r12_identifiability.md
?? research/r13_research_artifact_audit.md
?? research/r15_working_tree_audit.md
?? research/r16_consolidation_record.md
?? research/r9_research_decision.md
?? research/research_direction.md
?? research/theorem_review.md
?? tests/test_detection_profiles.py
?? tests/test_financial_validation.py
?? tests/test_radix_spectra.py
?? tests/test_r12_reproduction.py
```

R16's own record distinguishes its edits from work already present: it reports modifying `README.md` and eight pre-existing research Markdown files, and creating the R12 reproduction script, its focused test, and the R16 record. R16 did not claim ownership of the pre-existing initializer change or financial-workbench files. R17 adds only this audit document. These distinctions rely on the recorded prior status; the repository has no clean committed baseline for the untracked research work.

## 2. R16 Implementation Review

The R16 script, `experiments/reproduce_r12_radix_spectra.py`, uses the existing `modular_error_detection.radix_spectra` API: `radix_stabilization_position` and `enumerate_radix_spectrum_classes`. It uses the documented ordered radix tuple `(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20)` and modulus interval 2 through 5000 inclusive. It calculates substitution-only, transposition-only, and joint classes, plus the size of the all-zero joint class. Expected result counts are not embedded in the script.

For each radix, the script computes the maximum stabilization position over the bounded modulus interval and passes that shared inclusive endpoint to the existing enumerator. This matches the API documentation, which says a common endpoint at least as large as the maximum stabilization position suffices to compare complete spectra in that finite domain. The API derives the endpoint from the established valuation bound. Output is CSV on standard output, in fixed radix and field order; the script makes no file writes, network requests, or random choices.

The focused test exercises a small domain and checks its exact summary values and invocation-independent calculation path. It does not run the full 13-radix experiment as part of routine pytest. This is appropriate for test runtime, while leaving full-table reproduction as an explicit command.

## 3. Reproducibility Claim Audit

The README gives the command `python experiments/reproduce_r12_radix_spectra.py`, following the editable-install instructions. The script imports the installed package and therefore requires an environment in which the project package is importable; R16's record documents that the command succeeded under the project virtual environment and that an uninstalled system interpreter failed to import the package. The command and prerequisite are consistent when followed in the documented order.

The script is deterministic by inspection: fixed constants, integer arithmetic through the existing API, deterministic ranges/grouping, and CSV output with stable ordering and line endings. It reports the modulus bounds, inclusive endpoint, number examined, each class count, and zero-joint class size. The README and R12 note describe the output as a bounded computation, not proof outside the stated domain.

R16's consolidation record reports that the complete command was run and every field in all 13 R12 rows matched. R17 inspected that record, the script, the API, and the R12 table, but did not rerun the full experiment or independently recalculate its output. Therefore the full match is verified here as a recorded R16 result, not as a new R17 execution.

## 4. R12 and R16 Cross-Consistency

The R12 table has 13 rows for exactly the radices configured in the script. Its stated modulus domain is 2–5000. The R16 record's table reproduces the documented class counts and zero-joint-class sizes, and records the corresponding inclusive endpoints: 12, 7, 6, 5, 12, 4, 4, 4, 12, 3, 7, 3, and 6 in radix order. The R12 reproduction note gives the command, radix set, modulus range, common inclusive endpoint convention, and bounded-computation qualification.

The script's columns correspond to the R12 table's reported statistics: substitution spectrum classes, transposition spectrum classes, joint spectrum classes, and moduli in the zero joint class. It additionally prints the domain and endpoint needed to make the computation auditable. No discrepancy was found in the inspected values or labels. Full numeric equality is supported by the R16-recorded comparison; it was not recomputed during R17.

## 5. Mathematical Model Consistency

The reviewed R11 and R12 documents and `radix_spectra.py` use the fixed-width radix model: digits are in `0..q-1`, leading-zero positions are retained, and the checksum is the represented integer modulo `m`. The implementation's `radix_pair_weight` counts ordered unequal digit pairs whose difference is divisible by the reduced divisor. Substitution and transposition spectra use the corresponding gcd-reduced divisors with coefficients 1 and `q-1`.

The stabilization function returns the maximum prime-valuation cancellation position over primes dividing the radix, with zero when no such cancellation is needed. The enumerator includes positions `0..max_position`, and its docstring requires a common endpoint at least as large as the maximum stabilization position for complete spectra. The reproduction script follows that convention. The audited R16 work changes neither formulas nor the model's assumptions.

R11/R12 distinguish their general derivations from finite tables. The R12 modulus/radix table is evidence only for its stated finite grid. The theorem and identifiability claims have their own mathematical derivations and stated fixed-width finite-alphabet assumptions; they are not consequences merely of the table.

## 6. Research-Claim Consistency

The README describes a reproducible computational-mathematics investigation and explicitly makes no novelty or publication-priority claim. R11 and R12 likewise bound the mathematical model and computational domains. The literature matrix and prior-art claim matrix distinguish inspected sources from inaccessible primary texts and state that “not located” is not evidence of absence. The records identify Verhoeff as close prior work and leave exact Gumm and Damm relationships unresolved where full-text review was unavailable.

No unsupported novelty, priority, or universal-field claim was found in the reviewed README, R11, R12, or R16 record. R16's addition is a reproduction route for an existing bounded table, not a new mathematical result. This audit did not perform a new literature search or independently verify external references.

## 7. Historical Document Audit

R16 added historical-status notes where earlier recommendations could be mistaken for current decisions: `research_direction.md`, `r9_research_decision.md`, `novelty_boundary.md`, and `novelty_boundary_r8.md`. R13 and R15 identify themselves as historical audit snapshots and point to later work. The R16 record explains that it did not mechanically label every derivation or prior-art evidence document.

One small residual gap remains in `research/r10_count_spectrum_theorem.md`: its final section, “Exact recommended next step,” proposes a further classification direction, while R12 later says to close the inverse-problem line absent stronger evidence. R10 is a dated research record by sequence, but it lacks an opening status note that would make this supersession immediately clear. This does not affect the theorem or R12 conclusions. A short historical-status note linking to R12 would remove the ambiguity in a future documentation-only pass.

## 8. README Public-Facing Audit

The README links the formal model and R11–R13 research notes, explains the decimal sweep and its finite scope, and documents the R12 reproduction command, radices, modulus interval, statistics, deterministic output, and bounded-result limitation. It states that theorem-derived formulas and computational class counts have different evidential status. The editable installation instructions precede the command that imports the package, so the system-interpreter import issue recorded in R16 is an environment prerequisite rather than an incorrect command.

The research navigation list does not link R15 or R16, but the README's reproduction subsection and R12 link provide the user-facing instructions and the relevant research table. This is optional navigation polish, not a functional or research-claim defect. No mismatch between the inspected README command and actual script path or behavior was found.

## 9. Test Architecture Audit

The ordinary suite includes `tests/test_r12_reproduction.py`, which checks a small bounded summary, and `tests/test_radix_spectra.py`, which includes direct digit-pair checks for small radices/moduli. The small direct calculation is a separate route from the production gcd/reduced-divisor formula, although its domain is intentionally limited. The full R12 grid is not repeated in pytest; the dedicated command is the appropriate full-run mechanism.

The R16 record reports 11 focused tests and 216 tests in the full suite, both passing. R17 did not rerun tests, per the audit scope. These counts are reported as prior-phase evidence and were not independently confirmed in this audit. No lint, static type-check, or formatter configuration was found in the inspected `pyproject.toml`; pytest is the configured test runner, with Python source rooted under `python/`.

## 10. Reproducibility Readiness

| Dimension | Status | Evidence and limit |
|---|---|---|
| Mathematical specification | **READY** | R11/R12 state the model, formulas, stabilization, and assumptions; finite computational tables are separately labeled. |
| Reproduction implementation | **READY** | The script invokes the existing API, derives its endpoint, and emits stable CSV without hardcoded expected counts. |
| Full experiment reproduction | **READY, based on R16 record** | R16 records a completed run and all 13 rows matching R12. R17 did not rerun it. |
| Independent implementation validation | **PARTIALLY READY** | Direct digit-pair comparison covers small parameter values; the full 13-radix table is not independently enumerated from source strings. |
| Routine test coverage | **PARTIALLY READY** | Fast API/script tests are present; pytest intentionally does not repeat the large full-grid computation. |
| Literature review | **PARTIALLY READY** | Claim boundaries and access limits are documented; full-text Gumm and Damm relationships remain unresolved, and R17 did no new search. |
| Documentation status | **PARTIALLY READY** | R16 resolves the formal-model question and labels key planning notes; R10 retains a superseded next-step recommendation without an explicit status note. |
| Repository consolidation | **PARTIALLY READY** | R16 outputs remain in an intentionally dirty, unstaged working tree alongside earlier untracked work; this audit does not establish a clean, committed release snapshot. |

These labels describe separate readiness dimensions, not a single release score.

## 11. Financial Workbench Boundary

The README and mathematical research notes keep the checksum study as the main research narrative. R13 describes the financial workbench as a separate package and product concern. The Phase 7/8 CLI is not presented in the radix reproduction command or R12 mathematical model. R16's record states that financial-workbench behavior was not modified. This audit reviewed only that stated boundary and did not inspect or assess the financial implementation.

## 12. Final Research Artifact Structure

The current structure has a clear main path: `formal_model.md` specifies the decimal model; R11 develops the radix generalization; R12 presents identifiability analysis and bounded observations; `radix_spectra.py` implements the bounded spectrum API; the R12 experiment script reproduces the table; and the README provides entry points. Literature matrices and detailed prior-art notes preserve evidence and access limitations. R9–R16 records preserve the development history.

There is some intentional overlap among prior-art and historical research notes. The principal remaining navigation ambiguity found in this review is the unmarked R10 recommendation described above. The working tree also contains local/untracked modules and tests; status alone does not identify which untracked files are intended for a future commit.

## 13. Blocking Issues

No mathematical inconsistency, hardcoded reproduction result, incorrect endpoint convention, or unsupported novelty claim was identified in the inspected R16 artifacts. No blocking defect was found that invalidates the R12 table or its documented reproduction route.

The R10 historical-status gap is non-blocking and documentation-only. R17 did not execute the full reproduction, tests, or external-source checks; conclusions depending on those activities are explicitly attributed to the R16 record or prior research records.

## 14. Final Consolidation Readiness

The research artifacts are internally coherent for review as a bounded, reproducible study, with the status qualifications above. The R16 objective is substantially met: the stale arbitrary-radix question is resolved within the project's fixed-width model, the full-table reproduction path is recorded, and key older planning documents are labeled. The recorded full reproduction matched every R12 row.

The working tree is not a clean release or commit candidate: it contains pre-existing modifications and many untracked files, and R17 adds one more untracked audit document. No assessment here implies that all present untracked files have been reviewed for inclusion. Before consolidation into a commit, the owner should decide file ownership and scope. The one focused documentation follow-up is to mark R10 as historical and point to R12's later decision; no mathematical rework is indicated.

## 15. Minimum Next Phase

Make a narrow documentation-only update to the opening of `research/r10_count_spectrum_theorem.md`, identifying it as a historical theorem-discovery record and directing readers to R12 for the later status of the inverse-problem line. Then review the intended commit inventory against the dirty working-tree baseline. No new experiment, theorem, literature search, or financial-workbench change is indicated by this audit.

R17 itself added only this audit document. It did not run pytest or the full R12 reproduction, modify any existing report or source file, stage changes, or change Git configuration.
