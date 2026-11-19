# spelling-coverage-compound-orders-asymmetric

A compounding grammar over partial-feature segments and aliases, so the character table has no single spelling per segment. The words are the strings over the grammar's symbols; the rows are what C# HermitCrab accepts as compounds. The set pins which spellings, orders and boundaries count as a route.

Two endocompounding rules, one head-first and one non-head-first, whose head and non-head MPR licences differ. C# accepts only the head-first order here.

Source: sillsdev/PanGloss pull request 354. The expected rows are what C# HermitCrab (sillsdev/machine `1ddef2bd2f1503717de95556116df8e4a63846d6`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each joining the stems with no `+` between them. The loader writes a `+` there (see "What producible does not cover" in docs/fieldworks-cannot-say.md), so the boundary is left out of this grammar.
- `LoadLanguage` (181-205) builds the MPR feature groups, with `LoadInflClassMprFeature` writing the inflection classes; here `exceptionFeatures` holds m1, m2; compounding production restrictions come from `exceptionFeatures` and a compound's output MPR feature from `inflClasses`.
