# partial-feature-literal-output

Words over a small rewrite grammar. Each row is what C# HermitCrab returns: the output spellings of the rewrite parse to the root, and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

Singleton class targets/outputs or a literal output do not certify a scalar rewrite relation.

The length neighbor is an independent negative control. Ordinary rewrite shapes and partial feature inventories retain the existing loader-based producibility claim.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadRewriteRule` writes the phonological rule.
