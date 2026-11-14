#!/usr/bin/env python3
"""Measure parser cost per word with the PanGloss release binary.

  measure.py <grammar.xml> <words.txt> <out.tsv> [extra pangloss args]

Runs `pangloss batch ... --cost-column --threads 1` and writes `word<TAB>len<TAB>status<TAB>cost<TAB>parses`
sorted by cost. The cost column is the engine's fixed-weight prediction of parse instructions; it is
the measure the calibration ladders are built on, not wall-clock time.
"""
import os
import subprocess
import sys

PANGLOSS = os.environ.get("PANGLOSS", "pangloss")


def run(grammar, words, raw, extra=()):
    subprocess.run([PANGLOSS, "batch", grammar, words, raw, "--cost-column", "--threads", "1", "--word-timeout-ms", os.environ.get("WORD_TIMEOUT_MS", "20000"), *extra],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rows = []
    for line in open(raw, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) >= 7 and f[3] in ("ok", "SKIPPED", "CAP", "TIMEOUT") or (len(f) >= 5 and f[3] != "STARTED"):
            sig = f[4]
            cost = int(f[-1]) if f[-1].isdigit() else -1
            rows.append((f[1], len(f[1]), f[3], cost, 0 if sig == "-" else sig.count(";") + 1))
    return rows


if __name__ == "__main__":
    rows = run(sys.argv[1], sys.argv[2], sys.argv[3] + ".raw", sys.argv[4:])
    rows.sort(key=lambda r: r[3])
    with open(sys.argv[3], "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")
    for r in rows:
        print("\t".join(map(str, r)))
