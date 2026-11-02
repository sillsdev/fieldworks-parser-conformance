"""Shared helpers for the suite's checks. Standard library only; PyYAML is used when installed."""
import hashlib
import re
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
