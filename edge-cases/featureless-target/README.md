# featureless-target

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `target` | `edge-cases/featureless-target` | a featureless rewrite whose output is a class of two segments, in two cells (the target a literal segment, or a one-member class): both outputs parse as one root. | unchanged |
| `alias` | `edge-cases/alias-output-featureless` | a phoneme with two spellings as the output of an obligatory rewrite, in a grammar with no feature system, in two cells (the input written as a literal segment, or as a one-member natural class): both spellings parse and the unchanged root does not. | `a`→`b`, `d`→`h`, `e`→`j`, `f`→`l`, `g`→`m`, `i`→`n`, `k`→`p`, `o`→`q`, `s`→`r`, `t`→`v`, `u`→`w`, `z`→`x` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-8). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `target`: former README of `featureless-target`

### featureless-target

A featureless rewrite whose output is a class of two segments: both outputs parse as one root and the unchanged root does not surface. The cells differ in the rewrite's target: a literal segment (beside a two-member class), or a one-member class. A literal or singleton target must not hide an ambiguous output. `featureless-unused-feature` stays separate: it declares a feature system.

#### Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `literal` | `edge-cases/featureless-literal-target` | the target is a literal segment | unchanged |
| `singleton` | `edge-cases/featureless-singleton-target` | the target is a one-member natural class | `a`→`e`, `i`→`o`, `k`→`u`, `s`→`g`, `t`→`d`, `z`→`f` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`) returned on a fresh `hc-conformance --propose` run over each member grammar and word list; none is copied from PanGloss's staged copy. No C# defect or Machine issue is claimed. FieldWorks producibility is a loader shape claim inherited from featureless-segment-class-rewrite, without a round-trip fwdata witness.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.

### Cell `alias`: former README of `alias-output-featureless`

### alias-output-featureless

A phoneme with two spellings as the output of an obligatory rewrite, in a grammar with no feature system. Each cell writes the same rewrite with a different input: a literal segment, or a one-member natural class. Both spellings parse to the root and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

#### Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `literal` | `edge-cases/alias-output-0-literal` | the rewrite's input is a literal segment | unchanged |
| `singleton` | `edge-cases/alias-output-0-singleton` | the rewrite's input is a one-member natural class | `a`→`e`, `i`→`o`, `k`→`u`, `s`→`g`, `t`→`d`, `z`→`f` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`) returned on a fresh `hc-conformance --propose` run over each member grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.
