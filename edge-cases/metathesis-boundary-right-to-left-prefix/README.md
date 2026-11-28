# metathesis-boundary-right-to-left-prefix

A right-to-left metathesis across a `+` boundary, where only segments move. The cells differ in which affix owns the boundary: a prefix's closing `+` or a suffix's opening `+`. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `prefix` | `edge-cases/metathesis-boundary-right-to-left-prefix` | a right-to-left metathesis across the `+` that closes a prefix, where only segments move and the boundary ends up in front of the swapped pair. | unchanged |
| `suffix` | `edge-cases/metathesis-boundary-right-to-left-suffix` | a right-to-left metathesis across the `+` that opens a suffix, where only segments move and the boundary ends up in front of the swapped pair. | `a`→`b`, `p`→`d`, `s`→`f`, `t`→`g` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
