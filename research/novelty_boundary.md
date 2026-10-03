# R7 Novelty Boundary

> Historical literature-boundary snapshot from R7. Later source assessments and the R12 research decision refine its status; retain this as a record of the evidence reviewed at that stage.

## Purpose and evidence limits

This note bounds the research claims supported by the current project after a literature review. It does not claim that a search can prove a result absent from all literature. The detailed claim mapping is in [prior_art_claim_matrix.md](prior_art_claim_matrix.md); the mathematics and assumptions are in [formal_model.md](formal_model.md). The project's [R6 profile engine](detection_profile_engine.md) packages those formulas as software, but software implementation does not establish a new theorem.

## What is definitely established prior art

1. **Error-detecting codes and check characters are mature areas.** Hamming's 1950 paper is foundational for binary error detection/correction codes, though it is not the direct source of this decimal weighted-sum model. Verhoeff's 1969 monograph is a direct, extensive treatment of decimal error-detecting codes, including modular sums, weighted sums, generalized weights, single errors, adjacent transpositions, detection rates, and computer-assisted searches.
2. **Weighted modular check equations are established.** In a weighted sum \(S(x)=\sum_iw_ix_i\pmod m\), substitution and transposition changes follow by subtraction. Verhoeff §2.3.3, pp. 54–55 explicitly examines weighted modular decimal checks and the conditions on weights for single errors and transpositions. This substantially covers the mathematical framework in which the project's positional checksum sits.
3. **Modulus-11 check digits and weighted decimal identifiers predate this project.** Verhoeff discusses modulus-11 weighted schemes; the International ISBN Agency documents the ISBN-10 scheme with weights 10 through 1 and X for a check value of 10. That is a check-character code, distinct from this project’s unweighted integer residue, but it makes generic “modulus 11 detects digit errors” statements old and too broad.
4. **Universal single-error and adjacent-transposition guarantees occur in prior check-digit systems.** Verhoeff's monograph constructs/checks decimal systems with these guarantees; the abstract for Gumm (1985) describes a one-check-digit method for arbitrary number systems using dihedral groups; Damm (2000) treats existence in group systems through anti-symmetric mappings. Those constructions are not the project's plain linear residue, but they preclude framing such guarantees as a new general idea.
5. **Classification and equivalence of check systems are prior topics.** Schulz's 2001 chapter §§3.1–3.2 defines equivalence notions for group-based check systems and discusses preservation of error rates and computed equivalence classes. The project’s proposed equality of plain-modulus profiles is a distinct observable-specific relation, but equivalence as a research direction is not unprecedented.
6. **Computational search and detection-rate analysis are prior art.** Verhoeff documents measured error statistics, scheme-specific detection-rate tables, transformations that preserve rates, and a search program (§§0.5, 2.3, 3.3–3.4). A broad claim to first compute or enumerate decimal checksum behavior would be unsupported.

## What is directly derivable from established theory

For an integer-valued string (N(x)=\sum_kx_k10^k), a substitution changes the value by \((b-a)10^k\). Swapping adjacent digits changes it by \(9(b-a)10^k\), up to sign. These are immediate subtractions and are instances of the established weighted-sum identities

\[
\Delta_{\mathrm{sub}}=(b-a)w_i,\qquad
\Delta_{\mathrm{swap}}=(a_i-a_j)(w_i-w_j)
\]

modulo (m). Taking (w_k=10^k) specializes the general model. The gcd cancellation lemma then gives the necessary-and-sufficient conditions

\[
\frac{m}{\gcd(m,10^k)}\mid |b-a|,
\qquad
\frac{m}{\gcd(m,9\cdot10^k)}\mid |b-a|.
\]

Those exact conditions are useful formal statements for this model, but no new proof technique is involved. The factorization and stabilization formulas, universal-detection tests, and modulus-11/moduli-3-and-9 consequences follow by elementary divisibility plus the finite digit-difference bound \(1\le |b-a|\le9\). We found no matching statement in the inspected source locations; that is not a novelty determination.

The count

\[
W(h)=2\sum_{j=1}^{\lfloor9/h\rfloor}(10-hj)
\]

is a direct finite count of ordered decimal digit pairs whose nonzero difference is divisible by (h). We did not locate this generic formula or an identical named function in the bounded literature search. Existing decimal-code literature does calculate scheme-specific rates and digit-pair conditions, especially Verhoeff's tables and weighted-code analysis. Therefore the formula is a potentially useful compact representation, but its prior-art status remains **insufficiently located**; it must not be described as new.

## What the project contributes computationally

