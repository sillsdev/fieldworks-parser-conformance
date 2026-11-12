# Updating the conformance suite

This file says how to change the suite and what to run before the change leaves your machine. It applies to
this repository, which engines (sillsdev/machine's C# HermitCrab and PanGloss) consume as a clone pinned by
commit, not as a submodule. Nothing here assumes any engine's build, layout or language. Commands run from the root of this
repository; `python3` is the only tool the checks need.

If this file disagrees with `.github/workflows/`, the scripts in `scripts/`, or the files you are changing,
prefer the executable behaviour and say so.

## 1. The rule

The suite covers only grammars a real FieldWorks project can produce. FieldWorks builds every grammar
through `HCLoader.cs` (`Src/LexText/ParserCore/HCLoader.cs` in the FieldWorks repository), and that loader
reaches less than the HermitCrab XML can say. A grammar that needs a construct the loader never writes does
not belong here, however expressible it is in the XML and however well an engine handles it.

- Before you author, change or keep a fixture, check each construct it uses against the table in
  [docs/fieldworks-cannot-say.md](docs/fieldworks-cannot-say.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it), against the census
  `fieldworks-writable-shapes.tsv` (every DTD member, with the `HCLoader.cs` line that writes it, only labels
  it, or never writes it), and against [PROTOCOL.md](PROTOCOL.md) section 9.
- The standard is the round trip: a real FieldWorks project, put through the loader, yields the grammar. Reading
  the loader source is weaker evidence. `fieldworks_producible: true` is a claim read from the loader until the
  fixture has a FieldWorks witness (section 3), and only the 11 fixtures that carry one are certified today (of
  137; none of the 16 stress fixtures has one). Say which of the two you are relying on in the pull request.
- If the grammar needs a construct in that table, stop. Rewrite the grammar without it or do not add it.
  Do not relax `fieldworks_producible`: every fixture must carry `true`, and `scripts/check_words_schema.py`
  and the consuming engines' gates fail on anything else.
- A new construct goes into `fieldworks-writable-shapes.tsv`, with its loader line, before a fixture may use it.

## 2. Adding, changing or deleting a fixture

A fixture is a directory under `languages/` or `edge-cases/` holding `grammar.xml` and `words.yaml`, and
optionally a `README.md` and a `fieldworks/` witness. [docs/what-it-is.md](docs/what-it-is.md) and
[docs/consuming.md](docs/consuming.md) ("Consuming the suite from another repository") describe the files; `schema/words.schema.json` and
`HermitCrabInput.dtd` validate them.

1. Check producibility (section 1). Name the `HCLoader.cs` function that writes each construct you rely on.
2. Write `grammar.xml` and `words.yaml`. Put `fieldworks_producible: true` directly after `requires`.
   Give each word a `note` that says what it pins.
3. Take the expected rows from an engine run, never from memory. Run the consuming engine's self-check or
   adapter with a `--propose`-style option if it has one (sillsdev/machine's runner does), or run an engine
   through the `batch` contract in [PROTOCOL.md](PROTOCOL.md) and read its TSV. Read every row against the
   rules before you accept it. A row the engine produces and you cannot explain is a finding, not a pin.
   Record the build you took the rows from in the fixture's `words.yaml` header
   (`# oracle-provenance: ...`) and, if it is a new build, add it to [PROVENANCE.md](PROVENANCE.md).
4. Update [docs/grammars.md](docs/grammars.md): one bullet per fixture, in the group it belongs to, in the
   form `` - `edge-cases/name`: one short line. `` `scripts/check_grammars_md.py` fails if a fixture is
   missing, listed twice or gone.
5. If you ruled a construct out, add a row to the table in [docs/fieldworks-cannot-say.md](docs/fieldworks-cannot-say.md) named in section 1 and, when the loader
   verdict changed, update `fieldworks-writable-shapes.tsv`. Cite the `HCLoader.cs` function and line, and
   the FieldWorks commit you read. If you delete a fixture for this reason, add its row to the table in
   [docs/engine-only-fixture-retirement.md](docs/engine-only-fixture-retirement.md).
6. Regenerate the manifest (section 2a), then read the `git diff`. The manifest should move only for the
   fixtures you touched.
7. Delete a fixture by removing its directory and its line in `docs/grammars.md`, then regenerating. Remove a
   `dead-rules-allowed.tsv` line that names it.
8. Tell the consuming engines. sillsdev/machine and PanGloss each pin a commit of `main` in `conformance.commit`,
   so a change reaches an engine when it bumps that pin. Their own self-check is regenerated on their side, not
   here. The order of the pull requests, and what each pin names at each step, is in
   [.claude/skills/land-a-conformance-change/SKILL.md](.claude/skills/land-a-conformance-change/SKILL.md).

### 2a. Generated files

| File | Written by | Checked by |
|---|---|---|
| `generated/hc-conformance-manifest.v2.json` | `python3 scripts/generate_manifest.py` | `python3 scripts/generate_manifest.py --check`, and CI |
| `generated/stress-manifest.v2.json` | the same command | the same `--check`, and CI |
| `coverage.csv`, `rules.csv` | the consuming engine's coverage report (sillsdev/machine's runner: `--coverage-report`) | that engine's CI; **not yet checked here** |

- The stress manifest lists `stress/edge-cases/*` in the same layout and is kept apart from the conformance
  manifest, which consumers pin: changing a stress fixture changes only the stress manifest.
- The manifest hashes `grammar.xml` and `words.yaml` of every fixture, the DTD, `constructs.txt`,
  `parity-check.py` and the two schemas. Editing a fixture `README.md`, a file under `docs/`, or this file
  changes nothing generated.
- `coverage.csv` and `rules.csv` are derived from `words.yaml` and `constructs.txt`. Until a Python generator
  exists here, regenerate them with the consuming engine's runner and commit the result in this repository.

### 2b. Hand-edited files with no generator

| File | Change it when |
|---|---|
| `dead-rules-allowed.tsv` | a fixture declares a rule on purpose that no word exercises (add a row with the reason), or a word now exercises an allowed rule (delete the row). |
| `constructs.txt` | the checklist of constructs gains or loses an entry. |
| `fieldworks-writable-shapes.tsv` | the loader census changes (section 1). |
| `PROVENANCE.md` | a new engine build supplied ground truth. |

## 3. Optional FieldWorks witnesses

A `fieldworks_producible: true` fixture may carry a `fieldworks/` directory with a real FieldWorks project.
[PROTOCOL.md](PROTOCOL.md) section 10 defines it. This repository stores witnesses and checks their shape;
it never opens one. The PanGloss `xample-projector` tool produces and reads them; it stays in PanGloss.

- Add one only when a real project backs the claim. Do not hand-edit `project.fwdata`.
- The directory holds exactly `project.fwdata`, `phonology-mutations.yaml` and `WritingSystemStore/`, and
  `WritingSystemStore/` holds only `.ldml` files.
- Keep each `.ldml` minimal: only the elements that define the writing system (`identity`, `layout`,
  `characters`, `delimiters`, `collations`, `special`). Remove the CLDR locale data LibLCM copies in
  (dates, numbers, units, display names); nothing reads it. Keep the `generation` date at the value the
  other witnesses use, so identical writing systems stay byte-identical.
- `phonology-mutations.yaml` carries `version: 1` and a `base_sha256` equal to the SHA-256 of
  `project.fwdata`. Recompute it whenever the project changes. `scripts/check_fwdata.py` checks it.
- `.gitattributes` marks `*.fwdata` binary: its exact bytes are hashed, so do not let an editor or a checkout
  change its line endings.
- No file may carry a username, email address, or local path. `scripts/privacy_lint.py` fails on them.

## 4. Before you push

Run each command from the repository root and read the output. Do not push on a partial run.

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

`generate_manifest.py --check` covers both manifests, `check_grammars_md.py` covers both fixture lists (and the
stress README table), and `check_fwdata.py` covers stress witnesses as well as fixture witnesses.

- `check_words_schema.py` needs PyYAML and jsonschema, and `check_dtd.py` needs lxml or `xmllint`; CI
  installs them (`pip install -r scripts/requirements.txt`). The other scripts use the standard library only.
- Then run the self-check of each consuming engine you can reach (for sillsdev/machine,
  `--fixtures <path to this clone> --include-pathological`, and `--fixtures <path to this clone>/stress` for the
  stress fixtures; its `conformance/` is a clone at its own pinned commit, so it does not see your change, and its
  tests read this clone when `HC_CONFORMANCE_SUITE=<path to this clone>` is set).
  This repository cannot run an engine; CI here proves the files are well formed, not that an engine agrees
  with them.

## 5. Stress fixtures

The grammars under `stress/edge-cases/` measure the cost of an engine's analysis pass. They are not
conformance fixtures, and this section says how they differ from sections 1 to 4.

**What stays the same.** The one rule applies: only what FieldWorks can produce, with the same evidence
(section 1) and the same meaning of `fieldworks_producible: true` (a claim read from the loader until a
`fieldworks/` witness exists, section 3). Every stress fixture carries the flag; none has a witness yet (0 of
16), and `stress/README.md` states the count.

**What differs.**

| | Conformance fixture | Stress fixture |
|---|---|---|
| Directory | `languages/<name>/` or `edge-cases/<name>/` | `stress/edge-cases/<name>/` |
| Expected output means | what the oracle engine does, read against the rules; each word pins one behaviour | parity: an optimization must return the same parses; the words are a workload, and a changed row is the failure |
| Measure | pass or fail | work steps, never wall time; `budget_ms` only guards against a hang |
| `words.yaml` starts with | front matter | `# kind: stress (...)`, then `fieldworks_producible: true` and `budget_ms` |
| `exercises`, coverage, `rules.csv`, `dead-rules-allowed.tsv` | yes | none; no ledger counts them |
| Fixture `README.md` | optional | none; `stress/README.md` describes every fixture in one table |
| Listed in | `docs/grammars.md` bullets, `generated/hc-conformance-manifest.v2.json` | the `docs/grammars.md` "Stress grammars" bullets, the `stress/README.md` table and `generated/stress-manifest.v2.json` |
| Run by | the consumer's default runner | only on request, through the consumer's opt-in stress category |

**Adding or changing a stress fixture.**

1. Check producibility as in section 1 and name the `HCLoader.cs` function that writes each construct. Say in
   the pull request whether a witness exists (it will not).
2. Write `stress/edge-cases/<name>/grammar.xml` and `words.yaml`. Start `words.yaml` with
   `# kind: stress (timing and optimization parity fixture, not conformance; see stress/README.md)`, then
   `fieldworks_producible: true` and `budget_ms`. In the header comment say what the grammar models and what it
   really exercises; do not name a script or a switch that is not in a repository.
3. Take the expected rows from an engine run, never from memory: three identical runs of the reference engine
   (sillsdev/machine `master` for the existing fixtures). Record the build in the header
   (`# oracle-provenance: ...`) and, if it is new, in [PROVENANCE.md](PROVENANCE.md). Read each row against the
   grammar. A row you cannot explain is a finding to file, not a pin. A word an engine in the field renders
   differently from `master` is left out and named in `stress/README.md` (see `polundanasak`).
4. Change an existing row only when the correct behaviour of the reference engine changed, and say which change
   (for example FLEx-style null-affix boundaries) in the pull request. An optimization that moves a row has failed;
   it is not a reason to edit the row.
5. Add a row to the table in [stress/README.md](stress/README.md): what the fixture really exercises (checked
   against the words and the grammar, not copied from the commit that added it), the word count, the no-parse
   count, and the sillsdev/machine issue or pull request by number. Never cite a local file for a machine
   record; cite the issue. Update the witness sentence if a witness was added.
6. Add a bullet to the "Stress grammars" section of [docs/grammars.md](docs/grammars.md) and keep its count sentence
   true. Update the counts in [docs/README.md](docs/README.md) (`stress/ ... 16 timing` and "The 16 timing grammars") and the numbers line of the root README.
7. Run `python3 scripts/generate_manifest.py` and read the diff. Only `generated/stress-manifest.v2.json` may
   move; if the conformance manifest moves, you changed something it hashes.
8. Delete a fixture by removing its directory, its README row and its bullet, and regenerating. Rename one only
   with the consumers in step 9: the directory name `stress/` and the fixture names are read by sillsdev/machine.
9. Tell the consumers (section 2, step 8). sillsdev/machine's stress test and runner discover the directory
   themselves; a rename or a changed row there is a bump of its pin.

`stress/README.md` shows how a consumer runs the fixtures; this repository cannot, so CI proves only that the files are
well formed, listed, and hashed.
