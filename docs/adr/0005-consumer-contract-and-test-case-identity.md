# The consumer contract and test case identity

Status: accepted (owner, 2026-11-27)

## Context

Consumers (PanGloss, Machine) pin a commit of this repository. Merging and retiring test cases is planned, so ids will change. Without a
rule a consumer's own records of "which test case covers what" silently dangle. Mature suites (test262, CommonMark,
html5lib-tests) keep names stable and track renames explicitly rather than promising compatibility.

## Decision

- Consumers pin a commit. There are no compatibility promises beyond what follows.
- Every wave that renames or removes test cases appends rows to `docs/renames.tsv`. Its columns never break:
  `old_id`, `new_id` (or `retired`), `covered_by`, then any extra columns (`wave`) at the end.
- Each settled wave gets a git tag `wave-YYYY-MM-DD`. A second wave on the same date takes a numeric suffix: `wave-YYYY-MM-DD-2`, then `-3`.
- A test case's id is its directory path: a stable public name. It never encodes tier, status or exception state.
- An id is never reused once retired. Restoring the same retired test case under its old id is not reuse.
- A merge keeps one member's id and maps the other members in `renames.tsv`.
- Chains are allowed: `renames.tsv` is append-only, so a consumer resolves an old id by following last entries to a live id or `retired`.

## Consequences

- A consumer bumping its pin reads `renames.tsv` between its old and new commit and updates its own records mechanically.
- Wave tags give consumers named, settled points to pin.
- Ids that cannot change when a test case's status changes mean an exception ([ADR 0007](0007-exceptions-live-in-status-yaml.md))
  never forces a rename.
- Cost: a directory path is a long, language-flavoured name that cannot be tidied later, so names are chosen once.
- Today: `docs/renames.tsv` exists and lists the retired ids; `scripts/check_renames.py` enforces it. Wave tags `wave-YYYY-MM-DD` are applied after each wave merges.

## Alternatives considered

- **Opaque numeric ids.** Rejected: unreadable in diffs and failure output, and still need a rename map when cases merge.
- **Ids that encode tier or status.** Rejected: every promotion or exception change would be a rename.
- **Semantic-version releases with compatibility promises.** Rejected: the suite is pinned by commit and changes shape too often to promise anything.
- **Allow reuse of retired ids.** Rejected: an old pin would silently mean a different test case.

## Sources

- test262 contribution rules: <https://github.com/tc39/test262/blob/main/CONTRIBUTING.md>
- JSON Schema Test Suite: <https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/main/README.md>
- toml-test: <https://github.com/toml-lang/toml-test/blob/master/README.md>
