# mpr-wide-inflection-classes

Ten families of 30 inflection classes (300 features) plus exception features, so one grammar carries 303 MPR features. Each family has a parent class and 29 children; rules block or admit by class, by family and by an exception feature.

The compounding rule `compound` restricts its head and non-head MPR features but does not set an output MPR restriction: the staged copy also set `outputProdRestrictionsMprFeatures`, which `HCLoader.cs` never writes (cannot-say row 10), so it is removed here and the one word that depended on it (`balabalamu`) is re-pinned to what C# returns.

Synthetic forms. Source: sillsdev/PanGloss pull request 340. The expected rows are what C# HermitCrab (sillsdev/machine `1ddef2bd2f1503717de95556116df8e4a63846d6`, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a fresh `hc-conformance --propose` run over this grammar and word list; none is copied from PanGloss's staged copy.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.

- `LoadCharacterDefinitionTable` writes the segments and their spellings.
- `LoadRootAllomorph` writes each root's allomorph.
- `LoadEndoCompoundingRule` writes each compounding rule as one subrule, so the 1 rule here is an endocompound with the `+` boundary between the stems, the output the loader writes (1952-1961).
- `LoadInflAffixProcessRule`, `LoadDerivAffixProcessRule` and `LoadFormAffixProcessAllomorph` write the affix rules and their allomorphs.
- `LoadAffixTemplate` writes the affix template and its slots.
- `LoadLanguage` (181-205) builds the MPR feature groups, with `LoadInflClassMprFeature` writing the inflection classes; here `inflClasses` holds 300 features, `exceptionFeatures` holds exA, exB, `lexEntryInflTypes` holds variant; compounding production restrictions come from `exceptionFeatures` and a compound's output MPR feature from `inflClasses`.
