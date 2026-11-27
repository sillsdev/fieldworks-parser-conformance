---
name: building-grammars
description: >-
  Use for any new grammar need in the conformance suite, and before adding, extending, merging, retiring or
  renaming a test case or removing a word. Triggers: a reference bug or pending upstream change to record; a
  PanGloss conformance-staging case to graduate; a behaviour label, loader path or bug no test case detects; a
  generated probe grammar that found a difference; a changed expected result; the periodic review.
---

# Building grammars

A test case earns its place by what it **detects** ([ADR 0008](../../../docs/adr/0008-value-is-detection.md)).
This skill decides whether a need gets a new test case, builds it, and keeps the set small. Terms are those of
[GLOSSARY.md](../../../GLOSSARY.md); file, script and field names stay as they are.

| Need | Source of truth |
|---|---|
| File layout, producibility, checks, landing route | [AGENTS.md](../../../AGENTS.md) |
| Word format, `morpher:`/`variants:` | [PROTOCOL.md](../../../PROTOCOL.md) |
| Expected results come only from the reference | [ADR 0002](../../../docs/adr/0002-reference-is-the-only-source-of-expected-results.md) |
| The reference commit | [ADR 0003](../../../docs/adr/0003-reference-commit-may-be-unmerged.md) |
| Scope (FieldWorks-producible only; XAmple is out) | [ADR 0004](../../../docs/adr/0004-scope-fieldworks-producible-only.md) |
| Ids, `renames.tsv`, waves | [ADR 0005](../../../docs/adr/0005-consumer-contract-and-test-case-identity.md) |
| Comparison of analyses | [ADR 0006](../../../docs/adr/0006-comparison-semantics.md) |
| Exceptions, `status.yaml` | [ADR 0007](../../../docs/adr/0007-exceptions-live-in-status-yaml.md) |
| What a test case is valued for | [ADR 0008](../../../docs/adr/0008-value-is-detection.md) |
| Authored versus derived files, generated no-parse words | [ADR 0009](../../../docs/adr/0009-repo-commits-authored-files-only.md) |
| PR order, pins, reproducing a bug, `--propose` | [land-a-conformance-change](../land-a-conformance-change/SKILL.md) |
| Merge, retire, rename, remove a word, periodic review | [maintaining.md](maintaining.md) |

> **Until epic S1 lands** the ADRs' "Today" notes apply: exceptions are the `upstream` field
> (PROTOCOL.md section 12) and prose notes, the manifests, `coverage.csv` and `rules.csv` stay committed
> (AGENTS.md section 2a), words carry `exercises` and `constructs.txt` is the top level of the behaviour-label vocabulary, and merge waves
> wait for the behaviour-label vocabulary. Use `scripts/upstream_status.py` for exception status.

Terms used here beyond the glossary: a **detector** is a test case (or word) that fails when a behaviour or
bug regresses; the **last detector** is the only one that does. A **bug build** is a build with the bug: the
parent of the fix commit, or an unlanded candidate's commit.

## 1. Intake: state the need

Write one line before you touch a file: `<what is detected> | <the word that shows it> | <the reference's
result for that word>`.

| Need arrives as | First action |
|---|---|
| A reference bug (`sillsdev/machine#N`, `LT-N`, `sillsdev/FieldWorks#N`) | Reproduce it on the reference commit (land-a-conformance-change section 3). |
| A PanGloss bug where the reference is right | That is a consumer divergence: it stays in PanGloss under its own issue. No test case. |
| A PanGloss staged case | Replay its staged words on the reference commit. A staged family is one need. |
| A behaviour label, loader function or bug nothing detects | Show with `git grep` that no test case carries it. |
| A generator finding | Reduce it (section 3, step 2) before deciding anything. |

Then classify the change with land-a-conformance-change section 1.

## 2. Admission: decide where it goes

Take the first rung that fits. Paste the evidence into the commit body.

1. **Already detected.** `git grep` the issue id, behaviour label and word shape across `*/words.yaml`,
   `*/README.md`, and the exception notes (`upstream` fields and "Known oracle limitation (machine#N, open)" notes until `status.yaml` exists). If a test case already fails on the bug build, add or update its exception
   if one is due, and stop.
