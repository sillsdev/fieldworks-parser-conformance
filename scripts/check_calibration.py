#!/usr/bin/env python3
"""Check the calibration families under calibration/ (batch A scale families, batch B structural families).

For each family: grammar.xml is the DTD-valid output of scripts/calib_a_gen.py (batch A) or scripts/calib_b_gen.py (batch B) (regenerated and compared byte
for byte), words.yaml passes schema/words.schema.json with fieldworks_producible true, words.txt lists exactly
the words of words.yaml (plus the cap-words.work-cap-N.yaml file, whose name must carry the cap), every word is 5 to 40 characters, and calibration/README.md names
the family. Needs PyYAML, jsonschema and lxml or xmllint (pip install -r scripts/requirements.txt).
"""
import json
import sys

import calib_a_gen
import calib_b_gen
import check_dtd
from suite import ROOT, load_words

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required: pip install -r scripts/requirements.txt")

OUT = ROOT / "calibration"


HEADER = "CALIBRATION ONLY: never run in conformance or engine test runs"
CONSUMER_CATEGORIES = ("languages", "edge-cases", "stress/edge-cases")


def check_lexsize(validator, readme, grammars):
    """The lexicon-size ladder: four grammars, one word list. A grammar over MAX_COMMIT_BYTES is not committed;
    its grammar.sha256 must equal the hash of what the generator writes."""
    problems, lists, base = [], {}, None
    for name, n in calib_a_gen.LEXSIZES.items():
        d = OUT / name
        xml = calib_a_gen.fam_lexsize(n)["xml"]
        digest = calib_a_gen.sha256_hex(xml)
        if (d / "grammar.sha256").read_text(encoding="utf-8").strip() != digest:
            problems.append(f"{name}: grammar.sha256 differs from the generator's grammar")
        big = len(xml.encode("utf-8")) > calib_a_gen.MAX_COMMIT_BYTES
        if big:
            if (d / "grammar.xml").exists():
                problems.append(f"{name}: grammar.xml is over {calib_a_gen.MAX_COMMIT_BYTES} bytes and must not be committed")
        else:
            grammars.append(d / "grammar.xml")
            if (d / "grammar.xml").read_text(encoding="utf-8") != xml:
                problems.append(f"{name}/grammar.xml differs from what scripts/calib_a_gen.py generates")
        if name not in readme:
            problems.append(f"calibration/README.md does not name {name}")
        data = load_words(d / "words.yaml")
        for error in validator.iter_errors(data):
            problems.append(f"{name}/words.yaml: {'/'.join(str(p) for p in error.absolute_path)}: {error.message[:160]}")
        if data.get("fieldworks_producible") is not True:
            problems.append(f"{name}/words.yaml: fieldworks_producible must be true")
        yaml_words = [w["word"] for w in data["words"]]
        lists[name] = yaml_words
        if (d / "words.txt").read_text(encoding="utf-8").split() != yaml_words:
            problems.append(f"{name}: words.txt does not list the words of words.yaml in order")
        for w in yaml_words:
            if not 5 <= len(w) <= 40:
                problems.append(f"{name}: word {w!r} is not 5 to 40 characters")
        print(f"{name}: {len(yaml_words)} words, grammar {'hash only' if big else 'committed'}")
    if len({tuple(v) for v in lists.values()}) != 1:
        problems.append("the lexsize grammars do not share one word list")
    return problems


