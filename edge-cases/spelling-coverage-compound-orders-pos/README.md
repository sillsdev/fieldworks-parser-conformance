# spelling-coverage-compound-orders-pos

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `pos` | `edge-cases/spelling-coverage-compound-orders-pos` | Two endocompounding rules, one head-first and one non-head-first, restricted by head and non-head part of speech. | unchanged |
| `orders` | `edge-cases/spelling-coverage-compound-orders` | Two endocompounding rules, one head-first and one non-head-first, both stems licensed by the same MPR feature, plus a third entry outside the licence. | `a`→`b`, `e`→`d`, `i`→`f`, `p`→`g`, `s`→`h`, `x`→`j`, `y`→`k`, `á`→`l` |
| `asymmetric` | `edge-cases/spelling-coverage-compound-orders-asymmetric` | Two endocompounding rules, one head-first and one non-head-first, whose head and non-head MPR licences differ. C# accepts only the head-first order here. | `a`→`m`, `e`→`n`, `i`→`o`, `p`→`q`, `s`→`r`, `x`→`v`, `y`→`w`, `á`→`z` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-10). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `pos`: former README of `spelling-coverage-compound-orders-pos`

### spelling-coverage-compound-orders-pos

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

Two endocompounding rules, one head-first and one non-head-first, restricted by head and non-head part of speech.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.

### Cell `orders`: former README of `spelling-coverage-compound-orders`

### spelling-coverage-compound-orders

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

Two endocompounding rules, `cr1` with the head first and `cr2` with the non-head first, both stems licensed by the same MPR feature, plus a third entry outside the licence. C# accepts both stem orders for the licensed pair and rejects every word containing the unlicensed entry.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadLanguage` (181-205) builds the MPR feature groups, with `LoadInflClassMprFeature` writing the inflection classes; here `exceptionFeatures` holds m1, m2; compounding production restrictions come from `exceptionFeatures` and a compound's output MPR feature from `inflClasses`.

### Cell `asymmetric`: former README of `spelling-coverage-compound-orders-asymmetric`

### spelling-coverage-compound-orders-asymmetric

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

Two endocompounding rules, one head-first and one non-head-first, whose head and non-head MPR licences differ. C# accepts only the head-first order here.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadLanguage` (181-205) builds the MPR feature groups, with `LoadInflClassMprFeature` writing the inflection classes; here `exceptionFeatures` holds m1, m2; compounding production restrictions come from `exceptionFeatures` and a compound's output MPR feature from `inflClasses`.
