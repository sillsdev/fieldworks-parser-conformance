# lexical-lookup-sibling-allomorphs

Pins `Morpher.LexicalLookup` in sillsdev/machine, as changed by [machine #627](https://github.com/sillsdev/machine/pull/627).

As of 2026-11-14, #627 is merged to machine master (2026-11-12, commit `1eae2268`). PanGloss pins its C# reference at
machine `e63b8863`, the tip of unmerged #615, which contains #627; that reference gives `bu` no parse, matching `expect_fail: true`.

The rows below were measured from #627 head `d26dd375` with the #615 conformance runner, before the merge. This comparison
records the behavior at that time: pre-merge master parsed `bu` as `BU|bu`, while #627 did not. Every other word had the
same result on those two measured builds.

| Word | Pre-merge master | #627 head (`d26dd375`) | Why |
|---|---|---|---|
| `bu` | `BU\|bu` | no parse | analysis matches only allomorph `bui`, whose environment fails; pre-merge master also tried sibling `buii` |
| `tuk` | `TUIK` | same | deletion rule at work, single allomorph |
| `bak`, `baak` | one parse | same | matched allomorph synthesises |
| `tak` | `TAKN`, `TAKV` | same | homographs, no part of speech asked |
| `takt` | `TAKN+NSUF` | same | verb homograph skipped (earlier on #627, by syntactic feature) |
| `taksa` | `TAKV+VSUF` | same | noun homograph skipped, mirror of `takt` |

The #627 change does two things: (1) only the root allomorph that matched the input is proposed for synthesis, not every sibling allomorph
of its entry (`bu` pins this; it changes output); (2) a root allomorph whose entry's syntactic features do not unify with the
input's is skipped before synthesis (`takt`, `taksa` pin that output is unchanged; it only saves work).

FieldWorks-producible: an entry with two allomorphs, one with a "Require" environment (`/ _ [C]`), and a hiatus deletion
rule `i -> 0 / [+high -cons] _` at the default Deletion Reapplications 0. This is `fieldworks_producible: true`, read from the loader
(`HCLoader.cs`), without a FieldWorks witness.

Not pinned because the cause is not yet explained: in the pre-merge comparison, a suffixed `but` parsed on master through
sibling `buii` and did not parse on #627, and `bui` as a non-first allomorph also failed to parse `but` on pre-merge master
when the sibling was some unrelated allomorph. Reported on the machine PR rather than pinned.
