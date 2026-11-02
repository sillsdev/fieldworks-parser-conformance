# right-to-left-segments-environment

A right-to-left iterative rewrite rule whose subrule has a literal right context: "a" becomes "e"
only when the next segment is "y". The context is the segment "y" (what an `IPhSimpleContextSeg`
lowers to).

- `ey`: ROOT1 ("ay" underlying) with "a" rewritten to "e" because "y" follows.
- `a`: ROOT2, unchanged; no "y" follows, so the rule does not fire.
- `ay`: `expect_fail`. ROOT1's raw underlying shape is not a surface form, because the rule is
  obligatory wherever its context matches.
- `e`, `y`: `expect_fail`; no root produces either.

Graduated from PanGloss staging in Machine PR #480. The grammar was once authored with an inline
`<Segments>` literal in the environment, a shape FieldWorks cannot write (README row 1); it is now
the plain segment.
