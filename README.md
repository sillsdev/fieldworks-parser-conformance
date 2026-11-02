# The morphological parser conformance suite

A general-purpose, engine-agnostic conformance test suite for what a morphological/phonological
parser needs to get right: grammars in the HermitCrab XML format, words, and the parses a reference
engine produces for them.

**The one rule: the suite holds only what a real FieldWorks project can produce.** FieldWorks never
authors HermitCrab XML; it builds a grammar from a LibLCM project through `HCLoader.cs`, and that
loader reaches less than the XML can say. A grammar that needs something the loader never writes does
not belong here, however expressible it is in the XML and however well an engine handles it. Every
fixture records the verdict as `fieldworks_producible: true` in its `words.yaml`. The constructs left
out, why FieldWorks cannot write each one, and the 23 fixtures removed for using them are in
[what the XML can say but FieldWorks cannot, so we do not test it](#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it).
[`docs/grammars.md`](docs/grammars.md) lists every grammar that remains.

**The standard is the round trip.** "Producible" means a real FieldWorks project round-trips to the grammar: a
project built in FieldWorks (LibLCM), put through `HCLoader.cs`, yields the fixture's `grammar.xml`. That the
loader source could write a construct is weaker evidence. Until a fixture has a FieldWorks witness (a
`fieldworks/` directory, [PROTOCOL.md](PROTOCOL.md) section 10), its `fieldworks_producible: true` is a claim
read from the loader. Only the 9 fixtures that carry a witness are certified today (all under `edge-cases/`);
the other 124 of the 133 fixtures rest on the loader reading alone.

**Who uses it.** This repository contains no engine. sillsdev/machine (the C# HermitCrab) mounts it as a
git submodule at `conformance/`, pinned to a commit on `main`; PanGloss mounts it as a submodule that
follows `main` (`branch = main`). Both run it through their own runners. Their gates, ledgers and
coverage measurements live in their own repositories. To change the
suite, read [AGENTS.md](AGENTS.md). Where a fixture or document names a ledger, a test or a source path
of one of those repositories, it is a historical or cross-repository reference, not a file here.
The commit hashes cited in fixtures are plain text, explained in [PROVENANCE.md](PROVENANCE.md).

**What passing means today.** An engine reproduces the reference implementation's observable parse
behaviour — signature, status, pinned crash — on every fixture its declared capability profile
admits.

How complete the fixture set is, as measured per DTD surface, is tracked by the consuming engines, not here.

**Rule order is part of the contract, not an implementation detail.** A parse runs in two passes:
the word is **torn down** to find candidate stems, then **built back up** to check the rebuild
reproduces the surface it started from. This is analysis-by-synthesis — propose by stripping,
confirm by regenerating — and the engine's own vocabulary is *unapply* for the first pass and
*apply* for the second.

| Pass | Direction | Per-stratum order |
|---|---|---|
| **Analysis** — tearing down (`unapply`) | surface inward | phonological rules unapplied **first**, then affix templates and morphological rules |
| *lexical lookup* | the hinge | each stripped form is looked up for real lexical entries; `Morpher.Synthesize` calls this, so the engine places it at the **start of the build-up** |
| **Synthesis** — building up (`apply`) | stem outward | morphological rules and affix templates first, *mutually recursive* — each may invoke the other — then phonological rules **last** |

Strata run in declaration order building up, and reversed tearing down. Note the two passes are
mirror images: whatever runs last on the way up runs first on the way down.

Two consequences a consumer must reproduce. **Within one stratum pass a phonological rule cannot
feed a morphological rule or template** — phonology runs after morphology in synthesis and before it
in analysis — so that class of interaction does not exist and needs no coverage. **Across strata it
can**: stratum *N*'s phonological output is stratum *N+1*'s morphological input. And because
analysis is the inverse of synthesis, an interaction that *feeds* in one direction *bleeds* in the
other, so an interaction witnessed only in synthesis is untested in the direction a proposer runs.

The order is fixed by the engine, not by the grammar: the reference engine builds it as an unconditional cascade, which is also why
`Stratum/cyclicity` and `phonologicalRuleOrder` are inert — there is no branch point for them to
select.

`PROTOCOL.md` specifies the adapter contract in engine-agnostic terms; nothing in this repository depends on
any engine's build, layout, or language. The C# HermitCrab supplies the seed construct vocabulary
(`constructs.txt`) and is the **founding oracle** that generated every fixture's ground truth, but it is not a
hard boundary: any engine that implements `PROTOCOL.md`'s contract can be validated here, declaring a partial
**capability profile** (e.g. morphotactics-only, no phonological rules) to be measured fairly against just the
subset it claims to support.

## Shape

```
languages/<name>/    grammar.xml + words.yaml   -- 6 typologically-selected synthetic languages
edge-cases/<name>/   grammar.xml + words.yaml   -- 127 focused micro-grammars for things no shared grammar hosts
stress/              16 timing and optimisation-parity grammars (not conformance; see stress/README.md)
                     docs/grammars.md and that README list each; generated/stress-manifest.v2.json hashes them
docs/grammars.md     one line for every fixture above; scripts/check_grammars_md.py keeps it complete
coverage.csv         language x word x construct (written by a consuming engine's coverage report)
rules.csv            language x grammar rule id x exercising words (same)
dead-rules-allowed.tsv  rules a fixture declares on purpose that no word exercises, with the reason
constructs.txt       the checklist vocabulary of construct tags that `exercises:` values are drawn from
fieldworks-writable-shapes.tsv  the census of which DTD members HCLoader.cs writes (see below)
HermitCrabInput.dtd  the published grammar DTD (the authoritative copy)
schema/              Draft 2020-12 contracts for the authoring and product formats
generated/           the versioned JSON manifest a consumer imports, and the stress manifest (scripts/generate_manifest.py)
parity-check.py      the engine-free migration parity proof
scripts/             the checks CI runs
PROTOCOL.md          the adapter contract
PROVENANCE.md        which engine builds supplied the ground truth
AGENTS.md            how to change the suite
```

The 16 timing grammars in `stress/` are listed in that directory's README and in `docs/grammars.md`. The manifest above does not
count them; `generated/stress-manifest.v2.json` does, in the same layout, and `scripts/generate_manifest.py --check` checks both.
None of the 16 has a FieldWorks witness yet; the rule and the expected-output meaning are in `stress/README.md`.

## Consuming the suite from another repository

`words.yaml` is the single canonical authored format — the only place case data (inputs, parses,
rejections, skips, `neutralizes`) lives. There is no generated JSON restatement of it: an earlier
`hc-conformance-corpus/v1` product duplicated that ground truth into a 409KB file, and it carried
less than the 383KB of authored `words.yaml`/`grammar.xml` sources it was generated from, because
those sources hold 1011 comment lines of reasoning — why a fixture exists, what it pins — that JSON
cannot express. Two representations of the same ground truth also meant a permanent drift gate. It
has been deleted, along with `schema/conformance-corpus.schema.json`.

What that product genuinely contributed was provenance, not case data, so that is what survives as
`generated/hc-conformance-manifest.v2.json` (`hc-conformance-manifest/v2`, `schema/conformance-manifest.schema.json`): one entry per fixture carrying `fixtureId`, `category`, `displayLanguage`, `grammarPath`,
`grammarSha256`, `wordsPath`, `wordsSha256`, `caseCount`, and `expectedCrash`, plus top-level
`dtdPath`, `dtdSha256`, `sourceHash`, and the three format-version identifiers
(`hc-conformance-manifest/v2`, `hc-conformance-words/v1`, `sil-machine-hermit-crab-input-xml/v1`).
A consumer reads the manifest to discover fixtures and verify integrity, then reads `grammar.xml`
and `words.yaml` directly for the actual grammar and cases. Paths inside the manifest are
relative to the root of this repository, with no leading directory name (`edge-cases/<name>/grammar.xml`),
never relative to the manifest itself. A consumer that mounts this repository as `conformance/` prepends
that itself. Version 2 dropped the `conformance/` prefix that version 1 carried.

Regenerate with `python3 scripts/generate_manifest.py`; `python3 scripts/generate_manifest.py --check` verifies
the checked-in bytes and exits nonzero on drift. CI also validates every grammar against the DTD and every
`words.yaml` against `schema/words.schema.json`.

The DTD is published at `HermitCrabInput.dtd` and is the authoritative copy; sillsdev/machine keeps an
embedded copy that a test of its own holds byte-identical. When resolving a grammar's DOCTYPE, admit only the
system identifier `HermitCrabInput.dtd` and map it to the published DTD path the manifest records. Any other
external entity, network fetch, or filesystem fallback should be refused rather than attempted.

Two files are required per fixture: `grammar.xml` and `words.yaml`. An optional `README.md`
preserves the fixture's rationale and oracle history; optional FieldWorks witnesses are described
in the protocol. `words.yaml` is the single ground truth: front matter (`language`,
`inspired_by`, `sources`, `requires`) plus one entry per word, each carrying a `note` and either
`parses` (`signature`/`gloss`/`rules`/`exercises`, one per distinct analysis), `expect_fail` +
`blocked_by` (well-formed input, zero valid analyses), or `expect_skip` (the oracle throws
`InvalidShapeException`, e.g. an undeclared segment — status "SKIPPED", not "ok"). Optional fields:
`provenance` (bug/PR reference), `guess` (a `LexicalGuess` parse),
`budget_ms`/`expect_crash` (edge-cases only). Signature comparison treats the members of each bracketed
class `[...]` as a set (`|b[ae]t` equals `|b[ea]t`; PROTOCOL.md section 4, sillsdev/machine#573).
Signatures are authored-and-verified, never blindly
regenerated: a consuming engine's self-check fails on a mismatch, and a proposed patch is for a human to accept. Full schema: `schema/words.schema.json`.

## The six languages

| Directory | Grammar name | Simulates |
|---|---|---|
| `templatic-root-modification` | TemplaticRootModification | Templatic root-and-pattern morphology, stem names, OCP co-occurrence, simultaneous rewrite |
| `metathesis-phase-isolation` | MetathesisPhaseIsolation | Infix, circumfix, reduplication, metathesis, subtractive truncation |
| `polysynthetic-stratal-derivation-chain` | PolysyntheticStratalDerivationChain | Derivation-then-inflection recursion across strata, incorporation-style compounding, guessed stems |
| `suffixing-evidential-adjacency-chain` | SuffixingEvidentialAdjacencyChain | Evidential suffix chain, morpheme-adjacency co-occurrence, `requires: []` — the XAmple-eligible, phonology-free grammar |
| `suffixing-extension-slot-ordering` | SuffixingExtensionSlotOrdering | Verbal extension suffixes in template slots, MPR features in the loader's two groups, reduplication, post-nasal mutation, stem names on rules and root allomorphs |
| `suffixing-vowel-harmony` | SuffixingVowelHarmony | Alpha-variable vowel harmony, merges, gradation and epenthesis in one stratum, a circumfix, an infix |

Each is a dense, synthetic grammar (invented lexemes and segment inventories, no orthographic claim
about any real language) where ordinary words exercise several constructs at once, rather than a
one-mechanism probe. `edge-cases/` holds the things no shared grammar can host faithfully:
loader/XML-semantics probes, an `expect_crash` pin, a `budget_ms` pathological stress case, and
allomorphy/rewrite pins whose exact rule shape a naturalistic grammar wouldn't contain.

## Truncation identity companions

Three edge cases derive from one truncation grammar, whose original stays unchanged:
`truncate-morphotactic-identity` adds explicit `MorphemeId` labels; `truncate-morphotactic-subsumption`
uses root `ag` plus prefix rule `X` with the original leading truncation rule `B` and insertion rule
`C`; `truncate-morphotactic-copy-u` adds a copying suffix rule `U` to the explicit-ID A/B/C grammar.
These cases preserve the distinction between a parse's allomorph order in its signature and its
forward rule application order in `words.yaml`'s `rules` list. Repeated signature strings are
intentional and remain repeated rows.

The checked-in expectations were captured from the combined #500+#506 C# source state: sillsdev/machine #556
plus the #500 `ApplyRhs` relocation. The two commit hashes, the assembly SHA-256 values and the reproduction
recipe are recorded in [PROVENANCE.md](PROVENANCE.md) as plain text; the expected rows do not depend on a
temporary staging file.

An engine without both fixes does not satisfy these complete identity rows reliably, because its
copied annotations differ. Keep the full combined-oracle multisets; do not weaken them to match the
pre-fix base output.

The corrected C# traces report the same analysis features for these rows:
`pos=[posV]`, `syntactic=[POS:v]`, `realizational=ANY`, and the default MPR feature set.
Each root token is its entry's single root XML allomorph, and each rule token is that rule's
single allomorph; every observed allomorph has index 0 and count 1. Signature token order is
the final morph occurrence order, while the tables below retain the separate forward rule
application order. All positive words have status `ok`; `bag` and `bau` have status `ok` with
zero parses, as declared by `expect_fail`. None of the fixture words is skipped.

Stable source attribution is `ROOT` = `root32`/`root32_1` in the identity and copy-U fixtures;
`ROOTAG` = `root32`/`root32_1` in subsumption; `A` = `mruleTruncTrail`, `B` =
`mruleTruncLead`, `C` = `mruleTruncOptIns`, `X` = `mrulePrefixX`, and `U` = `mrU`. The
corresponding `MorphemeId` is explicit in each companion grammar; runtime GUIDs are not used as
fixture identities.

`truncate-morphotactic-identity` expected parses:

| Word | Signature | Forward rule order |
|---|---|---|
| `sag` | `ROOT|sag` | root |
| `sas` | `ROOT33|sas` | root |
| `a` | `ROOT+B+A|a` | B, A |
| `a` | `ROOT+A+B|a` | A, B |
| `ga` | `ROOT+B+C+A|ga` | B, A, C |
| `ga` | `ROOT+A+C+B|ga` | A, B, C |
| `ga` | `C+B+ROOT+A|ga` | B, C, A |
| `ga` | `ROOT+C+A|ga` | A, C |
| `ga` | `C+ROOT+A|ga` | C, A |
| `bag` | no parses | — |

`truncate-morphotactic-subsumption` expected parses:

| Word | Signature | Forward rule order |
|---|---|---|
| `ag` | `ROOTAG|ag` | root |
| `ag` | `ROOTAG+X+B|ag` | X, B |
| `sag` | `X+ROOTAG|sag` | X |
| `gag` | `X+C+ROOTAG|gag` | X, C |
| `gag` | `X+C+ROOTAG+B|gag` | X, B, C |
| `gag` | `X+C+ROOTAG+B|gag` | C, X, B |
| `gag` | `C+ROOTAG|gag` | C |
| `bag` | no parses | — |

`truncate-morphotactic-copy-u` expected parses (the repeated `ROOT+C+A+U|gau` identity is retained):

| Word | Signature | Forward rule order |
|---|---|---|
| `gau` | `ROOT+A+C+B+U|gau` | A, B, C, U |
| `gau` | `ROOT+B+C+A+U|gau` | B, A, C, U |
| `gau` | `B+A+C+ROOT+U|gau` | B, C, A, U |
| `gau` | `C+B+ROOT+A+U|gau` | A, B, U, C |
| `gau` | `C+A+ROOT+B+U|gau` | B, A, U, C |
| `gau` | `ROOT+U+C+A+B|gau` | A, U, B, C |
| `gau` | `ROOT+C+A+U|gau` | A, C, U |
| `gau` | `C+A+ROOT+U|gau` | C, A, U |
| `gau` | `ROOT+C+A+U|gau` | A, U, C |
| `au` | `B+ROOT+A+U|au` | A, B, U |
| `au` | `A+ROOT+B+U|au` | B, A, U |
| `au` | `ROOT+A+U+B|au` | A, U, B |
| `sagu` | `ROOT+U|sagu` | U |
| `bau` | no parses | — |

Every listed allomorph is index 0; the named roots and rules in the signatures are their explicit
`MorphemeId` values. The rules use the existing `AffixProcessRule: subtraction/truncation`
construct label; the fixtures do not introduce new coverage categories. All three declare
`morphologicalRuleOrder="unordered"`, which HCLoader emits. Their words are intentionally synthetic,
but that does not make the grammar constructs FieldWorks-unproducible, so all three correctly carry
`fieldworks_producible: true`.

The combined #500+#506 corrected-engine audit that flips those copied grammars from `unordered` to
`linear` loses analyses in all three companions; the exact changed words and signatures are recorded
in sillsdev/machine's `morphological-rule-order-measurement.md`. The checked-in grammars remain `unordered`,
matching HCLoader's emitted order.

The ordinary conformance runner checks signature multiplicity and the set of rule IDs associated
with each signature. It currently canonicalizes rule IDs before comparing them, so the ordered
`rules` lists preserve the observed application histories but do not independently gate their order.

Fixture and case totals are summed from `generated/hc-conformance-manifest.v2.json`, not
hand-copied here: two prose totals in this file have already drifted from the manifest twice, so
this file does not repeat them -- read the manifest (`python3 scripts/generate_manifest.py --check`), whose
per-fixture `caseCount` is what that check verifies.

## What the XML can say but FieldWorks cannot, so we do not test it

The suite keeps only grammars a real FieldWorks project can produce (see the rule at the top). The
constructs below are valid in `HermitCrabInput.dtd`, and the engine implements them except where a row
says otherwise, but `HCLoader.cs` never writes them. No FieldWorks project can reach them, so a fixture
that needs one would test the engine against input FieldWorks never sends, and the suite does not pin
them. Do not author a fixture for any of them. The `todo` lines in sillsdev/machine's `semantic-coverage-baseline.txt` for
`Family`, `RealizationalRule`, `CharacterDefinitionTable/isActive/no`,
`MorphologicalPhonologicalRuleFeatureGroup/outputType/append`, `isCliticRule`, `ExcludedEnvironments`,
`blockable/false`, the foot-feature elements and `HeadRequiredHeadFeatures` and
`NonHeadRequiredHeadFeatures` name constructs in this table; leave them `todo`.

This is a different list from the surfaces that no engine reads at all (sillsdev/machine tracks eleven of those).
These the engine does read, and FieldWorks never writes. Subcategorization (row 17) and row 18 are read by no
engine path either.

**Where this was checked.** FieldWorks commit `620cd9903f46941ee85947615dba15c8888c8e7a`,
`Src/LexText/ParserCore/HCLoader.cs`, which was last changed by
`6b8a75287221a1b5ab6d15d6f6eedc117690ef98`; LibLCM commit `d564a719b1cce16c25ebea53a537393cb757f5d1`.
The line numbers below are for that file. sillsdev/machine's `fieldworks-producibility.tsv` and its generator were written
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

Rows 1 to 6, 8, 9, 10, 17 and 18 cover the 26 `No` rows of sillsdev/machine's `fieldworks-producibility.tsv` (row 17
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
only if it defines one, and 15 of the 133 grammars do. Most fixtures write their affix and compound outputs without the boundary, and the
effect of that on a parse is not measured. A claim that an output is "written as HCLoader writes it" is
therefore made only where the output carries the boundary, as in the circumfix of
`languages/suffixing-vowel-harmony`.

The 23 fixtures removed for these constructs, each mapped to the construct that disqualified it, are in
[`docs/engine-only-fixture-retirement.md`](docs/engine-only-fixture-retirement.md).

## Growth policy: every bug fix lands with a conformance addition

> **Every bug fix in a conforming engine lands together with a conformance addition** — a new word,
> a new grammar, or a new edge-case.

The cheap path, in order of preference:

1. **Add a word.** One `words.yaml` entry (word + `note` + `parses` + `provenance`) in the language
   whose grammar already covers the territory. No grammar changes.
2. **Extend a grammar** when no existing language's grammar can express the trigger but the
   phenomenon is typologically plausible for one of the six (e.g. a new evidential-chain
   interaction belongs in `suffixing-evidential-adjacency-chain`).
3. **Add an edge-case** when the pin is too specific to embed naturalistically (an XML-loader quirk, a
   crash, an unusual rule shape). It must still be a grammar FieldWorks can produce; a pin that needs
   a construct in [the section on what FieldWorks cannot produce](#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it)
   belongs outside this suite.
4. **Add a new `languages/` member** only for genuinely new typological territory not covered by any
   of the six, not for an incremental variant of one that already exists.

Then follow [AGENTS.md](AGENTS.md).

## See also

- `PROTOCOL.md` — the adapter contract: CLI shape, TSV format, signature algorithm, capability
  profiles, per-engine grammar representation.
- `PROVENANCE.md` — the engine builds that supplied the checked-in ground truth.
- `docs/` — the fixture contract, the list of grammars, and the rationale documents.
