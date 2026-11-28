# compound-homophonous-suffixes

A right-headed noun-noun and a left-headed verb-noun endocentric compound rule beside four homophonous
category-changing suffixes.

**Optimization risk.** The suffixes converge on one shape before the compounding rules are tried on it, and
again on the head after a compound is split. If the skip is ever extended to compounding rules, compound rows
would depend on the root filter, which is not part of the shape: this test case pins the compound path.

**Why it is producible.** The compounding rules are the endocentric shape `LoadEndoCompoundingRule` writes
(head and non-head any one or more segments, joined by `+`); the noun-noun rule carries the compound `maxApps`
setting, which the loader reads for endocentric rules.

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
