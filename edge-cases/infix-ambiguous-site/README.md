# infix-ambiguous-site

An infix whose environment matches at more than one place in the stem. The root `mime` has two vowels, so
`mrAfter` (insert `gu` after a vowel) and `mrBefore` (insert `gu` before a vowel) can each go in two places.
All lexemes are invented.

| Word | Reading | C# oracle (4d9b454d) |
|---|---|---|
| `migume` | `mrAfter` at the first vowel | parses |
| `mimegu` | `mrAfter` at the last vowel, empty right part | no parse |
| `mimgue` | `mrBefore` at the last vowel | parses |
| `mguime` | `mrBefore` at the first vowel | no parse |

The oracle applies an affix-process allomorph at one place only (`SynthesisAffixProcessRule` takes
`SingleOrDefault` of the anchored match), and a parse is kept only if re-synthesis reproduces the word
(`Morpher.IsWordValid`). So the oracle's parse set is its synthesis output, not every legal reading. Its
determinized matcher prefers the greedy `any*` branch (High-priority quantifier arcs, determinized in arc order).
The two `expect_fail` rows record that the other site is never synthesized; they are not a claim that the other
reading is wrong.

Both grammars use the two-part shape HCLoader writes for a form-allomorph infix
(`HCLoader.LoadFormAffixProcessAllomorph`, infix branch): left = `any*` + left context, right = right context +
`any*`. The `+` boundary segments FieldWorks adds around the form are omitted, as in most fixtures here.

Bug source: the Rust port. PanGloss up to 0.19.5 failed `mimgue` and `mguime` because its matcher NFA and subset
construction differed from C# (arc priority types, arc insertion order, epsilon-closure keying), so it took the
first site. Reported as sillsdev/PanGloss#297 and fixed by PanGloss#299; PanGloss 0.19.6 passes every word. C#
itself is not at fault. Related: sillsdev/machine#630 and #638 (same comparator family), and conformance #39
(`infix-split-root-allomorph-environment`, a different problem).
