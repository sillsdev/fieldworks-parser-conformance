# adhoc-prohibition-affix-environment-copies

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `affix-environment` | `edge-cases/adhoc-prohibition-affix-environment-copies` | [XAmple] a prohibition on a prefix allomorph that has two environments and two morphosyntactic analyses. | unchanged |
| `affix-msa` | `edge-cases/adhoc-prohibition-affix-msa-copies` | [XAmple] a prohibition on a prefix entry that has two morphosyntactic analyses. | `a`→`f`, `b`→`h`, `d`→`j`, `g`→`l`, `t`→`m` |
| `circumfix-pairings` | `edge-cases/adhoc-prohibition-circumfix-pairings` | [XAmple] a prohibition that names a circumfix, which pairs with each of its prefix and suffix halves. | `a`→`n`, `b`→`p`, `d`→`q`, `g`→`r`, `i`→`s`, `k`→`v`, `o`→`w`, `t`→`x` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-9). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `affix-environment`: former README of `adhoc-prohibition-affix-environment-copies`

### adhoc-prohibition-affix-environment-copies

Synthetic. An ad hoc allomorph prohibition on a prefix allomorph that has two environments and two equal MoInflAffMsas (MergeMSAs off). HCLoader registers one allomorph per MSA per environment (HCLoader.cs:1160-1178), so the one FieldWorks allomorph compiles to four copies (`subTa1a`, `subTa1b`, `subTa2a`, `subTa2b`), and the prohibition is attached to every copy, on the first side and on the rest side (HCLoader.cs:2212-2236). The model is PanGloss's `adhoc-affix-environment-copies` test case.

#### What it pins

