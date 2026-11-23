# family-blocked-generation

Stem family `famF` holds A (`aa`) and B (`aat`); suffix T appends `t`, so A+T and B share the surface `aat`
and B, a family relative, blocks A+T. Pins sillsdev/PanGloss#423 (fixed by #432).

The second `B|aat` row for `aat` is the blocked A+T derivation. C# HermitCrab (Word.cs, `CheckBlocking`)
turns it into a fresh B seed, so the parse returns two derivations with the same signature: the plain lookup
of B and the blocked A+T. C#'s `ValueEquals` dedup does not collapse them. The suite compares multisets
(PROTOCOL.md sections 3 and 4.3), so the duplicate is pinned. PanGloss currently reports one `B|aat`, a
multiplicity divergence tracked in PanGloss#423 and #432.

The rows are what C# HermitCrab (sillsdev/machine `e63b8863d37d3189c2b11fcaf9d43be74962ad70`, the tip of
machine #615, see [PROVENANCE.md](../../PROVENANCE.md)) returned on a `hc-conformance` run over this grammar
and word list. The forward direction (`GenerateWords(A, [T])` returns `aat`; PanGloss returned nothing) cannot
be expressed in `words.yaml` and is asserted in PanGloss.

FieldWorks producibility is read from `HCLoader.cs`; no `fieldworks/` witness is claimed.
