#!/usr/bin/env python3
"""Pick the ladder words for one family from measured candidates.

  pick_words.py <family> <work-dir> [--n N] [--seeds a,b,c]

Writes <work-dir>/grammar.xml, candidates.txt, measured.tsv and ladder.tsv. The ladder is the cheapest
word that parses (1x) plus the candidate nearest to 4x, 16x, 64x and 256x of it, plus the dearest
word with no analysis (the wasted search). Ties are broken toward a spread of word lengths.
"""
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure  # noqa: E402

RUNGS = [1, 4, 16, 64, 256]
MAXPARSES = 220      # keep words.yaml readable: a rung never needs more analyses than this


def mutants(word, rnd, k):
    out = set()
    for _ in range(k * 4):
        w = word
        op = rnd.choice(["dup", "dup", "swap", "sub", "drop"])
        i = 2 * rnd.randrange(max(1, len(w) // 2))
        j = 2 * rnd.randrange(max(1, len(w) // 2))
        if op == "dup":
            w = w[:i] + w[i:i + 2] + w[i:]
        elif op == "swap":
            w = w[:i] + w[j:j + 2] + w[i + 2:]
        elif op == "sub":
            w = w[:i] + w[j:j + 2] + w[i + 2:]
        else:
            w = w[:i] + w[i + 2:]
        if 5 <= len(w) <= 40:
            out.add(w)
        if len(out) >= k:
            break
    return list(out)


def climb(work, rows, target, rounds):
    """Local search toward the top rung: mutate the dearest parsing words, keep what the engine measures."""
    import random
    rnd = random.Random(7)
    seen = {r[0] for r in rows}
    for _ in range(rounds):
        ok = [r for r in rows if 0 < r[4] <= MAXPARSES and 5 <= r[1] <= 40]
        # the words closest to the target from either side seed the next round
        seeds = sorted(ok, key=lambda r: abs(math.log(r[3] / target)))[:12]
        new = []
        for r in seeds:
            new += [m for m in mutants(r[0], rnd, 40) if m not in seen]
        new = list(dict.fromkeys(new))
        if not new:
            break
        seen.update(new)
        (work / "climb.txt").write_text("\n".join(new) + "\n")
        got = measure.run(str(work / "grammar.xml"), str(work / "climb.txt"), str(work / "climb.raw"))
        rows += [r for r in got if r[2] == "ok" and r[3] > 0]
        rows.sort(key=lambda r: r[3])
    ok = [r for r in rows if 0 < r[4] <= MAXPARSES and 5 <= r[1] <= 40]
    return rows, ok


def main():
    fam, work = sys.argv[1], Path(sys.argv[2])
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 400
    seeds = sys.argv[sys.argv.index("--seeds") + 1].split(",") if "--seeds" in sys.argv else ["1", "2", "3"]
    work.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(HERE / "calib_b_gen.py"), "grammar", fam, str(work)], check=True)
    words = []
    for sd in seeds:
        out = subprocess.run([sys.executable, str(HERE / "calib_b_gen.py"), "candidates", fam, str(n), sd, str(work)], check=True, capture_output=True, text=True).stdout.split()
        words += [w for w in out if w not in words]
    (work / "candidates.txt").write_text("\n".join(words) + "\n")
    rows = measure.run(str(work / "grammar.xml"), str(work / "candidates.txt"), str(work / "raw.tsv"))
    rows = [r for r in rows if r[2] == "ok" and r[3] > 0]
    rows.sort(key=lambda r: r[3])
    with open(work / "measured.tsv", "w") as fh:
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")
    ok = [r for r in rows if 0 < r[4] <= MAXPARSES and 5 <= r[1] <= 40]
    base = ok[0][3]
    if "--climb" in sys.argv:
        rows, ok = climb(work, rows, base * 256, int(sys.argv[sys.argv.index("--climb") + 1]))
    chosen, used = [], set()
    for k in RUNGS:
        tgt = base * k
        best = min((r for r in ok if r[0] not in used), key=lambda r: abs(math.log(r[3] / tgt)))
        used.add(best[0])
        chosen.append((f"{k}x", best))
    bad = [r for r in rows if r[4] == 0 and 5 <= r[1] <= 40]
    if bad:
        chosen.append(("wasted", bad[-1]))
    with open(work / "ladder.tsv", "w") as fh:
        for tag, r in chosen:
            fh.write("\t".join([tag, r[0], str(r[1]), str(r[3]), str(r[4])]) + "\n")
            print(tag, r[0], r[1], r[3], r[4])


if __name__ == "__main__":
    main()
