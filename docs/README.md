# The conformance suite: documentation

These documents ship **with** the fixtures. That is deliberate: a consumer receives this repository and
nothing else (sillsdev/machine and PanGloss mount it as a submodule), so anything explaining the suite that
lives outside it may as well not exist.

The suite covers only grammars a real FieldWorks project can produce. A grammar FieldWorks cannot
produce does not belong, however expressible it is in the XML. The constructs left out and the reason
for each are in the README section
[what the XML can say but FieldWorks cannot, so we do not test it](../README.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it).

Read in this order.

| | |
|---|---|
| [what-it-is.md](what-it-is.md) | the suite, the fixture contract, the two-file format |
| [grammars.md](grammars.md) | every grammar in the suite, one line each, grouped by area |
| [engine-only-fixture-retirement.md](engine-only-fixture-retirement.md) | the 23 fixtures still removed for needing a construct FieldWorks cannot produce (four more were restored), and which construct |
| [PROTOCOL.md](../PROTOCOL.md) | the adapter contract an engine must implement |
| [AGENTS.md](../AGENTS.md) | how to add, change or delete a fixture, and what to run before you push |
| [PROVENANCE.md](../PROVENANCE.md) | which engine builds produced the checked-in ground truth, as plain-text commit hashes |

Rationale documents for individual fixture groups: [final-template-partial-discriminators.md](final-template-partial-discriminators.md),
[final-template-partial-root.md](final-template-partial-root.md),
[shared-template-unconstrained-suffix.md](shared-template-unconstrained-suffix.md),
[template-category-sharing.md](template-category-sharing.md),
[irregular-variant-overgeneration.md](irregular-variant-overgeneration.md) and
[parser-settings-variants.md](parser-settings-variants.md).

`.fwdata` witnesses and XAMPLE comparison are produced and run by
[PanGloss](https://github.com/sillsdev/PanGloss)'s `xample-projector` tool, which stays in PanGloss; this
repo stores the witnesses but never executes them.

## If you are implementing an engine

You need **`PROTOCOL.md` and nothing else here.** Your entire obligation is to produce the same
parses for each fixture's `grammar.xml` and words. If you do, you inherit whatever this suite covers.

The measurements that justify calling the fixture set complete (counterfactual census, interface inventory,
severance sweep, interaction chains, data-flow obligations) are kept by sillsdev/machine, because they are
computed by running its HermitCrab engine. They are not part of this repository, and you are never measured
against them.

## If you are extending the suite

Read [AGENTS.md](../AGENTS.md). The one rule is the first thing in it: add only what FieldWorks can produce.
