# A test case is valued by what it detects

Status: accepted (owner, 2026-11-27)

## Context

The suite has 263 conformance test cases across several waves of authoring and a plan to merge duplicates. Merging needs a rule for "unique".
Coverage-based reduction (afl-cmin, libFuzzer `-merge`, suite-reduction literature in the research notes) is cheap but keeps
whatever happens to reach new code, and test262-style suites govern by feature labels. Owner's words: "it is in the different
interacting names and rules we can easily look for duplicates or truly unique checks."

## Decision

A test case is valued by what it detects, in this order.

1. **Bugs**, open or fixed. The last detector of a bug is never removed.
2. **Behaviour labels**, from a hierarchical vocabulary. Its top level is the current 31 constructs; it names sub-behaviours and
   interactions. The last word carrying a label is never removed. A new label is admitted only when it names something no existing
   label does.
3. **Language profiles** (`languages/*`), judged as representatives of a language type and retired only by owner decision.
4. **C# code paths unique to the test case**, as a backstop that only nominates. Removal needs a written reason the path is incidental.

A grammar may test several behaviours, provided every word carries its behaviour label, so a failing word points to one behaviour.
A merged grammar keeps every label of its members.

## Consequences

- Pruning is decidable: a test case is redundant when every bug it detects and every label it carries is covered elsewhere.
- Merging is safe because labels, not directory names, are the unit that must survive; combined grammars lose no checks.
- Cost: every word needs a label, and the vocabulary needs an owner so it does not grow by synonym.
- Today: words carry an `exercises` tag, per word and per parse, and `constructs.txt` lists the 31 constructs. The sub-behaviour
  and interaction vocabulary and the per-word label requirement are not built. Until S1 and its behaviour-label sub-issue land,
  `exercises` and `constructs.txt` apply and merge waves wait for the vocabulary.
  The code-path backstop needs coverage runs the Machine runner can already produce.

## Alternatives considered

- **Coverage-only reduction.** Rejected: it keeps one arbitrary representative per path and discards bug detectors that share a path.
- **One behaviour per grammar.** Rejected: it multiplies grammars; labelled words give the same attribution in one grammar.
- **Keep everything.** Rejected: duplicate checks make waves slower to review and hide what is truly unique.
