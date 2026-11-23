# spelling-coverage-compound-multirule

Synthetic grammar with two verb roots `x` and `y`, aliased vowels and no phonological rules. Two compounding rules in one stratum: `cr1` joins head then non-head with a null boundary insertion (`^0`), `cr2` joins non-head then head. The stem cap is the default of two.

Every word over the grammar's symbols up to the length shown in `words.yaml` is listed, with the analyses C# HermitCrab returns for it (an empty list means no analysis), so the rows pin which spellings parse and how many analyses each gets.

Source: sillsdev/PanGloss pull request 355. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
