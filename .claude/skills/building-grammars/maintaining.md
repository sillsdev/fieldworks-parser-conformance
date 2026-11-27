# Maintaining the suite: merge, retire, remove a word, rename, review

Part of [building-grammars](SKILL.md); its terms and its "until epic S1 lands" note apply here. Merges,
retirements, renames, and changes to the file format or to PROTOCOL.md go through a PR with a
sonnet-reviewer LAND verdict (AGENTS.md, "Landing").

**Detection is the guardrail** ([ADR 0008](../../../docs/adr/0008-value-is-detection.md)):

- the last detector of a bug is never removed;
- the last word carrying a behaviour label is never removed;
- language profiles (`languages/*`) are retired only by owner decision;
- C# code paths only nominate a test case: removal needs a written reason the path is incidental;
- a merged grammar keeps every member's behaviour labels.

Judge by the behaviour labels (`python3 scripts/suite.py labels "<label>"` lists the words carrying one, and a top-level label
includes its children), the exception notes and the bug builds. A label on one test case only is a unique check.

## Merge: fold a family into a survivor

Eligible when the members form a **family** and no cannot-merge reason (SKILL.md section 2) holds between
them. Read the grammars, not a line count.

| Kind | When | Words |
|---|---|---|
| **union** | grammars identical apart from `<Name>` and comments, or one is a superset that replays the other's results | the survivor is an existing member and keeps its id; absorbed words replay |
| **variants** | grammars identical, only `morpher:` settings differ | one `variants:` run per absorbed test case |
| **rebuild** | members share a word list and differ in one parameter | each member becomes a **cell**: its own rule, segments and words, so cells cannot interact |

1. List members, survivor id and kind. The survivor id is not a retired id of a different test case
   (`docs/renames.tsv`) and is not an existing directory other than a member.
2. Write the survivor's grammar; for a rebuild, a cell map from each member's rules and words to the survivor's.
3. Take every result from the reference with `--propose`.
4. **Replay.** Every absorbed word's result is unchanged (rebuild: matches under the cell map). A mismatch
   means the cells interact: leave that member out and say `interaction` in the family README.
5. **Detection.** For each bug a member detects, the survivor still fails on the bug build; each member's
   behaviour labels are carried over. A member that cannot be shown stays out.
6. Carry over notes, citations and exceptions (re-keyed to the survivor).
7. Remove the absorbed directories, append one `docs/renames.tsv` line per absorbed id, run the checks.
8. The commit body carries the cell map, the replay and detection results, the test case count before and
   after, and the changed-result table.

## Retire

Retire a test case only when each of these is checked and written in the commit body:

1. It is not the last detector of any bug and no exception names it.
2. It carries no behaviour label that no other word carries.
3. It is not a language profile, unless the owner decided to retire it.
4. If a C# code path is unique to it, the commit gives the reason the path is incidental.
5. A named test case covers what it detected (this is `covered_by`).

Then remove the directory, append its `docs/renames.tsv` line, run the checks.

## Remove a word

Only for one of these, named in the commit body: **result was wrong** (cite the finding), **merge** (the cell
map names the word that stands for it), or **generated no-parse word** (ADR 0009). Never remove the last word
carrying a behaviour label or the only word that fails on a bug build.

## Rename, and telling the consumers

Consumers pin the suite by commit ([ADR 0005](../../../docs/adr/0005-consumer-contract-and-test-case-identity.md)),
so a rename, merge or retirement lands on `main` first and consumers follow at their next bump. An id is its directory path,
is never reused for a different test case once retired, and never encodes tier, status or exception state.

**`docs/renames.tsv` is a contract.** Tab-separated, one header line, columns in this order:

| Column | Value |
|---|---|
| `old_id` | the removed test case's path (`edge-cases/<name>`, `languages/<name>`) |
| `new_id` | the replacing id, or the literal `retired` |
| `covered_by` | for `retired`, the id that covers what it detected; otherwise empty |
| `wave` | the wave that removed it, named `wave-YYYY-MM-DD`; never empty |

Lines are appended, never edited or removed. Restoring a retired test case appends `X`, `X`, empty, `wave`, and each id's last entry rules; a retired id never becomes another id's `new_id`. Each settled wave gets a git tag with the same name.

The consumer contract is the `docs/renames.tsv` entries plus the wave tag. After the wave lands, notify the
PanGloss lead with the tag and the new entries.

## Periodic review

When asked for one, list the test cases whose every bug and behaviour label is detected elsewhere, and
exceptions that `python3 scripts/suite.py status` reports resolved. Report each candidate with a proposed decision
(merge, retire, keep with reason) to the requester; apply accepted decisions with this page.
