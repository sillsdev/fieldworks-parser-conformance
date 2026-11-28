# quantified-alpha-bounded-ltr-left

Synthetic repeated-alpha environment: C# requires every repetition of the voice variable to agree. Mixed `c`/`t` repetitions must leave the root unchanged and uniform repetitions must permit the rewrite. The cells differ in the repetition's bound (exactly two, two or more, up to two, any number including none), the rewrite's direction and the environment's side. In the `zero` cells the stretch may be empty and four more roots are declared. This test case holds all 12 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses (the letters of the Latin-1 block are used when the ASCII ones run out). Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `bounded-ltr-left` | `edge-cases/quantified-alpha-bounded-ltr-left` | exactly 2 segments, left-to-right application, environment on the left | unchanged |
| `bounded-ltr-right` | `edge-cases/quantified-alpha-bounded-ltr-right` | exactly 2 segments, left-to-right application, environment on the right | `a`→`b`, `c`→`d`, `e`→`f`, `t`→`g` |
| `bounded-rtl-left` | `edge-cases/quantified-alpha-bounded-rtl-left` | exactly 2 segments, right-to-left application, environment on the left | `a`→`h`, `c`→`j`, `e`→`k`, `t`→`l` |
| `bounded-rtl-right` | `edge-cases/quantified-alpha-bounded-rtl-right` | exactly 2 segments, right-to-left application, environment on the right | `a`→`m`, `c`→`n`, `e`→`o`, `t`→`p` |
| `bounded-zero-left` | `edge-cases/quantified-alpha-bounded-zero-left` | up to 2 segments, including none, left-to-right application, environment on the left | `a`→`q`, `c`→`r`, `e`→`s`, `t`→`v` |
| `bounded-zero-right` | `edge-cases/quantified-alpha-bounded-zero-right` | up to 2 segments, including none, left-to-right application, environment on the right | `a`→`w`, `c`→`x`, `e`→`z`, `t`→`à` |
| `unbounded-ltr-left` | `edge-cases/quantified-alpha-unbounded-ltr-left` | 2 or more segments, left-to-right application, environment on the left | `a`→`á`, `c`→`â`, `e`→`ã`, `t`→`ä` |
| `unbounded-ltr-right` | `edge-cases/quantified-alpha-unbounded-ltr-right` | 2 or more segments, left-to-right application, environment on the right | `a`→`å`, `c`→`æ`, `e`→`ç`, `t`→`è` |
| `unbounded-rtl-left` | `edge-cases/quantified-alpha-unbounded-rtl-left` | 2 or more segments, right-to-left application, environment on the left | `a`→`é`, `c`→`ê`, `e`→`ë`, `t`→`ì` |
| `unbounded-rtl-right` | `edge-cases/quantified-alpha-unbounded-rtl-right` | 2 or more segments, right-to-left application, environment on the right | `a`→`í`, `c`→`î`, `e`→`ï`, `t`→`ð` |
| `unbounded-zero-left` | `edge-cases/quantified-alpha-unbounded-zero-left` | a stretch of any length, including none, left-to-right application, environment on the left | `a`→`ñ`, `c`→`ò`, `e`→`ó`, `t`→`ô` |
| `unbounded-zero-right` | `edge-cases/quantified-alpha-unbounded-zero-right` | a stretch of any length, including none, left-to-right application, environment on the right | `a`→`õ`, `c`→`ö`, `e`→`ø`, `t`→`ù` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Reference: hc.dll, Machine `18cf242f`; 17 complete word rows per cell (19 in the `zero` cells) recorded with the conformance batch adapter, no skipped or capped rows.
Divergence: PanGloss `docs/divergences/058-repeated-environment-alpha-agreement.md`.
FieldWorks: `HCLoader.cs:2338-2344,2745-2770`.
Upstream PR: none (Rust-only bug).
Every cell was graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480); the ordered words, statuses and analysis-signature multiplicities are preserved.
The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
