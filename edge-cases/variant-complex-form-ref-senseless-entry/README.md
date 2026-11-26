# variant-complex-form-ref-senseless-entry

A sense-less FieldWorks entry `tu` whose one `LexEntryRef` is a complex-form ref (`ComplexEntryTypes` set, `VariantEntryTypes` empty, `RefType` 1) to the stem `ta`. HCLoader treats every entry ref of a sense-less entry as a variant source, whatever its type (`LoadLexEntries`, `HCLoader.cs:639-668`), and `GetInflTypes` yields the plain (null) type when `VariantEntryTypes` is empty (`HCLoader.cs:706-710`), so `tu` is loaded once under `ta`'s Noun MSA by `LoadLexEntryOfVariant` (`HCLoader.cs:782-856`), with `ta`'s morpheme name. An importer that models the ref as a complex form only never builds `tu`.

## What it pins

- `ta`: the main stem (control).
- `tu`: parses as `TA`, the variant copy under `ta`'s MSA.
- `tata`: no analysis. The grammar has no compounding rule, so the entry copy does not compound with its stem (control).

Without the `tu` entry the word has no analysis (checked at `ba6dfa10`).

## Grammar shape

`grammar.xml` is the per-copy form: one stratum holds `ta` and `tu`, both with `MorphemeId` `TA`. Nothing was converted from the staged grammar. The grammar cannot itself say the entry came from a complex-form ref, so what the fixture holds an importer to is the loader's behaviour on that ref, which this suite pins as the resulting grammar.

## Oracle

Every row was taken with `hc-conformance --propose` at sillsdev/machine `ba6dfa10` (tip of #615, the suite pin). The three staged rows, taken at `aab4c598`, replayed unchanged.

## FieldWorks source witness

None is stored. PanGloss staged a `fieldworks/project.fwdata` (authored with `xample-projector author --variant-of eTu=eTa`, then the `LexEntryRef` edited by hand to carry the stock "comp. of" type and `RefType` 1) without the `phonology-mutations.yaml` and `WritingSystemStore/` this suite's witness shape requires, and the hand edit is outside what section 3 of AGENTS.md allows. Its data was read against the loader: `tu` has no senses or MSAs, one `LexEntryRef` (`ComplexEntryTypes` `1f6ae209-141a-40db-983c-bee93af0ca3c`, no variant types, component `ta`) and one stem MoStemAllomorph; `ta` has a sense and a Noun MoStemMsa. That is the input `HCLoader` turns into this grammar. `fieldworks_producible: true` therefore rests on the loader source (FieldWorks origin/main `d36ff645`), not on a certified witness.

Source: PanGloss#174 (staging `conformance-staging/edge-cases/variant-complex-form-ref-senseless-entry`).
