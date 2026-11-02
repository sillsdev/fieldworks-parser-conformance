#!/usr/bin/env python3
"""Write or check generated/hc-conformance-manifest.v2.json and generated/stress-manifest.v2.json.

The manifests record paths and hashes only; words.yaml and grammar.xml stay the ground truth.
Paths are relative to the root of this repository, with no leading directory name.
Hashes are SHA-256 of UTF-8 text with a BOM stripped and CR/CRLF normalised to LF.
The stress manifest lists the fixtures under stress/edge-cases/ in the same layout. It is a separate file
so the conformance manifest, which consumers import and pin, does not change when a stress fixture does.

    python3 scripts/generate_manifest.py            write both manifests
    python3 scripts/generate_manifest.py --check    exit 1 if either checked-in file is stale
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from suite import FIXTURE_GROUPS, ROOT, STRESS_GROUP, fixture_dirs, fixture_id, sha256_text, words_summary

FORMAT = "hc-conformance-manifest/v2"
WORDS_FORMAT = "hc-conformance-words/v1"
GRAMMAR_FORMAT = "sil-machine-hermit-crab-input-xml/v1"
DTD = "HermitCrabInput.dtd"
OUTPUT = "generated/hc-conformance-manifest.v2.json"
STRESS_FORMAT = "hc-conformance-stress-manifest/v2"
STRESS_OUTPUT = "generated/stress-manifest.v2.json"
ADDITIONAL_SOURCE_FILES = (
    "constructs.txt",
    "parity-check.py",
    "schema/words.schema.json",
    "schema/conformance-manifest.schema.json",
)


def build(
    root: Path = ROOT,
    fmt: str = FORMAT,
    prefix: str = "",
    dtd: str = DTD,
    groups=FIXTURE_GROUPS,
    sources=ADDITIONAL_SOURCE_FILES,
) -> dict:
    dtd_path = prefix + dtd
    dtd_hash = sha256_text(root / dtd)
    fixtures = []
    for directory in fixture_dirs(root, groups):
        fid = fixture_id(directory, root)
        language, cases, crash = words_summary(directory / "words.yaml")
        if crash and cases != 1:
            raise SystemExit(f"{fid}: expect_crash fixtures must hold exactly one case, found {cases}")
        fixtures.append(
            {
                "caseCount": cases,
                "category": "stress"
                if fid.startswith("stress/")
                else "language"
                if fid.startswith("languages/")
                else "edge-case",
                "displayLanguage": language,
                "expectedCrash": crash,
                "fixtureId": fid,
                "grammarPath": f"{prefix}{fid}/grammar.xml",
                "grammarSha256": sha256_text(directory / "grammar.xml"),
                "wordsPath": f"{prefix}{fid}/words.yaml",
                "wordsSha256": sha256_text(directory / "words.yaml"),
            }
        )
    fixtures.sort(key=lambda f: f["fixtureId"].encode("utf-8"))
    text = [fmt, "\n", dtd_path, "\0", dtd_hash, "\n"]
    for f in fixtures:
        text += [f["fixtureId"], "\0", f["grammarSha256"], "\0", f["wordsSha256"], "\n"]
    for relative in sorted(sources):
        path = root / relative
        text += [prefix + relative, "\0", sha256_text(path) if path.is_file() else "<absent>", "\n"]
    source_hash = hashlib.sha256("".join(text).encode("utf-8")).hexdigest()
    return {
        "dtdPath": dtd_path,
        "dtdSha256": dtd_hash,
        "fixtures": fixtures,
        "formatVersion": fmt,
        "grammarFormatVersion": GRAMMAR_FORMAT,
        "sourceHash": source_hash,
        "wordsAuthoringFormatVersion": WORDS_FORMAT,
    }


def serialize(manifest: dict) -> bytes:
    return (json.dumps(manifest, separators=(",", ":"), sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def stress_build() -> dict:
    return build(fmt=STRESS_FORMAT, groups=(STRESS_GROUP,), sources=("schema/words.schema.json",))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if a checked-in manifest is stale")
    args = parser.parse_args()
    stale = False
    for output, manifest in ((OUTPUT, build()), (STRESS_OUTPUT, stress_build())):
        fresh = serialize(manifest)
        count = len(manifest["fixtures"])
        target = ROOT / output
        if args.check:
            current = target.read_bytes() if target.is_file() else b""
            if current != fresh:
                print(f"{output} is stale: run python3 scripts/generate_manifest.py and commit the result")
                stale = True
            else:
                print(f"{output} is fresh: {count} fixtures")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(fresh)
        print(f"wrote {output}: {count} fixtures")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
