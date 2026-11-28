# deletion-optional-reduplication

An h-deletion rule undone before CV reduplication and four homophonous suffixes.

**Optimization risk.** Undoing the deletion puts an optional `h` before every consonant, so the reduplication
pattern `[C^1][V^1]` is matched on shapes with optional segments inside and between the copies. A skip must
compare the optional flags on shape nodes: two shapes that differ only in an optional mark are different.
`kahta` and `kakahta` stay rejected.

**Why it is producible.** The rule is an ordinary deletion (empty output) with a right environment; the
reduplication is the bracket pattern `LoadReduplicationPatterns` turns into two copies of the same input parts.

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
