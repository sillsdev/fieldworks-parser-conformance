# spelling-coverage-compound-multirule-affixes

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label. Each cell has its own boundary definition: the boundary character of every cell after the first is mapped like a letter (the map column), because two cells cannot share a boundary spelling that appears in signatures. A character the cell tests (a quote, a combining mark, a Thai mark) is never mapped.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `affixes` | `edge-cases/spelling-coverage-compound-multirule-affixes` | two compounding rules, a free prefix and a free suffix. | unchanged |
| `multirule` | `edge-cases/spelling-coverage-compound-multirule` | Two compounding rules that each write a `+` boundary, one head-first and one non-head-first, with both orders in the same stratum. | `a`→`b`, `e`→`d`, `i`→`f`, `p`→`g`, `s`→`h`, `x`→`j`, `y`→`k`, `á`→`l`, `+`→`~` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-6). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `affixes`: former README of `spelling-coverage-compound-multirule-affixes`

### spelling-coverage-compound-multirule-affixes

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. The two compounding rules of `multirule` (head-first `cr1` and non-head-first `cr2`) together with the free prefix `PRE` (writes `s`) and suffix `SUF` (writes `i`).

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `multirule`: former README of `spelling-coverage-compound-multirule`

### spelling-coverage-compound-multirule

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. Two compounding rules in one stratum: `cr1` joins head then non-head with a null boundary insertion (`^0`), `cr2` joins non-head then head. The stem cap is the default of two.

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
