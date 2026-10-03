# R18 — Final Research Artifact Consolidation Record

## 1. Starting State

R18 began in `E:\modular-error-detection` on branch `main`, at `e971497488dfea70699330dc7bd14643c9a996fa`, tracking `origin/main`. The worktree was intentionally dirty and had no staged changes. It contained the pre-existing modified README and package initializer, the R14–R17 untracked research and implementation work, and the separate financial workbench files. No pre-existing paths were cleaned, reverted, staged, or committed.

The full initial status was recorded directly before editing. It matched the preceding R17 status, with no R18 files present. Git commands used the one-command safe-directory override because of repository ownership; no Git configuration changed.

## 2. Historical R10 Update

Added a short status note below the title in `research/r10_count_spectrum_theorem.md`. It identifies the final proposed next step as the R10 state of the investigation and points to the subsequent R11/R12 work and R12's later decision. No mathematical result or original section was rewritten.

## 3. Research Summary Created

Created `research/research_summary.md` as the central researcher-facing overview. It follows the requested 18-section structure and summarizes the fixed-width model, two error classes, divisibility conditions, finite-alphabet counts, position spectra, radix analysis, identifiability, implementation, validation, experiments, limitations, and research position.

The R12 table is reproduced using the values already documented in R12 and the R16 validation record. It is explicitly described as a bounded computational observation. The summary does not claim novelty or extend the mathematical scope.

## 4. Repository Navigation

Added one bullet to the existing README research-notes list linking to `research/research_summary.md`. No other README section was changed. The summary maps the proof documents, historical research notes, prior-art records, audits, package modules, tests, and R12 reproduction script. It identifies R9–R17 as development/audit history and itself as the researcher-facing entry point.

## 5. Mathematical Scope Preserved

The documents retain the established model: fixed-width radix-$q$ digit strings with leading-zero positions, $m\ge2$, and a residue of the represented integer. Only single substitutions and unequal adjacent transpositions are described. The existing $W_q$, reduced-divisor spectra, stabilization, finite-length counts, equivalence, and identifiability claims are summarized from the existing records; no new theorem or error model was added.

## 6. Research-Claim Boundary

The summary calls the work a reproducible computational-mathematics investigation and expressly states that the repository does not establish a novelty claim. It distinguishes mathematical derivations from bounded computational observations and does not assert that the formulas are absent from literature.

## 7. Reproducibility Position

The summary documents the editable-install command from `pyproject.toml`, the established workspace-virtual-environment pytest command, and the R12 reproduction command. It explains that the reproduction uses the existing radix API, calculates the finite configured experiment, writes CSV to standard output, and needs no network or stored result files. It attributes the 13-row match to the existing R16 record; R18 did not rerun the experiment.

## 8. Literature Boundary

The summary names the reviewed literature areas and sources, preserves the documented access limitations, and states that exact Gumm/Damm relationships remain unresolved where full primary texts were not verified. R18 conducted no literature search and made no new source claims.

## 9. Remaining Limitations

The work remains limited to fixed-width data and its two error models; the finite-alphabet count loses information above its threshold; computational experiments are bounded; independent direct-pair validation covers small ranges; some prior-art comparisons remain unresolved; and no novelty claim is established. The financial workbench is explicitly kept separate from the mathematical contribution.

## 10. Final Research Position

The researcher-facing architecture is now: README navigation to `research_summary.md`; the summary's concise account and links; detailed model/proof, implementation, experiment, literature, and historical records behind it. R10 is clearly historical, and R11/R12 provide the later radix and identifiability development. Earlier records remain intact as chronology.

## 11. Exact Next Step

Review the two new research documents and the limited README/R10 changes, then decide which of the intentionally dirty working-tree files belong in a future consolidation. No further mathematics, experiment, literature search, or implementation change is indicated by R18.

R18 changed `README.md` and `research/r10_count_spectrum_theorem.md`, and created `research/research_summary.md` and this record. It changed no source code or tests. Tests and the R12 reproduction were not rerun. Validation was limited to documentation encoding, structure, links, whitespace, math delimiters, and Git diff checks. No files were staged, committed, or pushed.
