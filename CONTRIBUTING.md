# Contributing

[AGENTS.md](AGENTS.md) holds the mechanics: how to add, change or delete a fixture, which files are generated,
and what to run before you push. This page holds the policy and the commands.

## Growth policy: every bug fix lands with a conformance addition

> **Every bug fix in a conforming engine lands together with a conformance addition** — a new word,
> a new grammar, or a new edge-case.

The cheap path, in order of preference:

1. **Add a word.** One `words.yaml` entry (word + `note` + `parses` + `provenance`) in the language
   whose grammar already covers the territory. No grammar changes.
2. **Extend a grammar** when no existing language's grammar can express the trigger but the
   phenomenon is typologically plausible for one of the six (e.g. a new evidential-chain
   interaction belongs in `suffixing-evidential-adjacency-chain`).
3. **Add an edge-case** when the pin is too specific to embed naturalistically (an XML-loader quirk, a
   crash, an unusual rule shape). It must still be a grammar FieldWorks can produce; a pin that needs
   a construct in [the section on what FieldWorks cannot produce](docs/fieldworks-cannot-say.md#what-the-xml-can-say-but-fieldworks-cannot-so-we-do-not-test-it)
   belongs outside this suite.
4. **Add a new `languages/` member** only for genuinely new typological territory not covered by any
   of the six, not for an incremental variant of one that already exists.

Then follow [AGENTS.md](AGENTS.md).

## Run the checks

From the repository root, with `python -m pip install -r scripts/requirements.txt` done once:

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

CI runs the same scripts (`.github/workflows/checks.yml`). Do not push on a partial run.
