# metathesis-middle-context-emptied-edges

Rule `pr0` is `s p t -> t p s`: a metathesis whose switches are `s` and `t` with the middle segment `p` between them,
plus a deletion `pd0` (`a -> 0`), prefixes `PR0` (`s+`) and `PR1` (`p+`) and roots `t`, `st` and `at`. Forward,
`s+p+t` becomes `t+p+s`, shown as `tps`, `tp+s` or `t+ps`. C# generates these but cannot parse them:
`AnalysisMetathesisRuleSpec` drops everything between the switch groups, so analysis looks for adjacent switches and
cannot undo the swap. This is **divergence 127, sillsdev/machine#619** (open; PanGloss#388).

The three rows are `expect_fail: true`: they pin what the C# reference does today, which #619 calls a bug, and `status.yaml` gives the parses each should produce once #619 is fixed (`R0+PR0+PR1` and `R2+PR0+PR1`). `st` and `p+t` are controls. `st` has
no middle segment, so `pr0` does not apply and the result is the same with or without the fix. The expectation was
checked: building ba6dfa10 with the #619 fix (293f6f8d) makes the three words parse as above and leaves `st`
unchanged. The grammar is the issue's own probe and is kept whole; the three words are rejected without `pd0` too, so
the deletion is incidental and only supplies the control's `R2` and `PR0+R2` rows. Each word has a `reference-defect` row in `status.yaml` with the intended answer; the rows do not
depend on an unmerged change, so the test case still runs on every build.

**FieldWorks-producible.** A metathesis rule with a middle context, a deletion rewrite rule and two prefix processes
(`HCLoader.LoadMetathesisRule`, `LoadRewriteRule`, `LoadAffixProcessRule`). `pr0` already names the later group as
`leftSwitch` (`leftSwitch="pr0n2" rightSwitch="pr0n0"`), the form `LoadMetathesisRule` (2152) writes, so no
conversion was needed and all 4 staged rows replayed unchanged; control `p+t` was added so the prefix `PR1` is exercised by a parse, and `pr0` is listed in `dead-rules-allowed.tsv` because only the rejected rows reach it. All lexemes are synthetic. Rows come from the C#
self-check (`hc-conformance --propose`) at sillsdev/machine `ba6dfa10`; no row was filled from PanGloss output.
