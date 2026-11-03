# Glossary

One line for each term the suite uses. Each is defined from what this repository says; the source is named.

- **fixture**: a directory under `languages/` or `edge-cases/` holding `grammar.xml` and `words.yaml`, and optionally a `README.md` and a `fieldworks/` witness ([AGENTS.md](../AGENTS.md) section 2).
- **grammar**: a fixture's `grammar.xml`, a `HermitCrabInput` XML document validated against `HermitCrabInput.dtd` ([what-it-is.md](what-it-is.md)).
- **witness**: a fixture's `fieldworks/` directory (`project.fwdata`, `phonology-mutations.yaml`, `WritingSystemStore/`), a real FieldWorks project backed out of its `grammar.xml` ([PROTOCOL.md](../PROTOCOL.md) section 10).
- **FieldWorks-producible**: a real FieldWorks project can produce the grammar through `HCLoader.cs`; every fixture records it as `fieldworks_producible: true`, a claim read from the loader until a witness certifies it ([fieldworks-cannot-say.md](fieldworks-cannot-say.md)).
- **signature**: the morpheme IDs of one parse in morph order joined by `+`, then `|` and the surface shape; a word's signatures are sorted and joined with `;`, and no parse is `-` ([PROTOCOL.md](../PROTOCOL.md) section 3).
- **reference engine**: the C# HermitCrab in sillsdev/machine, whose observable parse behaviour a passing engine reproduces ([consuming.md](consuming.md)).
- **oracle**: the engine whose output supplied the expected parses; the founding oracle is that same C# HermitCrab ([PROTOCOL.md](../PROTOCOL.md), [PROVENANCE.md](../PROVENANCE.md)).
- **adapter**: an executable `<engine-binary> batch <grammar> <words.txt> <output.tsv>` that runs an engine over a word list and writes a TSV ([PROTOCOL.md](../PROTOCOL.md) section 1).
- **capability profile**: the set of capabilities an engine declares (for example `phonology`); a fixture whose `requires` is not covered is skipped for that engine ([PROTOCOL.md](../PROTOCOL.md) section 5).
- **stress fixture**: a grammar under `stress/` for timing and optimisation-parity work on the analysis pass; not a conformance fixture ([stress/README.md](../stress/README.md)).
- **manifest**: a generated JSON file listing each fixture with its paths, SHA-256 hashes and case count: `generated/hc-conformance-manifest.v2.json`, and `generated/stress-manifest.v2.json` for the stress grammars ([consuming.md](consuming.md)).
- **ledger**: a consuming engine's own record of what its fixtures cover (coverage cells, gate obligations); it lives in that engine's repository, not here ([consuming.md](consuming.md)).
- **`requires`**: the `words.yaml` front-matter array naming the capabilities a fixture needs (`phonology`, `morpher-settings`); empty means pure morphotactics, runnable by any engine ([PROTOCOL.md](../PROTOCOL.md) section 5).
