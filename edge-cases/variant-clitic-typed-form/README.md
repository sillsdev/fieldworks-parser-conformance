# variant-clitic-typed-form

A sense-less FieldWorks entry `=ke` of the enclitic morph type, whose one variant entry ref names the stem `ta`. HCLoader splits every entry's forms into stem and clitic buckets and runs `LoadLexEntries` and `LoadMorphologicalRules` for each (`HCLoader.cs:299-305`), so the variant is loaded in the Clitics stratum twice, both times under `ta`'s Noun MSA: as a stem copy (`LoadLexEntryOfVariant`, `HCLoader.cs:782-856`) and as a clitic rule (`LoadMorphologicalRules`, `HCLoader.cs:896-924`, which for a stem MSA calls `LoadCliticAffixProcessRule`). An engine that builds variants for the stem bucket only parses `ke` and never `take`.

## What it pins

- `ta`: the main stem (control).
- `ke`: the variant's Clitics-stratum stem copy parses alone as `ta`'s MSA (`TA`).
- `take`: the variant's clitic rule `mrKe` attaches to `ta` (`TA+TA`).
- `keke`: the clitic rule attaches to the variant's own stem copy.
- `tu`, `keta`: no analysis. `tu` is spelled by nothing; `keta` shows the enclitic never precedes its host and that the two stems do not compound.

Without the rule, `take` and `keke` have no analysis; without the stem copy, `ke` and `keke` have none (checked at `ba6dfa10`).

## Grammar shape

`grammar.xml` is the per-copy form: `Main` holds `ta`; a second stratum named `Clitics` holds the clitic rule `mrKe` (no part of speech, listed in that stratum's `morphologicalRules`) beside the stem copy `eKe` with the same `MorphemeId` as `ta`. No `isCliticRule` attribute is set: the rule is a clitic by its stratum's name. HCLoader also makes a Surface stratum, which would hold no rule here (the same two-stratum form as `adhoc-prohibition-variant-enclitic-first`). Nothing was converted from the staged grammar.

## Oracle

Every row was taken with `hc-conformance --propose` at sillsdev/machine `ba6dfa10` (tip of #615, the suite pin). The five staged rows, taken at `aab4c598`, replayed unchanged; `keta` is new.

## FieldWorks source witness

None is stored. PanGloss staged a `fieldworks/project.fwdata` (authored with `xample-projector author --variant-of eTe=eTa`, then the variant's MoStemAllomorph morph type was edited from stem to enclitic by hand) without the `phonology-mutations.yaml` and `WritingSystemStore/` this suite's witness shape requires, and the hand edit is outside what section 3 of AGENTS.md allows. Its data was read against the loader: the entry has no senses or MSAs, one `LexEntryRef` (RefType 0, no variant types) to `ta`, and one MoStemAllomorph of the enclitic type (`d7f713e1-e8cf-11d3-9764-00c04f186933`); `ta` has a Noun MoStemMsa. That is the input `HCLoader` turns into this grammar. `fieldworks_producible: true` therefore rests on the loader source (`FieldWorks` origin/main `d36ff645`), not on a certified witness.

Source: PanGloss#174 (staging `conformance-staging/edge-cases/variant-clitic-typed-form`).
