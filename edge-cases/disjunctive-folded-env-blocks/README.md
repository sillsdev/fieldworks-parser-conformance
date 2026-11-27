# disjunctive-folded-env-blocks

Pins sillsdev/PanGloss#444 (Motif #316). One suffix rule `mrDat` has two allomorphs, in this order:

- allomorph 0, input `stem* n`, adds `ka`: what `HCLoader.cs` builds for a FieldWorks suffix allomorph with the
  environment `/ n _`. The left context is folded into the input pattern and no `AllomorphEnvironment` is written
  (`Environments` is empty).
- allomorph 1, input `stem+`, adds `ku`: the lexeme form.

Roots `ban` and `bas`. C# HermitCrab's disjunctive property (`SynthesisAffixProcessRule`) stops after an allomorph
that produced output when it has no environments and does not free-fluctuate with the next one, so `banku` is
never offered allomorph 1: allomorph 0 matches the stem `ban`, the word it builds is `banka`, validity rejects
it against the surface, and `ban+ku` has no parse. This is documented HermitCrab behaviour, not a defect. PanGloss
agrees on the result; its guided synthesis discards allomorph 0's output silently rather than rejecting it
later, which is the explanation gap in PanGloss#444.

| word | C# result | pins |
|---|---|---|
| `banku` | no parse | the #444 shape |
| `basku` | `bas+DAT` | control: allomorph 0 does not match `bas`, allomorph 1 applies |
| `banka` | `ban+DAT` | the alternate itself still parses |
| `ban` | bare root | control |

The rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`, the tip of
machine #615 returned in `hc-conformance` self-check mode.
FieldWorks producibility is read from `HCLoader.cs` (`LoadFormAffixProcessAllomorph`); no `fieldworks/` witness is
claimed.
