# clitic-stratum-homophonous

Three enclitics in the Clitics stratum spelled like four derivational suffixes in the Morphology stratum.

**Optimization risk.** One shape is reached in both strata by different rules. A skip keyed on the shape alone,
without the rule (which fixes the stratum), would mix the two strata's rows.

**Why it is producible.** Both strata are the unordered `Morphology` and `Clitics` strata `HCLoader.cs` writes;
the clitics are placed by `LoadCliticAffixProcessRule` (1079), the suffixes by `LoadDerivAffixProcessRule`.

**Guards.** sillsdev/machine#653: analysis re-matches the same rule on the same shape once per parent path, and the
planned fix skips the re-match. This test case's rows must stay identical (same parses, same multiset) after that
optimization; a changed row is a failure of the optimization, not a reason to edit the row. The rows are C#
HermitCrab at machine `e63b8863` (hc-conformance self-check). All lexemes are invented.
