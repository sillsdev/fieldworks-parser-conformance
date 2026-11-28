# partial-feature-literal-output

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `literal-output` | `edge-cases/partial-feature-literal-output` | a rewrite with a literal output in a grammar whose declared feature has no segment values. | unchanged |
| `unused-feature` | `edge-cases/featureless-unused-feature` | the featureless class rewrite plus one declared symbolic feature that no segment carries: the same two outputs still parse. | `a`→`b`, `i`→`d`, `k`→`f`, `s`→`g`, `t`→`h`, `z`→`j` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-8). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `literal-output`: former README of `partial-feature-literal-output`

### partial-feature-literal-output

Words over a small rewrite grammar. Each row is what C# HermitCrab returns: the output spellings of the rewrite parse to the root, and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

Singleton class targets/outputs or a literal output do not certify a scalar rewrite relation.

The length neighbor is an independent negative control. Ordinary rewrite shapes and partial feature inventories retain the existing loader-based producibility claim.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.

### Cell `unused-feature`: former README of `featureless-unused-feature`

### featureless-unused-feature

Words over a small rewrite grammar. Each row is what C# HermitCrab returns: the output spellings of the rewrite parse to the root, and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

The ordinary rewrite has a segment-class bundle whose alternatives the concrete surface probe does not preserve. Literal and singleton input spellings must not hide an ambiguous output; an unused declared feature must not certify segment specification.

No C# defect or Machine issue is claimed. FieldWorks producibility is a loader shape claim inherited from featureless-segment-class-rewrite, without a round-trip fwdata witness.

The regression must refuse before construction. Positive and negative word controls are retained in words.yaml.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.
