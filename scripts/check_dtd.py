#!/usr/bin/env python3
"""Validate every grammar.xml (fixtures and stress) against HermitCrabInput.dtd.

Uses lxml when installed, otherwise xmllint. Grammars name the DTD as SYSTEM "HermitCrabInput.dtd";
the published copy at the repository root is the only DTD ever loaded, and no network access is made.

lxml validates against the published DTD whether or not the file declares it, so a grammar with no DOCTYPE
passes validation. Consumers that load the DTD from the declaration (machine's runner) reject such a file, so
this script also requires line 2 of every grammar to be the DOCTYPE line, read as plain text.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from suite import ROOT, STRESS_GROUP, fixture_dirs

try:
    from lxml import etree
except ImportError:
    etree = None


def grammars():
    dirs = fixture_dirs() + [d for d in sorted((ROOT / STRESS_GROUP).iterdir()) if (d / "grammar.xml").is_file()]
    return [d / "grammar.xml" for d in dirs]


DOCTYPE_EXAMPLE = '<!DOCTYPE HermitCrabInput SYSTEM "HermitCrabInput.dtd">'
DOCTYPE_LINE = re.compile(r'<!DOCTYPE HermitCrabInput SYSTEM "HermitCrabInput\.dtd"(\[\])?>')


def doctype_problems(files):
    problems = []
    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) < 2 or not DOCTYPE_LINE.fullmatch(lines[1]):
            problems.append(f"{path.relative_to(ROOT).as_posix()}:2: line 2 must be {DOCTYPE_EXAMPLE}")
    return problems


def with_lxml(files):
    dtd = etree.DTD(str(ROOT / "HermitCrabInput.dtd"))
    parser = etree.XMLParser(load_dtd=False, no_network=True, resolve_entities=False)
    problems = []
    for path in files:
        document = etree.parse(str(path), parser)
        if not dtd.validate(document):
            for entry in list(dtd.error_log)[:5]:
                problems.append(f"{path.relative_to(ROOT).as_posix()}:{entry.line}: {entry.message}")
    return problems


def with_xmllint(files):
    problems = []
    with tempfile.TemporaryDirectory() as scratch:
        shutil.copy(ROOT / "HermitCrabInput.dtd", scratch)
        for index, path in enumerate(files):
            copy = Path(scratch) / f"g{index}.xml"
            shutil.copy(path, copy)
            run = subprocess.run(
                ["xmllint", "--noout", "--nonet", "--valid", str(copy)], capture_output=True, text=True
            )
            if run.returncode != 0:
                problems.append(f"{path.relative_to(ROOT).as_posix()}: {run.stderr.strip()[:300]}")
    return problems


def main() -> int:
    files = grammars()
    problems = doctype_problems(files)
    if etree is not None:
        problems += with_lxml(files)
    elif shutil.which("xmllint"):
        problems += with_xmllint(files)
    else:
        sys.exit("neither lxml nor xmllint is available: pip install -r scripts/requirements.txt")
    for problem in problems:
        print(problem)
    print(f"dtd: {len(files)} grammars, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
