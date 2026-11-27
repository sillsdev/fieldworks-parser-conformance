# Exceptions live in one status.yaml

Status: accepted (owner, 2026-11-27); amends [ADR 0001](0001-aspirational-upstream-fixtures.md)

## Context

Departures from the reference are tracked in several places today: the `upstream` block in 5 `words.yaml` files and "Known oracle
limitation" prose in 4 `words.yaml` files (16 mentions). Changing an upstream reference rehashes a test case. ADR 0001
introduced the `upstream` field as the machine-readable form of one kind of departure. A consumer cannot list every exception
without reading every `words.yaml`.

## Decision

- All exceptions live in one `status.yaml` at the suite root. A row is keyed by test case, plus word where the exception is
  per word, and carries the upstream ref, the kind and the reason. The kinds are reference defect and pending upstream.
- Consumer divergences, differences only a consumer has, stay in that consumer's repo under its own issue. They never enter this file.
- This amends ADR 0001: its allowance stands, but the dependency is recorded in `status.yaml`, not in the `upstream` field of `words.yaml`.

## Consequences

- One resolver answers "what is known wrong, and where is the upstream fix". Re-pointing an upstream ref no longer rehashes a test case.
- Closing an exception is deleting a row, at the moment the C# gate turns red ([ADR 0002](0002-reference-is-the-only-source-of-expected-results.md)).
- Consumers read one file for exceptions and keep their own divergences elsewhere, so the suite never carries a consumer's quirks.
- Today: `status.yaml` does not exist. Until epic S1 lands it, the `upstream` field ([PROTOCOL.md](../../PROTOCOL.md) section 12) and
  `scripts/upstream_status.py` apply, plus the prose notes.

## Alternatives considered

- **Keep `upstream` per test case.** Rejected: several mechanisms, each parsed differently, and every re-point rehashes a test case.
- **One file per kind.** Rejected: the lifecycle is the same, and a reader looking for "what is wrong with this test case" would need to search several files.
- **Record consumer divergences here too.** Rejected: it gives one consumer's bugs a place in everyone's pinned copy and blurs "the reference says X" with "PanGloss does Y".

## Sources

- Expectation files that record known departures: <https://web-platform-tests.org/tools/wptrunner/docs/expectation.html>
- V8's test262 status file: <https://chromium.googlesource.com/v8/v8.git/+/master/test/test262/test262.status>
- Apache POI integration exceptions list: <https://github.com/apache/poi/blob/trunk/test-data/poi-integration-exceptions.csv>
