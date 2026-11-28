# compound-allomorph-identity

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `plain` | `edge-cases/compound-allomorph-identity` | 2 cells in one grammar, each with its own rules and words. `plain`: one lexical entry with two root allomorphs under a copy/copy compounding rule, so reusing one allomorph and using both give different identities; `separated`: A prefix on the non-head side of a compound, so the same root recurs with another morpheme between. | unchanged |
| `distinct-entries` | `edge-cases/compound-allomorph-identity-distinct-entries` | 2 cells in one grammar, each with its own rules and words. `distinct-entries`: two entries and two endocompounding rules, one head-first and one non-head-first, covering distinct roots in each order and ambiguity; `same-spelling`: one entry whose two allomorphs spell the same string under compounding, so every pairing is a distinct derivation. | `a`→`f`, `b`→`g`, `d`→`h`, `p`→`j` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-7). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `plain`: former README of `compound-allomorph-identity`

### compound-allomorph-identity

One lexical entry with two root allomorphs under a copy/copy compounding rule, with and without a prefix rule that can separate a repeated root. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

#### Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `plain` | `edge-cases/compound-allomorph-identity` | One lexical entry with two root allomorphs under a copy/copy compounding rule, so reusing one allomorph and using both give different identities. | unchanged |
| `separated` | `edge-cases/compound-allomorph-identity-separated` | A prefix on the non-head side of a compound, so the same root recurs with another morpheme between. | `a`→`b`, `p`→`d` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

#### Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

##### Cell `plain`: former README of `compound-allomorph-identity`

##### Two allomorphs of one entry under ordinary compounding

One lexical entry has two root allomorphs and a copy/copy non-recursive compounding rule. Reusing one allomorph (`aa`, `pp`) is the single identity `[m]`; using both (`ap`, `pa`) is `[m, m]`. The structural neighbors (`aaa`, an explicit boundary) are rejected.

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

##### Cell `separated`: former README of `compound-allomorph-identity-separated`

##### A repeated root separated by a prefix

A prefix rule that inserts a segment on the non-head side of a compound, so the same root recurs with another morpheme between.

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `distinct-entries`: former README of `compound-allomorph-identity-distinct-entries`

### compound-allomorph-identity-distinct-entries

Compounding over lexical entries only: two entries under two endocompounding rules, and one entry whose two allomorphs have the same spelling. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

#### Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `distinct-entries` | `edge-cases/compound-allomorph-identity-distinct-entries` | Two entries and two endocompounding rules, one head-first and one non-head-first, covering distinct roots in each order and ambiguity. | unchanged |
| `same-spelling` | `edge-cases/compound-allomorph-identity-same-spelling` | One entry whose two allomorphs spell the same string under compounding, so every pairing is a distinct derivation. | `a`→`b`, `p`→`d` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

#### Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

##### Cell `distinct-entries`: former README of `compound-allomorph-identity-distinct-entries`

##### Distinct entries and both head positions

Two entries (one with two allomorphs, one with a two-segment allomorph) and two endocompounding rules, `cr1` with the head first and `cr2` with the non-head first. Covers distinct roots in each order, a root equal in spelling to a compound, and ambiguity (`ppp`, `pp`).

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

##### Cell `same-spelling`: former README of `compound-allomorph-identity-same-spelling`

##### Two allomorphs with identical spelling

One entry whose two allomorphs spell the same string under compounding, so every pairing is a distinct derivation: two occurrences of the single identity and two of the two-occurrence identity for the doubled word.

Synthetic forms. Source: sillsdev/PanGloss pull request 353. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
