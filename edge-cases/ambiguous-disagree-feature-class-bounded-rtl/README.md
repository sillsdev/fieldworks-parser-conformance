# ambiguous-disagree-feature-class-bounded-rtl

Synthetic ambiguous disagreement over alpha-governed back and round values on the four-vowel table, where hc.dll requires `ia` and rejects the other words. The cells differ in the rewrite's environment and the class it ranges over. This test case holds all 4 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `bounded-rtl` | `edge-cases/ambiguous-disagree-feature-class-bounded-rtl` | an optional segment, right-to-left application, environment on the right. | unchanged |
| `unbounded-ltr` | `edge-cases/ambiguous-disagree-feature-class-unbounded-ltr` | a stretch of any length, including none, left-to-right application, environment on the right. | `a`→`b`, `i`→`d`, `u`→`f`, `y`→`g` |
| `mixed-plus` | `edge-cases/ambiguous-disagree-mixed-plus-class` | no environment at all, left-to-right application. | `a`→`h`, `i`→`j`, `u`→`k`, `y`→`l` |
| `repeated-minus` | `edge-cases/ambiguous-disagree-repeated-minus-partial-focus` | one segment, left-to-right application, environment on the left. | `a`→`m`, `i`→`n`, `u`→`o`, `y`→`p` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

Label re-check of the `bounded-rtl` cell: on the reference, flipping the rule to left-to-right, raising the environment's upper bound to 2 or to no bound, and deleting the optional element each leave all 16 results unchanged, so neither the direction nor the bound is exercised and the old `bounded repeat` label is not evidenced. Making the element mandatory (minimum 1) changes `ia` and `au`. The 14 other words of the cell carry the alpha-variable label; `ia` and `au` carry `zero-minimum repeat`, the construct their results depend on.

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `bounded-rtl`: former README of `ambiguous-disagree-feature-class-bounded-rtl`

### ambiguous-disagree-feature-class-bounded-rtl: provenance and regression rationale

Graduated from PanGloss staging into this suite.
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### ambiguous-disagree-feature-class-bounded-rtl

Synthetic feature-defined vowel class with an ambiguous minus-alpha rewrite context and a bounded right-to-left optional environment. This test case is a negative witness for the still-refused lowerability shape; the authored class is a FeatureNaturalClass, not an explicit SegmentNaturalClass.

Reference: hc.dll, Machine `18cf242f`; 16 complete rows, 0 skipped. The reference accepts only `ia` as `AU|[iy]a`. Evidence: `docs/divergences/evidence/079-partial-explicit-class/refusal-witnesses/`.
FieldWorks/Machine: `HCLoader.cs:2338-2344, 2745-2770`; Machine `XmlLanguageLoader.cs:696-719`.
Ledger: `docs/divergences/079-partial-explicit-class-disagreement.md`.
Upstream PR: none (network closed).

### Cell `unbounded-ltr`: former README of `ambiguous-disagree-feature-class-unbounded-ltr`

### ambiguous-disagree-feature-class-unbounded-ltr: provenance and regression rationale

Graduated from PanGloss staging into this suite.
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### ambiguous-disagree-feature-class-unbounded-ltr

Synthetic feature-defined vowel class with an ambiguous minus-alpha rewrite context and an unbounded left-to-right optional environment. This test case is a negative witness for the still-refused lowerability shape; the authored class is a FeatureNaturalClass, not an explicit SegmentNaturalClass.

Reference: hc.dll, Machine `18cf242f`; 16 complete rows, 0 skipped. The reference accepts only `ia` as `AU|[iy]a`. Evidence: `docs/divergences/evidence/079-partial-explicit-class/refusal-witnesses/`.
FieldWorks/Machine: `HCLoader.cs:2338-2344, 2745-2770`; Machine `XmlLanguageLoader.cs:696-719`.
Ledger: `docs/divergences/079-partial-explicit-class-disagreement.md`.
Upstream PR: none (network closed).

### Cell `mixed-plus`: former README of `ambiguous-disagree-mixed-plus-class`

### ambiguous-disagree-mixed-plus-class: provenance and regression rationale

Graduated from PanGloss staging into this suite.
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### ambiguous-disagree-mixed-plus-class

Synthetic ambiguous minus alpha on a complete class, with an agreeing occurrence
on a partial class. hc.dll still requires ia, despite the omitted u in that class.
Reference: hc.dll, Machine `18cf242f`; 16 complete rows.
Entry: docs/divergences/067-ambiguous-disagreement-proposals.md.
FieldWorks: HCLoader.cs:2745-2770,2799-2808.
Upstream PR: none (network closed).

### Cell `repeated-minus`: former README of `ambiguous-disagree-repeated-minus-partial-focus`

### ambiguous-disagree-repeated-minus-partial-focus: provenance and regression rationale

Graduated from PanGloss staging into this suite.
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### ambiguous-disagree-repeated-minus-partial-focus

Synthetic repeated minus alpha on a complete class and an agreeing focus on
a partial class. hc.dll requires ii from iu.
Reference: hc.dll, Machine `18cf242f`; 16 complete rows.
Analysis binding: docs/divergences/069-analysis-binds-overridden-alpha.md.
Confirmed FST proposal: docs/divergences/067-ambiguous-disagreement-proposals.md.
FieldWorks: HCLoader.cs:2338-2344,2745-2770,2799-2808.
Upstream PR: none (network closed).
