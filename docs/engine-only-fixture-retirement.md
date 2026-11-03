# Engine-only fixture retirement: decision record

**Decision (owner).** The conformance suite keeps only grammars a real FieldWorks project can
produce, that is, fixtures marked `fieldworks_producible: true`. A fixture that needs a construct
`HCLoader.cs` (FieldWorks `ParserCore`) cannot emit tests the engine against input FieldWorks never
sends, so it cannot catch a regression a FieldWorks user would see. Such a fixture is converted
to a producible grammar when that preserves its purpose, and deleted when it does not.
`ConformanceFixtureGateTests.EveryFixtureIsMarkedFieldWorksProducible` enforces the rule.

No fixture is kept engine-only. The constructs the suite does not test, and why FieldWorks cannot write
each one, are in the README section
[what the XML can say but FieldWorks cannot, so we do not test it](../README.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it).
The construct numbers used below are that section's row numbers.

## Result

27 fixtures were deleted. Four were later restored as producible grammars, so 23 stay deleted
(see "Restored" below). 133 fixtures remain (6 `languages/`, 127 `edge-cases/`), every one
`fieldworks_producible: true`; two of them, `edge-cases/compound-max-applications` and
`edge-cases/final-template-partial-trace`, are new. The count comes from `generated/hc-conformance-manifest.v2.json`
(`python3 scripts/generate_manifest.py --check`), not from this page.

## Marked producible without a grammar change

* `edge-cases/final-template-merge-key`: its note named no construct `HCLoader.cs` cannot emit.

## Converted to a producible grammar

Each conversion was re-run against the C# oracle; every remaining expected row is unchanged
except where listed.

* `edge-cases/template-category-sharing`, `edge-cases/final-template-partial-root`,
  `edge-cases/final-template-partial-discriminators`: dropped `outputPartOfSpeech` from slot rules
  (`LoadInflAffixProcessRule` never sets an output part of speech) and, in the two partial
  fixtures, from stratum-level partial rules; removed `partOfSpeech` from the two partial entries
  of `final-template-partial-root` (`LoadLexEntry` sets `IsPartial` only when the MSA has no part
  of speech). No row changed.
* `edge-cases/clitic-rule-designation`, `edge-cases/clitic-flex-layout-blocking-morphology`,
  `edge-cases/non-clitic-after-final-template-layout`: dropped `isCliticRule` (FieldWorks marks a
  clitic only through a stratum named `Clitics`) and the rules and words that depended on the
  non-clitic/clitic contrast, and for the last the Surface-stratum rule. All remaining rows are
  unchanged. These three now pin less than before: the blocking-stratum reset in
  `clitic-flex-layout-blocking-morphology` is no longer observable, and
  `non-clitic-after-final-template-layout` is close to a duplicate of `clitic-rule-designation`.
* `edge-cases/chained-output-feature-override-loss`: `morphologicalRuleOrder` `linear` to
  `unordered` (the loader hardcodes unordered strata). The #504 pin holds: `zudiua` has no parse at
  52d069f8 and parses at 7109531e, for both orders.
* `languages/suffixing-evidential-adjacency-chain`: four `require` co-occurrence rules replaced by
  18 single-other `exclude` rules (the loader builds exclude constraints only; an exclude rule
  with several `otherMorphemes` fires only when all of them co-occur, so "any of" needs one rule
  per morpheme). `siputuku` (first person plural inclusive with no evidential) now parses, because
  an exclude rule cannot refuse the absence of a morpheme. Two negative controls were added,
  `siputukusi` and `sipulupasi`, each shown to parse when the reportative exclude rules are
  removed. The AND-not-OR pin for #311 (`walaknkicha`, blocked by `mrEvidConjectural`) is unchanged.
