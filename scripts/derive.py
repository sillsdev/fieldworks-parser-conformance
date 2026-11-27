"""Everything derived from the authored files: the two manifests, coverage.csv and rules.csv (ADR 0009).

None of it is committed. `python3 scripts/suite.py generate` writes a consumer's copy; the checks call the builders
here directly. coverage.csv and rules.csv are byte-for-byte what sillsdev/machine's `hc-conformance --coverage-report`
writes, so a consumer may use either. Standard library plus PyYAML.
"""
import csv
import hashlib
import io
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from suite import FIXTURE_GROUPS, LABEL_SEP, vocabulary, word_labels, ROOT, STRESS_GROUP, expand_words, fixture_dirs, fixture_id, load_words, sha256_text, words_summary

FORMAT = "hc-conformance-manifest/v2"
WORDS_FORMAT = "hc-conformance-words/v1"
GRAMMAR_FORMAT = "sil-machine-hermit-crab-input-xml/v1"
DTD = "HermitCrabInput.dtd"
MANIFEST = "hc-conformance-manifest.v2.json"
STRESS_FORMAT = "hc-conformance-stress-manifest/v2"
STRESS_MANIFEST = "stress-manifest.v2.json"
CORE_TIER = "core-tier.txt"  # the test cases a consumer runs on every pull request (scripts/tiers.py)
ADDITIONAL_SOURCE_FILES = (
    "constructs.txt",
    "parity-check.py",
    "schema/words.schema.json",
    "schema/conformance-manifest.schema.json",
)


def manifest(root: Path = ROOT, fmt: str = FORMAT, prefix: str = "", dtd: str = DTD,
             groups=FIXTURE_GROUPS, sources=ADDITIONAL_SOURCE_FILES) -> dict:
    """The manifest records paths and hashes only. Hashes are SHA-256 of UTF-8 text, BOM stripped, line ends LF."""
    dtd_path = prefix + dtd
    dtd_hash = sha256_text(root / dtd)
    fixtures = []
    for directory in fixture_dirs(root, groups):
        fid = fixture_id(directory, root)
        language, cases, crash = words_summary(directory / "words.yaml")
        if crash and cases != 1:
            raise SystemExit(f"{fid}: expect_crash test cases must hold exactly one word, found {cases}")
        fixtures.append({
            "caseCount": cases,
            "category": "stress" if fid.startswith("stress/") else "language" if fid.startswith("languages/") else "edge-case",
            "displayLanguage": language,
            "expectedCrash": crash,
            "fixtureId": fid,
            "grammarPath": f"{prefix}{fid}/grammar.xml",
            "grammarSha256": sha256_text(directory / "grammar.xml"),
            "wordsPath": f"{prefix}{fid}/words.yaml",
            "wordsSha256": sha256_text(directory / "words.yaml"),
        })
    fixtures.sort(key=lambda f: f["fixtureId"].encode("utf-8"))
    text = [fmt, "\n", dtd_path, "\0", dtd_hash, "\n"]
    for f in fixtures:
        text += [f["fixtureId"], "\0", f["grammarSha256"], "\0", f["wordsSha256"], "\n"]
    for relative in sorted(sources):
        path = root / relative
        text += [prefix + relative, "\0", sha256_text(path) if path.is_file() else "<absent>", "\n"]
    return {
        "dtdPath": dtd_path,
        "dtdSha256": dtd_hash,
        "fixtures": fixtures,
        "formatVersion": fmt,
        "grammarFormatVersion": GRAMMAR_FORMAT,
        "sourceHash": hashlib.sha256("".join(text).encode("utf-8")).hexdigest(),
        "wordsAuthoringFormatVersion": WORDS_FORMAT,
    }


def stress_manifest(root: Path = ROOT) -> dict:
    return manifest(root, fmt=STRESS_FORMAT, groups=(STRESS_GROUP,), sources=("schema/words.schema.json",))


