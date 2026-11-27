# The reference commit may be an unmerged Machine commit

Status: accepted (owner, 2026-11-27)

## Context

The reference engine lives in sillsdev/machine. The behaviour the suite needs (ordering fixes, the conformance runner, writable
affix `maxApps`) sits in open pull requests, so master alone cannot generate or verify the results. The current
reference commit, `ba6dfa106`, is the tip of machine #615, which is stacked on #500 and #556. Machine #506 showed analysis
order varies under parallelism and that #556 makes the multiset deterministic, so an older master would give unstable results.

## Decision

The reference commit may be an unmerged Machine commit, provided that:

- a tag in sillsdev/machine keeps it reachable, so force-pushes and branch deletion cannot orphan it;
- it is recorded in exactly one place in the suite, the `reference.commit` file;
- it is re-pointed to master within one wave of its PR merging.

## Consequences

- The suite is never blocked on Machine's review queue, and CI builds the engine at one commit (the `reference-engine` job).
- A single pin means a bump is one-line and reviewable; no result header names a different build.
- Risk: an unreachable commit invalidates every result at once, hence the tag requirement. A stale pin after merge
  is bounded to one wave by the re-point rule.
- Today: `reference.commit` holds `ba6dfa106` and CI builds it. The tag in sillsdev/machine and the "one wave" re-point are
  owner discipline, not checked by a script. Until epic S1 lands, `PROVENANCE.md` and per-test-case `# oracle-provenance:`
  header lines also name builds; they are to be reduced to the one pin.

## Alternatives considered

- **Pin to master only.** Rejected: master lacks the fixes the suite depends on, and results would be unstable under parallelism.
- **Pin to a release.** Rejected: Machine releases lag the work and would hold the suite behind the same review queue.
- **Record the build per test case.** Rejected: several pins drift apart, and a re-point means editing many files and rehashing them.
