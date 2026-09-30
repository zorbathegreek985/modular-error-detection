# Phase 4 Research Plan

## Research objectives

Phases 1–3 established a reproducible finite sweep, a per-length view, and exact event-count formulas for fixed-width decimal strings. Phase 4 adds context around those results: the algebra behind residue checks, how check-character systems relate to error-detecting codes, and how selected decimal schemes differ from the project's deliberately simple residue test.

The goal is to document known foundations and define useful follow-up questions. This phase does not claim novelty, propose an algorithm ranking, or change the existing experiment. The current experiment remains limited to moduli 2–30, lengths 1–4, single-digit substitutions, and unequal adjacent transpositions.

## Research questions

- Why do modular checksums detect some alterations and miss others?
- How do the modulus and positional weights determine the residue change caused by an error?
- What does the modulus 11 proof establish for this project's two error models, and what remains outside its scope?
- How does a plain integer residue check differ from practical decimal check-character algorithms such as Luhn, Verhoeff, and Damm?
- How do error-detecting checks differ from codes that can locate or correct errors?
- Which limitations follow from the model and which are consequences of the finite computational range?

## Planned documents

| Document | Purpose |
|---|---|
| [Mathematical foundations](mathematical_foundations.md) | Define residue checks and connect them to the substitution and transposition formulas used in Phase 3. |
| [Checksum algorithms comparison](checksum_algorithms_comparison.md) | Describe Luhn, modulus 11 systems, Verhoeff, and Damm without ranking them. |
| [Error detection and error correction](error_detection_vs_error_correction.md) | Contrast checksums, parity, and CRC with Hamming and Reed–Solomon coding. |
| [Checksum history](checksum_history.md) | Provide a cautious, sourced timeline of selected developments. |
| [Limitations and future work](limitations_and_future_work.md) | State the current scope and identify exploratory extensions. |

## Evidence and writing conventions

The project’s equations and computed counts are internal results. Claims that follow algebraically from the stated error definitions are identified as proofs; sweep observations are explicitly restricted to the saved finite range. Descriptions of established schemes and dates are attributed to published papers, standards, RFCs, or patent records where available. Historical summaries are selective and do not imply that a listed milestone was the first of its kind unless the cited source supports that claim.

Future directions are proposals, not results. Any later empirical comparison should specify input formats, check-symbol conventions, error models, and event weighting before comparing rates.
