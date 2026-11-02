#!/usr/bin/env python3
"""Check relative links in every Markdown file of the suite.

A link is `[text](target)`. Targets with a URL scheme are not fetched; only
relative targets are resolved, and a `#anchor` into a Markdown file must match
a heading there (GitHub slug rules, simplified). Exits 1 if any link is broken.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def slug(heading: str) -> str:
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def anchors(path: Path) -> set:
    found, seen, in_fence = set(), {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        if in_fence:
            continue
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            base = slug(m.group(1))
            n = seen.get(base, 0)
            seen[base] = n + 1
            found.add(base if n == 0 else f"{base}-{n}")
    return found


def markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.relative_to(root).parts:
            continue
        yield path


def main() -> int:
    broken, checked = [], 0
    for md in markdown_files(ROOT):
        in_fence = False
        for number, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
            if in_fence:
                continue
            line = re.sub(r"`[^`]*`", "", line)
            for target in LINK.findall(line):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                checked += 1
                file_part, _, anchor = target.partition("#")
                dest = (md.parent / file_part).resolve() if file_part else md
                rel = md.relative_to(ROOT)
                if not dest.exists():
                    broken.append(f"{rel}:{number}: missing target {target}")
                elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                    broken.append(f"{rel}:{number}: no heading for #{anchor} in {target}")
    for item in broken:
        print(item)
    print(f"link check: {checked} relative links, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
