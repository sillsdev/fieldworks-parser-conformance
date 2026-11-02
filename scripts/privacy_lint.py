#!/usr/bin/env python3
"""Fail on private material in any file of this public repository.

Looks for: email addresses; home-directory and drive paths (Linux /home/<user>, macOS /Users/<user>,
Windows C:\\Users\\<user>, WSL /mnt/<drive>/); and any extra literal strings listed in the environment
variable PRIVACY_LINT_EXTRA (comma separated, case-insensitive), which is how a maintainer adds a
login or a project name without writing it into this file. Findings print file and line only, never
the matched text. Standard library only.
"""
import os
import re
import sys

from suite import ROOT

PATTERNS = {
    "email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    "linux home path": re.compile(r"(?<![\w.])/home/[A-Za-z0-9_.-]+"),
    "macos home path": re.compile(r"(?<![\w.])/Users/[A-Za-z0-9_.-]+"),
    "windows user path": re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}[^\\\s\"'`<>]+", re.I),
    "wsl or drive mount path": re.compile(r"(?<![\w.])/mnt/[a-z](?:/|\b)"),
    "windows repo path": re.compile(r"[A-Za-z]:\\{1,2}(?:repos|Documents)\\", re.I),
}
SKIP_DIRS = {".git", "__pycache__"}


def extra_terms():
    raw = os.environ.get("PRIVACY_LINT_EXTRA", "")
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


def main() -> int:
    extras = extra_terms()
    findings, scanned = [], 0
    for directory, subdirs, files in os.walk(ROOT):
        subdirs[:] = [d for d in subdirs if d not in SKIP_DIRS]
        for name in files:
            path = os.path.join(directory, name)
            relative = os.path.relpath(path, ROOT).replace(os.sep, "/")
            scanned += 1
            with open(path, "rb") as handle:
                text = handle.read().decode("utf-8", errors="replace")
            for number, line in enumerate(text.splitlines(), 1):
                for label, pattern in PATTERNS.items():
                    if pattern.search(line):
                        findings.append(f"{relative}:{number}: {label}")
                lowered = line.lower()
                for term in extras:
                    if term in lowered:
                        findings.append(f"{relative}:{number}: configured term")
    for finding in findings:
        print(finding)
    print(f"privacy lint: {scanned} files, {len(findings)} findings, {len(extras)} extra terms configured")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
