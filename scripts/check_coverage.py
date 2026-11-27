#!/usr/bin/env python3
"""Check coverage.csv and rules.csv against the fixtures' words.yaml and grammar.xml.

The two ledgers are written by a consuming engine's coverage report (sillsdev/machine's runner). This
script re-derives what it can from the files in this repository, so a changed fixture whose ledger rows
went stale fails here and not only in the engine's CI.

  coverage.csv  one row per (language, word, parse signature, exercises tag); a word with no parse has an
                empty signature. Compared as a multiset, so the file must match exactly.
  rules.csv     one row per (language, rule id) with the words whose parses name the rule in `rules` and,
                prefixed with `!`, the words that name it in `blocked_by`, joined with `;`. Every row with
                words must match exactly. A row with no words is a rule declared on purpose and exercised by
                no word; its id must exist in a grammar.xml of that language (several fixtures can share a
                language name, so whether another fixture's word names it is not checked).
                Which unexercised rules a grammar declares is the engine's to say, so that half is not derived.

Standard library plus PyYAML. Exits 1 on any difference. Usage: python3 scripts/check_coverage.py
"""
import csv
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

from suite import ROOT, fixture_dirs, load_words

LIMIT = 8


def derive():
    coverage = Counter()
    rules = Counter()
    ids = defaultdict(set)  # language -> every id attribute in its grammars
    for d in fixture_dirs():
        words = load_words(d / "words.yaml")
        lang = words["language"]
        for el in ET.parse(d / "grammar.xml").getroot().iter():
            if el.get("id"):
                ids[lang].add(el.get("id"))
        by_rule = defaultdict(list)
        for case in words["words"]:
            tags = case.get("exercises") or []
            parses = case.get("parses") or []
            if parses:
                for p in parses:
                    for t in p.get("exercises") or tags:
                        coverage[(lang, case["word"], p["signature"], t)] += 1
                    for r in p.get("rules") or []:
                        by_rule[r].append(case["word"])
            else:
                for t in tags:
                    coverage[(lang, case["word"], "", t)] += 1
            for r in case.get("blocked_by") or []:
                by_rule[r].append("!" + case["word"])
        for r, ws in by_rule.items():
            rules[(lang, r, ";".join(dict.fromkeys(ws)))] += 1
    return coverage, rules, ids


def read(name):
    with open(ROOT / name, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def report(name, extra, missing, problems):
    for label, counter in (("in the file but not derived from words.yaml", extra),
                           ("derived from words.yaml but not in the file", missing)):
        if counter:
            problems.append(f"{name}: {sum(counter.values())} row(s) {label}")
            for row in list(counter)[:LIMIT]:
                problems.append("    " + ",".join(row))


def main():
    coverage, rules, ids = derive()
    problems = []

    cov_rows = Counter(tuple(r) for r in read("coverage.csv")[1:])
    report("coverage.csv", cov_rows - coverage, coverage - cov_rows, problems)

    rule_rows = read("rules.csv")[1:]
    with_words = Counter(tuple(r) for r in rule_rows if r[2])
    report("rules.csv", with_words - rules, rules - with_words, problems)
    for lang, rule, words in rule_rows:
        if not words:
            if rule not in ids[lang]:
                problems.append(f"rules.csv: {lang},{rule} has no words and no such id in the language's grammar.xml")

    if problems:
        print("check_coverage: FAIL (regenerate the ledgers with the engine's coverage report)")
        print("\n".join(problems))
        return 1
    print(f"check_coverage: ok ({sum(coverage.values())} coverage rows, {len(rule_rows)} rule rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