The repository makes the formulas executable as exact position/length profiles, with rational rates, universal-detection flags, and an analytic cross-check against exhaustive enumeration. The historical experiment supplies 232 per-length rows for moduli 2–30 and lengths 1–4 and 58 pooled modulus/error-class rows. This is a finite computational illustration, not a proof for arbitrary moduli or lengths. Its distinctive value that can currently be evidenced is **reproducibility within this repository**: definitions, code, tests, and saved artifacts can be inspected together. No comparative study establishes that this exact implementation format or sweep is unique, and Verhoeff's documented search makes broader computational novelty claims inappropriate.

The behavioral relation “same position-resolved reduced-divisor/count/rate signature” is mathematically well-defined once the observables and domain are fixed. It is a project-specific equivalence relation in that exact form. Prior work on check-system equivalence and rate-preserving transformations (Schulz 2001; Verhoeff 1969) is a substantial analogue. The currently available evidence does not establish that the resulting classes of plain moduli are novel, useful, or minimal.

## What remains insufficiently located

- Whether a prior source gives the same generic ordered digit-pair count as (W(h)), perhaps as an undetected substitution/transposition probability or a digit-difference distribution.
- Whether the two stable reduced-divisor formulas already appear in alternate radix/valuation notation.
- Whether a prior classification treats plain residue moduli by equality of all position-resolved substitution and unequal-swap profiles.
- Whether the R6 API's bundle of divisors, counts, rates, and flags offers a useful minimal representation beyond the elementary formulas.
- Whether the saved finite tables expose an interpretive structure not already apparent from Verhoeff's decimal-code survey, weighted-code analysis, or later check-character literature.

These are open literature questions, not positive novelty claims. Search coverage so far included Hamming, Verhoeff, Gumm, Damm, ISO/IEC 7064, ISBN-10, Luhn's patent, weighted checksum descriptions, and adjacent substitution/transposition coding work. Full text was directly inspected for Verhoeff and Schulz; Hamming's publisher metadata plus a short open extract, ISO's official preview, ISBN.org's FAQ, Luhn's patent, and Abdel-Ghaffar's publisher abstract were accessible. Gumm's and Damm's full papers were not accessible. The [matrix](prior_art_claim_matrix.md) records exact limits source by source.

## Research question to abandon or narrow

Abandon any framing that asks whether plain modular decimal checks can detect substitutions/swaps, whether modulus 11 can provide those guarantees, or whether a weighted checksum can be analyzed from its positional weights. These are answered by the project's short derivations and are broadly covered by established weighted-check and decimal-code literature. Also abandon “first exhaustive computational study” or “new checksum” language.

The earlier broad question about a complete exact profile for arbitrary (m,n) is mathematically answered by the reduced divisors and (W(h)); as a standalone theorem it appears elementary and closely aligned with established weighted checksum analysis. It should not be presented as a paper contribution unless a targeted full-text review finds a precise gap and the project can show why that gap matters.

## Questions still worth investigating

1. **Primary-source overlap question:** Does the exact combination of a generic digit-difference count (W(h)), the reduced-divisor profile, and prime-factor stabilization already occur in check-digit/error-statistics literature under another notation? This is the immediate unresolved boundary.
2. **Narrow classification question:** If prior work does not already answer it, what are the necessary and sufficient arithmetic conditions for two moduli to induce identical *all-position* profiles for both specified error classes? The question becomes worthwhile only if the classification is simpler or more explanatory than directly comparing the two (h)-sequences and if its relation to existing check-system equivalence is explicit.
3. **Interpretive-value question:** Does the profile equivalence partition or compact representation yield a nontrivial result for a declared domain or observable, rather than simply compressing equal outputs? This requires a clear theorem or use case and comparative literature evidence.

The first question must be resolved before investing in a new equivalence theorem or claiming a gap. No current evidence supports describing any of these as novel.

## Paper-level assessment

| Form | Current evidence that is sufficient | What is missing | Assessment |
|---|---|---|---|
| Mathematical research paper | Exact definitions, correct derivations, and general (m,n) formulas are documented. | A nontrivial result beyond elementary specialization, a completed prior-art comparison, and a demonstrated mathematical insight or consequence. | Not supported in the present form. A narrow classification might become a candidate only after the prior-art question is resolved. |
| Computational mathematics paper | Exact profile engine, finite historical outputs, formula checks, and reproducible repository artifacts are available. | A computational question with insight beyond formulas, independent verification design, and a comparison to prior decimal-code searches and analyses. | Possible direction, but present results alone do not demonstrate a publishable computational contribution. |
| Reproducibility/computational experiment paper | Input definitions and saved results support rerunning/reconciling the configured finite study. | External users/use cases, evaluation of reproducibility contribution, and explicit comparison with earlier computational treatments such as Verhoeff's search. | Current repository is a reproducible project artifact; paper suitability is not established. |
| Technical note | The elementary proof can be presented concisely with exact scope and careful finite/proven distinction. | A clear audience/useful reason to publish the specialization and confirmation that no directly matching note exists. | The most proportionate possible format, but still requires a targeted prior-art search and a distinct reason for publication. |
| Educational/tutorial article | The project has accessible worked examples, visualizations, and a clean distinction between residue checks and check-character systems. | Pedagogical evaluation, a target readership, and careful sourcing of established methods. | Potentially appropriate as educational material; this would be a teaching contribution, not a novelty claim. |

