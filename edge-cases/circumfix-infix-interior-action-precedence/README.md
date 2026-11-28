# circumfix-infix-interior-action-precedence

Test cases of one family (the grammars are the same shape and differ in one parameter each), folded into one grammar. This test case holds all 3 as cells, so it keeps the id of its first member; the other members' ids are in `docs/renames.tsv`.

## Cells

Each former test case is one **cell**: its own segments, natural classes, rules, entries and words, so cells cannot interact. Cell 1 keeps its letters; every later cell spells its segments with letters no other cell uses. Every grammar id, morpheme id and rule id in a cell ends in `_<cell>`, so a signature or a rule trace names its cell. Each word's `note` starts with `[cell <name>]`, and each word keeps its own behaviour label.

| Cell | Former test case | What differs | Letters (former to cell) |
|---|---|---|---|
| `interior-action` | `edge-cases/circumfix-infix-interior-action-precedence` | [XAmple] one allomorph that is both circumfixing and infixing in the same output. | unchanged |
| `non-first-allomorph` | `edge-cases/circumfix-non-first-allomorph-selection` | [XAmple] a circumfix allomorph that is chosen after an ordinary suffix allomorph of the same rule fails. | `a`→`d`, `e`→`f`, `i`→`g`, `k`→`h`, `m`→`j`, `n`→`l`, `s`→`o`, `t`→`p` |
| `reduplication` | `edge-cases/circumfix-reduplication-precedence` | [XAmple] one allomorph that is both circumfixing and reduplicating in the same output. | `a`→`q`, `e`→`r`, `k`→`v`, `m`→`w`, `n`→`x`, `t`→`à` |

Replay: every former word, mapped by its cell's letters and ids, returns the reference's result unchanged, and no word of one cell parses in another (`hc-conformance --propose` prints no patch). Former ids are in `docs/renames.tsv` (wave-2026-11-27-9). The expected rows are what C# HermitCrab returned on a fresh `hc-conformance --propose` run over the merged grammar and the cell-mapped word list (sillsdev/machine `d492d1005e18358f35d8b7b9527d01e1dac9e644`).

## Former READMEs

Each cell's own rationale, as it stood before the merge. Ids and letters in them are the former ones; the cell map above translates them.

### Cell `interior-action`: former README of `circumfix-infix-interior-action-precedence`

### circumfix-infix-interior-action-precedence: provenance and regression rationale

Graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480).
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### STAGING: circumfix-infix-interior-action-precedence

#### Why this test case exists

Pins census **C3** (`docs/conformance/circumfix-structural-composite-census.md`,
`openspec/changes/plan-construct-coverage-completion` task 4.3b): `crate::emit::classify_affix`'s
interior-action test used to run BEFORE its leading-AND-trailing test, so an RHS that is
SIMULTANEOUSLY circumfixing (an `InsertSegments` before the first `CopyFromInput`, another after
the last) AND infixing (a THIRD `InsertSegments` sitting strictly between two `CopyFromInput`
actions) classified `Role::Infix` — the wrong taxonomic label for a morph that genuinely wraps the
root on both sides — and was routed to `crate::preexpand` instead of `build_structural_composites`,
whose own comment names circumfix explicitly as needing its unconditional
(`probe_would_refuse`-independent) path. After the fix, the leading-AND-trailing test runs FIRST, so
this shape now classifies `Role::CircumfixPrefix` and is routed to `build_structural_composites`
instead.

**Important correction, found by testing rather than assuming:** an earlier draft of this document
claimed `crate::preexpand` "can only splice literal text, never wrap a root on both sides." That is
WRONG. `crate::preexpand::extend` (its own module doc) ALSO calls
`pg_rules::morph::synthesize_cached` — the SAME real engine `build_structural_composites` uses — so
it is NOT incapable of producing this exact surface. Confirmed directly: temporarily reverting
`classify_affix`'s reordering and re-running `circumfix_infix_interior_action_recall_parity` (below)
showed it PASSING even without the fix — recall for `kebzatan` was never actually lost. What the fix
demonstrably changes is OWNERSHIP: `circumfix_infix_ownership_handoff_is_clean` (below) DOES fail
without the fix. See "Recall argument" for the corrected, narrower claim the fix actually rests on.

