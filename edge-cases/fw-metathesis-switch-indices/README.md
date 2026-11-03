# fw-metathesis-switch-indices

Synthetic. A FieldWorks metathesis rule (`PhMetathesisRule`) with one left environment context and two switch contexts: structural description `a t k`, `StrucChange` `0 2 -1 1 -1`, so the left switch index is 1 (`t`) and the right switch index is 2 (`k`). HCLoader names the context at the right switch index `r` and the one at the left switch index `l`, and `XmlLanguageWriter` writes them as `leftSwitch="prule1_r"` and `rightSwitch="prule1_l"`; the rule turns `atk` into `akt`.

## What it pins

- `akta`, `aktas`: R0 (underlying `atka`) surfaces swapped. `atka`, `atkas` have no analysis.
- `itka`, `itkas`, `tika`, `tikas`: controls, the left environment `a` does not hold, so the forms surface unchanged. `ikta`, `kita`, `kitas`: no analysis.

## Oracle

hc.dll shipped with FieldWorks 9.3.10 (SIL.Machine.Morphology.HermitCrab): the live `HCLoader` language built from `fieldworks/project.fwdata` and `XmlLanguageLoader` on this `grammar.xml` give the same analysis count for all 11 words (`xample-projector parse-hc`, `projectionAgrees` true). Signatures and rule traces were read from PanGloss's engine, whose counts equal those; `hc-conformance --fixtures` (sillsdev/machine, run on this fixture alone) reports 1 passed, 0 failed, so the C# engine confirms the expectations.

## FieldWorks witness

`fieldworks/project.fwdata` is not hand-edited. It was authored with the PanGloss `xample-projector` tool: `author` from a plain grammar (three roots and a suffix), then `configure-probe` with `feature-class` (`distinct`, so each phoneme has its own identity feature) and the new `metathesis` operation (`description` `[a, t, k]`, `leftEnv` 0, `leftSwitch` 1, `rightSwitch` 2). `project` (HCLoader + XmlLanguageWriter) then produced the rule and character definitions in `grammar.xml`; this fixture removes the per-object `Properties` (session-specific handles) and adds `MorphemeId` (HCLoader writes none) so signatures name morphemes. FieldWorks 9.3.10, LibLCM 11.
`phonology-mutations.yaml` carries no cases: every phoneme is referenced by the rule or its natural class, so neither mutation vocabulary operation can run with `require_unreferenced`. `base_sha256` matches the project.

## Not pinned

A rule with a middle context (one segment between the two switches) behaves differently in hc.dll and in PanGloss; it is recorded in the PanGloss pull request, not here.
