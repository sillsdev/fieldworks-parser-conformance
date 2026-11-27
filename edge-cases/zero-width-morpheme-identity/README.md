# zero-width-morpheme-identity

Synthetic. A root `sag` (noun), two overt category toggles (`mrA2B`: noun to verb, suffix `u`; `mrB2A`: verb to noun, suffix `i`) and a zero-width rule `mrThird` (noun to verb, copies the stem, inserts nothing). Un-applying `mrThird` maps a shape to itself, so the same surface can be reached through different rule histories (sillsdev/machine#506, #500).

## What it pins

- `sag`: two analyses, the bare root and root plus `mrThird`.
- `sagu`: root plus `mrA2B` (control that the toggle works alone).
- `sagi`, `sagui`: the toggles and the zero-width rule combined; `sagui` is the word that gave three different answers across fresh-process runs of an earlier build. Its answer is stable at ba6dfa10 with one thread (machine#506, comment 7219130646), so it is pinned from the C# run.

## Existing fixtures considered

- `convergent-zero-derivation-identity`: the closest. Its null affixes insert the boundary pair `+∅` and sit beside homophonous overt suffixes, and its words test the convergence of those homophones. The cases here need a zero-width rule that inserts nothing (not even a boundary pair) and toggles of the category in a cycle; adding that rule would change which words in the other fixture are ambiguous, so it was not extended.
- `truncate-morphotactic-identity` and `strrep-identity`: identity rules by truncation or string replacement, with different input conditions and no category cycle.
- `edge-cases/truncate-morphotactic`: a truncation rule, not a zero-width one.

## Oracle

C# HermitCrab at sillsdev/machine `ba6dfa10`, self-check (`hc-conformance --propose`), one thread. Provenance: `founding-oracle machine-commit=ba6dfa10 verified-date=2026-11-27`. The grammar was staged by PanGloss; no row comes from PanGloss.

## FieldWorks producibility

A zero-width affix form is loadable by HCLoader (`IsValidRuleForm`, `LoadAffixProcessAllomorph`, which accepts a rule whose form inserts nothing). `fieldworks_producible: true`.