* The #612 pass over fixtures already marked `true` (no row changed except where listed):
  * Seven fixtures whose `linear` stratum lists morphological rules or holds an affix template now
    say `unordered`, because the engine reads the order for both (`compounding-breadth`,
    `head-ambiguous-compounding`, `recursive-endocentric-compounding`,
    `subrule-morphosyntactic-gating`, `guesser-pattern-root-fallback`,
    `pattern-root-required-environment`, `standalone-combining-mark`); the oracle found no change
    in any word. `morphological-rule-order-measurement.md` (sillsdev/machine#480) has the count.
  * 18 fixtures dropped `outputPartOfSpeech` from every slot rule. No row changed.
  * `edge-cases/morphotactic-attribute-breadth`: the partial stem entry `eNap` lost its part of
    speech, the partial slot rule `mrPartial` became the ordinary suffix `mrMo` (so `kulmo`'s
    signature is `KUL+MO|kulmo`), and the partial stratum rule `mrPO` lost its
    `outputPartOfSpeech`. `napmo` and `pogliti` still pin the two partial flags.
  * `FieldWorksProducibleShapeTests` fails when a `true` fixture brings any of these shapes back.

## Restored (4)

Each was deleted, then rebuilt as a grammar the loader can produce, and each keeps its purpose with the
changes listed. The oracle confirmed every expected row; each changed word was shown to change under a
targeted mutation of the grammar.

* `languages/suffixing-vowel-harmony` (27 words; two respelled, see below): `outputPartOfSpeech` dropped from the three slot rules.
  `ruleCollective`, the circumfix with one `RequiredEnvironments`, stays: the loader writes exactly that
  shape (README row 14), so the recorded reason for deleting it was wrong.
* `edge-cases/feature-gating-breadth` (15 words became 10: 4 kept, 11 dropped, 6 added): its stratum is
  `unordered`, the rule-list order words, the realizational-rule words and the foot-feature words are
  gone, and six words pin what is left. It pins a root's own head feature reaching a rule's gate and a
  rule's output overwriting it. The per-word record is in "Words dropped, added or re-derived".
* `languages/suffixing-extension-slot-ordering` (52 words): the two `RealizationalRule`s, `family`,
  `outputObligatoryFeatures` and foot features are gone, its MPR features sit in the loader's two groups
  (`inflClasses` and `exceptionFeatures`), its stratum is `unordered`, and six words are dropped and
  four re-derived (named below). It gained a second stem name, a rule and a root allomorph that name it, and two
  homophone roots (`daxeh`, `dax`) so that a stem name on a rule and on a root allomorph each decide a
  word.
* `edge-cases/right-to-left-segments-environment` (5 words): its right context is written as the
  segment `y` rather than as an inline `Segments` literal with a table. All five signatures are kept.

`languages/fusional-realizational-morphology` stays deleted: its premise is a `RealizationalRule` and
three custom MPR groups.

## Words dropped, added or re-derived

Each fixture below changed which words it holds. The first number is the word count before the
change, the second the count now. A word is **kept** when its expected result and signatures are
unchanged, **dropped** when it is gone, **re-derived** when it stays but its expected result changed,
and **added** when it is new.

* `edge-cases/feature-gating-breadth` (15 to 10).
  * Kept (4): `kal`, `kalka`, `tun`, `tunka`.
  * Dropped (11): the foot-feature words `mol`, `molka`, `nal`, `nalno`, `nalnomu` (`HCLoader.cs` never
    loads a foot feature); the realizational-rule words `kalid`, `kalidka`; and the rule-list order
    words `kalkano`, `kalnoka`, `kalmuid`, `kalidmu` (an `unordered` stratum has no list order to pin).
  * Added (6): `kalpi`, `tunpi`, `tunpika`, `kalpika`, `tunkapi`, `kalkapi`.
* `languages/suffixing-extension-slot-ordering` (56 to 52).
  * Dropped (6): `lima`, `limaile`, `limape`, `limapeile` (the realizational rule `RPAST` and its blocking
    check) and `zamed`, `zimed` (the realizational rule `rrRRealTest` and the family `famRRealBlock`).
  * Re-derived (4, each from no parse to one parse because the stratum is `unordered`): `yxkibz`,
    `sekwz`, `sekhw`, `dalehiz`.
  * Added (2): `daxeh`, `dax`. The 46 others are kept.
* `languages/suffixing-vowel-harmony` (27 to 27): `etemik` and `esalik` became `etemig` and `esalig`, the
  forms the circumfix can surface. The other 25 are kept.
* `edge-cases/compounding-breadth` (10 to 5). Dropped: `kaki` (`NonHeadRequiredHeadFeatures`), `kutu`
  (`HeadRequiredHeadFeatures`), `kati` (`NonHeadRequiredFootFeatures`), `patu`
  (`HeadRequiredFootFeatures`) and `kamtu` (`multipleApplication="0"` on a compound). Kept: `ka`, `tu`,
  `katu`, `katumi`, `kaptu`. A compound rule that reads head or foot features, or has a cap of 0, is
  unproducible (README rows 24, 19 and 23), so its negative controls went with it.
* `edge-cases/morphotactic-attribute-breadth` (29 to 24).
  * Dropped: `kulba` (a cap of 0 on an affix rule), `kuldedede` (three copies against a cap of 2, which
    HCLoader cannot set) and `topdori`, `topdo`, `topri`.
  * Re-derived: `kulde` is `KUL+ONCE` (was `KUL+TWICE`) and `kuldede` has no parse (was one), because
    `mrRep1` keeps the default cap of 1.
  * Lost with `topdori`, `topdo` and `topri`: the pair `mrConferExcl` (a derivational rule writing
    `mprExclFlag`) and `mrExclReader` (a slot rule excluding it). A derivational rule writes only an
    inflection class or a production restriction, and a slot rule excludes only an inflection-type
    feature, which only a variant entry carries (README row 27). The dataflow cell
    `MorphologicalOutput.MPRFeatures->MorphologicalInput.excludedMPRFeatures` therefore has no flagged
    witness.
* `edge-cases/final-template-partial-trace` (5 to 5, new): its rules were rebuilt as an unslotted partial
  rule and a derivational rule, with no output feature, so no word changed. Both final-template gates
  are still pinned: `sagft` against `sagfq` for the prohibition, `sagfqf` against `sagftf` for the
  requirement.
* `languages/suffixing-evidential-adjacency-chain` (30 to 32): added `siputukuchikshi` and
  `walaknkichiktan`, which tell a somewhere-to-the-side exclusion from an adjacent one. The 30 others are kept.
* `edge-cases/disjunctive-recheck` (12 to 16): added `pakde`, `pakze`, `pakzeta`, `pakdeta` (the `ruleE`
  re-check witnesses). `pakda` now fails as an ordinary disjunctive stop, not as a re-check rejection.

## Deleted (23)

None could be converted to a producible grammar without losing its premise, except where the doubts
below say otherwise. The first column is the fixture name; the second is the construct (README row
numbers) that made it unproducible, with what the grammar used; the third is what it tested. A fixture
may need more than one construct.

| Fixture | Construct (README row) | What it tested |
|---|---|---|
| `edge-cases/bistratal-overlapping-segment-representation` | 1: two character tables, one per stratum | whether a segment spelled differently on two strata is accepted or refused when each stratum has its own lexicon (the refusal side of shared representation) |
| `edge-cases/cross-table-root-respelling` | 1: tables `tIn` and `tFin` | a root entered on an inner stratum surfaces spelled by the final table's segment with the same feature bundle, with no phonological rule |
| `edge-cases/default-symbol-after-merge` | 2: a `defaultSymbol` | default-symbol matching on a segment produced by a merge rule |
| `edge-cases/feature-system-breadth` | 7: `isActive="no"` on a symbolic feature, a complex feature, a feature value, both natural class kinds and a lexical entry; 20: `ExcludedEnvironments` on the allomorph of `eSal` | deactivation of feature-system elements, complex features, right-to-left metathesis and an alpha variable |
| `edge-cases/loader-default-symbol` | 2: a `defaultSymbol` | an under-specified segment counts as the default value (nasal +), so a rule that targets oral segments must not apply to it |
| `edge-cases/loader-isactive-breadth` | 1, 7, 8: three character tables, `isActive="no"` on more than a dozen kinds, `family` twice | an inactive decoy beside the live declaration for each collection the XML loader filters |
| `edge-cases/loader-isactive` | 7: a second, inactive `PhonologicalFeatureSystem` block | the loader uses only the active feature-system block |
| `edge-cases/metathesis-comparison-crash` | 5: a `leftSwitch` that names the earlier group | the engine's pinned failure when the left switch is the earlier of the two groups |
| `edge-cases/mpr-group-overwrite-without-realizational` | 4: a custom-named group (`ThemeGroup`) | an overwrite-mode MPR group in a grammar with no realizational rule |
| `edge-cases/mpr-overwrite-order-dependence` | 4: an overwrite group and an append group | on an unordered stratum, an overwrite group keeps only what the last rule wrote, so the result depends on application order |
| `edge-cases/multi-table-metathesis-shared-representation` | 1: tables `t0` and `t1` | metathesis across two tables that share a representation |
| `edge-cases/realizational-reduplication-no-proposal-route` | 3: a `RealizationalRule` | reduplication driven by a realizational rule |
| `edge-cases/rewrite-analysis-feature-neutralization` | 1: tables `tCore` and `tSurf` | cross-table respelling together with analysis-side feature neutralization |
| `edge-cases/rewrite-default-environment` | 2: a `defaultSymbol` | default-symbol matching in a rule's environment |
| `edge-cases/rewrite-default-epenthesis` | 2: a `defaultSymbol` | default-symbol matching around an epenthesis rule |
| `edge-cases/rewrite-default-full-set` | 2: a `defaultSymbol` | default-symbol matching when a rule names the full feature set |
| `edge-cases/rewrite-default-narrow` | 2: a `defaultSymbol` | default-symbol matching in a narrowing rule |
| `edge-cases/right-to-left-cross-table-segments-environment` | 1: two tables and a `characterDefinitionTable` on `Segments` | a right-to-left rewrite whose right environment is an inline `Segments` literal spelled in the second table |
| `edge-cases/segment-natural-class-table-binding` | 1: tables `t0` and `t1`, one per stratum, with a natural class over segments | a natural class over segments binds to its own stratum's table |
| `edge-cases/synthesis-stratum-render-stale-table` | 1: tables `tRoot` and `tFace` | the parse signature is spelled with a stratum's table that synthesis carried forward |
| `edge-cases/two-table-shared-representation-recall` | 1: tables `t0` and `t1`, one per stratum | the recall side of shared representation: material threaded from one table to the other through a rule |
| `languages/fusional-realizational-morphology` | 3, 4, 9, 10: `RealizationalRule` `rrPast`, three custom MPR groups, `outputObligatoryFeatures` on a compound, required and excluded MPR features on the compound head (`mrCompoundConstrained`) | a fusional language with realizational tense, ablaut, stem names and constrained compounding |
| `languages/prefixal-discontinuous-slot-dependency` | 11: MPR output from the slot rule `mrModeTrans`, required by a later slot | a prefixing language where a later slot depends on an earlier, non-adjacent one |

Counts by row: 1 has 9 fixtures, 2 has 6, 3 has 2, 4 has 3, 5 has 1, 7 has 3, 8 has 1, 9 has 1,
10 has 1, 11 has 1, 20 has 1. Rows 6 and 19 have none left: their fixtures were restored. A fixture that
needs several rows is counted under each.

## Trace-verified surfaces lost and gained

The sections from here to the end record how the retirement moved the coverage measurements of sillsdev/machine
(its trace floor, its ledgers and its test classes). Those files and tests came from sillsdev/machine#480 and are not in
this repository; the section is history, kept for the reasoning.

`GrammarCoverageGateTests.TraceFloor` counts the surfaces a verified parse's rule trace proves. The
corpus had 61 before the producible rewrite and has 58 now; the floor was lowered once for each step.
Compared surface by surface (a surface whose witness fixture merely changed does not count):

* Lost (5): `dtd:element/HeadRequiredFootFeatures` and `dtd:element/NonHeadRequiredFootFeatures` (foot
  features, README row 19), `dtd:element/HeadRequiredHeadFeatures` and
  `dtd:element/NonHeadRequiredHeadFeatures` (row 24), all four witnessed by `compounding-breadth`; and
  `dtd:enum/MorphologicalRule/multipleApplication/2` (row 22), witnessed by
  `morphotactic-attribute-breadth`. None of the five can be produced by FieldWorks.
* Gained (2): `dtd:enum/CompoundingRule/multipleApplication/2` (`compound-max-applications`) and
  `dtd:enum/MorphologicalOutput/redupMorphType/suffix` (`suffixing-extension-slot-ordering`).
* The step from 61 to 60 was the three cells lost in the first round (the two foot-feature elements and
  `MorphologicalRule/multipleApplication/2`) net of the two gained; the step from 60 to 58 is the two
  head-feature elements of a compound.

## Ledger cells lost, by name

The ledger pins moved when the ledgers were regenerated on the producible corpus. Each cell lost, and
why:

* Gate arms (`gate-obligations.tsv`, 18 to 16 evidenced; 11 to 10 Blocked and 7 to 6 Control):
  `NonPartialRuleProhibitedAfterFinalTemplate` Blocked and Control, both witnessed by
  `final-template-partial-trace` before it was rebuilt. The ledger takes the first word that a severed
  attribute flips from failing to parsing. Severing `MorphologicalRule.partial` now flips `sagfqf`, whose
  trace names `NonPartialRuleRequiredAfterNonFinalTemplate`, not the prohibition; severing
  `AffixTemplate.final` changes `sagftf` first, in the wrong direction. The ledger is right to say
  NotEvidenced, and a mutation check shows why this is not only a ledger artefact. No word in
  `final-template-partial-trace` depends on the gate at the default configuration (`sagft` and `sagfqf` also
  fail by other checks). Removing the synthesis gate alone, or the analysis gate alone, changes no result of
  the 143-run self-check. Removing both fails only `final-template-partial-discriminators [variant
  enforce-final]` (word `pilfbvb`), which is the only result-level test of the gate. The words `sagft` and
  `sagfq` still sit in `words.yaml`, but they pin nothing about this gate. The gate stays recorded as lost
  (`obligation-triage.tsv`, bucket 3, Open). FieldWorks can set `MakePartialsFinal` (`HCParser.cs:168`), so
  the gate is producible; adding a fixture variant for it is possible, and nothing here claims otherwise.
  Gates with both arms evidenced: 7 to 6.
* Dataflow cell (`dataflow-obligations.tsv`, satisfied 9 to 8, not satisfied 96 to 106, unknown 193 to
  184): `MorphologicalOutput.MPRFeatures->MorphologicalInput.excludedMPRFeatures` (`PresentGatedForm`),
  lost with `topdori`, `topdo` and `topri` (above). The other cells of that chain, and two chains that
  now end in the overwrite group `lexEntryInflTypes`, moved from Unknown to NotSatisfied or are
  structurally hazardous.
* Interaction chains (`interaction-chains.tsv`, 33 rows and 18 exercised to 34 rows and 22 exercised; 8
  hazardous): the new `StemName` junction (`Allomorph.stemName` to `MorphologicalRule.requiredStemName`,
  from the `suffixing-extension-slot-ordering` stem-name rebuild) is added and exercised. The four
  `LexicalEntry.ruleFeatures` chains become exercised and hazardous (three were unexercised).
  `MorphologicalOutput.MPRFeatures -> PhonologicalSubrule.requiredMPRFeatures` becomes exercised. One chain is
  lost: `MorphologicalOutput.MPRFeatures -> MorphologicalInput.excludedMPRFeatures` goes from exercised to
  unexercised with `topdori`, `topdo` and `topri` (the dataflow cell above). Chains with a paired witness: 9
  to 8.
* Surfaces (`fold-in-candidates.tsv`, 46 to 44 rows): `dtd:element/HeadRequiredHeadFeatures` and
  `dtd:element/NonHeadRequiredHeadFeatures` (row 24), also dropped from the counterfactual ledger.
  `dtd:element/AssignedHeadFeatures` is now evidenced by `feature-gating-breadth` (`tunka`).
* Interface witness rows (1197 to 1194; Evidenced 206 to 205; RequiredByLoader 87 to 85) and
  grammar-coverage rows (1532 to 1527: 122 to 120 surface, 1197 to 1194 interface): the same removals.
* Construct-claim rows (1386 to 1381; confirmed 788 to 786, unmapped 589 to 586; contradicted stays 9).
* Gap baseline (`semantic-coverage-gap-baseline.tsv`): with slot `exclReaderSlot` gone, the two
  unresolved ordering pairs `exclReaderSlot~exASlot` and `mbSlot~exclReaderSlot` of
  `morphotactic-attribute-breadth` become the one pair `mbSlot~exASlot`. Open ordering debt goes down by
  one and nothing is hidden.

## Retirement doubts

The one fixture below might be convertible with a loss. The four others that were in doubt are restored (above).
The conversion was tried on a scratch copy and checked with the founding oracle.

* `languages/fusional-realizational-morphology`. The same removals, plus `mrCompoundConstrained`, change
  five of 62 words (`ferid`, `ygofz`, `yxpedz`, `sodh`, `gofwh`); the realizational point is lost.
  Partial doubt. Not restored: its premise is the realizational rule.

Claims in the deleted fixtures' notes that do not hold at FieldWorks `620cd990`:

* `edge-cases/loader-isactive-breadth` says an allomorph has no inactive state. A form with `IsAbstract`
  is skipped (`IsValidRuleForm`, `IsValidLexEntryForm`). The fixture still needs three tables and `family`.
* `languages/prefixal-discontinuous-slot-dependency` says one required-MPR list applies to every subrule.
  That is true of a derivational rule; `mrSubj` sits in a slot, where subrules may differ. Its other
  reason, MPR output from a slot rule, holds.
* No deleted fixture used differing `requiredMPRFeatures` across the subrules of a non-inflectional rule.
  Row 12 is a shape the suite avoids; it is not a reason any fixture was deleted.
* `edge-cases/metathesis-comparison-crash` stays out, but the switch order is an editor guarantee
  (`MetaRuleFormulaControl.GetNextCell`), not a LibLCM data-model one.
