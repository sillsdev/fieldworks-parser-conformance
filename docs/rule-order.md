# Rule order is part of the contract

This is the order in which a conforming engine applies phonological and morphological rules. It is fixed
by the reference engine, so every consumer must reproduce it.

**Rule order is part of the contract, not an implementation detail.** A parse runs in two passes:
the word is **torn down** to find candidate stems, then **built back up** to check the rebuild
reproduces the surface it started from. This is analysis-by-synthesis — propose by stripping,
confirm by regenerating — and the engine's own vocabulary is *unapply* for the first pass and
*apply* for the second.

| Pass | Direction | Per-stratum order |
|---|---|---|
| **Analysis** — tearing down (`unapply`) | surface inward | phonological rules unapplied **first**, then affix templates and morphological rules |
| *lexical lookup* | the hinge | each stripped form is looked up for real lexical entries; `Morpher.Synthesize` calls this, so the engine places it at the **start of the build-up** |
| **Synthesis** — building up (`apply`) | stem outward | morphological rules and affix templates first, *mutually recursive* — each may invoke the other — then phonological rules **last** |

Strata run in declaration order building up, and reversed tearing down. Note the two passes are
mirror images: whatever runs last on the way up runs first on the way down.

Two consequences a consumer must reproduce. **Within one stratum pass a phonological rule cannot
feed a morphological rule or template** — phonology runs after morphology in synthesis and before it
in analysis — so that class of interaction does not exist and needs no coverage. **Across strata it
can**: stratum *N*'s phonological output is stratum *N+1*'s morphological input. And because
analysis is the inverse of synthesis, an interaction that *feeds* in one direction *bleeds* in the
other, so an interaction witnessed only in synthesis is untested in the direction a proposer runs.

The order is fixed by the engine, not by the grammar: the reference engine builds it as an unconditional cascade, which is also why
`Stratum/cyclicity` and `phonologicalRuleOrder` are inert — there is no branch point for them to
select.

`PROTOCOL.md` specifies the adapter contract in engine-agnostic terms; nothing in this repository depends on
any engine's build, layout, or language. The C# HermitCrab supplies the seed construct vocabulary
(`constructs.txt`) and is the **founding oracle** that generated every fixture's ground truth, but it is not a
hard boundary: any engine that implements `PROTOCOL.md`'s contract can be validated here, declaring a partial
**capability profile** (e.g. morphotactics-only, no phonological rules) to be measured fairly against just the
subset it claims to support.
