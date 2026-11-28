# partial-inherited-output-target

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `target` | `edge-cases/partial-inherited-output-target` | intervocalic lenition in a grammar whose symbolic feature covers only some segments, in two cells (the target a two-member segment class plus two rules whose output is the class {s,z}, or a one-member segment class): both output spellings parse and the unchanged root does not. | unchanged |
| `feature` | `edge-cases/partial-inherited-output-feature` | intervocalic lenition in a grammar whose symbolic feature covers only some segments, with the target class written as a feature class: both output spellings parse and the unchanged root does not. | `a`→`h`, `i`→`j`, `k`→`l`, `s`→`m`, `t`→`n`, `z`→`q` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-6). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `target`: former README of `partial-inherited-output-target`

### partial-inherited-output-target

Intervocalic lenition in a grammar whose symbolic feature covers only some segments, where the target class is written as a segment class. Both output spellings parse and the unchanged root does not surface. The `literal` cell writes the target as a two-member segment class and adds two rules whose output is the segment class {s,z}: it drops voice, so a voiceless input gives s and a voiced input gives z (the words isi, izi, ipi, ibi). The `singleton` cell writes the target as a one-member segment class.

#### Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`.

The grammar declares a shared symbolic feature `cell` and every segment carries its cell's value. Without it, a feature class in one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `literal` | `edge-cases/partial-inherited-output-literal` | the target is a two-member segment class, plus the {s,z} output-class rules | unchanged |
| `singleton` | `edge-cases/partial-inherited-output-singleton` | the target is a one-member segment class | `a`→`e`, `i`→`o`, `k`→`u`, `s`→`g`, `t`→`d`, `z`→`f` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`) returned on a fresh `hc-conformance --propose` run over each member grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadFeatureStruct` and `LoadNaturalClass` write single-valued feature structures and an omitted segment feature.
- `LoadPatternNode` and `TryLoadSimpleContext` read the natural-class output context.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.

### Cell `feature`: former README of `partial-inherited-output-feature`

### partial-inherited-output-feature

Words over a small rewrite grammar. Each row is what C# HermitCrab returns: the output spellings of the rewrite parse to the root, and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.