2. **Add words** to a test case whose grammar already produces the case, unchanged.
3. **Extend a grammar** only when every existing word replays unchanged under `--propose`. A moved result means
   the extension interacts: go to rung 4.
4. **Family member**: a new test case beside its family. Name the **cannot-merge reason**:
   - **settings**: different `morpher:` settings *and* a different grammar (settings alone are a `variants:`
     run, PROTOCOL.md section 8);
   - **grammar-wide**: a different character definition table, feature system or stratum structure;
   - **order**: depends on a rule order the sibling cannot take;
   - **loader**: witnesses a different `HCLoader.cs` function;
   - **interaction**: adding it to the sibling moves an existing result (give the `--propose` diff).
5. **New test case**, only for a **behaviour label or loader function nothing detects** (rung 1's `git grep`
   shows none), or a **named bug** (an issue id and the word whose result differs on the bug build). A
   language profile also needs typological territory none of the existing profiles covers.

A staged family or a matrix is one test case with one cell per member (a rebuild merge in
[maintaining.md](maintaining.md)). A new id must not be a retired id of a different test case (`docs/renames.tsv`); restoring the same retired test case under its old id is allowed.
Done when the commit body names the rung, its evidence and, for rungs 4 and 5, the reason.

## 3. Build

1. **Producibility.** Name the `HCLoader.cs` function that writes each behaviour (AGENTS.md section 1). The
   only exception is ADR 0001's pending-upstream allowance.
2. **Minimal grammar.** Start from the nearest sibling and vary **one feature**. Remove every element no word
   needs. Reduce a generator finding the same way.
3. **Words.** At least one **detecting word** and one **control**, each with its behaviour label (ADR 0008).
   Show both by mutation: change the varying feature, run `--propose`, confirm the detecting word's result
   flips and the control's does not. Record the mutation in the README. No-parse words may be generated from a
   declared rule (ADR 0009); the format is decided in epic S5, so until then list them.
4. **Results from the reference only.** In a sillsdev/machine checkout at `ba6dfa106`, run
   `dotnet run --project src/SIL.Machine.Morphology.HermitCrab.Conformance -c Release -- --fixtures <suite clone> --propose`,
   apply its patch unedited, run it again. Never edit a result by hand or take one from a consumer. Read every result against
   the rules; one you cannot explain is reported as a finding.
5. **Check.** AGENTS.md section 4.

Done when the second `--propose` run prints no patch and the checks pass.

## 4. Exceptions

Exceptions live only in one `status.yaml` at the suite root (ADR 0007; created in epic S1), keyed by test case, plus word where
needed. Each has a kind, an upstream ref and a reason:

- **reference defect**: the reference is wrong. Keep the C# result as the expected result and record the
  intended answer, so the gate fails when the fix lands; then delete the exception (ADR 0002).
- **pending upstream**: results come from a build of the upstream PR (ADR 0001).

Until `status.yaml` exists, follow the existing `expect_fail` precedent: keep the C# result and give the word a note "Known oracle limitation (machine#N, open)" with the intended answer. An exception with no upstream issue or PR is not admissible: file the issue first. A duplicate analysis caused
by a C# bug is an exception, never deduplicated (ADR 0006). Never write a tier; it is computed.

## 5. Changed results

Every changed result of an existing word needs one reason in the commit body (`word | old | new | reason`):
**reference change** (cite the Machine PR and both commits), **grammar change**, **result was wrong** (cite the
finding), or **protocol change** (cite the section). A result that moves with no reason is a finding: run
`--propose` three times, confirm the word's `morpher:` block applied, report both results. Never regenerate
results to make a failing run pass.

## 6. Land and report

Route per AGENTS.md "Landing": additions go to `main` after the gate; merges, retirements, renames and
format or protocol changes go through a PR with a sonnet-reviewer LAND verdict. Commit only authored files
(ADR 0009). Report: the need line; the rung and reason; detecting word, control and mutation result; the
changed-result table or "none"; exceptions added; the checks run; the SHA.

Read [maintaining.md](maintaining.md) before you merge, retire or rename a test case, remove a word, or run
the periodic review.
