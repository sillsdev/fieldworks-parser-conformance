# Updating the conformance suite

This file says how to change the suite and what to run before the change leaves your machine. It applies to
this repository, which is consumed by engines (sillsdev/machine's C# HermitCrab and PanGloss) as a
submodule. Nothing here assumes any engine's build, layout or language. Commands run from the root of this
repository; `python3` is the only tool the checks need.

If this file disagrees with `.github/workflows/`, the scripts in `scripts/`, or the files you are changing,
prefer the executable behaviour and say so.

## 1. The rule

The suite covers only grammars a real FieldWorks project can produce. FieldWorks builds every grammar
through `HCLoader.cs` (`Src/LexText/ParserCore/HCLoader.cs` in the FieldWorks repository), and that loader
reaches less than the HermitCrab XML can say. A grammar that needs a construct the loader never writes does
not belong here, however expressible it is in the XML and however well an engine handles it.

- Before you author, change or keep a fixture, check each construct it uses against the table in
  [README.md](README.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it), against the census
  `fieldworks-writable-shapes.tsv` (every DTD member, with the `HCLoader.cs` line that writes it, only labels
  it, or never writes it), and against [PROTOCOL.md](PROTOCOL.md) section 9.
- The standard is the round trip: a real FieldWorks project, put through the loader, yields the grammar. Reading
  the loader source is weaker evidence. `fieldworks_producible: true` is a claim read from the loader until the
  fixture has a FieldWorks witness (section 3), and only the 9 fixtures that carry one are certified today (of
  133). Say which of the two you are relying on in the pull request.
- If the grammar needs a construct in that table, stop. Rewrite the grammar without it or do not add it.
  Do not relax `fieldworks_producible`: every fixture must carry `true`, and `scripts/check_words_schema.py`
  and the consuming engines' gates fail on anything else.
- A new construct goes into `fieldworks-writable-shapes.tsv`, with its loader line, before a fixture may use it.

## 2. Adding, changing or deleting a fixture

A fixture is a directory under `languages/` or `edge-cases/` holding `grammar.xml` and `words.yaml`, and
optionally a `README.md` and a `fieldworks/` witness. [docs/what-it-is.md](docs/what-it-is.md) and the README
section "Consuming the suite from another repository" describe the files; `schema/words.schema.json` and
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
5. If you ruled a construct out, add a row to the README section named in section 1 and, when the loader
   verdict changed, update `fieldworks-writable-shapes.tsv`. Cite the `HCLoader.cs` function and line, and
   the FieldWorks commit you read. If you delete a fixture for this reason, add its row to the table in
   [docs/engine-only-fixture-retirement.md](docs/engine-only-fixture-retirement.md).
6. Regenerate the manifest (section 2a), then read the `git diff`. The manifest should move only for the
   fixtures you touched.
7. Delete a fixture by removing its directory and its line in `docs/grammars.md`, then regenerating. Remove a
   `dead-rules-allowed.tsv` line that names it.
8. Tell the consuming engines. sillsdev/machine pins a commit of `main` in its submodule, so a change reaches
   it when it bumps the pin; PanGloss follows `main`, so it sees a change once the commit is on `main`. Their
   own self-check and ledgers are regenerated on their side, not here.

### 2a. Generated files

| File | Written by | Checked by |
|---|---|---|
| `generated/hc-conformance-manifest.v2.json` | `python3 scripts/generate_manifest.py` | `python3 scripts/generate_manifest.py --check`, and CI |
| `coverage.csv`, `rules.csv` | the consuming engine's coverage report (sillsdev/machine's runner: `--coverage-report`) | that engine's CI; **not yet checked here** |

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

- `check_words_schema.py` needs PyYAML and jsonschema, and `check_dtd.py` needs lxml or `xmllint`; CI
  installs them (`pip install -r scripts/requirements.txt`). The other scripts use the standard library only.
- Then run the self-check of each consuming engine you can reach (for sillsdev/machine,
  `--fixtures conformance --include-pathological`, and `--fixtures conformance/stress` for the stress fixtures).
  This repository cannot run an engine; CI here proves the files are well formed, not that an engine agrees
  with them.
