# infix-ambiguous-site

An infix whose environment matches at more than one place in the stem. The root `mime` has two vowels, so
`mrAfter` (insert `gu` after a vowel) and `mrBefore` (insert `gu` before a vowel) can each go in two places.

| Word | Reading | C# oracle (4d9b454d) | PanGloss 0.19.5 |
|---|---|---|---|
| `migume` | `mrAfter` at the first vowel | parses | parses |
| `mimegu` | `mrAfter` at the last vowel, empty right part | no parse | no parse |
| `mimgue` | `mrBefore` at the last vowel | parses | no parse |
| `mguime` | `mrBefore` at the first vowel | no parse | parses |

The oracle applies an affix-process allomorph at one place only (`SynthesisAffixProcessRule` takes
`SingleOrDefault` of the anchored match), and a parse is kept only if re-synthesis reproduces the word
(`Morpher.IsWordValid`). So the oracle's parse set is its synthesis output, not every legal reading. The two
`expect_fail` rows record that; they are not a claim that the other reading is wrong.

Both grammars use the two-part shape HCLoader writes for a form-allomorph infix
(`HCLoader.LoadFormAffixProcessAllomorph`, infix branch): left = `any*` + left context, right = right context +
`any*`. The `+` boundary segments FieldWorks adds around the form are omitted, as in most fixtures here.

The two rows where PanGloss differs are `mimgue` and `mguime`. See the PanGloss issue linked from
sillsdev/machine#480 for the cause.
