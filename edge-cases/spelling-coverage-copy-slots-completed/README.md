# spelling-coverage-copy-slots-completed

Root aliases, compatible distinct definitions, prefix and suffix insertion, an optional final slot and copied underlying nodes with independently chosen spellings; this variant has the root definition's omitted second feature filled with minus.

The suffix rule `SUF` applies once (`multipleApplication="1"`). The staged copy asked for two applications, which `HCLoader.cs` never writes for a morphological rule (cannot-say row 22), so the repeated-suffix words are rewritten to what C# returns for a single application; two words (`ass`, `pass`) differ from the staged rows because of that. Structural neighbors stay rejected.

Synthetic forms. Source: sillsdev/PanGloss pull request 350. The expected rows are what C# HermitCrab (sillsdev/machine `1ddef2bd2f1503717de95556116df8e4a63846d6`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadAffixTemplate` writes the affix template and its slots.
