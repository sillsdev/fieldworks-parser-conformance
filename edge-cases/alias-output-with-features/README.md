# alias-output-with-features

The same pair as `alias-output-featureless`, in a grammar that declares a symbolic feature carried by every segment. A phoneme with two spellings is the output of an obligatory rewrite; each cell writes the rewrite's input as a literal segment or as a one-member natural class. Both spellings parse to the root and the unchanged root does not surface. The feature system is why this is a separate test case from `alias-output-featureless`: it is a grammar-wide difference.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rule, roots and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`.

The grammar declares a shared symbolic feature `cell` and every segment carries its cell's value. Without it, a feature class in one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `literal` | `edge-cases/alias-output-1-literal` | the rewrite's input is a literal segment | unchanged |
| `singleton` | `edge-cases/alias-output-1-singleton` | the rewrite's input is a one-member natural class | `a`→`e`, `i`→`o`, `k`→`u`, `s`→`g`, `t`→`d`, `z`→`f` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv`.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`) returned on a fresh `hc-conformance --propose` run over each member grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadFeatureStruct` writes each segment's feature value.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.
