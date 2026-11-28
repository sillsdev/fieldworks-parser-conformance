# spelling-coverage-compound-junction-mark

Compounds at the junction where a character that decomposes to a base plus a combining mark is in the character table (MaxRoots 3). The cells differ in the role of the character: a spelling of a segment that starts with a combining mark, or a spelling of the compound boundary. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label. Each cell has its own boundary definition: the boundary character of every cell after the first is mapped like a letter (the map column), because two cells cannot share a boundary spelling that appears in signatures. A character the cell tests (a quote, a combining mark, a Thai mark, `é`) is never mapped. `MaxRoots: 3` is the setting of every cell.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `mark` | `edge-cases/spelling-coverage-compound-junction-mark` | A phoneme spelling that begins with a combining mark follows a root at the compound junction. | unchanged |
| `boundary-mark` | `edge-cases/spelling-coverage-compound-junction-boundary-mark` | The compound boundary is written as the code `é`, a letter that decomposes to a base plus a combining mark. | `a`→`b`, `p`→`d`, `s`→`f`, `t`→`g`, `á`→`h`, `+`→`~`, `-`→`#`, `=`→`%` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `mark`: former README of `spelling-coverage-compound-junction-mark`

### spelling-coverage-compound-junction-mark

A phoneme spelling that begins with a combining mark follows a root at the compound junction.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `boundary-mark`: former README of `spelling-coverage-compound-junction-boundary-mark`

### spelling-coverage-compound-junction-boundary-mark

The compound boundary is written as the code `é`, a letter that decomposes to a base plus a combining mark.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
