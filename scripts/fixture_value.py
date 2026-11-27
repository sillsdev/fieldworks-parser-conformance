#!/usr/bin/env python3
"""What does each test case detect? Reports that inform merge and retire decisions (ADR 0008), never decide them.

A measurement tool like measure.py, not a check. Output goes to stdout or --out and is attached to the issue that
uses it; it is derived and never committed (ADR 0009). Standard library plus PyYAML (already required by suite.py).

  fixture_value.py bugs                       every bug id cited by a test case, and the test cases that cite it
  fixture_value.py candidates --machine DIR   for each machine#N, the commits in DIR's history that mention it
  fixture_value.py detection  --builds F ...  per bug: the words that fail on the bug build and pass on the fixed one
  fixture_value.py coverage   --runner DLL    one instrumented hc-conformance run per test case: covered, unique and
                                              marginal lines and branches (a backstop: it only nominates)

detection (ADR 0008 items 1 and 4). The builds file is JSON, kept outside the repository:

  {"fixed": {"runner": "/path/to/hc-conformance"},
   "bugs": {"machine#653": {"runner": "/path/to/hc-conformance-at-bug-build"},
            "pangloss#58":  {"runner": "/path/to/hc-conformance", "adapter": "/path/to/pangloss batch {grammar} {words} {output}"}}}

`runner` is a built `hc-conformance` (a DLL, an executable, or a command line). Without `adapter` the C# engine
inside that runner is the engine under test, so a C# bug build is the reference runner rebuilt with the fix
reverted. With `adapter` the runner only drives an external engine through the batch contract (PROTOCOL.md), so a
PanGloss bug build is a PanGloss binary from before its fix. The fixed build is the reference runner at
reference.commit. The suite is replayed whole, once per build (44 s), and a word is a detection of a bug when it
fails on the bug build and passes on the fixed build; test cases that do not cite the bug are reported as well,
marked, since they detect it too.

coverage. `--runner` is the reference runner's DLL. Each test case is copied into a one-case suite and run under
`dotnet-coverage collect` filtered to the engine's source files; cobertura output gives lines and branch
conditions. Per test case: covered (all it hits), unique (hit by it alone) and marginal (added when test cases are
taken greediest first; the test cases that add 0 lines and 0 branches are the first removal candidates to
examine, and examining them is a written reason, not this number).
"""
import argparse
import csv
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from suite import ROOT, fixture_dirs, fixture_id

# Only the engine counts: the HermitCrab library and the SIL.Machine core it sits on, not the runner or the tool.
_ENGINE_FILE = re.compile(r"/src/((?:SIL\.Machine|SIL\.Machine\.Morphology\.HermitCrab)/.+\.cs)$")

# Issue ids as the suite cites them. A bare `#N` is ambiguous (machine or PanGloss) and is reported as `?#N`.
_PATTERNS = [
    (re.compile(r"\b[Mm]achine(?:\s+(?:PRs?|issues?|pull request))?\s*#(\d+)"), "machine#{}"),
    (re.compile(r"\bmachine#(\d+)"), "machine#{}"),
    (re.compile(r"\bPanGloss(?:\s+(?:PRs?|issues?|pull request))?\s*#(\d+)"), "pangloss#{}"),
    (re.compile(r"\bFieldWorks#(\d+)"), "fieldworks#{}"),
    (re.compile(r"\b(LT-\d+)\b"), "{}"),
    (re.compile(r"\bdivergences?[/ ]+(\d{3})\b"), "pangloss-divergence-{}"),
]
_BARE = re.compile(r"(?<![\w/])#(\d{2,4})\b")
_DIVERGENCE_FILE = re.compile(r"docs/divergences/(\d{3})-")


def _ids_in(text: str):
    found = set()
    for pattern, template in _PATTERNS:
        for m in pattern.finditer(text):
            found.add(template.format(m.group(1)))
    for m in _DIVERGENCE_FILE.finditer(text):
        found.add(f"pangloss-divergence-{m.group(1)}")
    claimed = {m.group(1) for pattern, _ in _PATTERNS[:3] for m in pattern.finditer(text)}
    for m in _BARE.finditer(text):
        if m.group(1) not in claimed:
            found.add(f"?#{m.group(1)}")
    return found


def cited_bugs(root: Path = ROOT) -> dict:
    """{bug id: {test case id, ...}} from READMEs, words.yaml (notes and sources) and status.yaml."""
    import yaml

    bugs = defaultdict(set)
    for directory in fixture_dirs(root):
        fid = fixture_id(directory, root)
        for name in ("README.md", "words.yaml"):
            path = directory / name
            if path.is_file():
                for bug in _ids_in(path.read_text(encoding="utf-8")):
                    bugs[bug].add(fid)
    status = root / "status.yaml"
    if status.is_file():
        for row in (yaml.safe_load(status.read_text(encoding="utf-8")) or {}).get("exceptions", []):
            ref = str(row.get("ref", ""))
            ids = _ids_in(ref.replace("sillsdev/machine#", "machine#")) or {ref}
            for bug in ids:
                bugs[bug].add(row["case"])
    return bugs


