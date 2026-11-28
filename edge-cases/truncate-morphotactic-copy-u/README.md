# truncate-morphotactic-copy-u

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `copy-u` | `edge-cases/truncate-morphotactic-copy-u` | the truncation grammar with explicit morpheme ids and a copying suffix rule, so one surface form has several parses with different rule histories. | unchanged |
| `subsumption` | `edge-cases/truncate-morphotactic-subsumption` | a prefix rule, a leading truncation and an insertion rule over the root `ag`, so a rule can remove what an earlier rule added. | `a`→`d`, `b`→`f`, `g`→`h`, `i`→`j`, `s`→`k`, `u`→`l` |
| `identity` | `edge-cases/truncate-morphotactic-identity` | the truncation grammar with explicit morpheme ids, so repeated signatures stay distinct rows. | `a`→`m`, `b`→`n`, `g`→`o`, `i`→`p`, `s`→`q`, `u`→`r` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-9). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
