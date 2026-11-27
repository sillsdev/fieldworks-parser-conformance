"""The suite's one script: every check, the generator of derived files, and the exception report.

    python3 scripts/suite.py check                 run every check (this is what CI runs)
    python3 scripts/suite.py generate [--out DIR]  write the derived files: both manifests, coverage.csv, rules.csv
    python3 scripts/suite.py status [--strict]     list the rows of status.yaml by upstream state

Also the shared helpers the checks import. Standard library only; PyYAML is used when installed.
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_GROUPS = ("languages", "edge-cases")
STRESS_GROUP = Path("stress") / "edge-cases"

try:  # CI installs PyYAML; the fallback keeps the manifest tools usable without it.
    import yaml as _yaml
except ImportError:  # pragma: no cover - exercised only where PyYAML is absent
    _yaml = None


def read_text(path: Path) -> str:
    """UTF-8 text with a BOM stripped and line endings normalised to LF."""
    text = path.read_bytes().decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha256_text(path: Path) -> str:
    return hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()


def fixture_dirs(root: Path = ROOT, groups=FIXTURE_GROUPS):
    """Yield every fixture directory (one holding grammar.xml and words.yaml), sorted by id."""
    found = []
    for group in groups:
        base = root / group
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if (child / "grammar.xml").is_file() and (child / "words.yaml").is_file():
                found.append(child)
    return found


def fixture_id(directory: Path, root: Path = ROOT) -> str:
    return directory.relative_to(root).as_posix()


def have_yaml() -> bool:
    return _yaml is not None


def load_words(path: Path):
    """Return the parsed words.yaml (PyYAML required)."""
    if _yaml is None:
        raise RuntimeError("PyYAML is required: pip install -r scripts/requirements.txt")
    return _yaml.safe_load(read_text(path))


def words_summary(path: Path):
    """Return (language, case_count, expect_crash) for a words.yaml."""
    if _yaml is not None:
        data = load_words(path)
        return data["language"], len(data["words"]), bool(data.get("expect_crash", False))
    text = read_text(path)
    language = re.search(r"^language:\s*(.+?)\s*$", text, re.M).group(1).strip("\"'")
    crash = re.search(r"^expect_crash:\s*true\s*$", text, re.M) is not None
    count, in_words = 0, False
    for line in text.split("\n"):
        if re.match(r"^words:\s*$", line):
            in_words = True
            continue
        if in_words and re.match(r"^[A-Za-z_][\w-]*:", line):
            in_words = False
        if in_words and re.match(r"^\s*- word:", line):
            count += 1
    # The first `- word:` indent defines the top-level list; variants nest deeper but sit
    # under their own `words:` key inside `variants:`, which ends this block above.
    return language, count, crash


# Each check is a module with main() -> exit code; they stay runnable on their own.
CHECKS = (
    ("status.yaml is well formed", "exceptions"),
    ("words.yaml matches the schema", "check_words_schema"),
    ("derived files generate and their invariants hold", "check_derived"),
    ("grammar.xml matches the DTD", "check_dtd"),
    ("docs/grammars.md and stress/README.md list every test case", "check_grammars_md"),
    ("FieldWorks witnesses are well formed", "check_fwdata"),
    ("Calibration families are well formed", "check_calibration"),
    ("Relative links resolve", "check_links"),
    ("No private paths, emails or user names", "privacy_lint"),
)


def run_checks() -> int:
    import importlib

    failed = []
    for title, module in CHECKS:
        print(f"== {title}")
        sys.stdout.flush()
        if importlib.import_module(module).main():
            failed.append(title)
    print("== " + ("FAILED: " + "; ".join(failed) if failed else f"all {len(CHECKS)} checks passed"))
    return 1 if failed else 0


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="run every check")
    generate = sub.add_parser("generate", help="write the derived files")
    generate.add_argument("--out", default=str(ROOT / "generated"), help="directory to write into (default: generated/, untracked)")
    status = sub.add_parser("status", help="list status.yaml rows by upstream state")
    status.add_argument("--machine-checkout", help="a sillsdev/machine checkout, for engine ancestry")
    status.add_argument("--strict", action="store_true", help="exit 1 if any row needs action")
    args = parser.parse_args(argv)
    if args.command == "check":
        return run_checks()
    if args.command == "generate":
        import derive

        for name in derive.write_all(Path(args.out)):
            print(f"wrote {Path(args.out) / name}")
        return 0
    import exceptions

    return exceptions.report(args.machine_checkout, args.strict)


if __name__ == "__main__":
    sys.exit(main())
