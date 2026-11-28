# spelling-coverage-compound-allomorphs

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 5 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `allomorphs` | `edge-cases/spelling-coverage-compound-allomorphs` | One entry with two root allomorphs under ordinary head-then-non-head compounding. | unchanged |
| `alias-deleted` | `edge-cases/spelling-coverage-compound-alias-deleted` | The aliased segment loses one alias; words using it are an invalid shape in C# and the remaining aliases still spell every stem. | `a`→`b`, `e`→`d`, `i`→`f`, `p`→`g`, `s`→`h`, `x`→`j`, `y`→`k`, `á`→`l` |
| `completed` | `edge-cases/spelling-coverage-compound-completed` | The aliased segment is given a complete feature bundle, so it no longer unifies with the vowels; C# rejects the compounds that depended on it. | `a`→`m`, `e`→`n`, `i`→`o`, `p`→`q`, `s`→`r`, `x`→`v`, `y`→`w`, `á`→`z` |
| `repeated-root` | `edge-cases/spelling-coverage-compound-repeated-root` | Two-node self-compounds of one root are accepted and structural neighbors are rejected. | `a`→`à`, `e`→`â`, `i`→`ã`, `p`→`ä`, `s`→`å`, `x`→`æ`, `y`→`ç`, `á`→`è` |
| `reversed-table` | `edge-cases/spelling-coverage-compound-reversed-table` | The repeated-root compound with the character table's segment definitions declared in reverse order. | `a`→`é`, `e`→`ê`, `i`→`ë`, `p`→`ì`, `s`→`í`, `x`→`î`, `y`→`ï`, `á`→`ð` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-6). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `allomorphs`: former README of `spelling-coverage-compound-allomorphs`

### spelling-coverage-compound-allomorphs

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

One entry with two root allomorphs under ordinary head-then-non-head compounding. Reusing one allomorph and mixing both are both accepted; the aliases of the aliased segment spell each stem.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

### Cell `alias-deleted`: former README of `spelling-coverage-compound-alias-deleted`

### spelling-coverage-compound-alias-deleted

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

The aliased segment loses one alias; words using it are an invalid shape in C# and the remaining aliases still spell every stem.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

### Cell `completed`: former README of `spelling-coverage-compound-completed`

### spelling-coverage-compound-completed

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

The aliased segment is given a complete feature bundle, so it no longer unifies with the vowels; C# rejects the compounds that depended on it.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

### Cell `repeated-root`: former README of `spelling-coverage-compound-repeated-root`

### Repeated-root compound spelling control

Two-node self-compounds of one root are accepted and structural neighbors are rejected.

Synthetic forms. Source: sillsdev/PanGloss pull request 350. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

### Cell `reversed-table`: former README of `spelling-coverage-compound-reversed-table`

### spelling-coverage-compound-reversed-table

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

The repeated-root compound with the character table's segment definitions declared in reverse order.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
