# narrowing-boundary-order-alpha-lhs

An obligatory rewrite rule `prSpirant` whose input is a vowel, a morpheme boundary and a stop carrying an alpha voicing variable, `V + [stop alpha-voice] -> V [fricative alpha-voice]`, with no environment. The grammar has one root `aa` and four suffixes `+pa`, `+ba`, `+fa`, `+va`. The rule has three nodes on the left (segment, boundary, segment) and two on the right, so analysing a word means undoing it by narrowing across the boundary: the vowel comes back, the boundary node comes back as an optional marker, and the surface fricative is widened back to a stop with the variable carried over. It is the boundary-order companion of `narrowing-boundary-first-alpha-lhs`, where the boundary is the first node.

## What it pins

- `aafa`: two parses. `AA+FA` (the suffix is underlying `f`, the rule does not apply, the boundary survives as the optional marker in `aa+?fa`) and `AA+PA` (underlying `p` spirantized to `f` after the root's vowel, voicelessness kept by the variable).
- `aava`: two parses, `AA+VA` and `AA+BA`, the same pair with voiced segments.
- `aapa`, `aaba`: no analysis. The rule is obligatory after the root's final vowel, so a stop never surfaces there. These are the negative controls.

With `prSpirant` removed from the stratum, `aafa` and `aava` lose their `AA+PA` and `AA+BA` parses and `aapa` and `aaba` parse, so the rule alone causes each row (checked at `ba6dfa10`).

## Grammar shape

Nothing was converted from the staged grammar, which is the staged file byte for byte (its leading XML comment still says "Staged for PanGloss issue 33").

`fieldworks_producible: true` rests on `HCLoader.cs`, not on a witness; see `narrowing-boundary-first-alpha-lhs` for the reading. `LoadPhonologicalRule` builds the left-hand side from every `IPhSimpleContext` in `StrucDescOS` through `LoadPatternNode`, which handles a boundary-marker context (FieldWorks `origin/main` `d36ff645`). PanGloss staged this test case as `false` because FieldWorks' rule editor offers boundary markers only in environments; the census does not forbid a boundary in the input, and `edge-cases/boundary-first-in-narrowing-lhs` (flagged `true`) has the same shape. A FieldWorks project whose rule input holds a boundary is not witnessed.

## Reference

Every row was taken with `hc-conformance --propose` at sillsdev/machine `ba6dfa10` (tip of #615, the suite pin). All four staged rows, verified at `c2454760` (which contains sillsdev/machine#539), replayed unchanged.

Source: PanGloss#33 (staging `conformance-staging/edge-cases/narrowing-boundary-order-alpha-lhs`, divergence 087).
