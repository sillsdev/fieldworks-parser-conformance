# Provenance of the ground truth

Every `words.yaml` here was produced by running an engine and reading its rows. For most fixtures that engine
is the C# HermitCrab in sillsdev/machine (the **founding oracle**, see `PROTOCOL.md`). The builds are named by
commit hash. This file is the one place the full hashes are kept.

**These hashes are plain text, not links.** They name commits in sillsdev/machine (and, for a few notes,
PanGloss) that are not part of this repository's history and are not guaranteed to stay reachable. The commit
`aab4c59819adb7b366915e09df2fb28c62b8c03a` is kept alive by the tag `pangloss-oracle-pin-aab4c598` on
sillsdev/machine; for the others, treat the hash as a name, not as an address. Fixture files and documents cite
a build by the first eight characters of its hash.

## Builds cited in fixtures

**Current status (2026-11-14):** sillsdev/machine #627 merged to master on 2026-11-12 (`1eae2268`). PanGloss PR #313
pins its C# oracle at machine `1ddef2bd` (now unreachable; see the `e63b8863` row), which is `4d9b454d` plus a cherry-pick of #627; that oracle gives `bu` no
parse, matching this fixture's `expect_fail: true`. The `d26dd375` row below records the earlier #615-runner measurement:
its merge status and pre-merge master result describe the state when that build was tested.

