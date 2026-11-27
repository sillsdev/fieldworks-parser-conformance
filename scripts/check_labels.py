#!/usr/bin/env python3
"""Check the behaviour-label vocabulary and that every word carries a label from it (ADR 0008; PROTOCOL.md section 14).

Fails when:
  - labels.tsv has a malformed line, a duplicate, a parent that is neither a construct nor an earlier line, or a
    checked_against entry that is not an existing label (the admission record every new label needs);
  - a child label is carried by no word (a label no word carries names nothing);
  - a word, a parse, or a generated_no_parse rule carries a label that is not in the vocabulary;
  - a word does not carry exactly one label (its own and its parses' together), or a generated_no_parse rule does not carry exactly one.
Variant runs repeat the default words and are not labelled. Needs PyYAML.
"""
import sys

from suite import LABEL_SEP, ROOT, child_labels, constructs, fixture_dirs, fixture_id, load_words, label_problem


def main() -> int:
    problems = []
    top = constructs()
    known = set(top)
    children = child_labels()
    if len(set(top)) != len(top):
        problems.append("constructs.txt lists a construct twice")
    for label, (checked, _) in children.items():
        parent = label.rsplit(LABEL_SEP, 1)[0] if LABEL_SEP in label else None
        if parent is None:
            problems.append(f"labels.tsv: {label!r} has no parent; a top-level label belongs in constructs.txt")
        elif parent not in known:
            problems.append(f"labels.tsv: {label!r}: parent {parent!r} is neither a construct nor an earlier line")
        for other in checked:
            if other not in known and other != label and other not in children:
                problems.append(f"labels.tsv: {label!r}: checked_against {other!r} is not an existing label")
        if parent is not None and checked and checked[0] != parent:
            problems.append(f"labels.tsv: {label!r}: checked_against must start with its parent")
        known.add(label)

    carried = set()
    words = 0

    def check(where, entry, what):
        for label in entry.get("exercises") or []:
            carried.add(label)
            if label not in known:
                problems.append(f"{where}: {what} carries {label!r}, which is not in constructs.txt or labels.tsv")

    for directory in fixture_dirs(ROOT):
        fid = fixture_id(directory)
        data = load_words(directory / "words.yaml")
        for word in data["words"]:
            words += 1
            check(fid, word, word["word"])
            for parse in word.get("parses") or []:
                check(fid, parse, f"{word['word']} {parse['signature']}")
            reason = label_problem(word)
            if reason:
                problems.append(f"{fid}: {word['word']} {reason}")
        for number, rule in enumerate(data.get("generated_no_parse") or []):
            check(fid, rule, f"generated_no_parse[{number}]")
            if len(rule.get("exercises") or []) != 1:
                problems.append(f"{fid}: generated_no_parse[{number}] must carry exactly one behaviour label")
    for label in children:
        if label not in carried:
            problems.append(f"labels.tsv: {label!r} is carried by no word")
    for problem in problems:
        print(problem)
    print(f"behaviour labels: {len(top)} constructs, {len(children)} child labels, {words} listed words, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