`grammar.xml`'s one `MorphologicalRule` (`mrCircInfix`) has a two-part LHS (`p1` = the root's first
segment, `p2` = the remainder) so its RHS can place an `InsertSegments` ("z") strictly between the
two `CopyFromInput` actions while ALSO leading with one `InsertSegments` ("ke") and trailing with
another ("an") — the exact simultaneously-circumfixing-and-infixing shape census C3 names.

#### What it pins

- `bat` (bare root): a plain control.
- `kebzatan` (root + `mrCircInfix`): `classify_affix` classified `subCircInfix`'s RHS `Role::Infix`
  before the fix (because of the interior "z" insert), routing `mrCircInfix` to `crate::preexpand`
  rather than `build_structural_composites` — a MISCLASSIFICATION, not a recall failure: `preexpand`
  already resynthesizes this surface correctly today (see the correction above). After the fix,
  `classify_affix` reads this RHS as `Role::CircumfixPrefix` and `mrCircInfix` is admitted into
  `build_structural_composites` instead.
- A companion Rust test (`rust/crates/pg-foma/tests/circumfix_candidate_selection.rs`) proves the
  proposer-to-confirm containment directly against the compiled FST (every analysis
  `pg_parse::Morpher` finds for `kebzatan` is reachable in `emit::emit`'s output — true both before
  and after the fix, per the correction above) and separately confirms the ownership handoff is
  clean (true ONLY after the fix): `emit::composite_candidate_rules` reports `mrCircInfix` in the
  structural set and NOT in `crate::preexpand`'s own candidate set (via that same public
  diagnostic), so the two composite mechanisms never both claim this rule and never both drop it.

#### Recall argument (task 4.3b's own obligation)

The load-bearing claim is narrower than "this closes a recall gap" — checked empirically, not
assumed: `crate::preexpand::extend` (its own module doc) ALSO calls
`pg_rules::morph::synthesize_cached`, the SAME real engine `build_structural_composites`'s
`struct_extend` calls (`pg_rules::morph::synthesize(ctx.g, base_word, rule)`,
`rust/crates/pg-foma/src/emit.rs`). Both are pure functions of `(Grammar, Word, MorphRuleDef)` that
execute every `OutputAction` in RHS document order, with no reference to `Role`/`classify_affix` and
no assumption that a `Copy` run is contiguous — confirmed by reading `pg-rules/src/morph.rs` and by
directly testing it: temporarily reverting this fix and re-running
`circumfix_infix_interior_action_recall_parity` showed `kebzatan` STILL reachable, because
`crate::preexpand` (which `Role::Infix` routed the rule to) already covers it. So an interior
non-`Copy` action between two `Copy`s adds no new representational burden to EITHER composite
mechanism once a rule reaches it — that part of the original argument holds, just not as a
recall-gap argument.

