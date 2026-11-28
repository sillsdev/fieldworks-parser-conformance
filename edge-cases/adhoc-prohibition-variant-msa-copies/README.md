# adhoc-prohibition-variant-msa-copies

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `variant-msa` | `edge-cases/adhoc-prohibition-variant-msa-copies` | [XAmple] a morpheme prohibition on one analysis of a stem that has a variant entry. | unchanged |
| `stem-msa` | `edge-cases/adhoc-prohibition-stem-msa-copies` | [XAmple] a prohibition on a stem entry that has two morphosyntactic analyses. | `a`→`f`, `b`→`h`, `d`→`j`, `g`→`k`, `t`→`m` |
| `allomorph-control` | `edge-cases/adhoc-prohibition-allomorph-variant-control` | [XAmple] a control for the variant cases, with an allomorph prohibition between a variant stem and a prefix. | `a`→`n`, `i`→`o`, `l`→`p`, `t`→`q` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-9). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `variant-msa`: former README of `adhoc-prohibition-variant-msa-copies`

### adhoc-prohibition-variant-msa-copies

Synthetic. An ad hoc MORPHEME prohibition on the Verb MSA of a stem entry that has a variant entry (no senses, no MSAs, one variant LexEntryRef to the main entry). HCLoader registers the variant once per main MSA under the MAIN entry's MSA (AddEntry, HCLoader.cs:728-735; LoadLexEntryOfVariant, 782-852) and attaches one rule per copy (LoadMorphemeCoOccurrenceRules, 2262-2290), so the prohibition holds for the variant too. A loader that covered the main entry only still parsed the variant.

#### What it pins

- `da`, `di`, `ba`, `bi`, `ga`, `gi`: parse as Noun and Verb.
- `taga`, `tagi` (no prohibition): parse once.
- `tada`, `tadi`: stem-first prohibition on the main Verb MSA: no analysis for main or variant.
- `taba`, `tabi`: prefix-first prohibition, one rule per rest-side copy (main, variant): no analysis.

Enclitic directions and the allomorph-kind variant control are pinned by `adhoc-prohibition-variant-enclitic-first`, `adhoc-prohibition-variant-main-first-enclitic` and `adhoc-prohibition-allomorph-variant-control`.

#### Reference

hc.dll at Machine `aab4c598`, self-check (`hc-conformance --fixtures`) PASS on signatures and traced rules. Provenance: `founding-oracle machine-commit=aab4c598 verified-date=2026-10-31`.

#### FieldWorks witness

`fieldworks/project.fwdata` is backed out of `grammar.xml` via LibLCM, not hand-edited: the `author` command of the PanGloss `xample-projector` tool (kept in the PanGloss repository, not here), extended with `--msa-copies` and `--variant-of` (extended with an MSA-copies and variant-entry option; the patch is not part of this repository). FieldWorks 9.3.10.1452, LibLCM 11.0.0.55173.
`author --grammar grammar.xml --name AdhocVariant --msa-copies eDaV,eDaN --msa-copies eBaV,eBaN --msa-copies eGaV,eGaN --variant-of eDiV=eDaV --variant-of eDiN=eDaN --variant-of eBiV=eBaV --variant-of eBiN=eBaN --variant-of eGiV=eGaV --variant-of eGiN=eGaN`
`phonology-mutations.yaml` `base_sha256` matches the project; the `remove-g-only` case ran through `mutate` (exit 0).

#### Verification

FieldWorks project through projector and hc.dll: da/di/ba/bi/ga/gi 2 each, taga 1, tagi 1, tada/tadi/taba/tabi 0. Controls (not kept here): no rule: tadi and tabi parse; rule on the main entry only: tadi and tabi parse (TA+DAV, TA+BAV).

Source: PanGloss issues #99 and #100 (fixes in PanGloss PRs #101 and #102).

### Cell `stem-msa`: former README of `adhoc-prohibition-stem-msa-copies`

### adhoc-prohibition-stem-msa-copies

Synthetic. An ad hoc allomorph prohibition on a stem entry with two stem MSAs (Verb first, Noun second) and a Verb-only prefix ta-. HCLoader attaches the prohibition to every MSA copy of the stem allomorph (HCLoader.cs:2163-2189), in both directions; a loader that kept one allomorph per allomorph identity wired it to the last (Noun) copy only and still parsed the prefixed word through the Verb copy.

#### What it pins

