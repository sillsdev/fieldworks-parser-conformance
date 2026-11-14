#!/usr/bin/env python3
"""Check the batch A calibration families under calibration/ (scale families).

For each family: grammar.xml is the DTD-valid output of scripts/calib_a_gen.py (regenerated and compared byte
for byte), words.yaml passes schema/words.schema.json with fieldworks_producible true, words.txt lists exactly
the words of words.yaml (plus cap-words.yaml), every word is 5 to 40 characters, and calibration/README.md names
the family. Needs PyYAML, jsonschema and lxml or xmllint (pip install -r scripts/requirements.txt).
"""
import json
import sys

import calib_a_gen
import check_dtd
from suite import ROOT, load_words

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required: pip install -r scripts/requirements.txt")

OUT = ROOT / "calibration"


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
        cap_yaml = d / "cap-words.yaml"
        cap_words = [w["word"] for w in load_words(cap_yaml)["words"]] if cap_yaml.is_file() else []
        listed = (d / "words.txt").read_text(encoding="utf-8").split()
        listed_cap = (d / "cap-words.txt").read_text(encoding="utf-8").split() if (d / "cap-words.txt").is_file() else []
        if listed != yaml_words:
            problems.append(f"{name}: words.txt does not list the words of words.yaml in order")
        if listed_cap != cap_words:
            problems.append(f"{name}: cap-words.txt does not list the words of cap-words.yaml in order")
        every = yaml_words + cap_words
        if len(set(every)) != len(every):
            problems.append(f"{name}: duplicate words")
        for w in every:
            if not 5 <= len(w) <= 40:
                problems.append(f"{name}: word {w!r} is {len(w)} characters, not 5 to 40")
        if name == "cal-prefilter-scale" and len(every) < 600:
            problems.append(f"{name}: {len(every)} words, fewer than the 600 that let --prefilter auto engage")
        if name == "cal-work-cap" and not cap_words:
            problems.append(f"{name}: no cap words")
        print(f"{name}: {len(yaml_words)} words, {len(cap_words)} cap words")
    problems += check_dtd.doctype_problems(grammars)
    if check_dtd.etree is not None:
        problems += check_dtd.with_lxml(grammars)
    else:
        problems += check_dtd.with_xmllint(grammars)
    for p in problems:
        print(p)
    print(f"calibration batch A: {len(calib_a_gen.FAMILIES)} families, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