What the fix actually rests on is narrower and still real: (1) taxonomic correctness — the rule
genuinely wraps the root on both sides, and `Role::Infix` is simply the wrong label independent of
which mechanism ends up covering it; (2) robustness — `build_structural_composites`'s
`CircumfixPrefix` admission is unconditional (`is_structural_rule`'s own comment), while
`crate::preexpand`'s coverage of this shape, though real, is incidental to a module whose own doc
frames its mechanism as interdigitation/boundary-fusion, never circumfix; (3) the capability layer
(`crate::capability::CircumfixStructuralCompositePredicate`) reads `is_structural_rule` as its own
ground truth — before the fix, a rule misclassified `Infix` here would make that predicate `Refuse`
a grammar `crate::preexpand` was already covering, an over-refusal consistent with the census's own
"every gap fails over-refusing, never a silent overclaim" finding.

**What would falsify the narrower claim:** discovering that `pg_rules::morph::synthesize` (or
anything `struct_extend`/`preexpand::extend` calls) special-cases the RHS action sequence's SHAPE
rather than just replaying it in order — e.g. some assumption baked into LHS/RHS matching that a
"circumfix" allomorph has exactly one contiguous copied span. No such special-casing exists in
either caller today; if one is ever added, this argument must be re-checked.

#### Reference discipline

**Reference: `pangloss` (this repo's own Rust engine), NOT the C# reference.** Authored fresh for
this task; no `dotnet`/C# toolchain available in this environment. Per `docs/
conformance-staging-plan.md`'s oracle-discipline note, this must be treated as `pangloss`-only
ground truth until independently re-verified against the C# reference.

#### Verification

Signatures captured by running `cargo test -p pg-parse --test conformance_fixtures_gate --
--nocapture`, which discovers this staged test case automatically and replays every word against
`pg_parse::Morpher` — the mismatch panic message on the first pass reported the engine's own actual
signature, transcribed verbatim into `words.yaml` above (not hand-derived). Final run: `3 passed; 0
failed`, `346 words checked across 29 fixtures` (the whole default corpus, this test case included).

#### Graduation

#### Reference provenance (reconciled 2026-08-31)


ust/tools/oracle-conformance.ps1 ran hc-conformance.exe self-check (C# reference,
machine commit caa4ddde) directly against this test case's
grammar.xml + words.yaml: PASS -- every word's signature and traced
ules: list matched. The
test case's words.yaml now carries # oracle-provenance: reference. Any "Reference discipline"
section below describes how this test case was originally authored, not its current verification
status.

### Cell `non-first-allomorph`: former README of `circumfix-non-first-allomorph-selection`

### circumfix-non-first-allomorph-selection: provenance and regression rationale

Graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480).
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### STAGING: circumfix-non-first-allomorph-selection

#### Why this test case exists

Pins census **C1** (`docs/conformance/circumfix-structural-composite-census.md`,
`openspec/changes/plan-construct-coverage-completion` task 4.3a): `crate::emit::rule_role`
classifies a rule's role from its FIRST allomorph only. Before the fix, `crate::emit::
is_structural_rule` inherited that first-allomorph view, so a rule whose allomorph 0 is an
ordinary Prefix/Suffix/None/Infix/Reduplication/Process shape but whose allomorph 1..n is
circumfix-shaped never had that later allomorph recognized as needing
`build_structural_composites` — the ONLY mechanism able to represent a discontinuous "wraps the
root on both sides" morph at all (the ordinary concatenative emission path is, by this crate's own
comment, "unconditionally unrepresentable" for that shape). This is a real, honest, fail-closed
recall gap: the affected allomorph is reported `uncovered` rather than silently mis-compiled, but
it is nonetheless never reachable from the proposer. The gap is order-of-declaration-dependent — it
appears and disappears purely as a grammar author reorders a rule's allomorphs in the XML, which is
what makes it worth fixing rather than documenting as a permanent boundary.

`grammar.xml`'s one `MorphologicalRule` (`mrMixed`) declares exactly this shape: allomorph 0
(`subSuffix`) is an ordinary suffix ("-s"); allomorph 1 (`subCircum`, declared SECOND) is the
circumfix ("ke-...-an", leading AND trailing `InsertSegments` around one `CopyFromInput`).

#### What it pins

- `mits` (allomorph 0, the ordinary suffix): the ordinary allomorph rides along once the rule is
  admitted as a structural candidate — over-inclusion here is safe by construction
  (`build_structural_composites` delegates to the real morphological engine,
  `pg_rules::morph::synthesize`, for every allomorph of an admitted rule, never re-deriving from a
  role label), mirroring the census's own "opposite order is safe" observation.
- `kemitan` (allomorph 1, the circumfix): THE load-bearing word. Before census C1's fix, this
  surface was unreachable from the FST proposer at all (`is_structural_rule` returned `false` for
  `mrMixed`, because `rule_role`'s allomorph-0 view reported `Role::Suffix`, and
  `Role::Suffix`'s only route to `true` — `rhs_drops_lhs_material` — does not hold for
  `subSuffix`'s LHS-preserving shape). After the fix (an allomorph-wise scan for
  `Role::CircumfixPrefix` added ahead of `rule_role`'s own classification), `mrMixed` is admitted and
  `kemitan` becomes reachable.
- A companion Rust test (`rust/crates/pg-foma/tests/circumfix_candidate_selection.rs`) proves the
  proposer-to-confirm containment directly against the compiled FST (every analysis
  `pg_parse::Morpher` finds for `kemitan` is reachable in `emit::emit`'s output), and separately pins
  the ORDER-INDEPENDENCE invariant the bug violated: the same rule with its two allomorphs declared
  in the OTHER order (circumfix first, suffix second) must be selected as a structural candidate
  identically. That inline-XML variant is not a second staged test case (mirrors
  `rust/crates/pg-foma/tests/phase_c_circumfix.rs`'s own precedent of hand-authored inline XML for
  an internal-invariant check that isn't itself a new conformance corpus entry).

#### Reference discipline

**Reference: `pangloss` (this repo's own Rust engine), NOT the C# reference.** Authored fresh for
this task; no `dotnet`/C# toolchain available in this environment. Per `docs/
conformance-staging-plan.md`'s oracle-discipline note, this must be treated as `pangloss`-only
ground truth until independently re-verified against the C# reference.

#### Verification

Signatures captured by running `cargo test -p pg-parse --test conformance_fixtures_gate --
--nocapture`, which discovers this staged test case automatically and replays every word against
`pg_parse::Morpher` — the mismatch panic message on the first pass reported the engine's own actual
signature, transcribed verbatim into `words.yaml` above (not hand-derived). Final run: `3 passed; 0
failed`, `346 words checked across 29 fixtures` (the whole default corpus, this test case included).

#### Graduation

#### Reference provenance (reconciled 2026-08-31)


ust/tools/oracle-conformance.ps1 ran hc-conformance.exe self-check (C# reference,
machine commit caa4ddde) directly against this test case's
grammar.xml + words.yaml: PASS -- every word's signature and traced
ules: list matched. The
test case's words.yaml now carries # oracle-provenance: reference. Any "Reference discipline"
section below describes how this test case was originally authored, not its current verification
status.

### Cell `reduplication`: former README of `circumfix-reduplication-precedence`

### circumfix-reduplication-precedence: provenance and regression rationale

Graduated from PanGloss staging into this suite (originally proposed as sillsdev/machine PR #480).
The ordered words, statuses and complete analysis-signature multiplicities are preserved.
Grammar preparation adds missing external DTD declarations and, where needed, consistently
renames alpha-variable labels `a`/`b` to the DTD vocabulary `α`/`β`; variable IDs and references
are unchanged. Required word notes and explicit rule-trace annotations are supplied separately.

The original rationale below is historical. References to `STAGING.md` mean this preserved
rationale; claims that a then-current reference was unavailable or unfixed describe that earlier
revision, not current verification. PanGloss-specific assertions remain in PanGloss.

---

### STAGING: circumfix-reduplication-precedence

#### Why this test case exists

Pins census **C2** (`docs/conformance/circumfix-structural-composite-census.md`,
`openspec/changes/plan-construct-coverage-completion` task 4.3c): `crate::emit::classify_affix`'s
reduplication test used to be an unconditional EARLY RETURN — computed and consulted before
`first_copy`/`last_copy` even existed — so an RHS that is SIMULTANEOUSLY circumfixing (an
`InsertSegments` before the first `CopyFromInput`, another after the last) AND reduplicating (the
SAME LHS part echoed by >= 2 `CopyFromInput` actions) always classified `Role::Reduplication`,
before the leading/trailing test further down ever ran. This is the one census item explicitly
flagged as coupled to `openspec/changes/plan-construct-coverage-completion` design.md row 11's
`Reduplication` carve-out: whichever role wins decides which MECHANISM claims the allomorph
(`Role::Reduplication` → `crate::peel::ReduplicationPeeler`; `Role::CircumfixPrefix` →
`build_structural_composites`), so it was deliberately left unscheduled until row 11's own boundary
could be re-checked alongside it (C1 and C3, the other two census items, closed independently
first).

#### The joint decision (task 4.3c's own obligation)

**Reachability, checked first, not assumed.** `MorphologicalOutput` is declared
`(CopyFromInput | InsertSimpleContext | ModifyFromInput | InsertSegments)*`
(`machine/src/SIL.Machine.Morphology.HermitCrab/HermitCrabInput.dtd:420`) — an unconstrained
repeated-choice group, so `<CopyFromInput index="p1"/>` may legally appear any number of times, in
any position, alongside any number of `<InsertSegments>`/other actions. `pg_grammar::load`
(`load.rs:1896-1901`) places no additional uniqueness constraint on `index` either — it only checks
that the referenced part exists. So an RHS that is simultaneously circumfix-shaped (leading AND
trailing insert) and reduplication-shaped (the same part `Copy`d twice) is fully DTD-legal and
loader-legal; this grammar is exactly that shape, not a vacuous or unreachable construction.

**Decision: `CircumfixPrefix` wins (mirrors C3's own resolution), and this is NOT merely a
relabeling — a genuine recall gap existed.** The other two options considered and rejected:

1. ~~Reduplication keeps winning, documented as a permanent boundary.~~ REJECTED: this would require
   showing the peel genuinely handles the circumfixing part, or that the combination is
   unreachable. Neither holds. `crate::peel::ReduplicationPeeler`'s four scan kinds (that module's
   own doc: prefix-copy, suffix-copy, separator+tail-copy, separator+suffix-peel) are each a
   ONE-SIDED surface-string match — none of them searches for a repeated span with independent
   material wrapping it on BOTH sides. Before this fix, an `AffixProcessRule` with this exact shape
   (peel-eligible per rule kind) was claimed by the peel but the peel's scans cannot actually find
   the wrapped reduplicated span — a real, silent recall gap dressed up as `ConfirmOnly`, not an
   honest refusal.
2. ~~Both mechanisms are wrong; refuse with a named witness.~~ REJECTED: `build_structural_composites`
   handles this shape correctly (see below), so refusing would be needlessly conservative — the
   real compiler already has a construction that works.
3. **`CircumfixPrefix` wins.** `build_structural_composites`'s `struct_extend` calls
   `pg_rules::morph::synthesize` directly (`emit.rs`), which replays every `OutputAction` in RHS
   document order with NO reference to `Role` and no assumption that a `Copy` run is contiguous or
   occurs only once per part — confirmed by reading `pg_rules::morph::synth_process_allomorph`'s own
   per-action loop over `allo.rhs`, plus that crate's own "Tier-2 #8 (reduplication morph
   attribution)" handling of a repeated `Input` part. A rule reaching `build_structural_composites`
   with this shape is therefore resynthesized faithfully — reduplicated copies AND wrapping inserts
   together — not merely "accepted." This is the SAME argument C1/C3 already established for the
   mechanism in general, extended here to the specific combined shape.

#### Row 11's carve-out, re-checked against current code (not assumed still valid)

`crate::peel::is_reduplication_rule` (`peel.rs`) only ever classifies a rule
`AffixProcess`-vs-`Realizational` — a `RealizationalRule` allomorph is never peel-eligible "even if
one of its allomorphs would classify as `Role::Reduplication`" (that function's own doc, citing
`ReduplicationProposer.IsReduplication`, `ReduplicationProposer.cs:233-247`). **This carve-out is
UNCHANGED by both C3's and C2's reordering, and remains the faithful C# behavior**: it is a rule-KIND
distinction (checked BEFORE `classify_affix` is even consulted — the `_ => false` arm), completely
orthogonal to the Role-shape distinction C2 resolves, which applies identically regardless of rule
kind. No C# citation needed beyond the one `is_reduplication_rule`'s own doc already carries, because
no code in that function changed at all — see the next paragraph for why.

**No code change was needed in `peel.rs`.** `is_reduplication_rule`'s `.any()` scan calls
`crate::emit::classify_affix` directly, per allomorph — the SAME function C2's fix reorders. Once
`classify_affix` stops returning `Role::Reduplication` for a simultaneously-circumfixing-and-
reduplicating RHS (returning `CircumfixPrefix` instead), that allomorph silently drops out of THIS
scan too, automatically, with zero lines changed in `peel.rs` — mechanically identical to how C3
closed the `crate::preexpand` handoff by only touching `classify_affix`. Only `peel.rs`'s DOC comment
was updated, to record this interaction and the reasoning above (`is_reduplication_rule`'s doc
comment, `peel.rs`).

#### What it pins

- `tam` (bare root): a plain control.
- `ketamtaman` (root + `mrCircRedup`): `classify_affix` classified `subCircRedup`'s RHS
  `Role::Reduplication` before the fix (the unconditional early return), routing `mrCircRedup` to
  `crate::peel::ReduplicationPeeler` — which cannot recall this exact surface (see above: a REAL
  recall gap, not a relabeling). After the fix, `classify_affix` reads this RHS as
  `Role::CircumfixPrefix` and `mrCircRedup` is admitted into `build_structural_composites` instead,
  which resynthesizes it correctly.
- A companion Rust test (`rust/crates/pg-foma/tests/circumfix_candidate_selection.rs`, C2 section)
  proves: (1) full proposer-to-confirm containment — every analysis `pg_parse::Morpher` finds for
  `ketamtaman` is reachable in `emit::emit`'s compiled net; (2) the ownership handoff is clean in the
  OTHER direction from C1/C3: `crate::peel::ReduplicationPeeler::new(&g).has_redup_rules()` is
  `false` for this grammar (the peel relinquishes the ONLY rule that could have made it `true`), so
  the peel is never even consulted for this word; (3) C1's and C3's own pinned behavior is unchanged
  by this fix (their existing tests re-verified passing, unmodified).

#### Reference discipline

**Reference: `pangloss` (this repo's own Rust engine), NOT the C# reference.** Authored fresh for
this task; no `dotnet`/C# toolchain available in this environment. Per
`docs/conformance-staging-plan.md`'s oracle-discipline note, this must be treated as `pangloss`-only
ground truth until independently re-verified against the C# reference.

#### Verification

Signatures captured by running `cargo test -p pg-parse --test conformance_fixtures_gate --
--nocapture`, which discovers this staged test case automatically and replays every word against
`pg_parse::Morpher` — the mismatch panic message on each pass reported the engine's own actual
signature, transcribed verbatim into `words.yaml` above (not hand-derived). Final run: `376 words
checked across 35 fixtures (2 skipped)`, this test case's 2 words included, all passing.

#### Graduation

#### Reference provenance (reconciled 2026-08-31)


ust/tools/oracle-conformance.ps1 ran hc-conformance.exe self-check (C# reference,
machine commit caa4ddde) directly against this test case's
grammar.xml + words.yaml: PASS -- every word's signature and traced
ules: list matched. The
test case's words.yaml now carries # oracle-provenance: reference. Any "Reference discipline"
section below describes how this test case was originally authored, not its current verification
status.
