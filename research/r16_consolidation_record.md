# R16 — Research Artifact Consolidation Record

## 1. Starting State

Repository: `E:\modular-error-detection`; branch `main`; `HEAD` `e971497488dfea70699330dc7bd14643c9a996fa`; upstream `origin/main`. No staged changes were present. The worktree already contained an R14 `README.md` modification, a pre-existing modification to `python/modular_error_detection/__init__.py`, and untracked financial-workbench modules, `profiles.py`, research documents through R15, and related tests. These pre-existing paths were preserved.

Before R16 the relevant dirty paths included the R14 additions `python/modular_error_detection/radix_spectra.py` and `tests/test_radix_spectra.py`; `README.md` was already modified by R14. All other pre-existing dirty paths are listed in the R15 baseline. R16 changes to already-dirty Markdown documents are specifically itemized here; their untracked/modified status does not mean they were created in R16.

The exact initial `git status --short --branch --untracked-files=all` output was:

```text
## main...origin/main
 M README.md
 M python/modular_error_detection/__init__.py
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
?? research/r9_research_decision.md
?? research/research_direction.md
?? research/theorem_review.md
?? tests/test_detection_profiles.py
?? tests/test_financial_validation.py
?? tests/test_radix_spectra.py
```

## 2. Stale-Question Resolution

In `research/formal_model.md`, the open-question list asked how the divisibility and universal-detection conditions generalize from decimal to arbitrary radix. R11 already derives and proves those results under the established fixed-width radix digit model. The bullet now labels that question as resolved within that model and links to R11. The surrounding note now distinguishes this resolved question from matters outside the decimal document's results. No formula, theorem, or model assumption changed, and no novelty claim was added.

## 3. Historical-Document Labeling

Added concise status notes to `research/research_direction.md`, `research/r9_research_decision.md`, `research/novelty_boundary.md`, and `research/novelty_boundary_r8.md`, identifying their stage-specific status and pointing readers to R12 as the later research decision. Added snapshot notes to R13 and R15 explaining that their proposed follow-ups are historical and have since been implemented or recorded in R16. The detailed prior-art source record and mathematical result notes were not mechanically relabeled.

## 4. R12 Reproduction Mechanism

Added `experiments/reproduce_r12_radix_spectra.py`, following the existing `experiments/` convention; there was no existing `scripts/` directory. The script calls `radix_stabilization_position` and `enumerate_radix_spectrum_classes` from the existing `modular_error_detection.radix_spectra` module. It performs separate substitution-only, transposition-only, and joint grouping for each configured radix, using moduli 2–5000 and that domain's common inclusive maximum stabilization endpoint.

The script writes deterministic CSV to standard output and creates no files itself. The computed columns are radix, modulus bounds, inclusive endpoint, moduli examined, substitution class count, transposition class count, joint class count, and zero-joint-class size. It does not hardcode expected result counts.

Added `tests/test_r12_reproduction.py`, a fast small-domain test of the reproduction summary function. It does not run the full 13-radix experiment during ordinary pytest.

## 5. Reproducibility Command

Documented command, from the repository root after the README's editable installation step:

```powershell
python experiments/reproduce_r12_radix_spectra.py
```

The command's CSV can be redirected by the caller; the script does not select an output path. The full run for this record used the existing project virtual environment:

```powershell
& ".\.venv\Scripts\python.exe" experiments/reproduce_r12_radix_spectra.py
```

The command exited 0 and printed one header plus 13 result rows. A preliminary attempt to run the README command with the uninstalled system `python` failed with `ModuleNotFoundError`; the system interpreter had no editable project installation. The documented workflow requires installing the project first, and the existing virtual-environment interpreter successfully executed the same script. No packages were installed during R16.

## 6. Validation Against R12

The captured CSV output was compared programmatically with the 13 numeric rows in the existing R12 Markdown table. Every row matched in all four reported counts; each output used 4,999 moduli and the computed common inclusive endpoint shown here:

