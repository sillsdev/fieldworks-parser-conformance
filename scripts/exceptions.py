"""status.yaml: the one place every tracked departure from the reference is recorded (ADR 0007, PROTOCOL.md section 12).

load() reads it, problems() checks it against schema/status.schema.json and the test cases it names, and report()
resolves each row's upstream reference (scripts/upstream.py) and groups the rows by what the owner must do.
Needs PyYAML and jsonschema (scripts/requirements.txt); the report also needs an authenticated gh for states.
"""
import json
import sys

from suite import ROOT, fixture_dirs, fixture_id, load_expanded_words, load_words, STRESS_GROUP
from upstream import resolve

STATUS = ROOT / "status.yaml"
GROUPS = [
    ("merged", "MERGED: re-point the reference commit past the merge, then delete the row"),
    ("closed-unmerged", "CLOSED UNMERGED: decide, retire (docs/engine-only-fixture-retirement.md) or re-check"),
    ("issue-closed", "ISSUE CLOSED: decide, retire or re-check"),
    ("rejected", "REJECTED (Jira Won't Fix/Won't Do): decide, retire or re-check"),
    ("pending", "PENDING"),
    ("satisfied", "SATISFIED"),
]


def load(path=STATUS) -> list:
    """The rows of status.yaml, or [] when it does not exist."""
    if not path.is_file():
        return []
    return (load_words(path) or {}).get("exceptions") or []


def test_cases() -> dict:
    """Every test case id (conformance and stress) -> the set of its words."""
    found = {}
    for d in fixture_dirs() + fixture_dirs(groups=(STRESS_GROUP,)):
        found[fixture_id(d)] = {w["word"] for w in load_expanded_words(d / "words.yaml")}
    return found


def problems(path=STATUS, cases=None) -> list:
    from jsonschema import Draft202012Validator

    if not path.is_file():
        return []
    schema = json.loads((ROOT / "schema" / "status.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    data = load_words(path)
    found = [
        f"status.yaml: {'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message[:200]}"
        for e in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.absolute_path))
    ]
    if found:
        return found
    cases = test_cases() if cases is None else cases
    seen = set()
    for row in data["exceptions"]:
        where = f"status.yaml: {row['case']}" + (f" word {row['word']!r}" if "word" in row else "")
        if row["case"] not in cases:
            found.append(f"{where}: names no test case")
        elif "word" in row and row["word"] not in cases[row["case"]]:
            found.append(f"{where}: the test case has no such word")
        key = (row["case"], row.get("word"), row["ref"])
        if key in seen:
            found.append(f"{where}: duplicate row for {row['ref']}")
        seen.add(key)
    return found


def entry(row: dict) -> dict:
    """A row as scripts/upstream.py reads an upstream entry."""
    return {"ref": row["ref"], "kind": row["ref_type"], "head": row.get("head"), "affects": row["affects"], "note": row["reason"]}


def report(machine_checkout=None, strict=False, rows=None, resolver=resolve) -> int:
    """Print every row by state. Exit 0 always; with strict, 1 when any row is merged, closed-unmerged, issue-closed or rejected."""
    rows = load() if rows is None else rows
    found = {k: [] for k, _ in GROUPS}
    for row in rows:
        state, reason = resolver(entry(row), machine_checkout)
        word = f" {row['word']!r}" if "word" in row else ""
        found[state].append(f"  {row['case']}{word}: {row['ref']} ({row['kind']}, affects {row['affects']}): {reason}")
    for key, title in GROUPS:
        if found[key]:
            print(f"{title} [{len(found[key])}]")
            print("\n".join(found[key]))
    print(f"status.yaml: {len(rows)} exceptions, " + ", ".join(f"{len(found[k])} {k}" for k, _ in GROUPS))
    needs = sum(len(found[k]) for k in ("merged", "closed-unmerged", "issue-closed", "rejected"))
    return 1 if strict and needs else 0


def main() -> int:
    found = problems()
    for p in found:
        print(p)
    print(f"status.yaml: {len(load())} exceptions, {len(found)} problems")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
