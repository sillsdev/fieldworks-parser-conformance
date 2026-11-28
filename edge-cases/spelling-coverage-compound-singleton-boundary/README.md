# spelling-coverage-compound-singleton-boundary

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label. Each cell has its own boundary definition: the boundary character of every cell after the first is mapped like a letter (the map column), because two cells cannot share a boundary spelling that appears in signatures. A character the cell tests (a quote, a combining mark, a Thai mark) is never mapped.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `singleton-boundary` | `edge-cases/spelling-coverage-compound-singleton-boundary` | 4 cells in one grammar, each with its own rules and words. `boundary`: at two stems, the literal `+` boundary is typed in accepted compounds of single-segment roots; `quote-boundary`: A literal double quote is a spelling of the `+` boundary used by both compounding rules; `thai-mark`: thai mai ek (U+0E48), a combining mark, is listed as a segment and starts a root; `merging-mark`: A segment U+0301 (a combining acute) follows a root, and neither compounding rule writes a boundary at the junction. | unchanged |
| `boundary` | `edge-cases/spelling-coverage-compound-boundary` | The compound inserts a `+` morpheme boundary between the stems, as the loader writes it; the boundary may also be declared explicitly in the character table (the same grammar), and a doubled boundary is not a route. | `a`→`r`, `e`→`v`, `i`→`w`, `p`→`z`, `s`→`à`, `x`→`â`, `y`→`ã`, `á`→`ä`, `+`→`&` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-7). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `singleton-boundary`: former README of `spelling-coverage-compound-singleton-boundary`

### spelling-coverage-compound-singleton-boundary

Compounds of single-segment roots at two stems, where the character table holds an unusual character. The cells differ in that character: the literal `+` boundary, a double quote as a boundary spelling, a Thai combining mark as a segment, and a combining acute as a segment. This test case holds all 4 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

#### Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label. Each cell has its own boundary definition: the boundary character of every cell after the first is mapped like a letter (the map column), because two cells cannot share a boundary spelling that appears in signatures. A character the cell tests (a quote, a combining mark, a Thai mark) is never mapped. `MaxRoots: 2` is the setting of every cell.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `boundary` | `edge-cases/spelling-coverage-compound-singleton-boundary` | At two stems, the literal `+` boundary is typed in accepted compounds of single-segment roots. | unchanged |
| `quote-boundary` | `edge-cases/spelling-coverage-compound-singleton-quote-boundary` | A literal double quote is a spelling of the `+` boundary used by both compounding rules. | `a`→`b`, `p`→`d`, `s`→`f`, `t`→`g`, `+`→`~` |
| `thai-mark` | `edge-cases/spelling-coverage-compound-singleton-thai-mark` | Thai mai ek (U+0E48), a combining mark, is listed as a segment and starts a root. | `a`→`h`, `p`→`j`, `s`→`k`, `t`→`l`, `+`→`#` |
| `merging-mark` | `edge-cases/spelling-coverage-compound-singleton-merging-mark` | A segment U+0301 (a combining acute) follows a root, and neither compounding rule writes a boundary at the junction. | `a`→`m`, `p`→`n`, `s`→`o`, `t`→`q`, `+`→`%` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

#### Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

##### Cell `boundary`: former README of `spelling-coverage-compound-singleton-boundary`

##### spelling-coverage-compound-singleton-boundary

At two stems, the literal `+` boundary is typed in accepted compounds of single-segment roots.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

##### Cell `quote-boundary`: former README of `spelling-coverage-compound-singleton-quote-boundary`

##### spelling-coverage-compound-singleton-quote-boundary

A literal double quote is a spelling of the `+` boundary used by both compounding rules.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

##### Cell `thai-mark`: former README of `spelling-coverage-compound-singleton-thai-mark`

##### spelling-coverage-compound-singleton-thai-mark

Thai mai ek (U+0E48), a combining mark, is listed as a segment and starts a root.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

##### Cell `merging-mark`: former README of `spelling-coverage-compound-singleton-merging-mark`

##### spelling-coverage-compound-singleton-merging-mark

A segment U+0301 (a combining acute) follows a root, and neither compounding rule writes a boundary at the junction.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `boundary`: former README of `spelling-coverage-compound-boundary`

### spelling-coverage-compound-boundary

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

The compound inserts a boundary between the stems. The boundary may appear in the word as its explicit spelling or be omitted; C# accepts both and rejects it anywhere else, including a doubled boundary (`a++a`).

This test case absorbed `spelling-coverage-compound-boundary-explicit`, whose grammar was identical apart from its `<Name>`; its one extra word is `a++a` (see `docs/renames.tsv`).

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound with the `+` boundary between the stems, the output the loader writes (1952-1961).
