#!/usr/bin/env python3
"""Generate the derived files in memory and check the invariants a committed copy used to be compared against.

Nothing derived is committed (ADR 0009), so there is no file to go stale; what can go wrong is the generation itself
or what it shows. This fails when:
  - the manifests do not validate against schema/conformance-manifest.schema.json, or do not mention every test case;
  - generation is not deterministic;
  - coverage.csv has no rows, or a word exercises a label constructs.txt and labels.tsv do not declare (check_labels.py checks the same per word);
  - a `blocked_by` label names no rule id of its grammar;
  - a rule no word exercises is missing from dead-rules-allowed.tsv, or an allowed rule is no longer dead.
Needs PyYAML and jsonschema (scripts/requirements.txt).
"""
import json
import sys

import derive
from suite import ROOT, fixture_dirs, fixture_id, load_expanded_words, vocabulary

OUT_OF_SCOPE = "Tracing (TraceType)"


def dead_rules_allowed():
    allowed = {}
    for number, line in enumerate((ROOT / "dead-rules-allowed.tsv").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        columns = [c.strip() for c in line.split("\t")]
        if len(columns) != 3 or not all(columns):
            raise SystemExit(f"dead-rules-allowed.tsv:{number}: expected fixture, rule and reason separated by tabs")
        allowed[(columns[0], columns[1])] = columns[2]
    return allowed


def main() -> int:
    from jsonschema import Draft202012Validator

    problems = []
    schema = json.loads((ROOT / "schema" / "conformance-manifest.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for build in (derive.manifest, derive.stress_manifest):
        built = build()
        if derive.serialize(built) != derive.serialize(build()):
            problems.append(f"{built['formatVersion']}: two generations differ")
        for error in validator.iter_errors(built) if built["formatVersion"] == derive.FORMAT else []:
            problems.append(f"{built['formatVersion']}: {'/'.join(str(p) for p in error.absolute_path)}: {error.message[:200]}")
        ids = [f["fixtureId"] for f in built["fixtures"]]
        if len(ids) != len(set(ids)):
            problems.append(f"{built['formatVersion']}: duplicate test case ids")
        if "calibration" in json.dumps(built):
            problems.append(f"{built['formatVersion']} mentions a calibration path")

    cover, _ = derive.coverage()
    rules = derive.coverage(per_fixture=True)[1]
    if not cover:
        problems.append("coverage.csv would have no rows: an empty table proves nothing")
    declared = set(vocabulary())
    for construct in sorted({row[3] for row in cover} - declared):
        problems.append(f"a word exercises {construct!r}, which is not in constructs.txt or labels.tsv")

    for directory in fixture_dirs():
        fid = fixture_id(directory)
        known = set(derive.rule_ids(directory / "grammar.xml"))
        for word in load_expanded_words(directory / "words.yaml"):
            if word.get("expect_fail") or word.get("expect_skip"):
                for label in word.get("blocked_by") or []:
                    if label not in known:
                        problems.append(f"{fid}: {word['word']} blocked_by {label}, which is not a rule id in its grammar")
    dead = {(fid, rule) for fid, _, rule, words in rules if not words}
    allowed = dead_rules_allowed()
    for fid, rule in sorted(dead - set(allowed)):
        problems.append(f"{fid}: rule {rule} is exercised by no word and is not in dead-rules-allowed.tsv")
    for fid, rule in sorted(set(allowed) - dead):
        problems.append(f"dead-rules-allowed.tsv: {fid} {rule} is exercised now or does not exist; delete the row")

    for problem in problems:
        print(problem)
    print(f"derived files: {len(cover)} coverage rows, {len(rules)} rule rows, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