These are assessments of evidence, not publication predictions.

## Literature needed before an arXiv/SSRN submission

- Obtain and inspect the full Gumm (1985) and Damm (2000) primary articles through an institutional library or other lawful route. Map their exact definitions and theorem statements; do not use their abstracts to attribute an unverified gcd or count formula.
- Trace the relevant citations from Verhoeff's §§2.3.3 and 3.1, especially the prior weighted-sum and modulus-11 analyses, and inspect the sources that formulate weighted-check detection criteria.
- Search scholarly databases and bibliographies for exact or equivalent formulas for digit-difference counts and undetected-error rates, including work using “coverage,” “error statistics,” “check equation,” and “weight sequence” rather than modern checksum terminology.
- Search for plain-residue modular equivalence/classification and compare carefully against group-based check-character equivalence; do not conflate these different models.
- If the exact (W(h))/stabilization combination is still not located, state search databases, queries, date, inclusion criteria, and inaccessible records so the boundary is auditable. A finite search record still does not prove absence.
- Check current manuscript references and permissions before reproducing source tables; cite sources for the claims they establish and label all new algebra as a derivation from stated definitions.

## Research ethics and citation audit

- No fabricated references, theorem identifiers, page citations, or quotations are used here.
- No result is called novel, first, or a new theorem. “Not located” is explicitly bounded to the records and sections inspected.
- Hamming's full original paper was not accessed in the publisher view; an open short extract and bibliographic page support only the limited description given.
- Verhoeff's full CWI scan was inspected at the cited sections. Its historical search/rate work is explicitly acknowledged as prior computational analysis.
- Gumm's and Damm's full texts were not accessed. Abstract-level claims are marked as such and are not used to prove the project's exact formulas.
- The official ISO page is an abstract/preview, not the paid standard text. ISBN support is from the International ISBN Agency FAQ, not an inspected ISBN standard clause.
- Luhn's accessible patent supports its described procedure and context; it is not treated as proof of every subsequent Luhn guarantee.
- The distinction between a check-character code with a valid-word set and this project's plain residue comparison is maintained throughout.

## Exactly one recommended next research action

**Conduct a focused primary-source overlap review of the full Gumm (1985) and Damm (2000) papers, obtained lawfully, and follow their citations back to weighted modular check analyses cited by Verhoeff.** The deliverable should be a page-and-theorem-level comparison against claims B–N, especially the general weighted-sum conditions, exact pair counts, stabilization formulas, and equivalence notions. This resolves the closest remaining literature uncertainty before any new theorem, paper framing, or implementation work is proposed.

## References consulted

- R. W. Hamming, “Error Detecting and Error Correcting Codes,” *Bell System Technical Journal* 29(2), 147–160 (1950), [DOI](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x).
- J. Verhoeff, *Error Detecting Decimal Codes*, Mathematical Centre Tract 29 (1969), [CWI repository record and scan](https://ir.cwi.nl/pub/32080).
- H. P. Gumm, “A new class of check-digit methods for arbitrary number systems,” *IEEE Transactions on Information Theory* 31(1), 102–105 (1985), [DOI](https://doi.org/10.1109/TIT.1985.1056991).
- M. Damm, “Check digit systems over groups and anti-symmetric mappings,” *Archiv der Mathematik* 75(6), 413–421 (2000), [DOI](https://doi.org/10.1007/s000130050524).
- R.-H. Schulz, “Check Character Systems and Anti-symmetric Mappings,” *Computational Discrete Mathematics*, LNCS 2122 (2001), 136–147, [author-hosted text](https://page.mi.fu-berlin.de/rhschulz/digits.pdf).
- ISO/IEC 7064:2003, *Information technology — Security techniques — Check character systems*, [official ISO page](https://www.iso.org/standard/31531.html).
- International ISBN Agency, [FAQs: General Questions](https://www.isbn.org/faqs_general_questions).
- H. P. Luhn, US Patent 2,950,048, “Computer for Verifying Numbers,” [patent text](https://patents.google.com/patent/US2950048A/en).
- K. A. S. Abdel-Ghaffar, “Detecting Substitutions and Transpositions of Characters,” *The Computer Journal* 41(4), 270–277 (1998), [publisher abstract](https://academic.oup.com/comjnl/article-abstract/41/4/270/476224).
- B. Parhami, *Dependable Computing: A Multilevel Approach*, ch. 13 excerpt, [author-hosted PDF](https://web.ece.ucsb.edu/~parhami/docs_folder/f33-book-dep-comp-pt4.pdf).
