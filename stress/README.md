# Stress fixtures

These grammars are for timing and optimization work on the analysis pass. They are not conformance
fixtures: they live under `stress/`, outside `edge-cases/` and `languages/`, so no manifest, coverage report
or default runner sees them. Each `words.yaml` starts with `# kind: stress`. They follow the same rule as the
suite: only grammars a FieldWorks project can produce (see the
[README section on what the XML can say but FieldWorks cannot](../README.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it)).

Expected output is a parity check: the original parses came from `master` (three identical runs were
required). The FLEx-style null-affix rows were updated against the current engine and reviewed against the
grammars; an optimization must return the same parses. The measure of a change is the number of
analysis steps, not wall-clock time.

Run them only on request. In a sillsdev/machine checkout that mounts this repository as `conformance/`:

```
dotnet test tests/SIL.Machine.Morphology.HermitCrab.Tests --filter TestCategory=Stress
dotnet run --project src/SIL.Machine.Morphology.HermitCrab.Conformance -- --fixtures conformance/stress --include-pathological
```

The test fixture is `[Explicit]` and `[Category("Stress")]`, so a plain `dotnet test` skips it. The issue numbers
in the table below (#490, #560, #572, #574, #575, #576, #579, #548) are sillsdev/machine issues and pull requests.

| Fixture | What it exercises | Built for |
|---|---|---|
| `bantu-tam-templates` | Bantu slot templates with required slots (subject, object, extension, TAM, final vowel); 12 of 60 words have no parse | #575, #576 (required-slot look-ahead) |
| `bantu-tam-templates-shared` | the same words with three trailing slots shared across templates | #575, #576 (required-slot look-ahead) |
| `bantu-tam-fusion` | the same Bantu slot templates, but each object and subject rule has a plain allomorph for stems that start with a consonant and a vowel-fusion allomorph for stems that start with a vowel (synthetic, not a real language; 31 of 65 words have no parse) | the impure-slot look-ahead, stacked on #576 |
| `truncating-slot-chain` | slot templates whose required and optional suffix slots each delete the vowel before them, so required slots are always missing a segment a later slot restores (synthetic; the look-ahead prunes next to nothing; 12 of 60 words have no parse) | the supply-set look-ahead, stacked on #579 (its worst case) |
| `early-lexicon-agglutinative` | agglutinative words whose root is found early; root-substring and edge-segment prunes | #572, #574 (root-substring prune, edge-segment prefilter) |
| `bantu-extension-chain` | chained verbal extensions | excluded co-occurrence check (parked; #490 ledger) |
| `bantu-extension-required-slot` | extension chain with a required slot | template replay at lookup (dead end; #490 ledger) |
| `required-template-slot` | a required template slot with decoy branches | template replay at lookup (dead end; #490 ledger) |
| `athabaskan-prefix-complex` | a dense prefix complex | excluded co-occurrence check (parked; #490 ledger) |
| `excluded-cooccurrence` | dense morpheme co-occurrence exclusions | excluded co-occurrence check (parked; #490 ledger) |
| `allomorph-list-density` | many allomorphs per morpheme | #560 (allomorph-loop cutoff) |
| `prefix-class-density` | many prefix classes | #560 (allomorph-loop cutoff) |
| `derivation-chain-homophone-roots` | derivation chains over homophonous roots | template replay at lookup (dead end; #490 ledger) |
| `env-bantu-concord` | allomorphs gated by the stem's edge segments, written in the input pattern (no `RequiredEnvironments`) | allomorph gating; built for the environment input prefilter (dead end; #490 ledger), which it no longer exercises |
| `env-austronesian-nasal-prefix` | nasal-prefix allomorphs gated by the stem's first segment, written in the input pattern (no `RequiredEnvironments`) | allomorph gating; built for the environment input prefilter (dead end; #490 ledger), which it no longer exercises |
| `env-zero-allomorphs` | zero allomorphs gated by rare segment classes in the input pattern; two prefix subrules (`subP1z`, `subP2z`) keep a left `RequiredEnvironments` | allomorph gating; built for the environment input prefilter (dead end; #490 ledger), which it barely exercises |

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
for environment checking, and any claim about its cost has no measurement behind it.

`mpr-bantu-concord` and `mpr-inflection-classes` were removed: both used custom-named `MorphologicalPhonologicalRuleFeatureGroup`
elements with `outputType="append"`, and HCLoader builds only three fixed groups (`inflClasses`, `exceptionFeatures`,
`lexEntryInflTypes`) with the default overwrite output, so they could not be kept as grammars a real project can produce.
An inflection-class benchmark can be rebuilt on the fixed `inflClasses` group, which a real project does produce.

Three expected parses of `bantu-tam-fusion` use a fusion allomorph: `kosaiarewabutani`, `waoarekum` and `somauarewab`. Each plain subrule takes only a stem whose first segment is not a vowel and each fusion subrule only a stem whose first segment is a vowel, so the two cannot shadow each other. Only the `tam_are` prefix produces a vowel-initial stem. Deleting all 200 `fsub_*` subrules makes those three words fail, and widening the plain subrules to any stem makes the three plain-form negatives (`kosiarewabutani`, `woarekum`, `somuarewab`) parse and the three fused words fail. The other 59 words use plain allomorphs only.

`early-lexicon-agglutinative` omits the word `polundanasak`: engines before #548 (synthesis
filtered by the allomorphs used) trace an extra phonological rule for it that master does not, so no single expectation passes on both.
`deep-derivation-trace` is not included: it measures trace memory and
its words have up to 864 parses each.
