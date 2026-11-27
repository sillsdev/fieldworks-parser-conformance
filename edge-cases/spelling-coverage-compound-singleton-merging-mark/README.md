# spelling-coverage-compound-singleton-merging-mark

A segment U+0301 (a combining acute) follows a root, and neither compounding rule writes a boundary at the junction.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70` returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
