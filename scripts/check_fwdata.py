#!/usr/bin/env python3
"""Check the shape of every fieldworks/ witness directory, in fixtures and stress (PROTOCOL.md section 10).

Structural only: the directory holds exactly project.fwdata, phonology-mutations.yaml and
WritingSystemStore/*.ldml; the fixture is fieldworks_producible: true; phonology-mutations.yaml is
version 1 and its base_sha256 equals the SHA-256 of the exact bytes of project.fwdata; and
project.fwdata and every .ldml are well-formed XML.

Freshness (issue #2): fieldworks-witness-grammars.tsv records the SHA-256 of the grammar.xml each witness was
authored against (text, line endings normalised, as the manifest hashes it), and it must still match. A witness
not listed there must be listed in fieldworks-stale-witnesses.tsv; a witness in both files, or a row whose fixture
has no witness, is a stale row. (The hash is not in phonology-mutations.yaml: its key vocabulary is v1 and
sillsdev/machine's gate rejects any other key.) Each .ldml must be minimal: only the six top-level elements that define a
writing system and at most LDML_MAX_BYTES. Standard library only.
"""
import hashlib
import re
import sys
import xml.etree.ElementTree as ET

from suite import ROOT, STRESS_GROUP, fixture_dirs, fixture_id, sha256_text

STALE_FILE = ROOT / "fieldworks-stale-witnesses.tsv"
HASH_FILE = ROOT / "fieldworks-witness-grammars.tsv"
LDML_ELEMENTS = {"identity", "layout", "characters", "delimiters", "collations", "special"}
LDML_MAX_BYTES = 65536


def read_table(path):
    """Tab-separated rows (comment lines skipped) as {first column: second column}."""
    if not path.is_file():
        return {}
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            first, _, rest = line.partition("\t")
            rows[first.strip()] = rest.strip()
    return rows


def main() -> int:
    problems, checked = [], 0
    stale = set(read_table(STALE_FILE))
    hashes = read_table(HASH_FILE)
    seen = set()
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
                tree = ET.parse(item)
            except ET.ParseError as error:
                problems.append(f"{item.relative_to(ROOT).as_posix()}: not well-formed XML: {error}")
                continue
            ldml = item.relative_to(ROOT).as_posix()
            extra = sorted({child.tag for child in tree.getroot()} - LDML_ELEMENTS)
            if extra:
                problems.append(f"{ldml}: not minimal, unexpected top-level elements {extra}")
            if item.stat().st_size > LDML_MAX_BYTES:
                problems.append(f"{ldml}: {item.stat().st_size} bytes exceeds the {LDML_MAX_BYTES} byte minimal-LDML limit")
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
        fixture = fixture_id(directory)
        seen.add(fixture)
        recorded = hashes.get(fixture)
        if recorded:
            current = sha256_text(directory / "grammar.xml")
            if recorded != current:
                problems.append(f"{name}: {HASH_FILE.name} has {recorded[:12]}... but grammar.xml is {current[:12]}...; "
                                "the witness is stale, regenerate it (do not just update the hash)")
            if fixture in stale:
                problems.append(f"{fixture}: listed in both {STALE_FILE.name} and {HASH_FILE.name}; keep one row")
        elif fixture not in stale:
            problems.append(f"{fixture}: no row in {HASH_FILE.name} or {STALE_FILE.name}")
    for table, rows in ((STALE_FILE, stale), (HASH_FILE, set(hashes))):
        for fixture in sorted(rows - seen):
            problems.append(f"{table.name}: {fixture} has no witness; delete the row")
    for problem in problems:
        print(problem)
    print(f"fwdata: {checked} witness directories, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
