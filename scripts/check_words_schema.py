#!/usr/bin/env python3
"""Validate every words.yaml (fixtures and stress) against its JSON Schema.

Needs PyYAML and jsonschema (pip install -r scripts/requirements.txt). Also validates each optional whynot.yaml sidecar against schema/whynot.schema.json (PROTOCOL.md section 11)
and resolves its ids in grammar.xml. Also fails any words.yaml that
carries the dropped fieldworks_producible key (ADR 0004).
"""
import json
import re
import sys

from suite import ROOT, STRESS_GROUP, fixture_dirs, fixture_id, load_words

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required: pip install -r scripts/requirements.txt")


def whynot_problems(directory, validator, words) -> list:
    """Validate an optional whynot.yaml: schema, ids that exist in grammar.xml, and words that exist."""
    path = directory / "whynot.yaml"
    if not path.is_file():
        return []
    name = directory.relative_to(ROOT).as_posix()
    data = load_words(path)
    problems = [
        f"{name}/whynot.yaml: {'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message[:200]}"
        for e in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    ]
    if problems:
        return problems
    xml = (directory / "grammar.xml").read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid="([^"]+)"', xml))
    morphemes = set(re.findall(r"<MorphemeId>([^<]+)</MorphemeId>", xml))
    listed = {w["word"]: w for w in words.get("words", [])}
    for row in data["rows"]:
        where = f"{name}/whynot.yaml: word {row['word']}"
        if row["word"] not in listed:
            problems.append(f"{where}: not a word of words.yaml")
        elif listed[row["word"]].get("expect_skip"):
            problems.append(f"{where}: a skipped word cannot carry a why-not row")
        failure = row.get("failure", {})
        for ref in list(row["expect"]) + list(failure.get("morphs", [])):
            if ref["morpheme"] not in morphemes:
                problems.append(f"{where}: morpheme {ref['morpheme']!r} is not a MorphemeId in grammar.xml")
            if ref["allomorph"] not in ids:
                problems.append(f"{where}: allomorph {ref['allomorph']!r} is not an id in grammar.xml")
        environment = failure.get("environment")
        if environment and environment["allomorph_id"] not in ids:
            problems.append(f"{where}: environment allomorph {environment['allomorph_id']!r} is not an id in grammar.xml")
    return problems


def main() -> int:
    schema = json.loads((ROOT / "schema" / "words.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    whynot_schema = json.loads((ROOT / "schema" / "whynot.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(whynot_schema)
    whynot_validator = Draft202012Validator(whynot_schema)
    Draft202012Validator.check_schema(json.loads((ROOT / "schema" / "whynot-output.schema.json").read_text(encoding="utf-8")))
    problems, checked = [], 0
    directories = fixture_dirs() + [
        d for d in sorted((ROOT / STRESS_GROUP).iterdir()) if (d / "words.yaml").is_file()
    ]
    for directory in directories:
        name = directory.relative_to(ROOT).as_posix()
        data = load_words(directory / "words.yaml")
        checked += 1
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
            where = "/".join(str(p) for p in error.absolute_path) or "(root)"
            problems.append(f"{name}/words.yaml: {where}: {error.message[:200]}")
        problems += whynot_problems(directory, whynot_validator, data)
        if "fieldworks_producible" in data:
            problems.append(f"{name}/words.yaml: fieldworks_producible is dropped (ADR 0004)")
    for problem in problems:
        print(problem)
    print(f"words schema: {checked} words.yaml files, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
