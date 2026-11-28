# zero-derivation-identity

Three null affixes (noun to verb, verb to noun, noun to noun, each inserting `+∅`) beside two
homophonous `-ti` suffixes that differ in category.

**Optimization risk.** Un-applying a null affix maps a shape to itself, so every rule is retried on an
unchanged shape under a different rule history. The per-path gates (category, one application per rule) must
still decide every arrival: `kattititi` stays rejected and the multiplicities of `kat`, `katti` and `sumsu`
must not change. This is the test case with the most table hits.

**Why it is producible.** FieldWorks writes an affix whose form is empty as `+∅`
(`LoadDerivAffixProcessRule`, null-affix form handling); see `edge-cases/authored-null-affix-allomorph`.

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
