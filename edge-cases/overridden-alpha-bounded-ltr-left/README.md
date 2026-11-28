# overridden-alpha-bounded-ltr-left

Synthetic neutralisation of an alpha-governed feature: a vowel focus binds plus alpha backness, its left environment is a vowel with minus alpha backness, and the replacement is the literal `i`, which overwrites the governed backness. hc.dll requires `ii` from the root `iu`. The cells differ in how many segments the environment's repeated stretch holds and in the rewrite's direction. This test case holds all 4 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses (the letters of the Latin-1 block are used when the ASCII ones run out). Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `bounded-ltr-left` | `edge-cases/overridden-alpha-bounded-ltr-left` | 1 to 2 segments, left-to-right application, environment on the left | unchanged |
| `bounded-rtl-left` | `edge-cases/overridden-alpha-bounded-rtl-left` | 1 to 2 segments, right-to-left application, environment on the left | `a`→`b`, `i`→`d`, `u`→`f`, `y`→`g` |
| `plain-ltr-left` | `edge-cases/overridden-alpha-plain-ltr-left` | no repeated stretch, left-to-right application, environment on the left | `a`→`h`, `i`→`j`, `u`→`k`, `y`→`l` |
| `unbounded-ltr-left` | `edge-cases/overridden-alpha-unbounded-ltr-left` | 1 or more segments, left-to-right application, environment on the left | `a`→`m`, `i`→`n`, `u`→`o`, `y`→`p` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Reference: hc.dll, Machine `18cf242f`; 16 complete rows per cell, all recorded in PanGloss `docs/divergences/evidence/069-overridden-alpha/`.
Owner regression: PanGloss `docs/divergences/069-analysis-binds-overridden-alpha.md` (also 067).
FieldWorks: `HCLoader.cs:2033-2067,2338-2344,2745-2770,2799-2808`.
Upstream PR: none (Rust-only defect).
Every cell was graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480); the ordered words, statuses and analysis-signature multiplicities are preserved.
The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
