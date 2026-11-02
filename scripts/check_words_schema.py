#!/usr/bin/env python3
"""Validate every words.yaml (fixtures and stress) and the manifest against their JSON Schemas.

Needs PyYAML and jsonschema (pip install -r scripts/requirements.txt). Also fails any conformance
fixture whose fieldworks_producible is not true (PROTOCOL.md section 9).
"""
import json
import sys

from suite import ROOT, STRESS_GROUP, fixture_dirs, fixture_id, load_words

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required: pip install -r scripts/requirements.txt")


def main() -> int:
    schema = json.loads((ROOT / "schema" / "words.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
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
        if directory in fixture_dirs() and data.get("fieldworks_producible") is not True:
            problems.append(f"{name}/words.yaml: fieldworks_producible must be true")
    manifest_schema = json.loads((ROOT / "schema" / "conformance-manifest.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(manifest_schema)
    manifest = json.loads((ROOT / "generated" / "hc-conformance-manifest.v2.json").read_text(encoding="utf-8"))
    for error in Draft202012Validator(manifest_schema).iter_errors(manifest):
        problems.append(f"manifest: {'/'.join(str(p) for p in error.absolute_path)}: {error.message[:200]}")
    for problem in problems:
        print(problem)
    print(f"words schema: {checked} words.yaml files + manifest, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
