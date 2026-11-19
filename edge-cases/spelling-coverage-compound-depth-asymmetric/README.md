# spelling-coverage-compound-depth-asymmetric

The head-first rule licenses different entries on each side. A rule that grows on the left cannot use those entries to hide the asymmetry.

Synthetic roots and compounding rules; MaxRoots is set in `words.yaml` where the row needs it. Source: sillsdev/PanGloss pull request 367. The expected rows are what C# HermitCrab (sillsdev/machine `1ddef2bd2f1503717de95556116df8e4a63846d6`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`, and every compounding rule here is an endocompound (names are unique, so `CheckExocompoundCaps` finds no mirrored pair); no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings (aliases included).
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 2 rules here are separate endocompounds (unique names), each with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadLanguage` (181-205) builds the MPR feature groups, with `LoadInflClassMprFeature` writing the inflection classes; here `exceptionFeatures` holds m1, m2, m3; compounding production restrictions come from `exceptionFeatures` and a compound's output MPR feature from `inflClasses`.
