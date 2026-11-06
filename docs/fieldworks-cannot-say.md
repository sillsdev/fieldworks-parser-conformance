# What FieldWorks can produce, and what it cannot

The suite holds only grammars a real FieldWorks project can produce. This page states the rule and the
standard of evidence, then lists every construct the XML can say and FieldWorks cannot.

**The one rule: the suite holds only what a real FieldWorks project can produce.** FieldWorks never
authors HermitCrab XML; it builds a grammar from a LibLCM project through `HCLoader.cs`, and that
loader reaches less than the XML can say. A grammar that needs something the loader never writes does
not belong here, however expressible it is in the XML and however well an engine handles it. Every
fixture records the verdict as `fieldworks_producible: true` in its `words.yaml`. The constructs left
out, why FieldWorks cannot write each one, and the 23 fixtures removed for using them are in
[what the XML can say but FieldWorks cannot, so we do not test it](#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it).
[`grammars.md`](grammars.md) lists every grammar that remains.

**The standard is the round trip.** "Producible" means a real FieldWorks project round-trips to the grammar: a
project built in FieldWorks (LibLCM), put through `HCLoader.cs`, yields the fixture's `grammar.xml`. That the
loader source could write a construct is weaker evidence. Until a fixture has a FieldWorks witness (a
`fieldworks/` directory, [PROTOCOL.md](../PROTOCOL.md) section 10), its `fieldworks_producible: true` is a claim
read from the loader. Only the 10 fixtures that carry a witness are certified today (all under `edge-cases/`);
the other 128 of the 138 fixtures rest on the loader reading alone.

## What the XML can say but FieldWorks cannot, so we do not test it

The suite keeps only grammars a real FieldWorks project can produce (see the rule at the top). The
constructs below are valid in `HermitCrabInput.dtd`, and the engine implements them except where a row
says otherwise, but `HCLoader.cs` never writes them. No FieldWorks project can reach them, so a fixture
that needs one would test the engine against input FieldWorks never sends, and the suite does not pin
them. Do not author a fixture for any of them. The `todo` lines in `semantic-coverage-baseline.txt` (from sillsdev/machine#480) for
`Family`, `RealizationalRule`, `CharacterDefinitionTable/isActive/no`,
`MorphologicalPhonologicalRuleFeatureGroup/outputType/append`, `isCliticRule`, `ExcludedEnvironments`,
`blockable/false`, the foot-feature elements and `HeadRequiredHeadFeatures` and
`NonHeadRequiredHeadFeatures` name constructs in this table; leave them `todo`.

This is a different list from the surfaces that no engine reads at all (the semantic-coverage ledgers tracked eleven of those).
These the engine does read, and FieldWorks never writes. Subcategorization (row 17) and row 18 are read by no
engine path either.

**Where this was checked.** FieldWorks commit `620cd9903f46941ee85947615dba15c8888c8e7a`,
`Src/LexText/ParserCore/HCLoader.cs`, which was last changed by
`6b8a75287221a1b5ab6d15d6f6eedc117690ef98`; LibLCM commit `d564a719b1cce16c25ebea53a537393cb757f5d1`.
The line numbers below are for that file. `fieldworks-producibility.tsv` and its generator (from sillsdev/machine#480, not in this repository) were written
against an earlier revision, so their line numbers are stale; their verdicts are unchanged. The
protocol's section 9 holds the rule that applies these to a fixture.

| # | Construct | Why FieldWorks cannot produce it (`HCLoader.cs`) | Deleted fixtures |
|---|---|---|---|
| 1 | More than one `CharacterDefinitionTable`, or a `characterDefinitionTable` on `Segments`/`InsertSegments` (producibility rows `InsertSegments.characterDefinitionTable`, `Segments.characterDefinitionTable`) | `LoadLanguage` calls `LoadCharacterDefinitionTable` once, with `PhonemeSetsOS[0]` (217). Every stratum is built from the one `m_table` (240, 243, 246, `CreateStrata` 387), and `Segments()` (2880) reads it. | 9 |
| 2 | `SymbolicFeature.defaultSymbol` | `LoadFeatureSystem` (2699) reads names and symbols and sets no default; the file never mentions a default symbol. | 6 |
| 3 | `RealizationalRule` | `LoadInflAffixProcessRule` (1025) carries `// TODO: use realizational affix process rules` (1027); the loader builds no realizational rule. | 2 |
| 4 | A custom-named or append-mode `MorphologicalPhonologicalRuleFeatureGroup` | `LoadLanguage` builds exactly three groups: `inflClasses` (181), `exceptionFeatures` (192) and `lexEntryInflTypes` (201). | 3 |
| 5 | A metathesis whose `leftSwitch` names the earlier group (producibility row `MetathesisSwitchPositionInversion`) | `LoadMetathesisRule` (2152) sets `LeftSwitchName = "r"` and `RightSwitchName = "l"` (2171-2172) and names the groups from the structural-change indices (2183-2186). The inverted order is unreachable from the editor: `MetaRuleFormulaControl.GetNextCell` (212-226) orders the cells left environment, left switch, right switch, right environment. LibLCM stores the indices as free text (`GetStrucChangeIndices`, `OverridesLing_Lex.cs:7775`), so this is an editor guarantee, not a data-model one. | 1 |
| 6 | `morphologicalRuleOrder="linear"` that changes a parse (producibility row `morphologicalRuleOrder`) | Every stratum that holds rules is built `Unordered`: `Morphology` (240), `Clitics` (243), each custom stratum (387). The `Surface` stratum (246) keeps the default `Linear` but holds no rule. A `linear` stratum with no listed morphological rule and no active affix template is harmless and stays allowed. | none (seven fixtures were rewritten to `unordered`, and `feature-gating-breadth` was restored without its three order-dependent words) |
| 7 | `isActive="no"` on a kind the loader does not filter, and a second `PhonologicalFeatureSystem` | The loader filters `Disabled` compound rules (254), affix templates (308), phonological rules (315) and ad hoc prohibitions (355, 361), and skips an `IsAbstract` allomorph form (`IsValidRuleForm` 549 at 556, `IsValidLexEntryForm` 592 at 598). It reads no inactive state for features, feature values, natural classes, lexical entries, strata, character tables or `Properties`, and `LoadFeatureSystem` is called once for the phonological feature system (211). | 3 |
| 8 | `LexicalEntry.family` | The file never reads a family. | 1 |
| 9 | Obligatory output features: `CompoundingRule.outputObligatoryFeatures`, `MorphologicalRule.outputObligatoryFeatures`, `LexicalEntry.obligatoryHeadFeatures`, `LexicalEntry.obligatoryFootFeatures`, and the `ObligatorySyntacticFeatures` failure reason | The file never mentions an obligatory feature. The engine reads `outputObligatoryFeatures` (`XmlLanguageLoader` 898, 1229) but never `obligatoryHeadFeatures` or `obligatoryFootFeatures`, which are engine-dead. | 1 |
| 10 | Head-input MPR features on a compound (`HeadMorphologicalInput.requiredMPRFeatures`, `.excludedMPRFeatures`) and `CompoundingRule.outputProdRestrictionsMprFeatures` | `LoadEndoCompoundingRule` (1891) sets only `OutMprFeatures` (1950) and the head and non-head production restrictions; `LoadExoCompoundingRule` (1971) sets `OutMprFeatures` at 2011 and 2038. Nothing sets head-input MPR features or an output production restriction. | 1 |
| 11 | MPR output (`MPRFeatures`) from a template-slot rule | A rule reached through an `AffixTemplate` slot is inflectional. `LoadInflAffixProcessRule` (1025) sets `RequiredMprFeatures` (1050) but never `OutMprFeatures`; only `LoadDerivAffixProcessRule` (975) does (1018). | 1 |
| 12 | Different `requiredMPRFeatures` on the subrules of one non-inflectional rule | `LoadDerivAffixProcessRule` adds one per-MSA list to every allomorph (1017); `LoadUnclassifiedAffixProcessRule` (1057) adds none. An inflectional rule also adds each allomorph's inflection classes (1118, 1145, 1172), so its subrules may differ. | none |
| 13 | `MorphemeCoOccurrenceRule` or `AllomorphCoOccurrenceRule` with `type="require"` | `LoadAllomorphCoOccurrenceRules` (2212) builds `ConstraintType.Exclude` (2232) and `LoadMorphemeCoOccurrenceRules` (2262) builds it at 2282. | none (one language was rewritten) |
| 14 | A `RequiredEnvironments` the loader has no site for: on an infix, a reduplication or a multi-action process rule, a left environment on a suffix, or a right environment on a prefix | `.Environments.Add` appears only in `LoadRootAllomorph` (870), `LoadCircumfixAffixProcessAllomorph` (1371) and `LoadFormAffixProcessAllomorph` (1626, 1653). The circumfix site writes one `Require` environment on a prefix-plus-suffix output, left from the prefix's context and right from the suffix's, so one environment on a circumfix is producible. The suffix site writes only a right environment (1626) and the prefix site only a left one (1653); the other side becomes part of the input pattern (1604-1619, 1632-1646). The infix and reduplication branches and `LoadAffixProcessAllomorph` (1383-1488), the path for a multi-action output, never touch environments. | none |
| 15 | `isCliticRule` | The loader never sets it. A rule is a clitic only because `LoadCliticAffixProcessRule` (1079) places it in the stratum named `Clitics` (243). | none (three fixtures were rewritten) |
| 16 | A slot rule with `outputPartOfSpeech`; a partial stem entry that has a part of speech; a partial rule inside a slot or with `outputPartOfSpeech` | `LoadInflAffixProcessRule` sets no output part of speech. `IsPartial` is set on an entry only when it has no part of speech (`LoadLexEntry` 757, `LoadLexEntryOfVariant` 817), and on a rule only when it has no slot (1031) or is unclassified (`LoadUnclassifiedAffixProcessRule` 1062, which a slot cannot hold). sillsdev/machine's `FieldWorksProducibleShapeTests` enforces these. | none (many were rewritten) |
| 17 | Syntactic subcategorization: the nine producibility rows `AffixTemplate.requiredSubcategorizedRules`, `CompoundingRule.headSubcategorizedRules`, `.nonHeadSubcategorizedRules`, `.outputSubcategorization`, `LexicalEntry.subcategorizations`, `MorphologicalRule.outputSubcategorization`, `.requiredSubcategorizedRules` and the two `OutputSubcategorizationOverride` attributes | The file never mentions subcategorization. The engine reads none of it either, so these are also among the surfaces no engine reads. | none |
| 18 | `LexicalEntry.morphologicalRules` | Never loaded; the engine does not read it either. | none |
| 19 | Foot features: `FootFeatures`, `AssignedFootFeatures`, `RequiredFootFeatures`, `OutputFootFeatures`, `HeadRequiredFootFeatures` and `NonHeadRequiredFootFeatures` | `LoadLanguage` adds only the head feature (`AddHeadFeature` 208) and never `AddFootFeature`; the file does not mention a foot feature. Every syntactic feature structure the loader builds is stored under the head feature (226, 759, 983, 991, 1038, 1175, 1826). | none (`feature-gating-breadth` and `suffixing-extension-slot-ordering` were rewritten) |
| 20 | `ExcludedEnvironments` on an allomorph | Every `AllomorphEnvironment` the loader builds is `ConstraintType.Require` (870, 1371, 1626, 1653); the file builds no `Exclude` environment. | 1 |
| 21 | `blockable="false"` on a `MorphologicalRule` or a `CompoundingRule` | The loader never sets `Blockable`, so it keeps the engine default `true`. (A `RealizationalRule` is row 3.) | none |
| 22 | `multipleApplication` other than 1 on a `MorphologicalRule` | `MaxApplicationCount` is assigned once, in `LoadEndoCompoundingRule` (1943-1945), from the `CompoundRules` `maxApps` entry of the parser parameters (116-124). No `AffixProcessRule` is given a cap, so every morphological rule keeps the engine default of 1. | none (two attributes in `morphotactic-attribute-breadth` were rewritten) |
| 23 | A compound-rule cap of 0, or above 9 | The Parser Parameters dialog (`HCMaxCompoundRulesDlg.ValidateValues`, `EnforceValidValue(rule, "MaxApps", 1, 9, true)`) accepts 1 to 9. `LoadExoCompoundingRule` (1971) never reads the entry, so an exocompound keeps 1, and a cap on either half of an exocompound pair is unproducible. A cap of 2 to 9 changes a parse only for a recursive endocentric rule with `MaxRoots` (user-set, 1 to 10, default 2) of 3 or more: `edge-cases/compound-max-applications`. | none (`compounding-breadth` lost one rule; row 24 cost it two more words) |
| 24 | `HeadRequiredHeadFeatures` or `NonHeadRequiredHeadFeatures` on a `CompoundingRule` | `LoadEndoCompoundingRule` (1891) builds the head and non-head required structures from the part of speech alone (1899-1921), and `LoadExoCompoundingRule` (1971) does the same (1973-1981). No compound rule reads a head feature of the word it joins, so a compound cannot select a root by its head features. The output is the part of speech alone as well (1923-1924, 1982-1983), so `OutputHeadFeatures` on a compound is unproducible too. | 2 words (`compounding-breadth`: `kaki`, `kutu`) |
| 25 | A stem name whose region is empty | `LoadLanguage` keeps only the regions that are not empty (`stemName.RegionsOC.Where(fs => !fs.IsEmpty)`, 223) and adds the stem name only when one is left (228). An empty `Region` therefore matches every word of its part of speech in the XML and matches nothing in FieldWorks. | none (`suffixing-extension-slot-ordering` gave `snG5` a region) |
| 26 | `OutputHeadFeatures`, `outputObligatoryFeatures` and `requiredStemName` on a template-slot rule | `LoadInflAffixProcessRule` (1025) sets the required part of speech (1035-1036), the required head features from the inflection features (1037-1038) and the required production restrictions, and nothing else: no output feature structure, no stem name. Only `LoadDerivAffixProcessRule` sets `OutputSyntacticFeatureStruct` (990-991) and `RequiredStemName` (1009-1011). Output MPR is row 11. | none (`final-template-partial-trace` was rewritten) |
| 27 | An MPR feature outside the three loader groups; an excluded MPR feature on anything but a slot rule's inflection-type feature; an inflection-type feature that a rule requires or writes; more than one inflection class on an entry or an output | `LoadLanguage` puts every MPR feature in `inflClasses`, `exceptionFeatures` or `lexEntryInflTypes` (181-205). A slot rule's `ExcludedMprFeatures` come only from the irregular inflection types of its slot (1766), and only a variant entry carries such a feature (`LoadLexEntryOfVariant` 796). A derivational affix writes one inflection class and the production restrictions (1015-1018), an entry has one inflection class (745-751), and a compound writes one (1950, 2011, 2038). | 3 words (`morphotactic-attribute-breadth`: `topdori`, `topdo`, `topri`) |

Rows 1 to 6, 8, 9, 10, 17 and 18 cover the 26 `No` rows of `fieldworks-producibility.tsv` (row 17
holds nine, row 9 five, row 10 three, row 1 two, and rows 2 to 6, 8 and 18 one each). Rows 7, 11 to 16 and 19 to 27
are shapes that no per-attribute row can express: the usage-level and mechanical checks of the protocol's
section 9 and the retirement record's list of what the suite no longer covers. Fixtures were deleted for
rows 1 to 5, 7 to 11 and 20; rows 6, 12 to 16, 19 and 21 to 27 cost no fixture, though rows 24 and 27 cost
words.

`fieldworks-writable-shapes.tsv` is the census behind rows 11 to 27: for each rule kind (slot rule, unslotted
partial rule, derivational rule, clitic rule, compounding rule, template, slot, stratum, stem name, lexical
entry, root allomorph, phonological and metathesis rules, co-occurrence rules) it says per DTD attribute and
element whether `HCLoader.cs` writes it, with the line. sillsdev/machine's `FieldWorksProducibleShapeTests` reads it and fails
a flagged fixture that uses a member the table calls `never` or does not list, so a new construct must be
added to the table with a loader line before a flagged fixture may use it. The conditions a row cannot say
(rows 14, 16 and 25 to 27, and a cap on an exocompound) are checked in that project's `FieldWorksWritableShapes`.

**What "producible" does not cover: the `+` boundary.** The flag and the census above are about which
members and environments a grammar uses, not about each output byte for byte. `HCLoader.cs` puts a `+`
morpheme boundary on the inside edge of every affix form and between the two parts of a compound (prefix
1358 and 1649, suffix 1360 and 1623, circumfix 1597, reduplication 1506, 1549 and 1564, compounds 1871,
1884, 1956, 2017 and 2044); the loader's table always has it (2761). A grammar file can write that boundary
only if it defines one, and 16 of the 138 grammars do. Most fixtures write their affix and compound outputs without the boundary, and the
effect of that on a parse is not measured. A claim that an output is "written as HCLoader writes it" is
therefore made only where the output carries the boundary, as in the circumfix of
`languages/suffixing-vowel-harmony`.

The 23 fixtures removed for these constructs, each mapped to the construct that disqualified it, are in
[`docs/engine-only-fixture-retirement.md`](engine-only-fixture-retirement.md).
