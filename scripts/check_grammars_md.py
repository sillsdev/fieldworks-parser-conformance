#!/usr/bin/env python3
"""The fixture lists must name every fixture exactly once and nothing else.

docs/grammars.md lists each conformance fixture as "- `group/name`: ...". Its "Stress grammars" section
lists each stress fixture as "- `stress/edge-cases/name`: ...", and the table in stress/README.md has one
"| `name` |" row per stress fixture. Each list must match the directories on disk, and the counts the prose
states (the number of stress grammars, here and in docs/README.md, and "N of M stress fixtures carry a FieldWorks witness") must match
the disk. Every stress fixture must start `# kind: stress` and declare `fieldworks_producible: true`.

The XAmple subset is every grammar with no phonological features and no phonological rules, computed from
grammar.xml: no SymbolicFeature or ComplexFeature under PhonologicalFeatureSystem, no SegmentDefinition with a
FeatureValue, and no PhonologicalRule or MetathesisRule. The "Which engines run which grammars" section of
docs/grammars.md must list exactly that set (marking those whose words.yaml has a `morpher:` block), every
`[XAmple]` tag on a fixture line must agree, and the XAmple, Hermit Crab and PanGloss rows of the README table
must carry the right counts.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from suite import ROOT, STRESS_GROUP, fixture_dirs, fixture_id

LISTED = re.compile(r"^- `((?:languages|edge-cases)/[^`]+)`", re.M)
STRESS_LISTED = re.compile(r"^- `(stress/edge-cases/[^`]+)`", re.M)
STRESS_ROW = re.compile(r"^\| `([^`]+)` \|", re.M)
STRESS_HEADING = "## Stress grammars"
WITNESS_SENTENCE = re.compile(r"\*\*(\d+) of (\d+) stress fixtures carry a FieldWorks witness\*\*")


def compare(label: str, listed: list, on_disk: set, problems: list) -> None:
    for name in sorted(on_disk - set(listed)):
        problems.append(f"fixture not listed in {label}: {name}")
    for name in sorted(set(listed) - on_disk):
        problems.append(f"{label} lists a fixture that does not exist: {name}")
    for name in sorted({n for n in listed if listed.count(n) > 1}):
        problems.append(f"{label} lists {name} more than once")


def check_stress(grammars_md: str, problems: list) -> int:
    directories = fixture_dirs(groups=(STRESS_GROUP,))
    on_disk = {fixture_id(d) for d in directories}
    section = grammars_md.partition(STRESS_HEADING)[2]
    if not section:
        problems.append(f"docs/grammars.md has no '{STRESS_HEADING}' section")
    compare("docs/grammars.md (Stress grammars)", STRESS_LISTED.findall(section), on_disk, problems)
    readme = (ROOT / "stress" / "README.md").read_text(encoding="utf-8")
    rows = [f"stress/edge-cases/{name}" for name in STRESS_ROW.findall(readme)]
    compare("stress/README.md (table)", rows, on_disk, problems)
    stated = re.search(r"^The (\d+) grammars under `stress/`", section, re.M)
    if not stated or int(stated.group(1)) != len(on_disk):
        problems.append(f"docs/grammars.md must say 'The {len(on_disk)} grammars under `stress/`'")
    docs_readme = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    for pattern in (r"^stress/\s+(\d+) timing", r"^The (\d+) timing grammars in `stress/`"):
        said = re.search(pattern, docs_readme, re.M)
        if not said or int(said.group(1)) != len(on_disk):
            problems.append(f"docs/README.md must say {len(on_disk)} stress grammars (pattern {pattern!r})")
    witnesses = sum(1 for d in directories if (d / "fieldworks").is_dir())
    claim = WITNESS_SENTENCE.search(readme)
    if not claim:
        problems.append("stress/README.md must say '**N of M stress fixtures carry a FieldWorks witness**'")
    elif (int(claim.group(1)), int(claim.group(2))) != (witnesses, len(on_disk)):
        problems.append(
            f"stress/README.md says {claim.group(1)} of {claim.group(2)} stress fixtures carry a witness; "
            f"the disk has {witnesses} of {len(on_disk)}"
        )
    for d in directories:
        words = (d / "words.yaml").read_text(encoding="utf-8-sig")
        if not words.startswith("# kind: stress"):
            problems.append(f"{fixture_id(d)}/words.yaml must start with '# kind: stress'")
        if not re.search(r"^fieldworks_producible:\s*true\s*$", words, re.M):
            problems.append(f"{fixture_id(d)}/words.yaml must declare fieldworks_producible: true")
    return len(on_disk)


XAMPLE_HEADING = "## Which engines run which grammars"
XAMPLE_TAG = "[XAmple]"
MORPHER_NOTE = "(needs `morpher-settings`)"
SUBSET_ENTRY = re.compile(r"^- `((?:languages|edge-cases|stress/edge-cases)/[^`]+)`( \(needs `morpher-settings`\))?\s*$", re.M)
TAGGED_ENTRY = re.compile(r"^- `((?:languages|edge-cases|stress/edge-cases)/[^`]+)`: (\[XAmple\] )?", re.M)
README_XAMPLE_ROW = re.compile(r"^\| XAmple\b.*?\|\s*(\d+) conformance \+ (\d+) stress\b", re.M)
README_ALL_ROW = re.compile(r"^\| (Hermit Crab|PanGloss)\b.*?\|\s*all (\d+) \+ (\d+)\s*\|", re.M)


def split_section(text: str, heading: str) -> tuple:
    """Return (text without the section, the section body) for a '## ' heading."""
    start = text.find(heading + "\n")
    if start < 0:
        return text, ""
    end = text.find("\n## ", start + len(heading))
    end = len(text) if end < 0 else end + 1
    return text[:start] + text[end:], text[start + len(heading):end]


def xample_features_and_rules(grammar: Path) -> tuple:
    """(has phonological features, has phonological rules) for one grammar.xml."""
    root = ET.parse(grammar).getroot()
    features = any(
        feature.tag in ("SymbolicFeature", "ComplexFeature")
        for system in root.iter("PhonologicalFeatureSystem")
        for feature in system.iter()
    ) or any(segment.find(".//FeatureValue") is not None for segment in root.iter("SegmentDefinition"))
    rules = any(True for tag in ("PhonologicalRule", "MetathesisRule") for _ in root.iter(tag))
    return features, rules


def xample_subset(directories: list) -> dict:
    """fixture id -> needs morpher-settings, for every grammar in the XAmple subset."""
    subset = {}
    for d in directories:
        features, rules = xample_features_and_rules(d / "grammar.xml")
        if not features and not rules:
            words = (d / "words.yaml").read_text(encoding="utf-8-sig")
            subset[fixture_id(d)] = re.search(r"^morpher:", words, re.M) is not None
    return subset


def check_xample(text: str, problems: list) -> None:
    conformance = xample_subset(fixture_dirs())
    stress = xample_subset(fixture_dirs(groups=(STRESS_GROUP,)))
    expected = {**conformance, **stress}
    rest, section = split_section(text, XAMPLE_HEADING)
    if not section:
        problems.append(f"docs/grammars.md has no '{XAMPLE_HEADING}' section")
    listed = {}
    for name, note in SUBSET_ENTRY.findall(section):
        if name in listed:
            problems.append(f"XAmple subset list names {name} more than once")
        listed[name] = bool(note)
    for name in sorted(set(expected) - set(listed)):
        problems.append(f"XAmple subset list is missing {name} (no phonological features, no phonological rules)")
    for name in sorted(set(listed) - set(expected)):
        problems.append(f"XAmple subset list names {name}, but it has phonological features or rules")
    for name in sorted(set(listed) & set(expected)):
        if listed[name] != expected[name]:
            problems.append(
                f"XAmple subset list {'lacks' if expected[name] else 'wrongly adds'} the {MORPHER_NOTE} note on {name}"
            )
    said = re.search(r"\*\*(\d+) conformance grammars and (\d+) stress grammars\*\*", section)
    if section and (not said or (int(said.group(1)), int(said.group(2))) != (len(conformance), len(stress))):
        problems.append(
            f"docs/grammars.md must say '**{len(conformance)} conformance grammars and {len(stress)} stress grammars**' "
            "in the XAmple subset section"
        )
    tagged = {n for n, tag in TAGGED_ENTRY.findall(rest) if tag}
    for name in sorted(set(expected) - tagged):
        problems.append(f"fixture line for {name} lacks the {XAMPLE_TAG} tag")
    for name in sorted(tagged - set(expected)):
        problems.append(f"fixture line for {name} carries {XAMPLE_TAG} but it has phonological features or rules")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    row = README_XAMPLE_ROW.search(readme)
    if not row:
        problems.append("README.md table needs an XAmple row ending 'N conformance + N stress'")
    elif (int(row.group(1)), int(row.group(2))) != (len(conformance), len(stress)):
        problems.append(
            f"README.md XAmple row says {row.group(1)} conformance + {row.group(2)} stress; "
            f"the grammars say {len(conformance)} + {len(stress)}"
        )
    all_conformance, all_stress = len(fixture_dirs()), len(fixture_dirs(groups=(STRESS_GROUP,)))
    rows = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in README_ALL_ROW.finditer(readme)}
    for engine in ("Hermit Crab", "PanGloss"):
        if engine not in rows:
            problems.append(f"README.md table needs a '{engine}' row whose last cell is 'all N + N'")
        elif rows[engine] != (all_conformance, all_stress):
            problems.append(f"README.md {engine} row says all {rows[engine][0]} + {rows[engine][1]}; the disk has {all_conformance} + {all_stress}")


NUMBERS_LINE = re.compile(
    r"\*\*(\d+) conformance grammars\*\* \((\d+) languages, (\d+) edge cases\)"
    r".*?\*\*(\d+) stress grammars\*\*.*?\*\*(\d+) FieldWorks witnesses\*\*"
)


def check_readme_numbers(problems: list) -> None:
    """The numbers line of the root README must match the disk."""
    conformance = fixture_dirs()
    groups = [fixture_id(d).split("/")[0] for d in conformance]
    stress = fixture_dirs(groups=(STRESS_GROUP,))
    actual = (
        len(conformance),
        groups.count("languages"),
        groups.count("edge-cases"),
        len(stress),
        sum(1 for d in conformance + stress if (d / "fieldworks").is_dir()),
    )
    line = NUMBERS_LINE.search((ROOT / "README.md").read_text(encoding="utf-8"))
    if not line:
        problems.append(
            "README.md needs a numbers line: '**N conformance grammars** (N languages, N edge cases) "
            "· **N stress grammars** · **N FieldWorks witnesses**'"
        )
        return
    said = tuple(int(n) for n in line.groups())
    if said != actual:
        labels = ("conformance grammars", "languages", "edge cases", "stress grammars", "FieldWorks witnesses")
        for label, s, a in zip(labels, said, actual):
            if s != a:
                problems.append(f"README.md numbers line says {s} {label}; the disk has {a}")


def main() -> int:
    text = (ROOT / "docs" / "grammars.md").read_text(encoding="utf-8")
    listed = LISTED.findall(split_section(text, XAMPLE_HEADING)[0])
    on_disk = {fixture_id(d) for d in fixture_dirs()}
    problems = []
    compare("docs/grammars.md", listed, on_disk, problems)
    stress = check_stress(text, problems)
    check_xample(text, problems)
    check_readme_numbers(problems)
    for problem in problems:
        print(problem)
    print(
        f"grammars.md: {len(listed)} entries, {len(on_disk)} fixtures; "
        f"{stress} stress fixtures; {len(problems)} problems"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
