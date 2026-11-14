# The FieldWorks parser conformance suite

**One suite of grammars, words and expected parses, so every FieldWorks parser engine can prove it gives the same answers.**
A linguist's project should parse a word the same way whichever engine runs it. This suite checks that it does.

**139 conformance grammars** (6 languages, 133 edge cases) · **16 stress grammars** · **11 FieldWorks witnesses**

## The one rule

A grammar is here only if a real FieldWorks project can produce it. FieldWorks writes less than the grammar format can say,
so anything it cannot write stays out. [What FieldWorks cannot say](docs/fieldworks-cannot-say.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it), construct by construct.

## The grammars

- **Hermit Crab**: rule-based and item-and-process. Morphological and phonological rules applied in order, with a C# engine in sillsdev/machine. This suite is written in its format (`grammar.xml`, `HermitCrabInput.dtd`). It needs a complete phonology: every letter of every form and word defined as a segment.
- **XAmple**: FieldWorks' other parser, in the AMPLE family, and a different algorithm (item-and-arrangement). It works on letters and ignores phonological features and rules, so any grammar with neither is in the XAmple subset.

A FieldWorks project switches between the two with one setting (`ActiveParser`).

### Which grammars each engine runs

| Engine | Phonology it needs | Grammars |
|---|---|---|
| XAmple | None: letters only; it ignores features and rules | 47 conformance + 6 stress, the [XAmple subset](docs/grammars.md#the-xample-subset) |
| Hermit Crab (machine) | Complete: every letter defined as a segment | all 139 + 16 |
| PanGloss | None, incomplete or complete | all 139 + 16 |

The suite has no grammar with incomplete phonology yet.

## Three projects, one suite

| Project | What it is | What it gets from the suite |
|---|---|---|
| [FieldWorks](https://github.com/sillsdev/FieldWorks) ([software.sil.org/fieldworks](https://software.sil.org/fieldworks/)) | The linguists' desktop app. It stores the grammar and runs either parser. | It does not run the suite; it sets the boundary. Every fixture must be something it can write, and witnesses are real `.fwdata` projects built from fixtures. |
| [machine](https://github.com/sillsdev/machine) | The C# Hermit Crab engine, and the reference that produced the expected parses. | `hc-conformance` runs the whole suite in machine's CI. |
| [PanGloss](https://github.com/sillsdev/PanGloss) | A Rust parser ported from Hermit Crab. | It runs the same fixtures through its own runner and must match. |

**And XAmple?** The suite has no XAmple expected answers, so it does not test XAmple. XAmple runs on the [subset](docs/grammars.md#the-xample-subset).
PanGloss's `xample-projector` turns a FieldWorks witness into both Hermit Crab and XAmple input and drives the real XAmple engine. That is how the two are compared today.

## Try it

```
git clone https://github.com/sillsdev/fieldworks-parser-conformance
cd fieldworks-parser-conformance
python -m pip install -r scripts/requirements.txt
python scripts/generate_manifest.py --check
python scripts/check_grammars_md.py
```

An engine consumes the suite by pinning a commit in `conformance.commit` and cloning it into an ignored `conformance/`.
Set `HC_CONFORMANCE_SUITE=<path>` to use a local copy. Details: [docs/consuming.md](docs/consuming.md).

## Where next

| If you want to | Go to |
|---|---|
| Learn the fixture format | [docs/what-it-is.md](docs/what-it-is.md) |
| Browse the grammars | [docs/grammars.md](docs/grammars.md) |
| Write an engine adapter | [PROTOCOL.md](PROTOCOL.md) |
| Consume the suite | [docs/consuming.md](docs/consuming.md) |
| Contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Time an engine | [stress/README.md](stress/README.md) |
| Look up a term | [docs/glossary.md](docs/glossary.md) |
| See what FieldWorks cannot say | [docs/fieldworks-cannot-say.md](docs/fieldworks-cannot-say.md) |
| Trace where results came from | [PROVENANCE.md](PROVENANCE.md) |
| Find every document | [docs/README.md](docs/README.md) |

## License

MIT. See [LICENSE](LICENSE).
