#!/usr/bin/env python3
"""The fixture lists must name every fixture exactly once and nothing else.

docs/grammars.md lists each conformance fixture as "- `group/name`: ...". Its "Stress grammars" section
lists each stress fixture as "- `stress/edge-cases/name`: ...", and the table in stress/README.md has one
"| `name` |" row per stress fixture. Each list must match the directories on disk, and the counts the prose
states (the number of stress grammars, here and in docs/README.md, and "N of M stress fixtures carry a FieldWorks witness") must match
the disk. Every stress fixture must start `# kind: stress` and declare `fieldworks_producible: true`.
"""
import re
import sys

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
    listed = LISTED.findall(text)
    on_disk = {fixture_id(d) for d in fixture_dirs()}
    problems = []
    compare("docs/grammars.md", listed, on_disk, problems)
    stress = check_stress(text, problems)
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
