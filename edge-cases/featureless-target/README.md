# featureless-target

A featureless rewrite whose output is a class of two segments: both outputs parse as one root and the unchanged root does not surface. The cells differ in the rewrite's target: a literal segment (beside a two-member class), or a one-member class. A literal or singleton target must not hide an ambiguous output. `featureless-unused-feature` stays separate: it declares a feature system.

## Cells

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
