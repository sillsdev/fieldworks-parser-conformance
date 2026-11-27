# The reference is the only source of expected results

Status: accepted (owner, 2026-11-27)

## Context

A conformance suite is only as trustworthy as its expected results. Differential-testing practice takes expected results from one named implementation or spec and records every
departure explicitly, rather than patching results to make a consumer pass. The suite has two
kinds of departure from the C# HermitCrab: places where C# is wrong today, and places where C# should change once an
upstream pull request lands ([ADR 0001](0001-aspirational-upstream-fixtures.md)).

## Decision

The reference, the C# HermitCrab at the pinned reference commit ([ADR 0003](0003-reference-commit-may-be-unmerged.md)), is the only
source of expected results.

- Every departure from it is an exception with an upstream link ([ADR 0007](0007-exceptions-live-in-status-yaml.md)). One mechanism covers
  both "C# is wrong today" and "C# should do this once an upstream change lands".
- Results are never hand-edited and never taken from a consumer.
- A word the reference gets wrong keeps the C# result as its expected result. The exception records the intended
  answer, so the C# gate fails loudly when a fix lands; that failure is the signal to close the exception.
- A test case that waits on an unmerged upstream PR takes its results from a build of that PR (ADR 0001).

## Consequences

- The suite never encodes an answer nobody can reproduce. Every expected result is regenerable from the reference commit, except pending-upstream results, which come from the upstream PR build.
- A fix in Machine shows up as a red C# gate on exactly the words concerned, not as silent drift.
- Cost: a consumer that is right and the reference that is wrong still needs an exception row and an upstream issue
  before the suite will say so.
- Today: `status.yaml` holds a row per exception, and a word row carries the intended answer (`intended:`) that `suite.py check`
  validates. The 16 "Known oracle limitation" prose notes are the rows that still need a hand-traced answer there.

## Alternatives considered

- **Take expected results from the best-agreeing consumer.** Rejected: it makes the suite circular and lets a
  consumer's bug become the standard.
- **Hand-correct results where C# is known wrong.** Rejected: results stop being reproducible and the upstream bug loses its detector.
- **Two mechanisms, one for defects and one for pending upstream work.** Rejected: the lifecycle is identical (cite, wait,
  close), so a second mechanism only splits the bookkeeping.

## Sources

- Differential testing: <https://en.wikipedia.org/wiki/Differential_testing>
- Csmith, differential testing of C compilers: <https://github.com/csmith-project/csmith>
- test262, expected results governed by the spec with a status file for departures: <https://github.com/tc39/test262/blob/main/INTERPRETING.md>
