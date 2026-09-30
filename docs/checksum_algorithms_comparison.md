# Checksum Algorithm Comparison

## Scope of comparison

The project computes the residue of a fixed-width decimal value and asks whether a specified alteration changes that residue. It does not append a check digit. The algorithms below generally append or verify a check character and may use position-dependent transformations. Their guarantees should not be inferred from the project's modulus sweep.

## Plain modulus checks and modulus 11 systems

**Basic principle.** A plain residue check accepts a value when its residue meets a chosen condition. For the current project, detection is simply a change in `N mod m`. Practical modulus 11 systems are not one single algorithm: they may use weighted sums, iterative recurrences, and a check character that can include a non-decimal symbol. ISO/IEC 7064 includes pure and hybrid systems and states detection guarantees for its specified systems.

**Targeted errors and strengths.** The project's unweighted decimal-value residue modulo 11 detects every single substitution and unequal adjacent transposition, as proved in [Mathematical Foundations](mathematical_foundations.md). This proof uses the exact `10^k` positional weights and nonzero digit differences modulo 11. ISO/IEC 7064 describes its family as detecting all single substitutions and all or nearly all local transpositions, among other errors.

**Limitations and relation to this project.** Those guarantees are scheme-specific. The project's theorem concerns two error types and a plain residue comparison; it does not establish all guarantees for every system called “mod 11,” nor does it validate a particular identifier standard. The project does not include a check symbol or weighted recurrence. [ISO/IEC 7064:2003](https://www.iso.org/standard/31531.html) is the normative reference for the systems it specifies.

## Luhn (often called a modulus 10 check)

