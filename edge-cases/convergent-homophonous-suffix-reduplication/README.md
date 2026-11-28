# homophonous-suffix-reduplication

A CV reduplication prefix `[C^1][V^1]` beside four homophonous category-changing suffixes and two homophonous
agreement suffixes in one optional slot of a verb template.

**Optimization risk.** The reduplication rule is retried on one shape (`kukuma`, `titisu`) once per homophonous
suffix un-applied above it, while the copy-agreement check (`prune_disagreeing_copies`) decides the result.
`tikumasi` and `kutisusi` must stay rejected on every arrival; the prune flag must stay part of the skip's key.
`kukumasina` adds two homophonous template-slot fillers.

**Why it is producible.** The prefix is the bracket pattern `LoadReduplicationPatterns` writes; the slot
suffixes sit in a template and not in the stratum's rule list, as the loader places inflectional slot affixes.

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
