# alias-output-featureless

A phoneme with two spellings as the output of an obligatory rewrite, in a grammar with no feature system. Each cell writes the same rewrite with a different input: a literal segment, or a one-member natural class. Both spellings parse to the root and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

## Cells

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