**Basic principle.** Luhn applies alternating position-dependent transformations: one digit in each pair of positions is doubled, with the decimal digits of a two-digit product added, then contributions are summed modulo 10. A check digit is chosen so the complete number satisfies the check condition. The patent describes a device for calculating or verifying numbers with an appended check digit ([US 2,950,048](https://patents.google.com/patent/US2950048A/en)). “Modulus 10” alone can also describe other checks; it should not be treated as synonymous with every mod-10 algorithm.

**Targeted errors and strengths.** The standard decimal Luhn transform is `f(d) = 2d` for `d < 5` and `f(d) = 2d - 9` for `d >= 5`; the other alternating positions contribute the unchanged digit. Modulo 10, `f` maps the ten digits bijectively to `0,2,4,6,8,1,3,5,7,9`. Thus changing one digit changes its contribution at either kind of position, so a single-digit substitution in a checked string is detected.

For an adjacent pair, one position uses `f` and the other uses the identity. Swapping digits `a` and `b` changes the pair sum by `(f(b)-b) - (f(a)-a)` modulo 10. The values of `f(d)-d` for `d=0,...,9` are `0,1,2,3,4,6,7,8,9,0`. The only repeated value is for digits 0 and 9, so among unequal adjacent pairs the `09`/`90` swap is undetected; all other unequal adjacent swaps change the Luhn sum. This derivation applies to the standard decimal Luhn check-digit calculation, where the checked sequence includes its check digit.

**Limitations and relation to this project.** The `09`/`90` collision shows that Luhn does not detect every adjacent transposition. The guarantees above concern single-digit substitutions and unequal adjacent transpositions in the standard decimal Luhn scheme; they do not extend to arbitrary multi-digit changes or every possible error pattern. Unlike this project's plain `N mod 10` sweep, Luhn is a check-digit algorithm with alternating nonlinear digit transforms. A direct rate comparison would need to define whether the check digit itself is in the editable string and how error events are counted.

## Verhoeff

**Basic principle.** Verhoeff's decimal check-digit method uses operations from the dihedral group of order 10 together with position-dependent permutations. The check digit is chosen so a fold over the digits, including the check digit, yields the valid state. J. Verhoeff's primary source is [*Error Detecting Decimal Codes*](https://ir.cwi.nl/pub/13045), Mathematical Centre Tract 29, 1969. An accessible technical description by Edith Law gives the D5 check equation and the position-dependent conditions used for single-error and adjacent-transposition detection ([Group Theory lecture notes, 2007](https://www.cs.cmu.edu/~elaw/files/grouptheory.pdf)).

**Targeted errors and strengths.** In Law's stated code equation, each position applies a permutation before group combination. A single changed digit therefore changes its position's group element; the notes state an additional inequality for adjacent unequal digits that ensures their transposition changes the check result. Under that equation and error model, the described scheme detects all single-digit substitutions and unequal adjacent transpositions. This is a claim about the documented Verhoeff construction, not every system using a dihedral group.

**Limitations and relation to this project.** It is a check-digit scheme, not a single integer residue modulo `m`; it should be analyzed with its own definitions and validation algorithm. The cited technical description supports the stated single-error and transposition conditions; it does not establish detection of every multi-error, insertion, deletion, or non-adjacent permutation. The CWI record confirms the Verhoeff monograph's bibliographic details, but its linked full text was not accessible during this review; the technical guarantee here is attributed to Law's accessible notes. This project does not implement or test Verhoeff.

## Damm

**Basic principle.** Damm's 2000 paper studies check-digit systems over groups and anti-symmetric mappings: [“Check digit systems over groups and anti-symmetric mappings”](https://doi.org/10.1007/s000130050524), *Archiv der Mathematik*. Its general results concern group-based systems. The decimal quasigroup construction is associated with Damm's 2004 dissertation, [*Total anti-symmetrische Quasigruppen*](https://archiv.ub.uni-marburg.de/diss/z2004/0516/pdf/dhmd.pdf). The university repository record identifies the dissertation, but its full text was inaccessible during this review.

**Targeted errors and strengths.** The 2000 paper's abstract states a general condition for group-based check-digit systems to detect single errors and adjacent transpositions. That result does not alone establish the properties of a particular decimal quasigroup table. The specific order-10 construction and the commonly stated guarantees of detecting every single-digit substitution and unequal adjacent transposition remain unverified here because the dissertation text could not be accessed. They are not asserted in this comparison as independently established facts.

**Limitations and relation to this project.** A guarantee for a specific quasigroup method depends on its operation table and check-digit convention; it cannot be inferred merely from the term “quasigroup.” This project neither implements a Damm table nor compares empirical event rates against the method. The specific decimal table and its error-detection guarantees require verification against an accessible copy of the dissertation or another direct technical source.

## Comparison notes

The systems use different check values, positional rules, and intended input contexts. A meaningful empirical comparison would first choose exact variants, state whether the appended check character is part of the error domain, keep leading-zero and equal-digit conventions explicit, and calculate rates from a common event model. No algorithm is ranked here.

## References

- Hans P. Luhn, [US Patent 2,950,048, *Computer for Verifying Numbers*](https://patents.google.com/patent/US2950048A/en), application filed 1954, patent granted 1960.
- J. Verhoeff, [*Error Detecting Decimal Codes*](https://ir.cwi.nl/pub/13045), 1969.
- Edith Law, [*Group Theory* lecture notes](https://www.cs.cmu.edu/~elaw/files/grouptheory.pdf), 2007, section “Verheoff Algorithm” (technical description of the D5 check equation and error conditions).
- H. M. Damm, [“Check digit systems over groups and anti-symmetric mappings”](https://doi.org/10.1007/s000130050524), 2000.
- H. Michael Damm, [*Total anti-symmetrische Quasigruppen*](https://archiv.ub.uni-marburg.de/diss/z2004/0516/pdf/dhmd.pdf), dissertation, Philipps-Universität Marburg, 2004; bibliographic record verified, full text inaccessible during this review.
- [ISO/IEC 7064:2003, *Check Character Systems*](https://www.iso.org/standard/31531.html).
