# Known engine divergences

The suite's expected answers are the founding oracle's: the C# HermitCrab in sillsdev/machine (hc.dll). See
[PROVENANCE.md](../PROVENANCE.md) and [PROTOCOL.md](../PROTOCOL.md). A fixture here passes when an engine
gives hc.dll's answer. Three fixtures are kept on purpose even though one engine, PanGloss, knowingly gives a
different answer for them. This page says which, why, and where the engine side of the decision lives.

## Why PanGloss diverges

PanGloss covers the whole range of HermitCrab grammars: featureless (XAmple-style) grammars, fully featured ones,
and everything between, where a phoneme gains features one at a time. Where hc.dll's behaviour comes only from a
feature the grammar has not defined yet, PanGloss keeps the generous behaviour and records it as a true divergence,
not a bug to fix. The decision is
[PanGloss ADR 0009](https://github.com/sillsdev/pangloss/blob/main/docs/adr/0009-partial-feature-grammars.md).
Neither engine is wrong here, and the suite's ground truth stays hc.dll's answer.

## The fixtures

| Fixture | PanGloss ledger entry | hc.dll (the suite's expectation) | PanGloss |
|---|---|---|---|
| `edge-cases/featureless-modify-from-input` | [128](https://github.com/sillsdev/pangloss/blob/main/docs/divergences/128-featureless-modify-from-input-keeps-every-root.md) | `kitas` = KITA only; `tisis`, `pisas`, `kakas`, `tata` have no parse | `kitas` = KITA and KATA; `tisis` = TASI+MODS; `pisas` = PASA+MODS |
| `edge-cases/unspecified-feature-minus-environment` | [129](https://github.com/sillsdev/pangloss/blob/main/docs/divergences/129-unspecified-feature-satisfies-minus-pin.md) | `Nata` parses (`NPFX+ATA\|N+?a[pt]a`); `mata` has no parse | `mata` parses (`NPFX+ATA\|m+?a[pt]a`); `Nata` has no parse |
| `edge-cases/unspecified-feature-minus-target` | [129](https://github.com/sillsdev/pangloss/blob/main/docs/divergences/129-unspecified-feature-satisfies-minus-pin.md) | `aa` = `ATA\|aa`; `a` = `PA\|a` | `aa` and `a` have no parse (the unspecified `a` is deleted too) |

- **Featureless `ModifyFromInput`.** hc.dll undoes a modification by adding the context's anti-feature structure
  to the node. In a grammar with no feature system, a segment is identified by its spelling alone, and that
  spelling is restricted to the new class, so a root whose vowel differs cannot be recovered. PanGloss recovers
  every root, as it does in a grammar with a feature system.
- **Unspecified feature against a `[feature:-]` pin.** hc.dll's synthesis rules match by subsumption, so a segment
  with no value for the feature does not satisfy the pin. PanGloss treats the missing value as compatible, so a
  grammar can add features to its phonemes gradually and keep working.

All three are `fieldworks_producible: true`, and none has a `fieldworks/` witness.

## How a divergence is marked

The expected rows in each `words.yaml` are hc.dll's, unchanged, with `# oracle-provenance: founding-oracle`. The
header also carries one fixed line, which a tool can read with a grep:

```
# known-engine-divergence: pangloss ledger=<entry> words=<comma-separated words>
```

`words` names the words on which the engines disagree. The line is a comment, because `words.yaml` front matter is a
closed vocabulary that machine's loader rejects on an unknown key, and the manifest has no per-engine field.
It changes no result and waives nothing here.

The waiver lives on the engine side. PanGloss lists the three fixture ids in its own known-divergence tooling
(`rust/tools/known-conformance-divergences.txt`), and a fixture id alone never waives a failure there: the reason
must match too. Any other engine that passes these fixtures needs no entry.

Do not copy PanGloss's `words.yaml` for these fixtures into the suite. Its rows record PanGloss's answers, and the
suite records the oracle's.
