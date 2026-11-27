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

from suite import FIXTURE_GROUPS, ROOT, STRESS_GROUP, fixture_dirs, fixture_id, load_words, sha256_text, words_summary

FORMAT = "hc-conformance-manifest/v2"
WORDS_FORMAT = "hc-conformance-words/v1"
GRAMMAR_FORMAT = "sil-machine-hermit-crab-input-xml/v1"
DTD = "HermitCrabInput.dtd"
MANIFEST = "hc-conformance-manifest.v2.json"
STRESS_FORMAT = "hc-conformance-stress-manifest/v2"
STRESS_MANIFEST = "stress-manifest.v2.json"
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
        for case in data["words"]:
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
    """Write the four derived files under `out`; return their names."""
    out.mkdir(parents=True, exist_ok=True)
    (out / MANIFEST).write_bytes(serialize(manifest(root)))
    (out / STRESS_MANIFEST).write_bytes(serialize(stress_manifest(root)))
    cover, rules = coverage(root)
    (out / "coverage.csv").write_bytes(csv_text(("language", "word", "signature", "construct"), cover).encode("utf-8"))
    (out / "rules.csv").write_bytes(csv_text(("language", "rule_id", "words"), rules).encode("utf-8"))
    return [MANIFEST, STRESS_MANIFEST, "coverage.csv", "rules.csv"]
