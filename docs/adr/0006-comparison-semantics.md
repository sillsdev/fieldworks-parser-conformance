# Comparison: a multiset of analyses keyed by signature

Status: accepted (owner, 2026-11-27)

## Context

A word can have several analyses, and an engine may return them in any order and may return the same analysis twice. Comparing sorted
strings hides duplicates and makes order a test failure. Machine #506 showed the C# result order varies under parallel analysis,
and #556 fixes the multiset though not the order.

## Decision

- A word's expected result is a multiset of analyses, compared ignoring order. Duplicates count.
- The comparison key is the signature: morph ids plus surface form (PROTOCOL.md section 3).
- The reference run is single-threaded and deterministic.
- A duplicate caused by a C# bug is recorded as an exception ([ADR 0007](0007-exceptions-live-in-status-yaml.md)),
  never silently deduplicated.

## Consequences

- Order differences are never failures. Count differences are, so a consumer that over- or under-generates is caught.
- A duplicate is a visible, trackable item with an upstream link rather than a normalised-away accident.
- The deterministic single-threaded run means regenerating results from the same reference commit gives the same bytes.
- Today: PROTOCOL.md sections 3 and 4 already sort signatures without deduplicating and compare them as a multiset, so this ADR matches current
  behaviour. What is not built until S1 lands: exception rows for duplicates, because `status.yaml` does not exist; the existing
  duplicate-bearing cases are explained in `words.yaml` notes.

## Alternatives considered

- **Compare sets (deduplicate).** Rejected: it hides an engine returning the same parse twice, which FieldWorks would display twice.
- **Compare ordered lists.** Rejected: order is nondeterministic under parallelism in the reference itself.
- **Key on surface form only.** Rejected: two analyses with the same surface form and different morphemes are different parses.
