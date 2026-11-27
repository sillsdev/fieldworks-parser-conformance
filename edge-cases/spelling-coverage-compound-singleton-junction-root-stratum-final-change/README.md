# spelling-coverage-compound-singleton-junction-root-stratum-final-change

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
