# spelling-coverage-compound-suffix-feeds

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. One compound `cr1` and one free suffix `SUF` (writes `i` after a verb) in an unordered stratum. The rows show where C# lets the suffix apply relative to the compounding.

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
