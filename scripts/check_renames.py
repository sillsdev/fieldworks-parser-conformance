#!/usr/bin/env python3
"""docs/renames.tsv is the contract consumers remap removed test case ids from (ADR 0005).

Fails when: the header's first columns are not old_id, new_id, covered_by, wave; a live test case id appears
in old_id (an id is never reused once retired); new_id is neither `retired` nor a live test case; covered_by
names a test case that is not live; wave is empty or not `wave-YYYY-MM-DD`; a row is malformed or repeats an
old_id; or an existing row changed or was removed against the merge base with origin/main (rows are only
appended). The merge-base comparison is skipped, with a note, when git or the base is unavailable.
"""
import re
import subprocess
import sys

from suite import ROOT, STRESS_GROUP, fixture_dirs, fixture_id

PATH = "docs/renames.tsv"
HEADER = ["old_id", "new_id", "covered_by", "wave"]
WAVE = re.compile(r"^wave-\d{4}-\d{2}-\d{2}$")


def parse(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def problems_for(lines, live, base_lines=None):
    problems = []
    if not lines or lines[0].split("\t")[: len(HEADER)] != HEADER:
        problems.append(f"{PATH}: the header must start with {'\t'.join(HEADER)}")
    seen = set()
    for number, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        if len(cells) < len(HEADER):
            problems.append(f"{PATH}:{number}: expected at least {len(HEADER)} tab-separated columns")
            continue
        old_id, new_id, covered_by, wave = cells[:4]
        where = f"{PATH}:{number} ({old_id})"
        if old_id in live:
            problems.append(f"{where}: old_id is a live test case; a retired id is never reused")
        if old_id in seen:
            problems.append(f"{where}: old_id appears more than once")
        seen.add(old_id)
        if new_id != "retired" and new_id not in live:
            problems.append(f"{where}: new_id {new_id!r} is neither 'retired' nor a live test case")
        for target in filter(None, covered_by.split(",")):
            if target not in live:
                problems.append(f"{where}: covered_by {target!r} is not a live test case")
        if not WAVE.match(wave):
            problems.append(f"{where}: wave {wave!r} must be wave-YYYY-MM-DD")
    if base_lines is not None:
        for number, old in enumerate(base_lines, start=1):
            if number > len(lines) or lines[number - 1] != old:
                problems.append(f"{PATH}:{number}: a row from the merge base changed or was removed; rows are only appended")
                break
    return problems


def base_text():
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout.strip()

    try:
        base = git("merge-base", "HEAD", "origin/main")
        return git("show", f"{base}:{PATH}") if git("ls-tree", base, PATH) else ""
    except (OSError, subprocess.CalledProcessError):
        return None


def main() -> int:
    live = {fixture_id(d) for d in fixture_dirs()} | {fixture_id(d) for d in fixture_dirs(groups=(STRESS_GROUP,))}
    path = ROOT / PATH
    if not path.is_file():
        print(f"{PATH} is missing")
        return 1
    base = base_text()
    if base is None:
        print(f"note: no merge base with origin/main; the append-only comparison is skipped")
    problems = problems_for(parse(path.read_text(encoding="utf-8")), live, None if base is None else parse(base))
    for problem in problems:
        print(problem)
    if not problems:
        print(f"{PATH}: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
