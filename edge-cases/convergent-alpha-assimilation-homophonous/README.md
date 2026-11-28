# alpha-assimilation-homophonous

Nasal place assimilation written with one feature variable, a nasal-final prefix `an-` and four homophonous
suffixes.

**Optimization risk.** Undoing the assimilation leaves an underspecified nasal whose variable is unresolved in
the shape, and `an-` is retried on that shape once per homophonous suffix. A skip of the re-match must key on
the feature lanes and the unresolved variables, not on the segment letters alone.

**Why it is producible.** The suffixes are as FieldWorks writes them (`LoadDerivAffixProcessRule`); the variable
sits in a phonological rule, where FieldWorks allows it (`LoadFeatureConstraints`).

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