| Short | Full hash | What it is | Files citing it |
|---|---|---|---|
| `4d9b454d` | `4d9b454d42a0da35e058641a65596339a79d115b` | Exact C# founding-oracle build used to propose and trace-check `empty-required-template-slot` and `infix-ambiguous-site`, to propose `nfa-literal-allomorph-environment`, and to take the analyses of the six batch B structural calibration families (`calibration/cal-*` listed in `calibration/README.md`; `hc-conformance --propose`, self-check mode). | `edge-cases/empty-required-template-slot/words.yaml`, `edge-cases/infix-ambiguous-site/words.yaml`, `edge-cases/nfa-literal-allomorph-environment/words.yaml`, the six batch B `calibration/cal-*/words.yaml` |
| `e63b8863` | `e63b8863d37d3189c2b11fcaf9d43be74962ad70` | The C# founding-oracle build for the fixtures that formerly cited `1ddef2bd`. Tip of sillsdev/machine #615 (branch `hermitcrab-conformance-runner`), stacked on #500 and #556 and **not yet merged**: re-point every `e63b8863` citation to the merge commit on master once those PRs land. Moved from `1ddef2bd` (`4d9b454d` plus a cherry-pick of #627, the build PanGloss pinned) because a force-push to #615 dropped `1ddef2bd`, leaving it unreachable; #615's change is on master as `1eae2268`. Results at `e63b8863` were checked equal to the recorded rows before the move. Dated entries below say `e63b8863` where they were written as `1ddef2bd`. `hc-conformance --propose` (self-check mode) took the rows of the fixtures graduated from PanGloss's `conformance-staging/` on 2026-11-19.  On 2026-11-20 the rows of `null-prefix-root-initial-deletion-later-suffix`, `epenthesis-beside-prefix-then-prefix-deletion` and `change-epenthesis-prefix-deletion-chain` (PanGloss#405, #406) were taken from hc-conformance built from a source export of machine 1ddef2bd (now `e63b8863`) (no local changes) and confirmed passing with `--fixtures`. On 2026-11-21 the rows of ten more PanGloss#374/#405 fixtures (`compound-after-an-insertion-keeps-the-bare-node`, `epenthesis-then-swap-keeps-its-edge-before-suffix`, `epenthesis-then-swap-with-root-keeps-its-edge`, `prefix-excluded-environment-after-epenthesis`, `prefix-required-environment-after-epenthesis`, `prefix-required-environment-after-epenthesis-later-compound`, `prefix-required-environment-after-epenthesis-later-suffix`, `root-required-environment-after-epenthesis-before-suffix`, `swap-across-a-deleted-node-keeps-the-gap-before-suffix`, `swap-leaves-a-deleted-node-in-place-before-suffix`) were taken from the same build and confirmed passing with `--fixtures`. On 2026-11-20 the same build is the stated source of the `metathesis-deletion-restores-segment-between-switches` rows (the four `expect_fail` rows record that it gives no parse, sillsdev/machine#649); those rows were taken on a local runner build, and confirmation on a clean `e63b8863` runner is pending. | `grep -rl e63b8863 edge-cases` |
| `aab4c598` | `aab4c59819adb7b366915e09df2fb28c62b8c03a` | The founding-oracle build most recent fixtures were verified against (the build PanGloss pins for its oracle). Tagged `pangloss-oracle-pin-aab4c598` on sillsdev/machine. | 82 files (`grep -rl aab4c598 .`) |
| `18cf242f` | `18cf242f4b114b0eb9bac304b4b171ca2f499a39` | Machine build cited in notes of the form "Oracle: hc.dll, Machine <hash>" as the oracle for the fixtures that carry them. | 74 files (`grep -rl 18cf242f .`) |
| `caa4ddde` | `caa4ddde8782557c6fb58cac57e4761ffcafc2a6` | Machine commit of an earlier C# verification, cited in the notes of the files listed. | 16 files (`grep -rl caa4ddde .`) |
| `f150e2a0` | `f150e2a005ce639f7d68ef17fb0db25b2f6aaa3c` | Original founding-oracle commit recorded when the first fixtures were graduated (verified 2026-09-16). | 8 files (`grep -rl f150e2a0 .`) |
| `d98d12a5` | `d98d12a5d514ce589d7495c71d055830e061a418` | Head of sillsdev/machine #556, one half of the combined #500+#506 oracle used for the truncation identity companions. | `docs/truncation-companions.md`, `edge-cases/truncate-morphotactic-copy-u/words.yaml`, `edge-cases/truncate-morphotactic-identity/words.yaml`, `edge-cases/truncate-morphotactic-subsumption/words.yaml`, `edge-cases/truncate-morphotactic/README.md` |
| `157c031e` | `157c031ef272d07c900db41b2d4a8852b13f64b0` | sillsdev/machine #500 `ApplyRhs` relocation, the other half of the combined oracle. | `docs/truncation-companions.md`, `edge-cases/truncate-morphotactic-copy-u/words.yaml`, `edge-cases/truncate-morphotactic-identity/words.yaml`, `edge-cases/truncate-morphotactic-subsumption/words.yaml` |
| `8bad1934` | `8bad193454a14422a3be59c3156513691ae3da3b` | Machine commit of 2026-09-15 cited as the oracle for the earliest graduated fixtures in the files listed. | `docs/final-template-partial-discriminators.md`, `docs/template-category-sharing.md`, `edge-cases/final-template-partial-discriminators/words.yaml`, `edge-cases/template-category-sharing/words.yaml` |
| `fa8d9b25` | `fa8d9b2540962981add315d06203e928a11c1853` | sillsdev/machine #480 head at the time the truncate-morphotactic fixtures were recorded. | `edge-cases/truncate-morphotactic-identity/words.yaml`, `edge-cases/truncate-morphotactic-subsumption/words.yaml`, `edge-cases/truncate-morphotactic/README.md` |
| `a20bce12` | `a20bce1231fab308810fa5a531257eef24f5df1b` | Machine build that includes merged #493, used for shared-template-unconstrained-suffix. | `docs/shared-template-unconstrained-suffix.md`, `edge-cases/shared-template-unconstrained-suffix/words.yaml` |
| `a2f80e28` | `a2f80e28debaffda8a65b3b11875c80479768bc7` | Founding-oracle commit recorded in October 2026 (verified 2026-10-15 and 2026-10-20) for the files listed. | `edge-cases/clitic-rule-designation/words.yaml`, `edge-cases/final-template-merge-key/words.yaml` |
| `c2454760` | `c2454760181d77a3284482483cf78d921a2c4b9b` | Second machine commit at which the boundary-narrowing-probe results were observed. | `edge-cases/boundary-narrowing-probe/README.md` |
| `25ddf914` | `25ddf914c0edb739a4445f9a088f7e06492a808d` | Founding-oracle commit recorded for pattern-root-required-environment (verified 2026-09-02). | `edge-cases/pattern-root-required-environment/words.yaml` |
| `25992041` | `259920414132bdd5a85542722d9af5509aed8943` | Machine commit at which the truncate-morphotactic two-parse and related results were re-loaded ten times. | `edge-cases/truncate-morphotactic/README.md` |
| `d26dd375` | `d26dd375731d8ed0738d826297eb265e32afefe5` | Head of sillsdev/machine #627 (not yet merged; approved 2026-11-12), run with the #615 conformance runner to take the rows of lexical-lookup-sibling-allomorphs. Master fails its word `bu`. | `edge-cases/lexical-lookup-sibling-allomorphs/words.yaml` |
| `7e5d5a64` | `7e5d5a64ce95693a2b0524f94470007d30a92510` | Head of sillsdev/machine #631 (the fix for #630), run with the conformance runner to propose the rows of infix-split-root-allomorph-environment. | `edge-cases/infix-split-root-allomorph-environment/words.yaml` |
| `e63b8863` | `e63b8863d37d3189c2b11fcaf9d43be74962ad70` | Tip of sillsdev/machine #615 (branch hermitcrab-conformance-runner), run with its conformance runner to take the rows of family-blocked-generation. | `edge-cases/family-blocked-generation/words.yaml`, `edge-cases/family-blocked-generation/README.md` |
| `0cbf85f1` | `0cbf85f17c4782cc9991f5fcb3c7f13df3bf8f4f` | sillsdev/machine master at `0cbf85f1`, merged locally with the conformance runner of machine #615 (the merge is a local build, not a commit; no hash exists for it). `hc-conformance --propose` (self-check mode) took the rows of the five partial-rule fixtures; rows identical with the partial-rule prune of machine #644 (the fix for #643). | `edge-cases/partial-rule-infixed-material/words.yaml`, `edge-cases/partial-rule-wrapped-material/words.yaml`, `edge-cases/partial-rule-deleted-material/words.yaml`, `edge-cases/partial-rule-truncated-material/words.yaml`, `edge-cases/final-template-partial-reachability/words.yaml` |