def cmd_bugs(args) -> int:
    bugs = cited_bugs(Path(args.suite))
    rows = sorted(bugs.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    out = []
    for bug, cases in rows:
        out.append(f"{bug}\t{len(cases)}\t{' '.join(sorted(cases))}")
    _emit("\n".join(out) + "\n", args.out)
    return 0


def cmd_candidates(args) -> int:
    lines = []
    for bug in sorted(b for b in cited_bugs() if b.startswith("machine#")):
        number = bug.split("#")[1]
        log = subprocess.run(
            ["git", "-C", args.machine, "log", args.ref, "--format=%h %s", "-E", f"--grep=#{number}\\b"],
            capture_output=True, text=True, check=False,
        ).stdout.strip()
        lines.append(f"{bug}\t{log.replace(chr(10), ' || ') or '(no commit mentions it)'}")
    _emit("\n".join(lines) + "\n", args.out)
    return 0


def _runner_command(spec: dict) -> list:
    runner = shlex.split(spec["runner"])
    if len(runner) == 1 and runner[0].endswith(".dll"):
        runner = ["dotnet", runner[0]]
    return runner


def run_suite(spec: dict, suite: Path) -> dict:
    """Replay the whole suite on one build. Returns {test case id: {failed words}} for failing test cases."""
    cmd = _runner_command(spec) + ["--fixtures", str(suite), "--include-pathological"]
    if spec.get("adapter"):
        cmd += ["--capabilities", spec.get("capabilities", "phonology"), "--adapter", spec["adapter"]]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode not in (0, 1):
        raise SystemExit(f"runner failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}")
    failed, current = {}, None
    for line in proc.stdout.splitlines():
        m = re.match(r"\[FAIL\] (\S+)", line)
        if m:
            current = failed.setdefault(m.group(1), set())
            continue
        m = re.match(r"    word '(.*)': ", line)
        if m and current is not None:
            current.add(m.group(1))
        elif not line.startswith("    "):
            current = None
    return failed


def detection(builds: dict, suite: Path = ROOT) -> dict:
    """{bug: {"citing": [...], "detectors": {test case: [words]}, "also": {test case: [words]}}}"""
    cited = cited_bugs(suite)
    baseline = run_suite(builds["fixed"], suite)
    result = {}
    for bug, spec in builds["bugs"].items():
        failed = run_suite(spec, suite)
        detectors = {}
        for case, words in failed.items():
            new = sorted(words - baseline.get(case, set()))
            if new:
                detectors[case] = new
        citing = cited.get(bug, set())
        result[bug] = {
            "citing": sorted(citing),
            "detectors": {c: w for c, w in sorted(detectors.items()) if c in citing},
            "also": {c: w for c, w in sorted(detectors.items()) if c not in citing},
        }
    result["_baseline_failing"] = {c: sorted(w) for c, w in sorted(baseline.items())}
    return result


def render_detection(result: dict) -> str:
    out = ["# Bug detection: which test cases detect each bug", "",
           "A detector fails on a build that has the bug and passes on the reference. The last detector of a bug",
           "is never retired (ADR 0008). Derived output; informs decisions, decides none.", ""]
    for bug in sorted(k for k in result if not k.startswith("_")):
        r = result[bug]
        out.append(f"## {bug}")
        out.append(f"- citing test cases: {len(r['citing'])}; detectors among them: {len(r['detectors'])}")
        if len(r["detectors"]) == 1:
            out.append("- LAST DETECTOR (only one test case detects it): " + next(iter(r["detectors"])))
        if not r["detectors"]:
            out.append("- no citing test case fails on the bug build (not a detection, or the build does not reproduce it)")
        for case, words in r["detectors"].items():
            out.append(f"  - {case}: {', '.join(words)}")
        for case, words in r["also"].items():
            out.append(f"  - also {case} (does not cite it): {', '.join(words)}")
        out.append("")
    if result.get("_baseline_failing"):
        out.append("## Failing on the fixed build itself (excluded from every detection above)")
        for case, words in result["_baseline_failing"].items():
            out.append(f"- {case}: {', '.join(words)}")
    return "\n".join(out) + "\n"


def cmd_detection(args) -> int:
    builds = json.loads(Path(args.builds).read_text(encoding="utf-8"))
    result = detection(builds, Path(args.suite))
    text = json.dumps(result, indent=1) + "\n" if args.json else render_detection(result)
    _emit(text, args.out)
    return 0


# ---------------------------------------------------------------- coverage


def parse_cobertura(path: Path):
    """(lines, branches): sets of 'file:line' hit and 'file:line:condition' taken."""
    lines, branches = set(), set()
    tree = ET.parse(path)
    for cls in tree.iter("class"):
        m = _ENGINE_FILE.search(cls.get("filename", "").replace("\\", "/"))
        if not m:
            continue
        name = m.group(1)
        for line in cls.iter("line"):
            number = line.get("number")
            if int(line.get("hits", "0")) > 0:
                lines.add(f"{name}:{number}")
            for cond in line.iter("condition"):
                if cond.get("coverage", "0%") not in ("0%", "0"):
                    branches.add(f"{name}:{number}:{cond.get('number')}")
    return lines, branches


def run_instrumented(case: Path, suite: Path, runner_dll: str, tool: str, work: Path):
    """Replay one test case under dotnet-coverage. Returns (lines, branches) or None when the case is skipped."""
    mini = work / "suite"
    if mini.exists():
        shutil.rmtree(mini)
    group = case.parent.name
    target = mini / group / case.name
    target.parent.mkdir(parents=True)
    shutil.copytree(case, target)
    out = work / "cov.xml"
    out.unlink(missing_ok=True)
    cmd = [tool, "collect", "-f", "cobertura", "-o", str(out),
           f"dotnet {runner_dll} --fixtures {mini} --include-pathological"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if not out.is_file():
        raise SystemExit(f"no coverage for {case}: {proc.stdout[-1000:]} {proc.stderr[-1000:]}")
    return parse_cobertura(out)


def coverage(cases, runner_dll: str, tool: str, suite: Path = ROOT, progress=None) -> dict:
    per = {}
    with tempfile.TemporaryDirectory(prefix="fixture-value-") as tmp:
        for i, case in enumerate(cases):
            fid = fixture_id(case, suite)
            per[fid] = run_instrumented(case, suite, runner_dll, tool, Path(tmp))
            if progress:
                progress(i + 1, len(cases), fid)
    return per


def summarise(per: dict) -> list:
    """Rows: test case, lines, branches, unique lines, unique branches, marginal lines, marginal branches, rank."""
    line_owners, branch_owners = defaultdict(set), defaultdict(set)
    for fid, (lines, branches) in per.items():
        for item in lines:
            line_owners[item].add(fid)
        for item in branches:
            branch_owners[item].add(fid)
    seen_l, seen_b, rows, remaining = set(), set(), {}, dict(per)
    rank = 0
    while remaining:
        # greedy: next the test case adding the most new lines, then branches, then id
        fid = min(remaining, key=lambda f: (-len(remaining[f][0] - seen_l), -len(remaining[f][1] - seen_b), f))
        lines, branches = remaining.pop(fid)
        rank += 1
        rows[fid] = (len(lines - seen_l), len(branches - seen_b), rank)
        seen_l |= lines
        seen_b |= branches
    result = []
    for fid in sorted(per):
        lines, branches = per[fid]
        unique_l = sum(1 for i in lines if len(line_owners[i]) == 1)
        unique_b = sum(1 for i in branches if len(branch_owners[i]) == 1)
        result.append((fid, len(lines), len(branches), unique_l, unique_b, *rows[fid]))
    return result


COVERAGE_HEADER = ["test_case", "lines", "branches", "unique_lines", "unique_branches", "marginal_lines",
                   "marginal_branches", "greedy_rank"]


def cmd_coverage(args) -> int:
    suite = Path(args.suite)
    cases = fixture_dirs(suite)
    if args.only:
        cases = [c for c in cases if any(fixture_id(c, suite).startswith(p) or fixture_id(c, suite) == p for p in args.only)]

    def progress(done, total, fid):
        print(f"[{done}/{total}] {fid}", file=sys.stderr)

    per = coverage(cases, args.runner, args.tool, suite, progress)
    rows = summarise(per)
    import io

    buf = io.StringIO()
    writer = csv.writer(buf, delimiter="\t", lineterminator="\n")
    writer.writerow(COVERAGE_HEADER)
    writer.writerows(rows)
    _emit(buf.getvalue(), args.out)
    return 0


def _emit(text: str, out) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
    else:
        sys.stdout.write(text)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("bugs", "candidates", "detection", "coverage"):
        p = sub.add_parser(name)
        p.add_argument("--out", help="write here instead of stdout")
        p.add_argument("--suite", default=str(ROOT), help="the suite root (default: this repository)")
        if name == "candidates":
            p.add_argument("--machine", required=True, help="a sillsdev/machine checkout")
            p.add_argument("--ref", default="HEAD", help="revision whose history is searched")
        if name == "detection":
            p.add_argument("--builds", required=True, help="builds file (JSON), see the module docstring")
            p.add_argument("--json", action="store_true", help="emit JSON instead of text")
        if name == "coverage":
            p.add_argument("--runner", required=True, help="path to the reference hc-conformance.dll")
            p.add_argument("--tool", default="dotnet-coverage", help="the dotnet-coverage executable")
            p.add_argument("--only", nargs="*", help="test case ids or id prefixes (a pilot)")
    args = parser.parse_args(argv)
    return {"bugs": cmd_bugs, "candidates": cmd_candidates, "detection": cmd_detection, "coverage": cmd_coverage}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
