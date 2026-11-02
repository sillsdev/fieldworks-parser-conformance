# quantified-alpha-unbounded-ltr-right: provenance and regression rationale

Graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480).
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current oracle was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

# quantified-alpha-unbounded-ltr-right

Synthetic repeated-alpha environment parity regression. C# requires every
repetition of the voice variable to agree. Mixed c/t repetitions must leave
the root unchanged; uniform repetitions must permit the rewrite.

Oracle: hc.dll, Machine `18cf242f`; 17 complete
word rows recorded with the conformance batch adapter, no skipped/capped rows.

Divergence: `docs/divergences/058-repeated-environment-alpha-agreement.md`.
FieldWorks: `HCLoader.cs:2338-2344,2745-2770`.
Upstream PR: none (Rust-only bug; network closed).