def check_isolation(readme):
    """Calibration words must never reach a conformance or engine run: no calibration path in either manifest, no
    calibration directory in a category the consumers enumerate, and the warning header everywhere."""
    problems = []
    for manifest in sorted((ROOT / "generated").glob("*manifest*.json")):
        text = manifest.read_text(encoding="utf-8")
        if "calibration" in text or any(n in text for n in list(calib_a_gen.FAMILIES) + list(calib_a_gen.LEXSIZES) + list(calib_b_gen.FAMILIES)):
            problems.append(f"{manifest.name} mentions a calibration path")
    names = set(calib_a_gen.FAMILIES) | set(calib_a_gen.LEXSIZES) | set(calib_b_gen.FAMILIES)
    for cat in CONSUMER_CATEGORIES:
        base = ROOT / cat
        if not base.is_dir():
            continue
        for child in base.iterdir():
            marker = (child / "words.yaml")
            kind = marker.read_text(encoding="utf-8").split("\n", 1)[0] if marker.is_file() else ""
            if child.name in names or child.name.startswith("cal-") or kind.startswith("# kind: calibration"):
                problems.append(f"{cat}/{child.name} is a calibration grammar in a category the consumers enumerate")
    for cat in ("languages", "edge-cases", "stress"):
        if (ROOT / cat / "calibration").exists():
            problems.append(f"{cat}/calibration exists")
    if HEADER not in readme.split("\n\n", 2)[1] + readme.split("\n\n", 2)[2][:600]:
        problems.append("calibration/README.md lacks the CALIBRATION ONLY header at its top")
    if HEADER.lower() not in (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower():
        problems.append("AGENTS.md lacks the calibration-only warning")
    for y in sorted((ROOT / "calibration").glob("*/*.yaml")):
        first = y.read_text(encoding="utf-8").split("\n", 1)[0]
        if HEADER not in first:
            problems.append(f"{y.relative_to(ROOT).as_posix()}: first line lacks the CALIBRATION ONLY header")
    return problems


def main() -> int:
    problems = []
    validator = Draft202012Validator(json.loads((ROOT / "schema" / "words.schema.json").read_text(encoding="utf-8")))
    readme = (ROOT / "calibration" / "README.md").read_text(encoding="utf-8")
    grammars = []
    for name, fn in calib_a_gen.FAMILIES.items():
        d = OUT / name
        grammar = d / "grammar.xml"
        grammars.append(grammar)
        if name not in readme:
            problems.append(f"calibration/README.md does not name {name}")
        if grammar.read_text(encoding="utf-8") != fn()["xml"]:
            problems.append(f"{name}/grammar.xml differs from what scripts/calib_a_gen.py generates")
        data = load_words(d / "words.yaml")
        for error in validator.iter_errors(data):
            problems.append(f"{name}/words.yaml: {'/'.join(str(p) for p in error.absolute_path)}: {error.message[:160]}")
        if data.get("fieldworks_producible") is not True:
            problems.append(f"{name}/words.yaml: fieldworks_producible must be true")
        yaml_words = [w["word"] for w in data["words"]]
        cap_yaml = d / calib_a_gen.CAP_YAML
        cap_words = []
        if cap_yaml.is_file():
            cdata = load_words(cap_yaml)
            cap_words = [w["word"] for w in cdata["words"]]
            if cdata.get("work_cap") != calib_a_gen.CAP_STEPS:
                problems.append(f"{name}: {cap_yaml.name} work_cap is not {calib_a_gen.CAP_STEPS}")
            for w in cdata["words"]:
                if w.get("expect_status") != "CAP" or not w.get("note"):
                    problems.append(f"{name}: cap word {w.get('word')!r} lacks expect_status CAP or a note")
        listed = (d / "words.txt").read_text(encoding="utf-8").split()
        listed_cap = (d / calib_a_gen.CAP_TXT).read_text(encoding="utf-8").split() if (d / calib_a_gen.CAP_TXT).is_file() else []
        if listed != yaml_words:
            problems.append(f"{name}: words.txt does not list the words of words.yaml in order")
        if listed_cap != cap_words:
            problems.append(f"{name}: {calib_a_gen.CAP_TXT} does not list the words of {calib_a_gen.CAP_YAML} in order")
        every = yaml_words + cap_words
        if len(set(every)) != len(every):
            problems.append(f"{name}: duplicate words")
        for w in every:
            if not 5 <= len(w) <= 40:
                problems.append(f"{name}: word {w!r} is {len(w)} characters, not 5 to 40")
        if name == "cal-prefilter-scale" and len(every) < 600:
            problems.append(f"{name}: {len(every)} words, fewer than the 600 that let --prefilter auto engage")
        if name == "cal-work-cap" and (not cap_words or not (d / "README.md").is_file()):
            problems.append(f"{name}: no cap words or no README.md")
        print(f"{name}: {len(yaml_words)} words, {len(cap_words)} cap words")
    for name, fn in calib_b_gen.FAMILIES.items():
        d = OUT / name
        grammars.append(d / "grammar.xml")
        if name not in readme:
            problems.append(f"calibration/README.md does not name {name}")
        if (d / "grammar.xml").read_text(encoding="utf-8") != fn().xml():
            problems.append(f"{name}/grammar.xml differs from what scripts/calib_b_gen.py generates")
        data = load_words(d / "words.yaml")
        for error in validator.iter_errors(data):
            problems.append(f"{name}/words.yaml: {'/'.join(str(p) for p in error.absolute_path)}: {error.message[:160]}")
        if data.get("fieldworks_producible") is not True:
            problems.append(f"{name}/words.yaml: fieldworks_producible must be true")
        yaml_words = [w["word"] for w in data["words"]]
        if (d / "words.txt").read_text(encoding="utf-8").split() != yaml_words:
            problems.append(f"{name}: words.txt does not list the words of words.yaml in order")
        ladder = [l.split("\t")[0] for l in (d / "ladder.tsv").read_text(encoding="utf-8").splitlines()[1:]]
        if ladder != yaml_words:
            problems.append(f"{name}: ladder.tsv does not list the words of words.yaml in order")
        if len(set(yaml_words)) != len(yaml_words):
            problems.append(f"{name}: duplicate words")
        for w in yaml_words:
            if not 5 <= len(w) <= 40:
                problems.append(f"{name}: word {w!r} is {len(w)} characters, not 5 to 40")
        print(f"{name}: {len(yaml_words)} words (batch B)")
    problems += check_lexsize(validator, readme, grammars)
    problems += check_isolation(readme)
    problems += check_dtd.doctype_problems(grammars)
    if check_dtd.etree is not None:
        problems += check_dtd.with_lxml(grammars)
    else:
        problems += check_dtd.with_xmllint(grammars)
    for p in problems:
        print(p)
    print(f"calibration: {len(calib_a_gen.FAMILIES)} batch A and {len(calib_b_gen.FAMILIES)} batch B families, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
