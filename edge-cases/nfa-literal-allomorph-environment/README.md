# Literal allomorph environment

The stem has a conditioned allomorph `gabs` before `a` and an elsewhere allomorph `gabas`.
The suffix and infix are synthetic. FieldWorks `HCLoader.LoadRootAllomorph` attaches a required
environment and `LoadEnvironmentPattern`/`LoadPatternNodes` build a literal segment as an unnamed
group. Machine's XML loader also builds the `<Segments>` node here as an unnamed group and inherits
the allomorph's character table. This is based on the loader source, without a FieldWorks witness.

Machine `4d9b454d` produced the recorded rows in `hc-conformance` self-check mode. Replacing the
`<Segments>` node with `<Segment segment="cA" />` produced the same five rows at that pin. An
earlier eight-word probe, which included infix-plus-suffix forms, also showed the same rows under
both encodings. Thus these words do not demonstrate a parse-selection difference caused by the
group's trailing epsilon; the test case records the reachable construction and its reference output.
It is not a failing-before regression for [PanGloss #300](https://github.com/sillsdev/PanGloss/issues/300).
