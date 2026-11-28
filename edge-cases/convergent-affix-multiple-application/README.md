# affix-multiple-application

Four suffixes spelled `ta`: noun-to-noun (`multipleApplication` 2), verb-to-verb (3) and two category changers
(1). Un-applying them reaches one shape by paths with different per-rule counts.

**Optimization risk.** A match table keyed on the shape must not carry a count decision from another path.
`kattatata` and `kattatatata` pin the exact multiset of rule applications; the count is read from the word's
trail in the caller after a table hit.

**Why it is producible.** Same as `affix-multiple-application`: FieldWorks gives an affix rule its cap from the
ParserParameters entry `HC/AffixRules/AffixRule[@guid][@maxApps]`, read in `HCLoader.cs` 131-138 and applied at
970-971, clamped to 1..10 (`docs/fieldworks-cannot-say.md` row 22). The reader is sillsdev/FieldWorks#1263 at
`0ead571c65df55e88525fe19a1a20e1d1ffe0054` (LT-22699), **not yet merged**: re-point the citation here, in
`status.yaml`, in `fieldworks-writable-shapes.tsv` and in row 22 when it lands. The strata
are `unordered`, as every FieldWorks stratum is.

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
