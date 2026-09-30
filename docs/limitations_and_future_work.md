# Limitations and Future Work

## Current limitations

- **Decimal strings only.** The implementation treats symbols as decimal digits with positional base-10 weights. It does not model letters, bytes, or arbitrary alphabets.
- **Narrow error models.** The experiment counts one substitution at one position or one unequal adjacent transposition. It does not evaluate multiple simultaneous changes, insertions, deletions, non-adjacent swaps, or mixed errors.
- **No probability model.** Events are counted uniformly under the stated enumeration. Real transcription and transmission errors do not necessarily occur uniformly, so the rates are not real-world error probabilities.
- **No correction capability.** A changed residue signals a mismatch but does not identify the error or recover the original string.
- **Finite computational range.** Saved exhaustive results cover moduli 2–30 and lengths 1–4. The modulus 11 universal result for the two defined error types follows from a separate proof; other unproven numerical patterns should not be generalized beyond the tested range.
- **No security guarantee.** A small checksum is not designed to resist deliberate changes or collisions chosen by an adversary.
- **Algorithm mismatch in external comparisons.** Practical check-digit systems may append a check character, use position-dependent transforms, or accept a different alphabet. Their detection rates cannot be compared fairly until their input and event conventions are aligned.

## Possible future work

These ideas are exploratory. Each would need a concrete data source or model, a documented event definition, and reproducible validation before supporting conclusions.

- Extend the derivation and implementation to arbitrary finite alphabets and positional bases.
- Define weighted human-entry error models from suitable empirical sources, distinguishing observed frequency from an assumed model.
- Simulate OCR confusions with explicit character-confusion matrices and report sensitivity to those assumptions.
- Compare selected identifier schemes used in financial or administrative identifiers, while respecting their official specifications and not implying endorsement for deployment.
- Study distributed-systems integrity mechanisms such as checksums and CRCs for accidental corruption, and distinguish them from cryptographic hashes and MACs used where adversarial integrity matters.
- Build a checksum analysis or recommendation tool that takes an explicit alphabet, error model, threat model, and implementation constraints as input. Such a tool would need independent validation and should not make unqualified “best algorithm” recommendations.
- Expand beyond detection to error-correcting codes only as a separately scoped study with explicit redundancy, distance, and decoding assumptions.

## Research discipline for extensions

Keep proofs, finite enumeration results, literature claims, and proposed work in separate sections. Record exact algorithm variants, data sources, parameter ranges, event weighting, and generated-artifact provenance. Do not present a proposed application as validated until the relevant domain requirements and failure costs have been reviewed.