The assembly hashes recorded for the combined #500+#506 oracle (the truncation identity companions, see
`docs/truncation-companions.md`):

- #556 `SIL.Machine.dll` SHA-256: `b265a40a44292614f51f7a65afc445ae34dde685cb40ce8c2d2de5521a0c299d`
- combined `SIL.Machine.Morphology.HermitCrab.dll` SHA-256: `4cd980453f51fd3cf29cf38a99f342f542e631eb23be6ba87b9433aab6c3d57f`
- Reproduction: start from the truncation grammar; add the identity labels or the stated companion rule or root;
  use the #556 Machine library and the #500 relocation in HermitCrab's copy/annotation transfer; parse every
  `words.yaml` word; retain every returned signature and forward trace.

## Short commit references in prose

Some fixture comments and READMEs cite a commit by eight characters or fewer (for example in `# oracle-provenance`
headers, "history row" notes, or "fixed at" notes). They name commits of sillsdev/machine, PanGloss, or their
branches at the time of writing, and are history, not instructions. The same applies to paths such as
`rust/tools/...`, `conformance/adapters/...`, `semantic-coverage-*.tsv` and `tools/xample-projector`, which belong to
those repositories and not to this one.

## FieldWorks witnesses

The eleven `fieldworks/` directories (`project.fwdata`, `phonology-mutations.yaml`, `WritingSystemStore/`) were
produced by the `author` command of PanGloss's `xample-projector` tool against FieldWorks 9.3.10.1452 and
LibLCM 11.0.0.55173, as each fixture README says. The tool's commit was not recorded with the witnesses; a
`WITNESSES.md` that records it is a later step. The writing-system files carry CLDR revision
`1f9188eccdd20d6b71d82723bbd185f439d50196` (`sil:identity revid`), a CLDR revision and not a machine commit.

## Other revisions cited

`docs/fieldworks-cannot-say.md` names FieldWorks commit `620cd9903f46941ee85947615dba15c8888c8e7a` (the `HCLoader.cs` the producibility
table was checked against), `6b8a75287221a1b5ab6d15d6f6eedc117690ef98` (the last commit to change that file) and
LibLCM commit `d564a719b1cce16c25ebea53a537393cb757f5d1`. Those are public FieldWorks and LibLCM commits and are
left as written.
