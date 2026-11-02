#!/usr/bin/env python3
"""docs/grammars.md must list every fixture exactly once as "- `group/name`: ..." and nothing else."""
import re
import sys

from suite import ROOT, fixture_dirs, fixture_id

LISTED = re.compile(r"^- `((?:languages|edge-cases)/[^`]+)`", re.M)


def main() -> int:
    text = (ROOT / "docs" / "grammars.md").read_text(encoding="utf-8")
    listed = LISTED.findall(text)
    on_disk = {fixture_id(d) for d in fixture_dirs()}
    problems = []
    for name in sorted(on_disk - set(listed)):
        problems.append(f"fixture not listed in docs/grammars.md: {name}")
    for name in sorted(set(listed) - on_disk):
        problems.append(f"docs/grammars.md lists a fixture that does not exist: {name}")
    for name in sorted({n for n in listed if listed.count(n) > 1}):
        problems.append(f"docs/grammars.md lists {name} more than once")
    for problem in problems:
        print(problem)
    print(f"grammars.md: {len(listed)} entries, {len(on_disk)} fixtures, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
