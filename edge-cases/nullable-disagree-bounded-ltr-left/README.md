# nullable-disagree-bounded-ltr-left

Synthetic back/round disagreement over the whole four-vowel class, with a nullable stretch in the environment that must still allow the rewrite at the word edge; `ia` is the one surface word. The cells differ in the stretch's bound, the rewrite's direction and the environment's side (one cell has no environment). This test case holds all 9 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses (the letters of the Latin-1 block are used when the ASCII ones run out). Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `bounded-ltr-left` | `edge-cases/nullable-disagree-bounded-ltr-left` | an optional segment, left-to-right application, environment on the left | unchanged |
| `bounded-ltr-right` | `edge-cases/nullable-disagree-bounded-ltr-right` | an optional segment, left-to-right application, environment on the right | `a`→`b`, `i`→`d`, `u`→`f`, `y`→`g` |
| `bounded-rtl-left` | `edge-cases/nullable-disagree-bounded-rtl-left` | an optional segment, right-to-left application, environment on the left | `a`→`h`, `i`→`j`, `u`→`k`, `y`→`l` |
| `bounded-rtl-right` | `edge-cases/nullable-disagree-bounded-rtl-right` | an optional segment, right-to-left application, environment on the right | `a`→`m`, `i`→`n`, `u`→`o`, `y`→`p` |
| `plain-ltr-right` | `edge-cases/nullable-disagree-plain-ltr-right` | no environment at all, left-to-right application | `a`→`q`, `i`→`r`, `u`→`s`, `y`→`v` |
| `unbounded-ltr-left` | `edge-cases/nullable-disagree-unbounded-ltr-left` | a stretch of any length, including none, left-to-right application, environment on the left | `a`→`w`, `i`→`x`, `u`→`z`, `y`→`à` |
| `unbounded-ltr-right` | `edge-cases/nullable-disagree-unbounded-ltr-right` | a stretch of any length, including none, left-to-right application, environment on the right | `a`→`á`, `i`→`â`, `u`→`ã`, `y`→`ä` |
| `unbounded-rtl-left` | `edge-cases/nullable-disagree-unbounded-rtl-left` | a stretch of any length, including none, right-to-left application, environment on the left | `a`→`å`, `i`→`æ`, `u`→`ç`, `y`→`è` |
| `unbounded-rtl-right` | `edge-cases/nullable-disagree-unbounded-rtl-right` | a stretch of any length, including none, right-to-left application, environment on the right | `a`→`é`, `i`→`ê`, `u`→`ë`, `y`→`ì` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Reference: hc.dll, Machine `18cf242f`; 16 complete rows per cell.
Divergence: PanGloss `docs/divergences/065-nullable-rewrite-environment.md` (also 067).
FieldWorks: `HCLoader.cs:2338-2344,2745-2770`.
Upstream PR: none (Rust-only defect).
Every cell was graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480); the ordered words, statuses and analysis-signature multiplicities are preserved.
The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