def serialize(value: dict) -> bytes:
    return (json.dumps(value, separators=(",", ":"), sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


# A rule-bearing element's id, and what names it at runtime: see GrammarRuleIndex in sillsdev/machine.
RULE_ELEMENTS = {"MorphologicalRule", "RealizationalRule", "CompoundingRule", "PhonologicalRule", "MetathesisRule"}
CO_OCCURRENCE = {"MorphemeCoOccurrenceRule": "primaryMorpheme", "AllomorphCoOccurrenceRule": "primaryAllomorph"}


def rule_ids(grammar: Path) -> list:
    """Every rule id the grammar declares, in document order (with the co-occurrence pseudo-ids)."""
    ids = []
    for el in ET.parse(grammar).getroot().iter():
        if el.tag in RULE_ELEMENTS:
            if el.get("id") is not None:
                ids.append(el.get("id"))
        elif el.tag in CO_OCCURRENCE:
            primary = el.get("primaryMorpheme") if el.tag == "MorphemeCoOccurrenceRule" else None
            primary = primary if primary is not None else el.get("primaryAllomorph")
            if primary is not None:
                ids.append(primary)
    return ids


def coverage(root: Path = ROOT, per_fixture: bool = False):
    """(coverage rows, rule rows): what `hc-conformance --coverage-report` writes, as lists of string tuples.
    With per_fixture each rule row is led by its test case's id (a language name can be shared by several)."""
    cover, rules = [], []
    for d in sorted(fixture_dirs(root), key=lambda d: fixture_id(d, root).encode("utf-8")):
        data = load_words(d / "words.yaml")
        language = data["language"]
        exercising = defaultdict(list)
        for case in expand_words(data):
            tags = case.get("exercises") or []
            if case.get("expect_fail") or case.get("expect_skip"):
                for construct in tags:
                    cover.append((language, case["word"], "", construct))
                for rule in case.get("blocked_by") or []:
                    exercising[rule].append("!" + case["word"])
            else:
                for parse in case.get("parses") or []:
                    for construct in dict.fromkeys((parse.get("exercises") or []) + tags):
                        cover.append((language, case["word"], parse["signature"], construct))
                    for rule in parse.get("rules") or []:
                        exercising[rule].append(case["word"])
        for rule in sorted(dict.fromkeys(rule_ids(d / "grammar.xml"))):
            row = (language, rule, ";".join(dict.fromkeys(exercising.get(rule, []))))
            rules.append((fixture_id(d, root),) + row if per_fixture else row)
    return cover, rules


def label_table(root: Path = ROOT) -> list:
    """The label-to-words table as (label, test case, word, words, source) rows, sorted by label then test case. A label's
    ancestors are credited too, so a construct lists every word carrying one of its children. A listed word is one row
    (source `listed`, words 1); a generated no-parse rule is one row named `generated_no_parse[i]` (source `generated`)
    whose `words` is the number of words it spans, so generated words never pass for listed ones."""
    from suite import generated_space_size

    found = defaultdict(list)
    for d in fixture_dirs(root):
        data = load_words(d / "words.yaml")
        fid = fixture_id(d, root)
        entries = [(word["word"], 1, "listed", word_labels(word)) for word in data["words"]]
        entries += [(f"generated_no_parse[{i}]", generated_space_size(rule), "generated", list(rule.get("exercises") or []))
                    for i, rule in enumerate(data.get("generated_no_parse") or [])]
        for name, count, source, labels in entries:
            credited = set()
            for label in labels:
                parts = label.split(LABEL_SEP)
                credited.update(LABEL_SEP.join(parts[:n]) for n in range(1, len(parts) + 1))
            for label in credited:
                found[label].append((fid, name, count, source))
    order = {label: i for i, label in enumerate(vocabulary(root))}
    return [(label, fid, name, count, source) for label in sorted(found, key=lambda l: (order.get(l, len(order)), l))
            for fid, name, count, source in found[label]]


def print_labels(label=None) -> int:
    """With no argument: one line per label, with its test case, listed word and generated word counts. With one: the
    words carrying it."""
    table = label_table()
    if label is None:
        summary = defaultdict(lambda: [set(), 0, 0])
        for lab, fid, _, count, source in table:
            summary[lab][0].add(fid)
            summary[lab][1 if source == "listed" else 2] += count
        for lab, (cases, listed, generated) in summary.items():
            print(f"{len(cases):4} test cases {listed:6} listed words {generated:7} generated words  {lab}")
        return 0
    rows = [r for r in table if r[0] == label]
    if not rows:
        print(f"no word carries {label!r}")
        return 1
    for _, fid, name, count, source in rows:
        print(f"{fid}\t{name}" + (f"\t({count} generated words)" if source == "generated" else ""))
    return 0


def csv_text(header, rows) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue()


def coverage_csv(root: Path = ROOT) -> str:
    return csv_text(("language", "word", "signature", "construct"), coverage(root)[0])


def rules_csv(root: Path = ROOT) -> str:
    return csv_text(("language", "rule_id", "words"), coverage(root)[1])


def write_all(out: Path, root: Path = ROOT) -> list:
    """Write the six derived files under `out`; return their names."""
    out.mkdir(parents=True, exist_ok=True)
    (out / MANIFEST).write_bytes(serialize(manifest(root)))
    (out / STRESS_MANIFEST).write_bytes(serialize(stress_manifest(root)))
    cover, rules = coverage(root)
    (out / "coverage.csv").write_bytes(csv_text(("language", "word", "signature", "construct"), cover).encode("utf-8"))
    (out / "rules.csv").write_bytes(csv_text(("language", "rule_id", "words"), rules).encode("utf-8"))
    (out / "labels.csv").write_bytes(csv_text(("label", "test_case", "word", "words", "source"), label_table(root)).encode("utf-8"))
    import tiers

    (out / CORE_TIER).write_text("\n".join(tiers.core(tiers.compute(root))) + "\n", encoding="utf-8", newline="\n")
    return [MANIFEST, STRESS_MANIFEST, "coverage.csv", "rules.csv", "labels.csv", CORE_TIER]
