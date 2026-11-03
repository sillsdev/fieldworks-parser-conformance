---
name: land-a-conformance-change
description: >-
  Use when a change touches expected parses across the suite, sillsdev/machine and PanGloss. Triggers: fixing a
  parser bug that changes expected parses; adding or changing a fixture or words; pinning a bug with a fixture;
  bumping `conformance.commit` in machine or PanGloss; landing stacked PRs across the suite, machine and
  PanGloss; "which order do these PRs land in"; a consumer fails rows the suite expects.
---

# Land a conformance change

This skill says which PRs a change needs, in what order, and what each repository's pin names at each step.
Mechanics live elsewhere; follow the links and do not restate them:

- Fixture files, producibility, generated files, checks: [AGENTS.md](../../../AGENTS.md).
- Growth policy (every bug fix lands with a fixture): [CONTRIBUTING.md](../../../CONTRIBUTING.md).
- Row format, signatures, the `batch` contract: [PROTOCOL.md](../../../PROTOCOL.md).
- Engine builds behind the rows: [PROVENANCE.md](../../../PROVENANCE.md).
- How consumers pin and read the suite: [docs/consuming.md](../../../docs/consuming.md).

Three repositories take part. Each pins another by commit:

| Repository | Holds | Pin it keeps |
|---|---|---|
| Suite (`sillsdev/fieldworks-parser-conformance`) | grammars, expected rows, manifests | none today |
| Machine (`sillsdev/machine`) | the reference engine (C# HermitCrab) and the runner `hc-conformance` | `conformance.commit`: a suite commit |
| PanGloss | the Rust engine, a port under test | `conformance.commit`: a suite commit |

The reference engine is machine's C# HermitCrab. A row is correct when the reference engine produces it and the
rules in the grammar explain it. Rows are never written from memory.

## Rules

- Never force-push without the owner's approval.
- Land in the order this page gives. A later PR names the earlier one in its body.
- One PR per repository per step.
- Every PR body says which other PRs it depends on and the landing order, with links.
- A pin is the full 40-character SHA of a commit on the suite's `main`. Machine and PanGloss CI fail a pin that is
  not an ancestor of the suite's `origin/main`. Never pin a branch commit, and never pin a squashed-away SHA.
- Do not edit `conformance/` inside machine or PanGloss. A suite change is a suite PR.
- Do not push, open a PR or tag unless the owner asked.

## 1. Classify the change

| Class | Test | Suite PR | Machine PR | PanGloss PR |
|---|---|---|---|---|
| (a) Suite only | The reference engine already produces the new or changed rows. | yes | pin bump | pin bump |
| (b) Reference-engine fix | The reference engine is wrong, and the fix changes expected rows. | yes, rows from the fixed engine | the fix, then the pin bump | pin bump, then port the fix or record a divergence |
| (c) PanGloss only | PanGloss differs from the reference and the reference is right. | only if no fixture pins it | none | the fix, or a divergence-ledger entry |
| (d) Docs or tooling | No fixture, grammar or row changes. | yes | pin bump only if a consumer needs it | pin bump only if a consumer needs it |

If you cannot tell, reproduce on the reference engine first (section 3).

## 2. Order of PRs and what each pin names

### (a) Suite only

| Step | PR | Suite `main` | Machine pin | PanGloss pin |
|---|---|---|---|---|
| 1 | Suite: fixture or words, rows taken from the reference engine | S0 -> S1 on merge | S0 | S0 |
| 2 | Machine: bump pin to S1, CI green, merge | S1 | S1 | S0 |
| 3 | PanGloss: bump pin to S1. Fix or record the rows it fails. | S1 | S1 | S1 |

Run machine's runner on the suite branch before step 1 merges (section 4). Suite CI does not run an engine.

### (b) Reference-engine fix

Today's order. The machine fix PR is based on machine `master`, or stacked on other machine PRs.

| Step | PR | Suite `main` | Machine pin | PanGloss pin |
|---|---|---|---|---|
| 1 | Machine fix PR (F) opened. It does not touch the pin. | S0 | S0 | S0 |
| 2 | Suite PR: expected rows captured by running machine's runner built from F's head against the suite branch (`HC_CONFORMANCE_SUITE` or `--fixtures`). Record F's head SHA in the fixture's `# oracle-provenance:` header and in [PROVENANCE.md](../../../PROVENANCE.md). | S0 | S0 | S0 |
| 3 | Suite PR lands. | S1 | S0 | S0 |
| 4 | F bumps `conformance.commit` to S1. Its CI passes. | S1 | S1 on F | S0 |
| 5 | F lands on machine `master`. Stacked machine PRs land base-first. | S1 | S1 | S0 |
| 6 | PanGloss bumps its pin to S1 and ports the fix, or records a divergence (class (c) steps). | S1 | S1 | S1 |

Stacked machine PRs:

- Land the base PR first, then rebase the next onto `master`, then land it.
- A machine PR must not bump the pin past rows its base does not yet satisfy. If PR B is stacked on PR A and
  S1 holds rows only A's fix produces, bump the pin in A, not in B. A bump in B alone fails B's CI until A lands.
- Capture each suite row set from the head that carries the fix for it. If rows need two machine PRs together,
  name both heads in the provenance header and say so in the suite PR.
- Every machine PR in a stack states its base and the landing order in its body.

**Hazard.** Between step 3 and step 5 the suite's `main` holds rows that machine `master` fails. Any other
consumer that bumps its pin to S1 or later fails those rows. Before step 3, tell the other consumers' owners not to
bump. Keep steps 3 to 5 as short as review allows. If F is slow, hold the suite PR in draft until F is approved.

Step 4 is why the order is suite first: machine's CI needs S1 to exist on the suite's `main`.

#### When #32 is built

This subsection describes a PROPOSED process
([suite issue #32](https://github.com/sillsdev/fieldworks-parser-conformance/issues/32)). It is not built.
Check that `reference.commit` exists at the repository root before using it; if not, use the order above.

Proposed: `reference.commit` names a machine commit. A suite CI job builds `hc-conformance` at that commit and runs
it on every suite PR. A row may carry `pending: sillsdev/machine#N`. The job accepts a failure only on pending
rows and reports a pending row that now passes. Machine's runner reports pending rows as pending, not failed.

| Step | PR | Suite `main` | `reference.commit` | Machine pin |
|---|---|---|---|---|
| 1 | Machine fix PR F opened (as above). | S0 | R0 | S0 |
| 2 | Suite PR: new rows marked `pending: sillsdev/machine#F`. Its CI passes on R0 because the failures are pending. | S0 -> S1 | R0 | S0 |
| 3 | Machine pin bump to S1 may land with or before F: pending rows do not fail. | S1 | R0 | S1 |
| 4 | F lands on machine `master` at commit R1. | S1 | R0 | S1 |
| 5 | Follow-up suite PR: clear `pending` on the rows, bump `reference.commit` to R1. The job reports the rows now pass. | S2 | R1 | S1 |
| 6 | Consumers bump to S2. | S2 | R1 | S2 |

The hazard narrows to pending rows, which consumers report as pending. Do not describe this as current until the
issue is closed and the file exists.

### (c) PanGloss-only difference

1. Reproduce on the reference engine (section 3). The reference is right.
2. If no fixture pins the behaviour, add one by class (a) first. The fixture is what shows PanGloss differs.
3. In PanGloss, fix the defect, or write a divergence-ledger entry (`docs/divergences/`) when the difference is
   planned to stay. Keep the waiver list in step with the ledger.
4. Open a machine issue only if the evidence also implicates the reference engine.

### (d) Docs or tooling

Suite PR only. Run the checks in section 4. Bump a consumer's pin only when it needs the change, for example a
fixed checker. A change that moves a manifest hash (anything in `generated/`) is not class (d).

## 3. A bug found by a consumer

1. Reproduce on the reference engine: run machine's runner or `batch` ([PROTOCOL.md](../../../PROTOCOL.md)) on the
   same grammar and words. Name the machine commit.
2. Decide who is wrong.

| Finding | Class | Action |
|---|---|---|
| Reference produces the suite's row; the consumer differs | (c), or a consumer-only bug | Fix the consumer. |
| Reference differs from the suite's row, and the reference is wrong | (b) | Machine fix PR, then the order in 2(b). |
| Reference differs from the suite's row, and the row is wrong | (a) | Suite PR with regenerated rows, citing the reference build. |
| Reference and suite agree, and both are wrong | (b) | Prove it by forward synthesis. Pin the right answer in a fixture and open a machine issue. |

3. A reference that is wrong needs proof: a hand-traced forward synthesis that builds the surface form. Write the
   trace in the fixture comment, set `oracle-provenance` to say which rows are recorded and which are derived, and
   link the machine issue. Without a fix PR the fixture is an unexplained failure.
4. Pin the bug with a fixture whenever one is missing ([CONTRIBUTING.md](../../../CONTRIBUTING.md)): add a word first,
   then extend a grammar, then add an edge case. A fixture that has never failed has proved nothing; show it failing
   on the unfixed engine.

## 4. Checks before each PR

Suite PR, from `<suite clone>` ([AGENTS.md](../../../AGENTS.md) section 4; the list is the one in
`.github/workflows/checks.yml`):

```
python3 scripts/generate_manifest.py --check
python3 scripts/check_words_schema.py
python3 scripts/check_dtd.py
python3 scripts/check_grammars_md.py
python3 scripts/check_fwdata.py
python3 parity-check.py
python3 scripts/check_links.py
python3 scripts/privacy_lint.py
```

Then run machine's runner against the suite branch, from `<machine clone>` with `<hc>` meaning
`dotnet run --project src/SIL.Machine.Morphology.HermitCrab.Conformance -c Release --`:

```
<hc> --fixtures <suite clone> --include-pathological
<hc> --fixtures <suite clone>/stress --include-pathological
<hc> --fixtures <suite clone> --check-manifest
HC_CONFORMANCE_SUITE=<suite clone> dotnet test tests/SIL.Machine.Morphology.HermitCrab.Tests -c Release --filter "FullyQualifiedName~ConformanceFixtureGateTests|FullyQualifiedName~ConformanceManifestTests|FullyQualifiedName~FieldWorksProducibleShapeTests"
```

- Build the runner from the machine commit that supplies the rows: the fix PR head for class (b), `master` for (a).
- `--propose` prints the `words.yaml` patch for each mismatch and writes nothing. Read every row against the rules.
- `HC_CONFORMANCE_SUITE` skips machine's pin check. That is intended for trying a suite branch. It also means a
  green local run says nothing about whether the pin is on the suite's `main`.
- Suite CI runs no engine. A fixture that machine's runner rejects can pass suite CI, land and be tagged. Always run
  the runner locally before a fixture change lands. (Until #32 is built, nothing else catches it.)

Machine PR that bumps the pin ([machine runner README](https://github.com/sillsdev/machine/blob/master/src/SIL.Machine.Morphology.HermitCrab.Conformance/README.md)):

1. Put the 40-character SHA of the suite commit on the one line of `conformance.commit`.
2. Build once so `conformance/` moves to it. Check that `cat conformance.commit` and `git -C conformance rev-parse HEAD`
   match.
3. Run the commands in that README's "Before you push". CI also checks the pin is on the suite's `main`.
4. Commit with a message that says what is now true, such as "Run the conformance suite at `<short sha>`, which adds
   the `<name>` fixture".

PanGloss pin bump: put the SHA in `conformance.commit`, run its conformance gate (`rust/tools/conformance.ps1`
fetches the suite at the pin; `rust/tools/run-conformance.sh` runs it), then act on each failing row: fix, or record a
divergence. A staged copy of a fixture that is now in the suite is deleted in the same commit as the bump.

## 5. Releases

After a fixture change lands on the suite's `main`:

1. Tag the next patch version (`v0.1.x`) on the merge commit. List tags first (`git tag`) and take the next number.
2. Write release notes: fixtures added, changed or removed; the machine commit the rows were recorded on; which
   consumers must bump.
3. Consumers may pin a tag's commit. A pin is still the commit SHA, and it must be on `main`.
4. Do not tag a commit whose fixtures machine's runner rejects. Run the section 4 commands on the tagged commit.

Tagging is a push. Do it only when the owner asks.

## 6. PR body checklist

- Class (a) to (d), and the PRs it depends on, in landing order, with links.
- Which engine and which commit produced each changed row; whether a FieldWorks witness backs the claim
  ([AGENTS.md](../../../AGENTS.md) section 1).
- Checks run, with the result of each. Name any check you skipped.
- For class (b): the hazard window and who was told not to bump.
- The line "Do not merge before `<PR>`" when the order matters.

## Stop and ask the owner

- A pin would point at a commit that is not on the suite's `main`.
- A rebase or force-push of a PR that other PRs depend on.
- A row that the reference engine produces and you cannot explain.
- Two machine PRs in a stack disagree about which rows they satisfy.
