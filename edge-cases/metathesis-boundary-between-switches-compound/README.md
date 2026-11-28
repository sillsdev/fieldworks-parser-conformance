# metathesis-boundary-between-switches-compound

A metathesis whose two switches have a boundary between them. The cells differ in where the boundary comes from (a compound junction, a boundary marker written in the pattern, the `+` closing a prefix). This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `compound` | `edge-cases/metathesis-boundary-between-switches-compound` | a metathesis whose two switches are the last segment of one compound part and the first of the next, with a `+` junction between them. | unchanged |
| `marker` | `edge-cases/metathesis-boundary-between-switches-marker` | a metathesis whose pattern writes a boundary marker between the switches, applied where the prefix adds a second boundary. | `a`→`b`, `p`→`d`, `s`→`f`, `t`→`g` |
| `prefix` | `edge-cases/metathesis-boundary-between-switches-prefix` | a metathesis whose switches are split by the `+` that closes a prefix, which the matcher steps over. | `a`→`h`, `p`→`j`, `s`→`k`, `t`→`l` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
