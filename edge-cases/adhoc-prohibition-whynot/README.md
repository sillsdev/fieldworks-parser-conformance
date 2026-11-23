# adhoc-prohibition-whynot

Synthetic. One ad hoc allomorph prohibition on a prefix: the prefix ta- (`subTa`) excludes the stem allomorph `aDa`, the plainest form `HCLoader.LoadAllomorphCoOccurrenceRules` writes (HCLoader.cs:2163-2189). The fixture carries the suite's first why-not row.

## What it pins

- `da`: parses. `taga`: parses (ga has no prohibition).
- `tada`: no analysis; the only derivation TA+DA is excluded by the prohibition.
- `whynot.yaml`, row for `tada`: asked for TA+DA, the first failure is `adhoc_prohibition` / `AllomorphCoOccurrenceRules`, naming `subTa` and then `aDa`. Format: [PROTOCOL.md](../../PROTOCOL.md) section 11.

## Status

The parse rows come from the reference engine: hc-conformance self-check at Machine `e63b8863` passes (`words.yaml` header). The why-not row is `status: pending`, pending runner support: no engine can produce a why-not result yet, so it was written from the grammar and the loader, not from an engine run, and nothing compares it. It becomes `asserted` once the reference engine's why-not output has been read against the grammar.

## FieldWorks witness

None. `fieldworks_producible: true` is a claim read from `HCLoader.cs`, not a round trip.
