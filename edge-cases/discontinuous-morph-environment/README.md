# discontinuous-morph-environment

A root allomorph with a Require environment (a following `u`), split into three pieces by a two-infix rule.

## Whole span, not each piece

The environment is tested once around the whole root span: to the left of the first root piece and to the
right of the last. The infix segments between the pieces are inside the word, not neighbours of the root.
So `zuexbu` (root `zeb`, infix `u` and `x`, suffix `u`) and `zuixdu` (root `zid`) parse: the suffix supplies the
`u` at the right edge of the span.

Earlier revisions of this fixture expected both words to have no parse, because the engine tested the
environment on each contiguous piece (the middle piece of `zuexbu` is followed by `x`). sillsdev/machine PR 631
changes the engine to the whole-span reading and these rows follow it.

## Open judgement call

No FieldWorks or XAmple source settles the infix case. FieldWorks stores a root allomorph environment as a plain
Require environment (`HCLoader.LoadRootAllomorph`, `HCLoader.cs:855-880`) and renders the infix in the
HermitCrab rule, so nothing there says whether the environment sees the infix segments. Whole span is the
best-supported reading (an environment describes the stem's neighbours), and it is a maintainer decision recorded
on sillsdev/machine#630. If the maintainers choose the per-piece reading, `zuexbu` and `zuixdu` go back to
`expect_fail: true`.

Suite PR 39 (`edge-cases/infix-split-root-allomorph-environment`) pins the same reading with a one-environment grammar.

## Results by engine build

| Build | `zuexbu`, `zuixdu` |
|---|---|
| sillsdev/machine master | no parse |
| sillsdev/machine PR 631 (head 787d7600) | parse |
