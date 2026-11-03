# Stress fixtures

These 16 grammars are for timing and optimization work on the analysis pass. They are not conformance
fixtures: they live under `stress/`, outside `edge-cases/` and `languages/`, so the conformance manifest,
the coverage files and a runner pointed at the suite root do not see them. Each `words.yaml` starts with
`# kind: stress`. [docs/grammars.md](../docs/grammars.md#stress-grammars) lists them too, and
`scripts/check_grammars_md.py` fails when either list loses one.

## The rule, and what "producible" means here

The stress fixtures follow the one rule of the suite: only what a real FieldWorks project can produce (see the
[README section on what the XML can say but FieldWorks cannot](../README.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it)).
"Producible" means a real FieldWorks project round-trips to the grammar: a project built in FieldWorks, put
through `HCLoader.cs`, yields the fixture's `grammar.xml`.

All 16 fixtures carry `fieldworks_producible: true`. That is a claim read from the loader, not a certificate.
**0 of 16 stress fixtures carry a FieldWorks witness** (a `fieldworks/` directory,
[PROTOCOL.md](../PROTOCOL.md) section 10), so none is certified; the 9 certified fixtures in this repository are
all conformance fixtures. Issue [#1](https://github.com/sillsdev/fieldworks-parser-conformance/issues/1) tracks
generating witnesses for the rest. `scripts/check_grammars_md.py` recounts the witnesses on disk and fails if
this sentence disagrees; `scripts/check_fwdata.py` checks the shape of any stress witness that is added.

## What the expected output means

Expected output is a parity check, not a conformance claim. The original parses came from sillsdev/machine
`master` (three identical runs were required). The FLEx-style null-affix rows of five fixtures
(`athabaskan-prefix-complex`, `excluded-cooccurrence` and the three `env-` fixtures) were regenerated against
the engine of sillsdev/machine#480 and reviewed against the grammars. An optimization must return the same parses. The measure of a
change is the number of analysis steps, not wall-clock time; each `budget_ms` is only a guard against a hang.
No engine build is recorded for these rows (the conformance fixtures record theirs in
[PROVENANCE.md](../PROVENANCE.md)).

## Running them

Run them only on request. This repository contains no engine, so nothing here runs them. A consumer that
clones the suite into `conformance/`, as sillsdev/machine does (see the root README), reaches them at
`conformance/stress`. In such a checkout, with sillsdev/machine's `StressFixtureParityTests` present:

```
dotnet test tests/SIL.Machine.Morphology.HermitCrab.Tests --filter TestCategory=Stress
dotnet run --project src/SIL.Machine.Morphology.HermitCrab.Conformance -- --fixtures conformance/stress --include-pathological
```

These are machine's commands, not this repository's; the paths are the consumer's. The stress grammars sit beside
`edge-cases/`, not inside it, so that a consumer's coverage gate, ledgers and manifest code need not learn to skip
them. A consumer that scans the mount recursively for `grammar.xml` would still find them; it should enumerate
`languages/` and `edge-cases/`, or skip `stress/`. The test fixture is
`[Explicit]` and `[Category("Stress")]`, so a plain `dotnet test` skips it. `generated/stress-manifest.v2.json`
records the path and SHA-256 of each fixture's `grammar.xml` and `words.yaml`, so a consumer can detect a changed
stress fixture the way it detects a changed conformance fixture. It is separate from, and does not change, the
conformance manifest `generated/hc-conformance-manifest.v2.json`.

## The fixtures

The numbers in the last column are sillsdev/machine issues and pull requests, which hold the optimization each
fixture was built for. "No parse" counts the words whose expected result is `expect_fail`.

| Fixture | What it exercises | Words (no parse) | Built for (sillsdev/machine) |
|---|---|---|---|
| `bantu-tam-templates` | 12 Bantu slot templates; the subject and TAM slots are required in each, the object, extension and final-vowel slots (and a plural slot in six templates) are optional | 60 (12) | #575, #576 (required-slot look-ahead) |
| `bantu-tam-templates-shared` | the same 60 words and templates, with the three trailing slots shared across templates | 60 (12) | #575, #576 (required-slot look-ahead) |
| `bantu-tam-fusion` | the same 12 templates, but each object and subject rule has a plain allomorph for a consonant-initial stem and an `fsub_*` allomorph (200 in all) for a vowel-initial stem, which writes the stem's first vowel on both sides of an inserted `i` (e.g. `saiarewab`): not real vowel fusion, but it copies an unbounded run the way Mbugwe's fusion allomorphs do (synthetic, not a real language) | 65 (31) | #579 (look-ahead through slots whose unmatched parts are unbounded runs), stacked on #576 |
| `truncating-slot-chain` | 5 slot templates (subject, TAM and extension required, three more optional) whose suffix slots each delete the vowel before them, so a required slot is always missing a segment a later slot restores (synthetic) | 60 (12) | #580 (supply-set look-ahead for slots that write back deleted segments), stacked on #579 |
| `early-lexicon-agglutinative` | 25 morphological rules and one vowel-harmony rule over 20 roots; each of the 19 words that parse starts with a root, and the other 40 words have no parse | 59 (40) | #572 (root-substring prune, closed), #574 (edge-segment prefilter) |
| `bantu-extension-chain` | seven optional suffix slots of five homophonous suffixes each, with 52 `exclude` co-occurrence rules between slots and for filler triples | 40 (0) | #602 (excluded co-occurrence check, parked) |
| `bantu-extension-required-slot` | five extension suffixes in any order in the stratum, then a verb template with a required TAM prefix and a noun template with a required class prefix, so extension-laden nominal forms die at the required slot | 50 (0) | #601 (template replay at lookup, E3, dropped on cost) |
| `required-template-slot` | a required TAM prefix and a required noun class prefix, with verb and noun roots that share shapes, so bare stems die at the required slot | 51 (4) | #601 (template replay at lookup, E3, dropped on cost) |
| `athabaskan-prefix-complex` | six optional prefix slots of four or five homophonous prefixes, 51 `exclude` rules between paired slots, and a zero-width prefix | 40 (0) | #602 (excluded co-occurrence check, parked) |
| `excluded-cooccurrence` | six optional prefix slots of four fillers, 12 `exclude` rules over pairs and triples, and a zero-width filler | 44 (5) | #602 (excluded co-occurrence check, parked) |
| `allomorph-list-density` | 5 suffix rules (30 allomorphs in all) whose allomorphs are gated by the stem's final context (last vowel, final vowel or consonant, final voicing), written in the input pattern | 46 (6) | #560 (allomorph-loop cutoff) |
| `prefix-class-density` | 4 prefix rules (20 allomorphs in all) whose allomorphs are gated by the stem's first segment, written in the input pattern | 48 (3) | #560 (allomorph-loop cutoff) |
| `derivation-chain-homophone-roots` | seven derivational suffixes that apply in any order, over verb and noun roots that share shapes, so verb-root candidates for a nominal derivation die at the required tense slot | 48 (0) | #601 (template replay at lookup, E3, dropped on cost) |
| `env-bantu-concord` | allomorphs gated by the stem's edge segments in the input pattern; no `RequiredEnvironments` | 40 (8) | allomorph gating; built for the required-environment pre-check (#601, a dead end), which it no longer exercises |
| `env-austronesian-nasal-prefix` | nasal-prefix allomorphs gated by the stem's first segment in the input pattern; no `RequiredEnvironments` | 40 (8) | allomorph gating; built for the required-environment pre-check (#601, a dead end), which it no longer exercises |
| `env-zero-allomorphs` | zero allomorphs gated by rare segment classes in the input pattern; two prefix subrules (`subP1z`, `subP2z`) keep a left `RequiredEnvironments` | 40 (1) | allomorph gating; built for the required-environment pre-check (#601, a dead end), which it barely exercises |

State of those issues on 2026-11-02: #576 and #579 merged; #575, #574, #580 and #560 open; #572 and #490
closed; #601 and #602 are open records of a rejected and a parked optimization. The issues are the authority.

Five fixtures (`allomorph-list-density`, `prefix-class-density`, `env-bantu-concord`, `env-austronesian-nasal-prefix`,
`env-zero-allomorphs`) once wrote their stem-side context as a RequiredEnvironments on a lone prefix or suffix. HCLoader
never writes that, so the 68 subrules now carry the same context in the input pattern, as HCLoader does, and no expected
row changed. The env- fixtures were built for the environment input prefilter, which these grammars no longer
exercise; they stay as allomorph-gating workloads. Their names are kept, and the names overstate what they
now cover: only `env-zero-allomorphs` has any `RequiredEnvironments`, two left environments on a lone prefix.

**Open item: a near-side density fixture.** The only environments HCLoader can write on an affix are a right
environment on a lone suffix and a left environment on a lone prefix (`HCLoader.cs` 1626 and 1653), so the
environment checks a FieldWorks project can reach are suffix right environments (for example, conditioned
on the next suffix's initial segment) and prefix left environments (conditioned on the preceding prefix's
last segment). No stress fixture carries either at density. Until one is built, there is no stress workload
for environment checking, and any claim about its cost has no measurement behind it. Issue
[#10](https://github.com/sillsdev/fieldworks-parser-conformance/issues/10) tracks it, with the renaming of the `env-` fixtures.

`mpr-bantu-concord` and `mpr-inflection-classes` were removed: both used custom-named `MorphologicalPhonologicalRuleFeatureGroup`
elements with `outputType="append"`, and HCLoader builds only three fixed groups (`inflClasses`, `exceptionFeatures`,
`lexEntryInflTypes`) with the default overwrite output, so they could not be kept as grammars a real project can produce.
An inflection-class benchmark can be rebuilt on the fixed `inflClasses` group, which a real project does produce.

Three expected parses of `bantu-tam-fusion` use a fusion allomorph: `kosaiarewabutani`, `waoarekum` and `somauarewab`. Each plain subrule takes only a stem whose first segment is not a vowel and each fusion subrule only a stem whose first segment is a vowel, so the two cannot shadow each other. Only the `tam_are` prefix produces a vowel-initial stem. Deleting all 200 `fsub_*` subrules makes those three words fail, and widening the plain subrules to any stem makes the three plain-form negatives (`kosiarewabutani`, `woarekum`, `somuarewab`) parse and the three fused words fail. The other 59 words use plain allomorphs only.

`early-lexicon-agglutinative` omits the word `polundanasak`: engines before sillsdev/machine#548 (synthesis
filtered by the allomorphs used) trace an extra phonological rule for it that master does not, so no single expectation passes on both.
`deep-derivation-trace` is not included: it measures trace memory and
its words have up to 864 parses each.
