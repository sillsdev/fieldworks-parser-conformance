# Scope: only grammars FieldWorks can produce; XAmple is out

Status: accepted (owner, 2026-11-27)

## Context

The suite exists so engines that parse for FieldWorks can be compared on the grammars FieldWorks users actually have. FieldWorks builds
every grammar through `HCLoader.cs`, which reaches less than the HermitCrab XML can say. An engine-only grammar,
valid XML that no FieldWorks project can yield, can be expressive but tests behaviour no user can reach; the
[retirement doc](../engine-only-fixture-retirement.md) records what was removed on that ground.
Separately, issue #23 asked for XAmple as a second reference.

## Decision

- Scope is grammars HCLoader can write. The evidence is a claim read from `HCLoader.cs`, plus optional FieldWorks project
  witnesses (PROTOCOL.md section 10). Engine-only test cases belong to the consumers' own tests.
- The exception is ADR 0001's pending-upstream allowance: a grammar needing a construct that an open FieldWorks or Machine
  change would make writable may be kept.
- XAmple is out of scope as a second reference. [ADR 0002](0002-reference-is-the-only-source-of-expected-results.md) allows one
  source of expected results. XAmple compatibility is at most a descriptive label. Issue #23 is closed with this reasoning.

## Consequences

- Every test case answers "could a FieldWorks user hit this?" with yes, or with a cited upstream change that would make it so.
- A consumer's engine-only cases have a home that is not this suite, so the suite stays small enough to review.
- XAmple-subset grammars remain visible as a computed label in the reader index, not as a source of results.
- Today: `fieldworks_producible: true` is carried by every `words.yaml` (279) and the DTD census is
  `fieldworks-writable-shapes.tsv`. The field is a flag that is never `false`, so it carries no information; epic S1 drops it, and the
  evidence moves to the census and witnesses. Until S1 lands, the field is still required by the schema check and consumer gates.
  Issue #23 is closed when this ADR lands.

## Alternatives considered

- **Keep every expressible grammar.** Rejected: it tests behaviour no FieldWorks user can reach and inflates the suite.
- **XAmple as a second reference.** Rejected: two sources of expected results need an arbitration rule, XAmple's semantics differ
  from HermitCrab's, and FieldWorks users get HermitCrab results for the grammars in scope.
- **Require a witness for every test case.** Rejected for now: a claim read from the loader is cheaper and the witness
  stays optional strong evidence.
