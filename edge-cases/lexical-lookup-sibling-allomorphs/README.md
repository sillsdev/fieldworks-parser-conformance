# lexical-lookup-sibling-allomorphs

Pins `Morpher.LexicalLookup` in sillsdev/machine, as changed by [machine #627](https://github.com/sillsdev/machine/pull/627).

**Master fails the word `bu` until #627 merges.** The expected rows are those of #627 (head `d26dd375`), where `bu` has no parse. Master
parses `bu` as `BU|bu`, so `hc-conformance` on master reports one mismatch in this fixture. Every other word gives the same
result on master and on #627.

| Word | Master | #627 | Why |
|---|---|---|---|
| `bu` | `BU\|bu` | no parse | analysis matches only allomorph `bui`, whose environment fails; master also tries sibling `buii` |
| `tuk` | `TUIK` | same | deletion rule at work, single allomorph |
| `bak`, `baak` | one parse | same | matched allomorph synthesises |
| `tak` | `TAKN`, `TAKV` | same | homographs, no part of speech asked |
| `takt` | `TAKN+NSUF` | same | verb homograph skipped (earlier on #627, by syntactic feature) |
| `taksa` | `TAKV+VSUF` | same | noun homograph skipped, mirror of `takt` |

Two changes in #627: (1) only the root allomorph that matched the input is proposed for synthesis, not every sibling allomorph
of its entry (`bu` pins this; it changes output); (2) a root allomorph whose entry's syntactic features do not unify with the
input's is skipped before synthesis (`takt`, `taksa` pin that output is unchanged; it only saves work).

FieldWorks-producible: an entry with two allomorphs, one with a "Require" environment (`/ _ [C]`), and a hiatus deletion
rule `i -> 0 / [+high -cons] _` at the default Deletion Reapplications 0. This is `fieldworks_producible: true`, read from the loader
(`HCLoader.cs`), without a FieldWorks witness.

Not pinned because the cause is not yet explained: with the same grammar, a suffixed `but` parses on master through sibling
`buii` and does not parse on #627, and `bui` as a non-first allomorph also fails to parse `but` on master when the sibling is some
unrelated allomorph. Reported on the machine PR rather than pinned.
