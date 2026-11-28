# compound-allomorph-identity

One lexical entry with two root allomorphs under a copy/copy compounding rule, with and without a prefix rule that can separate a repeated root. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `plain` | `edge-cases/compound-allomorph-identity` | One lexical entry with two root allomorphs under a copy/copy compounding rule, so reusing one allomorph and using both give different identities. | unchanged |
| `separated` | `edge-cases/compound-allomorph-identity-separated` | A prefix on the non-head side of a compound, so the same root recurs with another morpheme between. | `a`→`b`, `p`→`d` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `plain`: former README of `compound-allomorph-identity`

### Two allomorphs of one entry under ordinary compounding

One lexical entry has two root allomorphs and a copy/copy non-recursive compounding rule. Reusing one allomorph (`aa`, `pp`) is the single identity `[m]`; using both (`ap`, `pa`) is `[m, m]`. The structural neighbors (`aaa`, an explicit boundary) are rejected.

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

### Cell `separated`: former README of `compound-allomorph-identity-separated`

### A repeated root separated by a prefix

A prefix rule that inserts a segment on the non-head side of a compound, so the same root recurs with another morpheme between.

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
