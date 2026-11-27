# A test case is valued by what it detects

Status: accepted (owner, 2026-11-27)

## Context

The suite has 263 conformance test cases across several waves of authoring and a plan to merge duplicates. Merging needs a rule for "unique".
Coverage-based reduction (afl-cmin, libFuzzer `-merge`) is cheap but keeps whatever happens to reach new code. Owner's words: "it is in the different
interacting names and rules we can easily look for duplicates or truly unique checks."

## Decision

A test case is valued by what it detects.

1. **Bugs**, open or fixed. The last detector of a bug is never removed.
2. **Behaviour labels**, from a hierarchical vocabulary. Its top level is the current 31 constructs; it names sub-behaviours and
   interactions. The last word carrying a label is never removed. A new label is admitted only when it names something no existing
   label does.
3. **Language profiles** (`languages/*`), judged as representatives of a language type and retired only by owner decision.
4. **C# code paths unique to the test case**, as a backstop that only nominates. Removal needs a written reason the path is incidental.

A grammar may test several behaviours, provided every word carries its behaviour label, so a failing word points to one behaviour.
A merged grammar keeps every label of its members.

## Consequences

- A test case is a candidate for removal when every bug it detects and every label it carries is covered elsewhere, subject to items 3 and 4: a language profile is retired only by owner decision, and a code path only nominates, so removal needs a written reason the path is incidental.
- Merging is safe because labels, not directory names, are the unit that must survive; combined grammars lose no checks.
- Cost: every word needs a label.
- Today: words carry their behaviour labels in `exercises`, per word and per parse; `constructs.txt` is the top level and `labels.tsv` holds
  the child levels, with the existing labels each was checked against. `python3 scripts/suite.py check` fails on a word with no label
  or a label outside the vocabulary, and `python3 scripts/suite.py labels` prints the label-to-words table (PROTOCOL.md section 14).

## Alternatives considered

- **Coverage-only reduction.** Rejected: it keeps one arbitrary representative per path and discards bug detectors that share a path.
- **One behaviour per grammar.** Rejected: it multiplies grammars; labelled words give the same attribution in one grammar.
- **Keep everything.** Rejected: duplicate checks make waves slower to review and hide what is truly unique.

## Sources

- AFL technical details (corpus culling): <https://lcamtuf.coredump.cx/afl/technical_details.txt>
- libFuzzer corpus merging: <https://llvm.org/docs/LibFuzzer.html>
- Regression test selection and minimisation survey: <https://www.cse.chalmers.se/~feldt/advice/yoo_2010_regression_testing_survey.pdf>
