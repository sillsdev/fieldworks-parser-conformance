# final-template-partial-reachability

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `reachability` | `edge-cases/final-template-partial-reachability` | [XAmple] four final templates, only one of which a partial word can reach, with a partial rule and a partial entry. | unchanged |
| `root` | `edge-cases/final-template-partial-root` | [XAmple] a partial root with a final template, and ordinary rules blocked after the template. | `a`→`h`, `b`→`j`, `d`→`v`, `f`→`à`, `g`→`á`, `i`→`â`, `k`→`ã`, `n`→`ä`, `p`→`å` |
| `trace` | `edge-cases/final-template-partial-trace` | [XAmple] one word that both final-template refusals reject, and that parses once the partial rule is made ordinary. | `a`→`æ`, `f`→`ç`, `g`→`è`, `q`→`é`, `s`→`ê`, `t`→`ë` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-8). The `root` cell's former `morpher: MakePartialsFinal: false` is the engine default (`Morpher.AlwaysEnforceFinalTemplates` is a plain `bool`), so the merged test case has no `morpher:` block; the rationale of that cell is in `docs/final-template-partial-root.md`. The `root` and `trace` cells keep their two strata (the first stratum of the merged grammar holds their rules and lower entries; the last holds the reachability cell). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).
