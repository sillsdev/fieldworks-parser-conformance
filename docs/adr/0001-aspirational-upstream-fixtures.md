# Fixtures may be aspirational for upstream Machine and FieldWorks

Status: accepted (owner, 2026-11-25); amended by [ADR 0007](0007-exceptions-live-in-status-yaml.md)

Amended 2026-11-27: exceptions move from the `upstream` field to `status.yaml` once epic S1 lands; see [ADR 0007](0007-exceptions-live-in-status-yaml.md).

## Context

This suite is aspirational for sillsdev/machine (HermitCrab) and FieldWorks (`HCLoader.cs`): it
states what they should do, and sometimes they cannot yet. The
[engine-only retirement rule](../engine-only-fixture-retirement.md) keeps only grammars FieldWorks can
produce today, so a capability that needs a FieldWorks or Machine change could not be tested until that change
merged. Merges are slow and the suite is what motivates them.

## Decision

A conformance grammar may be committed once an issue or pull request exists against Machine or
FieldWorks for the capability it needs. It does not wait for the upstream merge. Expected rows still
come only from a real C# run, never from PanGloss output alone.

Precedents: `edge-cases/affix-multiple-application` (FieldWorks PR #1263 at `0ead571c`, unmerged, makes
affix `maxApps` writable); the oracle builds at the tip of unmerged machine PR #615 (`e63b8863`).

## Consequences

- **Refines the retirement rule.** A construct `HCLoader.cs` cannot write today is producible
  "aspirationally" once a FieldWorks issue or PR exists to make it writable. Its row in
  `fieldworks-writable-shapes.tsv` and `fieldworks-cannot-say.md` cites that issue or PR.
- **Before landing.** The upstream issue or PR is filed. The C# rows come from a real run; if the C#
  engine lacks the capability, they come from a build of the Machine PR, and the build SHA is recorded.
- **Citation.** The `words.yaml` oracle header and `PROVENANCE.md` name the issue or PR (and the SHA for a PR).
- **Re-point on merge.** When the upstream change merges, update those citations to the merged commit or
  release, and the table rows with them.
- **If upstream rejects it.** The fixture is retired under the retirement doc: converted to a
  producible grammar if that keeps its purpose, otherwise deleted.
- **Machine-readable.** The dependency is recorded in the `upstream` field of `words.yaml` ([PROTOCOL.md](../../PROTOCOL.md) section 12); `scripts/upstream_status.py` reports when it merges or closes.
