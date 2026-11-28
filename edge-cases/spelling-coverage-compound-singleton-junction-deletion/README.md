# spelling-coverage-compound-singleton-junction-deletion

A compound junction with a boundary of `+` and one phonological rule across or at it. The cells differ in the rule: deletion, epenthesis, feature change, a word-final feature change in the same stratum, metathesis, and a word-final feature change in a root stratum before the compounding stratum. This test case holds all 6 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label. The root-stratum cell keeps its two strata: its inner stratum (its rule and lexical entries) is the first stratum of the merged grammar and holds nothing of another cell; every other cell's rules and entries sit in the last stratum. `MaxRoots: 2` is stated once for the whole test case; two former members did not state it, and 2 is the engine's default.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `deletion` | `edge-cases/spelling-coverage-compound-singleton-junction-deletion` | A deletion rule removes a stem-final segment before a stem-initial segment across a compound junction that writes a boundary. | unchanged |
| `epenthesis` | `edge-cases/spelling-coverage-compound-singleton-junction-epenthesis` | An epenthesis rule inserts a segment between a stem-final and a stem-initial segment across the compound junction. | `a`→`b`, `p`→`d`, `s`→`f`, `t`→`g` |
| `featchange` | `edge-cases/spelling-coverage-compound-singleton-junction-featchange` | A feature-change rule rewrites a stem-final segment before a stem-initial segment across the compound junction. | `a`→`h`, `p`→`j`, `s`→`k`, `t`→`l` |
| `final-change` | `edge-cases/spelling-coverage-compound-singleton-junction-final-change` | A one-node feature change applies only at a word-final anchor, in the same stratum as the compounding rules. | `a`→`m`, `p`→`n`, `s`→`o`, `t`→`q` |
| `metathesis` | `edge-cases/spelling-coverage-compound-singleton-junction-metathesis` | A metathesis rule swaps a stem-final `p` and a stem-initial `t` across a compound junction with no written boundary. | `a`→`r`, `p`→`v`, `s`→`w`, `t`→`x` |
| `root-stratum-final-change` | `edge-cases/spelling-coverage-compound-singleton-junction-root-stratum-final-change` | a word-final one-node feature change in the root stratum, with the compounding rules and lexical entries in a later stratum. | `a`→`z`, `p`→`à`, `s`→`á`, `t`→`â` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-4). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `deletion`: former README of `spelling-coverage-compound-singleton-junction-deletion`

### spelling-coverage-compound-singleton-junction-deletion

A deletion rule removes a stem-final segment before a stem-initial segment across a compound junction that writes a boundary. C# deletes through the junction (`p` is accepted as the compound `Z+Y`).

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadRewriteRule` writes the phonological rule.

### Cell `epenthesis`: former README of `spelling-coverage-compound-singleton-junction-epenthesis`

### spelling-coverage-compound-singleton-junction-epenthesis

An epenthesis rule inserts a segment between a stem-final and a stem-initial segment across the compound junction. C# accepts `tap` and `ta+p` as `Z+Y`.

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadRewriteRule` writes the phonological rule.

### Cell `featchange`: former README of `spelling-coverage-compound-singleton-junction-featchange`

### spelling-coverage-compound-singleton-junction-featchange

A feature-change rule rewrites a stem-final segment before a stem-initial segment across the compound junction. C# accepts the rewritten compound (`sp`, `s+p`, `ssp` as `Z+Y`).

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadRewriteRule` writes the phonological rule.

### Cell `final-change`: former README of `spelling-coverage-compound-singleton-junction-final-change`

### spelling-coverage-compound-singleton-junction-final-change

A one-node feature change applies only at a word-final anchor, in the same stratum as the compounding rules.

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadRewriteRule` writes the phonological rule.

### Cell `metathesis`: former README of `spelling-coverage-compound-singleton-junction-metathesis`

### spelling-coverage-compound-singleton-junction-metathesis

A metathesis rule swaps a stem-final `p` and a stem-initial `t` across a compound junction with no written boundary. C# accepts `tp` as `Z+Y` through the swap.

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

C# at Machine e63b8863 returns four analyses for `tp` (`Z+Y|tp`) and six for `stp` (`PRE+Z+Y|stp`) through the metathesis; `pt` and `spt` are rejected controls, for which C# finds no analysis.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadMetathesisRule` writes the metathesis rule.

### Cell `root-stratum-final-change`: former README of `spelling-coverage-compound-singleton-junction-root-stratum-final-change`

### spelling-coverage-compound-singleton-junction-root-stratum-final-change

A one-node feature change that applies only at a word-final anchor, but the rule belongs to the root stratum and the compounding rules to a later stratum, with lexical entries in both. The compound junction is a word edge for the inner stratum's rule.

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadRewriteRule` writes the phonological rule.
- `CreateStrata` writes the strata.
