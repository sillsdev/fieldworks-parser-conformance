# literal-hash-affix-context

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 2 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

The grammar declares a shared symbolic feature `cell`, every segment carries its cell's value, and each feature-defined natural class is restricted to its cell's value. Without it a feature class or a segment context of one cell accepts the other cells' segments, because an unspecified feature matches anything.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `literal-hash` | `edge-cases/literal-hash-affix-context` | a literal `#` marker in an environment, which is not a word-edge anchor. | unchanged |
| `word-boundary` | `edge-cases/word-boundary-affix-rewrite` | a word-edge anchor in a rule that rewrites the edges of prefixes and roots. | `a`→`b`, `k`→`d`, `r`→`f`, `t`→`g` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-9). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `literal-hash`: former README of `literal-hash-affix-context`

### literal-hash-affix-context: provenance and regression rationale

Graduated from PanGloss staging into this suite.
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### Staged conformance case: literal hash boundary in affix rewrite contexts

#### Why this test case exists

This reproduces the context authored in Motif's `PrefixRootRewriteTraceTests`: its left and right
contexts point to a user-created `PhBdryMarker` whose code is `#`. HermitCrab treats that object as
a literal boundary marker in the shape. It is distinct from a word-edge anchor (`#` authored as a
word-boundary condition). Since the affix/root shape contains `+?`, not a literal `#` segment, the
rewrite does not produce `ta` or `at`.

The test case covers the one-segment prefix, a root-initial underlying `r`, a two-segment prefix, an
internal `r` control, and the suffix-final mirror. The expected unchanged forms and absent rewritten
forms are the C# reference behavior for this authored grammar.

#### Reference evidence

`words.yaml` signatures and rule traces were checked by the C# HermitCrab conformance harness built
from the pinned Machine commit `18cf242f` on 2026-10-09. The
targeted self-check passed: 1 test case, 0 failed. The harness accepted `ra`, `raa`, `ara`, `ar`,
and `a`; it rejected `ta`, `taa`, `ata`, and `at`.

The Motif report's object inspection confirms the authored left context has kind `boundary` and a
marker GUID, rather than the word-boundary context kind. That matches this test case. The earlier
word-edge-anchor test case passed both engines, so no PanGloss parser divergence is demonstrated.

#### Graduation

Candidate destination: `machine/conformance/edge-cases/literal-hash-affix-context/`. No upstream PR
has been opened.

#### Shared construct coverage note

The shared exercise tags record only positive affix analyses. The literal # boundary contexts
and missing rewrites remain described above as this test case's focal behavior.

### Cell `word-boundary`: former README of `word-boundary-affix-rewrite`

### word-boundary-affix-rewrite: provenance and regression rationale

Graduated from PanGloss staging into this suite.
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### Staged conformance case: word-boundary rewrite at affix edges

#### Why this test case exists

This pins the actual word-edge anchor behavior requested by the implementation brief. It uses
HermitCrab's `initialBoundaryCondition` and `finalBoundaryCondition`, rather than a user-created
boundary marker whose representation happens to be `#`. The one-segment prefix and root-initial
root produce `ta`; a two-segment prefix produces `taa`; the internal `r` control stays `ara`; and
the suffix mirror produces `at`.

`literal-hash-affix-context` is the companion test case for Motif's current authored context. It
uses a literal `PhBdryMarker` with code `#`, which the reference treats as a shape boundary, not as a
word-edge anchor.

#### Reference evidence

`words.yaml` signatures and rule traces were checked by the C# HermitCrab conformance harness built
from the pinned Machine commit `18cf242f` on 2026-10-09. The
targeted self-check passed: 1 test case, 0 failed. The reference accepted `ta`, `taa`, `ara`, `at`, and
`a`, and rejected the unchanged or misplaced-context controls `ra`, `raa`, `ata`, and `ar`.

#### Graduation

Candidate destination: `machine/conformance/edge-cases/word-boundary-affix-rewrite/`. No upstream PR
has been opened.