- `da`, `ba`, `ga`: parse.
- `taga` (no prohibition): two analyses, one per prefix MSA, both through the before-consonant copy, whose consonant class is the first node of its stem pattern (HCLoader folds a prefix's right context into the input pattern; the after-`a` environment never matches a word-initial prefix).
- `tada`: prefix first, one rule per copy: no analysis. Only the before-consonant copies match, so a rule on the first environment copy alone does not suppress it.
- `taba`: stem first, one rule per copy on the rest side: no analysis.

#### Reference

hc.dll at Machine `aab4c598`, self-check (`hc-conformance --fixtures`) PASS on signatures and traced rules. Provenance: `founding-oracle machine-commit=aab4c598 verified-date=2026-10-30`.

#### FieldWorks witness

`fieldworks/project.fwdata` is backed out of `grammar.xml` via LibLCM, not hand-edited: the `author` command of the PanGloss `xample-projector` tool (kept in the PanGloss repository, not here), extended (extended with MSA-copies, environment-copies, circumfix and variant-entry options; the patch is not part of this repository) with `--msa-copies`, `--env-copies`, `--variant-of`, circumfix rules and `--half-prohib`. FieldWorks 9.3.10.1452, LibLCM 11.0.0.55173.
`author --grammar grammar.xml --name AdhocEnv --msa-copies mrTa1,mrTa2 --env-copies subTa1a,subTa1b --env-copies subTa2a,subTa2b   (ParserParameters gets MergeMSAs=false)`
The authored project has one prefix allomorph with two PhoneEnvRC environments, two MoInflAffMsas, and two MoAlloAdhocProhibs (one per direction). Loaded back through HCLoader it emits the same four copies per MSA pair and eight AllomorphCoOccurrenceRules.
`phonology-mutations.yaml` `base_sha256` matches the project; the `remove-t-only` case ran through `mutate` (exit 0). (`g` is referenced by the environment's natural class, so the removal case names `t`.)

#### Verification

grammar.xml on hc.dll: da, ba, ga parse; taga TA1+GA, TA2+GA; tada, taba none. FieldWorks project through projector and hc.dll: same counts (the HC XML has no morph names, so only counts compare: da 1, ba 1, ga 1, taga 2, tada 0, taba 0).
Controls (not kept here): rule only on the two after-`a` copies (the first environment pass of each MSA): tada and taba both parse twice; rule on the first MSA's before-consonant copy only: tada TA2+DA, taba TA2+BA; rule on the last copy only: tada TA1+DA, taba TA1+BA.

Source: PanGloss-only (Rust) compile-step issues, not reference bugs.

### Cell `affix-msa`: former README of `adhoc-prohibition-affix-msa-copies`

### adhoc-prohibition-affix-msa-copies

Synthetic. An ad hoc allomorph prohibition on a prefix entry with two equal MoInflAffMsas (MergeMSAs off), so one prefix allomorph compiles to two morphological rules. HCLoader attaches the prohibition to every copy, on the first side and on the rest side; a loader that kept one allomorph per allomorph identity reached only one prefix copy.

#### What it pins

- `da`, `ba`, `ga`: parse.
- `taga` (no prohibition): two analyses, one per prefix copy.
- `tada`: prefix-first, one rule per prefix copy: no analysis.
- `taba`: stem-first, one rule per prefix copy on the rest side: no analysis.

#### Reference

hc.dll at Machine `aab4c598`, self-check (`hc-conformance --fixtures`) PASS on signatures and traced rules. Provenance: `founding-oracle machine-commit=aab4c598 verified-date=2026-10-31`.

#### FieldWorks witness

`fieldworks/project.fwdata` is backed out of `grammar.xml` via LibLCM, not hand-edited: the `author` command of the PanGloss `xample-projector` tool (kept in the PanGloss repository, not here), extended with `--msa-copies` and `--variant-of` (extended with an MSA-copies and variant-entry option; the patch is not part of this repository). FieldWorks 9.3.10.1452, LibLCM 11.0.0.55173.
`author --grammar grammar.xml --name AdhocAffix --msa-copies mrTa1,mrTa2   (ParserParameters gets MergeMSAs=false)`
`phonology-mutations.yaml` `base_sha256` matches the project; the `remove-g-only` case ran through `mutate` (exit 0).

#### Verification

FieldWorks project through projector and hc.dll: da 1, ba 1, ga 1, taga 2, tada 0, taba 0. Control with the rules on one prefix copy only (not kept here): tada parses as TA1+DA (rule on copy 2) or TA2+DA (rule on copy 1), likewise taba.

Source: PanGloss-only (Rust) compile-step issues, not reference bugs.

### Cell `circumfix-pairings`: former README of `adhoc-prohibition-circumfix-pairings`

### adhoc-prohibition-circumfix-pairings

Synthetic. An ad hoc allomorph prohibition naming a circumfix lexeme form. A FieldWorks circumfix entry has a circumfix-type lexeme form plus prefix and suffix alternate forms; HCLoader emits one allomorph per prefix half x suffix half pairing (HCLoader.cs:1097-1122; here ta/to x ka/ki = four subrules) and registers all of them under `entry.LexemeFormOA`, so the prohibition reaches every pairing (HCLoader.cs:2212-2236).

#### What it pins

- `da`, `ba`, `ga`: parse.
- `tagaka`, `tagaki`, `togaka`, `togaki`: one analysis each. `ga` also carries FieldWorks prohibitions that name only the prefix half `ta` (half first and stem first). A half is not a key of HCLoader's allomorph table, so they resolve to no rule: this is the "still parses" control, and `grammar.xml`, as HCLoader emits it, has no rule for them.
- `tadaka`, `tadaki`, `todaka`, `todaki`: circumfix first, one rule per pairing: no analysis.
- `tabaka`, `tabaki`, `tobaka`, `tobaki`: stem first, one rule per pairing: no analysis.

#### Reference

hc.dll at Machine `aab4c598`, self-check PASS on signatures and traced rules. Provenance: `founding-oracle machine-commit=aab4c598 verified-date=2026-10-30`.

#### FieldWorks witness

`fieldworks/project.fwdata` is backed out of `grammar.xml` via LibLCM, not hand-edited: the `author` command of the PanGloss `xample-projector` tool (kept in the PanGloss repository, not here), extended (extended with MSA-copies, environment-copies, circumfix and variant-entry options; the patch is not part of this repository) so that a rule whose subrules are the prefix x suffix cross product becomes one circumfix entry (created through `ILexEntryFactory.Create`, which makes the first prefix and suffix halves itself; the other halves are added) and `--half-prohib` adds the half-only prohibitions. FieldWorks 9.3.10.1452, LibLCM 11.0.0.55173.
`author --grammar grammar.xml --name AdhocCirc --half-prohib aGa=mrCirc:ta`
The authored project has one circumfix entry (lexeme form `ta- -ka`, halves ta, to, ka, ki), two MoAlloAdhocProhibs naming the circumfix lexeme form (one per direction) and two naming the half `ta` on `ga`. Loaded back through HCLoader it emits four pairing subrules and eight AllomorphCoOccurrenceRules; the half-only prohibitions add none.
`phonology-mutations.yaml` `base_sha256` matches the project; the `remove-g-only` case ran through `mutate` (exit 0).

#### Verification

grammar.xml on hc.dll: ga words 1 analysis each, da/ba words none. FieldWorks project through projector and hc.dll: same (da 1, ba 1, ga 1, ga words 1 each, all eight da/ba words 0).
Controls : rule on the ta-...-ka pairing only: only tadaka and tabaka are lost; rule on the to-...-ki pairing only: only todaki and tobaki are lost; no rule: all sixteen parse.

Source: PanGloss-only (Rust) compile-step issues, not reference bugs.
