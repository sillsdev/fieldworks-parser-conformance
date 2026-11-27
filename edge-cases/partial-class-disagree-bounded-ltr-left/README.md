# partial-class-disagree-bounded-ltr-left

Synthetic ambiguous disagreement over an explicit vowel class that omits some members of the four-vowel table: the rule flips backness at the first position and rounding at the second, so hc.dll accepts `ia` as `AU|ia` and rejects the other fifteen words. The cells differ in the class's members, the repeated stretch's bound, the rewrite's direction and the environment's side. This test case holds all 6 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses (the letters of the Latin-1 block are used when the ASCII ones run out). Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `bounded-ltr-left` | `edge-cases/partial-class-disagree-bounded-ltr-left` | class `i`, `a`; an optional segment, left-to-right application, environment on the left | unchanged |
| `bounded-rtl-left` | `edge-cases/partial-class-disagree-bounded-rtl-left` | class `a`, `u`; an optional segment, right-to-left application, environment on the left | `a`→`b`, `i`→`d`, `u`→`f`, `y`→`g` |
| `bounded-rtl-right` | `edge-cases/partial-class-disagree-bounded-rtl-right` | class `i`, `y`, `a`; an optional segment, right-to-left application, environment on the right | `a`→`h`, `i`→`j`, `u`→`k`, `y`→`l` |
| `unbounded-ltr-right` | `edge-cases/partial-class-disagree-unbounded-ltr-right` | class `i`, `a`; a stretch of any length, including none, left-to-right application, environment on the right | `a`→`m`, `i`→`n`, `u`→`o`, `y`→`p` |
| `unbounded-rtl-left` | `edge-cases/partial-class-disagree-unbounded-rtl-left` | class `i`, `y`, `a`; a stretch of any length, including none, right-to-left application, environment on the left | `a`→`q`, `i`→`r`, `u`→`s`, `y`→`v` |
| `unbounded-rtl-right` | `edge-cases/partial-class-disagree-unbounded-rtl-right` | class `a`, `u`; a stretch of any length, including none, right-to-left application, environment on the right | `a`→`w`, `i`→`x`, `u`→`z`, `y`→`à` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Oracle: hc.dll, Machine `18cf242f`; 16 complete rows per cell, in PanGloss `docs/divergences/evidence/067-ambiguous-disagreement/` and `evidence/079-partial-explicit-class/`.
Ledger: PanGloss `docs/divergences/079-partial-explicit-class-disagreement.md` (also 067).
FieldWorks: `HCLoader.cs:2338-2344,2745-2770,2799-2808`.
Upstream PR: none (Rust-only defect).
Every cell was graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480); the ordered words, statuses and analysis-signature multiplicities are preserved.
The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