| Radix | Endpoint | Substitution classes | Transposition classes | Joint classes | Zero-joint moduli |
|---:|---:|---:|---:|---:|---:|
| 2 | 12 | 13 | 13 | 13 | 4,987 |
| 3 | 7 | 16 | 16 | 23 | 4,977 |
| 4 | 6 | 19 | 20 | 30 | 4,966 |
| 5 | 5 | 21 | 21 | 35 | 4,961 |
| 6 | 12 | 38 | 37 | 58 | 4,877 |
| 7 | 4 | 26 | 25 | 45 | 4,943 |
| 8 | 4 | 29 | 29 | 48 | 4,933 |
| 9 | 4 | 32 | 29 | 57 | 4,910 |
| 10 | 12 | 62 | 55 | 103 | 4,811 |
| 11 | 3 | 33 | 32 | 59 | 4,923 |
| 12 | 7 | 56 | 55 | 88 | 4,784 |
| 16 | 3 | 47 | 44 | 90 | 4,816 |
| 20 | 6 | 84 | 83 | 129 | 4,725 |

**All 13 documented R12 rows matched.** The first comparison attempt used an overly strict table-header match and stopped before comparing data; correcting the comparison boundary yielded the row-by-row result above. No expected R12 values were changed. This validates the bounded computation, not any result outside its finite domain.

## 7. Documentation Updates

`README.md` now documents the exact command, radix list, modulus interval, reported statistics, deterministic output, existing radix API usage, and the distinction between theorem-derived formulas and bounded class-count observations. `research/r12_identifiability.md` now points to the command, parameters, endpoint convention, and expected relationship to its table. Neither document claims the finite table proves a general theorem.

R16 modified these pre-existing files: `README.md`, `research/formal_model.md`, `research/research_direction.md`, `research/r9_research_decision.md`, `research/novelty_boundary.md`, `research/novelty_boundary_r8.md`, `research/r12_identifiability.md`, `research/r13_research_artifact_audit.md`, and `research/r15_working_tree_audit.md`. README was already dirty from R14; the research documents were already present as untracked work. R16 created `experiments/reproduce_r12_radix_spectra.py`, `tests/test_r12_reproduction.py`, and this record, `research/r16_consolidation_record.md`.

Focused command `& ".\.venv\Scripts\python.exe" -m pytest -p no:cacheprovider --basetemp ".r16-pytest-tmp" tests/test_radix_spectra.py tests/test_r12_reproduction.py` passed **11 tests**. Full command `& ".\.venv\Scripts\python.exe" -m pytest -p no:cacheprovider --basetemp ".r16-pytest-tmp"` passed **216 tests**. The temporary directory was removed and verified absent. `git diff --check` exited 0; Git printed LF-to-CRLF warnings for `README.md` and the pre-existing modified package initializer. All changed Markdown/Python files decoded as UTF-8, had no replacement characters or trailing whitespace, and relative Markdown links resolved. No existing sweep/report/plot was regenerated.

## 8. Mathematical Scope Preservation

No implementation formula or mathematical conclusion was changed. The R16 additions use the existing radix API and leave unchanged (W_q), both spectra, reduced-divisor formulas, stabilization, identifiability, and the observable-spectrum equivalence definition. No checksum/error model, financial-workbench behavior, historical report, or plot was modified or regenerated.

## 9. Final Artifact Structure

The existing source-of-truth structure remains: `formal_model.md` specifies the decimal model; R11 contains the radix-general derivation; R12 contains the identifiability proofs and bounded observations; `radix_spectra.py` implements the bounded analytical API; and the new experiment command reproduces R12's table. R7–R9 planning and prior-art notes remain as historical records, with added status labels where current interpretation could otherwise be ambiguous. The README is the usage/navigation entry point. No duplicate theorem document or generated results file was added.

## 10. Remaining Limitations

- R12's table remains a bounded computation over the 13 named radices and moduli 2–5000; it does not prove results outside that domain.
- The direct-pair unit validation is intentionally limited to small radices/moduli. The full-table reproduction exercises the analytical implementation against saved results, not an independent full source-string enumeration.
- The README example/command requires the project to be installed as documented; an uninstalled interpreter cannot import the package.
- Gumm (1985) and Damm (2000) full-text relationships remain unresolved in the existing literature record. No novelty claim is made.
- The worktree retains unrelated pre-existing untracked and modified files. Nothing was staged, committed, or pushed.

## 11. Exact Next Step

Review this consolidation diff and preserve it as an unstaged working-tree change until the owner decides how to handle the repository's pre-existing dirty work. No additional mathematical expansion or novelty search is indicated.
