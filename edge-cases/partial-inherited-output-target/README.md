# partial-inherited-output-target

Intervocalic lenition in a grammar whose symbolic feature covers only some segments, where the target class is written as a segment class. Both output spellings parse and the unchanged root does not surface. The `literal` cell writes the target as a two-member segment class and adds two rules whose output is the segment class {s,z}: it drops voice, so a voiceless input gives s and a voiced input gives z (the words isi, izi, ipi, ibi). The `singleton` cell writes the target as a one-member segment class.

## Cells

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
