#!/usr/bin/env python3
"""Check the shape of every fieldworks/ witness directory, in fixtures and stress (PROTOCOL.md section 10).

Structural only: the directory holds exactly project.fwdata, phonology-mutations.yaml and
WritingSystemStore/*.ldml; the fixture is fieldworks_producible: true; phonology-mutations.yaml is
version 1 and its base_sha256 equals the SHA-256 of the exact bytes of project.fwdata; and
project.fwdata and every .ldml are well-formed XML. Standard library only.
"""
import hashlib
import re
import sys
import xml.etree.ElementTree as ET

from suite import ROOT, STRESS_GROUP, fixture_dirs


def main() -> int:
    problems, checked = [], 0
    for directory in fixture_dirs() + fixture_dirs(groups=(STRESS_GROUP,)):
        witness = directory / "fieldworks"
        if not witness.is_dir():
            continue
        checked += 1
        name = witness.relative_to(ROOT).as_posix()
        entries = sorted(p.name for p in witness.iterdir())
        if entries != ["WritingSystemStore", "phonology-mutations.yaml", "project.fwdata"]:
            problems.append(f"{name}: unexpected contents {entries}")
            continue
        words = (directory / "words.yaml").read_text(encoding="utf-8-sig")
        if not re.search(r"^fieldworks_producible:\s*true\s*$", words, re.M):
            problems.append(f"{name}: the fixture is not fieldworks_producible: true")
        store = witness / "WritingSystemStore"
        for item in sorted(store.iterdir()):
            if item.suffix != ".ldml":
                problems.append(f"{name}/WritingSystemStore: only .ldml files are allowed, found {item.name}")
                continue
            try:
                ET.parse(item)
            except ET.ParseError as error:
                problems.append(f"{item.relative_to(ROOT).as_posix()}: not well-formed XML: {error}")
        project = witness / "project.fwdata"
        try:
            ET.parse(project)
        except ET.ParseError as error:
            problems.append(f"{name}/project.fwdata: not well-formed XML: {error}")
        manifest = (witness / "phonology-mutations.yaml").read_text(encoding="utf-8-sig")
        if not re.search(r"^version:\s*1\s*$", manifest, re.M):
            problems.append(f"{name}/phonology-mutations.yaml: version must be 1")
        declared = re.search(r"^base_sha256:\s*([0-9a-f]{64})\s*$", manifest, re.M)
        actual = hashlib.sha256(project.read_bytes()).hexdigest()
        if not declared:
            problems.append(f"{name}/phonology-mutations.yaml: base_sha256 missing")
        elif declared.group(1) != actual:
            problems.append(f"{name}: base_sha256 {declared.group(1)[:12]}... != project.fwdata {actual[:12]}...")
    for problem in problems:
        print(problem)
    print(f"fwdata: {checked} witness directories, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
