# metathesis-swap-then-gap

Rule `pm0` swaps `p s`, and rule `pd0` deletes `t`. Roots `tpsa`, `ptsa` and `pst`, a prefix `NU0` (`+`) and a
suffix `SU1` (`a`). Forward, `NU0+pst` swaps to `+spt` and `pd0` deletes `t`, giving `+sp`. C# generates `+sp`,
`+spa`, `sp`, `spa`, `spaa` and `+spaa` but cannot parse them: analysis un-applies `pd0` first, restores an optional
`t?` between the switches of `pm0`, adds it to the first switch's capture and pairs the captures node by node, so the
swap is never undone. This is **divergence 132, sillsdev/machine#649** (open; PanGloss#411, a duplicate of #381);
the mechanism is that of `metathesis-deletion-restores-segment-between-switches`.

The six rows are `expect_fail: true`: they pin what the C# reference does today, which #649 calls a bug, and each note
says the parse it should give once #649 is fixed. `psa` and `psaa` are controls both engines agree on (the `t` of `ptsa` is
deleted, so no swap is needed). Removing `pd0` and the `t` of the roots makes all six words parse in C#, so the
deletion alone causes the rejection. Each of the six has a `reference-defect` row in `status.yaml` with the intended answer.

**FieldWorks-producible.** A metathesis rule, a deletion rewrite rule, a prefix process and a suffix process
(`HCLoader.LoadMetathesisRule`, `LoadRewriteRule`, `LoadAffixProcessRule`). The staged grammar named the earlier
switch as `leftSwitch`; `LoadMetathesisRule` (2152) sets `LeftSwitchName = "r"`, so the producible form names the
later group, and `pm0` now has `leftSwitch="pm0n1" rightSwitch="pm0n0"` (row 5 of
[docs/fieldworks-cannot-say.md](../../docs/fieldworks-cannot-say.md)). All 7 staged rows replayed unchanged; control `psaa` was added so the suffix rule `SU1` is exercised by a parse. All lexemes are
synthetic. Rows come from the C# self-check (`hc-conformance --propose`) at sillsdev/machine `ba6dfa10`; no row was
filled from PanGloss output.
