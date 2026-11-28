# spelling-coverage-compound-affix-feeds

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 4 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `affix-feeds` | `edge-cases/spelling-coverage-compound-affix-feeds` | one compound and a free prefix and a free suffix in one stratum. | unchanged |
| `affixes` | `edge-cases/spelling-coverage-compound-affixes` | A prefix and a suffix around a compound, with aliased roots and inserted segments; derivations place the affixes before, between and after the stems. | `a`→`b`, `e`→`d`, `i`→`f`, `p`→`g`, `s`→`h`, `x`→`j`, `y`→`k`, `á`→`l` |
| `prefix-feeds` | `edge-cases/spelling-coverage-compound-prefix-feeds` | a compound and a free prefix in one stratum. | `a`→`m`, `e`→`n`, `i`→`o`, `p`→`q`, `s`→`r`, `x`→`v`, `y`→`w`, `á`→`z` |
| `suffix-feeds` | `edge-cases/spelling-coverage-compound-suffix-feeds` | a compound and a free suffix in one stratum. | `a`→`à`, `e`→`â`, `i`→`ã`, `p`→`ä`, `s`→`å`, `x`→`æ`, `y`→`ç`, `á`→`è` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-8). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `affix-feeds`: former README of `spelling-coverage-compound-affix-feeds`

### spelling-coverage-compound-affix-feeds

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. A compound and both a prefix and a suffix rule in one stratum: the compound `cr1` joins head and non-head with nothing inserted, `PRE` writes `s` before a verb and `SUF` writes `i` after one, all in one unordered stratum.

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `affixes`: former README of `spelling-coverage-compound-affixes`

### spelling-coverage-compound-affixes

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

A prefix and a suffix around a compound, with aliased roots and inserted segments; derivations place the affixes before, between and after the stems.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `prefix-feeds`: former README of `spelling-coverage-compound-prefix-feeds`

### spelling-coverage-compound-prefix-feeds

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. One compound `cr1` and one free prefix `PRE` (writes `s` before a verb) in an unordered stratum. The rows show where C# lets the prefix apply relative to the compounding.

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.

### Cell `suffix-feeds`: former README of `spelling-coverage-compound-suffix-feeds`

### spelling-coverage-compound-suffix-feeds

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. One compound `cr1` and one free suffix `SUF` (writes `i` after a verb) in an unordered stratum. The rows show where C# lets the suffix apply relative to the compounding.

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
