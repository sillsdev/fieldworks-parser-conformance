# spelling-coverage-compound-singleton-junction-metathesis

A metathesis rule swaps a stem-final `p` and a stem-initial `t` across a compound junction with no written boundary. C# accepts `tp` as `Z+Y` through the swap.

Synthetic roots, two compounding rules `cr1` and `cr2`, and a prefix `PRE` (the last grammar of the group has no compounding rule). The word list is the words C# HermitCrab accepts over the grammar's symbols, with a few rejected controls where a row says so; each row is what C# returns.

C# at Machine e63b8863 returns four analyses for `tp` (`Z+Y|tp`) and six for `stp` (`PRE+Z+Y|stp`) through the metathesis; `pt` and `spt` are rejected controls, for which C# finds no analysis.

Source: sillsdev/PanGloss pull request 376. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadMetathesisRule` writes the metathesis rule.
