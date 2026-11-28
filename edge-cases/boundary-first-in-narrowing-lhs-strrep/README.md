# boundary-first-in-narrowing-lhs-strrep

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `first-strrep` | `edge-cases/boundary-first-in-narrowing-lhs-strrep` | the same merge in a grammar with no phonological features. | unchanged |
| `leftover-strrep` | `edge-cases/boundary-leftover-in-narrowing-lhs-strrep` | a merge that absorbs a nasal and a boundary, with no phonological features. | `a`→`d`, `b`→`f`, `k`→`g`, `m`→`h`, `n`→`j`, `o`→`l`, `t`→`p` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-9). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
