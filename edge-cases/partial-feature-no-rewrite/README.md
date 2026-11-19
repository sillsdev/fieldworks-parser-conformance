# partial-feature-no-rewrite

Words over a small rewrite grammar. Each row is what C# HermitCrab returns: the output spellings of the rewrite parse to the root, and the unchanged root does not surface. The set pins that a spelling-based shortcut must keep every spelling and every root identity.

Deleting all phonological rules still leaves two C# root identities on aka. No parser algorithm change is requested.

Expectations are the observed C# signatures, not hand-derived. This retains the original loader-shape producibility claim.

Source: sillsdev/PanGloss pull request 339. The expected rows are what C# HermitCrab (sillsdev/machine `1ddef2bd2f1503717de95556116df8e4a63846d6`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
