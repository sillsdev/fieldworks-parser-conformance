# affix-multiple-application

Pins HermitCrab's per-rule `multipleApplication` on derivational suffixes: CAUS (-ish) and APPL (-el) may each
apply twice, in either order, and CTL (-ox) keeps the default of 1. The negative rows fix the count at exactly 2.

**Why it is producible.** FieldWorks gives an affix rule its cap from the ParserParameters entry
`HC/AffixRules/AffixRule[@guid][@maxApps]` (motif#436), read in `HCLoader.cs` 131-138 and applied at 970-971,
clamped to 1..10. A rule with no entry keeps 1, which is what `mrCtl` stands for. The strata are `unordered`, as
every FieldWorks stratum is, so `katelish` (APPL then CAUS) parses.

**What is cited.** The FieldWorks reader is sillsdev/FieldWorks#1263 at `0ead571c65df55e88525fe19a1a20e1d1ffe0054`
(Jira LT-22699), **not yet merged**: re-point the FieldWorks citation here, in
`status.yaml`, in `fieldworks-writable-shapes.tsv` and in `docs/fieldworks-cannot-say.md` row 22 to
the merge commit when #1263 lands, alongside the existing machine #615 note. The rows come from C# HermitCrab at
machine `e63b8863` (self-check), reading `multipleApplication` from the XML.

**Not covered here.** `MergeMSAs=false` (the cap keyed on the MSA itself, not a merged representative) is a
FieldWorks loader option with no channel in this suite. #1263's HCLoader unit test covers it.
