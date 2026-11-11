# The conformance suite: documentation

These documents ship **with** the fixtures. That is deliberate: a consumer receives this repository and
nothing else (sillsdev/machine and PanGloss clone it at a pinned commit), so anything explaining the suite that
lives outside it may as well not exist.

The one rule: the suite holds only what a real FieldWorks project can produce. The rule, and the constructs left out, are in
[what FieldWorks cannot say](fieldworks-cannot-say.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it).

## By reader

### New here

| | |
|---|---|
| [../README.md](../README.md) | the front page: what the suite is, the three projects, a quick start |
| [what-it-is.md](what-it-is.md) | the suite, the fixture contract, the two-file format |
| [glossary.md](glossary.md) | one line for each term the suite uses |
| [grammars.md](grammars.md) | every grammar in the suite, one line each, grouped by area, and which engines run which |

### Implementing an engine

You need **`PROTOCOL.md` and nothing else here.** Your entire obligation is to produce the same
parses for each fixture's `grammar.xml` and words. If you do, you inherit whatever this suite covers.

| | |
|---|---|
| [PROTOCOL.md](../PROTOCOL.md) | the adapter contract an engine must implement |
| [rule-order.md](rule-order.md) | the rule-order contract, strata and the engine cascade |

The measurements that justify calling the fixture set complete (counterfactual census, interface inventory,
severance sweep, interaction chains, data-flow obligations) were computed by running sillsdev/machine's
HermitCrab engine (sillsdev/machine#480). They are not part of this repository, and you are never measured
against them.

### Consuming the suite

| | |
|---|---|
| [consuming.md](consuming.md) | who uses the suite, how they pin it, what passing means, and the manifest and fixture files |
| [grammars.md](grammars.md) | the six-language table and every fixture, and the XAmple subset |
| [../stress/README.md](../stress/README.md) | the 16 stress grammars and what their expected output means |

### Contributing

Read [AGENTS.md](../AGENTS.md). The one rule is the first thing in it: add only what FieldWorks can produce.

| | |
|---|---|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | the growth policy and how to run the checks |
| [AGENTS.md](../AGENTS.md) | how to add, change or delete a fixture, and what to run before you push |
| [truncation-companions.md](truncation-companions.md) | the three truncation edge cases derived from one grammar |

Rationale documents for individual fixture groups: [final-template-partial-discriminators.md](final-template-partial-discriminators.md),
[final-template-partial-root.md](final-template-partial-root.md),
[shared-template-unconstrained-suffix.md](shared-template-unconstrained-suffix.md),
[template-category-sharing.md](template-category-sharing.md),
[irregular-variant-overgeneration.md](irregular-variant-overgeneration.md) and
[parser-settings-variants.md](parser-settings-variants.md).

### Auditing

| | |
|---|---|
| [fieldworks-cannot-say.md](fieldworks-cannot-say.md) | the rule, the round-trip standard, and the 27-row table of what FieldWorks cannot say |
| [engine-only-fixture-retirement.md](engine-only-fixture-retirement.md) | the 23 fixtures still removed for needing a construct FieldWorks cannot produce (four more were restored), and which construct |
| [PROVENANCE.md](../PROVENANCE.md) | which engine builds produced the checked-in ground truth, as plain-text commit hashes |

`.fwdata` witnesses and XAMPLE comparison are produced and run by
[PanGloss](https://github.com/sillsdev/PanGloss)'s `xample-projector` tool, which stays in PanGloss; this
repo stores the witnesses but never executes them.

## Directory map

```
languages/<name>/    grammar.xml + words.yaml   -- 6 typologically-selected synthetic languages
edge-cases/<name>/   grammar.xml + words.yaml   -- 131 focused micro-grammars for things no shared grammar hosts
stress/              16 timing and optimisation-parity grammars (not conformance; see stress/README.md)
                     docs/grammars.md and that README list each; generated/stress-manifest.v2.json hashes them
docs/grammars.md     one line for every fixture above; scripts/check_grammars_md.py keeps it complete
coverage.csv         language x word x construct (written by a consuming engine's coverage report)
rules.csv            language x grammar rule id x exercising words (same)
dead-rules-allowed.tsv  rules a fixture declares on purpose that no word exercises, with the reason
constructs.txt       the checklist vocabulary of construct tags that `exercises:` values are drawn from
fieldworks-writable-shapes.tsv  the census of which DTD members HCLoader.cs writes (see below)
HermitCrabInput.dtd  the published grammar DTD (the authoritative copy)
schema/              Draft 2020-12 contracts for the authoring and product formats
generated/           the versioned JSON manifest a consumer imports, and the stress manifest (scripts/generate_manifest.py)
parity-check.py      the engine-free migration parity proof
scripts/             the checks CI runs
PROTOCOL.md          the adapter contract
PROVENANCE.md        which engine builds supplied the ground truth
AGENTS.md            how to change the suite
CONTRIBUTING.md      the growth policy and how to run the checks
```

The 16 timing grammars in `stress/` are listed in that directory's README and in `docs/grammars.md`. The manifest above does not
count them; `generated/stress-manifest.v2.json` does, in the same layout, and `scripts/generate_manifest.py --check` checks both.
None of the 16 has a FieldWorks witness yet; the rule and the expected-output meaning are in `stress/README.md`.
