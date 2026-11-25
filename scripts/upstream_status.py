#!/usr/bin/env python3
"""Report every fixture `upstream` entry with its state, grouped by what the owner must do (PROTOCOL.md section 12).

  python3 scripts/upstream_status.py [--machine-checkout DIR] [--strict]

Exit 0 always; --strict exits 1 when any entry is merged, closed-unmerged or issue-closed (a scheduled job, not the
per-PR gate). Needs PyYAML (scripts/requirements.txt) and, for states, an authenticated gh.
"""
import argparse
import sys

from suite import STRESS_GROUP, ROOT, fixture_dirs, fixture_id, load_words
from upstream import resolve

GROUPS = [
    ("merged", "MERGED: re-point header, PROVENANCE and TSV citations to the merge commit, then drop or keep the entry as history"),
    ("closed-unmerged", "CLOSED UNMERGED: decide, retire (docs/engine-only-fixture-retirement.md) or re-check"),
    ("issue-closed", "ISSUE CLOSED: decide, retire or re-check"),
    ("pending", "PENDING"),
    ("satisfied", "SATISFIED"),
]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--machine-checkout", help="a sillsdev/machine checkout, for engine ancestry")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any entry needs action")
    args = ap.parse_args(argv)
    found = {k: [] for k, _ in GROUPS}
    dirs = fixture_dirs() + [d for d in sorted((ROOT / STRESS_GROUP).glob("*")) if (d / "words.yaml").is_file()]
    for d in dirs:
        for e in load_words(d / "words.yaml").get("upstream") or []:
            state, reason = resolve(e, args.machine_checkout)
            found[state].append(f"  {fixture_id(d)}: {e['ref']} ({e['kind']}, affects {e['affects']}): {reason}")
    total = sum(map(len, found.values()))
    for key, title in GROUPS:
        if found[key]:
            print(f"{title} [{len(found[key])}]")
            print("\n".join(found[key]))
    print(f"upstream: {total} entries, " + ", ".join(f"{len(found[k])} {k}" for k, _ in GROUPS))
    needs = sum(len(found[k]) for k in ("merged", "closed-unmerged", "issue-closed"))
    return 1 if args.strict and needs else 0


if __name__ == "__main__":
    sys.exit(main())
