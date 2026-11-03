# Consuming the suite from another repository

This repository contains no engine. This page says who uses the suite and how they pin it, what passing
means, and which files a consumer reads.

## Who uses it and how it is pinned

**Who uses it.** This repository contains no engine. sillsdev/machine (the C# HermitCrab) and PanGloss each
name a commit of `main` in a file called `conformance.commit` and clone this repository at that commit into an
ignored `conformance/` directory; neither uses a submodule, and `HC_CONFORMANCE_SUITE` names a local copy
instead. Both run it through their own runners. Their gates, ledgers and
coverage measurements live in their own repositories. To change the
suite, read [AGENTS.md](../AGENTS.md). Where a fixture or document names a ledger, a test or a source path
of one of those repositories, it is a historical or cross-repository reference, not a file here.
The commit hashes cited in fixtures are plain text, explained in [PROVENANCE.md](../PROVENANCE.md).

## What passing means today

**What passing means today.** An engine reproduces the reference implementation's observable parse
behaviour — signature, status, pinned crash — on every fixture its declared capability profile
admits.

How complete the fixture set is, as measured per DTD surface, is tracked by the consuming engines, not here.

## Reading the suite

`words.yaml` is the single canonical authored format — the only place case data (inputs, parses,
rejections, skips, `neutralizes`) lives. There is no generated JSON restatement of it: an earlier
`hc-conformance-corpus/v1` product duplicated that ground truth into a 409KB file, and it carried
less than the 383KB of authored `words.yaml`/`grammar.xml` sources it was generated from, because
those sources hold 1011 comment lines of reasoning — why a fixture exists, what it pins — that JSON
cannot express. Two representations of the same ground truth also meant a permanent drift gate. It
has been deleted, along with `schema/conformance-corpus.schema.json`.

What that product genuinely contributed was provenance, not case data, so that is what survives as
`generated/hc-conformance-manifest.v2.json` (`hc-conformance-manifest/v2`, `schema/conformance-manifest.schema.json`): one entry per fixture carrying `fixtureId`, `category`, `displayLanguage`, `grammarPath`,
`grammarSha256`, `wordsPath`, `wordsSha256`, `caseCount`, and `expectedCrash`, plus top-level
`dtdPath`, `dtdSha256`, `sourceHash`, and the three format-version identifiers
(`hc-conformance-manifest/v2`, `hc-conformance-words/v1`, `sil-machine-hermit-crab-input-xml/v1`).
A consumer reads the manifest to discover fixtures and verify integrity, then reads `grammar.xml`
and `words.yaml` directly for the actual grammar and cases. Paths inside the manifest are
relative to the root of this repository, with no leading directory name (`edge-cases/<name>/grammar.xml`),
never relative to the manifest itself. A consumer that clones this repository into `conformance/` prepends
that itself. Version 2 dropped the `conformance/` prefix that version 1 carried.

Regenerate with `python3 scripts/generate_manifest.py`; `python3 scripts/generate_manifest.py --check` verifies
the checked-in bytes and exits nonzero on drift. CI also validates every grammar against the DTD and every
`words.yaml` against `schema/words.schema.json`.

The DTD is published at `HermitCrabInput.dtd` and is the authoritative copy; sillsdev/machine keeps an
embedded copy that a test of its own holds byte-identical. When resolving a grammar's DOCTYPE, admit only the
system identifier `HermitCrabInput.dtd` and map it to the published DTD path the manifest records. Any other
external entity, network fetch, or filesystem fallback should be refused rather than attempted.

Two files are required per fixture: `grammar.xml` and `words.yaml`. An optional `README.md`
preserves the fixture's rationale and oracle history; optional FieldWorks witnesses are described
in the protocol. `words.yaml` is the single ground truth: front matter (`language`,
`inspired_by`, `sources`, `requires`) plus one entry per word, each carrying a `note` and either
`parses` (`signature`/`gloss`/`rules`/`exercises`, one per distinct analysis), `expect_fail` +
`blocked_by` (well-formed input, zero valid analyses), or `expect_skip` (the oracle throws
`InvalidShapeException`, e.g. an undeclared segment — status "SKIPPED", not "ok"). Optional fields:
`provenance` (bug/PR reference), `guess` (a `LexicalGuess` parse),
`budget_ms`/`expect_crash` (edge-cases only). Signature comparison treats the members of each bracketed
class `[...]` as a set (`|b[ae]t` equals `|b[ea]t`; PROTOCOL.md section 4, sillsdev/machine#573).
Signatures are authored-and-verified, never blindly
regenerated: a consuming engine's self-check fails on a mismatch, and a proposed patch is for a human to accept. Full schema: `schema/words.schema.json`.

Fixture and case totals are summed from `generated/hc-conformance-manifest.v2.json`, not hand-copied:
two prose totals have already drifted from the manifest twice. The numbers line of the root README is
checked against the disk by `scripts/check_grammars_md.py`, and `python3 scripts/generate_manifest.py --check`
verifies the manifest's per-fixture `caseCount`.