- `da`, `ba`, `ga`: parse as Noun and Verb.
- `taga` (no prohibition): parses once, on the Verb copy.
- `tada`: prefix-first prohibition, rest side has both copies of da: no analysis.
- `taba`: stem-first prohibition on each copy of ba: no analysis.

#### Reference

hc.dll at Machine `aab4c598`, self-check (`hc-conformance --fixtures`) PASS on signatures and traced rules. Provenance: `founding-oracle machine-commit=aab4c598 verified-date=2026-10-31`.

#### FieldWorks witness

`fieldworks/project.fwdata` is backed out of `grammar.xml` via LibLCM, not hand-edited: the `author` command of the PanGloss `xample-projector` tool (kept in the PanGloss repository, not here), extended with `--msa-copies` and `--variant-of` (extended with an MSA-copies and variant-entry option; the patch is not part of this repository). FieldWorks 9.3.10.1452, LibLCM 11.0.0.55173.
`author --grammar grammar.xml --name AdhocStem --msa-copies eDaV,eDaN --msa-copies eBaV,eBaN --msa-copies eGaV,eGaN`
`phonology-mutations.yaml` `base_sha256` matches the project; the `remove-g-only` case ran through `mutate` (exit 0).

#### Verification

Replaying the fieldworks project through `XampleProjector project` (HCLoader.Load + XmlLanguageWriter) and hc.dll: da 2 analyses, ba 2, ga 2, taga 1, tada 0, taba 0, matching grammar.xml. Control with the rules on the last copy only (not kept here): tada parses as TA+DAV, taba as TA+BAV.

Source: PanGloss issues #99 and #100 (fixes in PanGloss PRs #101 and #102).

### Cell `allomorph-control`: former README of `adhoc-prohibition-allomorph-variant-control`

### adhoc-prohibition-allomorph-variant-control

Synthetic. Control for the morpheme-kind variant cases: an ad hoc ALLOMORPH prohibition between the stem allomorph of a variant entry and a Verb-only prefix allomorph. HCLoader loads the variant once per main MSA, each copy with its own allomorph object (LoadLexEntryOfVariant, HCLoader.cs:782-852), and keys an allomorph prohibition by that allomorph (LoadAllomorphCoOccurrenceRules, HCLoader.cs:2212-2236), so the one MoAlloAdhocProhib [variant allomorph, ta-] becomes one AllomorphCoOccurrenceRule per variant copy and never reaches the main entry's allomorph.

#### What it pins

- `la`, `li`: parse as Noun and Verb.
- `tala` (control): the prohibition names the variant allomorph only, so the Verb-only prefix still attaches to the main stem: `TA+LAV` once.
- `tali`: variant allomorph first: the variant's Verb copy is excluded with `ta-`: no analysis. A loader that dropped the prohibition would parse `TA+LAV|tali`; one that spread it to the main entry would also lose `tala`.

Not covered here: morpheme-kind prohibitions over variants (the two enclitic cases and `adhoc-prohibition-variant-msa-copies`).

#### Reference

hc.dll at Machine `aab4c598`, self-check (`hc-conformance --fixtures`) PASS on signatures and traced rules. Provenance: `founding-oracle machine-commit=aab4c598 verified-date=2026-10-31`.

#### FieldWorks source witness

`fieldworks/project.fwdata` is backed out of `grammar.xml` via LibLCM, not hand-edited: the `author` command of the PanGloss `xample-projector` tool (kept in the PanGloss repository, not here), with `--msa-copies` and `--variant-of`. FieldWorks 9.3.10.1452, LibLCM 11.0.0.55173.
`author --grammar grammar.xml --name adhocprohibitionallomorphvariantcontrol --msa-copies eLaV,eLaN --variant-of eLiV=eLaV --variant-of eLiN=eLaN`
`phonology-mutations.yaml` `base_sha256` matches the project; the `empty-phoneme-inventory` and `remove-i-only` cases ran through `mutate` (exit 0).

#### Verification

FieldWorks project through projector and hc.dll (FieldWorks 3.8.2.0 and the pinned build give the same counts), and `grammar.xml` through `hc-dotnet-wrapper.sh`: la/li 2 each, tala 1, tali 0. Controls (not kept here): no prohibition: `tali` parses once (TA+LAV).

Source: sillsdev/machine #480 (ad hoc prohibition conformance); the PanGloss staging copy is conformance-staging/edge-cases in sillsdev/PanGloss.
